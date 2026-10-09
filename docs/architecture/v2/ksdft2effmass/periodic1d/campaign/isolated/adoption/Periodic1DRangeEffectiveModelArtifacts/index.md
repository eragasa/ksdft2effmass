# `Periodic1DRangeEffectiveModelArtifacts`

## Purpose and status

This implemented row-023 retained-evidence DataObject keeps replayed truncation and
direct-fit coefficient models separate for one symmetric hopping range.

## Contract

`hopping_range_cells` is a nonnegative exact integer. Both `BlockHoppingModel1D`
records are scalar and contain exactly representatives `-r, ..., r`. Separate lowercase
SHA-256 identities bind the canonical truncated and fitted coefficient arrays. The
record does not assert that the two routes are equal or scientifically adequate.

## Evidence and limitations

The sidecar decoder authenticates the coefficient bytes. Scientific adoption reruns the
separate truncation and least-squares Actions and compares each candidate against its
matching replay inventory under a retained allowance. The route-separation and
contradictory-range tests provide bounded software evidence.

The coefficients describe effective models of a finite represented retained operator.
They do not establish parent-model accuracy, physical transferability, validation, UQ,
or acceptance.
