# Workflow v2 ProjectKoios migration structure

## Status

**Safe to defer while `ksdft2effmass.workflows.v2` remains a provisional local
compatibility boundary.** The current implementation is software verified for its
bounded foreground behavior, but it duplicates a substantial unpublished ProjectKoios
Workflows prototype and is not the final generic workflow owner.

## Current structure

The provisional implementation contains approximately nine thousand source lines. Its
largest modules currently include:

- `workflows/v2/runtime/service.py`, which owns the private multi-operation local
  runtime mechanics;
- `workflows/v2/core/models.py`, which owns many immutable workflow-core records; and
- `workflows/v2/runtime/foreground.py`, which owns foreground identities, plans,
  requests, evidence, workers, and reconcilers.

Public runtime operations are separated into immutable request objects, concrete
`DataObjectActionizer` performers, and immutable results. Internally, the concrete
runtime performers inherit one private `_LocalWorkflowRuntime`, so each performer can
access mechanics for operations other than its own even though its public `action`
method remains narrow.

The shared data-object hierarchy is correctly owned by `ksdft2effmass.base`, not by a
workflow-local `base` package. The established `ksdft2effmass.workflows` v1 package
remains separate and has no v2 compatibility alias.

## Deferred work

1. Bind the released ProjectKoios Workflows distribution and its exact contract
   versions when that owner becomes available and an applicable dependency change is
   authorized.
2. Construct an explicit class, identity, serialization, failure, and replay crosswalk
   between `ksdft2effmass.workflows.v2` and the released owner.
3. Prove value and retained-evidence equivalence for each migrated operation before
   replacing imports or removing the provisional implementation.
4. Split `service.py`, `models.py`, and `foreground.py` only along cohesive ownership
   boundaries after the external contracts stabilize. Do not perform cosmetic
   file-count reduction or create generic helper containers.
5. Replace broad inheritance from `_LocalWorkflowRuntime` with narrower private
   operation mechanics when doing so preserves one public request/actionizer/result
   boundary and all replay, authority, ambiguity, and evidence invariants.
6. Keep package-wide base tests separate from workflow-v2 integration tests, and keep
   the v2 dependency boundary closed against undeclared ProjectKoios imports.
7. Remove `ksdft2effmass.workflows.v2` only after all consumers have migrated and the
   deletion is separately authorized. Do not retain a compatibility alias.

## Revisit conditions

Revisit this debt when any of the following occurs:

- a ProjectKoios Workflows distribution publishes stable contracts;
- another maintained consumer adopts `ksdft2effmass.workflows.v2`;
- a materially changed runtime operation requires edits across unrelated portions of
  the large modules;
- the provisional namespace is proposed as a supported long-term public API; or
- a dependency, release, or removal plan is prepared for the workflow owner.

## Boundaries

This record does not authorize a ProjectKoios dependency change, consumer migration,
source deletion, release, publication, scheduler, queue, daemon, calculator dispatch,
or protected execution. It does not weaken the requirement for fresh attempt-bound
authority or permit retry of an ambiguous effect before conclusive query-only
reconciliation.

Passing software tests establishes implementation behavior only. It does not establish
scientific validity, numerical convergence, calculator execution, or acceptance of a
retained result.

## Completion criteria

This debt is complete when the authoritative external contracts are version-bound, the
crosswalk and equivalence evidence cover every maintained v2 operation, consumers use
the accepted owner, large internal modules have either cohesive boundaries or a
recorded reason to remain intact, and the provisional package is removed without an
alias under separately authorized deletion.
