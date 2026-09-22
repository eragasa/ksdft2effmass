# `ksdft2effmass.serialization` package

The public `ksdft2effmass.serialization` package owns nominal abstract contracts for
direct JSON wire conversion. `JsonSerializer[RecordT, WireT]` owns
`serialize(record)`, `JsonDeserializer[RecordT, WireT]` owns `deserialize(wire)`, and
`JsonCodec[RecordT, WireT]` combines matching directions. The wire type is closed to
`str` or `bytes`; the record type remains exact.

These ABCs own method shape only. Domain serializers continue to own schema versions,
canonicalization, units, compatibility, validation, and errors. The package does not
own generic domain parsing, filesystem access, persistence, scientific interpretation,
or execution authority.

Harness and application ActionObjects whose `execute` methods return ResultObjects do
not inherit these direct-value ABCs. Private canonical JSON mechanics likewise remain
implementation details. Periodic-1D `encode` and `decode` aliases are deprecated and
emit `DeprecationWarning`; `serialize` and `deserialize` are the supported methods.
