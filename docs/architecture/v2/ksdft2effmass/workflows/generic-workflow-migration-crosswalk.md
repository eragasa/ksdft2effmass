# Generic Workflow migration crosswalk and golden-parity plan

**Status:** design-only compatibility plan. No bridge, translator, Generic Workflow
runtime segment, payload codec, child route, migration, or retirement described here
is implemented or authorized. The conformance target is the proposed
`projectkoios.workflow.cpn-bindings@0.1.0` contract at SHA-256
`e6428a8b0d8a47d4f9a6596300fe5ccc65bb16c12e1cc8ffe64884720bd513c2`
(owner source commit `9ec0944dad3af1706edf01101e443e244da22ef5`, merged as
`3861f22db3b182743bd1e7ba6fe5721d7895948b`). That exact design
contract is a semantic target, not an importable API or a compatibility promise.

## Purpose

`ksdft2effmass` already owns substantial colored-Petri-net, Workflow aggregate,
control-plane, persistence, and replay behavior. The Si-VC integration must not
replace that behavior with an unrelated greenfield executor. It must transfer
generic execution responsibility to Generic Workflow through explicit bridges,
golden semantic witnesses, translation, and dual verification while preserving
`ksdft2effmass` ownership of its domain definitions.

This document fixes the migration units, equivalence claims, incompatibilities,
fixture families, gates, and retirement order. It does not select final Generic
Workflow Python module names; the owner contract explicitly defers that API.

The current-source inventory was inspected at `ksdft2effmass` revision
`2f30d7a37eab8306c7c17da0e2b316d63da8c74c`. The authoritative behavior is the
source plus its tests, not this inventory alone.

## Non-negotiable boundaries

- Domain repositories continue to author flat CPN definitions, owner codecs,
  payload bindings, child exports/bindings, initial-marking constructors, and
  runtime requests.
- Generic Workflow validates, compiles, links, persists, and executes immutable
  plans without importing `ksdft2effmass` or copying domain topology.
- Each executable net instance remains one flat CPN. Runtime nesting correlates a
  separately compiled child plan; it does not embed the child graph in the parent.
- Pure CPN validation, enablement, ordering, selection, and firing perform no
  artifact, codec, provider, worker, clock, filesystem, network, or calculator
  operation.
- Current `ksdft2effmass` runtime/control/persistence code is compatibility
  evidence and a temporary bridge. It is not the permanent generic executor.
- Passing parity proves bounded software behavior only. It does not establish
  scientific validity, calculator convergence, campaign acceptance, or execution
  authority.
- No calculator or external effect is part of golden-parity generation.

## Equivalence model

Migration uses four deliberately separate kinds of comparison.

| Comparison | Required meaning | Explicit non-claim |
|---|---|---|
| Structural parity | The normalized flat graph contains the same colors, places, transitions, arcs, variables, expressions, priorities, and selection policy. | Equal nominal definition strings alone are insufficient. |
| Behavioral parity | For the same admitted immutable input marking, current and target kernels produce the same validation classification, ordered enabled bindings, selection, consumed/read/inhibited/produced token witness, and successor marking. | Python class equality, `repr`, or incidental tuple layout is not required. |
| Runtime-state parity | Translation preserves the exact run, request, occurrence or legacy activation, attempt, authority, obligation, outcome, ambiguity, child, dependency, and transition correlations that exist. | Missing target safety state must not be inferred from a successful current result. |
| Persistence/replay parity | The old reader still reconstructs the old revision exactly, the target reader reconstructs the translated history, and independent replay reaches equivalent normalized state. | Target bytes and target content identities need not equal legacy bytes or identities. |

Identity equality is asserted only when both sides deliberately use the same
specified derivation. Otherwise a retained translation relation binds the exact
legacy identity, target identity, translator identity, source revision, target
contract identity, and semantic-witness identity. A translator must never relabel a
legacy digest as though it were a target digest.

A target execution must not invoke the current implementation as a runtime oracle.
The current implementation is used to create reviewed, immutable golden fixtures;
target behavior is then evaluated independently against those fixtures.

## Current-to-target crosswalk

### CPN kernel and executable semantic closure

