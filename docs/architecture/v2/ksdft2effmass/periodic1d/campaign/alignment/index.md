# `periodic1d.campaign.alignment`

## Purpose and status

This implemented canonical package owns campaign-specific alignment studies whose
inference contracts preserve explicit information boundaries. Row 062 moved the
blind-alignment family here from the underscored defect namespace without a
compatibility alias or retained-wire change.

Campaign alignment is not a generic basis, gauge, or frame utility. Reusable frame
alignment belongs to its scientific or numerical owner; this package owns campaign
inputs, observations, hidden-truth separation, inference policy, verification, and
retained evidence for explicitly identified studies.

## Reviewed facade and child map

The package facade exports exactly `BlindAlignmentCampaign` and
`BlindAlignmentEncodedDocuments`, using the defining class objects from its `blind`
child.

| Child | Responsibility | Canonical page |
|---|---|---|
| `blind` | Blind-alignment campaign with inference-visible observations separated from construction-only truth | [Blind alignment](blind/index.md) |

## Dependency boundary

Alignment campaigns may consume explicit scientific models, represented operators,
retention metadata, and reusable alignment Actions. Scientific model and operator
packages must not import campaign execution, repository paths, retained encoded
documents, hidden campaign truth, or acceptance policy.

Repository location belongs to explicit operation requests rather than encoded-document
records. No path, frame, gauge, source identity, scientific compatibility, or meaning
is inferred from payload names, dimensions, spectra, or hashes.

The blind baseline consumes row-065 matched-extraction records and row-030 canonical
finite-supercell adaptation through their explicit metadata contracts. The alignment
facade does not forward those types or duplicate their scientific metadata.

## Evidence and limitations

Rows 041 and 062 cover the encoded-document/location split, canonical family ownership,
curated facade identity, mirrored tests, and removed former route. Separate numerical
tests exercise inference and retained reconstruction. None of this establishes material
validation, execution provenance, convergence, uncertainty quantification,
transferability, or acceptance.

Original local work under the repository license.
