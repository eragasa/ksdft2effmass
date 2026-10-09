# `periodic1d.campaign.serialization`

## Purpose and status

This package owns shared strict periodic-1D campaign wire adaptation. Row 058 moved
`Periodic1DCampaignJsonDecoder` from the transitional underscored campaign package so
canonical campaign families do not depend on transitional ownership. The former deep
module and facade aliases are absent.

The decoder owns strict UTF-8 JSON document decoding, duplicate-key and nonfinite-token
rejection, closed immutable JSON values, and exact primitive/quantity adaptation. It
does not own any campaign schema, physical model, finite representation, retained
space or operator, represented form, effective model, provenance, validation,
uncertainty, or acceptance policy.

## Child map

| Child | Responsibility | Navigation |
|---|---|---|
| `decoding.Periodic1DCampaignJsonDecoder` | Strict shared wire-to-value adaptation | [Decoder](decoding/Periodic1DCampaignJsonDecoder/index.md) |

## Code and evidence

| Kind | Path |
|---|---|
| Implementation | `python/src/ksdft2effmass/periodic1d/campaign/serialization/decoding.py` |
| Claim-bearing class-owned tests | `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/test__Periodic1DCampaignJsonDecoder.py` |
| Route/artifact evidence | `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/test__integration__periodic_1d_encoded_result_document_artifacts.py` |
| Sphinx | `doc/sphinx/api/research-monograph-campaigns.rst` |

Original local work under the repository license. Passing decoder tests establish wire
behavior only, not decoded scientific correctness or scientific validation.
