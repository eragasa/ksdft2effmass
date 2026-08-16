# V2-ISSUE-029: Scientific disposition ownership and semantic closure

**Severity:** High
**Scope:** Package ownership, conclusion semantics, intended use, cited analyses, and supersession or withdrawal
**Status:** Open

## Current conflict

V2 declares a workflow-owned disposition recorder while `ScientificAnalysis` and `ScientificDisposition` appear analysis-owned, creating an import-direction conflict with `analysis → workflows` and the prohibition on workflows importing concrete analysis. The same purportedly closed disposition contract lacks its conclusion vocabulary and the policy meaning needed to interpret cited analyses, tolerances, uncertainty, conflicts, supersession, and withdrawal.

## Affected contracts

- [`docs/architecture/v2/repository-layout.md`](../repository-layout.md) — selected package edges forbid workflows from importing concrete analysis while assigning disposition recording to workflows.
- [`docs/architecture/v2/analysis/index.md`](../analysis/index.md) — analysis implementations depend on workflow contracts while disposition records appear analysis-owned.
- [`docs/architecture/v2/analysis/analysis-and-disposition.md`](../analysis/analysis-and-disposition.md) — recorder inputs cross the package boundary and the claimed closed conclusion vocabulary and interpretation policy remain undefined.
- [`docs/architecture/v2/workflow/service-model.md`](../workflow/service-model.md) — disposition recording is composed as workflow service behavior against analysis-owned concepts.
- [`docs/architecture/v2/workflow/control-plane.md`](../workflow/control-plane.md) — the control plane owns recording behavior without a dependency-valid abstract boundary.
- [`docs/architecture/v2/workflow/workflow-run.md`](../workflow/workflow-run.md) — persisted disposition references require stable ownership and semantics for replay and supersession history.

## Missing contract

`ScientificDisposition` lacks dependency-valid ownership for its records, recorder, and repository-facing boundary, plus a closed conclusion vocabulary and rules binding intended use, cited analyses, limitations, tolerances, convergence, uncertainty, conflicting findings, supersession, and withdrawal.

## Exclusions and claim boundary

Authority to record, supersede, or withdraw a disposition remains separately tracked by V2-ISSUE-010. This record defines no scientific meaning, acceptance rule, implementation, verification, validation, uncertainty quantification, or human acceptance.
