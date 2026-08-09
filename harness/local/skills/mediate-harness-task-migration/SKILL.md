---
name: mediate-harness-task-migration
description: Prepare or present one authorized HarnessTask migration review packet, record one explicit file disposition, or continue one serial Task-document migration after that explicit response.
---

# Mediate HarnessTask migration

Use this skill only for one explicitly authorized HarnessTask file-migration review. Do not use it for ordinary documentation edits, generic JSON serialization, task planning, unrelated checkpoint resolution, or general human review.

## Preparation

1. Reconstruct authority from durable local records. Require Stage 2B or another exact migration Task to be explicitly active.
2. Require exactly one authorized source and destination, plus explicit candidate Task JSON, mapping record, projection profile, source revision, and Git object or explicit absence. If any artifact is missing, name it exactly and stop.
3. Invoke the maintained preparation command with explicit root-relative paths. Verify its canonical result, packet binding, and review-document SHA-256 and byte count.
4. Present the complete generated review document. A brief orientation may precede it; never replace the document with a summary.
5. Stop for explicit human disposition.

## Disposition

1. Preserve the human response verbatim and require the caller to supply exactly one normalized choice: accept this file migration, revise the contract or mappings, retain Markdown ownership, or defer the file.
2. For revision, require exact authorized correction scope. Invoke the maintained disposition command with the original explicit inputs, packet binding, review-document identity, response, generic disposition, and migration disposition.
3. Verify the exact packet, decision, review-document, source, candidate, and disposition binding. Stop.

Never infer acceptance from tests, packet status, reviewer agreement, silence, or elapsed time. Never prepare the next file automatically.

## Command discipline

Work directly by default. Do not spawn subagents merely to read, construct, or render a packet. Use one read-only specialist only when the human explicitly requests independent semantic review. Never use intercom to recover context.

Use the maintained commands documented in `docs/api/harness-task.rst`; do not generate temporary Bash, Python heredocs, or ad hoc orchestration when they support the operation. The commands observe explicit files and translate outputs; existing immutable DataObjects and ActionObjects own validation, rendering, comparison, packet preparation, and decision compatibility.

The review document is deterministic but non-authoritative. Only an explicit human response supplies file acceptance. The commands do not apply migration, mutate control state, activate Stage 2B, or select a successor.
