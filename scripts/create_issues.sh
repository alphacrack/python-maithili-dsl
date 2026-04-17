#!/usr/bin/env bash
# Creates GitHub Issues from the backlog.
# Run from the repo root: bash scripts/create_issues.sh
# Requires: gh CLI authenticated (https://cli.github.com)

set -euo pipefail

REPO="alphacrack/python-maithili-dsl"

echo "Creating P0 issues..."

gh issue create --repo "$REPO" \
  --title "[SECURITY][P0] exec() runs with globals() — sandbox needed" \
  --body "**File:** \`maithili_dsl/cli.py:46\`

\`exec(python_code, globals())\` allows .dmai scripts to modify the CLI tool itself at runtime. A malicious \`.dmai\` file can import \`os\`, delete files, or exfiltrate data.

**Fix:** Execute in a restricted namespace: \`exec(python_code, {\"__builtins__\": safe_builtins}, local_ns)\`" \
  --label "security,P0"

gh issue create --repo "$REPO" \
  --title "[BUG][P0] Transpiler replaces keywords inside string literals" \
  --body "**File:** \`maithili_dsl/transpiler/transpile.py\`

**Reproduction:**
\`\`\`
Input:  छपाउ(\"यह में है\")
Output: print(\"यह in है\")
\`\`\`

The word \`में\` inside quotes gets replaced with \`in\`. The transpiler uses naive \`str.replace()\` with no awareness of string boundaries.

**Fix:** Use tokenization or regex with negative lookbehind for quoted regions." \
  --label "bug,P0"

gh issue create --repo "$REPO" \
  --title "[BUG][P0] Transpiler replaces keywords inside longer words" \
  --body "**File:** \`maithili_dsl/transpiler/transpile.py\`

**Reproduction:**
\`\`\`
Input:  नवयुग = ५
Output: __init__युग = 5
\`\`\`

\`नव\` (maps to \`__init__\`) is matched as a substring inside \`नवयुग\`.

**Fix:** Use word-boundary-aware replacement for Devanagari script." \
  --label "bug,P0"

gh issue create --repo "$REPO" \
  --title "[LICENSE][P0] LICENSE file is incomplete — has placeholders" \
  --body "The LICENSE file contains:
- \`[Your Name]\` instead of the actual copyright holder
- \`[MIT terms continued...]\` instead of the full MIT license text

This means the project is technically unlicensed. Must be fixed immediately." \
  --label "compliance,P0"

echo "Creating P1 issues..."

gh issue create --repo "$REPO" \
  --title "[QUALITY][P1] No tests exist — add pytest suite" \
  --body "Zero test files in the project. Need unit tests covering:
- Transpiler keyword replacement
- Devanagari numeral conversion
- Linter rule checks
- CLI file loading
- Import translation

**Action:** Add \`tests/\` directory with pytest. Target >80% coverage on core modules." \
  --label "testing,P1"

gh issue create --repo "$REPO" \
  --title "[INFRA][P1] No CI/CD pipeline — add GitHub Actions" \
  --body "No automated checks on push or PR. Code can be merged without any validation.

**Action:** Add \`.github/workflows/ci.yml\` with:
- Python 3.8, 3.10, 3.12 matrix
- pytest
- flake8 or ruff lint
- Build validation (pip install .)" \
  --label "infra,P1"

gh issue create --repo "$REPO" \
  --title "[SECURITY][P1] No input validation before exec" \
  --body "\`run_dmai_file()\` reads any file and execs it with no guardrails.

**Action:** Add file size limits, execution timeout, and restricted builtins." \
  --label "security,P1"

gh issue create --repo "$REPO" \
  --title "[COMPLIANCE][P1] Add SECURITY.md for vulnerability reporting" \
  --body "No documented process for reporting security vulnerabilities. Open source projects need this.

**Action:** Add \`SECURITY.md\` with responsible disclosure instructions and contact info." \
  --label "compliance,P1"

gh issue create --repo "$REPO" \
  --title "[PACKAGING][P1] Add pyproject.toml (PEP 517/518)" \
  --body "Only \`setup.py\` exists. Modern Python tooling expects \`pyproject.toml\`.

**Action:** Add \`pyproject.toml\` with build-system, project metadata, and tool configs (pytest, mypy, ruff)." \
  --label "packaging,P1"

echo "Creating P2 issues..."

gh issue create --repo "$REPO" \
  --title "[BUG][P2] Linter false positives for Devanagari identifiers" \
  --body "**File:** \`maithili_dsl/transpiler/linter.py:65\`

\`is_snake_case()\` regex only matches ASCII — it will always fail for Devanagari variable names.

**Action:** Update naming checks to support Devanagari script identifiers." \
  --label "bug,P2"

gh issue create --repo "$REPO" \
  --title "[DOCS][P2] CONTRIBUTING.md has duplicated README content" \
  --body "The CONTRIBUTING.md file contains the full README.md pasted above the actual contributing guidelines.

**Action:** Remove duplicated content." \
  --label "docs,P2"

gh issue create --repo "$REPO" \
  --title "[QUALITY][P2] Add type hints to all public functions" \
  --body "No function signatures have type annotations.

**Action:** Add type hints. Add \`mypy\` to CI." \
  --label "quality,P2"

gh issue create --repo "$REPO" \
  --title "[COMPLIANCE][P2] Add CODE_OF_CONDUCT.md" \
  --body "Open source projects should have a code of conduct for community health.

**Action:** Add Contributor Covenant." \
  --label "compliance,P2"

gh issue create --repo "$REPO" \
  --title "[PACKAGING][P2] Define public API in __init__.py" \
  --body "Both \`__init__.py\` files are empty — no public API exported.

**Action:** Define \`__all__\` and export key functions." \
  --label "packaging,P2"

echo "Creating P3 issues..."

gh issue create --repo "$REPO" \
  --title "[DOCS][P3] README clone URL references 'youruser'" \
  --body "README says \`git clone https://github.com/youruser/maithili-dsl.git\` — should be \`alphacrack/python-maithili-dsl\`." \
  --label "docs,P3"

gh issue create --repo "$REPO" \
  --title "[FEATURE][P3] Add while loop support (जबतक)" \
  --body "No \`while\` keyword mapping exists. Only \`for\` (\`प्रत्येक\`) is supported.

**Action:** Add \`जबतक\` → \`while\` to \`DEVNAGIRI_KEYWORD_MAP\`." \
  --label "enhancement,P3"

gh issue create --repo "$REPO" \
  --title "[FEATURE][P3] Add try/except support for error handling" \
  --body "No exception handling keywords mapped.

**Action:** Add \`प्रयास\` → \`try\`, \`अपवाद\` → \`except\`, \`अंततः\` → \`finally\`." \
  --label "enhancement,P3"

gh issue create --repo "$REPO" \
  --title "[FEATURE][P3] REPL mode for interactive Maithili coding" \
  --body "Listed as a future goal in README but not started.

**Action:** Add \`python_maithili --repl\` interactive mode." \
  --label "enhancement,P3"

gh issue create --repo "$REPO" \
  --title "[INFRA][P3] Add requirements-dev.txt with pinned dev dependencies" \
  --body "No dependency pinning for dev tools.

**Action:** Add \`requirements-dev.txt\` with pytest, mypy, ruff versions pinned." \
  --label "infra,P3"

echo ""
echo "✅ All 19 backlog issues created successfully!"
