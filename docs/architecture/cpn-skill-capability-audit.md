# CPN skill-capability audit

## Status and scope

This bounded control-plane audit and existing-skill hardening were human-accepted
on 2026-08-03 at 07:45:55 UTC. The accepted scope inventories repository-local
skills for reuse in prospective Colored Petri Net (CPN) testing, review, and
evidence-production subnets. The 22 currently unowned tests remain a separate
bounded evidence-ID migration task and do not block this audit's acceptance.
Runtime skill invocation/result-schema enforcement remains prospective.

This acceptance does not implement a CPN, launch P0 or another task, install
SNAKES, create production source or tests, add dependencies, or execute QE,
ABINIT, or Wannier90.

The machine-readable authority for the inventory and block mapping is
[`.pi/skills/skill-capability-inventory.json`](../../.pi/skills/skill-capability-inventory.json).
The deterministic validator is
[`.pi/skills/validate_skill_capabilities.py`](../../.pi/skills/validate_skill_capabilities.py).
This page explains the results without duplicating complete `SKILL.md` content.

## Execution boundary

A skill is an instruction/capability bundle applied by an external agent or
harness. It is not a CPN guard or transition.

```text
skill_capability_available
    +
test_or_review_requested
    -> request_skill_invocation
    -> skill_invocation_requested

external agent/harness outside guard evaluation:
    applies the selected skill to immutable inputs

skill_invocation_requested
    +
skill_invocation_result_received
    -> validate_skill_result
    -> evidence_accepted | evidence_rejected | review_findings_recorded
```

Guards inspect immutable token fields only. They never invoke an agent, load a
skill, edit files, run a command, or make a scientific judgment. Retries require
an immutable parent authorization identity or a request's pre-authorized retry
policy, create a new attempt identity, and retain previous failures and findings.

## Actual repository inventory

The maintained source of truth for the live skill inventory is
`.pi/skills/skill-capability-inventory.json`, checked against the eight canonical
filesystem skills. Task, checkpoint, and chain records are authoritative for
execution state, but are not skill-inventory inputs; retaining mutable snapshots
of them in the capability inventory would make that inventory stale.

| Skill | Path | Primary CPN suitability | Main current consumers |
|---|---|---|---|
| `design-data-action-objects` | `.pi/skills/design-data-action-objects/SKILL.md` | `COMPOSABLE_AFTER_HARDENING` | project design and implementation agents |
| `develop-architecture-decision` | `.pi/skills/develop-architecture-decision/SKILL.md` | `HUMAN_DECISION_SUPPORT` | `.pi/tasks/develop-architecture-decision-skill.md` |
| `develop-operator-records` | `.pi/skills/develop-operator-records/SKILL.md` | `COMPOSABLE_AFTER_HARDENING` | project operator agents and closed operator workflows |
| `develop-python-test-evidence` | `.pi/skills/develop-python-test-evidence/SKILL.md` | `COMPOSABLE_AFTER_HARDENING` | test writers and integration/evidence reviewers |
| `document-python-research-software` | `.pi/skills/document-python-research-software/SKILL.md` | `COMPOSABLE_AFTER_HARDENING` | documentation and integration-review agents |
| `graphify` | `.agents/skills/graphify/SKILL.md` | `ADVISORY_REVIEW_ONLY` | explicit human-requested local Graphify use only |
| `recommend-next-task` | `.pi/skills/recommend-next-task/SKILL.md` | `HUMAN_DECISION_SUPPORT` | parent planning transitions |
| `resolve-human-checkpoint` | `.agents/skills/resolve-human-checkpoint/SKILL.md` | `HUMAN_DECISION_SUPPORT` | parent checkpoint routing and `recommend-next-task` handoff |

The H4 renames from `choose-next-task` and `document-research-python` correct
identity without expanding capability. Those old names remain traceable in H4
migration evidence and historical records, not as live aliases. No duplicate
canonical name or obsolete `use-graphify` skill exists. Project agents under
`.pi/agents/` are consumers/executors, not additional skills. Deterministic
commands and scripts are tool capabilities, not skills.

