# `ksdft2effmass.model_systems.piab1d`

## Purpose and status

This implemented vertical slice composes a nondimensional one-dimensional
particle-in-a-box calculation around canonical PhysKit model, grid, Hamiltonian, and
eigensystem owners. KSD owns spectral reduction, diagnostics, convergence analysis,
independent verification, authenticated visualization projection, and calculation
provenance.

The maintained successor uses three direct scripts:

```text
run_01_calculation.py → run_02_verification.py → run_03_render.py
```

The scripts execute at module scope. They contain no Workflow, `main()` function,
argument parser, JSON-authored scientific input, generic study container, or duplicated
scientific kernel.

## Ownership

PhysKit owns:

- the PIAB1D continuum model;
- the homogeneous-Dirichlet full grid;
- the centered second-order finite-difference Hamiltonian;
- the represented eigensolution;
- quantity types; and
- canonical matrix norms.

KSD owns:

- typed PIAB1D configuration and result composition;
- Hamiltonian spectral reduction and KSD-specific residual meanings;
- convergence and retained-dimension selection composition;
- kinetic-potential decomposition under declared model classes;
- independent reconstruction and comparison composition;
- authenticated visualization data; and
- calculation-specific provenance and rendering policy.

## Implemented source map

```text
model_systems/piab1d/
├── configuration.py
├── result.py
├── diagnostics.py
├── visualization.py
└── analysis/
    ├── core.py
    ├── grid_sweep.py
    ├── residual_norms.py
    ├── finite_algebraic_diagnostics.py
    └── verification/
        ├── core.py
        ├── eigenpair_convergence.py
        ├── residual_norms.py
        ├── finite_algebraic_diagnostics.py
        ├── decomposition.py
        ├── reference.py
        ├── values.py
        └── verifier.py
```

The neighboring `study/` package supports exact historical retained-result contracts.
It does not own the direct successor design.

## Architectural invariants

- Every maintained scientific record is immutable and typed.
- Every matrix, vector, and scalar carries an explicit PhysKit unit.
- The successor uses the nondimensional convention declared by
  `UnitSystem.NONDIMENSIONAL` with `L = m = ℏ = 1`.
- Rectangular maps represent coordinate transformations; square Hamiltonian records
  validate represented operators.
- One eigensolution per grid supplies every sweep family.
- Verification reconstructs references without invoking production analyzers.
- Rendering consumes only digest-authenticated verification output.
- Each plot enum member has exactly one plotter.
- The closed rendering inventory contains 13 figures.
- Passing checks establish software and bounded numerical behavior only.

## Detailed pages

- [Implementation](implementation.md)
- [Numerical contract](numerics.md)
- [Scientific interpretation](scientifics.md)
- [Schematics](schematics.md)
