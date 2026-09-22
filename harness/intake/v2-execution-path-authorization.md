# Bounded v2 execution-path implementation authorization

## Human instruction and scope

Repository starting boundary: `f63f7204b6a61dc38f21bf5c2dc30e4360518bbc` on `dev`.

The human instructed:

> let's finish v2 and skip human review and acceptance but augment planning phases and review phase by an antagonistic review

The assistant distinguished the seven execution-path Tasks (Option A) from all
unfinished v2 Tasks (Option B). The human selected:

> A

The first planning pass found that application composition requires the unimplemented
Harness domain repository. The assistant asked:

> May I add that eighth task under the same review rules?

The human answered:

> yes

This expands the selected scope by exactly `migration.v2.harness.persistence`, not
by the rest of the Harness migration. Application composition must explicitly depend
on that owning result rather than silently implementing it or claiming a partial root
as complete.

The combined instruction authorizes planning, implementation planning,
implementation, deterministic corrections, software verification, and independent
antagonistic review for exactly:

1. `migration.v2.persistence.sqlite`
2. `migration.v2.workflows.persistence`
3. `migration.v2.workflows.read-models`
4. `migration.v2.workflows.contract-verification`
5. `migration.v2.campaigns.definitions`
6. `migration.v2.harness.persistence`
7. `migration.v2.application.composition`
8. `migration.v2.application.verification`

Canonical Task records still own each concern and its prerequisite declarations.
This is not authorization to complete every v2 Task, reopen accepted unrelated
Tasks, or run a scientific calculation. It permits minimal producer/consumer,
source, tests, compact test resources, documentation, Task, selection, and generated
projection changes needed for these eight concerns under their accepted contracts.

## Human-selected result-value serialization boundary

Workflow persistence implementation planning identified that the structural
`ResultObject` protocol exposes identity but not the complete outward-domain value
required for lossless aggregate reconstruction. The owning Workflow persistence
architecture had deferred the exact wire contract.

The assistant proposed:

> I recommend an **explicitly injected, typed result-value codec**, supplied by the outward domain through application composition—no registry or dynamic imports; unsupported versions remain incompatible.
>
> **May we adopt this boundary and continue through the planned reviews?**

The human answered:

> yes

This selects that dependency boundary for `migration.v2.workflows.persistence` and
its named consumers. Workflow persistence receives an explicit typed codec for
complete concrete result values; outward domains supply their concrete serialization
behavior through application composition, without an inward Workflow import of
calculator or integration implementations. The selection does not permit identity-only
substitutes, arbitrary-type reflection, dynamic imports, or a generic codec registry.
Unsupported concrete versions remain incompatible, not reconstructed successes.

Exact typed interfaces, supported concrete value/version coverage, wire representation,
identity binding, complete aggregate closure, failure cases, and software-verification
oracles remain subjects of implementation planning and independent antagonistic
review. This choice is not evidence that every arbitrary implementation of the open
protocol is serializable, and it does not resolve unrelated open contracts. Owning
architecture and public documentation must reflect the selected boundary during the
reviewed implementation. The eight-Task scope and all non-waived limits are unchanged.

## Completion and continuation

For these eight Tasks only, routine per-Task human-review and final human-acceptance
pauses are waived. Software verification and antagonistic review are not human
acceptance. Record completed work as `closed_software_verified`, with exact results
and residual limitations, rather than `closed_human_accepted_pass`. The following
named consumer may use an actually completed, software-verified prerequisite result
from this operation; lifecycle text alone is not proof of that result.

Progress only within the eight named Tasks and only after actual prerequisite
results and applicable reviews. This explicit bounded sequence does not enable
ambient or automatic successor activation. Clear selection when the authorized
sequence is finished; leave any blocked Task and its exact blocker explicit.

The human waived acceptance pauses, not verification failures. Do not relabel
unfinished implementation, unavailable evidence, or an unresolved material defect
as completed. Managed Git closeout remains separate: no commit or push is authorized
by this instruction, and no such boundary may be claimed complete.

## Review and write boundaries

Use one writer at a time in this checkout. The parent owns scope, arbitration, and
integration. Sequential delegated writers may own source, tests, accompanying
documentation, and the exact controlling Task state for their assigned slice.
No parent or other child writes concurrently with that writer. Independent
reviewers are fresh-context and read-only for the reviewed scope.

For each Task, challenge both planning and implementation planning before source
implementation, and challenge the implemented result after verification. Plans for
the eight-Task sequence may be prepared and independently challenged together,
provided each Task has an explicit section and its dependencies and decision
boundaries are separately covered. Reassess an affected implementation plan if an
earlier Task changes a consuming assumption.

