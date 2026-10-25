# QHO1D authored inputs

The direct QHO1D lifecycle declares scientific and algorithmic controls visibly in
`../run_01_calculation.py`. It does not read a JSON-authored scientific input.

During calculation, the typed `Qho1dConfiguration` is serialized through the shared
`BaseTypedRecord` JSON boundary and copied to the execution as
`inputs/configuration.json`. That execution copy is an output record of the authored
configuration, not an alternative source of authority.
