"""Shared fixtures for the Maithili DSL test suite."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = REPO_ROOT / "examples"


@pytest.fixture
def tmp_dmai_file(tmp_path):
    """Factory that writes a .dmai file into a tmp dir and returns its path."""

    def _make(content: str, name: str = "test.dmai") -> Path:
        path = tmp_path / name
        path.write_text(content, encoding="utf-8")
        return path

    return _make


@pytest.fixture
def run_cli():
    """Run the CLI as a subprocess and return CompletedProcess.

    Uses `python -m maithili_dsl` so the tests exercise the real entry
    point a user would hit, not just importable functions.
    """

    def _run(*args, cwd=None, timeout=30) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, "-m", "maithili_dsl", *args],
            capture_output=True,
            text=True,
            cwd=cwd or str(REPO_ROOT),
            timeout=timeout,
        )

    return _run


@pytest.fixture
def examples_dir() -> Path:
    return EXAMPLES_DIR
