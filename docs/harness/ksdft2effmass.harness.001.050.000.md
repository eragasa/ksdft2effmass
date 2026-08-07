---
document_id: ksdft2effmass.harness.001.050.000
task_id: harness-current.agents
parent: ksdft2effmass.harness.001.000.000
status: current
sphinx: excluded
---

# Agent and ownership inventory

This page accounts for the complete candidate population under `.pi/agents/` at
development revision `82b2f52912325c732dad8f88cdc90a22a4f7736f`. The revision
matched `origin/dev` when inspected. The inventory describes records; it does not
activate, retire, rename, or grant ownership to an agent. Current authority still
comes from the applicable human instruction, durable decisions, accepted
contracts, task and chain state, and any required validated ownership manifest.
An agent file's existence establishes availability to the harness, not authority
to act.

## Classification method

Each agent record was read in full. References were then checked across current
tasks, chains, checkpoints, ownership controls, retained harness-incubation
evidence, generic and local harness resources, the maintained control-plane
documentation, and this harness hierarchy. In the table:

- **Live** means a current, non-historical selection or assignment. No active
  task currently selects any phase-specific agent.
- **Historical** means a reference retained by a closed task, a closed chain, a
  resolved checkpoint, a superseded plan, a checksum catalog, or retained
  execution/review evidence.
- **Durable** identifies a broad current project role whose record is not limited
  to one named phase. It does not mean that the role is always authorized.
- A proposed durable role is a consolidation suggestion only. It is not an
  accepted replacement, alias, migration, or live-selection rule.

The harness-incubation chain reports H0, H1, H3, H2, and H4 closed and
human-accepted, with `active_task: null`; H5 is inactive. Every other current
chain also reports no active task. All repository checkpoint records are resolved
or superseded. Those facts are why the phase-bound records below are historical
references rather than live phase assignments.

## Complete agent inventory

