# `periodic1d.campaign.alignment.blind`

## Purpose and status

This package is the canonical owner of the periodic-1D synthetic blind-alignment
campaign. Row `PERIODIC-XWALK-062` moves the complete family from
`ksdft2effmass.campaigns.periodic_1d.defects.blind_alignment` without a compatibility
alias or retained-wire change.

The family keeps exact bytes, decoded controls, authenticated baseline adaptation,
inference-visible observations, construction-only hidden truth, numerical inference,
post hoc evaluation, campaign orchestration, retained-result correlation, and
independent verification as separate contracts. None is a physical material model or a
scientific-acceptance record.

## Mathematical contract

For anchor cross-covariance $C=L\Sigma R^\dagger$, singular values strictly above the
explicit rank tolerance define the identified sector and

$$
\widehat U=L_rR_r^\dagger,\qquad
P=\widehat U\widehat U^\dagger.
$$

After estimating the exterior scalar energy shift $\widehat\delta$, the finite
represented perturbation is

$$
\widehat V=\widehat U H_d\widehat U^\dagger
 -\widehat\delta P-PH_0P.
$$

A partial result has meaning only on $\operatorname{ran}P$. The software does not infer
a null-space completion, physical-model identity, represented-space compatibility,
gauge, energy reference, provenance, or acceptance from names, dimensions, spectra,
paths, or hashes.

## Reviewed facade

The leaf facade exports exactly:

- `BlindAlignmentCampaign`; and
- `BlindAlignmentEncodedDocuments`.

The same class objects are exposed deliberately by
`ksdft2effmass.periodic1d.campaign.alignment`. The broader campaign facade does not
flatten this specialized family. Lower-level records and Actions remain available only
from their defining modules. The former underscored family route is absent rather
than forwarded.

## Module hierarchy

| Module | Responsibility | Architecture page |
|---|---|---|
| `baseline` | Authenticate retained matched-extraction inputs and adapt the finite synthetic parent | [Baseline](baseline/index.md) |
| `campaign` | Operation-owned absolute roots, calculation, retained correlation, and narrow facade | [Campaign](campaign/index.md) |
| `case_execution` | Compose observation-only inference with separate post hoc evaluation | [Case execution](case_execution/index.md) |
| `construction` | Build visible observations and separately typed hidden truth | [Construction](construction/index.md) |
| `encoded_documents` | Preserve exact input and retained-result bytes only | [Encoded documents](encoded_documents/index.md) |
| `evaluation` | Compare successful inference against withheld synthetic truth | [Evaluation](evaluation/index.md) |
| `inference` | Full, identified-sector, and explicit rectangular polar-factor routes | [Inference](inference/index.md) |
| `input_records` | Closed immutable campaign controls and source identities | [Input records](input_records/index.md) |
| `records` | Observation, policy, request, and structured inference result | [Core records](records/index.md) |
| `result_encoding` | Canonical result encoding and exact retained correlation | [Result encoding](result_encoding/index.md) |
| `result_records` | Typed retained campaign result hierarchy | [Result records](result_records/index.md) |
| `result_serialization` | Closed version-one result adaptation | [Result serialization](result_serialization/index.md) |
| `serialization` | Closed version-one input adaptation | [Input serialization](serialization/index.md) |
| `verification` | Source authentication and numerically independent reconstruction | [Verification](verification/index.md) |
| `workflow` | Multi-case campaign composition without acceptance authority | [Workflow](workflow/index.md) |

## Information and operation boundaries

`BlindAlignmentEncodedDocuments` owns two exact nonempty byte sequences and no
filesystem location. `BlindAlignmentCampaignCalculationRequest`,
`BlindAlignmentCampaignRetainedCorrelationRequest`, and
`BlindAlignmentCampaignVerificationRequest` each own an explicit absolute repository
root. Their constructors validate representation and confinement syntax without reading
the filesystem. Executing Actions authenticate bytes before consuming source-owned
scientific metadata.

The observation constructor places the authored map, scalar shift, and planted defect
only in `BlindAlignmentHiddenTruth`. `BlindAlignmentInference` receives only
the observation and policy. `BlindAlignmentInferenceEvaluator` consumes hidden truth
only after inference and cannot alter the inferred result.

## Numerical and failure boundaries

