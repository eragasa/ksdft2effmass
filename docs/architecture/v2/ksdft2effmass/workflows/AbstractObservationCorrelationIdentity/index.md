# `AbstractObservationCorrelationIdentity`

## Status

**Accepted nominal-ABC migration contract; implementation pending.**

## Responsibility

`AbstractObservationCorrelationIdentity(ABC)` declares one abstract nonempty lexical
`value -> str` property for an integration-owned observation identity. Concrete
integrations retain the identity's nominal type and meaning; Workflow reads the value
without replacing it with a Workflow-owned identity.

QE parsed-document, parser, and normalization-policy identity classes inherit
explicitly. Structural lookalikes and aliases are rejected. Membership does not
authenticate an artifact or establish scientific meaning.

## Related architecture

- [Schematic](schematic.md)
- [Repository-wide migration](../../protocol-to-abc-migration.md)
