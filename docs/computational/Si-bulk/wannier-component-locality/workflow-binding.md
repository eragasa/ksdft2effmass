# Runtime-neutral CPN and hierarchical binding profile

**Status:** selected consumer architecture profile aligned to proposed Generic
Workflow contract `projectkoios.workflow.cpn-bindings@0.1.0`, exact owner
SHA-256 `e6428a8b0d8a47d4f9a6596300fe5ccc65bb16c12e1cc8ffe64884720bd513c2`
at owner commit `9ec0944dad3af1706edf01101e443e244da22ef5`. The
operator selected this successor as the current conformance target and directed
that Si-VC requirements lead the integration; Workflow is not a separate
scientific-acceptance or veto authority. Exact owner, consumer, provider, and
review-record identities are retained outside these content-derived documents so
that reciprocal future digests cannot form a hash cycle. Reviews of superseded owner or consumer bytes remain historical and do not transfer
to this profile. The generic binding selection remains current, but the later
cutoff/k-point→structure→final-confirmation decision supersedes the 56/55 Si-VC
consumer topology previously bound through this profile. A replacement topology and
renewed exact-byte review are required. The contract remains unimplemented. This selection does not create an importable
API, authorize a dependency change, implement a runtime, freeze H1--H3, or
authorize calculator execution.

## Purpose

Si-VC requires one runtime-neutral canonical colored Petri net (CPN) whose
scientific topology remains owned by `ksdft2effmass`, while Generic Workflow
owns runtime identity, persistence, authority, attempts, cancellation,
reconciliation, and replay. Reusable child workflows remain owned by their
domain providers.

This profile closes two architecture questions:

1. a domain JSON document is retained as an immutable content-addressed
   artifact and represented in a CPN marking by a typed reference token, rather
   than embedded as an unvalidated JSON string; and
2. the authoritative simulations-owned SCF workflow is invoked through a
   reviewed hierarchical child binding, rather than copying its places,
   transitions, guards, or expressions into the Si-VC net.

The Generic Workflow repository must own and implement the generic form of this
contract in conformance with the selected Si-VC requirements before Si-VC may
import it. Names below identify required roles and prospective protocol records;
they are not currently available Python imports.

## Ownership and dependency direction

```text
ksdft2effmass Si-VC definition
  |  scientific token schemas, policy, parent topology, child requirements
  v
Generic Workflow CPN/binding API
  |  canonical definition, marking, occurrence, hierarchy, runtime evidence
  v
projectkoios-simulations child/provider exports
     SCF child definition/facade, QE staging, execution, native evidence
```

The Generic Workflow kernel and service must not import `ksdft2effmass` or
`projectkoios-simulations`. Domain owners depend on the conforming Workflow API
and register bounded descriptors, codecs, and child exports through deployment
linking. Live provider objects and machine paths do not enter canonical CPN
state.

## Canonical CPN boundary

The owner contract distinguishes three identity layers:

- an owner-local nominal `CpnDefinitionIdentity` for the flat graph;
- a content-derived `WorkflowExecutionPlanIdentity` for the executable semantic
  closure; and
- a separate `WorkflowExecutionBindingsIdentity` for provider, worker,
  environment, resolver, and deployment linking.

The execution plan must bind:

- one canonical flat-definition representation identity and SHA-256 covering
  every semantic color, place, transition, arc, guard, inscription, and priority;
- one exact CPN execution-profile identity covering the value model, canonical
  definition/marking/binding/result representations, validation, expression
  evaluation, complete enablement enumeration, ordering, binding selection,
  external-output validation, and pure firing;
- one complete initial-marking contract;
- every payload schema, owner codec, payload-color binding, hierarchical child
  export/binding, route, mapper, and bounded-policy descriptor required to
  interpret the net; and
- compiler identity and semantic contract version.

