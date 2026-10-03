# Workflow defects

This directory records consolidated technical defects and their persistent
corrections in the Workflow architecture. A record identifies one architectural cause,
its evidence, and the boundary required for closure. It does not establish scientific
validation, human acceptance, execution authority, release status, or completion of
any external calculation.

## Consolidated defects

| Defect | Status | Consolidated architectural cause | Required boundary |
|---|---|---|---|
| [`defect00001`](defect00001-incomplete_task_execution_results_contract.md) | Closed | The former engine boundary admitted empty raw result tuples and lacked one common nonempty result container. | Persistent correction and software evidence complete. |
| [`defect00002`](defect00002-unclosed_task_execution_routes.md) | Closed | The former hierarchy permitted overlapping routes and exposed an authority-inadequate simulation execution shape. | Persistent correction and software evidence complete. |
| [`defect00003`](defect00003-plan_runtime_binding_conflation.md) | Closed | The former plan retained live Workflow and Task owners. | Persistent correction and software evidence complete. |

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
