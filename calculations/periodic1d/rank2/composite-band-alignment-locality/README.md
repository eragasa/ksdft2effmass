# Periodic-1D rank-two composite-band alignment and locality

## Identity and status

This directory is the maintained calculation and protocol home for

```text
ksdft2effmass.campaign.periodic-reduction.periodic1d.composite-band-alignment-and-locality
```

The family is a prospective periodic-1D rank-two successor. Its three tracked protocol
documents formerly lived under
`experiments/periodic-reduction/composite-band-alignment-and-locality/`. They are now
assigned here, with predecessor identities and remaining work recorded in
[`migration.md`](migration.md).

This family is distinct from the existing rank-two
[`band-equivalence-locality`](../band-equivalence-locality/README.md) model-adequacy
calculation. Shared reusable operations do not collapse the scientific identities,
inputs, thresholds, schemas, verification routes, or evidence policies of the two
families.

## Complete local inventory

| Surface | Current disposition |
|---|---|
| [`protocol.md`](protocol.md) | Exact migrated prospective protocol; selected controls and outstanding freeze points. |
| [`migration.md`](migration.md) | File-level predecessor crosswalk and actionable implementation/evidence ledger. |
| `python/src/ksdft2effmass/periodic1d/multiband_alignment.py` | Current reusable rank-two alignment-analysis surface to audit for direct canonical use. |
| `python/src/ksdft2effmass/periodic1d/campaign.py` | Current campaign-side composition surface requiring ownership reconciliation. |
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
- support-depth locality diagnostics and separately named spectral diagnostics;
- independent reconstruction and verification of decisive quantities;
- strict typed input/result/verification records and byte-owning provenance;
- bounded interpretation that does not claim continuum convergence, material validity, or
  publication acceptance.

The protocol remains prospective. It is not an immutable scientific version and does
not authorize a retained calculation.

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