Changing any semantic graph byte, CPN execution-profile component,
payload-color binding, child interface, mapper, route, or bounded policy must
change the plan identity. Deployment-only changes must not. A marking identity
must bind the flat definition, every place, token color/value, individual token
identity where required, multiplicity, and referenced payload-reference
identities. The run binds the exact execution plan and initial marking. None of
these identities may depend on a filesystem path, process identifier, wall
clock, or mutable registry lookup.

### Closed control records and expressions

Preserving an existing domain-owned flat topology sometimes requires a token to
carry a small immutable control record whose fields are inspected by a guard or
used to construct another control record. Replacing one such record with
additional scalar places or transitions would change the authoritative topology
and is not an equivalent export.

The exact CPN execution profile must therefore bind the owner contract's bounded
control-record value and expression language. Every admitted record-type
definition has a closed field set, field kinds, collection and nesting bounds,
and canonical representation identity. Field projection starts from a
record-producing expression and names one declared field path; record
construction names one exact record-type identity and supplies every required
field expression in canonical field order. Neither operation may invoke a Python
callable, import path, owner object, registry, payload codec, artifact resolver,
provider, filesystem, network, clock, or scientific-policy callback.

The value model, record-type definitions, owner mapping descriptors, field
projector, constructor expressions, expression grammar, evaluator, validators,
canonical representations, and
mutation behavior all contribute to the CPN execution-profile and execution-plan
identities. Large or scientific values remain payload references; bounded guard
facts may enter a control record only after outer admission and correlation.
The current scalar-only shadow kernel does not implement this selected future
profile.

## Domain JSON payload binding

### Selected representation

A CPN does not pass a file descriptor or mutable Python mapping. It passes a
token whose color declares the domain role and whose value identifies an
immutable JSON artifact.

The prospective generic reference record, called
`DomainPayloadReference` in this profile, must contain exactly the bounded
metadata needed to resolve and verify the document:

| Field | Meaning |
|---|---|
| `payload_identity` | Stable nominal identity in the owning domain |
| `schema_identity` | Exact schema family and major version |
| `media_type` | Registered JSON media type |
| `sha256` | SHA-256 of the exact canonical bytes |
| `byte_size` | Positive exact byte count |
| `artifact_identity` | Opaque immutable artifact-store identity |

It must not contain artifact bytes, arbitrary mappings, credentials, source
excerpts, or machine-specific paths. SHA-256 establishes byte identity only; it
does not establish chronology, producer authenticity, semantic validity,
scientific acceptance, or execution authority.

The generic CPN token carries the exact content-derived identity of the complete
six-field reference document as its admitted scalar value. Its color and the
execution plan identify the required schema, owner, codec, maximum payload
bytes, per-complete-marking reference-token count, and individual-token-identity
policy. The full reference is retained by the Workflow runtime and artifact
boundary, not reconstructed from an untrusted token string.

### Codec contract

For each admitted domain payload type, the owner must supply pure codec and
reference-assembly operations separated from artifact persistence:

```text
encode_canonical(typed_value)
  -> canonical_bytes + DomainPayloadEncodingMetadata
authorized_artifact_retention(canonical_bytes)
  -> artifact_identity
assemble_reference(canonical_bytes, encoding_metadata, artifact_identity)
  -> DomainPayloadReference
decode_canonical(canonical_bytes, reference)
  -> typed_value | closed_failure
```

The codec neither contains an artifact store nor fabricates or resolves an
artifact identity. The authorized outer artifact operation supplies that
identity; the pure assembler computes `sha256` and `byte_size` from the exact
bytes and constructs only the six fields above.

The canonical byte form selected by this profile matches Generic Workflow's
existing private runtime-event convention: one UTF-8 JSON object, no byte-order
mark or trailing newline, `ensure_ascii=false`, `allow_nan=false`, keys sorted
lexically, and compact `,` and `:` separators. Decoding must construct the typed
value and then require byte-for-byte equality with a fresh canonical encoding.
Workflow-bound control and provenance documents use only `null`, exact Booleans,
strings, signed 64-bit integers, arrays, and objects; scientific binary64 arrays
remain owner artifacts with their own exact schemas rather than acquiring an
implicit cross-language JSON-number convention here.

