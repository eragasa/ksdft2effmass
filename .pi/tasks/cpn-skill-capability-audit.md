# CPN skill-capability audit and bounded hardening

## Status

Closed and human-accepted on 2026-08-03 at 07:45:55 UTC. Six focused correction re-review lanes and final validator/integration spot-checks passed after deterministic corrections. P0 remains unlaunched. No production implementation, scientific test/fixture change, dependency change, external scientific execution, or successor-task launch is authorized by this acceptance.

## Human final acceptance

The human PI accepted the CPN skill-capability audit and bounded existing-skill hardening. Accepted scope includes the complete six-skill inventory and primary classifications, reuse rather than unjustified skill proliferation, 13 prospective review blocks, 12 deterministic tool blocks, pure-guard and external invocation boundaries, separated evidence/review/verification/acceptance authority, retry and correlation semantics, bounded skill-contract hardening, and the documented evidence-ID migration debt.

The 22 currently unowned tests do not block this audit's acceptance. Strict evidence-ID completion remains a separate bounded migration task. Runtime enforcement of skill invocation/result schemas remains prospective and belongs to later, separately launched CPN implementation. The acceptance explicitly does not launch P0 or any other task.

## Objective

Inventory every repository-local skill, classify its CPN suitability, map existing skills and deterministic tools to prospective testing/review blocks, harden unambiguous existing contracts, document one prospective testing subnet, and determine whether a genuine new-skill gap exists.

## Scope

Authorized:

- inspect all skills under `.pi/skills/` and `.agents/skills/` and their actual consumers;
- record a machine-readable capability inventory and concise Markdown explanation;
- clarify the external two-phase skill invocation/result boundary and evidence authority;
- harden existing triggers, inputs, outputs, side effects, failures, retry/idempotency, authorization, and stop conditions where accepted policy determines the correction;
- add and execute deterministic scripts for observed repeated skill-inventory and evidence-ID audits;
- correct the checkpoint validator to enforce its authoritative Draft 2020-12 schema;
- correct obsolete agent routing that conflicts with the completed VVUQ migration or current decision classes;
- request focused read-only reviews and apply deterministic findings.

Excluded:

- launching P0 or any P0–P11 implementation task;
- SNAKES installation or CPN runtime implementation;
- production Python/Rust source or maintained test/fixture changes;
- dependency or lockfile changes;
- QE, ABINIT, Wannier90, scheduler, MPI, or external scientific execution;
- scientific-result changes;
- creating a new skill absent a demonstrated gap and required human checkpoint.

## Inventory result

Six repository-local skills exist:

1. `.agents/skills/graphify/SKILL.md`;
2. `.agents/skills/resolve-human-checkpoint/SKILL.md`;
3. `.pi/skills/choose-next-task/SKILL.md`;
4. `.pi/skills/design-data-action-objects/SKILL.md`;
5. `.pi/skills/develop-operator-records/SKILL.md`;
6. `.pi/skills/document-research-python/SKILL.md`.

Each has exactly one primary classification in `.pi/skills/skill-capability-inventory.json`. Project agents are consumers/executors rather than additional skills. Deterministic commands are tool capabilities rather than AI skills.

## Artifacts

- `.pi/skills/skill-capability-inventory.json` — machine-readable inventory, token responsibilities, block mappings, deterministic tool inventory, subnet, and gap decision;
- `.pi/skills/validate_skill_capabilities.py` — exact skill existence/frontmatter/hash/classification/owner validator;
- `.pi/skills/audit_evidence_identifiers.py` — evidence-owner uniqueness/class/hierarchy/marker audit with strict mode;
- `docs/architecture/cpn-skill-capability-audit.md` — concise architecture explanation;
- bounded hardening edits to existing skills, checkpoint validator, test-agent ownership, and integration-review escalation policy.

## Deterministic findings and corrections

