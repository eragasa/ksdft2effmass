# `ksdft2effmass.periodic1d.isolated_band.definition`

## Purpose and status

Implemented immutable input contract for M1. The module freezes the model,
discretization sweeps, reciprocal training/evaluation meshes, selected band, finite
ranges, units, seeds, and numerical tolerances before execution.

## Public contract

- [`Periodic1DIsolatedBandCalculationDefinition`](Periodic1DIsolatedBandCalculationDefinition/index.md)

`withheld_reduced_momenta` deterministically constructs the disjoint staggered mesh with
offset $1/(N+1)$, where $N$ is the training extent.

## Ownership and dependencies

The definition owns validation and controls only. It does not run eigensolvers, infer
ranges, inspect retained results, or make scientific acceptance decisions. It composes
`Periodic1DFourierHamiltonianToyModel` and unit-aware quantities.

## Mapping and evidence

Source: `python/src/ksdft2effmass/periodic1d/isolated_band/definition.py`.
Direct evidence is in `TestPeriodic1DIsolatedBandCalculator`, especially the sample-role,
unit, and Boolean-boundary tests. Public rendering is included from
`doc/sphinx/api/ksdft2effmass/periodic1d/isolated_band.rst`.

## Limitations

The finite plane-wave reference, meshes, and ranges are controls, not convergence or
physical-validity claims.
