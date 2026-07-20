# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- Parentheses and quote characters inside string literals no longer trigger false unbalanced-linter warnings.
- Single-quote balance is now checked alongside double-quote balance (previously only double quotes were validated).
- Augmented assignments no longer produce invalid-variable-name linter errors.

### Added
- **PyPI publish pipeline** (`.github/workflows/publish.yml`) using
  Trusted Publishing (OIDC). Triggers: GitHub Release for production
  PyPI, pre-release or `workflow_dispatch` for TestPyPI, `build-only`
  dispatch for a credential-free dry run. The workflow builds sdist +
  wheel, runs `twine check --strict`, installs the wheel in a clean
  venv, runs the full pytest suite against the installed wheel, and
  verifies the release tag matches `__version__` before publishing.
- **`docs/RELEASE.md`** — step-by-step release process including
  one-time Trusted Publisher setup on PyPI + TestPyPI, routine
  release flow, version-bump convention, and recovery procedure for
  bad releases.
- **`build` and `twine`** added to `requirements-dev.txt`.

## [0.3.0] — 2026-04-17

This is a hardening and correctness release. Every P0 finding in
`AUDIT_REPORT.md` is closed.

### Added
- **Security sandbox.** `.dmai` files now execute inside a restricted
  `__builtins__` dict (no `exec`, `eval`, `compile`, `open`,
  `breakpoint`, direct `__import__`) and an import whitelist driven
  from `MAITHILI_MODULES`. Raw Python `import` lines that weren't
  translated from Maithili are rejected before `exec` by a static
  validator; a runtime `__import__` wrapper enforces the same
  whitelist as a second line of defense. Closes SEC-001.
- **Full pytest suite.** 142 tests across six files covering
  functional (every keyword, every numeral), linter rules, security
  (sandbox escapes, malicious imports), CLI exit codes, and
  end-to-end smoke tests over every `.dmai` in `examples/`. Overall
  coverage 95%; critical modules all ≥90%. Closes CQ-002.
- **GitHub Actions CI.** Matrix of Python 3.9/3.10/3.11/3.12 × Ubuntu
  + macOS = 8 jobs. Runs tests + coverage + examples smoke loop on
  every push and PR to `main` / `development`. Closes #6.
- **`python -m maithili_dsl` entry point.** New `__main__.py` allows
  module-style invocation without needing the console script.
- **CLI `--version` / `-V` flag.**
- **Named exit codes.** `EXIT_OK` / `EXIT_USAGE` / `EXIT_NOT_FOUND` /
  `EXIT_LINT_ERROR` / `EXIT_IMPORT_BLOCKED` / `EXIT_RUNTIME_ERROR` so
  CI and callers can distinguish failure modes. Closes PKG-002.
- **`pyproject.toml`.** PEP 517/518 build metadata with pytest +
  coverage config co-located. Closes PKG-001.
- **`SECURITY.md`** — responsible disclosure process + threat model.
- **`CHANGELOG.md`** — this file.
- **`.github/PULL_REQUEST_TEMPLATE.md`** — enforces test evidence and
  audit-reference fields on future PRs.
- **`requirements-dev.txt`** — pinned `pytest`, `pytest-cov`,
  `pytest-timeout`.
- **Public API exports.** `maithili_dsl/__init__.py` now exposes
  `__version__`, `transpile_maithili_code`, `lint_maithili_code`,
  `translate_exception_to_maithili`, `convert_devanagari_numerals`.
  Closes PKG-003.

### Fixed
- **Transpiler replaced keywords inside string literals.** `छपाउ("यह
  में है")` used to become `print("यह in है")`. The transpiler now
  tokenizes input and only replaces keywords in code regions, not in
  quoted strings or comments. Closes CQ-001 (first half).
- **Transpiler replaced keyword substrings of longer identifiers.**
  `नवयुग = ५` used to become `__init__युग = 5`. The transpiler now
  uses Devanagari-aware negative lookbehind/lookahead so keyword
  matches fire only at true word boundaries. Closes CQ-001 (second
  half).
- **Linter flagged `==` comparisons as assignments.** Any conditional
  using `==` / `!=` / `<=` / `>=` used to surface a spurious "invalid
  variable name" error. The linter now distinguishes comparison
  operators from assignments before validating the left-hand side.
- **Linter flagged `नव` constructors as unused functions.** `नव`
  (mapped to `__init__`) is invoked implicitly via class
  instantiation, so it's never called by name. The unused-function
  post-scan now skips it.
- **Linter flagged attribute assignments.** Lines like
  `स्वयं.नाम = नाम` were being checked as new-variable declarations.
  Attribute assignments (anything with `.` in the LHS) are now
  skipped.
- **LICENSE was unenforceable.** Contained `[Your Name]` and
  `[MIT terms continued...]` placeholders. Replaced with the full
  MIT license text and a real copyright holder. Closes LIC-001.

### Changed
- **Python minimum bumped from 3.6 to 3.9.** 3.6–3.8 are EOL and the
  new transpiler uses regex and f-string features that aren't worth
  conditionally supporting.
- **`README.md`** — fixed `youruser` placeholder, added Security and
  Testing sections, moved CI/CD out of "future goals" (it's shipped).
- **`CONTRIBUTING.md`** — removed the full README that was
  accidentally pasted above the actual contributing guide; expanded
  with real dev setup, test workflow, and security-change policy.

### Removed
- Nothing.

## [0.2.0]

Initial versioned release. See git history before 2026-04-17.
