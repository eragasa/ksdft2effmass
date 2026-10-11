# SCF candidate, accepted-parent, staging, and NSCF lineage contract

**Status:** consumer design response; unimplemented and unexecuted. This document
is aligned to Generic Workflow owner contract
`projectkoios.workflow.cpn-bindings@0.1.0`, exact SHA-256
`e6428a8b0d8a47d4f9a6596300fe5ccc65bb16c12e1cc8ffe64884720bd513c2`
at owner commit `9ec0944dad3af1706edf01101e443e244da22ef5`, and to
the selected simulations provider design. The provider document binds this
consumer profile in one direction; a separate retained cross-repository review
record binds the final owner, consumer, and provider hashes without reciprocal
content-digest references.

The provider proposal is suitable as a design input, while immutable artifact-set
and path-free success evidence plus canonical parser/exporter implementation and
golden bytes remain implementation blockers. Exact candidate bounds,
child-export correlation, terminal companion delivery, bounded cancellation,
and the version-bound expression-translation route are closed at design level.
This response adds the exact Si-VC-owned accepted-parent and staging documents.
It does not implement an owner or provider contract, accept a provider
capability, authorize a dependency change, or authorize execution.

## Decision summary

1. The unchanged simulations child retains its twelve-place/eight-transition
   topology and existing `terminal_outcome` token.
2. A successful terminal delivery for the Si-VC route requires an ordered pair:
   the terminal-port payload reference and one separately retained QE saved-state
   candidate reference.
3. The companion candidate is runtime evidence, not a second CPN terminal token.
   It must be declared by the child export and parent binding, retained after the
   terminal outcome, and bound into the delivery identity.
4. `ksdft2effmass` accepts neither a mutable directory nor a provider success
   token as an NSCF parent. Its `accept_production_scf_child` occurrence creates a
   distinct Si-VC accepted-parent reference.
5. NSCF staging consumes that accepted-parent reference, copies every and only
   manifest-listed regular file into a fresh attempt-scoped artifact set, and
   produces a receipt before NSCF dispatch authority can be admitted.
6. Post-NSCF lineage references the accepted SCF parent and staging receipt as
   well as the new NSCF provider candidate and semantic qualification.
7. The unchanged SCF child declares no universal in-net cancellation route.
   Linking must preserve that limitation and withhold quiescence for unresolved
   cancellation or ambiguity.

## Selected owner terminal-companion contract

The selected successor owner contract defines a closed, classification-specific
terminal-delivery requirement containing:

- one exact primary terminal-port identity and payload-reference contract;
- zero or more terminal-classification-specific companion-evidence requirements;
- for each requirement, exact role, schema, owner codec, minimum/maximum
  cardinality, production phase, and correlation-predicate descriptor identities;
- one canonical ordered mapper-input sequence;
- exact bounds on the companion-reference set;
- a delivery identity that binds the child export and plan, terminal history
  head, primary payload, every companion reference, child run/instance, intended
  parent occurrence, requirement, correlation, and mapper identities; and
- replay rules requiring each companion to be retained and fully verified before
  the delivery can permit parent firing.

For the SCF success classification, the companion set has cardinality exactly one
and role `qe-pw-scf-saved-state-candidate-reference`. Known-failure delivery has
an explicit empty companion tuple and zero total. The mapper receives references
already resolved and owner-validated by the outer runtime; it does not fetch
artifacts or invoke a codec inside CPN enablement or firing.

The companion requirement contributes to the child export, child plan, and
parent plan identities. The eventual evidence reference does not, because it is
created after the plans and terminal outcome. This derivation remains acyclic:

```text
child export + parent binding
  -> terminal-specific companion requirement
  -> child terminal outcome
  -> provider candidate retention
  -> terminal delivery(primary + companion)
  -> parent external-output mapping
  -> one parent firing
```

Exact owner, provider, and consumer document hashes are recorded in a separate
retained review record. They are not embedded reciprocally in these
content-derived design documents.

## Provider candidate adopted as input contract

The provider owns the proposed schema:

```text
schema: projectkoios.integrations.quantumespresso.
        qe-pw-scf-saved-state-candidate:1
codec:  projectkoios.integrations.quantumespresso.
        qe-pw-scf-saved-state-candidate-json:1
media:  application/vnd.projectkoios.
        qe-pw-scf-saved-state-candidate.v1+json
```

Its canonical document binds the exact successful calculator request,
occurrence, plan, effect intent, attempt, dispatch authorization, execution
evidence, child export/plan/run/net instance, evaluation/task, rendered input,
structure, executable, ordered pseudopotentials, normalized completion and
convergence evidence, terminal occurrence/outcome/history head, saved-state
manifest, immutable artifact set, counts, sizes, and source-verification
evidence.

