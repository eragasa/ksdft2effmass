# Migration phase 3: encoded campaign documents

## Status

**Implemented on the work branch.** Rows 037--057 are implemented through
`work/periodic-wannier90-encoded-documents`. The periodic-1D campaign remains under
development, so its calculation-directory verifier adapters and checksum catalog
evolve with the public campaign API.

The phase gate passed the bounded suite excluding the package-wheel module (4,420
passed and three external-Quantum-ESPRESSO fixtures skipped), the complete expensive
profile (148 passed), Ruff, formatting, source mypy, strict Sphinx, the seven applicable
checksum catalogs, retired-name scans, and diff checks. The two package-wheel tests were
unavailable because the locked worktree environment does not contain ``pip``; this is
an environment limitation outside the migrated periodic surfaces.

## Purpose

Correct software names and ownership for records that preserve encoded campaign input,
result, or auxiliary documents. This phase is a terminology and ownership migration,
not a scientific-retention implementation.

## Included crosswalk entries

Phase 3 implements `PERIODIC-XWALK-037` through `PERIODIC-XWALK-057` from
[`current-to-target-class-crosswalk.md`](current-to-target-class-crosswalk.md).

## Crosswalk implementation checklist

A box is checked only after the source disposition, affected imports and exports,
tests, documentation, and preservation checks for that exact migration unit are
complete. Renaming a definition without migrating every consumer does not complete an
entry.

### Pure periodic1d document containers

- [x] `PERIODIC-XWALK-037`: replace
  `Periodic1DIsolatedBandCampaignModel` with
  `Periodic1DIsolatedBandEncodedDocuments`.
- [x] `PERIODIC-XWALK-038`: replace `Periodic1DCompositeCampaignModel` with
  `Periodic1DCompositeEncodedDocuments`.
- [x] `PERIODIC-XWALK-039`: replace `Periodic1DStressCampaignModel` with
  `Periodic1DReductionChallengeEncodedDocuments`. The target name describes challenges
  to the nominal reduction assumptions and does not denote mechanical stress.

#### Row-037 reconciliation dossier

The current audit confirms that `Periodic1DIsolatedBandEncodedDocuments` owns exactly
`input_payload` and `result_payload` as nonempty exact built-in `bytes`, preserves each
caller-supplied byte object without decoding or copying, and remains an encoded document
rather than a physical model, retained space/operator, represented operator, effective
model, or campaign result. The retired definition and source module are absent. Row 058 subsequently moved the
owner into `periodic1d.campaign.isolated.encoded_documents`; its canonical campaign
and leaf facades export the same implementation class, while former underscored and
research-monograph facades retain no alias.

The maintained `input.json` and `result.json` artifacts remain at
`calculations/research-monograph/periodic-1d/` with SHA-256 identities
`ae17de790380dee76693e984b96fbb22773a40440e267d3e77b4543cafaad6fb` and
`37a4619e3a6ebf1c8ec9fac9f4c7cb5398ffe27254003529f736987c5f0bf71c`.
Routine class-owned software evidence verifies fields, immutability, exact synthetic
byte-object preservation, and rejection of wrong or empty representations. Separate
claim-bearing artifact-owned integration evidence verifies the maintained byte objects,
both checksum-catalog identities, canonical facades, and transitional-route removal.
The canonical scientist-facing dossier is
[`Periodic1DIsolatedBandEncodedDocuments`](../periodic1d/campaign/isolated/encoded_documents/Periodic1DIsolatedBandEncodedDocuments/index.md).
These checks establish bounded software and content-identity behavior only; they do not
authenticate provenance or establish decoded semantic correctness, scientific
validation, convergence, physical adequacy, uncertainty quantification, or acceptance.

#### Row-038 reconciliation dossier

The current audit confirms that `Periodic1DCompositeEncodedDocuments` owns exactly
`input_payload` and `result_payload` as nonempty exact built-in `bytes`, preserves each
caller-supplied byte object without decoding or copying, and remains an encoded document
rather than a physical model, retained band group, frame, retained or represented
operator, effective model, or decoded campaign result. Both reviewed public facades
export the same implementation class; the retired definition, source module, export,
and forwarding route are absent.

The maintained `composite-input.json` and `composite-result.json` artifacts remain at
`calculations/research-monograph/periodic-1d/` with SHA-256 identities
`2ce60a96b72747a820c68b05aa9dbe0beaecb5de03fd5e336c9c77cc7bf5fc20` and
`9231057d96be5e7277e5d76d7272a9bad0a00b02996b7e989164ab619e19c02f`.
Routine class-owned software evidence verifies fields, immutability, exact synthetic
byte-object preservation, and rejection of wrong or empty representations. Separate
claim-bearing artifact-owned integration evidence verifies the maintained byte objects,
both checksum-catalog identities, supported facades, and retired-route removal. The canonical scientist-facing dossier is
[`Periodic1DCompositeEncodedDocuments`](../periodic1d/campaign/composite/encoded_documents/Periodic1DCompositeEncodedDocuments/index.md).
These checks do not reconstruct unavailable frames, projectors, rough reciprocal
matrices, or withheld matrices, and they do not authenticate provenance or establish
decoded semantic correctness, scientific validation, convergence, physical adequacy,
uncertainty quantification, or acceptance.

