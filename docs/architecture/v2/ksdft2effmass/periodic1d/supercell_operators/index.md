# `ksdft2effmass.periodic1d.supercell_operators`

## Responsibility

Own the explicit-input, lossless `PERIODIC-XWALK-030` route from represented
periodic-1D supercell metadata and a dense matrix to the general
`ksdft2effmass.operators.OperatorRecord`.

## Public classes

- [`Periodic1DSupercellOperatorProvenance`](Periodic1DSupercellOperatorProvenance/index.md)
- [`Periodic1DSupercellOperatorMetadata`](Periodic1DSupercellOperatorMetadata/index.md)
- [`Periodic1DSupercellOperatorConstructor`](Periodic1DSupercellOperatorConstructor/index.md)

## Unavailable-data boundary

The caller must provide explicit three-dimensional cell vectors, exact ordered
per-state labels, energy and coordinate conventions, stable identities, and structured
provenance. Historical artifacts lacking these values remain unmigrated. Dimensions,
ordering descriptions, paths, file names, hashes, group IDs, and spectra are never
used to reconstruct them.
