# Agent-system migration crosswalk

## Scope

This crosswalk maps the implemented Architecture v1 Pi resources and execution
practice to the prospective v2 [agent system](../../v2/agents/index.md) and
[`ksdft2effmass.pi.agents`](../../v2/ksdft2effmass/pi/agents/index.md). It owns
the migration of capability, deterministic-operation, isolation, composition,
promotion, and rollback responsibilities.

The [Pi harness subagent migration](pi-harness-subagents.md) separately owns
repository role discovery, child-session delegation, assignments, worktrees,
handoffs, review, and Pi runtime artifacts. The two migrations meet at role
identity, launch reconciliation, and the distinction between conversational
roles and governed operations.

Architecture v1 remains implemented. Nothing on this page authorizes the v2
package, restricted operator, deterministic adapter, sandbox, action
composition, source mutation, self-improvement lifecycle, or protected
execution.

## Terms and responsibility split

The migration preserves three different execution roles:

| Role | Purpose | Mutation boundary |
|---|---|---|
| Conversational developer subagent | Produces provisional source, tests, or documentation under an exact assignment | General development tools only within the assignment and applicable ownership |
| Read-only reviewer subagent | Inspects an exact subject and reports findings | No mutation of the reviewed scope |
| Governed operator | Requests already accepted deterministic project operations | Closed typed action set; no general shell, edit, write, registration, or reload capability |

A parent Pi session may coordinate developer and reviewer subagents. It does not
become a governed operator merely by invoking a deterministic command. A
governed operator may propose candidate work, but it cannot author or activate
the composition that constrains it.

The deterministic owner of an operation remains its domain ActionObject and
repository. `ksdft2effmass.pi.agents` owns only Pi-facing transport,
content-identified composition, bounded invocation, and failure mapping. It does
not own Harness authority, scientific policy, successor construction, or
persistence.

## Implemented v1 baseline

The implemented baseline consists of:

- repository instructions, skills, and `.pi/agents/*.md` role descriptors;
- `.pi/settings.json` enablement overrides;
- general-purpose Pi tools for authorized development roles;
- installed Pi subagent orchestration and runtime control;
- direct Python commands and repository edits for authorized development work;
- deterministic domain operations invoked through ordinary development
  interfaces rather than a governed operator profile;
- project-local normalized descriptor/configuration values and generated agent
  catalog projections; and
- human-controlled integration, checkpoint, protected-action, and release
  boundaries.

V1 has no restricted operator profile, closed Pi action composition, public
`ksdft2effmass.pi.agents` package, trusted thin extension, operator sandbox,
composition promotion operation, or composition rollback operation.

## Current-to-target crosswalk

| V1 surface or practice | V2 disposition | Current migration state | Replacement or cutover evidence |
|---|---|---|---|
| `AGENTS.md`, skills, and role prompts | Retain as guidance and role context | Implemented | No capability or authority claim is derived from prompt text |
| `.pi/agents/*.md` | Retain reusable developer and reviewer descriptors; add a distinct governed-operator profile | Partially normalized | Stable role identities and capability ceilings are content-identified |
| General-purpose parent or child tools | Retain for explicitly authorized development roles | Implemented v1 behavior | Governed operator profile exposes no general mutation capability |
| Pi tool allowlists | Retain as model-request confinement | Implemented for project roles | Negative tool-surface checks demonstrate the selected profile only |
| Operating-system access inherited by Pi | Replace governed-operation reliance on ambient access with an explicit isolation profile | Not implemented | Platform-specific sandbox tests cover declared roots, network, process, resource, and credential policy |
| Project Pi extensions | Load only one identified thin adapter in governed profiles; disable ambient discovery | Not implemented | Profile and extension identities are fixed before session start |
| Direct edits to authoritative control state | Retain for authorized developer work during migration; replace governed operator mutation with domain ActionObjects and atomic repository transitions | No operator replacement | One exact operation passes transition and compatibility gates before its direct operator path is retired |
| Shell commands wrapping deterministic Python | Retain bounded developer commands; replace operator use with typed requests | Implemented v1 behavior | Closed request/result schemas and exact entrypoint identity are verified |
| Mutable or ambient action lookup | Prohibit for governed operation | No governed composition exists | Immutable `PiAgentActionComposition` identifies every exposed operation and predecessor |
| Pi runtime status, sessions, missions, receipts, and handoffs | Retain as runtime evidence and recovery artifacts | Implemented separation by policy | No runtime state is imported as Harness authority |
| Agent-generated source | Retain as provisional candidate work under the actual domain owner | Procedural v1 behavior | Candidate identity, sandboxed checks, independent review, and eligibility remain separate from promotion |
| Manual promotion or cutover | Replace governed composition changes with exact eligibility, human decision, authorized activation, and rollback target | Not implemented | New session starts from the accepted complete composition; running operator cannot reload itself |
| Hot reload and dynamic tools | Retain outside governed profiles where ordinary Pi use permits; prohibit for operator activation | Pi capability exists | Governed profile tests show no reload or registration path |

## Ordered migration increments

### 1. Inventory the implemented capability surface

Record selected repository roles, exact descriptor and project-settings
identities, Pi runtime names, enabled state, tool and skill ceilings, project
extensions, executable adapters, direct mutation routes, and authoritative
repositories. Runtime observations remain observations rather than Harness
state.

Completion evidence is a content-identified inventory with explicit omissions
and no inferred equivalence between repository role names and Pi runtime names.
This increment changes no role, setting, extension, or operation.

### 2. Freeze transport and composition contracts

Define closed immutable request, result, action-composition, authority-binding,
provenance, and failure contracts for one bounded development operation. Preserve
rejected, conflicting, indeterminate, and operational-error outcomes rather than
collapsing them into process success or failure.