The candidate is produced only after the unchanged child terminal outcome is
retained. It asserts provider candidacy, not Si-VC acceptance. The provider codec
must follow pure canonical encoding → authorized outer retention → pure six-field
reference assembly. The candidate, manifest, artifact set, execution evidence,
terminal outcome, and Workflow reference retain distinct identities.

The selected provider design fixes the version-one validation profile at a
262144-byte document cap, nesting depth 6, 512-byte ASCII identity bounds, exact
literal and safe-name grammars, 1–256 ordered pseudopotentials, 1–4096 manifest
artifacts, and a 64-GiB manifest-total cap, with lower/upper/out-of-bound vectors.
Those values are provider-owned and must be preserved byte-for-value by a future
codec. The provider still must define and test the immutable path-free artifact-set
contract and Workflow-correlated path-free success projection. A working-directory
string cannot satisfy either role.

## `SiVcAcceptedScfParent`

### Identities

| Concept | Exact value |
|---|---|
| Schema | `ksdft2effmass.si-vc.accepted-scf-parent:1` |
| Codec | `ksdft2effmass.si-vc.accepted-scf-parent-json:1` |
| Media type | `application/vnd.ksdft2effmass.si-vc.accepted-scf-parent.v1+json` |
| Payload identity prefix | `ksdft2effmass.si-vc.accepted-scf-parent:1:` |
| CPN payload role | `si-vc-accepted-scf-parent-reference` |

The payload identity is the prefix plus lowercase SHA-256 of the canonical payload
bytes. It is not embedded in the payload.

### Closed document

The canonical document contains exactly these top-level fields:

```text
schema_identity
schema_version
accepted_parent_kind
producer
campaign
workflow
candidate
assessment
acceptance
```

`schema_identity` is the exact schema above, `schema_version` is signed integer
`1`, and `accepted_parent_kind` is literal `production-scf-parent`.

#### `producer`

| Field | Meaning |
|---|---|
| `package_identity` | Exact `ksdft2effmass` package/source identity |
| `assembler_identity` | Exact pure accepted-parent assembler identity |
| `assembler_version` | Immutable implementation/version descriptor |
| `source_revision` | Exact source revision containing campaign policy |

#### `campaign`

| Field | Meaning |
|---|---|
| `campaign_identity` | Exact Si-VC campaign instance |
| `campaign_request_reference_identity` | Exact campaign request payload reference |
| `campaign_coordinate_reference_identity` | Exact production SCF coordinate reference |
| `scientific_role` | Literal `production-scf-parent` |

The coordinate remains a typed reference so this schema does not freeze H1–H3
values by implication.

#### `workflow`

| Field | Meaning |
|---|---|
| `parent_execution_plan_identity` | Exact Si-VC execution plan |
| `parent_run_identity` | Exact parent Workflow run |
| `parent_net_instance_identity` | Exact parent net instance |
| `acceptance_request_identity` | Exact prior request for acceptance |
| `acceptance_transition_occurrence_identity` | Exact reserved occurrence producing this payload |
| `acceptance_transition_identity` | Literal `accept_production_scf_child` |
| `predecessor_marking_identity` | Exact enabling parent marking |
| `selected_binding_identity` | Exact selected input binding/reservation evidence |

The occurrence exists before payload assembly. The payload must not identify the
future firing result, successor marking, accepted-parent reference, or retention
evidence.

#### `candidate`

| Field | Meaning |
|---|---|
| `candidate_reference_identity` | Exact six-field provider-candidate reference |
| `candidate_payload_identity` | Exact provider candidate payload identity |
| `candidate_schema_identity` | Exact provider candidate schema identity |
| `child_export_identity` | Decoded and verified immutable child export identity |
| `child_execution_plan_identity` | Decoded and verified child plan identity |
| `child_run_identity` | Decoded and verified child run |
| `child_net_instance_identity` | Decoded and verified child instance |
| `terminal_outcome_reference_identity` | Exact successful child terminal payload reference |
| `terminal_history_head_identity` | Exact accepted child history head |
| `manifest_reference_identity` | Exact provider saved-state manifest reference |
| `source_artifact_set_identity` | Exact immutable manifest-declared source set |

These copied correlations must equal the decoded provider candidate and retained
terminal delivery exactly. They are not caller assertions.

#### `assessment`