| Current owner/surface | Behavior that must be preserved | Generic Workflow target role | Bridge and parity disposition |
|---|---|---|---|
| `petrinet.colored.definitions` | Immutable colors, places, transitions, arcs, transition priority, and definition-level selection policy. | Canonical flat-definition representation inside an execution plan. | Export every semantic field to canonical owner-defined data. Mutating any field must change the canonical-definition digest and plan identity even when the nominal definition identity is unchanged. |
| `petrinet.colored.values` and `markings` | Closed scalar values, typed tokens, optional individual token identities, multiplicity, place markings, complete markings, and ordered binding assignments. | Exact value-model, bounded control-record, marking-representation, binding-representation, and token-identity profiles. | Compare normalized typed values and token occurrences, not Python object serialization. Payload-reference and bounded control-record values are explicit target extensions with their own profiles and fixtures, not silent expansions of current scalar semantics. |
| `ColoredPetriNetDefinitionValidator` and `ColoredPetriNetMarkingValidator` | Closed structural issue classification and fail-closed validation. | Definition- and marking-validator components of `WorkflowCpnExecutionProfile`. | Golden fixtures cover every current issue code and combinations where ordering matters. New payload-admission failures remain an outer target layer and are not mislabeled as current kernel behavior. |
| `ColoredPetriNetExpressionEvaluator` | Pure value-expression, guard, input-pattern, inhibitor, and output-template evaluation. | Exact evaluator identity in the execution profile, including the closed target `FIELD_PROJECTION` and `CONTROL_RECORD_CONSTRUCTOR` variants. | Legacy parity fixtures retain current scalar behavior. Separate explicit target fixtures cover bounded control records, projections, and constructors. Any attempt to resolve a payload or call a domain callback inside the kernel is a conformance failure. |
| `ColoredPetriNetTransitionEnabler` | Complete enabled-binding enumeration, validation failures, evaluator identity, ordering identity, and enabler identity. | Complete enablement enumeration plus ordering profile. | Compare the full ordered binding tuple and closed failure witness; comparing only the selected transition is insufficient. |
| `ColoredPetriNetBindingSelector` | Canonical selection and exact definition-permitted directed selection. | Binding selector and directive representation profile. | Preserve `selected`/`not_enabled`/`failure` behavior and directive correlation. Workflow permission remains independent of definition permission. |
| `ColoredPetriNetTransitionFirer` | Identity-closed firing input, revalidation, exact consume/read/inhibitor audit, produced tokens, and immutable successor. | External-output validation and pure firing components of the execution profile. | Compare normalized audit and successor marking. External output must be independently validated; a supplied result must not bypass selection correlation. |
| Nominal `ColoredPetriNetDefinitionIdentity` | Current owner-local graph name. | Target `CpnDefinitionIdentity`, still owner-local and nominal only. | Preserve an explicit nominal-identity mapping and never treat either name as complete semantic closure. The compiler additionally retains canonical graph bytes/digest and all execution-profile identities. |

The current kernel therefore becomes a source profile for the first bridge. It is
not copied into Generic Workflow as an unversioned implementation default. A
change to its value model, representation, validator, evaluator, enabler, ordering,
selector, external-output validation, or firer must create a new execution-profile
identity and execution-plan identity.

### Existing flat workflow definitions

| Current surface | Preserved definition behavior | Migration rule |
|---|---|---|
| `workflows/_dft_scf_bands.py` | Pure two-step SCF then fixed-density-bands logical replay, including fail-closed input/result/native-state correlations and exact CPN firing order. | Compile the existing definition and initial-marking construction into a plan. Do not redraw the topology or promote this private replay slice into a calculator executor. |
| `workflows/_dft_scf_nscf_dos.py` | Three independent Task definitions with SCF→NSCF→DOS result-availability dependencies and exact Task-to-transition bindings. | Compile the existing graph and Workflow composition. Do not reinterpret result availability as scientific acceptance or calculator success. |
| Future Si-VC constructor | Authoritative 56-place/55-transition campaign topology in `campaigns/si_vc/cpn/net.py`. | Add only after the bridge compiler and kernel parity gates pass. The simulations-owned SCF child remains a separately exported 12-place/eight-transition plan. |

The private DFT definitions are migration fixtures, not permanent generic package
examples and not authorization to execute QE.

### Workflow model and CPN adapter