### Why some skills remain `COMPOSABLE_AFTER_HARDENING`

The architecture, operator, test-evidence, and documentation skills now define invocation
profiles, immutable inputs, result fields, mutation boundaries, structured
failures, retry behavior, idempotency, deterministic-command authority, and stop
conditions. They still need a future harness to enforce correlation and expected
result schemas. Operator evidence
also has a current strict evidence-identifier gap described below. These facts
prevent an unqualified directly-composable classification.

### Advisory and human-decision boundaries

Graphify produces optional derived navigation evidence only. It cannot approve
architecture, establish repository state, or become a scientific oracle.
`recommend-next-task` recommends one task and stops for human selection.
`resolve-human-checkpoint` records an already supplied human decision; the skill
does not create acceptance authority.

No existing skill is classified `NOT_CPN_SUITABLE` or `DEFERRED`. This does not
mean every operation exposed by a skill is authorized. Graphify remote,
installation, hook, server, clone/fetch/push, and semantic-processing operations
remain prohibited without separate explicit human approval.

## Bounded hardening applied

### Shared invocation contracts

The DataObject/ActionObject, operator-record, documentation, next-task, and
checkpoint skills now state:

- required task, workflow, attempt, artifact, reference, and authorization
  inputs;
- review-only versus authorized writer profiles where relevant;
- structured result fields;
- permitted and forbidden mutation scope;
- deterministic command/result authority;
- failure, retry, replay, and idempotency behavior;
- exact stop conditions;
- no automatic successor launch or acceptance.

### Graphify

The project Graphify trigger now requires an explicit human request for
Graphify; broad topology, dependency, impact, navigation, and next-task questions
are not automatic triggers. The skill invokes only the validated local Graphify
0.9.2 executable at `$HOME/.local/bin/graphify` and blocks when that exact
location is unavailable or mismatched. It does not auto-install, upgrade,
discover fallbacks, rebuild after edits, select semantic backends, or dispatch
semantic extraction. Commands receive a sanitized environment that removes
known backend keys, confines output to `graphify-out/`, and disables Graphify's
query log. Read-only operations prohibit vocabulary, result, lesson, and other
generated-state writes.

### Checkpoint handling

The checkpoint trigger now matches its body: both an unresolved record and an
unambiguous current human answer are required. Expected-state comparison,
idempotent replay, conflict handling, partial-write reporting, and separate
resumption authority are explicit.

`.pi/checkpoints/validate_checkpoints.py` now executes the complete declared
Draft 2020-12 JSON Schema through `jsonschema`, including
`additionalProperties`, option structure, types, enums, and resolved-record
conditional constraints. Its dry run includes negative additional-property,
option-shape, contradictory-response, resolution, resumption, and deterministic-
correction probes. This establishes complete enforcement of the currently
declared schema, not lifecycle semantics absent from that schema. Adding option-
identity uniqueness, timestamp formats, or stronger status conditionals changes
an authoritative control-plane schema and is deferred for separate human review.

### Agent routing

The operator test agent no longer owns or accepts the completed transitional test
layout. The integration reviewer routes findings through the current decision
classes instead of automatically reopening a historical checkpoint.

Prospective P0 and later CPN implementation/test ownership remains intentionally
unassigned. Before any separately authorized P0 launch, the task must name
bounded owners; operator-only implementation/test agents are not default CPN
production owners.

## Skill-to-block mapping

Architectural review blocks produce finding sets unless paired with a
deterministic tool result. They do not independently satisfy final acceptance.

