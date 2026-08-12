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

## Authority isolation

- Evidence may support a claim but would not activate a Task.
- Telemetry may observe a transition but would not authorize or validate it.
- A receipt may document an attempted action but would not replace successor
  state.
- Generated state may be checked against authority but would not become source
  authority.
- Git history may recover prior state but would not automatically resume it.
- A capability catalog would be fixed for one running operator; an operator
  could not mutate its own available actions.

## Current active scientific work

This proposal does not pause, modify, or absorb
`bulk-silicon.records.periodic.extraction`. No Architecture v2 action may be
executed merely because its name appears here, and no successor activation is
proposed.
