# `AbstractNormalizedObservationSource`

## Status

**Implemented nominal-ABC contract; local software-verification evidence passes.**

## Responsibility

`AbstractNormalizedObservationSource(AbstractResultObject, ABC)` is the narrow nominal
boundary consumed by Workflow observation assembly. It declares the unchanged neutral
Kohn--Sham observation, exact artifact and producer correlations, parsed-document and
parser identities, applied normalization policy, parser version, and explicit
limitations. The target preserves every property of the current source contract:
`identity`, `observation`, `source_manifest_identity`,
`source_manifest_entry_identity`, `source_artifact_identity`,
`source_content_identity`, `source_producer_provenance_identity`,
`parsed_document_identity`, `parser_identity`, `parser_version`,
`normalization_policy`, and `limitation_values`.

The ABC performs no parsing, unit conversion, native-file access, numerical
transformation, persistence, or scientific interpretation. Concrete integrations own
all native meaning. `QuantumEspressoExtractedObservationResult` inherits explicitly.

## Inheritance

The source has one Workflow result route through `AbstractResultObject`; it does not
repeat a parallel result protocol. Test sources must inherit nominally. Objects with
matching fields but no inheritance are rejected.

## Related architecture

- [Schematic](schematic.md)
- [`AbstractResultObject`](../AbstractResultObject/index.md)
- [`AbstractObservationCorrelationIdentity`](../AbstractObservationCorrelationIdentity/index.md)
- [Repository-wide migration](../../protocol-to-abc-migration.md)