| Current owner/surface | Current meaning | Target mapping | Required treatment |
|---|---|---|---|
| `WorkflowComposition`, `TaskInstance`, `TaskStartGateSet` | Reusable Workflow identity, run-scoped Task instances, and `any_of`/`all_of` gate policy. Empty/no gates require direct invocation. | Domain-authored route and activation descriptors linked into a plan. | Preserve gate ordering and compatibility. Do not turn gates into Task input discovery or scheduling callbacks. |
| `TaskActivation` and direct/`any_of`/`all_of` selections | Exact run, instance, operation, attempt, input, and generic selection-result correlation. | Legacy activation bridge to target request and transition occurrence. | Every target occurrence must bind an exact prior request. The request is retained first; occurrence identity derives from it, never conversely. |
| `WorkflowResultTokenMapping` | One-to-one supplied ResultObject/input/variable/place/identified-token correlation. | Input mapper evidence plus admitted token-reference correlation. | Preserve exact coverage, order, and uniqueness checks. Replace a domain value with a six-field payload-reference identity only through an explicit owner codec and color binding. |
| `ColoredPetriNetWorkflowMapping` | Independent Workflow permission for directed selection plus direct and `all_of` transition mappings. | Plan route/mapping descriptors. | Mapping changes must change plan identity. A deployment binding cannot alter selection semantics. |
| `ColoredPetriNetWorkflowAdapter` | Effect-free enablement, selection, activation construction, result mapping, and firing-input preparation. | Bounded domain bridge around the generic kernel. | Split pure mapping from runtime orchestration. It must not authorize, dispatch, resolve artifacts, or invoke codecs inside guards/firing. |
| `ResultObject` and `TaskInputBinding` | Live immutable domain result objects and already-bound inputs. | Typed content-addressed domain payload references at the canonical boundary. | Live objects remain outside plans and tokens. The bridge uses pure owner encoding, authorized outer retention, pure six-field reference assembly, then full admission verification. |

A current `ResultObjectReference` is not the target six-field
`WorkflowDomainPayloadReference`. It retains a concrete Python `ResultObject`, its
owner/type/content identities, and producer provenance. Translation must preserve
that provenance while externalizing canonical owner bytes and constructing a new
six-field reference containing exactly `payload_identity`, `schema_identity`,
`media_type`, `sha256`, `byte_size`, and `artifact_identity`.

### WorkflowRun aggregate and replay

| Current record family | Preserved facts | Target mapping and gap disposition |
|---|---|---|
| `WorkflowDefinitionReference`, `WorkflowRuntimeBundle` | Exact Workflow, nominal CPN, Task definitions, schema, adapter, evaluator, ordering, enabler, selector, and firer identities. | Translate to the execution plan and exact CPN execution profile. Add canonical definition/marking/binding/result representation and external-output-validator identities; absence in legacy data is explicit, never guessed. |
| `WorkflowRun` initial/current markings and ordered transition records | One immutable aggregate revision with append-only state and canonical transition order. | Retain legacy revision identity and a target run/segment translation relation. Target run binds the exact plan and initial marking. |
| `TaskAttempt`, `TaskInvocationOutcome`, and failures | `started`, then `confirmed`, `rejected`, or `indeterminate`; confirmed alone carries results. | Map exact attempts and evidence. Legacy `indeterminate` maps to unresolved ambiguity, never to target success, terminal containment, or quiescence. |
| `ResultObjectReference`, `ResultProductionRecord`, `NativeOutputAdmission`, `ResultDependency` | Concrete immutable results, producer provenance, production identity, manifest admission, and explicit consumption edges. | Preserve provenance and dependency identities while converting payload bodies to verified references. Provider candidate evidence remains distinct from campaign acceptance. |
| `NestedWorkflowMembership`, `NestedWorkflowInvocationIntent` | Separate child run, parent activation/attempt, child identity, inputs, and creation-idempotency identity. | Translate to parent occurrence reservation, child-creation intent, v0.1 child ordinal `0`, and child-instance identity. Intent must remain durable before provider contact. |
| `NestedWorkflowTerminalObservation` | First observed `confirmed`, `rejected`, or `indeterminate` child outcome with exact export or reconciliation evidence. | Confirmed/rejected may map only through declared child terminal ports after child replay/quiescence checks. Legacy `indeterminate` is retained as ambiguity evidence but is nonterminal under the target contract. |
| `WorkflowRunReplayer` | Effect-free `equal`, `unequal`, `unsupported_version`, or `error` reconstruction using an explicit runtime bundle. | Preserve as the legacy replay leg. Target complete replay first verifies unchanged Generic Workflow Slice A and later segments, then payloads/runtime safety, then pure CPN replay. |

