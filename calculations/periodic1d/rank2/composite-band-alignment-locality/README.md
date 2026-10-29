# Periodic-1D rank-two composite-band alignment and locality

## Identity and status

This directory is the maintained calculation and protocol home for

```text
ksdft2effmass.campaign.periodic-reduction.periodic1d.composite-band-alignment-and-locality
```

The family now has a direct, typed, publication-independent implementation. Its three
tracked protocol documents formerly lived under
`experiments/periodic-reduction/composite-band-alignment-and-locality/`. They are now
assigned here, with predecessor identities and remaining work recorded in
[`migration.md`](migration.md). No retained execution has been created.

This family is distinct from the existing rank-two
[`band-equivalence-versus-hopping-locality`](../band-equivalence-versus-hopping-locality/README.md)
model-adequacy calculation. Shared reusable operations do not collapse the scientific
identities, inputs, thresholds, schemas, verification routes, or evidence policies of
the two families.

## Complete local inventory

| Surface | Current disposition |
|---|---|
| [`protocol.md`](protocol.md) | Frozen direct scientific and numerical contract; not an immutable retained experiment version. |
| [`migration.md`](migration.md) | File-level predecessor crosswalk and implementation/evidence ledger. |
| [`monograph-donor-crosswalk.md`](monograph-donor-crosswalk.md) | Exact ten-file donor, 19-consumer, digest, and scientific-channel disposition audit. |
| [`m2-parity.md`](m2-parity.md) | Named in-memory finite parity and explicit convention-adaptation record; not retained evidence. |
| [`technical-report/`](technical-report/README.md) | Comprehensive upstream provisional report, three authenticated review figures, bibliography, compiled review snapshot, and reproducible figure adapter; not retained evidence. |
| `run_01_calculation.py` | Direct calculate adapter; creates one new unsealed execution atomically and refuses overwrite. |
| `run_02_verification.py` | Direct byte-owning verification adapter; independently reconstructs all numerical channels. |
| `run_03_render.py` | Direct authenticated render adapter; publishes the closed three-PNG alignment, locality, and error-channel inventory atomically. |
| `python/src/ksdft2effmass/periodic1d/composite_band_alignment/` | Typed configuration, result, pure analysis, independent verification, authenticated visualization, and public exports. |
| [`../phase-3-split-audit.md`](../phase-3-split-audit.md) | Exact live-M2 recovery/consumer inventory, two-family channel split, parity gaps, implementation order, and removal gates. |
| `python/src/ksdft2effmass/periodic1d/multiband_alignment/` | Six-file live predecessor package; direct scientific successor is this family, but removal is blocked by M3 consumers. |
| `python/src/ksdft2effmass/periodic1d/admissible_sets/` | Direct M3 consumer of the M2 definition, producer, result, and verifier; migration belongs to Phase 4. |
| Historical `ksdft2effmass.experiments.multiband` package at `c5d34a93b4710a4a430738c404c775865d418d42` | Removed donor containing M2/M3 schemas, producer, verifier, quadratics, and rendering routes; recover definitions selectively, not the package wholesale. |
| Historical research-monograph periodic-1D package at the same revision | Removed donor containing composite, stress, extraction, and verification routes plus historical execution outcomes. |
| [`docs/tasks/tech_debt/composite-band-alignment-and-locality/`](../../../../docs/tasks/tech_debt/composite-band-alignment-and-locality/index.md) | Design and migration rationale; not the maintained calculation owner. |
| Immutable versions, retained calculation runs, and publication evidence | Absent. |

## Selected scientific contract

The prospective calculation owns the following concrete choices unless a later reviewed
protocol revision states otherwise:

- a one-dimensional inversion-symmetric periodic family;
- a rank-two parent fiber and a rank-two retained subspace;
- exact synthetic source and evaluation meshes with explicit construction/evaluation
  separation;
- a declared inter-sample alignment objective and tie policy;
- projectability, conditioning, energy-reference, gauge, and frame-transport conventions;
- explicit cyclic-conversion power and separately named interpolation, deliberate-truncation, and total Hamiltonian and spectral diagnostics;
- independent reconstruction and verification of decisive quantities;
- strict typed input/result/verification records and byte-owning provenance;
- bounded interpretation that does not claim continuum convergence, material validity, or
  publication acceptance.

The implementation is complete as a bounded software lifecycle, but the protocol is not
an immutable scientific version and does not authorize a retained calculation. Passing
software and numerical checks does not establish continuum convergence, material
validity, uncertainty quantification, publication acceptance, release, or sealing.

## Ownership boundary

Reusable finite-periodic, represented-linear-algebra, and unit-free optimization
behavior must be consumed directly from its reviewed owner. The calculation owns its
parent definition, sampling roles, alignment and locality composition, threshold policy,
wire schemas, verification sequencing, provenance, and interpretation. Calculation
scripts remain explicit effect adapters and must not become a second installable source
tree.

No installed package may import this calculation tree. Nothing here authorizes external,
remote, Quantum ESPRESSO, Wannier90, production, confirmatory, retained-evidence,
sealing, release, or publication execution.
