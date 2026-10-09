# `periodic1d.campaign.composite`

## Purpose and row-059 status

This package is the canonical owner of the periodic-1D composite campaign family.
`PERIODIC-XWALK-059` moved the campaign definition, request/result records, exact encoded
documents, correlation, bounded independent verification, orchestration, and scientific
adoption together. The former `ksdft2effmass.campaigns.periodic_1d` and
`ksdft2effmass.campaigns.research_monograph` facades expose no composite compatibility
aliases; former deep composite modules are absent.

The reviewed import routes are:

- `ksdft2effmass.periodic1d.campaign`; and
- `ksdft2effmass.periodic1d.campaign.composite`.

Both routes expose the same class objects. Importing the canonical campaign facade does
not initialize the transitional `ksdft2effmass.campaigns.periodic_1d` package.

## Ownership map

| Module | Responsibility | Navigation |
|---|---|---|
| `definition` | Immutable schema-one controls, explicit parent-qualified retained-band groups, and strict JSON serialization | [Definition](definition/index.md) |
| `results` | Immutable represented diagnostic channels and strict retained-result serialization | [Results](results/index.md) |
| `encoded_documents` | Exact input/result bytes only | [Encoded documents](encoded_documents/index.md) |
| `correlation_workflow`, `correlation` | Strict decoding, exact content identities, input/result inventory binding | [Correlation](correlation_workflow/index.md) |
| `campaign` | Encapsulated request-to-operation owner with fresh Actions per invocation | [Campaign](campaign/index.md) |
| `numerical_verification`, `verification` | Independent reconstruction of available channels and explicit unavailable-channel accounting | [Verification](verification/index.md) |
| `verified_workflow` | Correlation followed by bounded independent verification | [Verified workflow](verified_workflow/index.md) |
| `adoption` | Correlated construction of explicit finite-parent retained spaces/operators and represented forms | [Scientific adoption](adoption/index.md) |

## Scientific-object boundaries

The campaign definition is a control record, not a physical model. Its plane-wave
cutoff declares a finite parent representation, while each retained-band group carries
an explicit `Periodic1DSelectedBandRetentionDefinition` qualified to the declared
untruncated parent operator and reciprocal domain. Adoption derives a separate
finite-representation-qualified retention record. Neither definition is a projector or
proof of spectral isolation. The source campaign result owns finite diagnostic evidence,
not the retained mathematical space or exact retained operator.

Scientific adoption therefore constructs separate explicit objects:

1. finite plane-wave parent representation;
2. finite-parent-qualified retained subspace;
3. exact retained operator on that space;
4. smooth-gauge reciprocal represented operator samples;
5. complete smooth- and rough-gauge hopping represented forms; and
6. source-object correlation preserving the unchanged campaign result.

A gauge transformation can preserve a retained subspace and represented spectrum while
changing matrix entries and hopping locality. Complete discrete Fourier representation,
finite-range truncation, and direct finite-range fitting remain different operations.
Parent-model, finite-discretization, retention, gauge, transform, truncation, fit,
sampling/aliasing, and comparison errors are not collapsed. The exact source result
retains a reported smooth-projector digest string, but projector bytes are unavailable;
the adoption therefore cannot authenticate that digest against projector content.

## Retained artifacts and provenance boundary

The maintained calculation directory is
`calculations/research-monograph/periodic-1d/`. Row 059 preserves these data identities:

- `composite-input.json`:
  `2ce60a96b72747a820c68b05aa9dbe0beaecb5de03fd5e336c9c77cc7bf5fc20`;
- `composite-result.json`:
  `9231057d96be5e7277e5d76d7272a9bad0a00b02996b7e989164ab619e19c02f`.

`verify_composite.py` changed only its canonical import/documentation surface; its new
source identity, `0cba98bba1d37e445c6c5d7f353159c5db3fd4d68e31bdb7f6a077d231521aac`,
is recorded in `SHA256SUMS`. That script identity is separate from the
unchanged input/result wires. SHA-256 establishes exact content identity only—not
authorship, historical execution, repository provenance, decoded correctness,
numerical reproduction, convergence, scientific validation, uncertainty
quantification, or acceptance. No Quantum ESPRESSO, Wannier90, external, or production
calculation was invoked for this move.

## Evidence map

Routine intrinsic evidence includes:

- `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/composite/test__Periodic1DCompositeCampaignDefinition.py::TestPeriodic1DCompositeCampaignDefinition`;
- `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/composite/test__Periodic1DCompositeEncodedDocuments.py::TestPeriodic1DCompositeEncodedDocuments`.

Claim-bearing class-owned evidence includes the exact nodes rooted at:

- `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/composite/test__Periodic1DCompositeCampaign.py::TestPeriodic1DCompositeCampaign`;
- `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/composite/test__Periodic1DCompositeCampaignWorkflow.py::TestPeriodic1DCompositeCampaignWorkflow`;
- `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/composite/test__Periodic1DCompositeCampaignJsonSerializer.py::TestPeriodic1DCompositeCampaignJsonSerializer`;
- `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/composite/test__Periodic1DCompositeResultJsonSerializer.py::TestPeriodic1DCompositeResultJsonSerializer`;
- `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/composite/test__Periodic1DCompositeVerifiedWorkflow.py::TestPeriodic1DCompositeVerifiedWorkflow`;
- `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/composite/test__Periodic1DCompositeScientificAdoption.py::TestPeriodic1DCompositeScientificAdoption`; and
- `python/tests/numerical_verification/ksdft2effmass/periodic1d/campaign/composite/test__Periodic1DCompositeResultVerifier.py::TestPeriodic1DCompositeResultVerifier`.

The artifact-owned integration node is
`python/tests/software_verification/ksdft2effmass/periodic1d/campaign/composite/test__integration__composite_encoded_document_artifacts.py::TestPeriodic1DCompositeEncodedDocumentArtifacts`.
It checks exact retained bytes/checksum identities, canonical class identity, removal of
former routes, and fresh-interpreter canonical import independence. Ownership metadata
is colocated under each canonical test tree's `resources/` directory.

Passing this evidence establishes bounded software and retained numerical consistency
only. It does not establish parent convergence, physical adequacy, a material-property
claim, scientific validation, uncertainty quantification, or acceptance.
