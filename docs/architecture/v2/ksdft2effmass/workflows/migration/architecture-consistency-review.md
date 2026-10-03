# Workflow architecture consistency review

## Status

**Historical Workflow-only review; superseded as a repository-wide gate conclusion by the subsequent nominal-ABC decision.**

## Scope

Reviewed the class-owned target contracts, package inheritance schematic, consolidated
defects, and current-to-target crosswalk for the single coordinated Workflow
implementation run.

The review covers:

- generic Task and Workflow definitions;
- Task route inheritance and subclass enforcement;
- in-process results;
- simulation authority and nominal effect ownership;
- nested child-Workflow targeting;
- declarative plan compilation;
- process-local runtime binding closure;
- in-process engine invocation;
- Quantum ESPRESSO migration; and
- public API additions, changes, and removals.

## Consistency conclusions

1. **Definitions have one owner.** `AbstractTask` and `AbstractWorkflow` construct the
   generic frozen definitions; concrete operations add no definition schemas.
2. **Routes have one source.** Route-root ABCs supply `TaskExecutionKind`, subclass
   enforcement rejects overlap, and plan/binding constructors verify snapshots.
3. **Protected simulation effects have one method owner.** The target nominal
   `AbstractSimulationDispatchEffect` consumes the existing authority-bearing request.
   `AbstractSimulationTask` exposes no direct effect method. No unsupported generic
   `AbstractDispatchEffect` is introduced.
4. **Successful results have one shape contract.** `TaskExecutionResults` is ordered,
   nonempty, concrete, and shape-only; production and durable confirmation remain
   separate.
5. **Declarative and runtime state are separated.** `WorkflowExecutionPlan` contains no
   live adapter. `WorkflowExecutionBindings` owns complete process-local references.
6. **Nested targets are declarative.** `NestedWorkflowTarget` snapshots the child
   definition while runtime bindings verify concrete Task agreement.
7. **The initial engine scope is closed.** `WorkflowEngine.execute_in_process` accepts
   only the in-process route. Simulation and nested kinds fail closed and retain their
   existing specialized control paths.
8. **The migration is explicit.** The crosswalk identifies every current contract that
   changes, the QE ownership migration, public exports, removals, implementation order,
   and required evidence.
9. **Compatibility policy is consistent.** Retired protocols and signatures receive no
   aliases.
10. **Evidence claims remain bounded.** Architecture and future software checks do not
    imply execution, numerical verification, scientific validation, uncertainty
    quantification, or acceptance.

## Documentation checks

- Every target class has one class-owned `index.md` and `schematic.md`.
- All local Markdown links in the Workflow architecture surfaces resolve.
- The target-term audit found obsolete `TaskResultSet` only in historical defect
  descriptions explaining its replacement.
- `git diff --check` passed.
- Current implementation documentation remains explicitly distinct from target class
  contracts.

## Gate conclusion

The Workflow-only architecture-documentation gate was complete for its accepted scope.
No unresolved architecture choice remained within that scope. The subsequent decision
to replace every maintained `typing.Protocol` with a nominal ABC expands the gate and
requires an additional repository-wide review. The three consolidated defects have
accepted class-owned correction contracts and remain open only until the coordinated
source migration and required software evidence complete.

This conclusion does not itself start or authorize source implementation, periodic-1D
replay, protected execution, persistence migration, pushing, release, or publication.
