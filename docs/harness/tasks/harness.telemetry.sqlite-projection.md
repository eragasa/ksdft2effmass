<!-- Generated from SQLite control state; do not edit. -->
# Implement the local SQLite telemetry projection

[Task index](index.md) · [Previous](./harness.telemetry.session-jsonl-inventory.md) · [Next](./human-review-interface.audit-evidence-identifiers-correction.md)

## Status

`inactive`: proposed inactive; separate explicit human activation required and no automatic successor activation

## Objective

Implement a local query projection over normalized telemetry that supports deterministic report reconstruction without becoming repository authority.

## Parent and prerequisites

- Parent: `harness.telemetry`
- Depends on: `harness.telemetry.normalized-event-contract`

## Authority references

- docs/harness/ksdft2effmass.harness.004.000.000.md
- docs/research/agentic-development-case-study/agenticdevelopment_casestudy.00.md

## Authorized scope

- Use `.pi/runtime/harness-telemetry.sqlite3` as the intended local, uncommitted metadata-only projection path.
- Preserve Pi session JSONL as the source artifact; the projection does not become Task, graph, checkpoint, scientific, or human-decision authority.

## Completion criteria

- The local projection reconstructs deterministic reports from normalized metadata while remaining uncommitted, replaceable, and non-authoritative.

## Exclusions

- The Task remains inactive, requires separate explicit human activation, performs no work merely by existing, and activates no successor automatically.
- This layout does not authorize telemetry implementation, public telemetry interfaces, Pi extensions, session parsing, arbitrary historical-session discovery, SQLite creation, live instrumentation, runtime hooks, benchmarks, dashboards, remote export, external data transmission, sensitive payload retention, scientific work, dependency changes, lockfile changes, or changes to Pi.

## Historical source

No archived source.
