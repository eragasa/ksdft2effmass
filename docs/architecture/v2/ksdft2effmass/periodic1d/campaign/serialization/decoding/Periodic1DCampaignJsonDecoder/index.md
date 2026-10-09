# `Periodic1DCampaignJsonDecoder`

## Responsibility

This stateless wire Action decodes one exact built-in `bytes` document as strict UTF-8
JSON and adapts explicitly requested fields to closed immutable JSON values or exact
primitive, quantity, and dense complex-pair representations. Its non-writeable
`complex128` vector and matrix outputs centralize numeric pair adaptation while leaving
cardinality, basis, units, and scientific meaning to the consuming schema. Duplicate
keys, ordinary nonfinite constants, wrong exact representations, booleans at numeric
boundaries, malformed pairs, and binary64 overflow fail closed.

Schema selection and schema-specific interpretation remain with the consuming
campaign serializer. The decoder does not infer scientific identity, units, frame,
gauge, normalization, provenance, convergence, result kind, native-file presence, or
acceptance from names, shapes, paths, or payload content.

## Code and public route

| Surface | Mapping |
|---|---|
| Definition | `python/src/ksdft2effmass/periodic1d/campaign/serialization/decoding.py` |
| Qualified class | `ksdft2effmass.periodic1d.campaign.serialization.decoding.Periodic1DCampaignJsonDecoder` |
| Reviewed facade | `ksdft2effmass.periodic1d.campaign.Periodic1DCampaignJsonDecoder` |
| Transitional aliases | None |

## Evidence

`python/tests/software_verification/ksdft2effmass/periodic1d/campaign/test__Periodic1DCampaignJsonDecoder.py`
contains claim-bearing class-owned tests for strict document and primitive adaptation.
`test__integration__periodic_1d_encoded_result_document_artifacts.py` separately checks
the canonical route and former-route absence. Exact test ownership is recorded in the
colocated `resources/implementation-verification-ownership.json`.

Passing this evidence establishes strict wire adaptation only. It does not establish a
campaign schema, decoded scientific correctness, provenance, numerical reproduction,
convergence, scientific validation, uncertainty quantification, or acceptance.
Original local work under the repository license.