#### Row-039 reconciliation dossier

The current audit confirms that `Periodic1DReductionChallengeEncodedDocuments` owns
exactly `input_payload` and `result_payload` as nonempty exact built-in `bytes`,
preserves each caller-supplied byte object without decoding or copying, and remains an
encoded document rather than a physical model, finite representation, retained space or
operator, represented operator, effective model, or decoded campaign result. Both
reviewed public facades export the same implementation class; the retired definition,
source module, export, and forwarding route are absent.

“Reduction challenge” describes adversarial tests of potential, discretization,
band-isolation, gauge, hopping-range, and fitting-route assumptions. It does not denote
mechanical stress, strain, elasticity, or a stress tensor. The historical
`stress-input.json` and `stress-result.json` names, experiment identity
`research-monograph.periodic-1d.stress.v1`, and exact version-one wire bytes remain
unchanged. Renaming the Python document owner does not reinterpret or rewrite them.

The maintained files remain at `calculations/research-monograph/periodic-1d/` with
SHA-256 identities
`3be86c6ee7cb08c1c194aa97e856c89458907c23428bed19f6b38cdb437d987a` and
`5897e16570609f3b2ad2fb5cdefb39b8da9df6395e42796d8c5af77734cba394`.
Routine class-owned software evidence verifies fields, immutability, exact synthetic
byte-object preservation, and rejection of wrong or empty representations. Separate
claim-bearing artifact-owned integration evidence verifies the maintained byte objects,
both checksum-catalog identities, canonical facades, former-route removal, and fresh-
interpreter import independence. Row 060 subsequently moved the owner with its complete
family to `periodic1d.campaign.reduction_challenge.encoded_documents`. The canonical
scientist-facing dossier is
[`Periodic1DReductionChallengeEncodedDocuments`](../periodic1d/campaign/reduction_challenge/encoded_documents/Periodic1DReductionChallengeEncodedDocuments/index.md).
These checks do not decode or independently reconstruct challenge channels, attribute
numerical errors, authenticate provenance, validate a reduction, establish convergence
or physical adequacy, quantify uncertainty, or record acceptance.

#### Row-040 reconciliation dossier

The current audit confirms the split of the retired
`Periodic1DWannier90IntegrationModel` into three distinct responsibilities.
`Periodic1DWannier90EncodedDocuments` owns exactly the composite-input bytes,
Wannier90-result bytes, and explicit encoded-result kind.
`Periodic1DWannier90NativeArtifactGroup` separately owns one explicit group key and a
nonempty ordered tuple of uniquely named native artifact records.
`Periodic1DWannier90Integration` composes encoded documents and zero or more explicit
groups without discovering paths or executing Wannier90. The retired aggregate
definition, source module, export, alias, and forwarding route are absent.

The encoded owner supports only `WANNIER90` and `WANNIER90_PRECONDITIONED`; it does not
infer a kind from bytes, filenames, ranks, or native-file presence. The maintained
`composite-input.json`, `wannier90-result.json`, and
`wannier90-preconditioned-result.json` artifacts remain at
`calculations/research-monograph/periodic-1d/` with SHA-256 identities
`2ce60a96b72747a820c68b05aa9dbe0beaecb5de03fd5e336c9c77cc7bf5fc20`,
`d167294da9ebb53173b91fa69f089900f11e03917969bc028b9c0e69db951535`, and
`c4d6d32f8a52e93c447424b49b649e63fa036117bf88a4f8af6ed4e1d270316c`.
Routine class-owned evidence verifies both owners' exact fields and immutability, both
encoded variants, synthetic byte-object and artifact ordering, and fail-closed payload,
kind, group-key, member-type, and unique-name contracts. Separate
claim-bearing artifact-owned integration evidence verifies all three content identities,
explicit variant pairing, separate encoded/native owners, explicit campaign
composition, both supported facades, and retired-route removal. The canonical
scientist-facing dossier is
[`Periodic1DWannier90EncodedDocuments`](../periodic1d/campaign/wannier90/encoded_documents/Periodic1DWannier90EncodedDocuments/index.md).

The audit reads no external native artifact root and invokes no calculator. Content
identity does not establish execution provenance. A supported or preconditioned result
kind does not establish native-file availability, localization convergence, decoded
semantic correctness, physical validity, transferability, uncertainty quantification,
or acceptance. Existing synthetic native-workflow evidence remains a separate software
claim. Row 061 completed the later canonical movement of the integration campaign family.

### Compound periodic1d integration documents

- [x] `PERIODIC-XWALK-040`: split `Periodic1DWannier90IntegrationModel` into
  `Periodic1DWannier90EncodedDocuments` and the existing typed native-artifact-group
  ownership.

### Path-bearing periodic1d defect bundles

- [x] `PERIODIC-XWALK-041`: replace `BlindAlignmentCampaignModel` with
  `BlindAlignmentEncodedDocuments` and move `repository_root` to a campaign request.
- [x] `PERIODIC-XWALK-042`: replace `ContinuumRefinementCampaignModel` with
  `ContinuumRefinementEncodedDocuments`; pass `repository_root` explicitly to retained
  correlation and own it in the independent-verification request.