The codec must:

- consume and produce immutable owner-defined typed values, never `Any`, a raw
  mapping, or `object` as an unspecified software boundary;
- reject duplicate JSON keys, unknown keys, missing keys, unsupported versions,
  and invalid UTF-8;
- reject noncanonical bytes even when they decode to an equivalent JSON value;
- reject nonfinite numbers, Boolean-as-number substitutions, numeric strings,
  and integers or reals outside the schema's declared representation;
- impose explicit nesting, collection, and string bounds;
- validate all cross-field identities and domain invariants; and
- perform no filesystem, network, calculator, clock, random, authority, or
  persistence effect.

A structural reference decoder separately rejects malformed six-field
references and reference-identity mismatches without artifact access. Before a
reference token may enter an initial or successor marking, the runtime adapter
must resolve the exact color binding and codec, enforce the schema, media type,
maximum bytes, per-complete-marking reference-token count, and required
non-null unique token identities, resolve the immutable artifact, verify actual
byte count and SHA-256, and invoke canonical decoding plus owner validation.
Replay repeats those checks independently before pure CPN replay. Generic
Workflow does not interpret scientific fields or silently convert a JSON object
into generic scalar values.

### Guard rule

A guard must not fetch or parse an artifact payload. If a transition requires a
bounded fact such as an accepted/rejected status, that fact must already be an
explicit typed scalar/status value or a declared field of an admitted bounded
control record produced by a prior outer admission or acceptance transition.
The fact-bearing token must remain correlated with the payload reference from
which it was derived.

This rule prevents a mutable artifact store or hidden domain callback from
changing transition enablement without changing the marking.

## Hierarchical child-workflow binding

### Child export

A reusable child owner must publish an immutable child export containing:

- owner and workflow-family identities;
- the exact compiled child execution-plan identity and digest;
- the nominal flat child definition identity, canonical flat-definition
  representation identity and digest, and child CPN execution-profile identity;
- initial-marking constructor descriptor identity;
- constructor/export identity and supported contract version;
- typed input and terminal-output port identities;
- admitted payload-schema and codec identities at each port;
- the exact admitted terminal classifications already declared by the child;
  for the selected SCF child these are success and known failure, with no
  definition-declared cancelled classification;
- separate cancellation and reconciliation capability declarations; the
  selected SCF declaration has no cancellation input port, no in-net
  cancellation, `CONFIRMED_NOT_APPLIED` operational containment, and mandatory
  processing of `CONFIRMED_APPLIED` through existing event ports; and
- the child's authority and effect-capability declaration.

Unresolved ambiguity is nonterminal and is never an admitted child terminal
classification. It cannot map the parent transition or satisfy quiescence.

Post-hoc export verification remains a separate
`WorkflowChildExportEvidenceBinding` so evidence cannot create a cycle in the
export or execution-plan identity.

For Si-VC, the child export must reference

`projectkoios.simulations.workflows.pw_dft_scf.cpn.net::build_dft_pw_scf_net`

and its authoritative twelve-place/eight-transition behavior. The parent must
not reproduce those places, transitions, arcs, guards, or token expressions.
A detached inventory may expose names and counts for conformance inspection but
is not executable topology.

### Parent binding

The prospective `WorkflowHierarchicalChildBinding` record must bind:

- the nominal parent flat-definition and exact parent transition identities
  (`execute_scf_child`);
- the child export and child execution-plan identities;
- one parent input place and child input port mapping;
- for every admitted child terminal classification, its exact primary terminal
  port, terminal-delivery requirement, companion requirements, and parent
  outcome mapping;
- exact input, output, correlation, and canonical mapper-ordering descriptor
  identities;
- the child's exact cancellation capability and compatible reconciliation
  routes;
