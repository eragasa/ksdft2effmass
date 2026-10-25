# `ksdft2effmass.serialization` package

The public `ksdft2effmass.serialization` package owns nominal abstract contracts for
direct JSON wire conversion and temporarily incubates the reusable typed scientific
value codec intended for later migration to PhysKit. `JsonSerializer[RecordT, WireT]` owns
`serialize(record)`, `JsonDeserializer[RecordT, WireT]` owns `deserialize(wire)`, and
`JsonCodec[RecordT, WireT]` combines matching directions. The wire type is closed to
`str` or `bytes`; the record type remains exact. `TypedJsonMappingSerializer` and
`TypedJsonMappingDeserializer` are the generic concrete byte actions for typed
scientific mappings. Final record boundaries compose them as
`to_json -> to_dict -> serialize` and
`from_json -> deserialize -> from_dict`; domain records do not implement JSON
normalization.

These ABCs own method shape only. `TypedJsonValueCodec` separately owns recursive,
reversible JSON normalization for fixed-width numeric NumPy values, canonical SciPy
CSR values, PhysKit model-system units and quantities, registered enums, tuples,
mappings, and records exposing typed mappings. It performs no dynamic imports.
Model-system packages compose these reusable values and must not duplicate their wire
conversion.

Domain records continue to own their schema, correlated scientific invariants, units,
compatibility, validation, and errors. The package does not own filesystem access,
persistence, scientific interpretation, or execution authority. Once the typed-value
contract stabilizes, PhysKit should own it and KSD should consume it directly rather
than retain a compatibility facade.

Application ActionObjects whose `execute` methods return ResultObjects do not
inherit these direct-value ABCs. Private canonical JSON mechanics likewise remain
implementation details. Periodic-1D `encode` and `decode` aliases are deprecated and
emit `DeprecationWarning`; `serialize` and `deserialize` are the supported methods.
