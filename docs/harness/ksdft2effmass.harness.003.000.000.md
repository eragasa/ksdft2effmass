---
document_id: ksdft2effmass.harness.003.000.000
task_id: null
parent: ksdft2effmass.harness.000.000.000
status: pilot_packet_ready
sphinx: excluded
---

# Human review interface

> **Pilot packet ready; broader program inactive.** The first explicit-input packet
> API and one derived pilot packet are implemented. No decision record, persistence,
> runtime review workflow, correction, acceptance, or successor is active.

## Problem

Human source and test audits are currently performed conversationally. That process
mixes deterministic observations with human judgment, while repeated agent reviews
can add ceremony, duplicate findings, and obscure which actor has authority. The
harness should prepare compact, reviewable evidence without replacing human
judgment or presenting tool success as acceptance.

## Authority boundary

Deterministic Actions may inspect explicitly supplied artifacts and return structured
observations. An LLM may summarize, critique, and recommend. Only the human may
accept, reject, defer, remand, waive a finding, or authorize follow-on work. Passing
deterministic checks does not imply human acceptance, and duplicate reviewer runs
are not independent evidence. The interface must not resolve a decision, activate a
successor, or authorize protected work automatically.

## Architecture alternatives

### 1. Filesystem review packets

Maintain review inputs, observations, findings, limitations, and decisions as
versioned JSON and Markdown artifacts. This has transparent repository provenance
and a low initial implementation boundary, but cross-review queries and normalized
relations become increasingly cumbersome.

### 2. SQLite-backed review state

Represent observations, findings, dispositions, and their relations in a normalized
SQLite store. This supports querying and consistency constraints, but prematurely
selecting a schema could freeze conversational assumptions before the review
contract is understood.

### 3. Hybrid filesystem summaries and SQLite observations

Retain immutable human-readable filesystem summaries while normalizing observations
and relations in SQLite. This separates durable review packets from queryable state
and is the recommended long-term direction.

The hybrid recommendation is decision support only and remains unaccepted. The
[initial round](ksdft2effmass.harness.003.001.000.md) implements only a pure
explicit-input packet API and one derived Markdown pilot. It selects no persistent
filesystem or SQLite contract; those alternatives remain open while the review
boundary is evaluated.

## Claim boundary

A review packet may organize software-verification observations and human findings.
It cannot manufacture oracle independence, numerical correctness, scientific
validation, uncertainty quantification, provenance truth, or human acceptance.
Those conclusions require their own applicable evidence and authority.

## Navigation

- **Index:** [Harness documentation](ksdft2effmass.harness.000.000.000.md)
- **Parent:** [Harness documentation](ksdft2effmass.harness.000.000.000.md)
- **Previous:** [Incremental migration plan](ksdft2effmass.harness.002.001.009.md)
- **Next:** [Initial human-review interface round](ksdft2effmass.harness.003.001.000.md)
- **Child:** [Initial human-review interface round](ksdft2effmass.harness.003.001.000.md)
