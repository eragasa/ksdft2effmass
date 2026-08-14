# V2-ISSUE-002: Scientific dispatch and result-ingress atomicity

**Severity:** Implementation blocker

**Scope:** ScientificWorkflowRun persistence and external dispatch

## Conflict

CPN request firing, attempt reservation, external dispatch, result acceptance, artifact publication, result-token introduction, and successor transition recording do not yet have one complete crash-consistency contract. A failure between them can leave persisted marking, request, result, artifact, and external-process state inconsistent.

## Affected contracts

- `workflow/scientific/index.md` — *External action protocol*
- `workflow/control-plane.md` — request reservation versus request-token firing
- `workflow/persistence.md` — *Transaction boundaries*
- `workflow/artifact-and-provenance-model.md` — publication atomicity

## Required resolution

Define one authoritative request-side commit that records attempt and request reservation plus the successor marking or an outbox-equivalent dispatch obligation. Define idempotent dispatch and result-ingress operations and deterministic reconciliation after every interruption boundary.

## Acceptance condition

Recovery can classify and reconcile the persisted run, dispatch obligation, external result, artifacts, and next permitted transition without duplicate attempt or result acceptance.

This issue does not authorize external execution.