Reviews must seek concrete counterexamples, missing contract oracles, failure and
recovery gaps, provenance or authority confusion, hidden mutable state, unsupported
public behavior, dependency inversions, and unnecessary architecture. They must
report evidence-backed findings, not manufacture objections. Apply the
`actionable-review` finding dispositions, technical outcomes, and operator requests.
Use bounded correction/re-review passes; stop rather than silently waive a remaining
material finding or build an unbounded review loop.

## Direct continuation after deferred tooling diagnosis

After deferring the separate installed-package recovery/transport work, the human
asked what should follow. The assistant recommended continuing the selected
`migration.v2.workflows.persistence` Task directly, beginning with the retained
entry tests, then completing missing evidence, checks and independent review. The
assistant explicitly requested approval to switch from delegated implementation
to direct parent execution. The human answered:

> recommendation auhtorized

This authorizes the parent as sole implementation writer for that continuation.
Independent review remains required; the tooling deferral does not waive it. No
installed-package patch, transport probe, successor activation, scientific execution,
commit or push follows from this instruction. The existing eight-Task authority and
non-waived boundaries remain unchanged.

## Authority and dispatch evidence increment

The subsequent recommendation was to add independently authored authority timestamp
and dispatch-variant serialization evidence, including exact UTC preservation and
malformed records, within the selected Workflow persistence Task. The human answered:

> recommendation authorized

This bounded increment remains direct parent implementation with the existing
independent whole-Task review gate. It does not reactivate the deferred tooling
investigation or authorize a successor, commit, push or scientific execution.

## Human-selected nested Workflow history correction

The independent whole-Task reviews returned `CHANGES_REQUIRED`. The correctness
review reproduced a pending child invocation that could not acquire a persisted
terminal outcome while preserving both immutable history and one invocation per
child. The assistant presented three public-model corrections and recommended:

> B — Keep immutable child intent separate from terminal observations.

The human answered:

> recommendation authorized

This unambiguously selects **Option B: separate immutable child-invocation intent
and terminal-observation records** for `migration.v2.workflows.persistence`.
One intent owns the stable child identity, child-creation idempotency identity,
and original invocation/input correlations. Later terminal observations reference
that unchanged intent and the corresponding terminal attempt and generic Task
outcome. Generic outcomes remain generic; this decision does not select a stream
of repeated complete invocation-state records or outcome-owned child evidence.

The question and conceptual alternatives were retained as advisory artifacts, not
an activated repository checkpoint. This section records the current human
selection directly; it does not fabricate a checkpoint lifecycle or retroactively
turn the earlier recommendation into authority.

Decision artifacts are in
`/Users/eugene/.pi/agent/sessions/--Users-eugene-repos-ksdft2effmass--/subagent-artifacts/outputs/1a62effb-f96b-4a7d-8f5b-a055f16d288b/workflow-persistence-review/`:

- `nested-history-decision.md`, SHA-256
  `c765022d34c61844878c9d87b6fc368e49f168a46282181efcee39a0b2cf6e53`;
- `nested-history-checkpoint-proposal.md`, SHA-256
  `96bc4e85d3e02ce65f85cbe6199c1a22a33b84fd4fc5e43ed24a2c97ba64c960`;
- `correctness.md`, SHA-256
  `c0dcc9fb28c6965009f947d60e8abed73bc299f9a5375ee82c71589f282b5118`;
- `evidence.md`, SHA-256
  `af1d91fa4a55efaf27f0dab42f25f30ad303b0c422bc87a98060d09ff218f0a5`.

This authorizes revised implementation planning and independent antagonistic
plan review, followed by direct parent implementation and verification under the
existing sole-writer boundary. Exact record fields, wire/version compatibility,
structural/replay consumers and independent multi-revision lifecycle evidence
must be made explicit in that plan. Existing history and payloads must not be
rewritten, and missing intent events must not be invented. A new material choice
not determined by this selection remains a human boundary.

The already-authorized deterministic corrections remain in scope: bind each
new dispatch entry to its actual committing predecessor/successor revisions,
and correct the two affected test import groups. Neither correction nor the
nested lifecycle correction is yet implemented or verified by this decision.
Inherited conformance callable-ownership debt stays deferred to its owning
migration; it is not authorization for a subsystem rewrite.

The nested correction covers pending-to-first-terminal representation. It does
not authorize new repeated-terminal reconciliation, cancellation, compensation,
child execution or cross-stream atomicity semantics. Revised planning and later
implementation both retain independent review gates. All prior non-waived
boundaries, including no commit/push or automatic successor activation, remain
in force. No software completion or human acceptance is recorded.