- child-instance cardinality exactly one and sole signed-integer ordinal `0` for
  contract v0.1; and
- the binding contract version.

The binding contributes to the parent execution-plan identity but must not
contain that enclosing identity. Deployment linking may select a provider or
worker implementing the exact export, but may not change child plan or port
semantics. Fan-out greater than one is unsupported and requires a later
contract defining set retention, per-ordinal launch, aggregation, cancellation,
and terminal-set semantics.

### Fresh child instance

Selecting and durably reserving the parent substitution occurrence initiates a
child launch; it is not yet the logical parent CPN firing. Generic Workflow must
retain the unique child-creation intent before contacting a provider and derive
a fresh child net-instance identity from at least:

- parent run and net-instance identities;
- parent execution-plan and hierarchical-binding identities;
- parent transition-occurrence identity;
- exact selected parent input-token evidence; and
- the sole contract-v0.1 child ordinal `0`.

The parent transition remains reserved and logically unfired until an exact
accepted child terminal delivery has been mapped and the one atomic parent
firing can commit its successor marking.

The campaign must not manufacture an occurrence identity such as
`si-vc-occurrence-<digest>`. A repeated loop activation receives a new parent
occurrence and child instance. A retry of an unchanged launch receives a new
attempt under the same occurrence and must not create another child instance
when launch status is ambiguous.

### Port mapping

The Si-VC input mapping is:

```text
parent scf_child_required token
  -> SiVcScfChildRequirement JSON reference
  -> exact child request/input-port token
```

The terminal mapping is:

```text
child terminal outcome + SCF saved-state handoff reference
  -> correlated SiVcScfChildOutcome JSON reference
  -> parent scf_child_outcome token
```

The output mapping must verify that the child run, child instance, child
terminal outcome, and saved-state handoff all identify the expected parent
occurrence. A terminal observation from another child, occurrence, attempt,
definition, or parent marking is rejected or routed to reconciliation; it is
never accepted by lexical similarity alone.

## Runtime identity mapping

The Generic Workflow owner must provide distinct nominal identities for:

| Identity | Required derivation or correlation |
|---|---|
| Run | Exact execution plan, initial marking, and run subject |
| Net instance | Run plus root or parent-child instance relationship |
| Request | Run, expected prior state/revision, operation intent, ordered input references, actor/authority references, bounds, idempotency identity, expected output contract, and optional client nonce; no occurrence identity |
| Transition occurrence | Exact prior request, net instance, flat-definition identity, enabling marking revision, transition, ordered binding, exact token occurrences, and reservation identity |
| Plan | Occurrence, adapter descriptor, ordered effect intents, bounds, and runtime contract |
| Effect intent | Occurrence, operation kind, exact input references, expected evidence, ordinal, and any staging-receipt requirement identity |
| Attempt | Occurrence plus bounded attempt ordinal |
| Authority admission | Exact occurrence, attempt, plan, effect intent, authority decision, scope, and validity observation |
| Execution evidence | Exact attempt, authority admission, worker/provider identity, request, and observed result |
| Reconciliation | Exact ambiguous attempt, original idempotency/start identity, retained evidence, and query result |
| Child instance | Parent occurrence, hierarchical binding, exact child plan, selected input evidence, and sole ordinal `0` |
| Delivery | Exact child export/plan/run/instance, terminal classification/outcome/history head, primary reference, canonical companion sequence, requirement/correlation/mapper descriptors, and reserved parent occurrence; never the future parent firing |

Content-derived identities must be acyclic. Logical identities remain distinct
from artifact digests and execution-evidence identities. A digest mismatch is an
integrity failure, not proof that an effect did or did not occur.

## SCF-to-NSCF provenance handoff

### Hard requirement

The exact saved-state outputs of the accepted SCF child must be the verified
inputs staged for the correlated NSCF attempt. Copying is the selected
stage-isolation mechanism; provenance is the governing requirement.

The SCF provider may emit a candidate saved-state handoff only after:

