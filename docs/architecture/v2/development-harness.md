# Development harness

## Target responsibility

The development harness is conceptually aligned with
`projectkoios.bootstrap` from the future reusable repository
`eragasa/projectkoios-bootstrap`. This identifies a target ownership boundary;
it does not require a runtime dependency or freeze extraction timing.

Its authority is limited to:

- repository changes;
- software architecture;
- implementation;
- software verification;
- repository documentation;
- development review; and
- development lifecycle state.

## Core records

`HarnessTask` is an immutable development work definition. It owns scope,
preconditions, completion criteria, exclusions, and review requirements.
`DevelopmentTaskSelection` identifies the authorized active development work and
keeps automatic successor behavior explicit.

Neither object contains scientific CPN markings, calculator requests, numerical
observations, scientific findings, or parameter selections.

## Development lifecycle

A development operation moves through planned, active, implementation, software
verification, review, and completed states according to policy. Protected or
human-owned decisions remain explicit, but no stage is manufactured merely to
add ceremony. Routine deterministic corrections may use a shorter route.

The development harness may:

- observe an explicit repository root and starting revision;
- validate operation-specific repository preconditions;
- authorize bounded source and documentation changes;
- run software-verification and repository-conformance checks;
- project development control state; and
- record development review and acceptance.

It may not execute a scientific `Campaign`, advance a `CampaignRun`, classify a
calculator result scientifically, or record a `ScientificDisposition`.

## Reusable package boundary

`projectkoios.bootstrap` is the target reusable package for development-harness
contracts that are project-independent. Project policy, scientific
specifications, and project-specific Task composition remain outside the generic
package. Generic code receives explicit roots and inputs; it performs no ambient
repository discovery.

Exact package modules and wire formats remain unresolved until extraction proves
that their contracts are stable and project-independent.
