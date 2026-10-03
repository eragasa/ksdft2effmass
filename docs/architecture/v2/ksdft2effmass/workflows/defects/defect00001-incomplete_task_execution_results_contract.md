# DEFECT00001: incomplete Task execution-results contract

## Status

Closed after implementation, local software verification, and independent review
with no blocking findings.

## Consolidated scope

This record consolidates:

- the implemented engine's acceptance of empty Task result tuples;
- the proposed `TaskResultSet` name despite its ordered tuple representation; and
- the need to distinguish local result-shape validity from producer, activation,
  attempt, dispatch, artifact, and durable-outcome correlation.

## Problem

Before correction, the Workflow architecture did not define one unambiguous common
result value for all successful Task routes. The engine accepted an empty tuple even
though a confirmed `TaskInvocationOutcome` requires results. The proposed replacement
was called `TaskResultSet` despite preserving order, and its relationship to provenance
and durable confirmation was insufficiently restrictive.

These are one architectural defect: the Task execution boundary lacks a single,
precisely named value whose invariants stop at result shape and whose consumers retain
ownership of production and admission evidence.

## Evidence

- Before correction, `python/src/ksdft2effmass/workflows/engine.py` validated result
  type and identity uniqueness but not nonemptiness.
- `../task-and-colored-petri-net-adapter.md` specifies one or more returned results.
- `python/src/ksdft2effmass/workflows/runs/records.py` requires `bool(self.results)` for
  a confirmed invocation outcome.
- A bounded in-memory reproduction showed that the engine returns `()` unchanged from
  a direct scientific Task.
- The proposed architecture defines `TaskResultSet.results` as a tuple and preserves
  result order, so “set” is semantically misleading.
- Cardinality and identity checks alone do not establish result production,
  provenance, route admission, or durable confirmation.

## Consequence

The former engine boundary admitted an invocation that could not be represented as a
confirmed durable outcome. Ambiguous naming and insufficient boundary language could
also have caused callers to treat local shape validity as production or provenance
validity.

## Persistent correction

Replace the raw tuple and proposed `TaskResultSet` with the concrete frozen
[`TaskExecutionResults`](../TaskExecutionResults/index.md) DataObject. It must:

- contain one ordered, nonempty tuple of concrete `AbstractResultObject` instances;
- require exact `ResultObjectIdentity` values;
- require unique result identities;
- prohibit specialized subclasses; and
- claim only local result-shape validity.

Every successful in-process route and every confirmed specialized route must produce
or admit `TaskExecutionResults`. Rejected and indeterminate routes contain none.
`TaskExecutionResults` must not itself establish execution authority, result
production, artifact lineage, result ingress, or a confirmed `TaskInvocationOutcome`.
Those correlations remain with their existing route-specific and durable control
owners.

## Implementation evidence

`workflows/model.py` now owns final `TaskExecutionResults`; `WorkflowEngine` accepts
only that exact container. Focused constructor and engine evidence covers nonempty
ordered nominal results, unique identities, structural-lookalike rejection, and
wrong-container rejection. Durable `TaskInvocationOutcome` continues to require
separate result references and production records, so the container does not bypass
production correlation.

## Evidence boundary

This is a software-contract defect. It is not evidence that a scientific calculation
ran or that any result is numerically verified, scientifically validated,
uncertainty-quantified, or accepted.
