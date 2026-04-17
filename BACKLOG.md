# Maithili DSL — Project Backlog

> Generated: 2026-04-11 | Status: Active
> Tracking: GitHub Issues (use `scripts/create_issues.sh` to push)

---

## P0 — Critical (Must Fix)

### 1. [SECURITY] exec() runs with globals() — sandbox needed
- **File:** `maithili_dsl/cli.py:46`
- **Issue:** `exec(python_code, globals())` allows .dmai scripts to modify the CLI tool itself at runtime. A malicious `.dmai` file can import `os`, delete files, or exfiltrate data.
- **Fix:** Execute in a restricted namespace: `exec(python_code, {"__builtins__": safe_builtins}, local_ns)`
- **Labels:** security, P0

### 2. [BUG] Transpiler replaces keywords inside string literals
- **File:** `maithili_dsl/transpiler/transpile.py`
- **Proven:** `छपाउ("यह में है")` → `print("यह in है")` — the word `में` inside quotes gets replaced with `in`.
- **Fix:** Use tokenization or regex with negative lookbehind for quoted regions instead of blind `str.replace()`.
- **Labels:** bug, P0

### 3. [BUG] Transpiler replaces keywords inside longer words
- **File:** `maithili_dsl/transpiler/transpile.py`
- **Proven:** `नवयुग = ५` → `__init__युग = 5` — `नव` (maps to `__init__`) is matched as a substring.
- **Fix:** Use word-boundary-aware replacement (`\bकार्य\b` equivalent for Devanagari).
- **Labels:** bug, P0

### 4. [LICENSE] LICENSE file is incomplete
- **File:** `LICENSE`
- **Issue:** Contains `[Your Name]` placeholder and `[MIT terms continued...]` — not a valid MIT license.
- **Fix:** Replace with the full MIT license text with correct copyright holder name.
- **Labels:** compliance, P0

---

## P1 — High (Should Fix Soon)

### 5. [QUALITY] No tests exist
- **Issue:** Zero test files in the entire project. No unit tests, no integration tests, no test runner configured.
- **Fix:** Add `tests/` directory with pytest. Cover transpiler, linter, numeral conversion, and CLI.
- **Labels:** testing, P1

### 6. [INFRA] No CI/CD pipeline
- **Issue:** No GitHub Actions, no tox.ini, no pre-commit hooks. Code can be pushed without any automated checks.
- **Fix:** Add `.github/workflows/ci.yml` with lint + test + build steps.
- **Labels:** infra, P1

### 7. [SECURITY] No input validation before exec
- **Issue:** `run_dmai_file()` reads any file and execs it. No file size limits, no timeout, no sandboxing.
- **Fix:** Add file size limits, execution timeout, and restricted builtins.
- **Labels:** security, P1

### 8. [COMPLIANCE] No SECURITY.md
- **Issue:** No documented process for reporting security vulnerabilities.
- **Fix:** Add `SECURITY.md` with responsible disclosure instructions.
- **Labels:** compliance, P1

### 9. [PACKAGING] Missing pyproject.toml (PEP 517/518)
- **Issue:** Only `setup.py` exists. Modern Python tooling expects `pyproject.toml`.
- **Fix:** Add `pyproject.toml` alongside or replacing `setup.py`.
- **Labels:** packaging, P1

---

## P2 — Medium (Plan for Next Sprint)

### 10. [BUG] Linter may produce false positives for Devanagari identifiers
- **File:** `maithili_dsl/transpiler/linter.py:65`
- **Issue:** `var_name.isidentifier()` works for Devanagari in Python 3, but the linter's `is_snake_case()` regex only matches ASCII — it will always fail for Devanagari variable names.
- **Fix:** Update naming checks to support Devanagari script identifiers.
- **Labels:** bug, P2

### 11. [DOCS] CONTRIBUTING.md has duplicated README content
- **File:** `CONTRIBUTING.md`
- **Issue:** The file contains the full README.md pasted above the actual contributing guidelines.
- **Fix:** Remove duplicated content, keep only contributing-specific information.
- **Labels:** docs, P2

### 12. [QUALITY] No type hints in codebase
- **Issue:** No function signatures have type annotations. Makes it harder for contributors to understand the API.
- **Fix:** Add type hints to all public functions. Add `mypy` to CI.
- **Labels:** quality, P2

### 13. [COMPLIANCE] No CODE_OF_CONDUCT.md
- **Issue:** Open source projects should have a code of conduct for community health.
- **Fix:** Add Contributor Covenant or similar.
- **Labels:** compliance, P2

### 14. [PACKAGING] Empty __init__.py files
- **Issue:** `maithili_dsl/__init__.py` and `maithili_dsl/transpiler/__init__.py` are empty — no public API is exported.
- **Fix:** Define `__all__` and export key functions for programmatic use.
- **Labels:** packaging, P2

---

## P3 — Low (Nice to Have)

### 15. [DOCS] README references `youruser` in clone URL
- **Issue:** `git clone https://github.com/youruser/maithili-dsl.git` — should point to the real repo.
- **Fix:** Update to `alphacrack/python-maithili-dsl`.
- **Labels:** docs, P3

### 16. [FEATURE] Add `while` loop support (`जबतक`)
- **Issue:** No `while` keyword mapping exists. Only `for` (`प्रत्येक`) is supported.
- **Fix:** Add to `DEVNAGIRI_KEYWORD_MAP`.
- **Labels:** enhancement, P3

### 17. [FEATURE] Add `try/except` support for error handling
- **Issue:** No exception handling keywords mapped. Users can't write try/except in Maithili.
- **Fix:** Add `प्रयास` → `try`, `अपवाद` → `except`, `अंततः` → `finally`.
- **Labels:** enhancement, P3

### 18. [FEATURE] REPL mode for interactive Maithili coding
- **Issue:** Listed as a future goal in README but not started.
- **Fix:** Add `python_maithili --repl` interactive mode.
- **Labels:** enhancement, P3

### 19. [INFRA] No dependency pinning
- **Issue:** No `requirements.txt` or `requirements-dev.txt`. Project currently has zero deps, but test/lint tools need to be pinned.
- **Fix:** Add `requirements-dev.txt` with pytest, mypy, flake8 versions pinned.
- **Labels:** infra, P3

---

## Summary

| Priority | Count | Focus |
|----------|-------|-------|
| P0       | 4     | Security holes, data-corrupting bugs, invalid license |
| P1       | 5     | Testing, CI/CD, compliance foundations |
| P2       | 5     | Code quality, docs cleanup, contributor experience |
| P3       | 5     | Features, nice-to-haves, polish |
| **Total**| **19**| |
