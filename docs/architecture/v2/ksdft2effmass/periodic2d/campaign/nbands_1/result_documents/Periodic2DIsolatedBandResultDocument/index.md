# `Periodic2DIsolatedBandResultDocument`

## Purpose and row-056 disposition

`Periodic2DIsolatedBandResultDocument` is the immutable encoded result-document owner
for the retained version-one isolated periodic-2D campaign. `PERIODIC-XWALK-056` keeps
the class name and exact payload contract while correcting its defining module from
`definition.py` to `result_documents.py`.

The former module no longer defines, aliases, or forwards this class. The reviewed
package facades continue to expose the same public class name from its corrected owner.
This is an ownership correction, not a compatibility alias and not a scientific-model
migration.

## Public contract

### Construction

```python
Periodic2DIsolatedBandResultDocument(payload: bytes)
```

The constructor accepts one exact nonempty built-in `bytes` object. Strings, mutable
byte arrays, byte subclasses, and empty bytes fail closed. The supplied object is
retained without decoding, normalization, canonical re-encoding, coercion, or copying.

### State and invariants

| Field or property | Representation | Contract |
|---|---|---|
| `payload` | Exact nonempty built-in `bytes` | Original encoded result wire |
| `sha256` | 64-character lowercase hexadecimal `str` | SHA-256 of `payload`, derived on access |

The DataObject is frozen and slotted. Field reassignment and undeclared instance state
are rejected. `__post_init__` delegates the cohesive exact-byte check to
`_check_args_payload`.

The digest is computed from the encapsulated bytes directly. It is not computed from a
parsed JSON tree or a canonical serialization because either route would change the
wire-identity boundary.

## Ownership and dependency boundaries

The class imports only `dataclass` and `hashlib`. It owns no path, filename, repository
root, schema version, result kind, decoder, serializer, campaign request, calculator,
correlator, verifier, provenance record, or scientific acceptance decision.

`Periodic2DIsolatedBandEncodedDocuments` separately owns the paired input and result
bytes. Explicit composition may pass its `result_payload` to this class without copying;
that relationship does not make either DataObject an execution or provenance record.

`Periodic2DIsolatedBandCalculationResult` uses this document as its exact result value.
That typed composition records software structure only. Constructing either object does
not prove that the calculation Action ran.

## Retained artifact identity

Artifact-owned evidence reads the repository-maintained result without rewriting it:

| Artifact | SHA-256 |
|---|---|
| `calculations/research-monograph/periodic-2d/result.json` | `4eb55bde9d456d86bad1d65c8ac60267c07873c6936f8af876b07fd3e1d27be6` |

The same identity must appear in
`calculations/research-monograph/periodic-2d/SHA256SUMS`. Digest equality establishes
content identity only. It does not establish authorship, historical execution,
repository provenance, decoded correctness, numerical reproduction, convergence,
physical adequacy, scientific validation, uncertainty quantification, or acceptance.

## Supported imports

The exact defining class is exposed by three reviewed facades:

- `ksdft2effmass.periodic2d.campaign.nbands_1.Periodic2DIsolatedBandResultDocument`;
- `ksdft2effmass.periodic2d.campaign.Periodic2DIsolatedBandResultDocument`; and
- `ksdft2effmass.periodic2d.Periodic2DIsolatedBandResultDocument`.

The implementation identity is
`ksdft2effmass.periodic2d.campaign.nbands_1.result_documents.Periodic2DIsolatedBandResultDocument`.
The former `definition` module has no result-document attribute.

## Code mapping

| Code path | Qualified owner | Responsibility |
|---|---|---|
| `python/src/ksdft2effmass/periodic2d/campaign/nbands_1/result_documents.py` | `...result_documents.Periodic2DIsolatedBandResultDocument` | Exact immutable result bytes and derived digest |
| `python/src/ksdft2effmass/periodic2d/campaign/nbands_1/calculate.py` | `Periodic2DIsolatedBandCalculationResult` | Typed calculation-result composition |
| `python/src/ksdft2effmass/periodic2d/campaign/nbands_1/__init__.py` | `nbands_1` facade | Canonical campaign-family import |
| `python/src/ksdft2effmass/periodic2d/campaign/__init__.py` | `campaign` facade | Reviewed campaign import |
| `python/src/ksdft2effmass/periodic2d/__init__.py` | `periodic2d` facade | Reviewed package import |

## Test mapping

| Test path | Exact pytest node | Evidence ownership | Established behavior |
|---|---|---|---|
| `python/tests/software_verification/ksdft2effmass/periodic2d/campaign/nbands_1/test__Periodic2DIsolatedBandResultDocument.py` | `TestPeriodic2DIsolatedBandResultDocument::test_contract__retains_exact_bytes_and_derives_content_identity` | Class-owned routine | Exact field/module, byte identity, and fixed synthetic digest |
| same | `TestPeriodic2DIsolatedBandResultDocument::test_construction__rejects_nonexact_and_empty_payloads` | Class-owned routine | Strings, byte subclasses, and empty bytes fail closed |
| same | `TestPeriodic2DIsolatedBandResultDocument::test_construction__is_frozen_and_slotted` | Class-owned routine | Frozen and slotted intrinsic state |
| `python/tests/software_verification/ksdft2effmass/periodic2d/campaign/nbands_1/test__integration__periodic_2d_isolated_band_result_document_artifact.py` | `TestPeriodic2DIsolatedBandResultDocumentArtifact::test_retained_result__preserves_exact_bytes_and_catalog_identity` | Artifact-owned claim-bearing integration | Exact retained bytes and checksum-catalog identity |
| same | `TestPeriodic2DIsolatedBandResultDocumentArtifact::test_public_routes__share_result_document_without_definition_alias` | Artifact-owned integration | Three facades share the defining class; former owner has no alias |

## Sphinx mapping

| Sphinx path | Documented route | Role |
|---|---|---|
| `doc/sphinx/api/ksdft2effmass/periodic2d/campaign/nbands_1/serialization.rst` | `ksdft2effmass.periodic2d.campaign.nbands_1.Periodic2DIsolatedBandResultDocument` | User-facing encoded-result ownership and API |
| `doc/sphinx/api/research-monograph-campaigns.rst` | Same public class | Research-campaign API index |

## Evidence and scientific claim boundary

| Question | Status | Reason |
|---|---|---|
| Exact byte ownership | Supported | Intrinsic routine evidence |
| SHA-256 derivation | Supported | Fixed synthetic and retained-artifact evidence |
| Retained file identity | Supported | Reviewed digest literal and maintained checksum catalog |
| JSON decoding or schema correctness | Not claimed | Owned by explicit serializer/decoder Actions |
| Historical calculation execution | Not claimed | No execution record or native output is authenticated here |
| Scientific model or represented operator identity | Not claimed | No scientific metadata is owned by this DataObject |
| Convergence, validation, UQ, or acceptance | Not claimed | No scientific decision contract is evaluated |

## Provenance and limitations

The source and documentation are repository-maintained under the project license. No
retained artifact, checksum catalog, calculator output, dependency, or scientific
parameter is changed by row 056. Passing the mapped tests establishes bounded software
behavior and content identity only. Row 067 retains ownership of broader isolated-band
campaign decomposition.
