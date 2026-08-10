<!-- Generated from SQLite control state; do not edit. -->
# Add the live timing extension

[Task index](index.md) · [Previous](./harness.telemetry.effectiveness-evaluation.md) · [Next](./harness.telemetry.normalized-event-contract.md)

## Status

`inactive`: proposed inactive; separate explicit human activation required and no automatic successor activation

## Objective

Add live instrumentation only for timing and concurrency observations that persisted Pi session JSONL cannot establish precisely.

## Parent and prerequisites

- Parent: `harness.telemetry`
- Depends on: `harness.telemetry.sqlite-projection`

## Authority references

- docs/harness/ksdft2effmass.harness.004.000.000.md
- docs/research/agentic-development-case-study/agenticdevelopment_casestudy.00.md

## Authorized scope

- Observe prompt-to-first-token latency, streaming duration, monotonic tool duration, active versus waiting intervals, overlapping child-agent execution, and exact parent wait time where unavailable from persisted events.
- Do not duplicate observations already available reliably from persisted session events.

## Completion criteria

- The extension adds only demonstrated telemetry gaps, records measurement overhead, and leaves reliable persisted observations unduplicated.

## Exclusions

- The Task remains inactive, requires separate explicit human activation, performs no work merely by existing, and activates no successor automatically.
- This layout does not authorize telemetry implementation, public telemetry interfaces, Pi extensions, session parsing, arbitrary historical-session discovery, SQLite creation, live instrumentation, runtime hooks, benchmarks, dashboards, remote export, external data transmission, sensitive payload retention, scientific work, dependency changes, lockfile changes, or changes to Pi.

## Historical source

No archived source.
