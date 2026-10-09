# `Periodic1DReductionChallengeEncodedDocuments`

## Contract

A frozen, slotted exact-byte container with `input_payload` and `result_payload`.
Construction rejects non-`bytes` values and empty payloads. Byte identity is retained
without schema claims.

## Evidence and limitations

Routine class-owned tests verify intrinsic representation, immutability, and exact
synthetic-byte preservation. Artifact-owned integration evidence binds the maintained
wires to:

- input SHA-256 `3be86c6ee7cb08c1c194aa97e856c89458907c23428bed19f6b38cdb437d987a`;
- result SHA-256 `5897e16570609f3b2ad2fb5cdefb39b8da9df6395e42796d8c5af77734cba394`;
- the maintained `SHA256SUMS` entries; and
- canonical facade identity and former-route removal.

Digest equality establishes exact content identity only. It does not establish
authorship, historical execution, provenance, decoded correctness, numerical
reproduction, convergence, scientific validation, UQ, or acceptance.
