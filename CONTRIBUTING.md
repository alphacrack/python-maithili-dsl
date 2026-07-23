# 🤝 Contributing to the Devnagiri Maithili DSL

Welcome! Your contributions help make the Maithili DSL stronger and more
accessible. This guide covers local setup, the test workflow, and how to
submit a change for review.

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md).
By participating, you are expected to uphold it.

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

### Finding something to work on

Issues labeled [`good first issue`](https://github.com/alphacrack/python-maithili-dsl/labels/good%20first%20issue)
are scoped for newcomers; [`help wanted`](https://github.com/alphacrack/python-maithili-dsl/labels/help%20wanted)
issues are open to anyone. Labels follow a simple scheme:

| Label group | Meaning |
|-------------|---------|
| `P0`–`P3` | Priority, from critical to nice-to-have |
| `bug`, `enhancement`, `documentation`, `question` | Issue type |
| `security`, `testing`, `infra`, `packaging`, `quality`, `compliance` | Category |
| `area:transpiler`, `area:linter`, `area:cli` | Part of the codebase affected |
| `keyword-mapping` | Proposals for new Maithili keywords or module mappings |
| `translation` | Translating docs or messages into Maithili |
| `needs-triage` | New issue awaiting a maintainer's look |

Comment on an issue before starting significant work so it can be assigned
to you and effort isn't duplicated. New keyword ideas should go through the
**🔤 Keyword / mapping proposal** issue template — native-speaker input on
word choice is especially welcome.

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

## 📦 Releasing

Releases are cut by a project maintainer following the checklist in
[`docs/RELEASE.md`](docs/RELEASE.md). The short version:
publishing is triggered by creating a **GitHub Release** and uses
**Trusted Publishing (OIDC)** — no long-lived PyPI tokens are stored
in the repo.

Thanks for your interest! ❤️
