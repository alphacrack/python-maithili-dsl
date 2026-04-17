<!--
Thanks for contributing to python_maithili! Please fill in this template
so reviewers can evaluate the change quickly. Delete sections that do
not apply.
-->

## Summary

<!-- What does this PR do, in 1–3 sentences. -->

## Motivation / Audit Reference

<!-- Link the BACKLOG.md item or AUDIT_REPORT.md finding this PR closes
     (e.g. "Closes SEC-001", "Addresses P1 item #5"). -->

## Test Evidence

- [ ] `pytest -v` runs green locally
- [ ] Coverage is at or above the critical-module gate (cli / transpile / linter ≥90%)
- [ ] New tests added for any new behavior or regression
- [ ] `python -m maithili_dsl examples/*.dmai` smoke-tested the examples
- [ ] `python -m maithili_dsl --version` shows the expected version

<!-- Paste the tail of `pytest` output, or the commit that updated tests. -->

## Security Considerations

<!-- If this PR touches cli.py, the transpiler's string handling, the
     import whitelist, or the safe-builtins list, explain the threat
     model you considered. Otherwise write "N/A". -->

## Breaking Changes

<!-- List any behavior changes that users or CI consumers would notice.
     If none, write "None". -->

## Checklist

- [ ] CHANGELOG.md updated (Unreleased section)
- [ ] Version bumped if this is a release PR
- [ ] No new runtime dependencies added (or justification provided below)
- [ ] Docs updated if user-visible behavior changed
