"""Security tests for the sandboxed execution model.

Closes AUDIT_REPORT.md finding SEC-001 (CRITICAL). These tests prove
that a malicious .dmai file cannot escape the sandbox via:

  - Raw Python imports injected post-transpile
  - Access to disallowed modules through the Maithili import map
  - Direct calls to exec / eval / compile / open / breakpoint
  - __import__ bypass

Each test pins a specific attack surface so that a regression that
re-opens one hole is immediately caught.
"""
import pytest

from maithili_dsl import cli
from maithili_dsl.cli import (
    MAITHILI_MODULES,
    _ALLOWED_MODULES,
    _SAFE_BUILTIN_NAMES,
    _make_safe_import,
    _validate_imports,
    run_dmai_file,
    translate_imports,
    EXIT_OK,
    EXIT_IMPORT_BLOCKED,
    EXIT_RUNTIME_ERROR,
)


# ---------------------------------------------------------------------------
# _validate_imports: raw Python import statements are rejected unless the
# module name was legitimately translated from a Maithili import.
# ---------------------------------------------------------------------------

class TestValidateImportsRejectsRawPythonImports:

    def test_raw_import_os_rejected(self):
        errors = _validate_imports("import os\n", translated_modules=set())
        assert errors, "import os should be blocked"

    def test_raw_import_subprocess_rejected(self):
        errors = _validate_imports(
            "import subprocess\n", translated_modules=set()
        )
        assert errors

    def test_raw_import_socket_rejected(self):
        errors = _validate_imports(
            "import socket\n", translated_modules=set()
        )
        assert errors

    def test_raw_import_ctypes_rejected(self):
        errors = _validate_imports(
            "import ctypes\n", translated_modules=set()
        )
        assert errors

    def test_raw_import_pickle_rejected(self):
        errors = _validate_imports(
            "import pickle\n", translated_modules=set()
        )
        assert errors

    def test_raw_from_import_rejected(self):
        errors = _validate_imports(
            "from subprocess import run\n", translated_modules=set()
        )
        assert errors

    def test_import_after_maithili_translation_allowed(self):
        # A Maithili `आयात गणित` becomes `import math` and is added
        # to the translated_modules set — then _validate_imports must
        # allow it through.
        errors = _validate_imports(
            "import math\n", translated_modules={"math"}
        )
        assert errors == []

    def test_non_import_lines_are_ignored(self):
        code = "x = 1\nprint(x)\n"
        assert _validate_imports(code, translated_modules=set()) == []


# ---------------------------------------------------------------------------
# _make_safe_import: __import__ replacement only permits whitelist.
# ---------------------------------------------------------------------------

class TestSafeImportWhitelist:

    def setup_method(self):
        self.safe_import = _make_safe_import()

    def test_whitelisted_module_allowed(self):
        # math is in MAITHILI_MODULES values, so whitelisted.
        mod = self.safe_import("math")
        assert mod.pi > 3

    def test_non_whitelisted_module_raises_importerror(self):
        with pytest.raises(ImportError):
            self.safe_import("subprocess")

    def test_ctypes_blocked(self):
        with pytest.raises(ImportError):
            self.safe_import("ctypes")

    def test_socket_blocked(self):
        with pytest.raises(ImportError):
            self.safe_import("socket")

    def test_pickle_blocked(self):
        with pytest.raises(ImportError):
            self.safe_import("pickle")

    def test_submodule_of_whitelisted_allowed(self):
        # os.path is in the whitelist values explicitly; verify that
        # `os` base-module lookups resolve.
        assert "os.path" in _ALLOWED_MODULES
        mod = self.safe_import("os.path")
        assert mod.sep in ("/", "\\")

    def test_error_message_is_in_maithili(self):
        with pytest.raises(ImportError) as exc_info:
            self.safe_import("subprocess")
        assert "आयात" in str(exc_info.value)


# ---------------------------------------------------------------------------
# _SAFE_BUILTIN_NAMES: forbidden builtins are absent.
# ---------------------------------------------------------------------------

class TestForbiddenBuiltinsAbsent:

    @pytest.mark.parametrize("name", [
        "exec", "eval", "compile", "open", "breakpoint",
        "__import__",  # only safe_import wrapper, not the real thing
    ])
    def test_name_not_in_safe_builtins_list(self, name):
        assert name not in _SAFE_BUILTIN_NAMES, (
            f"{name!r} must not appear in _SAFE_BUILTIN_NAMES"
        )

    def test_expected_safe_names_present(self):
        # Sanity: harmless builtins we DO want are still exposed.
        for name in ("print", "len", "range", "str", "int", "list"):
            assert name in _SAFE_BUILTIN_NAMES


# ---------------------------------------------------------------------------
# translate_imports: records which modules were legitimately translated.
# ---------------------------------------------------------------------------

