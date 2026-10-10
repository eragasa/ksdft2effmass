# `ksdft2effmass.periodic1d.multiband_alignment.results`

## Purpose and status

Implemented immutable result contracts for M2 diagnostics, range-resolved locality, and
aggregate correlation.

## Public contract

- [`Periodic1DMultibandAlignmentDiagnostics`](Periodic1DMultibandAlignmentDiagnostics/index.md)
- [`Periodic1DMultibandAlignmentRangeResult`](Periodic1DMultibandAlignmentRangeResult/index.md)
- [`Periodic1DMultibandAlignmentCalculationResult`](Periodic1DMultibandAlignmentCalculationResult/index.md)

## Ownership and invariants

The records distinguish projector, pointwise frame, globally constrained frame,
represented-operator, attack-recovery, and hopping-range channels. Aggregate construction
binds the exact definition, mesh, unit, threshold, transform, and target identities.

## Mapping and evidence

Source: `python/src/ksdft2effmass/periodic1d/multiband_alignment/results.py`.
Every M2 execution, tamper, serializer, and verifier test exercises these correlations.

## Limitations

Result records summarize a finite synthetic protocol and do not encode material
acceptance, uncertainty, or a universal gauge-locality theorem.
