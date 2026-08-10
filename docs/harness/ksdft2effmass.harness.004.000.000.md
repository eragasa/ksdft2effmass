---
document_id: ksdft2effmass.harness.004.000.000
task_id: harness.telemetry
parent: ksdft2effmass.harness.000.000.000
status: proposed_inactive
sphinx: excluded
---

# Harness telemetry

## Purpose

`harness.telemetry` is the inactive operational program for implementing and
evaluating local harness telemetry. Every Task requires separate explicit
activation, performs no work merely by existing, and activates no successor
automatically.

The research motivation, hypotheses, questions, conceptual model, metrics,
experimental design, VVUQ boundaries, privacy policy, research-integrity policy,
and anticipated contribution remain owned by the [research
proposal](../research/agentic-development-case-study/agenticdevelopment_casestudy.00.md).
This page indexes only the proposed operational implementation sequence.

## Operational telemetry and effectiveness evaluation

Operational telemetry records bounded observations of harness execution.
Harness-effectiveness evaluation joins those observations with repository
evidence and applies Task-class-dependent judgments. Therefore:

```text
operational telemetry
≠
harness-effectiveness evaluation
```

Operational efficiency does not establish software correctness, scientific
validity, or general agent superiority.

## Task hierarchy

```text
harness.telemetry
├── harness.telemetry.session-jsonl-inventory
├── harness.telemetry.retrospective-parser
├── harness.telemetry.normalized-event-contract
├── harness.telemetry.sqlite-projection
├── harness.telemetry.baseline
├── harness.telemetry.live-timing-extension
├── harness.telemetry.effectiveness-evaluation
└── harness.telemetry.controlled-benchmarks
```

| Task ID | Title | Status | Parent | Prerequisites | Explicit activation |
|---|---|---|---|---|---|
| `harness.telemetry` | Harness telemetry program | Inactive | — | — | Yes |
| `harness.telemetry.session-jsonl-inventory` | Inventory selected Pi session JSONL | Completed | `harness.telemetry` | — | Yes |
| `harness.telemetry.retrospective-parser` | Implement the retrospective session parser | Inactive | `harness.telemetry` | `harness.telemetry.session-jsonl-inventory` | Yes |
| `harness.telemetry.normalized-event-contract` | Freeze the normalized telemetry event contract | Inactive | `harness.telemetry` | `harness.telemetry.retrospective-parser` | Yes |
| `harness.telemetry.sqlite-projection` | Implement the local SQLite telemetry projection | Inactive | `harness.telemetry` | `harness.telemetry.normalized-event-contract` | Yes |
| `harness.telemetry.baseline` | Measure the pre-simplification baseline | Inactive | `harness.telemetry` | `harness.telemetry.sqlite-projection` | Yes |
| `harness.telemetry.live-timing-extension` | Add the live timing extension | Inactive | `harness.telemetry` | `harness.telemetry.sqlite-projection` | Yes |
| `harness.telemetry.effectiveness-evaluation` | Evaluate harness effectiveness | Inactive | `harness.telemetry` | `harness.telemetry.baseline`, `harness.telemetry.live-timing-extension` | Yes |
| `harness.telemetry.controlled-benchmarks` | Define controlled harness benchmarks | Inactive | `harness.telemetry` | `harness.telemetry.effectiveness-evaluation` | Yes |

Each child has `harness.telemetry` as its explicit parent. Dotted identifiers do
not imply a relationship independently of the Task records and graph.

## Dependency sequence

```text
session-jsonl-inventory
→ retrospective-parser
→ normalized-event-contract
→ sqlite-projection
→ baseline
```

```text
sqlite-projection
→ live-timing-extension
```

```text
baseline
+ live-timing-extension
→ effectiveness-evaluation
→ controlled-benchmarks
```

These arrows follow the repository convention from prerequisite to dependent.

## Pi-session artifact source

The retrospective source is only an explicitly selected Pi session JSONL
artifact. The completed [structural inventory](../../harness/reports/telemetry/pi-session-jsonl-inventory.md)
records the observed fields, relationships, availability, and privacy boundary;
its [machine-readable report](../../harness/reports/telemetry/pi-session-jsonl-inventory.json)
does not freeze a parser or normalized event contract. The program performs no
recursive session discovery, and Task existence does not authorize reading
arbitrary historical sessions.

## Privacy boundary

Only metadata needed for the declared operational observations may be retained.
Prompts, responses, commands, tool arguments, tool results, headers, credentials,
environment values, personal communications, and unpublished scientific content
must not be retained. Remote export and external data transmission are excluded.

## Intended data flow

```text
Pi session JSONL
→ metadata-only normalized events
→ local SQLite projection
→ deterministic operational summaries
→ effectiveness evaluation joined with repository evidence
```

The intended projection path is `.pi/runtime/harness-telemetry.sqlite3`. It is
local, uncommitted, metadata-only, replaceable, and non-authoritative. Pi session
JSONL remains the source artifact; the projection cannot replace Task, graph,
checkpoint, scientific, or human-decision authority.

## Deferred implementation

This layout implements no telemetry code, public interface, Pi extension, parser,
database, instrumentation, runtime hook, dashboard, benchmark, or scientific
work. It changes no dependency or lockfile. Each implementation or evaluation
Task remains inactive pending separate explicit activation and its applicable
controls.

## Navigation

- [Harness documentation index](ksdft2effmass.harness.000.000.000.md)
- [Agentic-development telemetry research proposal](../research/agentic-development-case-study/agenticdevelopment_casestudy.00.md)