- `SKILL-001`: Graphify's generic trigger and install/external-processing runbook conflicted with repository optional/no-external policy. Correction: narrow the project trigger and add a prominent repository override; do not install or use external processing.
- `SKILL-002`: reusable review/document/operator skills lacked invocation/result, mutation, failure, retry, idempotency, and stop contracts. Correction: add profile-specific CPN-compatible boundaries without making skills guards or acceptance authorities.
- `SKILL-003`: checkpoint trigger wording was broader than its two-condition body, and replay/partial-failure behavior was absent. Correction: narrow the trigger and add expected-state, replay, conflict, partial-write, and separate-resumption rules.
- `SKILL-004`: checkpoint validation manually checked only part of the authoritative schema. Correction: use `Draft202012Validator`, validate the schema, and add negative dry-run probes.
- `SKILL-005`: the test agent retained obsolete transitional-layout ownership after migration completion. Correction: remove transitional ownership and prohibit recreation.
- `SKILL-006`: the integration reviewer automatically routed material findings to a historical checkpoint. Correction: use current deterministic/standing/human decision classes.
- `SKILL-007`: repeated evidence-ID audits had no deterministic owner. Correction: add an AST/docstring ownership audit. It expands the existing parametrized range to find 315 owned IDs, 22 unowned test functions, and zero duplicate/prefix/marker errors. Strict mode rejects the current 22-test gap; tests are not changed by this task.
- `SKILL-008`: successful result tokens lacked request/task/parent/attempt correlation and retries lacked explicit authorization. Correction: add correlated identities to success/failure contracts and require immutable parent authorization or a request's pre-authorized retry policy.
- `SKILL-009`: a nominally read-only Graphify consumer could inherit vocabulary, saved-result, and reflection writes. Correction: define a non-writing existing-graph query profile and require `choose-next-task` to use it or stop blocked.
- `SKILL-010`: an operator reference retained one obsolete technical-integration path and bare checkpoint affirmation excluded `blocked` records. Correction: use the maintained software-verification integration subtree and the shared unresolved-state definition.
- `SKILL-011`: the inventory validator under-enforced tool names, nested token/block fields, consumers/references, duplicates, and gap-analysis fields. Correction: enforce exact block sets, required nested fields, concrete paths/references, hashes, and composability residuals.
- `SKILL-012`: the documentation synchronization review and human-acceptance token were referenced but uncatalogued. Correction: add their owners and immutable responsibility fields.
- `SKILL-013`: the evidence audit counted only endpoints of one declared range and used textual marker matching. Correction: expand a normalized inclusive range, reject ambiguous multiple declarations, inspect executable AST markers, and add parser self-tests.
- `SKILL-014`: the synthetic checkpoint resolver accepted contradictory statements and dry-run labels could conflict with exit status. Correction: require unambiguous Option-B approval, reject negative/Option-A responses, and compute each stage label from its errors.
- `SKILL-015`: the declared checkpoint schema does not encode every plausible lifecycle invariant. Resolution: preserve the authoritative schema in this bounded task, narrow the evidence claim to complete enforcement of its currently declared constraints, and defer schema-semantic additions for separate human review.

## New-skill decision

No new skill is justified or created. Existing ownership is sufficient; remaining gaps are deterministic evidence drift, future harness enforcement, subsystem-specific dependency tooling, and deferred P0 agent routing. Creating a CPN or generic validation skill now would duplicate existing responsibilities and broaden triggers before a real launched consumer exists.

## Evidence boundary

Deterministic tool results may satisfy software gates when command, environment, and artifacts are recorded. Skill/agent reviews produce findings. Parent verification checks completeness. Human acceptance alone authorizes protected decisions. No review or collection of reviews establishes numerical convergence, scientific validation, UQ, physical correctness, expensive-run authorization, or final acceptance.

## Validation requirements

- exact six-skill filesystem/frontmatter/hash inventory;
- exactly one primary classification per skill;
- all requested review and deterministic tool blocks have owners;
- complete token responsibilities and external two-phase boundary;
- complete enforcement of the currently declared checkpoint JSON Schema and dry-run validation;
- evidence-ID audit default pass and strict expected rejection of the recorded 22-test gap;
- Markdown links/navigation and Sphinx warnings-as-errors;
- no production source/test/fixture/dependency/lock/generated-output changes;
- P0 and deferred ABINIT/hybrid work remain inactive;
- `git diff --check`;
- six focused read-only review lanes and parent verification.

## Validation and review result

- skill inventory: 6 filesystem/6 records, 13 review blocks, 12 deterministic tool blocks, 0 errors;
- malformed inventory probes: omitted fields plus five nested wrong-type/duplicate/extra cases all rejected;
- checkpoint validation: 5 records, all four dry-run stages passed, 0 unresolved, 0 duplicate decisions;
- evidence audit: self-test passed, 59 modules, 332 tests, 315 owned identifiers, 22 unowned tests, 0 structural errors;
- strict evidence audit: expected exit 1; the 22-test gap remains an unsatisfied gate;
- focused dependency/schema/fixture pytest: 29 passed;
- Ruff format/lint on the three control-plane scripts: passed;
- Sphinx 9.1.0 warnings-as-errors build: passed in removed temporary output;
- `git diff --check` and prohibited/generated-path scans: passed;
- six focused correction re-review lanes: architecture, contracts, inventory, deterministic tools, documentation, and integration passed after one nested-validator correction;
- final independent validator and integration spot-checks: passed.

No software-verification result above is scientific validation or UQ.

## Completion boundary

Completion of this audit establishes only a versioned skill/control-plane inventory, bounded contract hardening, and deterministic control-plane evidence. It does not implement skill invocation tokens, a harness result schema, the prospective subnet, SNAKES integration, or production testing workflows.
