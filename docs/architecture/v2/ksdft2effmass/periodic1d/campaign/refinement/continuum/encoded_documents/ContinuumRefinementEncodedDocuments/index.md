# `ContinuumRefinementEncodedDocuments`

## Canonical identity

`ContinuumRefinementEncodedDocuments` is the row-042 byte owner for the periodic-1D
separated continuum-refinement campaign. Its implemented defining name is
`ksdft2effmass.periodic1d.campaign.refinement.continuum.encoded_documents.ContinuumRefinementEncodedDocuments`.
The canonical target package is `periodic1d.campaign.refinement.continuum`; row 063 owns
that later family move.

## Responsibility

The frozen slotted DataObject stores, in order:

1. exact nonempty version-one input JSON bytes; and
2. exact nonempty version-one retained-result JSON bytes.

It preserves supplied byte objects without parsing, normalizing, re-encoding, coercing,
or copying them. It rejects non-`bytes` values and `bytes` subclasses with `TypeError`;
it rejects empty exact bytes with `ValueError`.

## Non-responsibilities

The class is not a parent lattice model, parabolic continuum approximation, finite
representation, retained space, represented operator, decoded axis record, convergence
result, verifier, provenance record, or acceptance decision. It does not own or infer
repository location.

Retained correlation receives an explicit absolute root at the executing facade method.
Independent verification owns its absolute root in a typed request whose construction
performs no access. No root, state space, scaling relation, source identity, provenance,
continuum validity, or meaning is inferred from filenames, payload content, array
shapes, spectra, or hashes.

## Retained artifact identities

| Artifact | SHA-256 content identity |
|---|---|
| `calculations/research-monograph/impurity-defect-1d-continuum-refinement/input.json` | `55d647a8c259d3a1f1e5c756b496a9d1a16fee0a691c7b53d2f877da5f287fdd` |
| `calculations/research-monograph/impurity-defect-1d-continuum-refinement/result.json` | `1f4029cc953e78eb8231e5a651676401b20d5b74f09ecb8cb38d72aa2e92c2dc` |

The maintained `SHA256SUMS` catalog repeats these identities. SHA-256 establishes
content identity only. It does not establish who produced the files, which software ran,
whether source identities are authentic, whether decoded or numerical claims are
correct, whether an asymptotic limit exists, or whether the result is accepted.

## Supported route and retirement

The supported current facade is
`ksdft2effmass.periodic1d.campaign.refinement.continuum`, where the exported
class object is the defining class object. The former aggregate
`ContinuumRefinementCampaignModel`, its `repository_root` field, and its
`defects/continuum_refinement/model.py` module are retired; no compatibility alias is
provided.

## Row-042 completion dossier

| Field | Reconciled content |
|---|---|
| Crosswalk identity | `PERIODIC-XWALK-042`; former owner `ContinuumRefinementCampaignModel` |
| Scientific category | Supporting encoded campaign document; not a scientific model, represented operator, or convergence result |
| Target ownership | Current defining module `ksdft2effmass.periodic1d.campaign.refinement.continuum.encoded_documents`; reviewed leaf facade `ksdft2effmass.periodic1d.campaign.refinement.continuum`; future row-063 target `periodic1d.campaign.refinement.continuum` |
| Preserved meaning | Input bytes precede retained-result bytes; exact payloads, digests, experiment identifiers, and payload-contained provenance paths remain byte-for-byte unchanged |
| Changed meaning | The aggregate campaign-model name and module are removed; correlation receives repository location at execution, while verification location moves into an explicit request |
| Representation contract | Two ordered, nonempty exact built-in `bytes`; state space, basis, gauge, geometry, units, energy reference, numeric dtype, array shape, and scientific ordering are not applicable at this encoded boundary |
| Construction route | Frozen slotted dataclass assignment preserves supplied byte objects; no selection, projection, transformation, refinement, fitting, decoding, normalization, or filesystem resolution occurs |
| Error boundaries | Wrong representations, including `bytes` subclasses, raise `TypeError`; empty exact bytes raise `ValueError`; correlation and verification reject unsupported or relative roots before source access |
| Source documentation | Full NumPy-style class and operation-boundary docstrings plus comments at exact-byte and explicit-path boundaries in `encoded_documents.py`, `campaign.py`, and `verification.py` |
| Public documentation | This class page, its [module dossier](../index.md), the [campaign methods narrative](../../numerical-techniques-and-scientific-reasoning.md), `doc/sphinx/concepts/periodic1d-continuum-refinement.rst`, and `doc/sphinx/api/research-monograph-campaigns.rst` |
| Verification | Five exact class-qualified nodes are enumerated in the [module test mapping](../index.md); three routine class-owned nodes and two artifact-owned integration nodes |
| Retained evidence | `input.json`, `result.json`, and their reviewed `SHA256SUMS` entries, with identities listed above |
| Unavailable information | Encoded storage does not supply authenticated execution provenance, decoded parent or approximation records, asymptotic convergence, scientific validation, UQ, or acceptance; none is inferred |
| Claim boundary | Software ownership and content identity only; no numerical reconstruction, continuum theorem, material adequacy, transferability, UQ, or acceptance claim |

## Verification dossier

Exact code, test, import, Sphinx, provenance, and evidence mappings are maintained by the
[parent module dossier](../index.md). Class-owned tests cover synthetic intrinsic
invariants. Artifact-owned integration tests cover maintained retained bytes,
checksum-catalog identities, public route identity, retired-route absence, and explicit
repository-location boundaries.

## Scientific status and limitations

The row-042 evidence establishes software structure and retained-byte identities only.
It does not rerun the campaign, invoke Quantum ESPRESSO or Wannier90, authenticate direct
or transitive sources, reconstruct the 31 retained axis and diagnostic records, prove an
asymptotic continuum theorem, validate a material model, establish transferability,
quantify uncertainty, or record scientific acceptance.

Original local work under the repository license.
