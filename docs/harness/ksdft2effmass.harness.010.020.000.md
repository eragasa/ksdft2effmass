---
document_id: ksdft2effmass.harness.010.020.000
task_id: harness-simplification.evidence
parent: ksdft2effmass.harness.010.000.000
status: proposed
sphinx: excluded
---

# Extractable evidence subsystem

> **Proposed architecture.** The current
> `ksdft2effmass.harness.pi.evidence` module audits evidence identifiers only.
> The subsystem described here does not yet exist.

The future `harness.pi.evidence` subsystem would own generic evidence records,
artifact identities, event references, queries, and reconciliation interfaces
that can be extracted independently of `ksdft2effmass` scientific policy.

## Proposed responsibilities

- immutable evidence-record and finding records;
- content identities and external artifact references;
- links from evidence to requirement, task, owner, command result, and review;
- append-only recording through the operational state interface;
- focused queries by task, owner, class, path, or requirement;
- full reconciliation of uniqueness, referential integrity, lifecycle, and
  retained artifact availability;
- deterministic exports for version-controlled summaries.

## Non-responsibilities

The subsystem would not decide scientific validity, infer VVUQ class from a
number, approve a task, resolve a checkpoint, run a command, or store large
calculation outputs. Project evidence namespaces and scientific acceptance rules
would remain project-local inputs.

## Focused validation

Focused evidence validation would check one supplied record family and its direct
references. Examples include validating one test-evidence migration, one command
result, or one review finding set. It should not require scanning unrelated
project history.

## Full reconciliation

Full reconciliation would check global identifier uniqueness, source/artifact
identities, task and requirement links, owner validity, event ordering, retained
artifact references, and current-state/export agreement. It would report derived
findings without silently repairing records.

## Extraction boundary

A standalone candidate would include only generic record models, schemas,
serialization, reconciliation logic, and tests. It would exclude local profiles,
`.pi` data, scientific modules, route configuration, and repository-specific
agent policy.

See the [unified state proposal](./ksdft2effmass.harness.010.010.000.md) and
[incremental migration plan](./ksdft2effmass.harness.010.050.000.md).