- [x] `PERIODIC-XWALK-043`: replace `FiniteRankOracleCampaignModel` with
  `FiniteRankOracleEncodedDocuments`; pass `repository_root` explicitly to calculation
  and retained correlation and own it in the independent-verification request.
- [x] `PERIODIC-XWALK-044`: replace `RouteReconciliationCampaignModel` with
  `RouteReconciliationEncodedDocuments` and move `repository_root` to a campaign
  request.

#### Row-041 reconciliation dossier

The row-041 audit confirms that `BlindAlignmentEncodedDocuments` owns exactly the
nonempty exact built-in-byte fields `input_document` and
`retained_result_document`. It performs no decoding, normalization, copying,
filesystem access, or scientific interpretation. Repository location belongs instead
to the explicit `BlindAlignmentCampaignCalculationRequest`,
`BlindAlignmentCampaignRetainedCorrelationRequest`, and
`BlindAlignmentCampaignVerificationRequest` operation boundaries. Those requests
require absolute paths but do not resolve them or authenticate sources during
construction.

Routine class-owned software evidence establishes exact field ownership, synthetic
object identity, fail-closed subtype and emptiness checks, immutability, and absence of
repository state. Separate artifact-owned integration evidence binds the maintained
`input.json` and `result.json` bytes to SHA-256 identities
`3476c0b1ed45913e5386be3688528d549f7eea15840b67559763d875406d7d48` and
`a3b7d20c870fe5d87fd6a591fbafe9a997e7a261a5bc08163c3273b4789416fe`,
respectively, verifies their checksum-catalog entries, confirms the defining-class
facade identity, and confirms removal of the former aggregate name and module.

The [canonical scientist-facing dossier](../periodic1d/campaign/alignment/blind/encoded_documents/BlindAlignmentEncodedDocuments/index.md)
records exact code, test, Sphinx, provenance, and evidence mappings. Content identity
does not establish execution provenance, decoded semantics, hidden-information
separation, numerical reconstruction, scientific validation, uncertainty
quantification, transferability, or acceptance. Row 062 owns the later move of the
campaign family to canonical `periodic1d.campaign.alignment.blind` ownership without
compatibility aliases or wire changes. No calculator execution is part of this audit.

#### Row-042 reconciliation dossier

The row-042 audit confirms that `ContinuumRefinementEncodedDocuments` owns exactly the
nonempty exact built-in-byte fields `input_document` and
`retained_result_document`. It performs no decoding, normalization, copying,
filesystem access, or scientific interpretation. Retained correlation receives an
explicit absolute repository root at its executing facade method, validates it before
decoding or source access, and then uses it for authenticated recalculation. Independent
verification owns exact documents and an absolute root in
`ContinuumRefinementVerificationRequest`; request construction performs no filesystem
access.

Routine class-owned software evidence establishes exact field ownership, synthetic
object identity, fail-closed subtype and emptiness checks, immutability, and absence of
repository state. Separate artifact-owned integration evidence binds maintained
`input.json` and `result.json` bytes to SHA-256 identities
`55d647a8c259d3a1f1e5c756b496a9d1a16fee0a691c7b53d2f877da5f287fdd` and
`1f4029cc953e78eb8231e5a651676401b20d5b74f09ecb8cb38d72aa2e92c2dc`,
respectively, verifies checksum-catalog entries, confirms the defining-class facade
identity, exercises fail-closed path boundaries without executing refinement, and
confirms removal of the former aggregate name and module.

The [canonical scientist-facing dossier](../periodic1d/campaign/refinement/continuum/encoded_documents/ContinuumRefinementEncodedDocuments/index.md)
records exact code, test, Sphinx, provenance, and evidence mappings. Content identity
does not establish execution provenance, decoded semantics, independent numerical
reconstruction, asymptotic convergence, continuum-limit validity, material adequacy,
transferability, uncertainty quantification, or acceptance. Row 063 subsequently moved
the complete family to canonical `periodic1d.campaign.refinement.continuum` ownership
without aliases or wire changes. No calculator execution is part of this audit.

#### Row-043 reconciliation dossier

The row-043 audit confirms that `FiniteRankOracleEncodedDocuments` owns exactly the
nonempty exact built-in-byte fields `input_document` and
`retained_result_document`. It performs no decoding, normalization, copying,
filesystem access, root solve, eigensolve, oracle qualification, or scientific
interpretation. Calculation and retained correlation receive explicit absolute
repository-root arguments at their executing facade methods and validate location
before payload decoding or source access. Independent verification owns exact documents
and an absolute root in `FiniteRankOracleVerificationRequest`; request construction
performs no filesystem access.

Routine class-owned software evidence establishes exact field ownership, synthetic
object identity, fail-closed subtype and emptiness checks, immutability, and absence of
repository state. Separate artifact-owned integration evidence binds maintained
`input.json` and `result.json` bytes to SHA-256 identities
`ab653338be4f1733c8dd39878526b3293e603f2f0b0e7b8241577db2406c5840` and
`64ab16a279d5f8ca18f725dadb15860811a45ea12758a91a7cd7166f6074dae0`,
respectively, verifies checksum-catalog entries, confirms the defining-class facade
identity, verifies encapsulated/repository input correlation and fail-closed path
boundaries without entering finite numerical reconstruction, and confirms removal of the former aggregate name and module.

