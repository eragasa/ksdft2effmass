# V2-ISSUE-022: Scientific-decision response trust, ResultObject provenance, and correction semantics

**Severity:** High
**Scope:** Scientific-decision ingress, trusted response evidence, producer provenance, correction, and replay
**Status:** Open

## Current conflict

`ScientificDecisionRecorder` receives a bare response but claims to validate source and authority without trusted response evidence; its no-Task `ScientificDecisionResolution` fits no closed producer-provenance variant; and append-only correction does not define the single effective marking token or replay treatment after supersession.

## Affected contracts

- [`docs/architecture/v2/human-decisions.md`](../human-decisions.md) — the recorder receives a verbatim response without an authenticated response snapshot or verification receipt and permits append-only correction without effective-token semantics.
- [`docs/architecture/v2/identity-version-and-failure-contracts.md`](../identity-version-and-failure-contracts.md) — the closed producer-provenance variants do not cover a no-Task resolution created by the recorder within Workflow ingress.
- [`docs/architecture/v2/ksdft2effmass/workflows/workflow-run.md`](../ksdft2effmass/workflows/workflow-run.md) — decision-origin transitions prohibit Task production state while requiring closed ResultObject provenance and replayable history.
- [`docs/architecture/v2/ksdft2effmass/workflows/task-and-colored-petri-net-adapter.md`](../ksdft2effmass/workflows/task-and-colored-petri-net-adapter.md) — decision ingress maps supplied resolutions without defining their producer-provenance case or repeat-ingress token behavior.
- [`docs/architecture/v2/ksdft2effmass/workflows/artifact-and-provenance-model.md`](../ksdft2effmass/workflows/artifact-and-provenance-model.md) — existing external and Workflow producer variants do not describe recorder-produced decision results.
- [`docs/architecture/v2/ksdft2effmass/workflows/control-plane.md`](../ksdft2effmass/workflows/control-plane.md) — trusted ingress and correction lack one effective replay-value contract.

## Missing contract

Scientific-decision ingress lacks authenticated or verified response evidence, trusted source/snapshot and authority-resolution semantics, a no-Task decision-origin ResultObject provenance variant, and exact predecessor, supersession, effective-token, repeat-ingress, and replay rules.

## Exclusions and claim boundary

Decision records grant neither execution nor scientific-disposition authority. Response wire spelling and authentication mechanism are excluded. This record establishes no implementation, verification, scientific validation, uncertainty quantification, or human acceptance.
