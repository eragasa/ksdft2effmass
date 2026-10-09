# `BlindAlignmentEncodedDocuments`

## Canonical identity

`BlindAlignmentEncodedDocuments` is the row-041 byte owner for the periodic-1D
blind-alignment campaign. Row 062 moved its complete family to the implemented defining
name
`ksdft2effmass.periodic1d.campaign.alignment.blind.encoded_documents.BlindAlignmentEncodedDocuments`
without an alias or retained-wire change.

## Responsibility

The frozen slotted DataObject stores, in order:

1. exact nonempty version-one input JSON bytes; and
2. exact nonempty version-one retained-result JSON bytes.

It preserves the supplied byte objects without parsing, normalizing, re-encoding,
coercing, or copying them. It rejects non-`bytes` values and `bytes` subclasses with
`TypeError`; it rejects empty exact bytes with `ValueError`.

## Non-responsibilities

The class is not a physical model, finite representation, retained space, represented
operator, decoded observation, hidden-truth record, inference result, verifier,
provenance record, or acceptance decision. It does not own or infer repository location.

Absolute repository roots belong to the calculation, retained-correlation, and
verification request types because those operation boundaries may authenticate
repository-relative sources. Request construction itself does not access the filesystem.
No root, frame, gauge, alignment map, scientific identity, provenance, or meaning is
inferred from filenames, payload content, array shapes, spectra, or hashes.

## Retained artifact identities

| Artifact | SHA-256 content identity |
|---|---|
| `calculations/research-monograph/impurity-defect-1d-blind-alignment/input.json` | `3476c0b1ed45913e5386be3688528d549f7eea15840b67559763d875406d7d48` |
| `calculations/research-monograph/impurity-defect-1d-blind-alignment/result.json` | `a3b7d20c870fe5d87fd6a591fbafe9a997e7a261a5bc08163c3273b4789416fe` |

The maintained `SHA256SUMS` catalog repeats these identities. SHA-256 establishes
content identity only. It does not establish who produced the files, which software ran,
whether the hidden-information boundary was respected, whether decoded or numerical
claims are correct, or whether the result is scientifically accepted.

## Supported route and retirement

The supported current facade is
`ksdft2effmass.periodic1d.campaign.alignment.blind`, where the exported class
object is the defining class object. The former aggregate
`BlindAlignmentCampaignModel`, its `repository_root` field, and its
`defects/blind_alignment/model.py` module are retired; no compatibility alias is
provided.

## Row-041 completion dossier

| Field | Reconciled content |
|---|---|
| Crosswalk identity | `PERIODIC-XWALK-041`; former owner `BlindAlignmentCampaignModel` |
| Scientific category | Supporting encoded campaign document; not a scientific model or represented operator |
| Target ownership | Implemented defining module `ksdft2effmass.periodic1d.campaign.alignment.blind.encoded_documents`; reviewed leaf facade `ksdft2effmass.periodic1d.campaign.alignment.blind`; the former underscored route is absent |
| Preserved meaning | Input bytes precede retained-result bytes; exact payloads, digests, experiment identifiers, and payload-contained provenance paths remain byte-for-byte unchanged |
| Changed meaning | The aggregate campaign-model name and source module are removed; repository location moves from the document owner into three explicit operation requests |
| Representation contract | Two ordered, nonempty exact built-in `bytes`; state space, basis, gauge, geometry, units, energy reference, numeric dtype, array shape, and scientific ordering are not applicable at this encoded boundary |
| Construction route | Frozen slotted dataclass assignment preserves supplied byte objects; no selection, projection, transformation, interpolation, fitting, decoding, normalization, or filesystem resolution occurs |
| Error boundaries | Wrong representations, including `bytes` subclasses, raise `TypeError`; empty exact bytes raise `ValueError`; semantic and source-authentication failures belong to downstream Actions |
| Source documentation | Full NumPy-style class and invariant docstrings plus comments at exact-byte and explicit-path boundaries in `encoded_documents.py`, `campaign.py`, and `verification.py` |
| Public documentation | This class page, its [module dossier](../index.md), the [family dossier](../../index.md), and `doc/sphinx/api/ksdft2effmass/periodic1d/campaign/alignment-blind.rst` |
| Verification | Five exact class-qualified nodes are enumerated in the [module test mapping](../index.md); three routine class-owned nodes and two artifact-owned integration nodes |
| Retained evidence | `input.json`, `result.json`, and their reviewed `SHA256SUMS` entries, with identities listed above |
| Unavailable information | Encoded storage does not supply authenticated execution provenance, decoded observation/truth records, frame or gauge meaning, or acceptance authority; none is inferred |
| Claim boundary | Software ownership and content identity only; no numerical reconstruction, convergence, physical adequacy, scientific validation, UQ, transferability, or acceptance claim |

## Verification dossier

Exact code, test, import, Sphinx, provenance, and evidence mappings are maintained by the
[parent module dossier](../index.md). Class-owned tests cover synthetic intrinsic
invariants. Artifact-owned integration tests cover maintained retained bytes,
checksum-catalog identities, public route identity, retired-route absence, and the
request-owned repository-location split.

## Scientific status and limitations

The row-041 evidence establishes software structure and retained-byte identities only.
It does not rerun the campaign, invoke Quantum ESPRESSO or Wannier90, authenticate the
campaign's direct or transitive sources, reconstruct its 34 retained numerical records,
prove alignment inference or hidden-truth separation, quantify uncertainty, validate a
material model, or record scientific acceptance.

Original local work under the repository license.
