# `Periodic1dRank1Calculator`

## Status and responsibility

Implemented calculation-owned, read-only composition in [`calculator.py`](calculator.py).

```python
source = Periodic1DFourierLocalityCalculationResult.from_json(result_bytes)
geometry = Periodic1DLatticeGeometry(1.0, PhysicalUnit("bohr"))
result = Periodic1dRank1Calculator(
    source_calculation=source,
    lattice_geometry=geometry,
).result()
```

The calculator restores the maintained `periodic1d.rank1` capability composition around
one exact typed Fourier-locality result. It does not duplicate reusable rank-one
implementation in the calculation tree.

## Inputs

The calculator requires:

1. one exact `Periodic1DFourierLocalityCalculationResult`; and
2. one explicit `Periodic1DLatticeGeometry`.

The retained predecessor result is dimensionless and does not store a physical direct
lattice. Consequently, geometry must be supplied by the current caller. Selecting
`1 bohr` reproduces the installed reduced-coordinate convention as a new explicit
correlation; it does not rewrite or retroactively reinterpret retained JSON bytes.

## Composition

The calculator selects the unique source mesh whose construction size equals
`configuration.production_construction_size`. It then composes:

- the unchanged source calculation as rank-one band equivalence;
- `Periodic1DRank1AlignmentApplicabilityAnalyzer` for the exact operator-trivial `U(1)`
  disposition;
- `Periodic1DRank1HoppingLocalityAnalyzer` for descriptive complete-coefficient tails;
  and
- `Periodic1DRank1SupportTruncationAnalyzer` for deliberate support-removal
  consequences.

Hopping locality and support truncation remain distinct views over the same exact source
mesh. The calculator does not infer one from the other or merge their meanings.

## Correlation invariants

`Periodic1dRank1CalculationResult` requires:

- exact maintained owner types;
- one production mesh retained by source-object identity;
- alignment bound to the exact source configuration;
- locality and truncation bound to the exact source calculation and production mesh;
- one shared explicit lattice geometry; and
- scalar band-subspace rank one.

Structurally equal reconstructed values are insufficient where identity correlation is
required.

## Schematic

```mermaid
flowchart LR
    B[retained typed result bytes] --> D[typed result admission]
    D --> C[Periodic1dRank1Calculator]
    G[explicit lattice geometry] --> C
    C --> P[unique production mesh]
    C --> A[operator-trivial U(1) applicability]
    P --> L[descriptive hopping-locality tails]
    P --> T[support-truncation consequences]
    D --> R[Periodic1dRank1CalculationResult]
    G --> R
    P --> R
    A --> R
    L --> R
    T --> R
```

## Persistence and evidence boundary

The calculator is an in-memory projection and introduces no serialization schema. It
performs no filesystem writes, external execution, evidence promotion, or publication
qualification. The retained execution remains byte-identical and unsealed.

Passing calculator tests establishes exact software correlation only. It does not
establish continuum convergence, a globally isolated band, physical material adequacy,
uncertainty quantification, or scientific acceptance.