There is a deliberate semantic correction at the nested boundary: the current model
can retain an `INDETERMINATE` first terminal observation, but the target contract
forbids unresolved ambiguity from being an admitted terminal classification or
satisfying quiescence. The translator must preserve the historical observation
without mapping it to an accepted child terminal delivery or parent firing.

Likewise, current replay equality covers the implemented WorkflowRun and pure CPN
history. It does not establish target payload verification, occurrence reservation,
child-create reconciliation, cancellation containment, staging receipt barriers, or
quiescence. These are additional later runtime segments, not facts inferred from a
legacy `equal` result.

### Control plane

| Current surface | Current behavior to preserve | Target segment | Known gap or restriction |
|---|---|---|---|
| `SimulationExecutionAuthorizer` | Closed `authorized`/`denied`/`error` decision for exact preparation or claim inputs and immutable authority snapshot. | Attempt-bound dispatch authorization. | Reusable for legacy dispatch parity only. Target authority also binds exact occurrence, plan, effect intent, worker/provider scope, bounds, and validity observation. |
| `SimulationDispatchPreparer` | Replay predecessor; create request correlation, started attempt, reserved grant, obligation, dependencies, and replay-equal candidate. | Request, occurrence/plan preparation, attempt, authority, and intent retention. | The target request must precede occurrence derivation. Existing activation-derived ordering needs an explicit acyclic bridge. |
| `SimulationDispatchClaimPreparer` | Replay predecessor; authorize and advance exact reservation to claimed state. | Claim/lease segment before worker effect. | A current claim is consumed for current authority purposes but does not prove target child, staging, cancellation, or quiescence safety. |
| `WorkflowRunDispatchEntryCommitter` and `SimulationDispatchAdapter` | Commit dispatch entry before effect; independently authorize at effect boundary; distinguish dispatched, denied, already-entered, error, and indeterminate. | Durable intent/entry plus exact attempt-bound effect dispatch. | `already_entered` and `indeterminate` never justify an automatic duplicate effect. |
| `SimulationDispatchReconciler` | Reduce exact observations to confirmed, rejected, indeterminate, conflict, or error. | Ambiguity reconciliation segment. | Target terminal reconciliation uses stricter dispositions; conflict/error/indeterminate remain unresolved unless a permitted target disposition is established. |
| `SimulationDispatchResultIngressPreparer` | Replay predecessor; atomically admit terminal attempt, invocation/dispatch outcome, dispositions, result/provenance, native-output admission, and transition. | Result/evidence processing and terminal parent commit. | Confirmed provider evidence is not campaign scientific acceptance. |

Current control records have no implemented target-equivalent cancellation state
machine, staging-receipt barrier, child-process containment proof, or full quiescence
verifier. Those capabilities must be added as later Generic Workflow runtime
segments. They are not parity obligations that can be marked satisfied by legacy
fields.

Outcome vocabulary must be translated conservatively:

| Current value | Allowed target interpretation |
|---|---|
| `confirmed` | Confirmed only for the exact record's bounded claim; it does not imply domain acceptance or quiescence. |
| `rejected` | Known negative outcome only when its exact evidence and target route admit that classification. |
| `indeterminate` | Unresolved ambiguity requiring reconciliation; nonterminal for target quiescence. |
| observation `conflict` or `error` | Unresolved operational evidence; no result, retry, parent firing, or success may be fabricated. |
| authorization `authorized` | Permission for the exact bound operation and phase only. It is not inherited by child, staging, cancellation, or later attempts. |
| obligation `completed` | Legacy obligation bookkeeping only; not target scientific success or global quiescence. |
| replay `equal` | Equality for the stated legacy bundle and run revision only. |

### Persistence

