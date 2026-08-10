# Normalize publication documentation

Status: completed; both child Tasks completed on 2026-08-09

Task identity: `harness.simplification.docs-json.publication`

Parent task: `harness.simplification.docs-json`

## Objective

Triage publication-preparation files and apply one coherent hierarchy before documentation/control-surface comparison.

## Decomposition

```text
harness.simplification.docs-json.publication.triage
→ harness.simplification.docs-json.publication.hierarchy
```

Both are ordinary Tasks. The first produces deterministic classifications plus an ambiguity queue; the second consumes the accepted result. Neither activates automatically.

## Completion

This parent is complete when both Tasks complete, their input/output identities agree, and unresolved publication roles have an explicit disposition. It does not add a separate parent acceptance step unless a material human-owned choice remains.
