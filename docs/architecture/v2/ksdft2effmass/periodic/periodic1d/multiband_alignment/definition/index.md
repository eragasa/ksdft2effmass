# `ksdft2effmass.periodic1d.multiband_alignment.definition`

## Purpose and status

Implemented immutable M2 input contract. It freezes the rank-two block parent, training
and staggered evaluation meshes, retained rank, attack harmonics, hopping ranges, frame
thresholds, units, and verification controls.

## Public contract

- [`Periodic1DMultibandAlignmentCalculationDefinition`](Periodic1DMultibandAlignmentCalculationDefinition/index.md)

`withheld_reduced_momenta` constructs the disjoint $1/(N+1)$-offset evaluation mesh.

## Ownership and dependencies

The definition owns controls and validation only. It composes
`Periodic1DBlockHamiltonianToyModel`; it does not construct frames, optimize unitaries,
run the calculation, or accept evidence.

## Mapping and evidence

Source: `python/src/ksdft2effmass/periodic1d/multiband_alignment/definition.py`.
Direct evidence covers Boolean rejection, generic identity-attack acceptance,
immutability, and result binding.

## Limitations

M2 v1 is rank two and declares a finite attack/family. Its thresholds are numerical
controls, not physical uncertainty bounds.
