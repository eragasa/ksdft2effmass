# `FiniteRankOracleCampaignResultDocument`

## Purpose and row-057 disposition

This frozen, slotted DataObject remains the named encoded result-document owner for the
finite-rank-oracle campaign. Row 057 keeps it in the campaign's existing
`result_documents.py` module, adds the deliberate leaf-package facade, and audits its
intrinsic, artifact, Sphinx, and architecture contracts. Row 064 retains ownership of
the later canonical package move.

## Public contract

```python
FiniteRankOracleCampaignResultDocument(payload: bytes)
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
| `calculations/research-monograph/impurity-defect-1d-analytical-oracle/result.json` | `64ab16a279d5f8ca18f725dadb15860811a45ea12758a91a7cd7166f6074dae0` |

Artifact-owned evidence requires the same identity in the maintained `SHA256SUMS`
catalog and confirms that `FiniteRankOracleEncodedDocuments.retained_result_document`
can be passed without copying. Content identity does not qualify the result as an oracle
for any evidence class or validity domain and does not establish authorship, execution
provenance, schema correctness, decoded observations, scientific validation,
uncertainty quantification, or acceptance.

## Supported imports

- defining route:
  `ksdft2effmass.periodic1d.campaign.oracle.finite_rank.result_documents.FiniteRankOracleCampaignResultDocument`;
- reviewed leaf facade:
  `ksdft2effmass.periodic1d.campaign.oracle.finite_rank.FiniteRankOracleCampaignResultDocument`.

No generic oracle facade, registry, factory, plugin point, or broader periodic-1D export
is introduced before row 064.

## Code and evidence mapping

| Surface | Path or node | Responsibility |
|---|---|---|
| Definition | `python/src/ksdft2effmass/periodic1d/campaign/oracle/finite_rank/result_documents.py` | Exact bytes and digest |
| Facade | `python/src/ksdft2effmass/periodic1d/campaign/oracle/finite_rank/__init__.py` | Deliberate leaf import |
| Routine evidence | `test__FiniteRankOracleCampaignResultDocument.py::TestFiniteRankOracleCampaignResultDocument` | Fields, module, fixed synthetic digest, failures, immutability |
| Artifact evidence | `test__integration__finite_rank_oracle_result_document_artifact.py::TestFiniteRankOracleResultDocumentArtifact::test_retained_result__preserves_bytes_catalog_identity_and_route` | Retained bytes, catalog identity, paired owner, facade |
| Sphinx | `doc/sphinx/api/research-monograph-campaigns.rst` | User-facing campaign API and limitations |

The test paths are rooted at
`python/tests/software_verification/ksdft2effmass/periodic1d/campaign/oracle/finite_rank/`
and are registered in the periodic-1D implementation-verification ownership metadata.

## Scientific boundary

This DataObject does not identify a parent model, finite represented operator,
finite-rank perturbation, bound-state eigenspace, analytical truth, oracle
qualification, or scientific conclusion. Passing its tests establishes bounded
software behavior and content identity only. No calculator is invoked and no retained
artifact is modified.
