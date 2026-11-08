# Arb enclosure records

`records.py` owns immutable, provider-result values without importing Python-FLINT:

- [`SignedExactInterval`](SignedExactInterval/index.md)
- [`ControlledParentLowestEigenvalueEnclosure`](ControlledParentLowestEigenvalueEnclosure/index.md)
- [`MediatedMaximumErrorEnclosure`](MediatedMaximumErrorEnclosure/index.md)

The records use `BaseTypedRecord` canonical serialization and claim no containment beyond
the producer action that constructs them.

[Back to the Arb capability](../index.md)
