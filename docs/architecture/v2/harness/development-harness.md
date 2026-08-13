# Development harness

## Responsibility

The development harness is owned by `ksdft2effmass.harness`. Its authority is limited to:

- repository changes;
- software architecture;
- implementation;
- software verification;
- repository documentation;
- development review; and
- development lifecycle state.

## Core records

`HarnessTask` is an immutable development work definition. It owns scope, preconditions, completion criteria, exclusions, and review requirements. `DevelopmentTaskSelection` identifies the authorized active development work and keeps automatic successor behavior explicit.

Neither object contains scientific CPN markings, calculator requests, numerical observations, scientific findings, or parameter selections.

## Development lifecycle

A development operation moves through planned, active, implementation, software verification, review, and completed states according to policy. Protected or human-owned decisions remain explicit, but no stage is manufactured merely to add ceremony. Routine deterministic corrections may use a shorter route.

The development harness may:

- observe an explicit repository root and starting revision;
- validate operation-specific repository preconditions;
- authorize bounded source and documentation changes;
- run software-verification and repository-conformance checks;
- project development control state through the deterministic [compiler architecture](compiler-architecture.md); and
- record development review and acceptance.

It may not execute a scientific `Campaign`, advance a `CampaignRun`, classify a calculator result scientifically, or record a `ScientificDisposition`.

## Package boundary

`ksdft2effmass.harness` owns development-harness contracts and composition. Project scientific specifications and scientific workflow state remain outside the harness package. Harness operations receive explicit roots and inputs; they perform no ambient repository discovery.

Submodule and wire-format details may be refined while preserving this package boundary.

## Unresolved issues

- Exact public fields of `HarnessTask` and `DevelopmentTaskSelection`.
- Closed lifecycle vocabulary and permitted transition rules.
- Representation of development review and acceptance.
- Boundary between generic repository operations and project-specific policy.
- Whether routine work uses the same lifecycle record with a shorter route or a distinct operation profile.