| Current surface | Preserved behavior | Target treatment |
|---|---|---|
| `WorkflowRunSerializer` and result-value codecs | Closed encode/decode results, exact schema/content binding, and fail-closed codec behavior. | Keep an immutable legacy reader. Translation resolves each supported owner codec explicitly; no ambient latest codec or silent schema upgrade. |
| `WorkflowRunTransactionValidator` | Validate the exact candidate/predecessor and bind candidate, serialized bytes, content, and revision identities. | Preserve as the legacy validation leg; target event/segment validation is independent. |
| `WorkflowRunAtomicRepository` | Opaque single-stream compare-and-swap, idempotent commit, and claim-load evidence through the shared revision store. | Adapt through a translation boundary and dual verification. Do not let a mutable projection repair either history. |
| Serialized concrete result payloads | Legacy durable payload representation where currently supported. | Retain original bytes unchanged. Target canonical history stores compact six-field references; authorized migration retains canonical payload bytes as immutable artifacts and records exact translation provenance. |

Migration is append-only. Existing run bytes, revision identities, and content
identities are never rewritten to look target-native. A failed or unsupported
translation leaves the legacy record readable and produces no target successor.

## Golden fixture specification

### Fixture envelope

Every golden fixture must be immutable, payload-free unless it explicitly tests a
synthetic payload reference, and contain:

- fixture identity and fixture schema identity;
- exact `ksdft2effmass` source revision and current implementation identities;
- exact owner-contract digest and target implementation revision when available;
- input semantic witness and expected output semantic witness;
- legacy identity values as observations, not presumed target identities;
- expected closed success/failure classification and diagnostic code;
- evidence-class label `synthetic-software-conformance`;
- generator identity and generation command; and
- SHA-256 for every retained fixture file.

No fixture contains credentials, private paths, calculator inputs, native scientific
outputs, or an execution grant. Synthetic reference fixtures use fake opaque
artifact identities and in-memory bytes only.

### Normalized semantic witnesses

The bridge projectors produce canonical data for comparison. At minimum:

1. **Definition witness:** every color and allowed kind; place and allowed color;
   transition, input/external-output variables and guard; arc endpoints and exact
   inscription; transition priority; selection policy.
2. **Marking witness:** definition identity relation; every place; each token color,
   typed value, individual identity, and multiplicity in canonical order.
3. **Enablement witness:** validation result; exact implementation/profile
   identities; complete ordered enabled bindings; closed failure code and phase.
4. **Selection witness:** enablement correlation, selector/ordering identities,
   outcome, selected binding, exact directive or absence, and failure code.
5. **Firing witness:** selected binding and external outputs; consumed/read token
   occurrences; inhibitor counts; produced tokens; outcome/failure; successor
   marking.
6. **Workflow witness:** run/instance/gate/input/activation/operation/attempt
   correlations and adapter outcome.
7. **Runtime witness:** request, occurrence-or-legacy-activation, plan, intent,
   attempt, authority, obligation, child, observation, outcome, reconciliation,
   and transition links, including explicit unsupported target fields.
8. **Persistence witness:** legacy revision/content identities, exact legacy bytes,
   translation relation, target segment identities, and each replay result.

Projectors must be pure, versioned, and separately tested. They may discard only
representation accidents explicitly named in their versioned contract. They must
not normalize away ordering, multiplicity, token identity, attempt identity,
directive presence, ambiguity, or failure classification.

### Initial fixture matrix

