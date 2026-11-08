# `first_passing_support.records`

## Purpose and status

Implemented owner of immutable typed values for the periodic-1D rank-one finite
first-passing-support certification proposition.

The module owns exact rational endpoints, closed nonnegative intervals, the frozen
objective and disposition vocabularies, producer/verifier identity, request identity,
complete result evidence, and exact endpoint classification. It does not produce or
verify outward containment.

## Public symbols

- [`FirstPassingSupportObjective`](FirstPassingSupportObjective/index.md)
- [`FirstPassingSupportDisposition`](FirstPassingSupportDisposition/index.md)
- [`ExactRational`](ExactRational/index.md)
- [`NonnegativeExactInterval`](NonnegativeExactInterval/index.md)
- [`FirstPassingIntervalEntry`](FirstPassingIntervalEntry/index.md)
- [`CertificationToolIdentity`](CertificationToolIdentity/index.md)
- [`FirstPassingSupportRequest`](FirstPassingSupportRequest/index.md)
- [`FirstPassingSupportResult`](FirstPassingSupportResult/index.md)

All maintained records derive from `BaseTypedRecord`. Their domain schemas are their
closed `_mapping()` and `_from_mapping()` implementations plus constructor invariants;
there is no parallel JSON Schema or proposition-specific codec.

## Shared boundaries

- [Certification implementation](../../../../implementation.md)
- [Certification numerics](../../../../numerics.md)
- [Certification scientific interpretation](../../../../scientifics.md)
- [First-passing-support leaf](../index.md)

## Provenance

Original local work under the repository license.
