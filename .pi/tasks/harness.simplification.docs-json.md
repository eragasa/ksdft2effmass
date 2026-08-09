# Migrate documentation and the JSON control surface

Status: blocked; all child Tasks are completed under Option C file-per-Task JSON authority, but the consolidated parent integration review failed on two current H3 resource-boundary findings; no child is active

Task identity: `harness.simplification.docs-json`

Prerequisite: `harness.simplification.api.action-object-grammar:completed`

## Objective

Correct the synchronization and authority delta between human-readable `docs/`, transitional Task records, and the selected JSON control surface. Preserve human-authored intake and documentation-owned subject matter while moving operational control fields to JSON-backed generated reference pages.

## Decomposition

```text
harness.simplification.docs-json.publication
→ harness.simplification.docs-json.authority-catalog
→ harness.simplification.docs-json.documentation-correction
→ harness.simplification.docs-json.schema-projection
```

`publication` further decomposes into:

```text
harness.simplification.docs-json.publication.triage
→ harness.simplification.docs-json.publication.hierarchy
```

Every node is the same Task type. Decomposition, prerequisites, and chain sequencing remain distinct relationships.

## Bootstrap boundary

Markdown Task records are transitional and non-executable. Before the JSON Task contract exists, only a current explicit human instruction may activate one exact Task. No child activates automatically, parent completion is not computed, scope is not inferred from the identifier hierarchy, and chain evaluation does not interpret Markdown decomposition.

## Correction rule

Apply one contract-consistent correction directly. Naming violations, stale operational prose, obsolete links, obvious generated or temporary files, and contradictions resolved by accepted precedence do not require human checkpoints. Human review is limited to materially different defensible choices at a human-owned boundary.

Documentation may explain and locate work but never independently activates a Task, supplies executable scope, selects a successor, or establishes completion or acceptance.

## Extractable harness boundary

Generic harness code may own neutral explicit-input inventory, hashing, extraction-result, relationship, partition-validation, schema-validation, and rendering mechanics. Project-local code owns repository roots, authority policy, document roles, Task identities, control schemas, projection profiles, and human decisions. Generic code must not depend on `.pi/` or ksdft2effmass-specific identities.

## Completion

The parent is complete when each decomposed Task completes, their inputs and outputs agree, deterministic corrections are applied, unresolved findings have explicit dispositions, and one consolidated parent integration review passes. No extra parent acceptance step is required unless a material human-owned choice remains.

## Consolidated integration review

The single consolidated review at revision `b6d0834b80b3d9ee64d86c02f66501bf9d7314be` failed. Its durable report is `.pi/evidence/docs-json/parent-integration-review.md`.

The review confirmed agreement of the completed child outputs but found two material current-state defects: the historical H3 validator retains an obsolete manifest-version invariant, and generic resources contain project-local identities or paths. The parent remains blocked. The future H3-validator-retirement Task is recorded but cannot start under its stated precondition unless a later explicit human decision changes that precondition or the parent first obtains a passing integration review through another authorized correction.