The [canonical scientist-facing dossier](../periodic1d/campaign/oracle/finite_rank/encoded_documents/FiniteRankOracleEncodedDocuments/index.md)
records exact code, test, Sphinx, provenance, and evidence mappings. It distinguishes
the retained legacy runner digest from current adapter bytes and newer explicit
implementation identities. Content identity does not establish execution provenance,
decoded semantics, independent numerical reconstruction, infinite-volume or continuum
convergence, oracle qualification beyond the exact campaign evidence class, material
adequacy, transferability, uncertainty quantification, or acceptance. Row 064
subsequently moved the complete family to canonical
`periodic1d.campaign.oracle.finite_rank` ownership without aliases or wire changes. No
calculator execution is part of this audit.

#### Row-044 reconciliation dossier

The row-044 audit confirms that `RouteReconciliationEncodedDocuments` owns exactly
nonempty exact built-in `input_document` and `retained_result_document` bytes. It
performs no copying, decoding, normalization, source authentication, filesystem access,
route construction, reconciliation, or scientific interpretation. Distinct
`RouteReconciliationCalculationRequest`,
`RouteReconciliationRetainedCorrelationRequest`, and
`RouteReconciliationVerificationRequest` records own the absolute root for their exact
operation. Request construction checks only type and lexical absoluteness and performs
no filesystem access.

Routine class-owned software evidence establishes exact field ownership, synthetic
object identity, fail-closed subtype and emptiness checks, immutability, and absence of
repository state. Separate artifact-owned integration evidence binds maintained
`input.json` and `result.json` bytes to SHA-256 identities
`aa7bd0750556bca3199678877f9ca2cd340f6c6b02885d6019c56173e912953f` and
`861097a6156999b615edd27cf68dcf36fd110248b9d24dc1b862eff5eeec3bdc`,
respectively, verifies checksum-catalog entries, confirms the defining-class facade
identity, verifies encapsulated/repository input correlation and request-root
boundaries without entering either numerical route, and confirms removal of the former aggregate name and module.

The [canonical scientist-facing dossier](../periodic1d/campaign/reconciliation/route/encoded_documents/RouteReconciliationEncodedDocuments/index.md)
records exact code, test, Sphinx, provenance, and evidence mappings and keeps the frozen
historical runner identity distinct from current adapter bytes. Content identity does
not establish execution provenance, decoded semantics, numerical reconstruction,
continuum or infinite-volume convergence, material adequacy, transferability,
uncertainty quantification, or acceptance. Row 066 subsequently moved the complete
family to canonical `periodic1d.campaign.reconciliation.route` ownership without
aliases or wire changes. No calculator execution is part of this audit.

### Periodic1d encoded result documents

- [x] `PERIODIC-XWALK-045`: replace `Periodic1DRetainedResultDocument`,
  `Periodic1DRetainedResultKind`, and `Periodic1DRetainedResultJsonSerializer` with
  `Periodic1DEncodedResultDocument`, `Periodic1DEncodedResultKind`, and
  `Periodic1DEncodedResultJsonSerializer`.

The renamed frozen owner now retains the exact nonempty source bytes as well as the
complete immutable JSON tree and validates that the tree decodes from those bytes and
that `source_sha256` identifies them. Shared strict parsing and immutable JSON ownership
now reside in `ksdft2effmass.serialization.json`; periodic-specific JSON container names
are retired without aliases. The six historical wire-kind values are unchanged and
explicit rather than inferred.
`serialize` emits canonical JSON; it does not misrepresent canonical bytes as the exact
historical source wire. The old class names and `decode`/`encode` forwarding methods
remain absent. Row 058 subsequently moved the shared document and decoder owners to
`periodic1d.campaign.result_documents` and `periodic1d.campaign.serialization` so the
first canonical family does not depend on the transitional underscored package. The
canonical campaign facade exposes them; former underscored and publication facades
retain no alias. Routine evidence is class-owned, while a separate integration module
binds all six maintained result wires and `SHA256SUMS` entries. The
[canonical dossier](../periodic1d/campaign/result_documents/Periodic1DEncodedResultDocument/index.md)
records exact code, imports, tests, hashes, Sphinx mapping, and claim boundaries.
Content identity and JSON persistence do not establish input correlation, provenance,
native-file presence, convergence, scientific validity, uncertainty, or acceptance.

### Periodic2d document containers

- [x] `PERIODIC-XWALK-046`: replace
  `Periodic2DIsolatedBandCampaignModel` with
  `Periodic2DIsolatedBandEncodedDocuments`.

The [row-046 canonical dossier](../periodic2d/campaign/nbands_1/encoded_documents/Periodic2DIsolatedBandEncodedDocuments/index.md)
confirms a frozen slotted exact-byte owner under canonical
`periodic2d.campaign.nbands_1`, three reviewed facades, absence of the retired name,
NumPy-style source and Sphinx documentation, class-owned synthetic evidence, and
artifact-owned binding of `input.json` and `result.json` to their maintained
`SHA256SUMS` identities. No payload was decoded, normalized, rewritten, or assigned
scientific meaning. Content identity does not establish provenance, numerical
reproduction, convergence, scientific validation, uncertainty, or acceptance. Row 056
separately audits the result-document owner, and row 067 owns wider campaign
decomposition.

