# `periodic1d.campaign.isolated`

## Purpose and status

This package is the canonical row-058 owner of the periodic-1D isolated-band campaign
family. It keeps campaign controls, exact encoded documents, decoded retained results,
calculation, correlation, independent verification, replay adoption, and orchestration
under one cohesive campaign namespace. The former
`ksdft2effmass.campaigns.periodic_1d` and publication facades expose no isolated-family
compatibility aliases. Shared strict decoding and generic encoded-result documents are
canonical siblings under `periodic1d.campaign.serialization` and
`periodic1d.campaign.result_documents`; they own wire mechanics only. Transitional
families may depend on those canonical owners, but this canonical family does not
depend on the former underscored campaign package.

## Ownership map

| Module | Responsibility | Navigation |
|---|---|---|
| `definition` | Version-one control record and strict JSON serializer | [Definition](definition/index.md) |
| `encoded_documents` | Exact input/result byte ownership only | [Encoded documents](encoded_documents/index.md) |
| `results` | Typed retained diagnostic results and result serializer | [Results](results/index.md) |
| `campaign` | Encapsulated input-to-operation owner | [Campaign](campaign/index.md) |
| `correlation_workflow`, `correlation` | Strict decoding, digest binding, and represented input/result agreement | This page |
| `calculation` | In-process reconstruction of demonstrated Appendix G numerical channels | This page |
| `numerical_verification`, `verification` | Independent reconstruction and explicit unavailable-channel accounting | This page |
| `verified_workflow` | Correlation followed by independent verification | This page |
| `adoption` | Authenticated replay and explicit scientific-object adoption | [Adoption](adoption/index.md) |

## Scientific boundaries

The campaign definition is a control record, not a physical model. Parent finite
representations, retained mathematical spaces, represented operators, complete hopping
representations, and truncated or fitted effective models remain distinct objects.
Encoded bytes and SHA-256 values establish content identity only. Correlation checks
relations represented by the two documents. Numerical verification covers only its
implemented channels and declared tolerances. None of these operations establishes
historical execution, convergence to an untruncated parent, physical adequacy,
scientific validation, uncertainty quantification, or acceptance.

## Retained identities

The maintained files remain unchanged at
`calculations/research-monograph/periodic-1d/`:

- `input.json`: `ae17de790380dee76693e984b96fbb22773a40440e267d3e77b4543cafaad6fb`;
- `result.json`: `37a4619e3a6ebf1c8ec9fac9f4c7cb5398ffe27254003529f736987c5f0bf71c`.

The maintained `verify_result.py` changed only its package import route and now has
catalog identity
`376683ad8503c60477654cdb5972e5e3b3f4cc05cf2df108cd2ab7bb30ec372e`.
This source-script identity is separate from the unchanged input and result wires.

No Quantum ESPRESSO, Wannier90, external, or production calculation is part of this
move.

## Public route and evidence

The reviewed import route is `ksdft2effmass.periodic1d.campaign`; the leaf route
`ksdft2effmass.periodic1d.campaign.isolated` exposes the same class objects. Source is
under `python/src/ksdft2effmass/periodic1d/campaign/isolated/`. Software and numerical
evidence mirrors that namespace under `python/tests/`; ownership metadata remains split
between routine/class-owned records and artifact-owned integration records.

Original local work under the repository license. Passing tests establish bounded
software behavior only, not scientific validation.
