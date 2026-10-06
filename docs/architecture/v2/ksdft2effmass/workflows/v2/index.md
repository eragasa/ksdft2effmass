# `ksdft2effmass.workflows.v2` provisional compatibility boundary

## Status

**Provisional migration implementation.** ProjectKoios Workflows owns the
intended generic workflow contracts. This package stages those requirements
inside `ksdft2effmass` until the separately distributed owner is available and
accepted as a dependency.

The package does not claim ownership of the eventual ProjectKoios API. Its
public names, immutable records, and operation boundaries are intentionally
shaped for a later explicit mapping. No compatibility alias connects v1 to v2.

## Included scope

The v2 package consumes the shared `ksdft2effmass.base` hierarchy and contains:

- immutable engine-neutral workflow core identities and transition records;
- opaque atomic revision persistence with the private local SQLite
  implementation;
- append-only local runtime records, canonical serialization, replay, and
  reservation/idempotency checks; and
- bounded foreground execution with deterministic plans, attempt-bound
  authorization, application-owned workers, query-only reconciliation, and
  terminal transition gating.

The shared [base hierarchy](../../base/index.md) duplicates the accepted
Ingestion-style data-object pattern without placing generic base types under the
workflow package.

Material operations use immutable request and result objects with concrete
`DataObjectActionizer` implementations exposing
`action(*, request) -> result`. Constructors, intrinsic validation, properties,
and cheap identity derivations remain data-object behavior rather than separate
actions.

## Implementation lineage

The initial core, persistence, and runtime implementation was adapted from the
isolated `projectkoios-workflow` foreground-runtime worktree rooted at commit
`63f127dd6922c16accb3dc857cfb2e28224a8958`. That source included uncommitted
Stage-B development, so the commit identifies only its starting baseline, not a
published or independently retrievable final implementation. Namespace and
implementation identities were changed explicitly for this provisional package;
no released ProjectKoios dependency is claimed.

## Ownership and migration rule

`ksdft2effmass.workflows.v2` is a temporary compatibility namespace. When the
ProjectKoios Workflows distribution is available, migration must compare exact
contracts and retained behavior before replacing imports. Scientific models,
calculations, validation, and interpretation remain owned by `ksdft2effmass`;
application policy and calculator dispatch remain outside this generic runtime.

The existing `ksdft2effmass.workflows` v1 package remains unchanged during this
slice. Consumers are not migrated automatically, and v2 does not import v1 or
provide aliases for it.

## Explicit exclusions

This slice adds no scheduler, queue, daemon, claim/lease service, plugin
registry, network client, process runner, calculator adapter, protected
execution, scientific acceptance rule, or publication behavior. Planning does
not grant execution authority. Ambiguous external effects remain ineligible for
retry until query-only reconciliation establishes non-application.

Passing software tests establishes implementation behavior only. It does not
establish calculator execution, numerical convergence, scientific validity, or
acceptance of any retained result.