| ID | Fixture family | Minimum required cases |
|---|---|---|
| `K-01` | Definition and marking validation | One accepted definition/marking and one fixture for every current issue code; same nominal definition with each semantic field mutated. |
| `K-02` | Enablement and ordering | No binding, one binding, multiple canonical bindings, consume/read/inhibitor combinations, guard false, and evaluator failure. |
| `K-03` | Selection | Canonical selection, permitted exact directive, prohibited directive, stale/mismatched directive, and not-enabled. |
| `K-04` | Firing | Successful consume/read/produce, external output, stale predecessor, selection mismatch, output mismatch, and each firing failure class. |
| `D-01` | SCF→bands replay | Confirmed two-firing route and every declared correlation/firing rejection code. |
| `D-02` | SCF→NSCF→DOS composition | Exact graph inventory, Task-instance/gate policy, Task-transition mapping, and stable compilation under changed run-scoped instance identities. |
| `A-01` | Workflow adapter | Direct, `any_of`, compatible `all_of`, incomplete/incompatible `all_of`, token-correlation mismatch, and independently prohibited direction. |
| `R-01` | WorkflowRun aggregate | Minimal run plus confirmed, rejected, and indeterminate invocation histories with exact attempts/results/failures. |
| `R-02` | Nested history | Intent retained before creation; confirmed/rejected export; indeterminate create or observation retained as unresolved; duplicate terminal delivery rejected. |
| `C-01` | Authority/preparation/claim | Authorized, denied, error, stale/revoked/claimed grant, replay-unequal predecessor, losing compare-and-swap, and retry with fresh identities. |
| `C-02` | Dispatch/reconciliation/ingress | Entered/already-entered, effect confirmed/rejected/indeterminate, conflicting observations, no automatic redispatch, and atomic confirmed ingress. |
| `P-01` | Serialization | Exact legacy round trip, malformed/unknown/unsupported content, codec failure, and preserved old bytes after target translation. |
| `P-02` | Repository | Compare-and-swap conflict, idempotent duplicate commit, claim receipt, validation failure with no commit, and real-SQLite retained revision. |
| `P-03` | Replay | Equal, unequal, unsupported version, error, noncanonical transition order, and broken predecessor/result/control correlations. |

These bridge fixtures supplement rather than replace the 48 conformance vectors in
the owner contract. In particular, later target-only suites must cover payload
reference admission, plan/profile closure, child export and delivery, exact
authority for every protected effect, staging receipts, cancellation, late
delivery, full replay, and quiescence.

## Dual-verification protocol

For every supported legacy revision:

1. Load exact legacy bytes through the pinned legacy reader.
2. Validate and replay the legacy run with its explicit legacy runtime bundle.
3. Require the expected legacy result; anything other than the fixture's closed
   expected result stops translation.
4. Project the legacy definition, marking, and history into a normalized semantic
   witness.
5. Translate through one versioned, pure translator into target plans, references,
   and runtime segments. Artifact retention, when eventually authorized, is an
   explicit outer operation and is not hidden in the translator.
6. Validate the target execution plan and every target segment independently.
7. Run unchanged Generic Workflow Slice A replay first, then every accepted later
   segment verifier with continuous predecessor/ordinal bridges.
8. Perform read-only payload verification and runtime-safety reconstruction.
9. Replay pure CPN behavior with the exact retained execution profile.
10. Project the target result to the corresponding semantic witness and compare it
    with the golden witness.
11. Retain the legacy-to-target translation relation and both replay results. Do not
    alter the legacy stream.

A mismatch, unsupported owner codec, missing payload, absent profile identity,
noncanonical definition, incomplete authority correlation, unresolved ambiguity,
or broken segment bridge produces a closed migration failure. It does not trigger
schema guessing, mutable repair, effect repetition, or partial promotion.

## Migration slices and gates

### Slice 0 — freeze compatibility evidence

- Pin source revisions and implementation identities.
- Add the normalized witness schemas and the `K`, `D`, `A`, `R`, `C`, and `P`
  fixture families.
- Run existing tests unchanged and retain checksums for golden files.

**Gate:** fixtures are reproducible from the pinned source, contain no protected
or scientific payloads, and receive independent review.

### Slice 1 — kernel/compiler bridge

- Implement canonical flat-definition export without moving definitions.
- Bind the full CPN execution profile.
- Compile `_dft_scf_bands` and `_dft_scf_nscf_dos` without topology changes.
- Run structural and behavioral parity.

**Gate:** every semantic mutation changes the required identities; every `K`,
`D-01`, and `D-02` witness matches; owner vectors 42--48 close bounded control
records and expressions; dependency checks prevent Generic Workflow from
importing `ksdft2effmass`.

### Slice 2 — model and adapter bridge

- Translate Task instances, gate policy, exact prior requests, activations, input
  mappings, and result mappings.
- Preserve direct/`any_of`/`all_of` behavior and directive restrictions.

**Gate:** every `A-01` fixture matches and request→occurrence derivation is acyclic.

### Slice 3 — aggregate and persistence translation

- Add append-only identity translation records.
- Preserve immutable legacy readers and exact source bytes.
- Translate run, attempts, results, dependencies, nested intent/observations,
  authority, obligations, outcomes, and transitions.
- Perform dual validation and replay.