| Agent | Domain | Role | Access | Original phase | Current references | Lifecycle | Proposed durable role |
|---|---|---|---|---|---|---|---|
| [ksdft2effmass-architecture](../../.pi/agents/ksdft2effmass-architecture.md) | project | architecture | read-only | OperatorRecord architecture; later backend-neutral CPN and Rust/control-plane review | Live: broad current agent record, selected only by a future authorized task. Historical: closed operator-record chains and H0 inventory. | durable | ksdft2effmass-architecture |
| [ksdft2effmass-documentation](../../.pi/agents/ksdft2effmass-documentation.md) | project | documentation | writer | OperatorRecord documentation; later CPN, schemas, Sphinx, and evidence documentation | Live: broad current agent record, selected only by a future authorized task. Historical: closed operator-record chains and H0/H4 evidence. | durable | ksdft2effmass-documentation |
| [ksdft2effmass-harness-cutover-architecture-reviewer](../../.pi/agents/ksdft2effmass-harness-cutover-architecture-reviewer.md) | cross-domain | architecture | read-only | H4 generic/local dependency direction and rollback-safe routing | Live: none. Historical: closed H4 ownership, shadow/parity records, review closure, and checksums. | historical-reference-only | ksdft2effmass-harness-architecture |
| [ksdft2effmass-harness-cutover-integration-reviewer](../../.pi/agents/ksdft2effmass-harness-cutover-integration-reviewer.md) | cross-domain | integration-review | read-only | H4 parity, packaging, cutover, rollback, and integration safety | Live: none. Historical: closed H4 ownership, correction/closeout, shadow/parity, review closure, and checksums. | historical-reference-only | ksdft2effmass-harness-integration-reviewer |
| [ksdft2effmass-harness-cutover-skill-resource-reviewer](../../.pi/agents/ksdft2effmass-harness-cutover-skill-resource-reviewer.md) | cross-domain | integration-review | read-only | H4 canonical skill/resource identity and compatibility | Live: none. Historical: closed H4 ownership/review evidence and closed `ARCHITECTURE-DECISION-SKILL-1`. | historical-reference-only | ksdft2effmass-harness-integration-reviewer |
| [ksdft2effmass-harness-generic-resource-writer](../../.pi/agents/ksdft2effmass-harness-generic-resource-writer.md) | harness-generic | resource-writing | writer | H3 generic manifests, schemas, and skills | Live: none. Historical: accepted H1 ownership plan and closed H3 ownership/checksums. | historical-reference-only | ksdft2effmass-harness-implementation |
| [ksdft2effmass-harness-h2-verification-evidence-writer](../../.pi/agents/ksdft2effmass-harness-h2-verification-evidence-writer.md) | harness-generic | evidence-writing | writer | H2 retained software-verification and handoff evidence | Live: none. Historical: accepted H1 ownership plan and closed H2 ownership/checksums. | historical-reference-only | ksdft2effmass-harness-tests |
| [ksdft2effmass-harness-h3-verification-evidence-writer](../../.pi/agents/ksdft2effmass-harness-h3-verification-evidence-writer.md) | cross-domain | evidence-writing | writer | H3 generic/local resource verification and H3-to-H2 handoff evidence | Live: none. Historical: accepted H1 ownership plan and closed H3 ownership/checksums. | historical-reference-only | ksdft2effmass-harness-tests |
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
| [ksdft2effmass-harness-resource-architecture-reviewer](../../.pi/agents/ksdft2effmass-harness-resource-architecture-reviewer.md) | cross-domain | architecture | read-only | H3 generic/local resource architecture and intended Rust portability | Live: none. Historical: closed H3 ownership/checksums. | historical-reference-only | ksdft2effmass-harness-architecture |
| [ksdft2effmass-harness-resource-documentation-writer](../../.pi/agents/ksdft2effmass-harness-resource-documentation-writer.md) | cross-domain | documentation | writer | H3 generic and local resource documentation | Live: none. Historical: accepted H1 plan and closed H3 ownership/checksums. | historical-reference-only | ksdft2effmass-harness-documentation |
| [ksdft2effmass-harness-resource-evidence-vvuq-reviewer](../../.pi/agents/ksdft2effmass-harness-resource-evidence-vvuq-reviewer.md) | cross-domain | validation | read-only | H3 fixtures, independent oracles, evidence, and VVUQ boundaries | Live: none. Historical: closed H3 ownership/checksums. | historical-reference-only | ksdft2effmass-harness-tests |
| [ksdft2effmass-harness-resource-integration-reviewer](../../.pi/agents/ksdft2effmass-harness-resource-integration-reviewer.md) | cross-domain | integration-review | read-only | H3 validation, leakage, documentation, control-plane, and handoff | Live: none. Historical: closed H3 ownership/checksums. | historical-reference-only | ksdft2effmass-harness-integration-reviewer |
| [ksdft2effmass-harness-resource-test-writer](../../.pi/agents/ksdft2effmass-harness-resource-test-writer.md) | cross-domain | tests | writer | H3 generic and local textual fixtures | Live: none. Historical: accepted H1 plan and closed H3 ownership/checksums. | historical-reference-only | ksdft2effmass-harness-tests |
| [ksdft2effmass-harness-resource-validation-writer](../../.pi/agents/ksdft2effmass-harness-resource-validation-writer.md) | harness-generic | validation | writer | H3 deterministic textual-resource completion validation | Live: none. Historical: accepted H1 plan and closed H3 ownership/checksums. | historical-reference-only | ksdft2effmass-harness-tests |
| [ksdft2effmass-harness-skill-resource-cutover-writer](../../.pi/agents/ksdft2effmass-harness-skill-resource-cutover-writer.md) | cross-domain | resource-writing | writer | H4/TEST-EVIDENCE-SKILL-1 live skill/resource cutover; later architecture-decision skill resources | Live: none. Historical: closed H4 ownership and closed `ARCHITECTURE-DECISION-SKILL-1`. | historical-reference-only | ksdft2effmass-harness-implementation |
| [ksdft2effmass-implementation](../../.pi/agents/ksdft2effmass-implementation.md) | project | implementation | writer | OperatorRecord production source; later backend-neutral CPN contracts/source | Live: broad current agent record, selected only by a future authorized task. Historical: closed operator-record chains and H0/H4 evidence. | durable | ksdft2effmass-implementation |
| [ksdft2effmass-integration-reviewer](../../.pi/agents/ksdft2effmass-integration-reviewer.md) | project | integration-review | read-only | OperatorRecord final integration; later CPN, evidence, documentation, and control-plane review | Live: broad current agent record, selected only by a future authorized task. Historical: closed operator-record tasks/chains, H0/H1/H4 evidence, and inactive future task mentions. | durable | ksdft2effmass-integration-reviewer |
| [ksdft2effmass-tests](../../.pi/agents/ksdft2effmass-tests.md) | project | tests | writer | OperatorRecord tests; later backend-neutral CPN, repository-wide test evidence, and harness-package tests | Live: broad current agent record, selected only by a future authorized task. Historical: closed operator-record chains and H0/H4 evidence. | durable | ksdft2effmass-tests |

