# M2 documentation amendment 2

This sidecar records documentation-only hardening. It changes no M2 input, prospective
control, numerical algorithm, retained numerical result, disposition, or scientific
claim.

- The retained `source.sha256` correlates with all 24 listed paths at identified commit
  `2e010d9f`.
- `protocol-amendment-2.json` records the source-docstring and documentation scope.
- `source-documentation-amendment-2.sha256` binds current source bytes after that
  hardening. It does not replace the historical execution-source record.
- `SHA256SUMS.documentation-amendment-2` seals the retained manifests, this amendment,
  and the current-source sidecar without rewriting retained `SHA256SUMS`.

Verify the sidecar boundary from this directory and the current source inventory from
the repository root:

```bash
shasum -a 256 -c SHA256SUMS.documentation-amendment-2
shasum -a 256 -c calculations/ICMSEP2026/conference/paper_1/multiband-alignment/source-documentation-amendment-2.sha256
```
