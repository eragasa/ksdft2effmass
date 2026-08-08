---
document_id: ksdft2effmass.harness.001.005.000
task_id: harness-current.agents
parent: ksdft2effmass.harness.001.000.000
status: current
sphinx: excluded
---

# Agent and ownership inventory

This page accounts for the complete population under `.pi/agents/` after the
bounded durable-harness-role migration from development revision
`ad00272fba2219505bf52f82362a84bad27fede0`, which matched `origin/dev` at
preflight. The inventory describes retained records; it does not activate,
rename, or grant ownership to an agent. Current authority still comes from the applicable human
instruction, durable decisions, accepted contracts, task and chain state, and
any required validated ownership manifest. An agent file's existence establishes
neither selectable runtime discovery nor authority to act.

## Classification method

Each agent record was read in full. References were then checked across current
tasks, chains, checkpoints, ownership controls, retained harness-incubation
evidence, generic and local harness resources, the maintained control-plane
documentation, and this harness hierarchy. In the table:

- **Live** means a current, non-historical selection or assignment. No active
  task currently selects any phase-specific agent.
- **Selectable** means exposed by PI's runtime discovery after project settings
  are applied. Only the 10 durable records are selectable.
- **Historical** means a reference retained by a closed task, a closed chain, a
  resolved checkpoint, a superseded plan, a checksum catalog, or retained
  execution/review evidence.
- **Durable** identifies a broad current project role whose record is not limited
  to one named phase. It does not mean that the role is always authorized.
- **Durable harness** identifies one of the reusable harness capability records
  created by `harness-simplification.agents.durable-roles`. Availability is not
  assignment, activation, replacement, or acceptance.

The harness-incubation chain reports H0, H1, H3, H2, and H4 closed and
human-accepted, with `active_task: null`; H5 is inactive. The completed bounded
project-role simplifications used only durable harness writers and a durable
reviewer under explicit ownership. The final architecture-role refinement used
the same three durable harness capabilities without reactivating a
phase-specific agent. The other durable roles remain unassigned and available
unless a future authorized task selects them. All repository checkpoint records
are resolved or superseded. Those facts are why the phase-bound records below are historical
references rather than live phase assignments.

## Complete agent inventory

