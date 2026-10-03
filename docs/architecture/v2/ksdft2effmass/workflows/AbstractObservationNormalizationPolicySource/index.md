# `AbstractObservationNormalizationPolicySource`

## Status

**Implemented nominal-ABC contract; local software-verification evidence passes.**

## Responsibility

`AbstractObservationNormalizationPolicySource(ABC)` declares the exact applied
integration policy through abstract `identity ->
AbstractObservationCorrelationIdentity` and `version -> str` properties. The
integration owns policy interpretation and support; Workflow only retains and
correlates the exact object.

`QuantumEspressoObservationNormalizationPolicy` inherits explicitly. Nominal
membership does not establish that normalization is physically adequate or accepted.

## Related architecture

- [Schematic](schematic.md)
- [`AbstractObservationCorrelationIdentity`](../AbstractObservationCorrelationIdentity/index.md)
- [Repository-wide migration](../../protocol-to-abc-migration.md)