## Compatibility clarification: no existing v1 pending runs

The conditional Option B plan identified a further compatibility question:
whether to preserve v1 behavior and apply the corrected model to new v2 streams
only, or additionally implement explicit continuation of persisted v1 pending
children through a version transition. The assistant explained that the first
option is the smaller non-migrating boundary, preserves existing bytes/readers
and previously supported operations, but does not repair legacy pending-child
advancement. The recommendation was conditional on whether existing v1 pending
runs need continuation. The human clarified:

> we don't have any v1 pending runs

This is a human-provided repository-use fact, not an agent-calculated inventory
or a claim that no v1 data of any kind exists. In the context of the existing
bounded authorization and conditional recommendation, it removes the need for
legacy pending-run continuation. Work proceeds with **compatibility option 1:
preserve v1 and apply Option B to newly created v2 streams only**. This normalized
scope is distinct from the verbatim response above.

The finalized plan must retain exact v1 reconstruction, serialization, historical
bytes/content/receipts, supported replay and previously legal same-v1 extensions.
It must explicitly pair the v1 and v2 model, wire and writer identities; reject
cross-version successors before store submission; and demonstrate the new
pending-to-first-terminal lifecycle using v2 histories. No old bytes, records,
identity labels or missing events are rewritten or invented. Legacy pending-child
advancement remains a documented limitation, not a defect claimed repaired for
v1. The human clarification does not authorize creating or automatically
restarting children, deleting legacy artifacts, or treating future v1 pending
runs as automatically upgradeable.

The conditional plan and independent review remain unchanged historical reports
in the external `e652803e-d322-4c6a-8eef-d4c3018e3ba1/workflow-option-b/`
artifact directory: `implementation-plan.md` has SHA-256
`29564b84034ed663129a0bbc1845775a13b08124c281fb1239d337ec0e6c61fb`,
and `implementation-plan-review.md` has SHA-256
`79b6456b2ffeb1b0eafa34f82f52dcf28098c88f3c0f532fdd6b6b83d75691b5`.
The review also requires synchronization of three additional live documentation
pages; this is a deterministic plan correction, not another architecture choice.

Finalize this branch and its documentation scope, then perform the bounded
independent re-review before direct parent implementation. The later implemented
correction still requires software checks and independent review. No Task
completion, scientific execution, dependency change, successor activation,
commit or push is authorized by this clarification.

## Superseding instruction: correct the current v1 model

After the assistant explained the defect and proposed a second WorkflowRun
format, the human instructed:

> so just update the v1

This supersedes the preceding new-v2-streams-only compatibility direction and
the associated model/wire/writer version-2 plan. Correct the current v1
WorkflowRun implementation using the already selected Option B separation of
immutable child intent and terminal observations. Do not introduce a second
format, schema-2 runtime/reference bundle, cross-version transition policy or
production migration for this correction.

The earlier statement that there are no v1 pending runs remains a human-provided
use fact, not evidence that all v1 artifacts are disposable. Stored data and
historical bytes must not be rewritten or deleted. The bounded revised plan
should preserve existing v1 behavior where compatible and implement the
append-only lifecycle directly within v1, with explicit typed reconstruction
and independent multi-revision evidence. This instruction authorizes correction
of the maintained v1 public model/wire contract, not fabricated historical
intent, arbitrary compatibility machinery or loss of existing data.

The obsolete finalization reviewer run
`1a89a893-99c6-4599-a37a-e05e4aa28810` was intentionally stopped following this
human redirection; terminal state was observed as `stopped`. Its interrupted
review is not a completed gate or an infrastructure failure. Earlier plans and
reports remain unchanged historical artifacts, not current versioning authority.

Use a bounded revised-plan challenge and then direct parent implementation under
the existing sole-writer boundary. Keep the dispatch-entry revision-binding and
two import-group corrections in scope. Independent implemented-result review
and software checks remain required. No installed-package recovery, dependency
change, scientific execution, data deletion, commit, push or successor
activation follows from this instruction.

## Non-waived boundaries

Stop for a genuine unresolved scientific, public-contract, or architectural choice
not determined by existing authority. Routine implementation choices and corrections
under an accepted contract require no additional human approval.

No dependency or licensing change, scientific setting change, QE/Wannier invocation,
remote computation, external project-data transmission, destructive calculation-data
operation, history rewriting, release, publication, or new scientific-acceptance
claim is authorized. Existing unresolved checkpoints remain binding. No reviewer or
passing check may supply authority for these actions.

Preserve retained calculation artifacts and historical acceptance records. Use
synthetic local software tests and fixture-process tests only; they do not establish
scientific validation, production convergence, or a historical scientific run.
