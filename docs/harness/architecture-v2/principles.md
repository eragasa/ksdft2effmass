# Architecture v2 principles

> **Proposed architecture; inactive; not implemented; not accepted.**

These principles are planning criteria. They do not alter the current harness or
the accepted `bulk-silicon.records.periodic.extraction` implementation.

## Authority before representation

1. Authoritative sources would be explicit and read once into an immutable
   `HarnessSourceSnapshot`.
2. Normalized `HarnessState` would be derived, not an additional authority.
3. SQLite, SQL, generated Task Markdown, manifests, reports, receipts, and
   telemetry would be projections or observations, never fallback authority.
4. Git history would preserve prior states and decision boundaries without
   keeping closed, operationally irrelevant records live.
5. Compilation, checking, and synchronization would share one semantic path;
   alternate validators would not reconstruct competing meanings.

## Cohesive ownership

A proposed class would exist only when it owns a meaningful invariant, state
boundary, transformation, or extension contract. Incidental algorithmic steps
would remain methods. There would be no class per file format, table, control
record, or procedural step. ResultObjects would be semantic DataObjects without
nominal inheritance merely to label that relationship.

The proposed dependency direction is:

```text
generic compilation and domain behavior
← project-specific composition
```

Project-specific composition may depend on generic behavior. Generic behavior
must not import project-specific composition.

## Public extension strategy under evaluation

Architecture v2 must not silently choose an extension model. The proposal
compares four boundaries:

| Strategy | Benefits | Risks | Proposed disposition |
|---|---|---|---|
| Public concrete composable objects | Stable inspectable values and explicit dependencies; useful to downstream projects | Too many public objects can freeze incidental design | **Preferred provisionally** for meaningful architectural boundaries only |
| Public protocols for demonstrated families | Allows multiple validators or projectors without common inheritance | Premature protocols encode imagined implementations | **Conditional proposal** only after at least two real interchangeable implementations |
| Private implementation owners | Keeps helper algorithms changeable and avoids accidental compatibility promises | Can hide policy if the public contract is incomplete | **Preferred provisionally** for incidental algorithms and one-off mechanics |
| Unrestricted subclass/plugin extension | Third parties can inject behavior dynamically | Mutable catalogs, unclear authority, unsafe loading, compatibility burden | **Not recommended** for the proposed v2 boundary |

The provisional recommendation is documented stable import paths for meaningful
architectural objects, explicit composition for extension, private incidental
steps, and protocols only for demonstrated families. The running operator would
not mutate its available action catalog. This recommendation remains unaccepted.

The plan does not propose plugin frameworks, service locators, mutable global
registries, dependency-injection frameworks, abstract bases without multiple
real implementations, compatibility layers for pre-alpha code, or public
wrappers around helper logic.

## Explicit repository ownership

Repository-sensitive Actions would receive an explicit absolute repository root.
Maintained paths would never be resolved from ambient `cwd`, and Git operations
would use the supplied root, for example:

```bash
git -C <absolute-repository-root> ...
```

Canonical paths would be confined beneath that root. The invocation directory
may be observed as diagnostic information, but it would not establish repository
authority or select a worktree.

## Context-specific preconditions

Execution context would be an operation-specific precondition and postcondition
contract, not one globally frozen session state. An Action would state only the
conditions relevant to its actual inputs and effects:

- read-only inspection may require an exact revision;
- source modification validates its starting revision but intentionally changes
  working-tree state;
- control synchronization validates authoritative inputs and intentionally
  changes projections;
- scientific execution binds executable and input identities; and
- a scientific parser would not depend on a control-state digest unless control
  state is genuinely one of its inputs.

Architecture v2 would not require every Action to carry an irrelevant global
context digest. Dirty state may be diagnostic or an explicit operation
constraint; it is not automatically a universal failure.

## Policy-selected operation lifecycle

Preflight, implementation, verification, read-only review, and human acceptance
are distinct stages. Policy selects only the stages applicable to an operation's
risk and claim boundary; a stage does not automatically imply a separate Task,
agent, checkpoint, commit, or human decision. The complete proposed semantics
and routes are defined in [operation lifecycle](operation-lifecycle.md).

Current v1 may declare mutating delegation unauthorized, but only later
restricted dispatch could strongly enforce one mutating identity. Ownership
manifests represent actual concurrent or delegated mutation; read-only review is
conditional post-implementation activity outside mutating ownership. This
execution-topology work remains proposed and deferred.

## Correctness before telemetry

Deterministic execution-context validation and session observation are distinct:

```text
deterministic execution-context validation
≠
session observation and telemetry
```

The intended sequence is:

```text
explicit request
→ context validation
→ confined Action execution
→ ResultObject
→ optional operation observation
```

Telemetry consumes operation transitions and ResultObjects, optionally through
operation receipts. It does not authorize an operation, replace precondition
validation, or make an otherwise unsafe repository-sensitive Action safe.
Correctness therefore must not depend on telemetry, and such an Action must
remain safe when no telemetry store exists. Telemetry also does not create a
competing finding hierarchy or automatically create Tasks or checkpoints.

Existing structured findings and validation results remain the defect
vocabulary. Architecture v2 would not introduce a competing
`HarnessFailureObservation` finding hierarchy. A later receipt may retain
existing findings without redefining them.

## Architecture boundary

The harness governs scientific execution, including applicable repository and
protected-execution preconditions. Scientific records do not depend on harness
telemetry. Repository-context and telemetry objects would not be introduced into
periodic scientific records, and this proposal does not depend on the current
QEXSD implementation.

## Scientific fast path as acceptance scenario

The primary future architecture acceptance scenario would be the completed QE
tutorial sequence:

```text
human authorization
→ one bounded calculation
→ compact provenance
→ artifact inventory
→ semantic extraction
→ human review
```

Architecture v2 should require fewer harness-only mutations and validation
passes than v1 while preserving protected-action authority, provenance, exact
scientific boundaries, and human review.

A later comparison should measure, without implementing telemetry in this Task:

- human decisions;
- control-state mutations;
- generated artifacts changed;
- commands invoked;
- validation wall time;
- harness effort relative to scientific-task effort;
- duplicate repository reads;
- duplicate validation passes;
- correction cycles;
- agent tool calls; and
- unexpected sidecar or temporary artifacts.

These are effectiveness observations, not proof of software correctness,
scientific validity, or general agent superiority.

## Explicit planning non-goals

No source or test refactoring, SQLite change, control migration, CLI change, Pi
extension, agent/skill change, telemetry, CPN integration, pseudopotential work,
simulation, periodic extraction, dependency change, release action, or successor
activation is proposed for execution by this planning Task.
