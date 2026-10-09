# `Periodic1DSupercellOperatorConstructor`

**Defined in:** `ksdft2effmass.periodic1d.supercell_operators`

## Role

Action that combines an exact record identity, operator kind, complete explicit
supercell metadata, and dense matrix into the general immutable `OperatorRecord`.
`OperatorRecord` remains the represented-operator owner; campaign envelopes may
compose it but do not own duplicate matrix semantics.

## Complexity and failures

For dimension `N`, defensive complex128 storage requires `O(N^2)` time and memory.
There is no arbitrary size cap. Invalid semantic types, nonfinite or incompatible
shapes, unrepresentable numeric values, and allocation failure remain distinct error
boundaries.

## Evidence

`test__Periodic1DSupercellOperatorConstructor.py` checks exact transfer of labels,
cell vectors, provenance, matrix values, and immutability plus dimension mismatch
rejection. These checks do not authenticate provenance or establish convergence or
scientific validity.
