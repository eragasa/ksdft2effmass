# Architecture v2 migration plan

> **Proposed architecture; inactive; not implemented; not accepted.**

This is a bounded sequence proposal, not a set of activated Tasks. No child Task
is created by this plan. Every slice would require separate authority, exact
path ownership, proportional verification, and a stop decision before the next
slice.

## Governed-operation lifecycle sequence

The first bounded slice would formalize the proposed
[operation lifecycle](operation-lifecycle.md) and incorporate explicit
repository-context validation into operation-specific preflight before any
telemetry implementation. The eight lines below are an ordered planning
sequence, not eight Tasks:

```text
1. freeze operation-state semantics
2. reuse or define minimum request/result boundaries
3. implement repository-context preflight
4. implement policy-selected lifecycle transitions
5. add receipts for actual governed operations
6. integrate optional read-only review
7. inspect Pi session events
8. design telemetry only from observed needs
```

Correctness must be established without a telemetry store. Pi-event inspection
is deferred until governed operations produce demonstrated observation needs;
it is not permission to add telemetry. Receipt persistence, event formats,
querying, retention, privacy, correlation, recurrence analysis, and failure
catalogs remain later separate decisions.

## Current-to-target context dispositions

| Current behavior | Target behavior | Status |
|---|---|---|
| Ambient working-directory dependence | Explicit repository-root ownership | Proposed |
| Ad hoc Git-context checks | `ObserveRepositoryContext` | Proposed |
| Prompt-only context assertions | `ValidateRepositoryContext` | Proposed |
| Result logs without a common envelope | Optional `HarnessOperationReceipt` | Deferred |
| Unexamined Pi session data | Retrospective inventory | Deferred |
| No recurrence analysis | Evidence-driven later design | Deferred |

No disposition introduces repository-context or telemetry fields into periodic
scientific records, and none depends on the active QEXSD implementation.

## Proposed slices

### 1. Governed-operation lifecycle and repository-context preflight

- **Objective:** Establish distinct preflight, implementation, verification,
  conditional read-only review, and conditional human-acceptance semantics, then
  make selected repository-sensitive operations validate explicit repository
  ownership during applicable preflight.
- **Current owner:** Ambient command context, prompts, ad hoc Git checks, and
  operation-specific procedural routing.
- **Target owner:** Minimum operation request/result boundaries, policy-selected
  lifecycle transitions, `RepositoryContext`, `RepositoryContextRequirement`,
  `ObserveRepositoryContext`, and `ValidateRepositoryContext` using existing
  structured findings and ResultObjects where sufficient.
- **Retained public behavior:** Existing valid operations, authority boundaries,
  finding vocabulary, conditional review, and human decision ownership.
- **Allowed changes:** Freeze operation-state semantics; reuse or define minimum
  request/result boundaries; add explicit-root, operation-specific preflight;
  implement policy-selected transitions; add receipts only for actual governed
  operations; and integrate optional read-only review.
- **Prohibited expansion:** No class per lifecycle state, universal replay of all
  validators, telemetry store, JSONL, SQLite observation projection, middleware,
  hooks, scientific-record dependency, global context digest, ambient repository
  discovery, or automatic Task/checkpoint creation.
- **Verification:** Route accounting; clean isolated-worktree acceptance;
  dirty-policy, exact starting-revision, delegation-policy, and path-escape cases;
  and `HARNESS.CONTEXT.WORKTREE_MISMATCH` before repository conclusions.
- **Rollback boundary:** Remove selected integrations while retaining current
  operation routes; no telemetry migration is involved.
- **Stopping condition:** Stop if stages are forced into Tasks or classes, safety
  depends on telemetry, or one global context shape must contain conditions
  irrelevant to an operation.

### 2. Immutable source and normalized-state boundaries

- **Objective:** Introduce explicit source artifacts, one closed source snapshot,
  and a minimal normalized state without changing outputs.
- **Current owner:** Canonical input resolver, repository ingestors, Task/resource/
  evidence adapters.
- **Target owner:** `HarnessRepositoryLoader`, `HarnessSourceSnapshot`,
  `HarnessCompiler`, `HarnessState`.
