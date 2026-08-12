# Architecture v2 principles

> **Proposed architecture; inactive; not implemented; not accepted.**

These principles are planning criteria. They do not alter the current harness or
the active `bulk-silicon.records.periodic.extraction` Task.

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
