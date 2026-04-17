# Maithili DSL — Full Audit Report

> Audit Date: 2026-04-11
> Auditor: Project Maintainer (automated + manual review)
> Scope: Security, License, Code Quality, Packaging, Compliance, Dependencies

---

## 1. Security Audit

### Finding SEC-001: Unrestricted code execution via exec() [CRITICAL]
- **Location:** `maithili_dsl/cli.py:46`
- **Description:** `exec(python_code, globals())` executes transpiled user code with full access to the CLI process's global namespace. Any `.dmai` file can import `os`, `subprocess`, or `sys` and perform arbitrary system operations.
- **Evidence:** Direct code inspection — no sandboxing, no restricted builtins.
- **Recommendation:** Replace `globals()` with a restricted execution namespace.

### Finding SEC-002: No input validation [HIGH]
- **Location:** `maithili_dsl/cli.py:26-33`
- **Description:** `run_dmai_file()` reads any file path without size limits, type checking, or timeout protection.
- **Evidence:** The function accepts any path and reads the entire file into memory.
- **Recommendation:** Add file size limit (e.g., 1MB), file extension check, and execution timeout.

### Finding SEC-003: No vulnerability reporting process [MEDIUM]
- **Description:** No `SECURITY.md` exists. No documented way for security researchers to report vulnerabilities.
- **Recommendation:** Add SECURITY.md with responsible disclosure process.

---

## 2. License Audit

### Finding LIC-001: LICENSE file is incomplete [CRITICAL]
- **Location:** `LICENSE`
- **Evidence:** File contains placeholder text:
  - Line 3: `Copyright (c) 2025 [Your Name]`
  - Line 13: `[MIT terms continued...]`
- **Impact:** The project is effectively unlicensed. Contributors and users have no legal permission to use the code.
- **Recommendation:** Replace with complete MIT license text with correct copyright holder.

### Finding LIC-002: No license headers in source files [LOW]
- **Description:** Individual `.py` files do not contain license headers or copyright notices.
- **Recommendation:** Optional for MIT-licensed projects, but good practice. Consider adding a brief header.

### Finding LIC-003: No third-party dependency licenses to audit [PASS]
- **Description:** The project has zero runtime dependencies. Only uses Python standard library.
- **Status:** No license conflicts possible.

---

## 3. Code Quality Audit

### Finding CQ-001: Transpiler uses naive string replacement [CRITICAL]
- **Location:** `maithili_dsl/transpiler/transpile.py:4-7`
- **Evidence (reproduced):**
  ```
  Input:  छपाउ("यह में है")
  Output: print("यह in है")     ← keyword replaced inside string literal
  
  Input:  नवयुग = ५
  Output: __init__युग = 5       ← keyword replaced inside identifier
  ```
- **Impact:** Any Maithili text containing a keyword substring will be corrupted. This affects every non-trivial program.
- **Recommendation:** Implement proper tokenizer that respects string boundaries and word boundaries.

### Finding CQ-002: Zero test coverage [HIGH]
- **Description:** No test files, no test configuration, no test runner.
- **Recommendation:** Add pytest with tests for transpiler, linter, numeral conversion, CLI.

### Finding CQ-003: No type annotations [LOW]
- **Description:** No type hints on any function.
- **Recommendation:** Add type hints progressively. Add mypy to CI.

---

## 4. Packaging Audit

### Finding PKG-001: No pyproject.toml [MEDIUM]
- **Description:** Only `setup.py` exists. PEP 517/518 compliance requires `pyproject.toml`.
- **Recommendation:** Add pyproject.toml with build system and metadata.

### Finding PKG-002: setup.py version mismatch risk [LOW]
- **Description:** Version is `0.2.0` in setup.py but there's no `__version__` in `__init__.py`. No single source of truth.
- **Recommendation:** Define version in one place and import/reference it.

### Finding PKG-003: Empty __init__.py files [LOW]
- **Description:** No public API defined. Users importing the package get nothing.
- **Recommendation:** Export key functions via `__all__`.

---

## 5. Compliance Audit

| Item | Status | Notes |
|------|--------|-------|
| LICENSE file | FAIL | Incomplete — has placeholders |
| SECURITY.md | MISSING | No vulnerability reporting process |
| CODE_OF_CONDUCT.md | MISSING | No community guidelines |
| CONTRIBUTING.md | PARTIAL | Exists but contains duplicated README content |
| .gitignore | PASS | Covers common patterns |
| README.md | PARTIAL | Clone URL has placeholder `youruser` |

---

## 6. Infrastructure Audit

| Item | Status | Notes |
|------|--------|-------|
| CI/CD (GitHub Actions) | MISSING | No automated testing on push/PR |
| Pre-commit hooks | MISSING | No code quality gates |
| Dependency pinning | N/A | Zero runtime deps; dev deps not specified |
| Release process | MISSING | No tags, no changelog, no PyPI publishing |

---

## 7. Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 3 (exec sandbox, LICENSE, transpiler bugs) |
| HIGH     | 3 (input validation, no tests, no CI) |
| MEDIUM   | 3 (SECURITY.md, pyproject.toml, linter false positives) |
| LOW      | 5 (type hints, license headers, version, init, deps) |
| PASS     | 2 (no dependency license conflicts, .gitignore) |
| **Total**| **16 findings** |

---

## 8. Recommended Fix Order

1. Fix LICENSE file (5 minutes — removes legal risk immediately)
2. Fix transpiler str.replace bugs (core functionality is broken)
3. Sandbox exec() (security critical)
4. Add basic test suite (prevents regressions while fixing above)
5. Add GitHub Actions CI (automates quality going forward)
6. Add SECURITY.md + CODE_OF_CONDUCT.md (compliance basics)
7. Everything else by priority
