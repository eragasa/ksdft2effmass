<!-- Generated from SQLite control state; do not edit. -->
# Implement the retrospective session parser

[Task index](index.md) · [Previous](./harness.telemetry.normalized-event-contract.md) · [Next](./harness.telemetry.session-jsonl-inventory.md)

## Status

`inactive`: proposed inactive; separate explicit human activation required and no automatic successor activation

## Objective

Implement a read-only transformation from explicit Pi session JSONL through provisional metadata-only observations to a deterministic operational summary.

## Parent and prerequisites

- Parent: `harness.telemetry`
- Depends on: `harness.telemetry.session-jsonl-inventory`

## Authority references

- docs/harness/ksdft2effmass.harness.004.000.000.md
- docs/research/agentic-development-case-study/agenticdevelopment_casestudy.00.md

## Authorized scope

- Use a provisional internal representation until real controlled session variants have been inspected.
- Preserve unknown event kinds without inventing semantics, distinguish unavailable values from zero, and accept only explicitly selected session JSONL inputs.

## Completion criteria

- Controlled examples produce deterministic metadata-only observations and summaries while unknown kinds and unavailable values remain explicit.

## Exclusions

- The Task remains inactive, requires separate explicit human activation, performs no work merely by existing, and activates no successor automatically.
- This layout does not authorize telemetry implementation, public telemetry interfaces, Pi extensions, session parsing, arbitrary historical-session discovery, SQLite creation, live instrumentation, runtime hooks, benchmarks, dashboards, remote export, external data transmission, sensitive payload retention, scientific work, dependency changes, lockfile changes, or changes to Pi.

## Historical source

No archived source.