| Agent | Domain | Role | Access | Original phase | Current references | Lifecycle | Maintained replacement |
|---|---|---|---|---|---|---|---|
| [ksdft2effmass-architecture](../../.pi/agents/ksdft2effmass-architecture.md) | project | architecture | read-only | Optional project architecture analysis and human decision support | Live: generalized optional durable record, available only for explicitly task-authorized work. Analysis is read-only by default; only exact task ownership can permit narrow documentation or decision-record writes. Historical: the same identity retains closed OperatorRecord, backend-neutral CPN, Rust/control-plane, and H0 references. | durable | ksdft2effmass-architecture |
| [ksdft2effmass-documentation](../../.pi/agents/ksdft2effmass-documentation.md) | project | documentation | writer | OperatorRecord documentation; later CPN, schemas, Sphinx, and evidence documentation | Live: concise generalized maintained-documentation record, available only through an authorized task and validated ownership assignment. Historical: the same identity retains OperatorRecord and CPN documentation work, closed operator-record chains, and H0/H4 evidence. | durable | ksdft2effmass-documentation |
| [ksdft2effmass-harness-architecture](../../.pi/agents/ksdft2effmass-harness-architecture.md) | cross-domain | architecture | read-only | Durable harness architecture capability | Live: available for a future explicit genuine architecture assignment; not currently assigned. Historical: none. | durable | ksdft2effmass-harness-architecture |
| [ksdft2effmass-harness-cutover-architecture-reviewer](../../.pi/agents/ksdft2effmass-harness-cutover-architecture-reviewer.md) | cross-domain | architecture | read-only | H4 generic/local dependency direction and rollback-safe routing | Live: none. Historical: closed H4 ownership, shadow/parity records, review closure, and checksums. | historical-reference-only | ksdft2effmass-harness-architecture |
| [ksdft2effmass-harness-cutover-integration-reviewer](../../.pi/agents/ksdft2effmass-harness-cutover-integration-reviewer.md) | cross-domain | integration-review | read-only | H4 parity, packaging, cutover, rollback, and integration safety | Live: none. Historical: closed H4 ownership, correction/closeout, shadow/parity, review closure, and checksums. | historical-reference-only | ksdft2effmass-harness-integration-reviewer |
| [ksdft2effmass-harness-cutover-skill-resource-reviewer](../../.pi/agents/ksdft2effmass-harness-cutover-skill-resource-reviewer.md) | cross-domain | integration-review | read-only | H4 canonical skill/resource identity and compatibility | Live: none. Historical: closed H4 ownership/review evidence and closed `ARCHITECTURE-DECISION-SKILL-1`. | historical-reference-only | ksdft2effmass-harness-integration-reviewer |
| [ksdft2effmass-harness-documentation](../../.pi/agents/ksdft2effmass-harness-documentation.md) | cross-domain | documentation | writer | Durable harness documentation capability | Live: available for explicit assignment. Historical: used under exact ownership for all five completed project-role simplifications, including the final architecture-role refinement. | durable | ksdft2effmass-harness-documentation |
| [ksdft2effmass-harness-generic-resource-writer](../../.pi/agents/ksdft2effmass-harness-generic-resource-writer.md) | harness-generic | resource-writing | writer | H3 generic manifests, schemas, and skills | Live: none. Historical: accepted H1 ownership plan and closed H3 ownership/checksums. | historical-reference-only | ksdft2effmass-harness-implementation |
| [ksdft2effmass-harness-h2-verification-evidence-writer](../../.pi/agents/ksdft2effmass-harness-h2-verification-evidence-writer.md) | harness-generic | evidence-writing | writer | H2 retained software-verification and handoff evidence | Live: none. Historical: accepted H1 ownership plan and closed H2 ownership/checksums. | historical-reference-only | ksdft2effmass-harness-tests |
| [ksdft2effmass-harness-h3-verification-evidence-writer](../../.pi/agents/ksdft2effmass-harness-h3-verification-evidence-writer.md) | cross-domain | evidence-writing | writer | H3 generic/local resource verification and H3-to-H2 handoff evidence | Live: none. Historical: accepted H1 ownership plan and closed H3 ownership/checksums. | historical-reference-only | ksdft2effmass-harness-tests |
| [ksdft2effmass-harness-implementation](../../.pi/agents/ksdft2effmass-harness-implementation.md) | cross-domain | implementation | writer | Durable generic and project-local harness implementation capability | Live: available for explicit assignment. Historical: used under exact ownership for all five completed project-role simplifications, including the final architecture-role refinement. | durable | ksdft2effmass-harness-implementation |
| [ksdft2effmass-harness-integration-reviewer](../../.pi/agents/ksdft2effmass-harness-integration-reviewer.md) | cross-domain | integration-review | read-only | Durable final harness integration-review capability | Live: available for explicit assignment. Historical: performed the independent reviews of all five completed project-role simplifications, including the final architecture-role refinement. | durable | ksdft2effmass-harness-integration-reviewer |
| [ksdft2effmass-harness-local-doc-control-writer](../../.pi/agents/ksdft2effmass-harness-local-doc-control-writer.md) | cross-domain | control-writing | writer | H4 maintained documentation, live agent references, task/chain control, cutover, and rollback | Live: none. Historical: closed H4 ownership and shadow/parity/checksum evidence. | historical-reference-only | ksdft2effmass-harness-documentation |
| [ksdft2effmass-harness-local-python-writer](../../.pi/agents/ksdft2effmass-harness-local-python-writer.md) | harness-local | implementation | writer | H4 project-local composition, adapters, shadow routing, and parity records | Live: none. Historical: accepted H1 ownership plan and closed H4 ownership/shadow/parity evidence. | historical-reference-only | ksdft2effmass-harness-implementation |
| [ksdft2effmass-harness-local-resource-writer](../../.pi/agents/ksdft2effmass-harness-local-resource-writer.md) | harness-local | resource-writing | writer | H3 local profiles, extensions, and manifest | Live: none. Historical: accepted H1 plan, closed H3 ownership, and H4 migration/checksum evidence. | historical-reference-only | ksdft2effmass-harness-implementation |
| [ksdft2effmass-harness-local-test-parity-writer](../../.pi/agents/ksdft2effmass-harness-local-test-parity-writer.md) | harness-local | tests | writer | H4 local tests, shadow parity, retained evidence, and completion validator | Live: none. Historical: closed H4 ownership, shadow/parity, review, and checksum evidence. | historical-reference-only | ksdft2effmass-harness-tests |
| [ksdft2effmass-harness-option-a-contract-resource-writer](../../.pi/agents/ksdft2effmass-harness-option-a-contract-resource-writer.md) | cross-domain | resource-writing | writer | H2-HC01 Option A bounded H1/H3 contract-resource correction | Live: none. Historical: resolved H2-HC01 correction in closed H2 ownership/checksums. | historical-reference-only | ksdft2effmass-harness-implementation |
| [ksdft2effmass-harness-python-architecture-rust-reviewer](../../.pi/agents/ksdft2effmass-harness-python-architecture-rust-reviewer.md) | harness-generic | architecture | read-only | H2 generic Python architecture and intended Rust portability | Live: none. Historical: closed H2 ownership, architecture reviews, and checksums. | historical-reference-only | ksdft2effmass-harness-architecture |
| [ksdft2effmass-harness-python-documentation-writer](../../.pi/agents/ksdft2effmass-harness-python-documentation-writer.md) | harness-generic | documentation | writer | H2 maintained public harness documentation | Live: none. Historical: accepted H1 plan, closed H2 ownership, and H4 migration/checksum evidence. | historical-reference-only | ksdft2effmass-harness-documentation |
| [ksdft2effmass-harness-python-evidence-vvuq-reviewer](../../.pi/agents/ksdft2effmass-harness-python-evidence-vvuq-reviewer.md) | harness-generic | validation | read-only | H2 software-verification evidence and VVUQ-boundary review | Live: none. Historical: closed H2 ownership/reviews and H4 shadow/parity/checksum evidence. | historical-reference-only | ksdft2effmass-harness-tests |
| [ksdft2effmass-harness-python-implementation-writer](../../.pi/agents/ksdft2effmass-harness-python-implementation-writer.md) | harness-generic | implementation | writer | H2 generic Python 36-interface implementation | Live: none. Historical: accepted H1 plan, closed H2 ownership, and H4 migration/checksum evidence. | historical-reference-only | ksdft2effmass-harness-implementation |
| [ksdft2effmass-harness-python-integration-reviewer](../../.pi/agents/ksdft2effmass-harness-python-integration-reviewer.md) | harness-generic | integration-review | read-only | H2 imports, resources, packaging, dependency direction, and validation | Live: none. Historical: closed H2 ownership, integration reviews, and checksums. | historical-reference-only | ksdft2effmass-harness-integration-reviewer |
| [ksdft2effmass-harness-python-test-writer](../../.pi/agents/ksdft2effmass-harness-python-test-writer.md) | harness-generic | tests | writer | H2 class-owned/artifact-owned software-verification and completion gate | Live: none. Historical: accepted H1 plan, closed H2 ownership, and H4 migration/checksum evidence. | historical-reference-only | ksdft2effmass-harness-tests |
| [ksdft2effmass-harness-resource-architecture-reviewer](../../.pi/agents/ksdft2effmass-harness-resource-architecture-reviewer.md) | cross-domain | architecture | read-only | H3 generic/local resource architecture and intended Rust portability | Live: none. Historical: closed H3 ownership/checksums. | historical-reference-only | `develop-harness-resources`; ksdft2effmass-harness-architecture |
| [ksdft2effmass-harness-resource-documentation-writer](../../.pi/agents/ksdft2effmass-harness-resource-documentation-writer.md) | cross-domain | documentation | writer | H3 generic and local resource documentation | Live: none. Historical: accepted H1 plan and closed H3 ownership/checksums. | historical-reference-only | ksdft2effmass-harness-documentation |
| [ksdft2effmass-harness-resource-evidence-vvuq-reviewer](../../.pi/agents/ksdft2effmass-harness-resource-evidence-vvuq-reviewer.md) | cross-domain | validation | read-only | H3 fixtures, independent oracles, evidence, and VVUQ boundaries | Live: none. Historical: closed H3 ownership/checksums. | historical-reference-only | `develop-python-test-evidence`; ksdft2effmass-harness-tests |
| [ksdft2effmass-harness-resource-integration-reviewer](../../.pi/agents/ksdft2effmass-harness-resource-integration-reviewer.md) | cross-domain | integration-review | read-only | H3 validation, leakage, documentation, control-plane, and handoff | Live: none. Historical: closed H3 ownership/checksums. | historical-reference-only | ksdft2effmass-harness-integration-reviewer |
| [ksdft2effmass-harness-resource-test-writer](../../.pi/agents/ksdft2effmass-harness-resource-test-writer.md) | cross-domain | tests | writer | H3 generic and local textual fixtures | Live: none. Historical: accepted H1 plan and closed H3 ownership/checksums. | historical-reference-only | `develop-python-test-evidence`; ksdft2effmass-harness-tests |
| [ksdft2effmass-harness-resource-validation-writer](../../.pi/agents/ksdft2effmass-harness-resource-validation-writer.md) | harness-generic | validation | writer | H3 deterministic textual-resource completion validation | Live: none. Historical: accepted H1 plan and closed H3 ownership/checksums. | historical-reference-only | maintained resource/checksum/local-composition Actions |
| [ksdft2effmass-harness-skill-resource-cutover-writer](../../.pi/agents/ksdft2effmass-harness-skill-resource-cutover-writer.md) | cross-domain | resource-writing | writer | H4/TEST-EVIDENCE-SKILL-1 live skill/resource cutover; later architecture-decision skill resources | Live: none. Historical: closed H4 ownership and closed `ARCHITECTURE-DECISION-SKILL-1`. | historical-reference-only | ksdft2effmass-harness-implementation |
| [ksdft2effmass-harness-tests](../../.pi/agents/ksdft2effmass-harness-tests.md) | cross-domain | tests | writer | Durable harness software-verification capability | Live: available for a future explicit test assignment; not currently assigned. Historical: none. | durable | ksdft2effmass-harness-tests |
| [ksdft2effmass-implementation](../../.pi/agents/ksdft2effmass-implementation.md) | project | implementation | writer | Generalized production-source implementation of accepted public contracts on explicitly assigned paths | Live: concise durable record, available only through an authorized task and validated ownership assignment. Historical: the same identity retains closed OperatorRecord and backend-neutral CPN work, closed operator-record chains, and H0/H4 evidence. | durable | ksdft2effmass-implementation |
| [ksdft2effmass-integration-reviewer](../../.pi/agents/ksdft2effmass-integration-reviewer.md) | project | integration-review | read-only | Generalized durable cross-surface review of materially affected assigned work and connecting interfaces | Live: concise independent read-only record, available only through an authorized task with defined scope and review authorization. Historical: the same identity retains closed OperatorRecord, CPN, evidence, documentation, and control-plane review work, closed operator-record tasks/chains, and H0/H1/H4 evidence. | durable | ksdft2effmass-integration-reviewer |
| [ksdft2effmass-tests](../../.pi/agents/ksdft2effmass-tests.md) | project | tests | writer | Stable project test-evidence capability for independently checking task-assigned accepted public contracts | Live: concise durable record, available only through an authorized task and validated ownership assignment. Historical: the same identity retains closed operator-record chains and H0/H4 evidence. | durable | ksdft2effmass-tests |