| Field | Meaning |
|---|---|
| `scf_observations_reference_identity` | Exact Si-VC-normalized SCF observations |
| `convergence_assessment_reference_identity` | Exact campaign convergence assessment |
| `convergence_policy_identity` | Exact frozen policy applied to this coordinate |
| `completion_accepted` | Exact Boolean `true` |
| `convergence_accepted` | Exact Boolean `true` |
| `assessment_evidence_reference_identities` | Nonempty unique lexical tuple of supporting references |

Provider `completed`/`converged` evidence and campaign acceptance remain separate.
The campaign fields can be true only after the applicable guarded assessment
transitions have committed.

#### `acceptance`

| Field | Meaning |
|---|---|
| `acceptance_policy_identity` | Exact Si-VC production-parent policy |
| `disposition` | Literal `accepted` |
| `accepted_candidate_delivery_identity` | Exact primary-plus-companion child delivery |
| `accepted_convergence_transition_occurrence_identity` | Exact prior `accept_scf_convergence` occurrence |
| `acceptance_evidence_reference_identities` | Nonempty unique lexical tuple of campaign evidence references |

### Bounds and invariants

- Canonical encoding uses the owner control-JSON profile: UTF-8, no BOM or
  trailing newline, exact keys, sorted object keys, compact separators,
  `ensure_ascii=false`, `allow_nan=false`, and no binary64 values.
- The payload is at most 65536 bytes. Every identity is nonempty ASCII without
  controls and at most 512 bytes. Implementation/version descriptors are at most
  256 bytes.
- Each evidence tuple contains 1–32 nonempty unique identities in lexical order.
- No field may contain a filesystem path, command, credential, payload body,
  native file bytes, mutable handle, or live provider/domain object.
- All workflow, child, candidate, manifest, assessment, and delivery correlations
  must form one retained acyclic chain.
- The candidate must be the success companion delivered for the exact child
  occurrence selected by this parent route.
- `accept_scf_convergence` and `accept_production_scf_child` must belong to the
  same campaign coordinate and accepted candidate chain.
- Candidate success alone cannot construct this value. Failed, cancelled,
  ambiguous, mismatched, nonquiescent, or unassessed child evidence is rejected.
- Pure encoding and reference assembly perform no artifact or runtime effect.

## `SiVcSavedStateStagingReceipt`

### Identities

| Concept | Exact value |
|---|---|
| Schema | `ksdft2effmass.si-vc.saved-state-staging-receipt:1` |
| Codec | `ksdft2effmass.si-vc.saved-state-staging-receipt-json:1` |
| Media type | `application/vnd.ksdft2effmass.si-vc.saved-state-staging-receipt.v1+json` |
| Payload identity prefix | `ksdft2effmass.si-vc.saved-state-staging-receipt:1:` |
| CPN payload role | `si-vc-saved-state-staging-receipt-reference` |

### Closed document

The exact top-level fields are:

```text
schema_identity
schema_version
receipt_kind
producer
requirement
source
nscf_dependency
staging
transfer
verification
disposition
```

`schema_version` is `1`, `receipt_kind` is literal
`scf-to-nscf-saved-state-copy`, and `disposition` is literal `succeeded`.

| Record | Exact fields |
|---|---|
| `producer` | `worker_identity`, `implementation_identity`, `implementation_version` |
| `requirement` | `staging_receipt_requirement_identity`, `receipt_schema_identity`, `receipt_codec_identity` |
| `source` | `accepted_parent_reference_identity`, `candidate_reference_identity`, `manifest_reference_identity`, `source_artifact_set_identity` |
| `nscf_dependency` | `nscf_occurrence_identity`, `nscf_request_identity`, `nscf_plan_identity`, `nscf_attempt_identity`, `dependent_execution_effect_intent_identity` |
| `staging` | `staging_effect_intent_identity`, `staging_attempt_identity`, `staging_authority_identity` |
| `transfer` | `destination_artifact_set_identity`, `artifact_count`, `total_byte_size` |
| `verification` | `source_verification_evidence_identity`, `destination_verification_evidence_identity`, `manifest_equivalence_evidence_identity` |

The receipt payload must not identify its own future six-field reference, the
post-hoc staging execution-evidence event, or the future dependent-dispatch
authority/evidence. After retention, the staging execution-evidence event identifies
the resulting receipt reference. Source and destination verification identities
are pre-receipt inputs, so the ordering remains acyclic.

The receipt uses the same canonical JSON and identity/text bounds as the accepted
parent. `artifact_count` is a positive signed 64-bit integer; `total_byte_size` is
positive, equals the manifest total exactly, and does not exceed the requirement's
bound.

A successful receipt requires every and only manifest-declared regular file in a
fresh nonoverlapping destination set, exact relative-path preservation, and source
and destination size/digest verification. Links, traversal, special files,
undeclared files, collisions, count/size violations, or indeterminate writes
produce no success receipt. No private path appears in the payload or canonical
Workflow events.

