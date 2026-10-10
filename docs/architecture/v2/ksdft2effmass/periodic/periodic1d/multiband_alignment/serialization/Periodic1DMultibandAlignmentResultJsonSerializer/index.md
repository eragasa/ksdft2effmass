# `Periodic1DMultibandAlignmentResultJsonSerializer`

## Purpose

Stateless canonical encoder for the complete M2 result.

## Operation and wire contract

`serialize(record)` requires the exact M2 aggregate and returns UTF-8 bytes under schema
`ksdft2effmass.periodic1d.multiband-alignment-calculation-result.v1`. The document
includes parent/retention/attack controls, mesh roles, diagnostics, complete transforms,
Hermiticity, and range channels. Keys are sorted, separators compact, complex values are
ordered pairs, nonfinite values are forbidden, and one newline terminates the document.

## Failures and limitations

Wrong record type raises `TypeError`; nonfinite values fail JSON encoding. Serialization
does not recompute or accept evidence. Exact bytes aid provenance but do not establish
chronology or semantic validity.
