# `first_passing_support.validation`

## Purpose and status

Implemented structural-correlation owner for canonical first-passing-support request and
result bytes.

The module admits the shared `BaseTypedRecord` JSON representation, authenticates exact
bytes by SHA-256, checks request/result identity and selected-support correlation, and
returns a typed validation record. It does not calculate enclosures, replay containment,
or grant scientific acceptance.

## Public symbols

- [`FirstPassingSupportWireValidation`](FirstPassingSupportWireValidation/index.md)
- [`FirstPassingSupportWireValidator`](FirstPassingSupportWireValidator/index.md)

## Shared boundaries

- [Certification implementation](../../../../implementation.md)
- [Certification numerics](../../../../numerics.md)
- [Certification scientific interpretation](../../../../scientifics.md)
- [First-passing-support leaf](../index.md)

## Provenance

Original local work under the repository license.
