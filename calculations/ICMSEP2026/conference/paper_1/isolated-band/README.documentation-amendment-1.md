# M1 documentation amendment 1

This sidecar describes a post-result documentation and provenance amendment. It does
not change `input.json`, `protocol.md`, `result.json`, numerical controls, numerical
results, or scientific claims.

- `protocol-amendment.json` records the documentation scope and the pre-existing
  `source.sha256` correlation defect.
- The retained `source.sha256` does not correlate with identified commit `ee89d347`:
  two listed files have different committed digests and `periodic1d/studies.py` is
  absent. The cause is not established. The retained manifest must therefore not be
  presented as proof of the exact committed producer tree.
- `source-documentation-amendment-1.sha256` binds the current source inventory after
  documentation hardening. It is not asserted to be the source that produced the
  retained result.
- `SHA256SUMS.documentation-amendment-1` seals the retained manifests, this amendment,
  and the current-source sidecar without rewriting the retained `SHA256SUMS`.

From this directory, verify the sidecar package boundary with:

```bash
shasum -a 256 -c SHA256SUMS.documentation-amendment-1
```

From the repository root, verify the current source inventory with:

```bash
shasum -a 256 -c calculations/ICMSEP2026/conference/paper_1/isolated-band/source-documentation-amendment-1.sha256
```
