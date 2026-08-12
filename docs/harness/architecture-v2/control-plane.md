# Architecture v2 control plane

> **Proposed architecture; inactive; not implemented; not accepted.**

Architecture v2 proposes a minimal live control state while preserving current
v1 authority until a later migration is separately activated and verified.

## Proposed live state

$$
K=(P,T,G,Q,A,U,C),
$$

where:

- $P$ is applicable policy;
- $T$ is the live Task catalog;
- $G$ is the operational Task graph;
- $Q$ is selection state;
- $A$ is active authorization;
- $U$ is unresolved human decisions; and
- $C$ is the capability catalog.

The proposed live control plane would contain only:

- applicable policy;
- active, prospective, and resumable Tasks;
- operational graph relationships;
- explicit selection state;
- at most one active authorization;
- unresolved human decisions; and
- available agents, skills, and actions.

A completed Task would remain live only while it has a demonstrated operational
role, such as satisfying a prerequisite or preserving a resumable boundary.
Removal from live state would not erase Git history or accepted evidence.

## Proposed non-authoritative or historical classifications

| Surface | Proposed classification |
|---|---|
| SQLite | Deterministic immutable projection |
| SQL export | Deterministic recovery/inspection projection |
| Generated Task Markdown | Documentation projection |
| Projection manifests | Generated artifact-set description |
| Reports | Derived evidence or analysis, according to their declared claim |
| Action receipts | Non-authoritative execution observations |
| Telemetry | Non-authoritative operational observation |
| Resolved checkpoints | Git history or retained decision evidence, not unresolved authority |
| Closed Tasks with no operational role | Git history |
| Historical chains | Git history |
| Archives retained only for prior operation | Git history after a verified migration |

This reduction is not performed by the planning Task. Current v1 records remain
authoritative according to existing policy.

## Transition model

A future typed control action would produce a candidate successor:

$$
K' = F_a(K,q),
$$

where $q$ is a typed request, $a$ is an action authorized for the current
operator profile, and $F_a$ is a deterministic transition. Candidate $K'$ would
not become current merely because it was constructed: successor-state
validation and synchronization must pass first.

The model separates four questions:

1. **Public software extensibility:** which objects downstream code may compose.
2. **Operator action availability:** which actions one fixed profile exposes.
3. **Transition validity:** whether $F_a(K,q)$ satisfies control invariants.
4. **Isolation:** which filesystem/process effects the operating environment can
   technically perform.

Passing one question does not answer another. A public action need not be
available to a scientific operator. An available action may still reject a
request. A valid transition does not prove operating-system confinement.

## Operation lifecycle policy

The proposed [operation lifecycle](operation-lifecycle.md) distinguishes
preflight, implementation, verification, conditional read-only review, and
conditional human acceptance. Applicable policy selects a route from operation
risk and claim boundaries. Lifecycle stages do not themselves create Tasks,
agents, checkpoints, commits, or human decisions.

Current v1 can declare mutating delegation unauthorized but does not strongly
enforce one mutating identity through restricted dispatch. A later v2 boundary
may distinguish `single_writer` from `delegated`; restricted dispatch, not an
ownership manifest alone, would enforce mutating identity. Manifests remain for
actual concurrent or delegated mutation, while read-only review remains outside
mutating ownership. This enforcement design is proposed and deferred.

## Execution-context contract

Repository execution context would be validated around each operation rather
than inserted into $K$ as one globally frozen session digest. A
`RepositoryContextRequirement` would state only the preconditions needed by the
requested Action. `ObserveRepositoryContext` would observe an explicit absolute
root, and `ValidateRepositoryContext` would compare that observation with the
requirement before repository-state conclusions or effects are produced.

Postconditions are likewise operation-specific. Read-only inspection can require
an unchanged exact revision; source modification can intentionally dirty a clean
starting worktree; synchronization can intentionally replace projections; and
scientific execution can bind executable and input identities. A scientific
parser would not acquire a control-state dependency merely because the control
plane can compute a digest.

Maintained paths would be confined beneath the supplied root and Git operations
would be root-qualified. Ambient `cwd` and invocation directory are not
repository authority. The same validation must work without a receipt or
telemetry store.

## Authority isolation

- Evidence may support a claim but would not activate a Task.
- Telemetry may consume operation transitions and ResultObjects, optionally
  through receipts, but would not authorize transitions, validate execution
  context, replace deterministic preconditions, create a competing finding
  hierarchy, or automatically create Tasks or checkpoints.
- A receipt may document an attempted action and retain existing findings but
  would not replace successor state or define a competing defect hierarchy.
- Generated state may be checked against authority but would not become source
  authority.
- Git history may recover prior state but would not automatically resume it.
- A capability catalog would be fixed for one running operator; an operator
  could not mutate its own available actions.

## Current active scientific work

This proposal does not pause, modify, or absorb
`bulk-silicon.records.periodic.extraction`. Harness governance of a later
scientific execution would not make periodic scientific records depend on
repository-context observations or harness telemetry. This proposal has no
dependency on the current QEXSD implementation. No Architecture v2 action may be
executed merely because its name appears here, and no successor activation is
proposed.
