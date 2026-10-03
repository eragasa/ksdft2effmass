# Workflow defects

This directory records consolidated technical defects in the proposed persistent
Workflow architecture. A record identifies one architectural cause, its current
evidence, and the boundary that must be satisfied before implementation proceeds. It
does not establish scientific validation, human acceptance, execution authority,
release status, or completion.

## Consolidated defects

| Defect | Status | Consolidated architectural cause | Required boundary |
|---|---|---|---|
| [`defect00001`](defect00001-incomplete_task_execution_results_contract.md) | Architectural contract documented; implementation pending | Current software and the blocked package proposal do not yet conform to the class-owned `TaskExecutionResults` contract. | Implement and integrate before the periodic-1D Workflow or durable confirmed-outcome integration. |
| [`defect00002`](defect00002-unclosed_task_execution_routes.md) | Architectural contracts documented; implementation pending | Current software does not yet enforce the accepted nominal route and simulation-effect contracts. | Implement in the coordinated migration before either specialized engine path. |
| [`defect00003`](defect00003-plan_runtime_binding_conflation.md) | Architectural contracts documented; implementation pending | Current software still combines declarative plans and live runtime adapters. | Implement the plan/bindings split before the first concrete periodic Workflow. |

## Consolidation history

The records consolidate the 2026-10-03 Workflow-engine smell test and subsequent
architecture critique through commit `95a73eed`:

- the original empty-result finding, ordered `TaskResultSet` naming concern, and
  provenance-sufficiency concern are consolidated into `defect00001`;
- the original overlapping-specialization finding, missing ABC-level enforcement, and
  simulation-authority contradiction are consolidated into `defect00002`; and
- the original shallow-plan-immutability finding and the retained-live-adapter critique
  are consolidated into `defect00003`.

The Workflow-focused suite had passed 1,053 tests, and focused Ruff, formatting,
strict mypy, and strict Sphinx checks had passed before these architecture findings
were recorded. Those results establish their stated software requirements only; they
do not erase these defects or authorize implementation, replay, or external execution.
