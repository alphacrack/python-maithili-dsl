"""Tests for the CLI entry point (run_dmai_file + main).

Exercises every exit-code path and confirms the user-facing messages
are stable.
"""
from pathlib import Path

import pytest

from maithili_dsl.cli import (
    EXIT_BAD_ENCODING,
    EXIT_IMPORT_BLOCKED,
    EXIT_LINT_ERROR,
    EXIT_NOT_FOUND,
    EXIT_OK,
    EXIT_RUNTIME_ERROR,
    EXIT_USAGE,
    main,
    run_dmai_file,
)


# ---------------------------------------------------------------------------
# run_dmai_file exit-code paths
# ---------------------------------------------------------------------------

def test_missing_file_returns_not_found(capsys):
    code = run_dmai_file("/nonexistent/path/to/file.dmai")
    captured = capsys.readouterr()
    assert code == EXIT_NOT_FOUND
    assert "not found" in captured.out.lower()


def test_non_utf8_file_returns_bad_encoding(tmp_path, capsys):
    path = tmp_path / "invalid.dmai"
    path.write_bytes(b"\xff\xfe")

    code = run_dmai_file(str(path))
    captured = capsys.readouterr()

    assert code == EXIT_BAD_ENCODING
    assert "UTF-8" in captured.out
    assert "Traceback" not in captured.out


def test_unreadable_file_returns_not_found(tmp_path, monkeypatch, capsys):
    path = tmp_path / "unreadable.dmai"
    path.write_text("छपाउ(\"hello\")\n", encoding="utf-8")

    def deny_read(*args, **kwargs):
        raise PermissionError("private path details")

    monkeypatch.setattr("builtins.open", deny_read)
    code = run_dmai_file(str(path))
    captured = capsys.readouterr()

    assert code == EXIT_NOT_FOUND
    assert "फाइल पढ़ल नहि जा सकल" in captured.out
    assert "private path details" not in captured.out


def test_lint_error_returns_lint_exit_code(tmp_dmai_file, capsys):
    # The leading = triggers the "'=' चिह्नक पहिले" lint error.
    path = tmp_dmai_file("= ५\n")
    code = run_dmai_file(str(path))
    captured = capsys.readouterr()
    assert code == EXIT_LINT_ERROR
    assert "लिंटर" in captured.out


def test_import_blocked_returns_blocked_exit_code(tmp_dmai_file):
    # Raw Python import → blocked by _validate_imports.
    path = tmp_dmai_file("import os\n")
    code = run_dmai_file(str(path))
    assert code == EXIT_IMPORT_BLOCKED


def test_valid_file_returns_ok(tmp_dmai_file, capsys):
    path = tmp_dmai_file("छपाउ(\"hello\")\n")
    code = run_dmai_file(str(path))
    captured = capsys.readouterr()
    assert code == EXIT_OK
    assert "hello" in captured.out


def test_runtime_error_returns_runtime_exit_code(tmp_dmai_file, capsys):
    # undefined variable → NameError inside exec → translated and exit 6.
    path = tmp_dmai_file("छपाउ(अपरिभाषित_चर)\n")
    code = run_dmai_file(str(path))
    captured = capsys.readouterr()
    assert code == EXIT_RUNTIME_ERROR
    assert "त्रुटि" in captured.out


# ---------------------------------------------------------------------------
# main() argv handling
# ---------------------------------------------------------------------------

def test_main_with_no_args_shows_usage(capsys):
    code = main([])
    captured = capsys.readouterr()
    assert code == EXIT_USAGE
    assert "Usage" in captured.out


def test_main_with_version_flag(capsys):
    from maithili_dsl import __version__
    code = main(["--version"])
    captured = capsys.readouterr()
    assert code == EXIT_OK
    assert __version__ in captured.out


def test_main_with_short_version_flag(capsys):
    code = main(["-V"])
    captured = capsys.readouterr()
    assert code == EXIT_OK


def test_main_dispatches_to_run_dmai_file(tmp_dmai_file, capsys):
    path = tmp_dmai_file("छपाउ(\"dispatched\")\n")
    code = main([str(path)])
    captured = capsys.readouterr()
    assert code == EXIT_OK
    assert "dispatched" in captured.out


# ---------------------------------------------------------------------------
# Subprocess: verify `python -m maithili_dsl` works end-to-end
# ---------------------------------------------------------------------------

def test_python_m_maithili_dsl_version(run_cli):
    result = run_cli("--version")
    assert result.returncode == 0
    assert "python_maithili" in result.stdout


def test_python_m_maithili_dsl_usage_on_no_args(run_cli):
    result = run_cli()
    assert result.returncode == EXIT_USAGE
    assert "Usage" in result.stdout


def test_python_m_maithili_dsl_runs_file(run_cli, tmp_dmai_file):
    path = tmp_dmai_file("छपाउ(\"subprocess-ok\")\n")
    result = run_cli(str(path))
    assert result.returncode == 0, (
        f"stdout={result.stdout!r} stderr={result.stderr!r}"
    )
    assert "subprocess-ok" in result.stdout