Dense SVD, eigensolver, and matrix-product routes require cubic time and quadratic
storage in represented dimension. No arbitrary dimension cap is imposed; allocation
failure may raise `MemoryError`. Public numerical boundaries reject booleans and numeric
strings. Unsupported semantic representations raise `TypeError`; closed-schema,
compatibility, identity, and domain failures raise `ValueError`; finite binary64 or
complex128 representation failures raise `OverflowError` where conversion occurs.
Structured campaign stops remain results rather than exceptions when the input is valid
but rank, spin, subspace angle, conditioning, or energy-anchor policy is not satisfied.

## Code mapping

| Source path | Principal symbols |
|---|---|
| `python/src/ksdft2effmass/periodic1d/campaign/alignment/blind/baseline.py` | `BlindAlignmentBaselineData`, `BlindAlignmentBaselineLoader`, `BlindAlignmentParentModelAdapter` |
| `python/src/ksdft2effmass/periodic1d/campaign/alignment/blind/campaign.py` | `BlindAlignmentCampaign`, calculation and retained-correlation requests/Actions |
| `python/src/ksdft2effmass/periodic1d/campaign/alignment/blind/construction.py` | observation construction request/result, `BlindAlignmentHiddenTruth`, constructor |
| `python/src/ksdft2effmass/periodic1d/campaign/alignment/blind/inference.py` | `BlindAlignmentInference` |
| `python/src/ksdft2effmass/periodic1d/campaign/alignment/blind/evaluation.py` | evaluation request/result and evaluator |
| `python/src/ksdft2effmass/periodic1d/campaign/alignment/blind/workflow.py` | workflow request and `BlindAlignmentCampaignWorkflow` |
| `python/src/ksdft2effmass/periodic1d/campaign/alignment/blind/verification.py` | verification request/result and independent verifier |
| remaining sibling modules | strict input/result records, wire adaptation, canonical encoding, and case composition |

## Tests and retained evidence

The mirrored implementation and test root is
`python/tests/ksdft2effmass/periodic1d/campaign/alignment/blind/`. Its eight cohesive
modules exercise strict input and result contracts, authenticated baseline adaptation,
observation construction, inference, post hoc evaluation, campaign composition, and
independent reconstruction. Artifact and route evidence lives at
`python/tests/software_verification/ksdft2effmass/periodic1d/campaign/alignment/blind/`
and is declared by its `resources/implementation-verification-ownership.json`.

Canonical migration nodes are:

- `TestCanonicalBlindAlignmentFamily::test_facades__export_defining_class_objects_only`;
- `TestCanonicalBlindAlignmentFamily::test_former_route__is_absent_without_forwarding_alias`;
- `TestCanonicalBlindAlignmentFamily::test_layout__mirrors_canonical_implementation_namespace`;
- `TestBlindAlignmentEncodedDocuments` (three intrinsic exact-byte nodes); and
- `TestBlindAlignmentEncodedDocumentArtifacts` (retained identity and request-location nodes).

Retained evidence remains byte-for-byte unchanged:

| Artifact | SHA-256 |
|---|---|
| `calculations/research-monograph/impurity-defect-1d-blind-alignment/input.json` | `3476c0b1ed45913e5386be3688528d549f7eea15840b67559763d875406d7d48` |
| `calculations/research-monograph/impurity-defect-1d-blind-alignment/result.json` | `a3b7d20c870fe5d87fd6a591fbafe9a997e7a261a5bc08163c3273b4789416fe` |

SHA-256 establishes content identity only. No artifact is rewritten by this migration.

## Sphinx and scientific limits

The complete source API is documented by
`doc/sphinx/api/ksdft2effmass/periodic1d/campaign/alignment-blind.rst`; the broader
campaign narrative remains in `doc/sphinx/api/research-monograph-campaigns.rst` and
`doc/sphinx/concepts/periodic-1d-defect-extraction.rst`.

Passing software or numerical checks establishes only the bounded synthetic contracts.
It does not establish material behavior, transferability, convergence, physical
adequacy, scientific validation, uncertainty quantification, or acceptance. No Quantum
ESPRESSO or Wannier90 execution is part of this family migration.

## Resolved dependency boundary

Rows 030--032 and 065 supplied canonical represented-operator, finite-fiber,
matched-extraction, and finite-supercell owners. The authenticated baseline consumes
matched-extraction records, strict wire adaptation, and finite-supercell construction
from those canonical owners. Their class objects are not forwarded by the removed
blind-alignment route. Row 030's explicit metadata contracts and row 065's
matched-extraction family eliminate the former canonical-to-transitional dependency;
scientific identity is not duplicated or inferred here. Importing the specialized
canonical leaf loads no module beneath `campaigns.periodic_1d`.

Original local work under the repository license.
