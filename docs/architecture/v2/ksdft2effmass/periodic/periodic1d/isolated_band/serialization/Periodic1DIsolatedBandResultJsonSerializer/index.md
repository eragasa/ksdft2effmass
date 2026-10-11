# `Periodic1DIsolatedBandResultJsonSerializer`

## Purpose

Stateless deterministic encoder for `Periodic1DIsolatedBandCalculationResult`.

## Operation

`serialize(record)` requires the exact M1 aggregate result and returns UTF-8 `bytes`.
The document includes calculation/model identity, conventions, controls, parent and
convergence evidence, training/evaluation samples, complete hopping data, Hermiticity,
and every range channel.

## Wire contract

Schema identity is
`ksdft2effmass.periodic1d.isolated-band-calculation-result.v1`. JSON keys are sorted,
separators are compact, `allow_nan=False`, complex values are `[real, imaginary]`, units
are explicit strings, and one newline terminates the document.

## Failures and limitations

Wrong record type raises `TypeError`; nonfinite values fail encoding. The serializer
does not verify evidence or provide a decoder. Canonical bytes support provenance but do
not prove chronology or correctness.
