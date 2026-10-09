# `ksdft2effmass.periodic1d.campaign.oracle.finite_rank`

## Purpose and status

This implemented canonical package owns the named periodic-1D finite-rank-oracle
campaign. Row 064 moved the implementation to
`ksdft2effmass.periodic1d.campaign.oracle.finite_rank` without a compatibility alias,
wire change, or dependency on the former underscored campaign route.

The campaign compares a finite-rank Bloch-resolvent construction with an independently
assembled finite site-space eigensolve for one frozen synthetic parent. The package
name does not make encoded bytes, repository paths, represented operators, numerical
observations, qualification records, or scientific conclusions interchangeable.

## Public facade

The reviewed current facade exports exactly:

- `FiniteRankOracleCampaign`;
- `FiniteRankOracleCampaignResultDocument`; and
- `FiniteRankOracleEncodedDocuments`.

Lower-level input, workflow, correlation, verification, and numerical operation types
remain in defining modules and are not flattened into the facade.

## Child map

| Child | Responsibility | Canonical page |
|---|---|---|
| `campaign` | Calculation, retained correlation, and independent-verification facade | [Campaign](campaign/index.md) |
| `contracts` | Immutable parent, rank-one, tolerance, provenance, and result records | [Contracts](contracts/index.md) |
| `input_decoding` | Closed version-one input adaptation | [Input decoding](input_decoding/index.md) |
| `parent_data` | Authenticated parent loading and maintained model adaptation | [Parent data](parent_data/index.md) |
| `numerical_actions` | Site-space construction and finite-rank resolvent route | [Numerical Actions](numerical_actions/index.md) |
| `comparison` | Oracle-versus-dense comparison records | [Comparison](comparison/index.md) |
| `workflow` | Campaign result assembly and fail-closed encoding | [Workflow](workflow/index.md) |
| `independent_reconstruction` | Separate verifier-side finite numerical implementation | [Independent reconstruction](independent_reconstruction/index.md) |
| `verification` | Authentication, structural comparison, and verification result | [Verification](verification/index.md) |
| `encoded_documents` | Exact input and retained-result bytes, excluding repository location | [Encoded documents](encoded_documents/index.md) |
| `result_documents` | Exact encoded result wire and derived content identity | [Result documents](result_documents/index.md) |

## Repository-location boundary

Encoded documents own bytes only. Calculation and retained correlation receive an
explicit absolute `repository_root` argument at their executing facade methods.
Independent verification owns exact documents and an absolute root in
`FiniteRankOracleVerificationRequest`. Request construction checks type and lexical
absoluteness without resolving or accessing the filesystem.

No generic campaign request is invented merely to make these distinct APIs look
symmetric. The location owner is the actual operation that authenticates
repository-relative sources.

## Implementation ownership

The canonical implementation is partitioned by cohesive owner rather than collected
in a monolithic Workflow module:

| Module | Owner |
|---|---|
| `contracts.py` | Immutable campaign, parent, root, and provenance records |
| `input_decoding.py` | Version-one input-schema adaptation over `CampaignJsonDecoder` |
| `parent_data.py` | Authenticated source loading plus explicit finite-hopping toy-model adaptation over `Periodic1DCampaignJsonDecoder` |
| `numerical_actions.py` | Existing finite-hopping fiber/supercell construction plus campaign-owned Hermitian projection and finite-rank resolvent oracle |
| `comparison.py` | Rank-one and special-control oracle-versus-dense observations |
| `workflow.py` | Campaign metadata, summary assembly, and fail-closed result encoding |
| `independent_reconstruction.py` | Independent oracle and dense numerical reconstruction |
| `verification.py` | Retained-source authentication, structural comparison, and verification result |

`serialization.json.StrictJsonDecoder` is the single owner of strict UTF-8 object
decoding, duplicate-key rejection, nonfinite-constant rejection, closed JSON values,
and exact primitive adaptation. `Periodic1DCampaignJsonDecoder` supplies the canonical
periodic-1D specialization and owns the nonempty
rectangular complex-pair matrix wire and returns an immutable `complex128` array without
assigning basis, unit, state space, operator, provenance, or scientific meaning.
Finite-rank classes own only their schema, source authentication, scientific records,
and campaign-specific adaptation; they do not reproduce JSON parser callbacks or the
complex-matrix wire parser. The independent reconstructor shares this wire adapter but
not production numerical algorithms, so numerical reconstruction remains independent.
The existing `Periodic1DEncodedResultJsonSerializer` emits a different
compact wire contract and therefore cannot replace the retained pretty-printed oracle
wire without changing exact bytes. The Workflow's schema-specific emission consequently
uses fail-closed `allow_nan=False` and remains covered by exact retained correlation.

