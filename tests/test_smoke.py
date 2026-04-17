"""Smoke tests: every example .dmai in examples/ executes end-to-end.

These tests drive the CLI as a real subprocess — the same code path a
user hits when running `python -m maithili_dsl examples/hello.dmai` —
so they catch packaging, entry-point, and integration regressions that
in-process tests would miss.

`error.dmai` is expected to fail linting (it contains intentionally
broken code for demo purposes) — so it gets an inverted assertion.
"""
from __future__ import annotations

import pytest

from maithili_dsl.cli import EXIT_LINT_ERROR, EXIT_OK


EXPECTED_OK = {
    "hello.dmai": ["हम मैथिली में कोड"],
    "person.dmai": ["हमर नाम सुमन"],
    # Devanagari numerals get converted to ASCII even inside string
    # literals (documented behavior of the numeral pre-pass).
    "calculator.dmai": ["जोड़ का परिणाम: 15", "5 × 1 = 5", "5 × 10 = 50"],
    "shopping_list.dmai": ["दूध", "रोटी", "कुल वस्तु: 4"],
}


@pytest.mark.smoke
@pytest.mark.parametrize("filename,expected_fragments", sorted(EXPECTED_OK.items()))
def test_example_runs_successfully(run_cli, examples_dir, filename, expected_fragments):
    """Each clean example .dmai file produces exit 0 and its expected output fragments."""
    path = examples_dir / filename
    assert path.exists(), f"Example missing: {path}"

    result = run_cli(str(path))

    assert result.returncode == EXIT_OK, (
        f"{filename} failed with exit {result.returncode}\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )
    for fragment in expected_fragments:
        assert fragment in result.stdout, (
            f"{filename}: expected {fragment!r} in output, got:\n{result.stdout}"
        )


@pytest.mark.smoke
def test_error_example_fails_linting(run_cli, examples_dir):
    """error.dmai contains intentionally broken code — it must be
    rejected by the linter, not executed."""
    path = examples_dir / "error.dmai"
    assert path.exists()

    result = run_cli(str(path))

    assert result.returncode == EXIT_LINT_ERROR
    assert "लिंटर" in result.stdout


@pytest.mark.smoke
def test_import_example_from_module_name(run_cli, tmp_dmai_file):
    """Spot-check that Maithili module imports work end-to-end via CLI."""
    path = tmp_dmai_file(
        "आयात गणित\n"
        "छपाउ(\"pi ~= \" + str(round(गणित.pi, २)))\n",
        name="import_math.dmai",
    )
    result = run_cli(str(path))
    assert result.returncode == EXIT_OK, (
        f"stdout={result.stdout!r} stderr={result.stderr!r}"
    )
    assert "3.14" in result.stdout
