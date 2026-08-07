# ARCHITECTURE-DECISION-SKILL-1 — develop-architecture-decision harness resource

Status: pending final human acceptance at `ARCHITECTURE-DECISION-SKILL-1-HC01` from starting revision `3927d41b93e6be480e9c29013984b9385808ad4c`

## Authority and boundary

The current human instruction authorizes this bounded one-writer harness resource task. It creates and activates the read-only `develop-architecture-decision` skill, canonical/reference/descriptor resources, byte-identical live resources, controlled H6-only fixtures and validator, generic/local manifest and profile synchronization, eight-skill inventory/validation, current local replay, selected local route, maintained harness documentation, and task evidence.

Writer: `ksdft2effmass-harness-skill-resource-cutover-writer`. Sole independent reviewer: `ksdft2effmass-harness-cutover-skill-resource-reviewer`.

No `.pi/agents/`, real H6 work, dispatch, ownership semantics, P2/P3/H5 surfaces, production/project tests or schemas, dependencies, locks, SQLite, replay redesign, execution/release, historical catalogs, final checkpoint, commit, or push may be changed. Canonical generic resources remain authoritative; local depends on generic and live resources are synchronized from canonical. The selected route remains `local`.

## Required behavior

The skill is read-only decision support. It reconstructs repository and durable state; separates facts, inferences, human choices, implementation consequences, and deferred questions; and proceeds only with exactly three materially distinct defensible A/B/C architectures across authority, ownership/dependency, state, persistence, dispatch, history, migration, and runtime. Status quo is permitted only if defensible; configuration variants are prohibited.

If three options are unavailable, it classifies the request as deterministic, underspecified, or unsuitable, identifies missing or controlling information, and stops without a checkpoint. Applicable output uses the exact required headings, compares common criteria, recommends exactly one option while preserving three, proposes actual summarized A/B/C choices plus D reconsider/defer, cites the document, and stops before selection or implementation. CPN request/result/retry/idempotency boundaries apply. No duplicated analysis or VVUQ overclaim is allowed.

## Implementation and review result

The canonical/local/live skill resources, descriptor, one direct conventions reference, controlled fixtures, deterministic validators, profile/manifests, eight-skill inventory, selected local route, and maintained documentation are complete. Three applicable and five non-applicable controlled cases pass. The sole reviewer reported one Medium inventory/documentation synchronization finding; the sole writer corrected it in the one permitted consolidated pass, and final deterministic validation passes. The skill has not been invoked, H6 has not been initialized, and no successor has been activated.

## Completion gates

Run ownership preflight with the task-specific chain:

```text
python .pi/task-ownership/validate_task_ownership.py --task ARCHITECTURE-DECISION-SKILL-1 --chain .pi/chains/develop-architecture-decision-skill.chain.json
```

Then run task completion, current H3 resource validation, eight-skill capability validation, selected local route, controlled architecture cases, JSON/link checks, and diff/protected-nonmutation checks. Reviewer gate is required after deterministic completion. One consolidated correction pass is permitted after that review. Final output is one pending skill-acceptance checkpoint; acceptance must not invoke the skill, initialize H6, or activate a successor.