- **Retained public behavior:** Current source selection and validation results.
- **Allowed changes:** Add internal/concrete boundaries and parity fixtures.
- **Prohibited expansion:** No projection, SQLite, CLI, control reduction, or
  action system changes.
- **Verification:** Same selected sources, normalized identities, findings, and
  generated outputs under deterministic parity cases.
- **Rollback boundary:** Revert the slice; current loader/ingestion remains sole
  route.
- **Stopping condition:** Stop if one immutable snapshot cannot represent current
  source authority without importing generated projections.

### 3. Compilation separate from projection

- **Objective:** Make normalized compilation independent of artifact formats.
- **Current owner:** Private complete candidate generation builder.
- **Target owner:** `HarnessCompiler` and `HarnessProjector`.
- **Retained public behavior:** Current sync/check artifact content.
- **Allowed changes:** Extract deterministic transformation boundaries.
- **Prohibited expansion:** No output deletion, format redesign, or publication
  change.
- **Verification:** Equal normalized state yields equal complete candidate set.
- **Rollback boundary:** Keep existing generation builder callable.
- **Stopping condition:** Stop on hidden repository reads or SQLite table rules
  required by compilation.

### 4. SQLite candidate, publication, and verification lifecycle

- **Objective:** Enforce temporary mutable construction and immutable maintained
  projection.
- **Current owner:** `dbcontrol`, migrator publication, source verifier.
- **Target owner:** private SQLite projector, `HarnessSynchronizer`, comparator.
- **Retained public behavior:** Logical SQLite content, SQL export, sync/check
  outcomes.
- **Allowed changes:** Candidate location, connection lifecycle, publication and
  read-only verification mechanics.
- **Prohibited expansion:** No schema or Task semantics change.
- **Verification:** Integrity, foreign keys, logical parity, failure rollback,
  and absence of maintained-path sidecars.
- **Rollback boundary:** Restore previous publisher and maintained artifact set.
- **Stopping condition:** Stop if any maintained command needs write access to the
  tracked database.

### 5. Domain validators separate from composition

- **Objective:** Keep Task, graph, resource, evidence, checkpoint, capability,
  and artifact rules with their domains.
- **Current owner:** Domain validators plus `HarnessValidator` composition.
- **Target owner:** Explicit domain validators and narrow validation composition.
- **Retained public behavior:** Existing finding meanings and aggregate status.
- **Allowed changes:** Dependency injection by explicit composition and result
  normalization.
- **Prohibited expansion:** No new evidence claims or CLI consolidation.
- **Verification:** Domain fixture parity, deterministic ordering, and claim-
  boundary agreement.
- **Rollback boundary:** Retain current aggregate validator until parity passes.
- **Stopping condition:** Stop if composition must duplicate domain rules.

### 6. Projectors separate from synchronization

- **Objective:** Make every projection side-effect-free with respect to maintained
  paths and centralize publication.
- **Current owner:** Control projector and migrator publisher.
- **Target owner:** `HarnessProjector`, `HarnessArtifactSet`,
  `HarnessSynchronizer`.
- **Retained public behavior:** SQLite, SQL, Markdown, indexes, graphs, and
  manifests that remain selected.
- **Allowed changes:** Complete candidate-set ownership and atomic replacement
  mechanics.
- **Prohibited expansion:** No live-state reduction or output-format removal.
- **Verification:** Candidate closure, stale-output handling, rollback injection,
  and check-without-write evidence.
- **Rollback boundary:** One complete prior artifact set.
- **Stopping condition:** Stop if a projector publishes or synchronizer recompiles.

### 7. Reduce live control state

- **Objective:** Represent only $K=(P,T,G,Q,A,U,C)$ as live authority.
- **Current owner:** Task/chain/checkpoint catalogs plus authoritative SQLite
  relationships.
- **Target owner:** live Task catalog, graph, selection, activation, unresolved
  decisions, and capability catalog.
- **Retained public behavior:** Current valid selection, one-active-Task rule,
  prerequisites, explicit activation, and human decision authority.
- **Allowed changes:** Move operationally irrelevant closed/history records to Git
  history after reachability proof.
- **Prohibited expansion:** No scientific Task modification or automatic
  successor activation.