`FiniteRankResolventOracle` is the one concrete, bounded analytical strategy. It owns
the Bloch fiber, local resolvent, bound-vector, and scalar-root algorithms directly and
is instantiated internally by the Workflow. There is no abstract strategy interface,
forwarding adapter, caller injection, registry, or plugin point. It is not a generic
oracle engine, qualification record, or acceptance mechanism. The
`FiniteRankSiteSpaceOperatorConstructor` remains a separate dense comparison route, and
the retained verifier preserves its independent numerical reconstruction.

The retained input does not declare a scientific hopping-model identity or a parent
Hermiticity tolerance, and its `composite_group_id` remains a group identity rather than
being reinterpreted as a model identity. `FiniteRankOracleParentModelAdapter` therefore
supplies explicit maintained adapter metadata: model identity
`periodic1d.finite-rank-oracle-parent.v1` and the retained route's unchanged
`1.0e-11` Hermiticity tolerance. These values identify and constrain the maintained
adaptation; they are not source-provided identities, execution provenance, scientific
validation, or acceptance thresholds. The energy unit comes from the authenticated
input contract.

Production fiber and supercell assembly now reuse
`Periodic1DPrimitiveFiberHamiltonianConstructor` and
`Periodic1DSupercellHamiltonianConstructor`. The finite-rank numerical owners retain
the pre-existing output Hermiticity check and symmetric projection, preserving the
retained wire exactly. The verifier continues to reconstruct both routes independently
and imports neither production constructor.

The reviewed facade, input deserializer, parent-data loader, numerical Workflow, and
independent verifier own behavior through instantiated campaign or ActionObjects. None
of these defining modules uses static or class-method namespace utilities. Private
schema validation, finite-operator, resolvent, digest, and comparison kernels remain
attached to their cohesive instance owner; their formulas and call order are unchanged.
Structural evidence scans every defining module, while retained correlation and
independent reconstruction provide numerical regression evidence.

## Scientific and evidence boundary

The authoritative finite experiment remains under
`calculations/research-monograph/impurity-defect-1d-analytical-oracle/`. Its protocol
keeps the represented parent, finite rank, Bloch-resolvent route, site-space route,
root tolerance, projector comparison, degeneracy controls, and finite-size sequence
explicit.

"Oracle" here identifies a bounded analytical comparison route. It does not denote a
generic production oracle, an oracle-qualification engine, a theorem, an
infinite-volume or continuum limit, material validation, transferability, uncertainty
quantification, or acceptance.

## Row-064 dossier

- **Supported imports:** the leaf facade exports only `FiniteRankOracleCampaign`,
  `FiniteRankOracleCampaignResultDocument`, and `FiniteRankOracleEncodedDocuments`;
  the `oracle` parent facade exports the same reviewed set. Lower-level numerical and
  verification owners remain in their defining modules.
- **Sphinx mapping:** `doc/sphinx/api/ksdft2effmass/periodic1d/campaign/finite-rank-oracle.rst`
  documents every defining module and the bounded meaning of “oracle.”
- **Provenance:** exact retained inputs, protocol, checksums, and reports remain under
  `calculations/research-monograph/impurity-defect-1d-analytical-oracle/`; migration
  changes no retained bytes and performs no calculator execution.
- **Tests-as-evidence:** canonical facade, former-route removal, import independence,
  exact encoded-document identities, and result-document identity are bound by
  `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/oracle/finite_rank/`.
  Its mirrored `resources/` manifest records ownership.
- **Claim boundary:** the resolvent route is qualified only for this finite synthetic
  evidence class and validity domain. Agreement does not establish an infinite-volume
  theorem, continuum convergence, material validity, transferability, UQ, or
  acceptance.

Rows 043 and 057 retain the encoded-pair and result-document evidence inherited by
this family. Row 064 additionally establishes canonical ownership, removal of the
former route, and independence from transitional periodic campaign imports. The
retained experiment is consumed read-only; this dossier does not rerun it or qualify
its oracle for another evidence class.

Original local work under the repository license.
