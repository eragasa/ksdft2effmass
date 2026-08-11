<!-- Generated from SQLite control state; do not edit. -->
# Implement source-aware control verification

[Task index](index.md) · [Previous](./harness.simplify-2.validation-retirement.repository-validation.md) · [Next](./harness.simplify-2.wire-validation-decomposition.md)

## Status

`active`: explicitly selected after generation-builder completion; automatic successor activation remains disabled

## Objective

Resolve the frozen canonical source inputs, generate an isolated candidate with the shared builder, and compare maintained control state semantically and projection-exactly without publication.

## Parent and prerequisites

- Parent: `harness.simplify-2.validation-retirement`
- Depends on: `harness.simplify-2.validation-retirement.generation-builder`

## Authority references

- AGENTS.md
- harness/reports/validation-retirement-inventory.json
- harness/tasks/harness.simplify-2.validation-retirement.json

## Authorized scope

- Implement private canonical-input resolution and source-aware comparison under `python/src/ksdft2effmass/harness/pi/local/control/`.
- Preserve `HarnessControlVerifier` identity and execute signature while reporting deterministic structured source, SQL, manifest, projection, integrity, foreign-key, schema, and semantic findings.
- Confine unexpected-artifact inspection to frozen publisher-owned paths and clean only verifier-owned temporary workspaces.

## Completion criteria

- Verification detects source drift, jointly modified SQLite and SQL, missing, changed, and unexpected owned projections while ignoring raw SQLite byte inequality and unrelated files.
- Verifier publishes nothing, cleans its temporary workspace after success and failure, and `harness_control check` returns one on drift.
- Control synchronization and affected deterministic validation pass.

## Exclusions

- Do not derive authority from maintained generated artifacts, search for or delete repository-wide temporary files, or claim arbitrary noncanonical request reconstruction.
- Do not add dependencies, a second database or publisher, telemetry, public wire kinds, or protected work.

## Historical source

No archived source.
