# `ksdft2effmass.model_systems.qho1d`

## Purpose and status

This vertical slice compares the nondimensional real-line harmonic oscillator, its
finite homogeneous-Dirichlet centered-difference representation, and an exact retained
number-state Hamiltonian after explicit common-coordinate alignment.

The maintained successor composes:

```text
run_01_calculation.py → run_02_verification.py → run_03_render.py
```

The scripts execute at module scope and contain no Workflow, `main()` function,
argument parser, JSON-authored scientific input, or reusable scientific kernel.

## Ownership

QHO1D model owners provide analytical number states, the finite harmonic Hamiltonian,
ladder operators, and the sampled-state comparison. The direct calculation owner
provides typed sweep composition, independent reference reconstruction, authenticated
visualization projection, execution correlation, and report/rendering policy.

Shared KSD infrastructure owns typed JSON records, maximum-error comparisons, aggregate
verification, PNG admission, and final representation boundaries.

## Implemented source map

```text
model_systems/qho1d/
├── model.py
├── comparison.py
├── configuration.py
├── result.py
├── analysis.py
├── verification_values.py
├── verification.py
└── visualization.py
```

The neighboring `study/` package supports historical JSON-authored calculation
contracts. It is not used by the direct successor.

## Invariants

- Maintained successor records are immutable and typed.
- All numerical values carry explicit `Unitless()` quantities under the declared
  nondimensional convention.
- The injection maps retained number-state coordinates into ordered finite-grid
  coordinates.
- Verification evaluates Hermite functions and constructs the finite Hamiltonian
  independently of production analyzers.
- Rendering consumes only a passing verification that authenticates the exact
  visualization projection.
- The closed rendering inventory contains three figures.
- Passing checks establish bounded software and numerical behavior only.

## Detailed pages

- [Implementation](implementation.md)
- [Numerical contract](numerics.md)
- [Scientific interpretation](scientifics.md)
- [Schematics](schematics.md)
