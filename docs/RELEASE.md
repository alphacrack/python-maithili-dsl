# Release Process

This document describes how to cut a new release of `python_maithili`
to PyPI. The workflow is **`.github/workflows/publish.yml`** and uses
**Trusted Publishing (OIDC)** — no API tokens are stored in GitHub.

---

## One-time setup (required before the first publish succeeds)

### 1. Create GitHub Environments

In the repo, go to **Settings → Environments** and create two
environments — they give us a place to pin the OIDC trust and (for
production) an optional manual-approval gate.

#### `testpypi`
- No required reviewers.
- Deployment branches: all branches (we publish to TestPyPI from
  feature branches too).

#### `pypi`
- **Required reviewers**: add yourself. Every production publish will
  wait for explicit approval. This is the final safety gate.
- Deployment branches: protected tags matching `v*` only
  (`v[0-9]+.[0-9]+.[0-9]+` and `v[0-9]+.[0-9]+.[0-9]+-*`).

### 2. Register the Trusted Publisher on PyPI

Go to <https://pypi.org/manage/project/python-maithili/settings/publishing/>
(owner only) and add a new "Trusted publisher":

| Field               | Value                          |
|---------------------|--------------------------------|
| Owner               | `alphacrack`                   |
| Repository          | `python-maithili-dsl`          |
| Workflow filename   | `publish.yml`                  |
| Environment name    | `pypi`                         |

### 3. Register the Trusted Publisher on TestPyPI

TestPyPI doesn't have the project yet, so use a **pending publisher**.
Go to <https://test.pypi.org/manage/account/publishing/> and under
"Pending trusted publishers" add:

| Field               | Value                          |
|---------------------|--------------------------------|
| PyPI Project Name   | `python-maithili`              |
| Owner               | `alphacrack`                   |
| Repository          | `python-maithili-dsl`          |
| Workflow filename   | `publish.yml`                  |
| Environment name    | `testpypi`                     |

The pending publisher converts to a real one the first time a workflow
run successfully creates the project on TestPyPI.

---

## Routine release workflow

### A. Dry-run build (no publish)

Push a PR or run **Actions → Publish to PyPI → Run workflow → `build-only`**.
This executes the full pipeline except the publish step:

- Build sdist + wheel.
- `twine check --strict` metadata validation.
- Install the wheel in a clean venv.
- Run the full pytest suite against the installed wheel.
- Upload the `dist/` artifact for inspection.

No credentials are required and nothing touches the network package
indexes. Use this whenever you want to confirm the package will build.

### B. Publish to TestPyPI (staging verification)

Two ways to trigger:

1. **Manual**: Actions → Publish to PyPI → Run workflow → `testpypi`.
2. **Automatic**: create a GitHub **pre-release** (check "This is a
   pre-release" when making the Release). Tag format: `v0.X.Y-rc1`,
   `v0.X.Y-dev1`, etc.

Version numbers you publish to TestPyPI are **separate** from
production PyPI — TestPyPI has its own index. Verify the install:

```bash
pip install \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  python-maithili==0.X.Y
python_maithili --version
```

Any version on TestPyPI cannot be re-used. If you need to iterate,
bump the version (`0.3.0.dev0`, `0.3.0.dev1`, ...) in
`maithili_dsl/__init__.py` before re-triggering.

### C. Publish to production PyPI

**Pre-flight checklist:**

- [ ] `CHANGELOG.md` has a section for the new version with date filled in.
- [ ] `maithili_dsl/__init__.py` has `__version__` set to the new version.
- [ ] `pyproject.toml` has matching `version = "..."`.
- [ ] `pytest` runs green on `main` CI.
- [ ] The same version was successfully published to TestPyPI and installed
      cleanly (step B).

**Cut the release:**

1. Ensure `main` has the final release commit on it (all three version
   strings updated, CHANGELOG finalized).
2. Create a new **GitHub Release** (not a pre-release):
   - Tag: `v0.X.Y` (must match `__version__` exactly; the workflow
     enforces this and refuses to publish on mismatch).
   - Target: `main`.
   - Title: `v0.X.Y`.
   - Body: the corresponding CHANGELOG section.
   - Leave "This is a pre-release" **unchecked**.
3. Click **Publish release**. The workflow fires.
4. If the `pypi` environment has required reviewers, approve the
   deployment in the Actions run.
5. After the run finishes, verify:

   ```bash
   pip install python-maithili==0.X.Y
   python_maithili --version
   ```

---

## Version bump convention

This project uses [Semantic Versioning](https://semver.org/):

| Change                                         | Bump  |
|------------------------------------------------|-------|
| Breaking API change (exit code semantics, etc) | MAJOR |
| New keyword / module / feature                 | MINOR |
| Bugfix, doc change, internal refactor          | PATCH |

Version is tracked in three places that must stay in sync:

1. `maithili_dsl/__init__.py` — `__version__` (single source of truth).
2. `pyproject.toml` — `version`.
3. `CHANGELOG.md` — section header and date.

The publish workflow's "Verify release tag matches package version"
step will fail the production publish if these drift.

---

## Recovery: what if a bad version reaches PyPI?

PyPI does not allow re-uploading the same filename. If you published
a broken release:

1. **Yank** (do not delete) the broken version on PyPI:
   <https://pypi.org/manage/project/python-maithili/releases/> →
   pick the version → "Yank release". This hides it from `pip install`
   without breaking already-pinned consumers.
2. Bump PATCH and release the fix via the normal flow above.
