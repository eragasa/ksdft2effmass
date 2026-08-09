---
document_id: ksdft2effmass.harness.002.001.013
task_id: harness.simplification.docs-json.task-document-migration
parent: ksdft2effmass.harness.002.001.000
status: deferred-inactive
sphinx: excluded
---

# Human review: serial six-file Task migration

> **Stage 2B is deferred and inactive.** Stage 2A was not architecture-accepted,
> the migration framework was removed, and no file migration is authorized. This
> page is retained as historical planning evidence.

## Purpose

Migrate exactly the six accepted Markdown Task sources one at a time under the
unchanged Stage-1 contract and human-accepted Stage-2A implementation. No later
file may be prepared before the current file is dispositioned and any accepted
migration is verified.

## File order and destinations

| Order | Source | Candidate maintained documentation |
|---:|---|---|
| 1 | `.pi/tasks/harness.simplification.docs-json.md` | `docs/harness/ksdft2effmass.harness.002.002.000.md` |
| 2 | `.pi/tasks/harness.simplification.docs-json.publication.md` | `docs/harness/ksdft2effmass.harness.002.002.001.md` |
| 3 | `.pi/tasks/harness.simplification.docs-json.publication.triage.md` | `docs/harness/ksdft2effmass.harness.002.002.002.md` |
| 4 | `.pi/tasks/harness.simplification.docs-json.publication.hierarchy.md` | `docs/harness/ksdft2effmass.harness.002.002.003.md` |
| 5 | `.pi/tasks/harness.simplification.docs-json.authority-catalog.md` | `docs/harness/ksdft2effmass.harness.002.002.004.md` |
| 6 | `.pi/tasks/harness.simplification.docs-json.documentation-correction.md` | `docs/harness/ksdft2effmass.harness.002.002.005.md` |

These destinations remain proposed. No destination exists and every source
remains authoritative until its own accepted migration is applied and verified.

## One-file packet

Each immutable packet must provide a concise human-readable before/after view:

- original Markdown;
- candidate canonical JSON;
- candidate maintained documentation;
- explanation of content moved to each destination;
- exact unexplained differences, if any;
- opaque-content preservation result;
- rollback identity; and
- one simple decision: accept, revise, retain Markdown, or defer.

Detailed mappings, identities, and validation evidence remain linked rather than
being required reading for the human decision.

## Decision effects

**Accept** authorizes only the current candidate migration followed by exact
verification. **Revise** authorizes only a bounded current-candidate correction
within the accepted contract. **Retain Markdown** leaves the current source
unmigrated and authoritative. **Defer** postpones the file without implied
acceptance. A required material contract change stops Stage 2B and returns for
explicit contract review.

## Serial boundary

The next packet cannot be prepared from silence, passing checks, reviewer
agreement, or the prior packet's acceptance. It begins only after the current
file has a durable disposition and any accepted migration has passed canonical
round trip, rendering, byte-structural comparison, graph, mixed-format
inspection, opaque-preservation, and rollback-identity checks.

## Exclusions

Stage 2B does not batch files, silently alter the accepted contract, normalize or
drop opaque content, implement selection state, cut over or delete the chain,
migrate other Tasks, add dependencies, change lockfiles, or perform SQLite,
telemetry, scientific, publication, external, protected, release, or unrelated
work.

## Activation boundary

A Stage-2B activation checkpoint may be created only after Stage 2A implementation
is explicitly human-accepted. Stage-2B activation itself accepts no file packet.

## Navigation

- **Index:** [Harness documentation](ksdft2effmass.harness.000.000.000.md)
- **Parent:** [First harness simplification round](ksdft2effmass.harness.002.001.000.md)
- **Previous:** [HarnessTask implementation and hardening](ksdft2effmass.harness.002.001.012.md)