- [x] `PERIODIC-XWALK-047`: replace `Periodic2DCompositeCampaignModel` with
  `Periodic2DCompositeEncodedDocuments`.

The [row-047 canonical dossier](../periodic2d/run/composite/encoded_documents/Periodic2DCompositeEncodedDocuments/index.md)
confirms a frozen slotted exact-byte owner, two reviewed facades, absence of the retired
name and source module, NumPy-style source and Sphinx documentation, class-owned
synthetic evidence, and artifact-owned binding of `composite-input.json` and
`composite-result.json` to maintained `SHA256SUMS` identities. No payload was decoded,
normalized, rewritten, or used to infer a retained space, frame, gauge, projector, or
operator. Content identity does not establish provenance, numerical reproduction,
convergence, scientific validation, uncertainty, or acceptance. Row 068 owns wider
composite-campaign decomposition and typed result adoption.

- [x] `PERIODIC-XWALK-048`: replace `Periodic2DTopologicalCampaignModel` with
  `Periodic2DTopologicalEncodedDocuments`.

The [row-048 canonical dossier](../periodic2d/run/topological/encoded_documents/Periodic2DTopologicalEncodedDocuments/index.md)
confirms a frozen slotted exact-byte owner, two reviewed facades, absence of the retired
name and source module, NumPy-style source and Sphinx documentation, class-owned
synthetic evidence, and artifact-owned binding of `topological-input.json` and
`topological-result.json` to maintained `SHA256SUMS` identities. No payload was decoded,
normalized, rewritten, or used to infer a model, phase, topological invariant, or
scientific conclusion. Encoded expected observations remain retained campaign content,
not qualified numerical oracles. Content identity does not establish provenance,
numerical reproduction, convergence, scientific validation, uncertainty, or
acceptance. Row 069 owns wider topological-observation decomposition.

- [x] `PERIODIC-XWALK-049`: replace
  `Periodic2DTopologicalPhaseSweepCampaignModel` with
  `Periodic2DTopologicalPhaseSweepEncodedDocuments`.

The [row-049 canonical dossier](../periodic2d/run/topological/phase_sweep/encoded_documents/Periodic2DTopologicalPhaseSweepEncodedDocuments/index.md)
confirms a frozen slotted exact-byte owner, two reviewed facades, absence of the retired
name and source module, NumPy-style source and Sphinx documentation, class-owned
synthetic evidence, and artifact-owned binding of
`topological-phase-sweep-input.json` and `topological-phase-sweep-result.json` to
maintained `SHA256SUMS` identities. No payload was decoded, normalized, rewritten, or
used to infer parameter-axis semantics, sample availability, a model, a phase, a
topological invariant, or a scientific conclusion. Encoded axes and expected
observations remain retained campaign content, not qualified numerical oracles.
Unavailable outcomes remain unavailable. Content identity does not establish
provenance, numerical reproduction, convergence, scientific validation, uncertainty,
or acceptance. Row 069 owns wider topological-observation decomposition.

- [x] `PERIODIC-XWALK-050`: replace
  `Periodic2DWannier90BalancedCampaignModel` with
  `Periodic2DWannier90BalancedEncodedDocuments`.

The [row-050 canonical dossier](../periodic2d/run/wannier90/balanced/encoded_documents/Periodic2DWannier90BalancedEncodedDocuments/index.md)
confirms a frozen slotted exact-result-byte owner, three reviewed facades, absence of
the retired name and source module, NumPy-style source and Sphinx documentation,
class-owned synthetic evidence, and artifact-owned binding of
`wannier90-balanced-result.json` to its maintained `SHA256SUMS` identity. The reviewed
contract contains no encoded input field, so none was invented. No payload was decoded,
normalized, rewritten, or used to infer native-file presence, execution provenance,
localization convergence, optimizer validity, model identity, or a scientific
conclusion. Content identity does not establish decoded correctness, numerical
reproduction, scientific validation, uncertainty, or acceptance.

- [x] `PERIODIC-XWALK-051`: replace `Periodic2DWannier90StudyCampaignModel` with
  `Periodic2DWannier90StudyEncodedDocuments`.

The [row-051 canonical dossier](../periodic2d/run/wannier90/study/encoded_documents/Periodic2DWannier90StudyEncodedDocuments/index.md)
confirms a frozen slotted exact-byte owner, three reviewed facades, absence of the
retired name and source module, NumPy-style source and Sphinx documentation, class-owned
synthetic evidence, and artifact-owned binding of `wannier90-study-input.json` and
`wannier90-study-result.json` to maintained `SHA256SUMS` identities. The retained input
declares six bounded cases over reciprocal-mesh, plane-wave-cutoff, and
auxiliary-embedding axes, but the byte container does not infer axis convergence,
completed execution, native-file presence, localization validity, or scientific
acceptance. Parent-model, discretization, embedding, localization, interpolation, and
comparison errors remain separate. Content identity does not establish provenance,
decoded correctness, numerical reproduction, scientific validation, uncertainty, or
acceptance.

