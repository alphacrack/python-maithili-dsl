"""Functional tests for the Maithili → Python transpiler.

Covers three major behaviors:
  1. Every keyword in DEVNAGIRI_KEYWORD_MAP maps correctly at word
     boundaries.
  2. Regression tests for AUDIT_REPORT.md CQ-001 (CRITICAL): keywords
     inside string literals and inside longer identifiers must NOT
     be replaced.
  3. The transpiled output is valid Python that can be compiled.
"""
import ast
import pytest

from maithili_dsl.transpiler.transpile import transpile_maithili_code
from maithili_dsl.transpiler.mappings import DEVNAGIRI_KEYWORD_MAP


# ---------------------------------------------------------------------------
# 1. Keyword coverage — every mapping works in isolation
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("maithili_kw,py_kw", list(DEVNAGIRI_KEYWORD_MAP.items()))
def test_each_keyword_translates(maithili_kw, py_kw):
    """Every entry in DEVNAGIRI_KEYWORD_MAP must translate when used
    as a standalone token."""
    source = f"{maithili_kw}"
    result = transpile_maithili_code(source)
    assert result == py_kw, (
        f"Expected {maithili_kw!r} → {py_kw!r}, got {result!r}"
    )


def test_function_definition_transpiles():
    src = "कार्य नमस्कार():\n    छपाउ(\"hi\")\n"
    out = transpile_maithili_code(src)
    assert "def नमस्कार():" in out
    assert "print(\"hi\")" in out


def test_class_with_constructor_and_self():
    src = (
        "वर्ग व्यक्ति:\n"
        "    कार्य नव(स्वयं, नाम):\n"
        "        स्वयं.नाम = नाम\n"
    )
    out = transpile_maithili_code(src)
    assert "class व्यक्ति:" in out
    assert "def __init__(self, नाम):" in out
    assert "self.नाम = नाम" in out


def test_for_in_range_with_numerals():
    src = "प्रत्येक i में range(१, ५):\n    छपाउ(i)\n"
    out = transpile_maithili_code(src)
    assert "for i in range(1, 5):" in out
    assert "print(i)" in out


def test_if_else_bool_none():
    src = (
        "यदि सत्य:\n"
        "    x = शून्य\n"
        "नहि त:\n"
        "    x = मिथ्या\n"
    )
    out = transpile_maithili_code(src)
    assert "if True:" in out
    assert "x = None" in out
    assert "else:" in out
    assert "x = False" in out


def test_import_from_as():
    src = "सँ गणित आयात sqrt स्वरूपे s\n"
    out = transpile_maithili_code(src)
    # Note: module-name translation happens in cli.translate_imports,
    # not in the transpiler. The transpiler only touches keywords.
    assert out == "from गणित import sqrt as s\n"


def test_return_statement():
    src = "कार्य f():\n    फेर करू ४२\n"
    out = transpile_maithili_code(src)
    assert "return 42" in out


# ---------------------------------------------------------------------------
# 2. CQ-001 regressions — string-aware + word-boundary behavior
# ---------------------------------------------------------------------------

class TestStringLiteralPreservation:
    """AUDIT_REPORT.md CQ-001: keywords inside string literals must
    NOT be replaced. The original bug:
        छपाउ("यह में है")  ->  print("यह in है")   ← WRONG
    """

    def test_maithili_keyword_inside_double_quotes_preserved(self):
        src = 'छपाउ("यह में है")'
        out = transpile_maithili_code(src)
        assert out == 'print("यह में है")', (
            f"में was wrongly replaced inside string literal: {out!r}"
        )

    def test_maithili_keyword_inside_single_quotes_preserved(self):
        src = "छपाउ('यह में है')"
        out = transpile_maithili_code(src)
        assert out == "print('यह में है')"

    def test_multiple_keywords_in_one_string(self):
        src = 'छपाउ("कार्य यदि में वर्ग")'
        out = transpile_maithili_code(src)
        # The surrounding छपाउ becomes print, but inside the string
        # every keyword must survive.
        assert out == 'print("कार्य यदि में वर्ग")'

    def test_escaped_quote_in_string(self):
        src = r'छपाउ("यह \"में\" है")'
        out = transpile_maithili_code(src)
        assert 'print(' in out
        assert r'\"में\"' in out

    def test_keyword_in_comment_preserved(self):
        src = "x = १  # यह में सत्य अछि\n"
        out = transpile_maithili_code(src)
        assert "# यह में सत्य अछि" in out, (
            "Comments should not have keywords replaced"
        )


class TestWordBoundaries:
    """AUDIT_REPORT.md CQ-001: keywords matched as substrings of
    longer identifiers must NOT be replaced. The original bug:
        नवयुग = ५  ->  __init__युग = 5   ← WRONG
    """

    def test_keyword_prefix_of_identifier_preserved(self):
        # नव (→ __init__) should NOT fire inside नवयुग
        src = "नवयुग = ५"
        out = transpile_maithili_code(src)
        assert out == "नवयुग = 5", f"नव fired inside नवयुग: {out!r}"

    def test_keyword_suffix_of_identifier_preserved(self):
        # में (→ in) should NOT fire inside कारमें
        src = "कारमें = १"
        out = transpile_maithili_code(src)
        assert out == "कारमें = 1"

    def test_keyword_as_prefix_then_space_does_fire(self):
        # Sanity check the other side: with a space after, नव fires.
        src = "नव "
        out = transpile_maithili_code(src)
        assert out == "__init__ "

    def test_two_adjacent_keywords(self):
        # Keywords separated by whitespace should both fire.
        src = "यदि सत्य:"
        out = transpile_maithili_code(src)
        assert out == "if True:"


# ---------------------------------------------------------------------------
# 3. End-to-end: transpiled Python must parse
# ---------------------------------------------------------------------------

class TestTranspiledPythonIsValid:
    def test_hello_parses(self):
        src = "कार्य नमस्कार():\n    छपाउ(\"hi\")\n\nनमस्कार()\n"
        out = transpile_maithili_code(src)
        ast.parse(out)  # raises if invalid

    def test_class_parses(self):
        src = (
            "वर्ग व्यक्ति:\n"
            "    कार्य नव(स्वयं, नाम):\n"
            "        स्वयं.नाम = नाम\n"
            "\n"
            "व्यक्ति१ = व्यक्ति(\"सुमन\")\n"
        )
        out = transpile_maithili_code(src)
        ast.parse(out)

    def test_loop_parses(self):
        src = "प्रत्येक i में range(१, ५):\n    छपाउ(i)\n"
        out = transpile_maithili_code(src)
        ast.parse(out)


# ---------------------------------------------------------------------------
# 4. Edge cases
# ---------------------------------------------------------------------------

def test_empty_input():
    assert transpile_maithili_code("") == ""


def test_only_whitespace():
    assert transpile_maithili_code("   \n\n  ") == "   \n\n  "


def test_only_ascii_passes_through():
    src = "x = 1 + 2\n"
    assert transpile_maithili_code(src) == src


def test_numerals_inside_strings_still_convert():
    # Documented current behavior: the numeral pass runs BEFORE
    # tokenization, so digits inside strings also get converted.
    # This may or may not be desirable, but it's the current contract.
    src = 'छपाउ("५ × ४")'
    out = transpile_maithili_code(src)
    assert out == 'print("5 × 4")'


def test_multiple_statements_preserve_newlines():
    src = "x = १\ny = २\nz = x + y\n"
    out = transpile_maithili_code(src)
    assert out == "x = 1\ny = 2\nz = x + y\n"
