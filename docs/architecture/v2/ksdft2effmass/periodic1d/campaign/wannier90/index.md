# `periodic1d.campaign.wannier90`

## Purpose and status

This package is the canonical row-061 owner of the retained periodic-1D Wannier90
campaign. It owns exact encoded documents, closed version-one result adaptation,
result-to-input authentication, explicit native-artifact correlation, independent
Wilson-loop verification, verified Workflow composition, and a cohesive integration
facade. Generic native Wannier90 parsing remains in
`ksdft2effmass.integration.wannier90`.

The former `ksdft2effmass.campaigns.periodic_1d` modules, `run.wannier90` package,
serialization wrapper, comparison wrapper, and research-monograph facade exports are
removed rather than forwarded.

## Scientific and execution boundary

This package does not define a physical model, retained mathematical state space,
represented Hamiltonian, effective model, topology result, polarization result,
material property, uncertainty statement, or scientific acceptance decision. It does
not discover paths or execute Quantum ESPRESSO or Wannier90. SHA-256 values establish
exact content identity only. The explicit result kind selects the schema first and is
then required to agree with the source's preconditioning declaration. Result-first
correlation authenticates the still-opaque composite input before input-owned
scientific controls are decoded. Integrated verification preserves that correlation
and requires it to identify the exact result bytes consumed by native verification.

The independent verifier forms Wilson loops from unitary polar factors of selected
native overlap matrices. Its second numerical route applies retained native gauge
matrices before loop formation. Circular phase assignment, loop unitarity, and overlap
conditioning remain separate diagnostics under explicit caller-supplied bounds. For a
multi-group request, every logical name, byte count, and digest is authenticated before
any group's scientific text is parsed.

## Implemented module hierarchy

| Module | Responsibility | Dossier |
|---|---|---|
| `encoded_documents` | Exact composite-input/result bytes and explicit result kind | [Encoded documents](encoded_documents/index.md) |
| `results` | Closed result schema, typed Wilson/center observations, circular comparison | [Results](results/index.md) |
| `correlation` | Result-first input authentication and ordered group correlation | [Correlation](correlation/index.md) |
| `native_artifacts` | Whole-request native inventory authentication barrier, parsing, and group correlation | [Native artifacts](native_artifacts/index.md) |
| `verification` | Numerically independent Wilson-loop verification | [Verification](verification/index.md) |
| `verified_workflow` | Ordered native authentication and independent verification composition | [Verified Workflow](verified_workflow/index.md) |
| `integration_correlation` | Correlation Action for the integration facade | [Integration correlation](integration_correlation/index.md) |
| `integration_verification` | Result-first campaign correlation followed by same-result native verification | [Integration verification](integration_verification/index.md) |
| `integration` | Immutable cohesive campaign facade | [Integration](integration/index.md) |

## Supported imports and documentation

The reviewed public imports are
`ksdft2effmass.periodic1d.campaign.<ClassName>` and
`ksdft2effmass.periodic1d.campaign.wannier90.<ClassName>`. Sphinx maps all public
classes at
`doc/sphinx/api/ksdft2effmass/periodic1d/campaign/wannier90.rst`.

## Exact evidence nodes

The canonical software evidence is owned by these exact pytest classes:

- `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/wannier90/test__Periodic1DWannier90EncodedDocuments.py::TestPeriodic1DWannier90EncodedDocuments`;
- `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/wannier90/test__Periodic1DWannier90ResultJsonSerializer.py::TestPeriodic1DWannier90ResultJsonSerializer`;
- `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/wannier90/test__Periodic1DWannier90CampaignWorkflow.py::TestPeriodic1DWannier90CampaignWorkflow`;
- `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/wannier90/test__Periodic1DWannier90NativeArtifactGroup.py::TestPeriodic1DWannier90NativeArtifactGroup`;
- `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/wannier90/test__Periodic1DWannier90NativeArtifactWorkflow.py::TestPeriodic1DWannier90NativeArtifactWorkflow`;
- `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/wannier90/test__Periodic1DWannier90WilsonVerifier.py::TestPeriodic1DWannier90WilsonVerifier`;
- `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/wannier90/test__Periodic1DWannier90VerifiedNativeWorkflow.py::TestPeriodic1DWannier90VerifiedNativeWorkflow`;
- `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/wannier90/test__Periodic1DWannier90Integration.py::TestPeriodic1DWannier90Integration`; and
- `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/wannier90/test__integration__wannier90_encoded_document_artifacts.py::TestPeriodic1DWannier90EncodedDocumentArtifacts`.

The ownership manifest is
`python/tests/software_verification/ksdft2effmass/periodic1d/campaign/wannier90/resources/implementation-verification-ownership.json`.
Passing these tests establishes the documented software behavior and bounded synthetic
numerical reconstruction only; it does not establish calculator correctness,
convergence, physical adequacy, scientific validation, UQ, or acceptance.

## Retained provenance

The exact retained result identities remain:

- `wannier90-result.json`:
  `d167294da9ebb53173b91fa69f089900f11e03917969bc028b9c0e69db951535`;
- `wannier90-preconditioned-result.json`:
  `c4d6d32f8a52e93c447424b49b649e63fa036117bf88a4f8af6ed4e1d270316c`.

No retained wire, calculator output, or external native root is modified by this
migration.