**Gate:** every `R` and `P` fixture passes; legacy and target histories remain
independently verifiable; no unsupported field is inferred.

### Slice 4 — payload-reference boundary

- Add pure owner codecs, authorized outer retention, pure reference assembly,
  payload-color bindings, structural reference validation, and full admission.
- Replace raw/string domain payloads only at this boundary.

**Gate:** owner-contract vectors 1–9 and 31 pass independently in owner and
consumer implementations. Guards and pure firing remain unable to read payloads.

### Slice 5 — nested child route

The merged provider design at SHA-256
`adfa47ba9007e3b08b02d219bf5d7b29de28a48531876c79559a510fc5484858`
(provider source commit `b6995de15dd44067c55d9055735d26b11b80e712`, merged
as `8e70e02cc0f723477bcac42b0f163097f628c88a`) is the current design
input. Its consumer disposition and exact lineage schemas are recorded in the
[Si-VC SCF saved-state lineage contract](../../../../computational/Si-bulk/wannier-component-locality/scf-saved-state-lineage.md).

- Consume the simulations-owned deterministic SCF child export and golden topology
  fixture.
- Require the success terminal-port payload plus its separately retained candidate
  companion evidence; do not add a second terminal token or hide lookup in the
  mapper.
- Add cardinality-one/ordinal-`0` child binding, durable creation intent,
  idempotent creation, terminal delivery, and normal parent firing.
- Do not copy the 12-place/eight-transition child topology into the parent.

**Gate:** owner-contract vectors 10--24 and 33--41 pass, including exact
classification-specific companions, ambiguity, cancellation race, late delivery,
and quiescence withholding. Provider candidate output remains separate from
Si-VC acceptance.

### Slice 6 — staging and protected runtime segments

- Add exact occurrence/attempt authority for each protected operation.
- Add the staging-receipt requirement, staging evidence, actual receipt retention,
  and dependent-dispatch barrier.
- Add cancellation, reconciliation, late-delivery, containment, and quiescence
  segments.

**Gate:** owner-contract vectors 20--30 and every applicable companion/replay
vector 33--41 pass; actual staging receipt is absent from
the plan and first appears only after staging evidence; no unresolved state is
classified quiescent.

### Slice 7 — Si-VC parent integration

- Compile the authoritative 56-place/55-transition flat parent.
- Link exact payload bindings and the SCF child export.
- Run all consumer and cross-repository fixtures without calculator execution.

**Gate:** all applicable owner vectors 1--48 plus the consumer and provider
fixtures pass; exact topology, plan closure, initial marking, parent/child
separation, accepted-parent route, NSCF staging lineage, replay, and quiescence
all pass software conformance review.

### Slice 8 — retirement

Duplicate project-owned runtime execution may be retired only after all earlier
gates pass, old retained histories remain readable and reproducible, dual operation
has covered every supported route, rollback has been tested, and the operator gives
separate explicit migration/retirement authorization. Domain definitions and owner
codecs are not retired merely because execution ownership moved.

## Stop conditions

Stop the migration and preserve both existing state and evidence if any of the
following occurs:

- topology, enabled-binding order, selection, token multiplicity/identity, audit,
  successor marking, or failure classification differs without an approved
  semantic change;
- a target identity cannot be derived acyclically from retained inputs;
- an old revision requires guessing a codec, schema, definition, profile,
  authority state, or terminal classification;
- an indeterminate/conflicting legacy record would have to be promoted to a target
  terminal or quiescent state;
- a bridge would put a live adapter, callable, provider, SNAKES object, path,
  credential, mutable registry, or payload body into a plan or CPN token;
- Generic Workflow would need to import a domain repository or copy its topology;
- replay would invoke an external effect or use a current registry default in place
  of a retained version;
- migration would rewrite legacy bytes or identities;
- a protected operation lacks exact separately scoped authority; or
- implementation, dependency, migration, execution, commit, push, merge, or
  release authority has not been separately granted where required.

## Completion claim boundary

Completion of this plan means only that a reviewed compatibility specification and
fixture program exist. Completion of bridge software would establish bounded
software conformance for the tested revisions. Neither statement establishes that
the Si-VC campaign is implemented, that the SCF→NSCF causal handoff is complete,
that a production calculation may run, or that any scientific hypothesis has been
accepted.
