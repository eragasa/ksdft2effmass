# `ContinuumRefinementCampaignResultDocument`

## Purpose and row-057 disposition

This frozen, slotted DataObject remains the named encoded result-document owner for the
continuum-refinement campaign. Row 057 keeps it in the campaign's existing
`result_documents.py` module, adds the deliberate leaf-package facade, and audits its
intrinsic, artifact, Sphinx, and architecture contracts. Row 063 retains ownership of
the later canonical package move.

## Public contract

```python
ContinuumRefinementCampaignResultDocument(payload: bytes)
```

| Field or property | Representation | Contract |
|---|---|---|
| `payload` | Exact nonempty built-in `bytes` | Encoded result wire retained without decoding or copying |
| `sha256` | 64-character lowercase hexadecimal `str` | SHA-256 derived directly from `payload` |

Strings, mutable byte arrays, byte subclasses, and empty bytes fail closed. The object
is frozen and slotted. `__post_init__` delegates exact-byte validation to the cohesive
`_check_args_payload` method. Digest derivation never parses or canonically re-encodes
the wire.

## Retained content identity

| Artifact | SHA-256 |
|---|---|
| `calculations/research-monograph/impurity-defect-1d-continuum-refinement/result.json` | `1f4029cc953e78eb8231e5a651676401b20d5b74f09ecb8cb38d72aa2e92c2dc` |

Artifact-owned evidence requires the same identity in the maintained `SHA256SUMS`
catalog and confirms that `ContinuumRefinementEncodedDocuments.retained_result_document`
can be passed without copying. Content identity does not establish authorship,
execution provenance, schema correctness, decoded observations, continuum convergence,
physical adequacy, validation, uncertainty quantification, or acceptance.

## Supported imports

- defining route:
  `ksdft2effmass.periodic1d.campaign.refinement.continuum.result_documents.ContinuumRefinementCampaignResultDocument`;
- reviewed leaf facade:
  `ksdft2effmass.periodic1d.campaign.refinement.continuum.ContinuumRefinementCampaignResultDocument`.

No broader defect or periodic-1D facade is introduced before row 063.

## Code and evidence mapping

| Surface | Path or node | Responsibility |
|---|---|---|
| Definition | `python/src/ksdft2effmass/periodic1d/campaign/refinement/continuum/result_documents.py` | Exact bytes and digest |
| Facade | `python/src/ksdft2effmass/periodic1d/campaign/refinement/continuum/__init__.py` | Deliberate leaf import |
| Routine evidence | `test__ContinuumRefinementCampaignResultDocument.py::TestContinuumRefinementCampaignResultDocument` | Fields, module, fixed synthetic digest, failures, immutability |
| Artifact evidence | `test__integration__continuum_refinement_result_document_artifact.py::TestContinuumRefinementResultDocumentArtifact::test_retained_result__preserves_bytes_catalog_identity_and_route` | Retained bytes, catalog identity, paired owner, facade |
| Sphinx | `doc/sphinx/api/research-monograph-campaigns.rst` | User-facing campaign API and limitations |

The test paths are rooted at
`python/tests/software_verification/ksdft2effmass/periodic1d/campaign/refinement/continuum/`
and are registered in the periodic-1D implementation-verification ownership metadata.

## Scientific boundary

This DataObject does not identify a parent lattice operator, continuum approximation,
embedding, discretization, retained space, represented operator, error relationship, or
scientific conclusion. Passing its tests establishes bounded software behavior and
content identity only. No calculator is invoked and no retained artifact is modified.