## Population totals

The totals below are derived by counting the rows in the complete inventory.
“Durable harness roles” counts current stable harness records, not proposed target
names.

| Category | Count |
|---|---:|
| Total agent records | 29 |
| Durable project roles | 5 |
| Durable harness roles | 0 |
| Phase-specific live roles | 0 |
| Historical-reference-only roles | 24 |
| Unresolved roles | 0 |

### Totals by domain

| Domain | Count |
|---|---:|
| project | 5 |
| harness-generic | 9 |
| harness-local | 3 |
| cross-domain | 12 |

### Totals by role

| Role | Count |
|---|---:|
| implementation | 3 |
| tests | 4 |
| documentation | 3 |
| integration-review | 5 |
| architecture | 4 |
| resource-writing | 4 |
| validation | 3 |
| control-writing | 1 |
| evidence-writing | 2 |
| other | 0 |

### Totals by access

| Access | Count |
|---|---:|
| writer | 18 |
| read-only | 11 |

### Totals by lifecycle

| Lifecycle | Count |
|---|---:|
| durable | 5 |
| phase-specific-live | 0 |
| historical-reference-only | 24 |
| unresolved | 0 |

## Proposed durable target sets

The proposed project set is:

```text
ksdft2effmass-implementation
ksdft2effmass-tests
ksdft2effmass-documentation
ksdft2effmass-integration-reviewer
ksdft2effmass-architecture
```

All five names already have broad current project records. Their presence does
not bypass task selection, path ownership, checkpoint, review, or human-authority
controls.

The proposed harness set is:

```text
ksdft2effmass-harness-implementation
ksdft2effmass-harness-tests
ksdft2effmass-harness-documentation
ksdft2effmass-harness-integration-reviewer
ksdft2effmass-harness-architecture
```

None of these five harness identities currently exists as an agent record. The
row-level mappings show how phase-specific responsibilities could be grouped if
a later authorized migration accepts that design. Architecture roles in both
sets are optional specialists for material architecture decisions; they are not
mandatory participants in routine work.

## Duplication findings

The 24 harness phase records repeat useful separation-of-duty rules, but encode
phase and path assignments in agent identities rather than supplying them only
through task-scoped ownership:

- H2 and H4 each have separate implementation writers, while H3 divides resource
  implementation among generic, local, fixture, validator, documentation, and
  retained-evidence writers.
- Project, H2 Python, H3 resource, and H4 local-parity test responsibilities are
  described in separate writers, with evidence grammar and completion-gate
  mechanics repeated.
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
  `ksdft2effmass-integration-reviewer`, and `ksdft2effmass-architecture`—appear
  to be the stable current project roles. Their broad records remain subject to
  task-specific authorization.
- No stable current harness role already exists. Every current agent whose name
  starts with `ksdft2effmass-harness-` is explicitly bound to H2, H3, H4,
  H2-HC01, TEST-EVIDENCE-SKILL-1, or another closed bounded harness task.
- No phase-specific agent remains selected by live configuration at the inspected
  revision. The H2, H3, and H4 ownership manifests still name their agents, but
  those manifests are retained evidence for phases whose authoritative chain is
  closed with no active task. Closed task text and checksum/shadow/parity records
  are historical mentions, not live launch authority.
- No lifecycle classification remains unresolved on the inspected state. This is
  not a retirement finding: a later activation or newly introduced selector
  would require reclassification before any retirement decision.
- The proposed replacement column is non-authoritative. No replacement agent,
  alias, dispatch rule, or migration has been created or accepted by this page.

## Existing partial and historical inventories

Several records contain valuable subsets, but none is a complete maintained
current accounting of all 29 agent records:

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