1. calculator execution has a retained successful terminal record;
2. the saved-state tree has been inventoried into a strict manifest; and
3. every manifest-listed regular file has been verified against that manifest.

The campaign may make that candidate eligible as an NSCF parent only after:

4. required SCF completion and convergence observations have been normalized;
   and
5. campaign policy has accepted the SCF result for the declared scientific
   role and coordinate.

This preserves provider evidence versus campaign acceptance. A zero return, a
`JOB DONE` marker, or a directory path alone is insufficient.

### SCF saved-state handoff and accepted-parent documents

The exact provider-response and Si-VC-owned schema design is specified in
[SCF saved-state lineage](scf-saved-state-lineage.md). The selected successor
owner contract now supplies the required classification-specific primary
terminal payload plus separately retained companion-evidence contract. Exact
owner, provider, and consumer document hashes are bound by a separate retained
cross-repository review record rather than by reciprocal future-digest references
inside these documents.

The provider-owned candidate handoff JSON document must bind at least:

- handoff schema identity and version;
- exact SCF child export and execution-plan identities;
- SCF Workflow run, net instance, transition occurrence, request, and attempt;
- authority-admission and successful execution-evidence identities;
- SCF child definition and terminal-outcome identities;
- saved-state manifest artifact identity, SHA-256, and byte size;
- prefix and calculation kind `scf`;
- exact calculator, rendered-input, structure, and pseudopotential identities;
  and
- the immutable saved-state artifact-set identity.

A separate Si-VC-owned accepted-parent JSON document must bind the unchanged
candidate handoff plus the scientific role, campaign coordinate, normalized
completion/convergence evidence, acceptance-policy identity, and exact
acceptance transition occurrence. NSCF staging consumes this accepted-parent
reference, not an unaccepted candidate handoff.

A private source-root path is a provider-local locator and must not appear in
canonical Workflow history or the CPN token. It is resolved only inside an
authorized isolated worker from the immutable artifact-set identity.

### Staging receipt

The parent execution plan and dependent NSCF effect intent bind only a
`WorkflowArtifactStagingReceiptRequirement` stating the required parent,
manifest, source artifact set, destination-role descriptor, verifier profile,
and relation to the dependent effect ordinal. The future receipt identity must
not appear in either record.

Before NSCF calculator dispatch, the separately authorized staging worker must:

1. resolve the exact accepted SCF parent, candidate handoff, and manifest;
2. verify the source manifest and every selected regular file;
3. create a fresh attempt-scoped NSCF workspace that does not overlap the SCF
   output tree;
4. copy every manifest-listed file while preserving its source-root-relative
   path;
5. reject symbolic links, path traversal, special files, undeclared
   substitutions, count/size-limit violations, and pre-existing destination
   collisions; and
6. verify the destination files against the same SCF manifest.

It then emits a canonical `SavedStateStagingReceipt` JSON artifact binding:

- the receipt-requirement, accepted SCF parent, candidate handoff, and manifest
  references;
- the dependent NSCF occurrence, request, plan, and attempt;
- the staging effect intent, staging attempt, and staging-authority identities;
- the attempt-scoped destination artifact-set identity;
- copied artifact count and total bytes;
- source- and destination-verification evidence identities;
- staging worker and implementation identities; and
- a closed terminal staging disposition.

The receipt is created only after successful staging and first enters staging
execution evidence. It must be durably retained before dependent NSCF dispatch
authorization is admitted. The dependent NSCF effect intent references only the
prior requirement; the later NSCF dispatch authority and execution evidence
must reference the exact actual receipt. A staging exception or indeterminate
write cannot be represented as a successful receipt.

### NSCF derived handoff

After successful NSCF execution, the NSCF saved-state handoff must bind both:

- the new post-NSCF manifest and semantic qualification evidence; and
- the accepted SCF parent, candidate handoff, and staging receipt.