## Population totals

The totals below are derived by counting the rows in the complete inventory.
“Durable harness roles” counts the available stable harness capability records;
it does not imply assignment or activation.

| Category | Count |
|---|---:|
| Total retained agent records | 34 |
| Selectable durable project roles | 5 |
| Selectable durable harness roles | 5 |
| Selectable phase-specific roles | 0 |
| Disabled historical-reference-only roles | 24 |
| Unresolved roles | 0 |

### Totals by domain

| Domain | Count |
|---|---:|
| project | 5 |
| harness-generic | 9 |
| harness-local | 3 |
| cross-domain | 17 |

### Totals by role

| Role | Count |
|---|---:|
| implementation | 4 |
| tests | 5 |
| documentation | 4 |
| integration-review | 6 |
| architecture | 5 |
| resource-writing | 4 |
| validation | 3 |
| control-writing | 1 |
| evidence-writing | 2 |
| other | 0 |

### Totals by access

| Access | Count |
|---|---:|
| writer | 21 |
| read-only | 13 |

### Totals by lifecycle

| Lifecycle | Count |
|---|---:|
| durable | 10 |
| phase-specific-live | 0 |
| historical-reference-only | 24 |
| unresolved | 0 |

## Runtime discovery disposition

PI project settings at [`.pi/settings.json`](../../.pi/settings.json) are the
configuration authority for selectable project-agent discovery. The exact
`subagents.agentOverrides` keys are the package-qualified runtime identities
reported by PI, and each of the 24 historical identities has `disabled: true`.
The 10 durable identities have no disabling override. PI's management `list`
action verifies exactly 10 selectable project agents: five durable project roles
and five durable harness roles, with no selectable phase-specific role.