The execution plan and dependent NSCF effect intent contain only the prior
`WorkflowArtifactStagingReceiptRequirement` identity. The actual receipt must be
durably retained and verified before the NSCF dispatch authorization is admitted.

## Derived NSCF lineage

Si-VC owns a later qualification wrapper, not the native provider NSCF result:

```text
schema: ksdft2effmass.si-vc.qualified-nscf-saved-state-lineage:1
codec:  ksdft2effmass.si-vc.qualified-nscf-saved-state-lineage-json:1
media:  application/vnd.ksdft2effmass.si-vc.
        qualified-nscf-saved-state-lineage.v1+json
role:   si-vc-qualified-nscf-saved-state-lineage-reference
```

Its exact top-level fields are:

```text
schema_identity
schema_version
lineage_kind
producer
campaign
workflow
scf_source
staging_receipt
nscf_candidate
qualification
```

`lineage_kind` is literal `qualified-uniform-nscf-saved-state`. The records bind:

- `producer`: exact package, assembler, version, and source revision;
- `campaign`: campaign, request, coordinate, and scientific role identities;
- `workflow`: NSCF request, occurrence, plan, effect intent, attempt, dispatch
  authority, successful execution evidence, and qualification-transition
  occurrence identities;
- `scf_source`: exact accepted-parent and provider-candidate references;
- `staging_receipt`: exact receipt reference, receipt requirement, source and
  destination artifact-set identities;
- `nscf_candidate`: exact future provider-owned NSCF candidate, post-NSCF
  manifest, and post-NSCF artifact-set references; and
- `qualification`: exact NSCF semantic-observation, requested-uniform-grid,
  qualification-policy, and evidence-reference identities, plus literal
  disposition `accepted`.

The provider-owned NSCF candidate schema is not yet defined, so this wrapper
cannot be implemented. It must not reinterpret native QE directories directly.
It is produced only after `qualify_nscf_semantics` accepts the exact provider
candidate for the requested uniform grid, bands, spin treatment, structure, and
source frame. A zero return, copied SCF tree, or post-NSCF manifest alone cannot
produce it.

The wrapper uses the same canonical profile and bounds as the accepted parent.
Its identity is the schema prefix plus SHA-256 of its canonical bytes and remains
distinct from every provider payload and Workflow reference identity.

## Bounded cancellation declaration for the unchanged child

The canonical SCF child export must truthfully declare:

```text
in_net_cancellation_capability = none
provider_confirmed_terminal_cancellation_classification = absent
reconciliation_capability = workflow-owned-bounded
```

`task_failed` is an existing event route only from the waiting or analysis
markings; it is not a universal cancellation transition. Generic Workflow may
establish containment through `CONFIRMED_NOT_APPLIED` when no effect occurred, or
through `CONFIRMED_APPLIED` followed by processing through existing child events
and proving no active process remains. Requested-only cancellation, timeout,
missing acknowledgement, worker loss, or lease expiry is unresolved.

A parent deployment whose policy requires universal in-net cancellation or a
provider-confirmed cancellation terminal token must fail linking against this
export. Si-VC quiescence remains withheld for every active or unresolved child,
attempt, process, cancellation, companion-handoff assembly, delivery, ambiguity,
invalid evidence, or partial application.

## Required conformance additions

In addition to every applicable owner and provider conformance vector, the
consumer fixture set must prove:

1. success delivery requires exactly one primary terminal reference and one
   candidate companion reference in canonical order;
2. missing, duplicate, wrong-role, wrong-schema, stale, or cross-child companion
   evidence produces no parent firing;
3. known child failure does not require or fabricate a success candidate;
4. candidate retention failure preserves the child terminal outcome but leaves
   the parent occurrence reserved and routes to reconciliation;
5. every copied accepted-parent correlation equals the decoded candidate and
   terminal delivery, including the exact immutable child export; a wrong or
   changed export fails closed;
6. provider completion/convergence does not bypass Si-VC convergence assessment;
7. changed policy, campaign coordinate, candidate, assessment, occurrence, or
   evidence changes the accepted-parent payload identity;
8. exact accepted-parent bytes pass pure codec, outer retention, reference
   assembly, structural reference, full admission, and replay verification;
9. staging source is the accepted parent, not the raw candidate or a path;
10. staging copies every and only manifest entries into a fresh artifact set and
    retains the receipt before NSCF authority;
11. any source/destination/manifest/count/size/identity mismatch produces no
    successful receipt and no dependent dispatch;
12. the receipt identity graph is acyclic under the selected staging-evidence
    representation;
