# Periodic-1D composite-band alignment/locality migration

This checklist belongs to the complete inventory in [`README.md`](README.md).

## Experiment-tree migration

Baseline source revision:
`40c84109bfd49718f1519f9bfd298f5ef90ddac0`.

| File | Baseline source SHA-256 | Migration disposition |
|---|---|---|
| `README.md` | `9018232866cd9648f2cb34f5335be7f8002064aba967423ba8d6ec0704b8415d` | Family/container ownership content integrated into this README; predecessor remains recoverable. |
| `periodic1d/README.md` | `3af8505cc93011c39521f5eebf27baef9ef6616ae45c3ab0db619506309728b4` | Periodic-1D identity, scientific status, and ownership content integrated into this README; predecessor remains recoverable. |
| `periodic1d/protocol.md` | `e62226605cb34a9f7449e33d57860a36d00fb91ed7d44f9eb47fcd5bf901c3a7` | Exact-byte move to `protocol.md`. |

- [x] Assign the experiment family to this calculation owner.
- [x] Record the three tracked files in the experiment family/container.
- [x] Create the file-by-file source → destination/disposition crosswalk above.
- [x] Migrate the family/container README and periodic-1D protocol content into this calculation surface.
- [x] Update maintained inventory, technical-debt, higher-rank, and publication consumers to the calculation path and current migration status.
- [x] Confirm no maintained link or executable consumer depends on the removed experiment path; remaining textual occurrences identify migration provenance.
- [x] Remove the experiment files after explicit migration authorization while preserving predecessor recovery above.

## Scientific and source migration

- [x] Record the live M2 revision, package tree, file/blob/content hashes, schemas,
  direct M3 consumers, and historical Conference Paper 1 package identities in
  [`../phase-3-split-audit.md`](../phase-3-split-audit.md).
- [x] Classify the live and historical M2 fields and diagnostics as adopted, adapted,
  rejected, or provenance-only between the composite and band-equivalence successors in
  [`../phase-3-split-audit.md`](../phase-3-split-audit.md).
- [x] Record exact revisions, blobs, SHA-256 identities, controls, schemas, and 19
  literal consumers for the separate monograph composite donor in
  [`monograph-donor-crosswalk.md`](monograph-donor-crosswalk.md).
- [x] Resolve eigensystem, Procrustes, and transport selection ownership: PhysKit owns
  dense complex-Hermitian eigensystems, Optimization owns batched unitary Procrustes,
  and KSD owns frame transport and scientific composition.
- [x] Freeze the exact parent coefficients, lowest rank-two space, 64/257 disjoint
  meshes, right action, three transform channels, one global diagnostic channel,
  ranges, units, tolerances, maximum rank-cutoff rule, and fail-closed rank policy.
- [x] Consume reusable source owners directly without importing historical campaigns or
  calculation-local workflow packages.
- [x] Define immutable constructor-owned configuration, section, and root result
  records with explicit mappings and concise aggregate correlation.
- [x] Define canonical typed JSON and exact record-owned field inventories; no parallel
  handwritten schema-v1 artifact is retained.
- [x] Implement a byte-owning independent verifier that does not invoke the producer or
  the Optimization alignment solver.
- [x] Implement explicit negative-Nyquist conversion power and separate disjoint-mesh
  interpolation, deliberate-truncation, and total channels in normalized Hamiltonian
  and sorted-band metrics.
- [x] Implement verifier-authenticated visualization data and the closed
  `rank2-composite-alignment.png` / `rank2-composite-locality.png` /
  `rank2-composite-error-channels.png` inventory using
  `ModelAnalysisPngFigureRenderer`.
- [x] Establish named finite M2 parity and explicit convention adaptations in
  [`m2-parity.md`](m2-parity.md); classify monograph channels as adopted, adapted,
  rejected, or provenance-only.
- [x] Preserve historical bytes and checksum chains unchanged and keep historical
  publication/evidence consumers bound to them.
- [x] Author and build the comprehensive upstream provisional technical report with
  literature positioning, exact analytic consequences, seven benchmarks, full finite
  results, authenticated figures, independent verification, historical parity,
  publication relationship, provenance, and explicit nonclaims.
- [ ] Complete independent review of the direct lifecycle before proposing any retained
  execution.

## Deliberate non-removal

The live `periodic1d.multiband_alignment` predecessor remains installed. Its six direct
M3 admissible-set consumers still block removal, as recorded by the Phase 3 split audit.
This successor does not wrap or facade that dependency. Phase 4 must migrate those
consumers to authenticated upstream bytes and digests before predecessor retirement.
