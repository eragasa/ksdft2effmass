# `PeriodicUniformGrid1D`

**Defined in:** `ksdft2effmass.periodic1d.finite_differences`

## Role

Immutable ordered grid on one half-open periodic cell. Coordinates are
`origin + j * period / point_count` for `j = 0, ..., point_count - 1`; the endpoint is
not duplicated.

## Invariants and evidence

Origin and period units are compatible, period is positive, and point count is an exact
built-in integer of at least three. `test__PeriodicUniformGrid1D.py` checks unit
conversion, immutable half-open coordinates, and minimum size. This is representation
software evidence, not discretization convergence.
