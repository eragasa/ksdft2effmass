# Encoded periodic-1D result documents

This package-level design surface owns the closed, immutable JSON representation used
to preserve complete Appendix G periodic-1D result wires. It is supporting campaign
infrastructure, not a physical model, finite representation, retained space, represented
operator, effective model, or scientific conclusion.

## Owned types

- [`Periodic1DEncodedResultDocument`](./Periodic1DEncodedResultDocument/index.md)
  binds one explicit wire kind, complete immutable decoded tree, exact source bytes, and
  SHA-256 source identity;
- `Periodic1DEncodedResultKind` enumerates the six explicitly supported historical wire
  identities; and
- `Periodic1DEncodedResultJsonSerializer` strictly decodes one configured kind and emits
  a deterministic canonical JSON representation by composing the shared
  [`ImmutableJsonCodec`](../../../serialization/json/immutable/index.md).

The former periodic-specific `Periodic1DJsonArray`, `Periodic1DJsonObject`,
`Periodic1DJsonScalar`, and `Periodic1DJsonValue` names are retired without aliases.
Reusable closed immutable JSON values belong to
`ksdft2effmass.serialization.json`; they assign no units, basis, gauge, state space,
operator meaning, provenance, result kind, or scientific identity.

## Boundaries

The serializer receives the wire kind explicitly. It does not infer kind, source-file
presence, provenance, or meaning from filenames, paths, identifiers, fields, ranks, or
shapes. Deserialization retains the source bytes exactly and derives their digest;
serialization emits canonical JSON bytes and does not claim byte equality with a
noncanonical source.

Filesystem location, artifact authentication, correlation with campaign inputs,
scientific decoding, native-file correlation, numerical verification, qualification,
and acceptance belong to separate operations and evidence.

Row 058 moved the implementation to
`ksdft2effmass.periodic1d.campaign.result_documents` because the first canonical
campaign family consumes this shared wire owner. The canonical campaign facade exposes
it; former underscored and publication facades retain no forwarding alias. Other
transitional periodic-1D families may import this canonical supporting owner until
their separately assigned moves.
