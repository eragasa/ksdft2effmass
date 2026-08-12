# Architecture v2 governed execution

> **Proposed architecture; inactive; not implemented; not accepted.**

This page describes an eventual operating model. It does not add Pi tools,
action code, profiles, schemas, or process isolation.

## Proposed request path

```text
restricted Pi operator
→ typed request
→ action authorization
→ deterministic ActionObject
→ candidate transition
→ successor-state validation
→ synchronization
→ non-authoritative receipt
```

```mermaid
sequenceDiagram
  participant O as Restricted Pi operator
  participant D as Action dispatcher
  participant Z as Authorizer
  participant A as Deterministic action
  participant V as State validator
  participant S as Synchronizer
  O->>D: typed request q
  D->>Z: descriptor + profile + current K
  Z-->>D: authorized action a or rejection
  D->>A: F_a(K,q)
  A-->>D: candidate K'
  D->>V: validate K'
  V-->>D: validation result
  D->>S: validated candidate artifacts
  S-->>D: synchronization result
  D-->>O: non-authoritative receipt
```

The proposed transition is

$$
K' = F_a(K,q).
$$

An action would receive explicit current state and a typed request, remain
deterministic for those inputs, and return candidate successor state. It would
not publish directly. Authorization, transition construction, successor
validation, synchronization, and receipt formation would remain separate.

## Candidate operational objects

The following names are planning candidates, not exact public or wire contracts:

| Candidate | Proposed responsibility |
|---|---|
| `HarnessActionDescriptor` | Stable action identity, input/result kinds, effect class, and required capabilities |
| `HarnessActionCatalog` | Immutable available descriptors for one operator profile |
| `HarnessActionContext` | Explicit current state, roots, and bounded effect dependencies |
| `HarnessActionDispatcher` | Route a typed request only to a catalog action |
| `HarnessActionAuthorizer` | Decide whether current authority and profile permit the request |
| `HarnessActionReceipt` | Non-authoritative observation of request identity, result identity, and synchronization outcome |

The running operator would not register, replace, or enable actions dynamically.
Project-specific catalogs could compose generic actions, but generic actions
would not import project-specific composition.

## Proposed capability profiles

| Profile | Proposed capability boundary |
|---|---|
| Harness developer | Compile, validate, project to temporary state, compare, and—under explicit authority—synchronize harness artifacts |
| Bounded implementation writer | Read assigned state and modify only explicitly owned implementation paths; no control activation or catalog mutation |
| Scientific workflow operator | Perform only explicitly authorized scientific actions with protected-execution checkpoints and fixed artifact roots |
| Read-only reviewer | Load, compile, validate, compare, and inspect receipts/evidence; no synchronization or execution |

Profiles would constrain action availability, not define public software
extensibility. The same public concrete object could exist without being exposed
to every operator.

## Isolation and limitations

A Pi tool allowlist is **not** an operating-system security boundary. It can
reduce accidental capability exposure but cannot by itself prevent filesystem,
process, network, credential, or kernel-level effects available through another
allowed tool or compromised process.

A later implementation would need to distinguish:

- semantic authorization in `HarnessActionAuthorizer`;
- immutable catalog membership;
- deterministic transition validation;
- repository path confinement;
- subprocess and network policy;
- credential/data boundaries; and
- operating-system sandboxing where required.

The proposal does not claim that deterministic actions make external execution
deterministic. External execution would remain a separately authorized effect
boundary producing correlated immutable result/failure records.

## Receipt boundary

A receipt would be useful for traceability but would not:

- authorize the action;
- prove the action was correct;
- replace successor state;
- establish software or scientific validation;
- provide human acceptance; or
- become fallback authority after synchronization failure.

No receipt schema is frozen here.