All 34 agent files remain in `.pi/agents/`. The 24 disabled files are preserved
byte-for-byte for closed-task provenance, retained ownership references, old
checksums and reviews, architectural history, and Git history reconstruction.
Retirement therefore means retirement from selectable discovery, not deletion
or historical rewriting. No active task assigns a phase-specific role, and
neither file presence nor runtime discoverability infers task authorization.

## Durable target sets

The durable project set is:

```text
ksdft2effmass-implementation
ksdft2effmass-tests
ksdft2effmass-documentation
ksdft2effmass-integration-reviewer
ksdft2effmass-architecture
```

All five names remain current project records, and all five durable roles have
been simplified. The test role independently checks accepted public contracts
on assigned paths; the implementation and documentation roles perform their
generalized work only on explicitly assigned paths; and the integration-review
role independently reviews materially affected surfaces and connecting
interfaces. The architecture role now provides proportional, explicitly
task-authorized architecture analysis and human decision support. It is read-only by default;
only exact task ownership can permit narrow documentation or decision-record
writes. Its sole durable routing is `develop-architecture-decision`, while an
authorized task may select supported subject-specific skills when needed.
Routing does not expand authority. No record bypasses task selection, path
ownership, checkpoint, review, or human-authority controls.

The available durable harness set is:

```text
ksdft2effmass-harness-implementation
ksdft2effmass-harness-tests
ksdft2effmass-harness-documentation
ksdft2effmass-harness-integration-reviewer
ksdft2effmass-harness-architecture
```

All five identities exist as reusable capability records. The implementation,
documentation, and integration-review roles were used under explicit,
non-overlapping ownership for all five completed project-role simplifications.
The harness tests and architecture roles remained unassigned. These uses do not
retroactively replace historical agents; discovery changes and retirement
require later separate authorization. Architecture roles in both sets are
optional specialists for material architecture decisions, not mandatory routine
participants.

## Duplication findings

The 24 harness phase records repeat useful separation-of-duty rules, but encode
phase and path assignments in agent identities rather than supplying them only
through task-scoped ownership:

- H2 and H4 each have separate implementation writers, while H3 divides resource
  implementation among generic, local, fixture, validator, documentation, and
  retained-evidence writers.
- Project, H2 Python, H3 resource, and H4 local-parity test responsibilities
  were described in separate writers, with evidence grammar and completion-gate
  mechanics repeated. The durable project test role now retains only stable
  capability and boundaries; skills own the mechanics and assignments own paths.
- The former project implementation record embedded OperatorRecord and CPN path,
  dependency, and correction procedure. Its durable role now retains generalized
  production-source responsibility and boundaries; tasks select supported
  subject specialization and ownership manifests supply paths.
- The former project documentation record embedded OperatorRecord and CPN
  topics, fixed path ownership, and task-specific recipes. Its durable role now
  retains generalized maintained-documentation responsibility and boundaries;
  tasks select supported subject specialization and ownership manifests supply
  paths.
- The former project integration-review record embedded OperatorRecord, CPN,
  fixed-path, fixed-command, correction-cycle, and checkpoint specialization.
  Its durable role now retains proportional, independent read-only cross-surface
  review; tasks define affected scope and select supported subject
  specialization.
- Project, H2 Python, and H3 resource documentation have distinct writers; H4
  adds a documentation/control writer that also synchronizes agent and chain
  references.
- Project, H2, H3, and H4 each define architecture review variants.
- H2 and H3 each define evidence/VVUQ reviewers, and H2/H3 also use separate
  retained-evidence writers.
- Project, H2, H3, and H4 each define integration-review variants; H4 further
  separates skill/resource review from architecture and integration review.
- H3 and H4 introduce phase-specific control, resource, cutover, and deterministic
  validation writers, including the one-off H2-HC01 Option A correction role.
- Ownership-manifest preflight, writer/read-only separation, checkpoint limits,
  PASS/FAIL reporting, path prohibitions, nonactivation rules, and human
  acceptance boundaries recur across agent records, ownership plans, tasks, and
  control-plane prose.
