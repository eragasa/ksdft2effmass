# Pi session JSONL telemetry inventory

## Source scope

Five explicitly selected, local Pi session JSONL artifacts were inspected using
the supported per-working-directory session store. They total 25,652,147 bytes
and use session format version 3. Three snapshots end in an assistant `stop`
entry; two end after a tool result and are classified as partial. Pi 0.84.1 was
the inspecting runtime, but the session header does not persist the package
version that wrote each source.

The maintained inventory uses opaque sample identifiers and records byte counts
and SHA-256 source identities. It contains no source paths or copied prompt,
response, command, argument, result, file, provider-body, environment,
credential, communication, or unpublished scientific content.

## Observed event families

Six exact top-level kinds were observed: `session`, `message`, `model_change`,
`thinking_level_change`, `compaction`, and `custom_message`. Message roles were
`user`, `assistant`, and `toolResult`. The selected sources include ordinary
terminal turns, successful and failed tool results, assistant provider errors,
ten compactions, model and reasoning-level changes, and 61 matched subagent
dispatch/result pairs.

No unambiguous cancellation, blocked call, retry, rate-limit, branch summary,
multi-child branch, or assistant `aborted` entry was observed. Their persisted
representation therefore remains unavailable or unresolved rather than being
inferred from sensitive payload text.

## Identity hierarchy

The header `id` identifies a session. Non-header entry `id` and `parentId` form a
tree; JSONL order records append order but does not select an active branch. A
tool-call block `id` correlates with `toolResult.toolCallId`. Turns can be
inferred along one entry path but have no explicit identity.

No durable Task identity or general agent-run identity was observed. Subagent
calls can be counted from an allowlisted tool category and matched to their
parent-session results, but safe child-session identity and cross-session
parentage were not established.

## Timing capabilities

Entry timestamps are ISO-8601 UTC strings with observed millisecond precision;
message timestamps are integral Unix milliseconds. The clock source is not
documented as monotonic.

File wall span, path-aware turn wall intervals, tool-call-to-result wall
intervals, and parent-observed subagent dispatch-to-result intervals are
retrospectively derivable with completeness caveats. Provider duration,
prompt-to-first-token latency, streaming duration, exact monotonic tool duration,
active versus waiting intervals, child concurrency, and exact parent wait time
require live instrumentation.

## Token and cost capabilities

Assistant and compaction usage objects directly expose input, output, cache-read,
cache-write, and total token counts. Reasoning tokens are conditionally present
and absence must remain unavailable. Numeric cost components and totals are
present, but currency is not persisted. Tool-result token usage and exact context
utilization were not observed.

## Reliability capabilities

`toolResult.isError` directly distinguishes aggregate success from error, and
assistant `stopReason` directly records `stop`, `toolUse`, or `error` in the
selected sources. It does not distinguish cancellation, blocking, timeout, or
rate limiting. Provider-error body text and tool-result payloads remain
prohibited, so those subtypes were not inferred. Session closure is also not an
explicit event; trailing state supports only a partial-snapshot classification.

## Metric disposition

Direct observations include model and reasoning changes, token and estimated-cost
fields, compaction count, tool success/error counts, dispatch count, and malformed
tool-call structure. Session and turn wall spans, parent-observed agent-run span,
context-token trajectory, and human-response wall gaps are derivable proxies.

Live instrumentation is required for provider, first-token, exact tool,
concurrency, and parent-wait timing. Task duration, retries, checkpoint frequency,
changed-path scope, validation outcomes, correction cycles, and verified Task
resolution require other authority or evidence. Duplicate dispatch, repeated
file reads, and semantic repeated-tool-call detection are prohibited when they
would require retaining or hashing tool arguments or payloads.

## Privacy exclusions

Payload-bearing fields are represented only by field path, type, presence, and
privacy class. Sensitive values are neither copied nor hashed. Synthetic fixtures
use deterministic redaction placeholders and synthetic identities; they contain
no source values.

## Implications for the retrospective parser

The parser must dispatch first on top-level `type` and then on `message.role`,
preserve unknown kinds, reconstruct paths through `id`/`parentId`, distinguish
unavailable values from zero, and redact payloads before retaining provisional
observations. Version-3 structures in the four sanitized fixtures are provisional
examples, not the normalized telemetry contract.

The complete field, relationship, source-identity, reliability, and metric
classification inventory is in
[`pi-session-jsonl-inventory.json`](pi-session-jsonl-inventory.json).
