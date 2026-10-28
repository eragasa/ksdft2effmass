# `Periodic1DFourierLocalityIndependentVerification` numerics

The record contains a nonempty immutable mapping of uniquely named
`MaximumAbsoluteErrorComparison` values. It does not contain an expected result or a
visualization projection.

`Periodic1DFourierLocalityIndependentVerifier.execute()` constructs the mapping. Direct
NumPy formulas produce independent reference values for the declared scientific
channels; exact inventories and identifiers compare exactly, while binary64 values use
named unit-aware tolerances. Separate `visualization_...` comparisons correlate each
projection field with the corresponding field of the admitted result.

The record introduces no tolerance or threshold. Those values come from the admitted
configuration and are independently applied where the scientific reference formulas or
decision checks require them.