The contract must bind request, attempt, idempotency, predecessor revision,
operation implementation, schema, policy, authority, candidate or committed
revision, and composition identities where applicable. It introduces no generic
public action registry or policy-owning dispatcher.

### 3. Select the threat model and isolation profile

State separately what Pi tool confinement, domain authorization, and operating-
system isolation establish. Select permitted roots, network policy, credential
policy, subprocess identity, environment filtering, process-tree termination,
resource limits, output bounds, and candidate-validation treatment for one
identified platform profile.

This step is a dependency and security boundary. Adding a sandbox, container,
service, or other dependency requires separate human authorization.

### 4. Implement the deterministic Pi adapter

Under separate source authority, implement the minimum
`ksdft2effmass.pi.agents` request, result, composition, and adapter contracts.
The adapter receives explicit immutable inputs, invokes one composed application
operation, validates the closed result, and maps Pi-specific failures without
reimplementing domain policy.

Software verification uses injected or deterministic operations. It invokes no
scientific executable and performs no authoritative mutation unless an exact
later test operation separately authorizes a disposable repository target.

### 5. Add an inspection-only Pi profile

Implement one thin content-identified Pi extension and one profile that disables
ambient extension discovery. Initially expose only root-confined inspection of
the accepted composition and operation schemas. Do not expose authoritative
mutation.

Verify exact tool names, schema rejection, bounded output, extension identity,
profile identity, runtime identity, and the absence of general shell, edit,
write, registration, and reload tools.

### 6. Add one bounded deterministic development operation

Expose one already-owned domain operation through the fixed adapter and profile.
Verify authorization denial, stale revision, conflict, validation rejection,
idempotent replay, indeterminate outcome, cancellation, timeout, output bounds,
provenance, and successful commit closure as applicable to that operation.

The first operation should be narrow, reversible, non-scientific, and useful
without creating a universal action framework. Its direct developer path remains
available until cutover acceptance.

### 7. Verify capability and isolation boundaries

Use adversarial negative cases to test traversal, symlink and hard-link policy,
case and Unicode handling, file-type replacement, environment leakage, ambient
imports, mutable `PATH`, network access, subprocess escape, process-tree
termination, resource exhaustion, oversized output, and candidate-controlled
validators according to the selected threat model.

Passing these checks establishes only the identified profile and platform
claims. It does not establish universal security or scientific correctness.

### 8. Introduce agent-authored candidates

Only after the fixed-operation path is understood may a governed operator
propose an improvement for separate developer assignment. Candidate source is
written in an isolated workspace under its domain owner and cannot modify the
active adapter, profile, composition, authority source, or promotion operation.

Verification, independent review, mechanical eligibility, human decision, and
promotion authorization remain distinct records and authorities.

### 9. Cut over one exact operation

Construct a complete candidate composition identifying all exposed operations,
schemas, implementations, dependencies, validators, profile and isolation
identities, compatibility findings, predecessor composition, and rollback
target. A current human decision selects the exact candidate; a separately
authorized activation starts a new governed session.

Retire the corresponding direct operator mutation route only after replacement
behavior passes its accepted compatibility gates. Authorized developer mutation
may remain where its broader role is still required.

### 10. Exercise rollback and recovery

Demonstrate rollback to the accepted predecessor composition without editing the
active composition in place. Reconcile state produced by the newer composition,
retain exact receipts and candidate identities, and require explicit authority
for destructive cleanup or quarantine.

No stopped or failed runtime silently resumes, promotes, rolls back, or discards
candidate work.

## Dependencies on the subagent migration

The following dependencies are directional:

| Agent-system increment | Required subagent-migration input |
|---|---|
| Capability inventory | Stable repository role, descriptor, settings, and Pi runtime identities |
| Inspection-only profile | Launch-time reconciliation of the selected profile and resolved Pi inventory |
| Candidate development | Explicit assignment, workspace ownership, and verifiable writer handoff |
| Independent review | Exact read-only subject and reviewer identity |
| Promotion eligibility | Verified candidate and review artifacts; never conversational agreement |
| Runtime recovery | Declared mission, run, session, patch, and worktree retention policy |

Conversational role availability never becomes an operation capability catalog.
Conversely, an accepted operation composition does not select a child role,
assign a Task, or grant path ownership.

## Compatibility, evidence, and rollback gates

Each cutover records:

- predecessor and candidate composition identities;
- exact request and result schema versions;
- operation and domain-owner identities;
- authority and repository revision bindings;
- compatibility findings for the retired direct route;
- tool-surface and isolation-profile evidence;
- candidate verification and independent review identities;
- human decision and separate activation authorization;
- rollback target and state-compatibility disposition; and
- residual limitations and excluded claims.

A passing process, test, review, or sandbox probe establishes only its declared
software or isolation condition. It does not provide human acceptance, protected-
action authority, scientific validation, or permission to retire another path.

## Deferred decisions

The following remain deferred until the increment that needs them:

- exact request, result, composition, and profile wire fields;
- the first deterministic development operation selected for exposure;
- the supported Pi version and TypeScript extension path;
- in-process versus bounded subprocess adapter invocation;
- the platform-specific OS isolation mechanism;
- runtime receipt and composition-retention locations; and
- compatibility-safe retirement of each direct operator mutation route.

A deferred decision blocks only its dependent increment. Material dependency,
public-contract, security-boundary, or operation-selection choices remain human-
owned.

## Status

Architecture v1 remains implemented. This crosswalk grants no v2 implementation,
source move, dependency change, operator launch, automatic promotion, protected
execution, publication, or release authority. Historical records are not
rewritten as typed requests, constrained runs, verified transitions, or accepted
compositions when those facts did not exist.