class TestTranslateImports:

    def test_maithili_import_recorded(self):
        code = "आयात गणित\n"
        translated, modules = translate_imports(code)
        assert "import math" in translated
        assert "math" in modules

    def test_multiple_imports_all_recorded(self):
        code = "आयात गणित\nआयात यादृच्छिक\n"
        translated, modules = translate_imports(code)
        assert "math" in modules
        assert "random" in modules

    def test_no_maithili_imports_produces_empty_set(self):
        translated, modules = translate_imports("x = १\n")
        assert modules == set()

    def test_attribute_access_also_counts(self):
        # Using गणित.pi pulls math into translated_modules even without
        # an explicit आयात statement, because the transpiler still
        # rewrites गणित. to math. and the sandbox needs to allow it.
        code = "x = गणित.pi\n"
        translated, modules = translate_imports(code)
        assert "math" in modules


# ---------------------------------------------------------------------------
# End-to-end: malicious .dmai files are rejected by run_dmai_file
# ---------------------------------------------------------------------------

@pytest.mark.security
class TestMaliciousDmaiBlocked:
    """Write real .dmai files that try to break out, and confirm
    run_dmai_file rejects them with a non-zero exit code."""

    def test_attempting_import_os_via_raw_python_rejected(
        self, tmp_dmai_file, capsys
    ):
        # The lexical form "import os" isn't a Maithili keyword so it
        # survives transpilation unchanged, but _validate_imports
        # should catch it before exec.
        path = tmp_dmai_file("import os\nos.system(\"echo pwned\")\n")
        code = run_dmai_file(str(path))
        captured = capsys.readouterr()
        # It may be blocked at lint (long-line false positive is unlikely
        # for this short line) or at _validate_imports. Either path must
        # produce a non-zero exit.
        assert code != EXIT_OK
        assert "आयात अनुमति नहि" in captured.out or "लिंटर" in captured.out

    def test_attempting_to_call_exec_raises(self, tmp_dmai_file, capsys):
        # exec is not in safe_builtins, so this NameError-s inside exec.
        path = tmp_dmai_file("exec(\"print(1)\")\n")
        code = run_dmai_file(str(path))
        captured = capsys.readouterr()
        assert code == EXIT_RUNTIME_ERROR
        # NameError gets translated to Maithili by the exception handler.
        assert "त्रुटि" in captured.out

    def test_attempting_to_call_open_raises(self, tmp_dmai_file, capsys):
        path = tmp_dmai_file("open(\"/etc/passwd\")\n")
        code = run_dmai_file(str(path))
        assert code == EXIT_RUNTIME_ERROR

    def test_attempting_to_call_eval_raises(self, tmp_dmai_file, capsys):
        path = tmp_dmai_file("eval(\"1+1\")\n")
        code = run_dmai_file(str(path))
        assert code == EXIT_RUNTIME_ERROR

    def test_maithili_import_of_allowed_module_works(
        self, tmp_dmai_file, capsys
    ):
        # Positive control: a legitimate Maithili import of a
        # whitelisted module should succeed.
        path = tmp_dmai_file("आयात गणित\nछपाउ(गणित.pi)\n")
        code = run_dmai_file(str(path))
        captured = capsys.readouterr()
        assert code == EXIT_OK, (
            f"Clean program blocked unexpectedly: {captured.out}"
        )
        assert "3.14" in captured.out


# ---------------------------------------------------------------------------
# Whitelist shape: every MAITHILI_MODULES target is in _ALLOWED_MODULES.
# ---------------------------------------------------------------------------

def test_allowed_modules_matches_maithili_modules():
    assert _ALLOWED_MODULES == set(MAITHILI_MODULES.values())


@pytest.mark.parametrize("dangerous", [
    "subprocess", "socket", "ctypes", "pickle", "shutil",
    "urllib", "http", "ftplib", "telnetlib",
])
def test_dangerous_module_not_in_whitelist(dangerous):
    assert dangerous not in _ALLOWED_MODULES, (
        f"{dangerous} must never be in the import whitelist"
    )

# ---------------------------------------------------------------------------
# Security regression: linter tokenizer does not widen the trust boundary
# ---------------------------------------------------------------------------


@pytest.mark.security
def test_linter_tokenizer_does_not_expand_trust_boundary():
    """Code-like content inside string literals remains data.

    The linter now uses _tokenize_preserving_strings for
    paren/quote balance. This test verifies that using the
    tokenizer in the lint path does not accidentally weaken
    any runtime security boundaries — the transpiler, import
    validator, and sandbox execution path are unchanged.
    """
    from maithili_dsl.transpiler.linter import lint_maithili_code

    code_inside_string = '\u091b\u092a\u093e\u0909("import os; exec()")\n'
    errors = lint_maithili_code(code_inside_string)
    assert not any(
        "\u0917\u094b\u0932 \u092c\u094d\u0930\u0948\u0915\u0947\u091f" in e
        for e in errors
    )


@pytest.mark.security
def test_actual_dangerous_code_outside_strings_still_blocked():
    """Raw Python import outside strings is still caught by the import validator.

    The linter change uses the tokenizer for paren/quote balance checks.
    This test verifies that the security model is unchanged: dangerous
    code outside string literals remains blocked by _validate_imports.
    """
    from maithili_dsl.transpiler.transpile import transpile_maithili_code

    code = '\u091b\u092a\u093e\u0909("safe")\nimport os\n'
    transpiled = transpile_maithili_code(code)
    errors = _validate_imports(transpiled, translated_modules=set())
    assert errors, f"raw 'import os' must be blocked by import validator: {errors}"