The post-NSCF manifest inventories the resulting finite saved-state bytes. The
parent reference records derivation. Neither record alone proves that the
requested NSCF k-point, band, spin, completion, or source-frame semantics are
correct; the separate NSCF semantic qualification gate remains mandatory before
Wannier preprocessing.

## Persistence and replay

Workflow event history retains compact identities and payload references, not
JSON bodies or native calculation files. The artifact store retains the exact
canonical JSON and manifest-listed native artifacts.

Complete replay is a future outer verifier and must not redefine the existing
bounded Slice A replay subject. It must:

1. invoke and accept unchanged Slice A identity-chain replay over the exact
   schema segment Slice A owns;
2. invoke each separately accepted later-slice segment verifier and validate
   continuous predecessor/ordinal bridges;
3. resolve each required payload reference by immutable artifact identity;
4. verify color binding, schema, media type, count/token-identity policy, byte
   size, SHA-256, exact codec, canonical decoding, and owner invariants;
5. reconstruct the retained reservation, child-creation intent, child instance,
   plan, attempt, authority, ambiguity/reconciliation, cancellation,
   receipt-barrier, terminal-delivery, one-parent-firing, and quiescence state;
6. replay pure CPN enablement, ordering, selection, output validation, and firing
   under the exact retained execution profile without calling providers; and
7. compare reconstructed parent/child markings and terminal outcomes with every
   retained identity.

Missing payloads, unsupported codecs, changed child exports, definition-closure
mismatches, or corrupt receipts fail closed. A projection or current pointer
must not repair authoritative history.

## Cancellation, late delivery, and quiescence

A parent finalization request prevents new child admission. Every admitted child
must then reach one of:

- an accepted definition-declared terminal success or known failure;
- when a different child explicitly declares it, provider-confirmed cancellation
  followed by that definition's declared cancelled terminal outcome; or
- a terminal reconciliation result proving `CONFIRMED_NOT_APPLIED` with no later
  attempt admitted, or proving `CONFIRMED_APPLIED` with its execution evidence
  processed through existing event ports to a definition-declared terminal
  outcome and with required containment completed.

The selected SCF child has no cancellation input port, no cancelled terminal
classification, and no in-net cancellation. `CONFIRMED_NOT_APPLIED` contains the
operation without fabricating a terminal token or firing the reserved parent
scientific transition. `CONFIRMED_APPLIED` is processed through the child's
existing event ports.

Cancellation is a separately authorized operation when it has external effects.
A lease expiry, missing acknowledgement, worker loss, or timeout is not proof of
cancellation or non-execution.

Late or duplicate child deliveries remain retainable. Delivery identity and
parent-occurrence correlation make acceptance idempotent. They cannot recreate
`campaign_active`, select another terminal outcome, or enable post-terminal
scientific work. Workflow may emit the campaign quiescence observation only
when every admitted child, claim, attempt, process, cancellation, and ambiguity
has one of the qualifying terminal outcomes above. `STILL_AMBIGUOUS`,
`EVIDENCE_INVALID`, `CONFIRMED_PARTIAL`, requested-only cancellation, active
leases or claims, and active or lost-but-unreconciled processes never satisfy
quiescence. Quiescence is not scientific success or campaign acceptance.

## Required conformance evidence

Before Si-VC implementation may depend on this profile, cross-repository tests
must establish at least:

1. every semantic flat-definition and CPN execution-profile mutation changes the
   execution-plan identity, including every bounded control-record schema,
   field-projection, record-construction, parser/grammar, evaluator, validator,
   and expression-representation mutation;
2. pure canonical encoding, authorized outer artifact retention, pure six-field
   reference assembly, structural decoding, and full payload verification remain
   distinct operations;
3. admission and replay reject wrong schema/media/owner/codec, digest or size
   mismatch, per-complete-marking reference-count overflow, and missing or
   duplicate required token identity;
4. generic markings contain compact payload-reference identities and no raw JSON
   objects, native payloads, credentials, or machine paths;
