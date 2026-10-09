# `FiniteRankOracleEncodedDocuments`

## Canonical identity

`FiniteRankOracleEncodedDocuments` is the row-043 byte owner for the periodic-1D
finite-rank-oracle campaign. Its implemented defining name is
`ksdft2effmass.periodic1d.campaign.oracle.finite_rank.encoded_documents.FiniteRankOracleEncodedDocuments`.
The canonical target package is `periodic1d.campaign.oracle.finite_rank`; row 064 owns
that later family move.

## Responsibility

The frozen slotted DataObject stores, in order:

1. exact nonempty version-one input JSON bytes; and
2. exact nonempty version-one retained-result JSON bytes.

It preserves supplied byte objects without parsing, normalizing, re-encoding, coercing,
or copying them. It rejects non-`bytes` values and `bytes` subclasses with `TypeError`;
it rejects empty exact bytes with `ValueError`.

## Non-responsibilities

The class is not a physical parent model, finite state space, represented host or defect
operator, retained subspace, Bloch-resolvent action, eigensolver, bound-state result,
provenance record, oracle-qualification record, or acceptance decision. It does not own
or infer repository location.

Calculation and retained correlation receive explicit absolute roots at their executing
facade methods. Independent verification owns its absolute root in a typed request whose
construction performs no access. No root, parent identity, state space, basis, ordering,
energy reference, source authenticity, scientific meaning, or oracle qualification is
inferred from filenames, payload content, dimensions, spectra, or hashes.

## Retained artifact identities

| Artifact | SHA-256 content identity |
|---|---|
| `calculations/research-monograph/impurity-defect-1d-analytical-oracle/input.json` | `ab653338be4f1733c8dd39878526b3293e603f2f0b0e7b8241577db2406c5840` |
| `calculations/research-monograph/impurity-defect-1d-analytical-oracle/result.json` | `64ab16a279d5f8ca18f725dadb15860811a45ea12758a91a7cd7166f6074dae0` |

The maintained `SHA256SUMS` catalog repeats these identities. SHA-256 establishes
content identity only. It does not establish who produced the files, which software
ran, whether direct or transitive sources are authentic, whether decoded or numerical
claims are correct, whether the analytical route is qualified for another evidence
class, or whether the result is accepted.

## Historical-runner boundary

The retained legacy result records the historical runner digest
`0f0ffde200456882981cc8b89bc3622af4dd00696ce0c17a0ad106ed957ffc06`.
The verifier recognizes that exact frozen historical identity for the legacy wire. It
does not pretend that the current adapter file has those bytes. Newer results carrying
explicit implementation fields follow their separate script-and-implementation identity
branch. This compatibility behavior is provenance checking for the bounded retained
campaign, not a generic oracle registry or qualification mechanism.

## Supported route and retirement

The supported current facade is
`ksdft2effmass.periodic1d.campaign.oracle.finite_rank`, where the exported
class object is the defining class object. The former aggregate
`FiniteRankOracleCampaignModel`, its `repository_root` field, and its
`defects/finite_rank_oracle/model.py` module are retired; no compatibility alias is
provided.

## Row-043 completion dossier

| Field | Reconciled content |
|---|---|
| Crosswalk identity | `PERIODIC-XWALK-043`; former owner `FiniteRankOracleCampaignModel` |
| Scientific category | Supporting encoded campaign document; not a scientific model, represented operator, numerical result, or qualification record |
| Target ownership | Current defining module `ksdft2effmass.periodic1d.campaign.oracle.finite_rank.encoded_documents`; reviewed leaf facade `ksdft2effmass.periodic1d.campaign.oracle.finite_rank`; future row-064 target `periodic1d.campaign.oracle.finite_rank` |
| Preserved meaning | Input bytes precede retained-result bytes; exact payloads, digests, experiment identifiers, and payload-contained paths remain byte-for-byte unchanged |
| Changed meaning | The aggregate campaign-model name and module are removed; calculation and correlation receive repository location at execution, while verification location belongs to an explicit request |
| Representation contract | Two ordered, nonempty exact built-in `bytes`; state space, basis, gauge, geometry, units, energy reference, numeric dtype, matrix rank, and scientific ordering are not applicable at this encoded boundary |
| Construction route | Frozen slotted dataclass assignment preserves supplied byte objects; no selection, projection, transformation, decoding, normalization, root solve, eigensolve, or filesystem resolution occurs |
| Error boundaries | Wrong representations, including `bytes` subclasses, raise `TypeError`; empty exact bytes raise `ValueError`; executing and verification boundaries reject unsupported or relative roots before source access and reject encapsulated or repository input bytes that disagree with provenance |
| Source documentation | Full NumPy-style class and operation-boundary docstrings plus explicit path and historical-runner boundaries in `encoded_documents.py`, `campaign.py`, and `verification.py` |
| Public documentation | This class page, its [module dossier](../index.md), `doc/sphinx/concepts/periodic-1d-defect-extraction.rst`, and `doc/sphinx/api/research-monograph-campaigns.rst` |
| Verification | Six exact class-qualified nodes are enumerated in the [module test mapping](../index.md); three routine class-owned nodes and three artifact-owned integration nodes, including encapsulated-input/provenance correlation |
| Retained evidence | `input.json`, `result.json`, and their reviewed `SHA256SUMS` entries, with identities listed above |
| Unavailable information | Encoded storage does not supply authenticated execution provenance, decoded parent/operator records, numerical reconstruction, infinite-volume or continuum convergence, material validation, UQ, or acceptance; none is inferred |
| Claim boundary | Software ownership and content identity only; no oracle qualification outside the exact retained campaign, theorem, material adequacy, transferability, UQ, or acceptance claim |

## Verification dossier

Exact code, test, import, Sphinx, provenance, and evidence mappings are maintained by the
[parent module dossier](../index.md). Class-owned tests cover synthetic intrinsic
invariants. Artifact-owned integration tests cover maintained retained bytes,
checksum-catalog identities, public route identity, retired-route absence, and explicit
repository-location boundaries.

## Scientific status and limitations

The row-043 evidence establishes software structure and retained-byte identities only.
It does not rerun the campaign, invoke Quantum ESPRESSO or Wannier90, authenticate the
source graph recursively, reconstruct the 24 retained sweep and boundary-control
records, prove an infinite-volume or continuum theorem, validate a material model,
establish transferability, qualify a production oracle, quantify uncertainty, or record
scientific acceptance.

Original local work under the repository license.
