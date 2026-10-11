# M3 documentation amendment 10

This sidecar records documentation-only hardening. It changes no M3 input, prospective
threshold, numerical algorithm, retained numerical result, certificate, disposition, or
scientific claim.

The corrected documentation distinguishes the continuous rectangle in
`(energy_shift_ratio, splitting_scale)` from the finite nine-angle global-rotation
inventory. It also describes the retained certificate as a splitting-axis gap that
lower-bounds Euclidean separation, not as arbitrary-direction support-function
optimization.

- `protocol-amendment-10.json` records the scope and non-effects.
- `source-documentation-amendment-10.sha256` binds current M3 and composed M2 source
  bytes after documentation hardening.
- `SHA256SUMS.documentation-amendment-10` seals the retained manifests, this amendment,
  and the current-source sidecar without rewriting retained `SHA256SUMS` or changing the
  digest consumed by the post-hoc sensitivity package.

Verify the sidecar boundary from this directory and the current source inventory from
the repository root:

```bash
shasum -a 256 -c SHA256SUMS.documentation-amendment-10
shasum -a 256 -c calculations/ICMSEP2026/conference/paper_1/constrained-admissible-sets/source-documentation-amendment-10.sha256
```