- Exact commands, validation gates, evidence inventories, resource identities,
  and path lists recur in agent records and phase ownership manifests. Those
  repetitions can drift even when the underlying separation of responsibilities
  remains valid.

Duplication is not itself authority to consolidate or retire a record. Any
migration must first inspect then-current live selectors and preserve required
writer/reviewer independence.

## Authority findings

- The five unprefixed records—`ksdft2effmass-implementation`,
  `ksdft2effmass-tests`, `ksdft2effmass-documentation`,
  `ksdft2effmass-integration-reviewer`, and `ksdft2effmass-architecture`—remain
  the stable current project roles. All five simplifications are complete. Their
  records retain durable capability and boundary definitions while task data
  supplies paths, deliverables, permissions, and any supported subject skill.
- Five stable harness capability roles exist. Three were assigned under exact
  ownership for the completed project-role simplifications without altering
  their durable identities; the harness test and architecture roles remained
  unassigned. The other 24 records whose names start with
  `ksdft2effmass-harness-` remain bound
  to H2, H3, H4,
  H2-HC01,
  TEST-EVIDENCE-SKILL-1, or another closed bounded harness task.
- No phase-specific agent remains selectable under project PI configuration at
  the inspected revision. The H2, H3, and H4 ownership manifests still name
  their agents, but those manifests are retained evidence for phases whose
  authoritative chain is closed with no active task. Closed task text and checksum/shadow/parity records
  are historical mentions, not live launch authority.
- No lifecycle classification remains unresolved on the inspected state. This is
  not a retirement finding: a later activation or newly introduced selector
  would require reclassification before any retirement decision.
- The durable-role column is a capability mapping, not a replacement rule. No
  alias, dispatch change, historical rewrite, or retirement is created by this
  page.

## Existing partial and historical inventories

Several records contain valuable subsets, but none is a complete maintained
current accounting of all 34 agent records:

- `.pi/evidence/pi-harness-incubation/H0/component-inventory.json` is a
  316-component H0 snapshot. Its agent section contains only the five broad
  project roles that existed in that inventory; the 24 later phase-specific
  harness records are absent. Its authority labels describe H0's inspected
  state, not today's lifecycle.
- `.pi/evidence/pi-harness-incubation/H0/capability-matrix.json` groups those same
  five records into the broad `agent_roles` capability. It is a historical
  capability view, not an agent-by-agent current lifecycle register.
- `.pi/evidence/pi-harness-incubation/H1/h3-h2-ownership-plan.json` planned H3,
  H2, and H4 separation, paths, handoffs, and future agent records. It contains
  superseded names for some H4 roles and retains a bounded H2-HC01 state; it is
  not a global current population inventory.
- H4 shadow/parity, traceability, review-closure, and checksum records document
  the specific agents and artifacts used during cutover. They intentionally
  preserve execution history and cannot determine current selection eligibility.
- The H2, H3, and H4 task-specific ownership manifests enumerate only the
  writers and reviewers for one closed phase. Other ownership manifests likewise
  describe their controlling task, not every repository agent.
- `docs/development/agent-control-plane.rst` explains authority, checkpoints,
  role separation, launch preflight, and historical H4 routing. It does not list
  every agent or assign each one a lifecycle and replacement mapping.

These records remain authoritative or evidentiary only for the claims owned by
their respective surfaces. This page supplies the missing maintained human
accounting without changing those records.

## Proposed future machine-readable inventory

A later, separately authorized harness change could create:

```text
harness/local/agent-inventory.json
```

That future local inventory should eventually own:

- stable agent identity;
- domain;
- role;
- access mode;
- lifecycle;
- replacement mapping; and
- live-selection eligibility.

This is only a proposed ownership location. This documentation task does not
create the file, define or accept a schema, modify a resource manifest or
profile, or change harness routing. A future schema decision must also define
how current task/chain selection and retained historical references are resolved
without treating file existence as authorization.

## Navigation

- **Index:** [Harness documentation](ksdft2effmass.harness.000.000.000.md)
- **Parent:** [Current harness architecture](ksdft2effmass.harness.001.000.000.md)
- **Previous:** [Validation and evidence](ksdft2effmass.harness.001.004.000.md)
- **Next:** [Current status and limitations](ksdft2effmass.harness.001.006.000.md)