- [x] `PERIODIC-XWALK-052`: replace `Periodic2DOptimizerBasinCampaignModel` with
  `Periodic2DOptimizerBasinEncodedDocuments`.

The [row-052 canonical dossier](../periodic2d/run/wannier90/optimizer_basin/encoded_documents/Periodic2DOptimizerBasinEncodedDocuments/index.md)
confirms a frozen slotted exact-byte owner, three reviewed facades, absence of the
retired name and source module, NumPy-style source and Sphinx documentation, class-owned
synthetic evidence, and artifact-owned binding of `study-input.json` and `result.json`
under `periodic-2d-optimizer-basin/` to maintained `SHA256SUMS` identities. The retained
wire describes nine configurations, eight smooth unitary initial gauges, 72 localization
attempts, and a negative frozen convergence disposition, but the byte container does
not authenticate execution, native files, basin classifications, optimizer validity,
global optimality, or scientific acceptance. Mesh, cutoff, embedding, initialization,
localization, and comparison effects remain separate. The retained negative disposition
must not be rewritten into a convergence claim. The companion
[numerical-techniques and scientific-reasoning note](../periodic2d/run/wannier90/optimizer_basin/numerical-techniques-and-scientific-reasoning.md)
documents the controlled unitary gauge family, parameter sequences, native/common
estimators, operational basin quotient, frozen gates, floating-point reasoning,
portable-verifier scope, observed negative result, and prohibited inferences. The
portable verifier now shares strict duplicate-free finite JSON decoding with the
reviewed serialization infrastructure, requires exact endpoint and nonconverged-list
multiplicity, confines resolved compact-source paths to the repository root, documents
missing-field and source-read failure categories, checks declaration/result uniqueness
before map construction, correlates the complete copied best endpoint, and has focused
adversarial regressions for each boundary. Its public execution route is decomposed into
cohesive source, campaign-metadata, declaration, configuration, summary, basin, and
disposition checks. It preserves distinct input/result evidence roles, exact claim and
authority metadata, observed-only and non-global boundaries, aggregate process
completion, and strict provenance-digest representation. It also correlates study axes,
derives finest-pair identities from axes and declared controls rather than names,
preserves the exact negative disposition and joint stability requirement, and correlates
the four selected embedding-summary fields without assigning physical meaning to
embedding. The immutable
verification Result rejects nonexact flags,
Boolean or noninteger counts, negative counts, and malformed retained-result digests;
direct construction does not claim Action execution. The campaign retains no shared or
replaceable verifier collaborator and creates one verifier Action per request. The
[frozen field-by-field verification contract](../periodic2d/run/wannier90/optimizer_basin/verification-contract.md)
classifies the complete retained schema and makes any additional check a reviewed
contract change rather than open-ended hygiene.

- [x] `PERIODIC-XWALK-053`: replace
  `Periodic2DOptimizerReanalysisCampaignModel` with
  `Periodic2DOptimizerReanalysisEncodedDocuments`.

  The encoded-document owner retains exact source-result and reanalysis-result bytes;
  it does not combine original optimizer observations with downstream diagnostics. The
  campaign-specific `optimizer_basin.reanalysis` package is subordinate to the original
  optimizer-basin owner rather than a generic reanalysis framework. Strict decoding
  adapts verifier-owned fields to closed immutable records. Request-scoped verification
  composes instantiated source-authentication, correlation, terminal-classification,
  spread, periodic-center, basin-partition, and refinement Actions. There are no static
  or class-method utility namespaces and no private computational kernel on the
  orchestration verifier; private methods are limited to cohesive intrinsic
  `_check_args_*` validation on DataObjects and Results. The portable contract
  authenticates compact repository sources and maintained estimator fixtures, but not
  the unavailable external native tree. It reconstructs bounded reported diagnostics
  without changing the row-052 negative convergence disposition or claiming global
  optimality, scientific validation, uncertainty quantification, or acceptance. The
  canonical class dossier and frozen field contract live under
  `periodic2d/run/wannier90/optimizer_basin/reanalysis/encoded_documents/Periodic2DOptimizerReanalysisEncodedDocuments/`.

- [x] `PERIODIC-XWALK-054`: replace
  `Periodic2DOptimizerRegressionCampaignModel` with
  `Periodic2DOptimizerRegressionEncodedDocuments`.

  The encoded-document owner retains exact standalone-result, analyzer-source, and
  regression-result bytes without owning repository location or statistical meaning.
  Request-scoped verification authenticates all three confined maintained sources,
  adapts consumed fields to closed immutable records, constructs the explicit retained
  256-observation/32-parameter design, and independently reconstructs right-censored
  log-normal likelihood, scores, finite-difference Hessian, deterministic-start
  clustered covariance, ratios, intervals, adjusted medians, and six probability
  checkpoints. Cohesive instantiated Actions own decoding, authentication, design,
  numerics, and correlation; no generic statistical framework, registry, plugin,
  static/class-method utility namespace, or private verifier kernel was introduced.

  The exact historical standalone-result wire contains bare `Infinity` only in fields
  outside the row-054 endpoint contract. A bounded campaign-specific adapter rejects
  duplicate keys, exposes no unconsumed nonfinite value, and requires every consumed
  scalar to be finite. The regression-result wire uses shared strict JSON and rejects
  all nonfinite extensions. The 16 starts remain deterministic controls rather than a
  sampled population. Reproduced model-based clustered intervals are neither causal nor
  physical uncertainty, and passing the frozen contract does not prove optimizer
  convergence, predict DFT behavior, establish scientific validation, or record
  acceptance. The canonical dossier and frozen field contract live under
  `periodic2d/run/wannier90/optimizer_basin/convergence_regression/`.