13. NSCF qualification binds the accepted SCF parent and exact staging receipt;
14. no qualified NSCF lineage is emitted for a wrong grid, band count, spin mode,
    structure, source frame, unconverged output, or unaccepted semantic evidence;
15. unchanged-child cancellation capability is represented exactly and cannot
    satisfy stronger parent policy; and
16. complete replay resolves payloads outside the kernel and reconstructs the
    companion, acceptance, staging, NSCF qualification, and quiescence barriers
    without an external effect.

## Readiness and stop conditions

Nested implementation remains blocked until all of the following exist:

- canonical bounded control-record/value/operation/export profiles, golden bytes,
  and deterministic 12/8 parity evidence under the provider's exact candidate
  bounds;
- an immutable path-free artifact-set contract and Workflow-correlated success
  projection;
- implemented and independently verified owner/consumer codecs and payload
  admission;
- a provider-owned NSCF candidate contract before derived NSCF lineage;
- cross-repository fixtures for all applicable vectors; and
- separate authorization for implementation, dependency changes, migration, or
  protected execution.

Stop rather than guess if any identity chain is unavailable, a mutable path would
enter canonical state, post-terminal evidence would create an identity cycle, the
child topology would change or be copied, cancellation capability would be
overstated, or provider evidence would be promoted to campaign acceptance.

## Consumer review disposition

### Finding 1

**Disposition: NO_ACTION_REQUIRED**
**Problem:** The pre-amendment owner target lacked an explicit
terminal-classification companion-evidence contract.
**Evidence:** The selected owner successor now defines closed primary and companion
requirements, canonical mapper order, correlation, durable delivery, replay,
ambiguity, and quiescence without changing child topology.
**Consequence:** None at design level; implementation must still pass the exact
companion conformance vectors.
**Next action:** Preserve the selected contract in implementation and fixtures.

### Finding 2

**Disposition: MUST_FIX**
**Problem:** No immutable path-free artifact-set identity contract or complete
Workflow-correlated success projection currently exists.
**Evidence:** The present manifest authenticates files, while existing native
execution evidence includes a working-directory string and the child emits no
saved-state candidate.
**Consequence:** The accepted parent could fail to prove that the staged bytes are
the exact outputs of the authorized successful attempt.
**Next action:** Add and independently verify the artifact-set and path-free success
projection boundaries before candidate admission.

### Finding 3

**Disposition: MUST_FIX**
**Problem:** Canonical control-record/value/operation/export profiles and golden
bytes do not yet exist.
**Evidence:** The selected design deliberately leaves the canonical flat-definition,
execution-profile, plan, export, and fixture digests unavailable until an
authorized implementation parses the exact version-bound SNAKES expression
surface through a closed AST grammar and exports the source net.
**Consequence:** The child cannot yet be linked or replayed as an exact canonical
Workflow plan.
**Next action:** After separate authorization, implement the closed parser/exporter
and pass deterministic 12/8 golden parity before payload binding or nesting.

### Finding 4

**Disposition: NO_ACTION_REQUIRED**
**Problem:** The unchanged child cannot support a general in-net cancellation
claim.
**Evidence:** The selected provider design declares zero cancellation ports, zero
cancelled terminal classifications, no in-net cancellation, exact
`CONFIRMED_NOT_APPLIED` containment, and required processing of applied results
through existing event ports.
**Consequence:** None at design level if incompatible deployment policy fails
linking.
**Next action:** Preserve the exact bounded declaration in future export fixtures.

### Finding 5

**Disposition: NO_ACTION_REQUIRED**
**Problem:** The superseded provider proposal lacked exact candidate bounds.
**Evidence:** The selected provider design fixes document/depth, lexical,
identity, safe-name, integer, pseudopotential, manifest-count, total-size, and path
bounds plus boundary vectors.
**Consequence:** None at design level if a future codec preserves them exactly.
**Next action:** Preserve the corrected validation profile in schema and fixtures.

### Finding 6

**Disposition: NO_ACTION_REQUIRED**
**Problem:** Saved-state delivery might be assumed to require a replacement or
copied child CPN.
**Evidence:** The candidate is post-terminal companion evidence, and the proposed
exporter traverses the authoritative factory without adding topology.
**Consequence:** None if the stated boundary and migration order are preserved.
**Next action:** None.

**ReviewOutcome: CHANGES_REQUIRED**
The selected provider proposal is a usable design input, but Findings 2 and 3
block a claim of nested-route implementation readiness.

**OperatorRequest: NONE**
No human choice is needed to apply these deterministic design corrections. Any
future implementation, dependency change, migration, or protected execution still
requires its own applicable authorization.
