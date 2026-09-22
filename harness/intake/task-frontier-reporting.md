# Scoped Task-frontier discovery and reporting

## Human request

After a next-Task query inspected only the globally selected Task and initially
missed the broader simulation campaign, the human clarified:

> no we have a whole list of simulation tasks that need to be done

The subsequent inventory required an ad hoc one-pass scan of the simulation Task
catalog. The human then instructed:

> this find all tasks need to be more efficient, make a list of recommendations

The resulting recommendations were to add a deterministic scoped frontier command,
separate global selection from discovery, classify candidate and disposition states,
compute prerequisite closure and blockers, represent campaign priority without prose
inference, distinguish execution from disposition, provide compact JSON and table
output, reuse existing Harness owners, integrate discovery into next-Task selection,
verify catalog and classification consistency, and avoid caching until profiling shows
a need.

The human directed:

> add these to the software development task queue

## Recording decision and boundary

The existing software Task
`migration.v2.harness.critical-path-reporting` already owns dependency-frontier and
blocker reporting. This request expands that Task rather than creating a duplicate
Task, competing graph, or second queue authority. The canonical Task remains under
`tasks/software/` with its existing identity, parent, lifecycle, and explicit
activation requirement.

This recording operation authorizes only the Task and intake update plus necessary
generated projection synchronization. It does not activate implementation, select a
public wire-format change, authorize scientific or protected execution, reprioritize
a simulation campaign, modify `harness/task-selection.json`, or activate a successor.

## Proposed work after explicit activation

1. Define an immutable explicit-scope request and a structured frontier result, with
   reusable analysis owned by a cohesive `TaskFrontierAnalyzer` ActionObject.
2. Add a minimal typed `list-task-frontier` CLI adapter supporting all-catalog,
   configured-category, and exact-campaign scopes.
3. Load each configured canonical Task once and derive results through the existing
   Task model, registry, prerequisite contracts, and selection input. SQLite and
   generated projections remain derived outputs, not authority.
4. Report the globally selected Task separately so one active research Task cannot
   hide a simulation or software campaign frontier.
5. Classify executable candidates, preflight or decision candidates, direct and
   transitive blockers, protected-execution boundaries, deliberate deferrals,
   completed or superseded work, and campaign reviews.
6. Preserve deterministic topological, root, leaf, blocker, frontier, and unweighted
   longest-dependency-path reporting without schedule or duration claims.
7. Define a machine-readable human-owned campaign-priority and child-disposition
   contract before relying on it. Do not parse ordering from `status_detail` prose or
   duplicate canonical parent and prerequisite topology.
8. Distinguish “every child needs an explicit disposition” from “every child must be
   executed.” Inventory membership never grants or implies execution authority.
9. Emit deterministic structured JSON and a compact table with Task identity, title,
   status, scope, unresolved prerequisites, protected boundaries, and recommended
   next operation.
10. Update the next-Task recommendation procedure to obtain a scoped frontier before
    exact single-Task inspection. `TaskStateInspector` remains the bounded owner once
    one exact candidate and canonical path are known.
11. Verify complete indexing, duplicate and unresolved references, scoping,
    prerequisite closure, selected-Task separation, classification, ordering, output
    formats, and non-authorization of protected actions.
12. Use a deterministic one-pass implementation first. Add caching only if measured
    representative performance demonstrates a real bottleneck and an explicit
    invalidation contract is accepted.

The proposed capability is software planning infrastructure only. Its output cannot
activate a Task, approve a human decision, establish prerequisite completion,
authorize execution, or provide scientific validation or acceptance.
