# 🤝 Contributing to the Devnagiri Maithili DSL

Welcome! Your contributions help make the Maithili DSL stronger and more
accessible. This guide covers local setup, the test workflow, and how to
submit a change for review.

---

## 🛠 Development setup

Clone and install the package in editable mode together with the
development dependencies:

```bash
git clone https://github.com/alphacrack/python-maithili-dsl.git
cd python-maithili-dsl
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
pip install -r requirements-dev.txt
```

Run a sample file to verify the CLI works:

```bash
python -m maithili_dsl examples/hello.dmai
# or, equivalently, via the console script:
python_maithili examples/hello.dmai
```

---

## 🧪 Running tests

**Always run the full suite before opening a PR.** It takes ~1 second.

```bash
pytest -v --cov=maithili_dsl --cov-report=term-missing
```

The test suite is organized by tier:

| File | What it covers |
|------|----------------|
| `tests/test_numeral.py`   | Devanagari → ASCII numeral conversion |
| `tests/test_transpile.py` | Functional: every keyword + string-literal + word-boundary regressions |
| `tests/test_linter.py`    | Every lint rule, exception translations |
| `tests/test_security.py`  | Sandbox: import whitelist, safe builtins, malicious-file rejection |
| `tests/test_cli.py`       | CLI entry point, every exit code, subprocess invocation |
| `tests/test_smoke.py`     | End-to-end: every example in `examples/` runs via the CLI |

The project enforces a coverage gate of **≥85% overall** and **≥90% on
the critical modules** (`cli.py`, `transpiler/transpile.py`,
`transpiler/linter.py`). If your change drops coverage below that,
please add tests.

### Security changes

Any change touching `cli.py`, the transpiler's string handling, the
import whitelist (`MAITHILI_MODULES`), or the safe-builtins list
(`_SAFE_BUILTIN_NAMES`) must include:

1. A new test in `tests/test_security.py` proving the intended behavior.
2. A short "Security Considerations" section in the PR description.

---

## 🧩 How you can contribute

- 📚 Improve keyword mappings and add new features (see `BACKLOG.md` P3)
- 🧪 Expand test coverage, especially on edge cases
- 🐛 Fix a backlog item (see `BACKLOG.md`)
- 🌐 Help add Tirhuta script support
- ✍️ Translate documentation into Maithili
- 🔐 Report a security vulnerability via the process in `SECURITY.md`

---

## 📬 Submitting changes

1. Fork the repository and create a topic branch off `development`
   (not `main` — `main` is the released line).
2. Make your changes in logical commits — one concern per commit.
   Follow conventional-commit style where reasonable
   (`fix(linter): ...`, `feat(cli): ...`).
3. Run `pytest` and make sure it's green.
4. Open a Pull Request targeting `development`. The PR template will
   prompt you for test evidence and any security considerations.

Thanks for your interest! ❤️
