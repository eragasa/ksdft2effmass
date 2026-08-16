# Agent-system migration crosswalk

## Scope

This crosswalk maps the implemented Architecture v1 Pi resources and execution
practice to the prospective V2 [agent system](../../v2/agents/index.md) and
[`ksdft2effmass.pi.agents`](../../v2/ksdft2effmass/pi/agents/index.md). It does
not claim that the V2 package, restricted operator, deterministic adapter,
sandbox, action composition, or self-improvement lifecycle is implemented.

## Crosswalk

| V1 surface or practice | V2 disposition |
|---|---|
| `AGENTS.md`, skills, and role prompts | Retain as guidance and role context; never treat as capability enforcement |
| `.pi/agents/*.md` | Retain reusable descriptors; distinguish developer, operator, and reviewer capability ceilings |
| General-purpose parent or child tools | Retain only for explicitly authorized development roles; replace governed operator mutation with a closed action set |
| Pi tool allowlists | Retain and strengthen as model-request confinement, not OS security or operation authority |
| Project Pi extensions | Load only an identified thin adapter in governed profiles; disable ambient discovery |
| Direct edits to authoritative control state | Replace with explicitly composed domain ActionObjects and atomic repository transitions |
| Shell commands wrapping deterministic Python | Replace operator use with typed `ksdft2effmass.pi.agents` requests; retain bounded developer commands where authorized |
| Pi runtime status, sessions, missions, and handoffs | Retain as runtime evidence and recovery artifacts, never Harness authority |
| Agent-generated source | Retain as provisional candidate work in an isolated workspace under the actual domain owner |
| Manual promotion or cutover | Replace with identified eligibility evidence, explicit human decision, complete composition activation, and rollback target |
| Hot reload and dynamic tools | Retain as ordinary Pi capabilities outside governed promotion; prohibit them for operator action activation |

The existing [Pi harness subagent crosswalk](pi-harness-subagents.md) continues to
own child-session, delegation, worktree, handoff, and review migration. This page
owns the broader top-level agent capability and deterministic-operation boundary.

## Migration order

1. Inventory current roles, tool surfaces, mutation paths, authoritative state,
   extensions, and executable adapters without changing them.
2. Freeze the V2 request, result, action-composition, authority-binding,
   persistence, and threat-model contracts.
3. Implement `ksdft2effmass.pi.agents` under a separate authorized source Task.
4. Implement one thin Pi extension and one inspection-only profile without
   enabling authoritative mutation.
5. Add one bounded deterministic development operation and verify schema,
   authorization, stale revision, conflict, rejection, idempotency, indeterminate
   outcome, provenance, and output behavior.
6. Verify the operator tool surface and the selected OS isolation boundary with
   adversarial negative cases.
7. Introduce agent-authored candidate work only after fixed accepted actions and
   promotion behavior are understood.
8. Cut over one exact operation with a complete predecessor composition,
   accepted candidate composition, human promotion decision, and tested rollback.
9. Retire the corresponding direct operator mutation path only after replacement
   behavior passes its accepted compatibility gates.

No step activates its successor. Migration preserves historical records without
rewriting them as typed requests, constrained runs, verified transitions, or
accepted compositions when those facts did not exist.

## Status

Architecture v1 remains implemented. This crosswalk grants no V2 implementation,
source move, dependency change, operator launch, automatic promotion, protected
execution, publication, or release authority.