- **Verification:** Before/after authority queries, reachability proof, resumable
  boundaries, and generated projection parity for retained live state.
- **Rollback boundary:** Decision-boundary commit restoring prior control set.
- **Stopping condition:** Stop on unresolved operational consumers or loss of an
  accepted prerequisite/decision.

### 8. Typed semantic control transitions

- **Objective:** Introduce deterministic $K'=F_a(K,q)$ actions.
- **Current owner:** Manual record edits, prompts, validators, and current CLIs.
- **Target owner:** typed requests, action authorizer, deterministic ActionObjects,
  successor validator.
- **Retained public behavior:** Human authority, fail-closed validation, explicit
  activation, no automatic successor.
- **Allowed changes:** One bounded transition at a time with candidate-state
  evidence.
- **Prohibited expansion:** No unrestricted filesystem/process action or plugin
  registry.
- **Verification:** Positive/negative authorization, deterministic successor,
  invalid-state rejection, and no-publication tests.
- **Rollback boundary:** Leave manual current route available until demonstrated
  parity.
- **Stopping condition:** Stop if action availability and transition authority
  cannot be separated.

### 9. Restricted Pi action exposure

- **Objective:** Expose a fixed action catalog per operator profile.
- **Current owner:** Prompts, agent tool lists, and unrestricted tool execution.
- **Target owner:** descriptors, immutable catalog, dispatcher, profiles, bounded
  effect context.
- **Retained public behavior:** Existing human authority and underlying public
  library composability.
- **Allowed changes:** Pi-local exposure and profile-specific request routing.
- **Prohibited expansion:** No claim of OS sandboxing, runtime catalog mutation,
  service locator, or remote execution.
- **Verification:** Catalog immutability, denied-action cases, path confinement,
  and profile capability matrices.
- **Rollback boundary:** Remove the restricted operator integration without
  altering core actions.
- **Stopping condition:** Stop if allowlists are presented as a security boundary.

### 10. One real scientific vertical slice

- **Objective:** Exercise authorization → execution → provenance → inventory →
  extraction → human review through v2.
- **Current owner:** Existing scientific Tasks and protected-execution policy.
- **Target owner:** Same scientific domain owners using v2 control/actions.
- **Retained public behavior:** Scientific inputs, settings, artifacts,
  provenance, warning disposition, and human review.
- **Allowed changes:** Harness routing/evidence only under separate protected
  authorization.
- **Prohibited expansion:** No new calculation, settings change, backend, or
  validation claim merely for architecture testing.
- **Verification:** Compare the effectiveness measures in
  [principles](principles.md) and exact scientific-output identity.
- **Rollback boundary:** Preserve the accepted v1 reproduction route and external
  artifacts.
- **Stopping condition:** Stop on any scientific-byte/meaning drift or greater
  ceremony without justified control benefit.

### 11. Delete superseded v1 behavior after parity

- **Objective:** Remove only v1 behavior proven superseded and unused.
- **Current owner:** v1 modules, facades, CLIs, projections, tests, and docs.
- **Target owner:** accepted v2 surfaces and Git history.
- **Retained public behavior:** Demonstrated required operations and supported
  contracts only.
- **Allowed changes:** Delete unreachable pre-alpha compatibility and duplicate
  routes with synchronized tests/docs.
- **Prohibited expansion:** No speculative replacement or deletion by count.
- **Verification:** Downstream consumer audit, full gates, v1/v2 parity evidence,
  one consolidated review, and human acceptance.
- **Rollback boundary:** One deletion commit after a retained pre-deletion
  boundary.
- **Stopping condition:** Stop on any unresolved consumer or parity failure.

## Sequence rules

Slices are serial and bounded. A slice cannot infer activation of the next.
No big-bang branch may combine live-state reduction, action exposure, SQLite
lifecycle changes, and v1 deletion. At most one consolidated correction pass
should follow each material implementation review; unresolved architecture or
scientific decisions return to the human boundary.

## Effectiveness decision

A later v2 acceptance comparison should report raw measures and contextualize
harness effort against the scientific work. Lower counts are not automatically
better: fewer human decisions must not erase protected-action authority, and
fewer validations must not reduce required evidence. The target is removal of
duplicate or ceremonial work while retaining meaningful controls.
