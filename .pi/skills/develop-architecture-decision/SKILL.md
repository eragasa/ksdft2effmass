---
name: develop-architecture-decision
description: Produces read-only decision support for a material architecture choice by reconstructing durable repository state, preserving exactly three distinct defensible architectures, recommending one, and stopping for a human decision.
---

# Develop an architecture decision

Use this skill only when a material architecture choice remains open. It is read-only decision support: inspect repository and durable state, write the requested decision document and checkpoint proposal only as returned artifacts, and stop before selection or implementation. The caller, not this skill, controls persistence of those artifacts.

Read [the complete conventions](references/architecture-decision-conventions.md) before analysis.

## Inputs

Require a correlated request identity, task and parent-workflow identities, attempt identity, immutable artifact references, authority order, decision scope, expected output locations/schema, and termination policy. Inspect unresolved checkpoints, canonical Task and selection state, durable human decisions, accepted contracts, relevant source and maintained documentation in authority order. Do not treat historical ownership or evidence as current authority.

Separate every material statement as an observed fact, inference, human choice, implementation consequence, or deferred question. Identify conflicts rather than resolving them by preference.

## Applicability gate

Proceed only when exactly three materially distinct, defensible architectures can be compared across authority, ownership, dependency direction, state, persistence, dispatch, history, migration, and runtime. A defensible status quo may be one option; never include it merely to fill a slot. Configuration variants of one architecture are not distinct options.

If three options are unavailable, return exactly one classification:

- `deterministic`: accepted authority leaves one compatible correction;
- `underspecified`: missing information prevents three defensible architectures; or
- `unsuitable`: the question is not an architecture decision.

Identify the missing or controlling information and stop without a checkpoint.

## Decision output

For an applicable request, preserve exactly Option A, Option B, and Option C. Use the exact document headings and required option facets in the conventions. Compare all three against common criteria, make exactly one recommendation, and retain the two nonrecommended options honestly.

The checkpoint proposal must summarize the actual A/B/C conceptual architectures, cite the decision document, and offer `D — Reconsider or defer`. It must never use generic accept/correct/reject choices. The skill stops before implementation.

## CPN invocation boundary

A guard may inspect immutable token fields but must never load or invoke this skill. An external harness consumes a correlated `SkillInvocationRequestToken` outside guard evaluation. The result preserves request, task, parent-workflow, attempt, skill-content, and input-artifact identities; produced decision/checkpoint artifacts; findings; commands; warnings; mutation summary; failure classification; and completion status.

Retries require immutable parent authorization or a pre-authorized retry policy, a new attempt identity, and retained prior results/findings. Read-only analysis is observationally idempotent only for identical artifact identities. A changed repository snapshot is a new input, not a replay.

## Prohibitions and stop

Do not select an option, implement it, activate a successor, rewrite history, mutate dispatch or persistence, duplicate the full analysis in another artifact, or claim that review agreement establishes software verification, numerical verification, scientific validation, uncertainty quantification, physical correctness, or human acceptance. Stop after the three-option document and checkpoint proposal, or after the non-applicable classification.
