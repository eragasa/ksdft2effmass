# `ksdft2effmass.serialization` package

The public `ksdft2effmass.serialization` package owns nominal abstract contracts for
direct JSON wire conversion. Its [`json`](json/index.md) child owns strict decoding and
[recursively immutable JSON values](json/immutable/index.md). `JsonSerializer[RecordT, WireT]` owns
`serialize(record)`, `JsonDeserializer[RecordT, WireT]` owns `deserialize(wire)`, and
`JsonCodec[RecordT, WireT]` combines matching directions. The wire type is closed to
`str` or `bytes`; the record type remains exact.

These ABCs own method shape only. The JSON child owns wire-level strictness,
immutability, and canonical byte mechanics. Domain serializers continue to own schema
versions, scientific fields, units, compatibility, source authentication, provenance,
and errors. The package does not own filesystem access, persistence, scientific
interpretation, or execution authority.

Application ActionObjects whose `execute` methods return ResultObjects do not inherit
these direct-value ABCs. Direct codecs use only `serialize` and `deserialize`; domain
packages do not add compatibility forwarding aliases.
