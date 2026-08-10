<!-- Generated from SQLite control state; do not edit. -->
# Implement the complete SQLite-hybrid harness control cutover

[Task index](index.md) · [Previous](./harness.simplification.resources.h3-validator-retirement.md) · [Next](./harness.telemetry.md)

## Status

`completed`: bounded migration completed; no successor activated

## Objective

Consolidate structured harness control information in one tracked authoritative SQLite database while retaining executable code and human-authored content in ordinary files.

## Parent and prerequisites

- Depends on: `harness.simplification.evidence.naming`

## Authority references

- AGENTS.md

## Authorized scope

- Migrate Tasks, evidence, tests, agents, skills, resources, decisions, and generated projection identities into the SQLite-hybrid control model.

## Completion criteria

- The deterministic database, SQL recovery representation, projections, reader cutover, and bounded validation agree.

## Exclusions

- Runtime observations, telemetry, scientific calculations, protected execution, release actions, and successor activation remain excluded.

## Historical source

No archived source.