- [x] `PERIODIC-XWALK-055`: replace
  `Periodic2DOptimizerStandaloneCampaignModel` with
  `Periodic2DOptimizerStandaloneEncodedDocuments`.

  The encoded-document owner retains exact proposal, deterministic-start-design, and
  standalone-result bytes without owning repository location, native execution,
  convergence, basin meaning, provenance, validation, or acceptance. Request-scoped
  verification authenticates all three confined maintained wires and the directly
  declared extractor, adapts verifier-owned fields to closed immutable records, and
  independently reconstructs 256 endpoint transitions, native spread algebra,
  terminal-trace classes, summaries, 16 group partitions, best observed endpoints,
  ordered representatives, threshold-qualified basin members, spread-eligible rejected
  comparisons, derived start-block presence, threshold sensitivity, post-hoc controls,
  and the exact negative finite-design disposition.

  Proposal and initial-gauge documents use shared strict JSON. The exact historical
  result wire contains bare positive `Infinity` only at the complete indexed paths of
  two rejected-comparison extended-real fields. A bounded adapter rejects extra nesting,
  missing indices, look-alike ancestors, duplicate keys, `NaN`, `-Infinity`, and
  nonfinite values at every other path. Cohesive instantiated Actions own decoding,
  authentication, endpoint arithmetic, correlation, and orchestration; no registry,
  plugin, static/class-method utility namespace, generic optimizer framework, or private
  replay kernel was introduced. The canonical dossier includes sibling `index.md`,
  `schematic.md`, `numeric.md`, and `scientific.md` pages plus the frozen field contract
  under `periodic2d/run/wannier90/optimizer_basin/standalone/`. Passing establishes
  bounded compact-source and arithmetic consistency only; it does not authenticate
  external native files, prove global or general optimizer convergence, establish
  scientific validation or uncertainty quantification, or record acceptance.

### Existing result-document owners

- [x] `PERIODIC-XWALK-056`: keep
  `Periodic2DIsolatedBandResultDocument` as an encoded result document and move its
  defining implementation from the mixed scientific-definition module to
  `periodic2d.campaign.nbands_1.result_documents` without an alias. The class preserves
  one exact nonempty built-in byte object and derives SHA-256 directly from those bytes.
  Routine and artifact-owned evidence bind intrinsic immutability, strict
  representation rejection, the retained `result.json` and checksum identity, the
  paired-document result bytes, three reviewed facades, and former-owner absence. The
  [canonical dossier](../periodic2d/campaign/nbands_1/result_documents/Periodic2DIsolatedBandResultDocument/index.md)
  distinguishes content identity from schema meaning, decoded correctness, execution,
  provenance, scientific identity, numerical reproduction, convergence, validation,
  UQ, and acceptance. Row 067 retains broader campaign decomposition.
- [x] `PERIODIC-XWALK-057`: verify or move each existing defect result-document owner
  without changing payloads:
  - [x] `ContinuumRefinementCampaignResultDocument`;
  - [x] `FiniteRankOracleCampaignResultDocument`; and
  - [x] `RouteReconciliationCampaignResultDocument`.

#### Row-057 reconciliation dossier

Each class remains by name in its campaign-owned `result_documents.py` module after
its complete family move in row 063, 064, or 066. Each is a frozen, slotted DataObject with a
short delegated validation entry point, exact nonempty built-in-byte acceptance, direct
SHA-256 derivation over those bytes, comprehensive source documentation, and a deliberate
leaf-package facade. No compatibility alias, broad facade, generic result-document
base, registry, factory, plugin point, or inferred scientific metadata was introduced.

Routine class-owned evidence verifies exact field and module ownership, identity
preservation, a fixed synthetic digest, fail-closed string/byte-subclass/empty handling,
and operational immutability. Artifact-owned integration evidence composes each owner
with its campaign's paired encoded-document owner and binds maintained `result.json`
bytes to the `SHA256SUMS` identities
`1f4029cc953e78eb8231e5a651676401b20d5b74f09ecb8cb38d72aa2e92c2dc`,
`64ab16a279d5f8ca18f725dadb15860811a45ea12758a91a7cd7166f6074dae0`, and
`861097a6156999b615edd27cf68dcf36fd110248b9d24dc1b862eff5eeec3bdc` for
continuum refinement, finite-rank oracle, and route reconciliation, respectively.

Canonical dossiers are recorded for
[`ContinuumRefinementCampaignResultDocument`](../periodic1d/campaign/refinement/continuum/result_documents/ContinuumRefinementCampaignResultDocument/index.md),
[`FiniteRankOracleCampaignResultDocument`](../periodic1d/campaign/oracle/finite_rank/result_documents/FiniteRankOracleCampaignResultDocument/index.md),
and
[`RouteReconciliationCampaignResultDocument`](../periodic1d/campaign/reconciliation/route/result_documents/RouteReconciliationCampaignResultDocument/index.md).
Exact bytes and matching SHA-256 establish content identity only. They do not establish
schema meaning, decoded correctness, authorship, execution provenance, continuum or
finite-size convergence, state-space alignment, route compatibility, oracle
qualification, scientific validation, uncertainty quantification, or acceptance. No
retained artifact or calculator output changed, and no calculator was invoked.

