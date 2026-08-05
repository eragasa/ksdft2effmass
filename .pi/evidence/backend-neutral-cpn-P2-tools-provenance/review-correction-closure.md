# P2 correction closure: **FAIL**

Most recorded findings are closed:

- raw credential-bearing fields removed;
- attempt/retry lineage and attempt correlation added;
- real calendar validation added;
- derived result statuses remove schema/runtime contradictions;
- validators are owner-local;
- public string enums are documented `StrEnum`;
- stale P2 and 14-page MyST status text corrected;
- R2/E2 hashes and recorded commands pass.

## Residual findings

### HIGH — Diagnostic paths accept a single backslash

`python/src/ksdft2effmass/provenance/tools.py:84` checks:

```python
if "\\\\" in text
```

That string represents **two** consecutive backslashes. Consequently, a single backslash is accepted:

```text
ExternalExecutionFailure(..., diagnostic_paths=("diag\\stderr.txt",), ...)
→ accepted
```

This contradicts:

- schema rejection at `specification/provenance/v1/provenance-v1.schema.json:424-430`;
- public contract at `docs/api/provenance.md:92-96`;
- user guide at `docs/user-guide/provenance-and-artifacts.md:59`;
- the test requirement at `test__ExternalExecutionFailure.py:76-91`, which does not include a backslash case.

Thus H1/H2 path behavior and schema/runtime synchronization remain unresolved.

### MEDIUM — R2 does not bind all corrected documentation/control artifacts

R2 calls itself the “post-review corrected source-schema-test-documentation” boundary at `replay-inputs.json:4-7`, but its documentation inventory at `:20-39` includes only five P2 pages. It omits corrected stale-status/MyST files such as:

- `docs/api/workflows-cpn.md`
- `docs/concepts/cpn-contract.md`
- `docs/user-guide/colored-petri-nets.md`
- `docs/user-guide/dft-backends.md`
- `docs/user-guide/external-dependencies.md`
- `docs/user-guide/installation.md`
- `docs/verification/cpn-contract.rst`
- expanded `task-ownership.json`

R2/E2 itself is internally consistent: input hash `10b16c…774c`, zero mismatches, status PASS.

### Validation note

The maintained local harness route returned **FAIL**, despite its replay subprocess exiting zero. Direct P2 checkpoint, ownership, and completion validators passed. This route failure is residual validation risk; no harness files were changed or investigated beyond the read-only result.