| Responsibility | Existing owner | Result authority |
|---|---|---|
| `ArchitectureContractReviewBlock` | `design-data-action-objects` + architecture agent | advisory findings |
| `SourceDocumentationReviewBlock` | `document-python-research-software` + documentation/integration agent | advisory findings |
| `TestDocumentationReviewBlock` | `develop-python-test-evidence` + test/integration agent | advisory findings |
| `VVUQClassificationReviewBlock` | `develop-python-test-evidence` + test/integration agent | advisory evidence classification |
| `PublicApiInventoryReviewBlock` | operator skill + deterministic `__all__`/test inventory | mixed review/tool evidence |
| `StaticDependencyDirectionReviewBlock` | focused dependency-direction pytest + architecture/integration review | deterministic topology result plus findings |
| `SchemaFixtureReviewBlock` | focused schema/fixture pytest + operator review | deterministic software evidence plus findings |
| `NumericalEvidenceReviewBlock` | marked numerical pytest + `develop-python-test-evidence` semantic review | bounded numerical verification plus findings |
| `IntegrationReviewBlock` | project integration reviewer applying audited skills | advisory parent input |
| `StalePathReviewBlock` | deterministic inventory/search + integration review; Graphify only when explicitly human-requested | software/control-plane evidence plus findings |
| `CheckpointReviewBlock` | checkpoint skill + checkpoint validator | human decision record plus deterministic schema result |
| `TaskSelectionReviewBlock` | `recommend-next-task` | advisory recommendation; human selection required |
| `DocumentationSynchronizationReviewBlock` | documentation skill + documentation/integration reviewer | advisory synchronization findings; deterministic Sphinx/link evidence remains separate |

## Deterministic tool blocks

The authoritative pass/fail owner is the command and recorded environment, not an
agent's interpretation.

| Block | Deterministic owner |
|---|---|
| `PytestBlock` | configured pytest command and marked tests |
| `RuffFormatBlock` | Ruff format check |
| `RuffLintBlock` | Ruff lint check |
| `MypyBlock` | configured mypy run |
| `SphinxWarningsAsErrorsBlock` | Sphinx `-W` build to a temporary output directory |
| `JsonSchemaValidationBlock` | focused schema/fixture pytest using Draft 2020-12 validation |
| `ChecksumValidationBlock` | SHA-256 command with expected digest and artifact identity |
| `GitDiffCheckBlock` | `git diff --check` |
| `EvidenceIdentifierAuditBlock` | `.pi/skills/audit_evidence_identifiers.py --self-test --strict` |
| `CheckpointSchemaValidationBlock` | `.pi/checkpoints/validate_checkpoints.py --include-fixtures --dry-run` |
| `StaticDependencyDirectionToolBlock` | focused operator comparison dependency-direction pytest |
| `SkillCapabilityInventoryValidationBlock` | `.pi/skills/validate_skill_capabilities.py` |

Ruff, mypy, pytest, and Sphinx already have established configuration. The schema,
fixture, and operator dependency-direction tests already own their narrow
executable evidence. A general AI skill must not replace them.

## Evidence-identifier deterministic finding

Repeated historical evidence-ID audits had no reusable deterministic owner.
`.pi/skills/audit_evidence_identifiers.py` now distinguishes a test function's
first-line owner declaration from cross-references elsewhere in prose. It checks
executable-owner uniqueness, expands one normalized inclusive range used by a
parametrized test, rejects ambiguous multiple declarations, and checks evidence-
class prefix/hierarchy agreement, syntax, and executable AST module markers. A
built-in deterministic self-test exercises the range and marker parsers.

The non-strict audit currently reports:

```text
evidence_modules=59
test_functions=332
owned_evidence_identifiers=315
unowned_test_functions=22
audit_errors=0
```

The 22 unowned tests are limited to the maintained
`OperatorRecordDifferenceResult` facets and `OperatorRecordDifferencer` module.
Strict mode correctly fails on this current gap. This task does not edit tests;
resolving the gap requires a separately authorized bounded test-documentation
task. The finding is software-evidence inventory drift, not evidence that the
assertions fail and not scientific validation.

## Capability tokens

Prospective immutable responsibilities are:

- `SkillIdentityToken`: stable name, path, and content SHA-256;
- `SkillCapabilityToken`: capability, invocation-contract version, references,
  side-effect class, authorization, and validation status;
- `SkillInvocationRequestToken`: request/capability, task/attempt, immutable
  artifacts, output schema, evidence class, mutation scope, termination policy,
  parent workflow, and immutable retry authorization identity or policy;
- `SkillInvocationResultToken`: correlated request/task/parent/attempt,
  skill/input/output identities, findings, commands/results, mutations, warnings,
  failure class, and completion status;
- `SkillInvocationFailureToken`: correlated request/task/parent/attempt, retry
  authorization/eligibility, partial effects, and retained findings;
- `SkillReviewFindingSetToken`: scoped finding IDs, severity, evidence, and
  recommendations;
- `DeterministicToolResultToken`: tool/version/environment, exact command,
  artifacts, exit status, and output references;
- `ParentVerificationToken`: required/received evidence inventory, missing or
  rejected evidence, scope, and status;
- `HumanAcceptanceResultToken`: correlated request/task, preserved human response,
  normalized decision, authorized scope, record paths, and status.

Durable scientific evidence stores structured results and artifact references,
not hidden chain-of-thought or unrestricted conversation transcripts.

## Evidence authority

```text
Deterministic verification result
    may satisfy a software gate only with command, environment, and artifacts

Agent review result
    produces findings and recommendations

Parent verification result
    checks evidence completeness and consistency

Human acceptance result
    authorizes protected scientific, architectural, public-contract, resource,
    and execution decisions
```

No skill or collection of agreeing agents establishes numerical convergence,
scientific validation, UQ, physical correctness, expensive-run authorization, or
final acceptance.

## Prospective testing subnet

This is an architectural composition, not a SNAKES implementation:

```text
implementation_artifacts_ready
    -> request_static_verification
    -> static_verification_requested

static_verification_requested
    ├── RuffFormatBlock
    ├── RuffLintBlock
    ├── MypyBlock
    └── StaticDependencyDirectionToolBlock

static_results_complete
    -> request_test_verification
    -> test_verification_requested

test_verification_requested
    ├── PytestBlock
    ├── EvidenceIdentifierAuditBlock
    └── external VVUQClassificationReviewBlock

test_results_complete
    -> request_documentation_verification
    -> documentation_verification_requested

documentation_verification_requested
    ├── SphinxWarningsAsErrorsBlock
    ├── external SourceDocumentationReviewBlock
    └── external DocumentationSynchronizationReviewBlock

all_required_evidence_present
    -> request_integration_review
    -> integration_review_requested

external reviewer:
    integration_review_result_received
    -> review_findings_recorded

required deterministic results + review findings
    -> parent_verification_requested
    -> parent_verification_passed | parent_verification_failed

parent_verification_passed
    -> human_acceptance_requested
```

Deterministic checks may run in parallel. A missing or nonzero required result
blocks the join. Reviews run outside guards and may record blocking findings.
After correction, new artifact and attempt identities are used; prior failures
remain durable. Parent verification checks completeness but cannot grant human
acceptance.

## New-skill gap analysis

No genuine AI-skill gap justifies a new skill now.

Existing skills and agents already cover architecture ownership, operator
contracts, documentation, integration review, advisory topology, checkpoint
handling, and task-selection support. The observed gaps were existing trigger,
contract, routing, and deterministic-tool ownership defects. Extending current
owners avoids overlapping triggers and generic workflow skills.

Remaining gaps are not new-skill gaps:

- strict evidence-ID ownership has 22 unowned tests;
- dependency-direction tooling is intentionally operator-subsystem-specific;
- result-schema enforcement requires a future harness/runtime contract;
- P0 implementation/test agent ownership must be selected only if P0 is later
  explicitly launched.

No `run-science`, `validate-everything`, `manage-workflow`, `review-code`, or CPN
implementation skill is proposed or created.
