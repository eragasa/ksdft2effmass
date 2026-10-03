# DEFECT00001: incomplete Task execution-results contract

## Status

Architectural contract documented; implementation and integration remain required
before implementing the periodic-1D Workflow or durable confirmed outcomes.

## Consolidated scope

This record consolidates:

- the implemented engine's acceptance of empty Task result tuples;
- the proposed `TaskResultSet` name despite its ordered tuple representation; and
- the need to distinguish local result-shape validity from producer, activation,
  attempt, dispatch, artifact, and durable-outcome correlation.

## Problem

The Workflow architecture does not yet define one unambiguous common result value for
all successful Task routes. The current engine accepts an empty tuple even though a
confirmed `TaskInvocationOutcome` requires results. The proposed replacement is called
`TaskResultSet` but preserves order, and its relationship to provenance and durable
confirmation is not sufficiently restrictive.

These are one architectural defect: the Task execution boundary lacks a single,
precisely named value whose invariants stop at result shape and whose consumers retain
ownership of production and admission evidence.

## Evidence

- `python/src/ksdft2effmass/workflows/engine.py` validates result type and identity
  uniqueness but not nonemptiness.
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

An invocation can pass the current engine boundary yet be impossible to represent as a
confirmed durable outcome. In the proposed architecture, ambiguous naming and
insufficient boundary language could also cause callers to treat local shape validity
as production or provenance validity.

## Persistent correction

Replace the raw tuple and proposed `TaskResultSet` with the concrete frozen
[`TaskExecutionResults`](../TaskExecutionResults/index.md) DataObject. It must:

- contain one ordered, nonempty tuple of concrete `ResultObject` instances;
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

## Required evidence

Before closure, focused software verification must show rejection of empty, non-tuple,
non-ResultObject, wrong-identity, and duplicate-identity values; preservation of result
order; prohibition of subclass-based alternate contracts; and successful use by
confirmed outcome construction without bypassing production correlation.

## Evidence boundary

This is a software-contract defect. It is not evidence that a scientific calculation
ran or that any result is numerically verified, scientifically validated,
uncertainty-quantified, or accepted.
