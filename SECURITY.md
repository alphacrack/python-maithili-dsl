# Security Policy

## Supported versions

Only the latest minor release receives security patches. Older versions
are best-effort.

| Version | Supported           |
|---------|---------------------|
| 0.3.x   | ✅ current           |
| 0.2.x   | ⚠️ critical fixes only |
| < 0.2   | ❌ not supported     |

## Threat model

`python_maithili` executes user-supplied `.dmai` files. The sandbox in
`maithili_dsl/cli.py` is the project's primary trust boundary. It
enforces:

1. **Import whitelist.** Only modules present in `MAITHILI_MODULES` (the
   Maithili → Python module map) are importable from a `.dmai` file.
   Raw Python `import` statements that were not translated from Maithili
   names are rejected by `_validate_imports` before `exec` runs. The
   `__import__` builtin inside the sandbox is replaced with a wrapper
   that re-checks the whitelist at runtime.
2. **Safe builtins.** The execution namespace's `__builtins__` is a
   curated dict (`_SAFE_BUILTIN_NAMES`). Notably absent: `exec`, `eval`,
   `compile`, `open`, `breakpoint`. Any `.dmai` script that calls these
   gets a `NameError` translated to Maithili.
3. **No shared globals.** `exec` runs with a fresh globals dict — it
   cannot read or modify the CLI's own process state.

If you find a way to bypass any of these, please report it.

## Reporting a vulnerability

Please do **not** open a public issue for security problems. Instead:

- Email: **jha.bishwas@gmail.com** with the subject line
  `[SECURITY] python_maithili` and a proof-of-concept.
- Or use GitHub's private vulnerability reporting at
  https://github.com/alphacrack/python-maithili-dsl/security/advisories/new

Please include:

- A `.dmai` file that demonstrates the issue.
- The Python version and OS.
- What the sandbox *should* have prevented, and what actually happened.

## Response SLA

- **Acknowledgement**: within 3 business days.
- **Triage + severity classification**: within 7 business days.
- **Patch + coordinated disclosure**: depends on severity; typically
  within 30 days for HIGH/CRITICAL findings.

## Scope

In scope:

- Sandbox escape from within a `.dmai` file.
- Ability to read or modify files outside the CWD without being invoked
  by an explicitly-whitelisted module call.
- Denial of service via a small `.dmai` input (e.g., catastrophic regex
  backtracking in the transpiler).

Out of scope:

- Issues that require first compromising the machine running
  `python_maithili` (e.g., modifying the installed package).
- Social engineering.
- Resource-exhaustion attacks that require arbitrarily large input
  (basic DoS via huge files).
