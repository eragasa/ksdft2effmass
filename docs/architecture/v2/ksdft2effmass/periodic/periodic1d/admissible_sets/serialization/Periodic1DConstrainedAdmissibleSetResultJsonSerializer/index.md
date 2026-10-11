# `Periodic1DConstrainedAdmissibleSetResultJsonSerializer`

## Purpose

Stateless canonical encoder for the complete M3 result.

## Operation and wire contract

`serialize(record)` requires the exact M3 aggregate and emits UTF-8 bytes under schema
`ksdft2effmass.periodic1d.constrained-admissible-set-result.v1`. It records
composed M2 controls, parameter/unit meanings, quadratics, all candidate losses, case
proofs, evaluation roles, locality, and explicit scope exclusions. Keys are sorted,
separators compact, nonfinite JSON forbidden, complex values ordered pairs, and one
terminal newline emitted.

## Failures and limitations

Wrong type raises `TypeError`; unsupported wire-unit expressions or nonfinite values fail
closed. Serialization does not recompute proof objects. Canonical bytes support
provenance but do not establish chronology, manifest correlation, or correctness.