The current row-057 gate passed 45 focused and affected tests, Ruff, formatting, strict
mypy over the six source/facade files and six dedicated evidence modules, Sphinx with
warnings as errors, all 36 entries in the three retained checksum catalogs, six
ownership records containing 12 unique evidence IDs, local architecture links, and
`git diff --check`. These checks establish software behavior and retained content
identity only; they do not establish scientific correctness or validation.

### Cross-cutting synchronization

- [x] Remove former payload-only class definitions, imports, exports, aliases, and
  forwarding modules.
- [x] Update every consuming campaign, request, serializer, correlator, verifier,
  Workflow, test, and Sphinx page.
- [x] Verify exact field-byte equality and SHA-256 identity for every renamed owner.
- [x] Confirm calculation payloads, reports, and provenance are unchanged and each
  `SHA256SUMS` catalog validates after any in-development adapter update.
- [x] Run the phase completion gate and record any unavailable check.

## Source slices

### 3.1 Pure encoded-document containers

Rename every `...CampaignModel` whose owned scientific state consists only of exact
payload bytes to `...EncodedDocuments`.

- Move 1D records out of `model/retained/` into campaign-owned document modules under
  the existing `ksdft2effmass.campaigns.periodic_1d` namespace.
- Move 2D records out of `model/retained/` into document modules below
  `ksdft2effmass.periodic2d.campaign`.
- Update concrete campaigns, requests, serializers, verifiers, exports, tests, and
  Sphinx pages to consume the renamed record.
- Remove the old class definitions and imports without compatibility aliases or
  forwarding modules.

The 1D namespace does not migrate to `ksdft2effmass.periodic1d` in this slice; that is
phase 5.

### 3.2 Compound Wannier90 bundle

Split `Periodic1DWannier90IntegrationModel` into encoded-document ownership and its
existing typed native-artifact groups. The encoded owner stores the same composite
input and result bytes and result-kind identity. Native artifact records retain their
existing path, digest, role, and grouping semantics.

### 3.3 Encoded result-document terminology

Rename archival uses:

- `Periodic1DRetainedResultDocument` to `Periodic1DEncodedResultDocument`;
- `Periodic1DRetainedResultKind` to `Periodic1DEncodedResultKind`; and
- `Periodic1DRetainedResultJsonSerializer` to
  `Periodic1DEncodedResultJsonSerializer`.

Names such as `Periodic1DRetainedLocalizationResult` remain unchanged because they
describe selected-space scientific content rather than archival persistence. The
historical stress document owner became `Periodic1DReductionChallengeEncodedDocuments`
in this slice; row 060 subsequently moved it with the complete canonical campaign
family.
`Periodic2DIsolatedBandResultDocument` and defect result-document records already state
document ownership and require only relocation or import correction where applicable.

### 3.4 Path-bearing defect source bundles

Split each defect-campaign `...CampaignModel` that combines input/result bytes with
`repository_root`:

- the new `...EncodedDocuments` DataObject owns exact bytes only; and
- an existing or dedicated campaign request owns repository location and filesystem
  access.

This split must not move filesystem behavior into the encoded DataObject or create a
generic repository manager.

## Preservation contract

For every renamed, relocated, or split record:

- payload fields remain exact `bytes` and are never decoded and re-encoded merely for
  migration;
- payload byte sequences and SHA-256 identities remain unchanged;
- experiment identifiers, result kinds, provenance strings, and repository-relative
  paths remain unchanged;
- calculation input, result, report, and figure payloads remain unchanged;
- in-development verifier adapters may migrate with the public API, and their
  `SHA256SUMS` entries are updated in the same change so the complete catalog validates;
- serializers reconstruct the same typed semantic content;
- wrong runtime types remain rejected rather than coerced;
- no class gains `PeriodicModel` inheritance because of its former location; and
- no old name remains through alias, re-export, forwarding module, or deprecated route.

## Excluded work

Phase 3 does not:

- implement a retention construction, retained space, or retained operator;
- migrate scientific parent, defect, or effective models;
- change calculation, correlation, verification, or acceptance policy;
- rerun a retained calculation or native external program;
- alter a numerical value, tolerance, schema version, or wire format; or
- remove `Periodic2DCampaign`.

## Completion gate

Phase 3 is complete only when:

1. rows 037--057 have implemented terminal dispositions;
2. source, public exports, tests, Sphinx pages, and architecture prose use encoded
   document terminology consistently;
3. a source scan finds no former payload-only `...CampaignModel` definition or import;
4. fixture tests establish exact field-byte and digest preservation through renamed
   owners;
5. retained verifier CLIs and affected campaign software and numerical tests pass
   without modifying retained payloads; and
6. formatting, Ruff, source and targeted-test mypy, Sphinx warnings-as-errors,
   documentation links, and `git diff --check` pass or an unavailable gate is reported.