5. the Si-VC parent references the authoritative SCF child export and contains
   no copied child place, transition, arc, guard, or expression definitions;
6. the referenced SCF child canonical export has the expected twelve places and
   eight transitions at the frozen provider revision;
7. v0.1 rejects child cardinality other than one or child ordinal other than
   signed integer `0`;
8. child export, child plan, child instance, occurrence, request, attempt,
   authority, outcome, terminal history head, companion, and delivery
   correlations reject every stale or wrong-identity substitution;
9. an SCF failure, timeout, ambiguous effect, rejected convergence record, or
   incomplete manifest cannot emit an accepted SCF saved-state handoff;
10. staging copies every and only manifest-listed regular file into a fresh
    nonoverlapping NSCF workspace and verifies identical bytes before dispatch;
11. the plan and dependent NSCF effect intent contain only the receipt
    requirement, while the actual receipt is durably retained before dependent
    dispatch authority can be consumed;
12. tampering with one source file, destination file, manifest, handoff,
    receipt, plan, execution profile, canonical definition, child export, or
    event identity fails closed;
13. outer replay first accepts the unchanged Slice A and later segment verifiers,
    then reconstructs the full runtime safety state and exact parent/child
    markings without provider or calculator calls;
14. ambiguous child launch or calculator execution enters reconciliation and
    never causes automatic duplicate dispatch;
15. cancellation and late/duplicate delivery reach quiescence without a second
    campaign terminal token;
16. unresolved, invalid-evidence, partial-application, requested-only
    cancellation, and active-process states cannot satisfy quiescence; and
17. successful software conformance is reported separately from scientific
    convergence, material validation, uncertainty quantification, and human
    acceptance.

## Current evidence and remaining gap

The selected owner proposal
`projectkoios.workflow.cpn-bindings@0.1.0`, exact SHA-256
`e6428a8b0d8a47d4f9a6596300fe5ccc65bb16c12e1cc8ffe64884720bd513c2`,
now maps this consumer profile into owner vocabulary and closes the bounded
control-record, field-projection, record-construction, and terminal-companion
design contracts. Its focused owner-side review reported no blocking design
finding. Neither that review nor the operator's governance selection implements
the contract or authorizes migration or execution.

The selected simulations provider design specifies a closed candidate schema and
deterministic exporter around the unchanged 12-place/eight-transition child. It
closes exact candidate bounds, exact child-export correlation, truthful bounded
cancellation, and a version-bound closed-AST route for translating the frozen
SNAKES expression surface at design level. The provider document intentionally
binds this exact consumer profile in one direction; this document does not embed
the provider's future digest. A separate retained cross-repository review record
binds the resulting owner, consumer, and provider bytes without a content-hash
cycle.

Nested implementation still requires a path-free immutable artifact-set/success
projection plus separately authorized canonical parser/exporter implementation,
golden bytes, and conformance fixtures. The Si-VC consumer disposition and exact
accepted-parent/staging design are recorded in
[SCF saved-state lineage](scf-saved-state-lineage.md).

The existing simulations NSCF runner already verifies a parent SCF saved-state
manifest, copies each manifest-listed file into a fresh local NSCF `outdir`, and
verifies the copied destination before launching a stub or authorized
calculator. Its focused saved-state and NSCF tests pass with stub executables.
This is positive software evidence for the byte-copy mechanism.

It does not close this profile. The authoritative SCF child currently reports a
calculator-output artifact and normalized observation but does not emit the
Workflow-correlated saved-state handoff defined above. The NSCF runner accepts
independently configured parent paths and manifest metadata rather than a
hierarchically correlated child outcome. Generic Workflow also lacks an
implemented canonical-plan, payload-binding, child-binding, complete-replay,
effect, authority, cancellation, quiescence, and reconciliation API required
here.

Therefore Si-VC implementation and protected execution remain blocked pending
separately authorized conforming implementation and cross-repository conformance
evidence.
