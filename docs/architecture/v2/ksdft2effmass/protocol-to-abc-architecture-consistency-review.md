# Protocol-to-ABC architecture consistency review

## Status

**Complete; post-commit independent correction review found no blocking finding.**

This record closes the expanded documentation gate only. It does not authorize source
implementation or protected execution.

## Scope

The bounded review covers:

- the thirteen maintained `typing.Protocol` declarations currently present under
  `python/src/ksdft2effmass`;
- their target nominal ABCs and class-owned schematics;
- the consolidated Workflow defect corrections;
- the declarative-plan/process-local-binding separation;
- exact result, observation, calculator, persistence, and operator-representation
  boundaries; and
- the explicit exclusion of QE-specific Workflow redesign.

## Contract closure

The [complete crosswalk](protocol-to-abc-migration.md) contains thirteen current-to-target
rows. The [exhaustive symbol inventory](protocol-to-abc-symbol-inventory.md) records
declarations, exports, production implementations, positive and negative test doubles,
boundary consumers, evidence owners, and exact target actions. Each target ABC has one
owning `<ClassName>/index.md` and `schematic.md`:

- one calculator ABC;
- three operator-representation ABCs;
- one shared-persistence ABC; and
- eight Workflow result, observation, control, effect, codec, and repository ABCs.

Every retired name is removed without an alias in the target. Structural lookalikes,
virtual subclass registration, discovery, and registry fallback are prohibited.

## Dependency and authority consistency

- Analysis-owned grid, boundary, and interval records may inherit operator-owned ABCs
  without reversing dependency direction. Existing operator modules import no analysis
  package; affected analysis modules add any required operator-owned ABC imports.
- `SQLiteAtomicRevisionStore` inherits the shared store ABC; the Workflow repository
  composes that ABC and remains Workflow-owned.
- Integration-owned observation identities, policy, and result inherit Workflow-owned
  read-only ABCs; Workflow imports no QE package.
- `AbstractPlaneWaveCalculator` remains distinct from the authority-bearing
  `AbstractSimulationDispatchEffect`. An executor with an incompatible method signature
  is not admitted through nominal coincidence.
- `LocalQuantumEspressoExecutor` belongs to the dispatch-effect route. QE Tasks have no
  direct calculator invocation in the accepted target.
- QE-specific Workflow families are outside this migration. No
  `AbstractQeSimulationWorkflow` or alternate QE Workflow ABC is introduced.

## Workflow consistency

The three consolidated defect corrections remain aligned:

1. `TaskExecutionResults` is one concrete, nonempty, ordered, identity-unique shape
   object containing nominal `AbstractResultObject` values.
2. `AbstractTask` enforces exactly one route root; `AbstractScientificTask` is
   route-less, and route behavior belongs to the in-process, simulation, or nested
   route ABC.
3. `WorkflowExecutionPlan` is declarative, while `WorkflowExecutionBindings` contains
   the exact plan and live process-local adapters.

The engine contract is consistently bindings-only:

```python
execute_in_process(
    bindings: WorkflowExecutionBindings,
    activation: TaskActivation,
) -> TaskExecutionResults
```

The engine reads the plan contained by the validated bindings object. It receives no
separate plan argument and performs no plan/binding correlation at invocation time.

## Result admission

The target does not equate every class named `Result` with a Workflow result. The
initial nominal `AbstractResultObject` set is the seven exact concrete families already
crossing the maintained Workflow serialization and execution boundaries. Narrower
observation membership inherits from that one result ABC. Tests must reject
attribute-compatible objects without nominal inheritance.

## Checks performed

The final writer pass established:

- all thirteen target ABCs have class-owned `index.md` and `schematic.md` files;
- an independent local-target checker resolved **384 local Markdown links across all
  142 files** under `docs/architecture/v2/ksdft2effmass/`; no target was missing;
- `uv run --project python sphinx-build -W --keep-going -b html doc/sphinx
  /tmp/ksdft2effmass-docs-html-protocol-abc` succeeded;
- the Workflow engine signature and plan/binding ownership contradictions are removed;
- current owning architecture pages use nominal terminology for the migrated ports;
- no proposed QE-specific Workflow ABC remains outside the historical decision record;
- `git diff --check` passes;
- `python/src`, `python/tests`, and `calculations` have no working-tree changes; and
- current source still contains thirteen Protocol declarations, as expected before the
  separately authorized implementation run.

The local-link pass found and corrected three pre-existing repository/Sphinx-relative
paths before its successful final run. The captured strict-Sphinx transcript is at
`/tmp/ksdft2effmass-sphinx-protocol-abc.log`; it is execution-local evidence and is not
claimed as a retained scientific artifact.

## Independent-review correction record

The first expanded independent review reported five blocking documentation findings.
The correction pass:

1. added the exhaustive concrete symbol and export inventory;
2. restored all omitted `AbstractNormalizedObservationSource` properties in its
   schematic and class contract;
3. made `executor_identity` explicitly abstract;
4. removed the remaining separate-plan engine wording; and
5. updated current architecture terminology or marked historical structural passages
   explicitly superseded by the nominal migration.

These corrections required a fresh independent re-review; the writer did not convert
them into acceptance by assertion.

The second independent review, run
`d97c981a-2c2d-499e-b047-1d26a125bd01`, confirmed those signature, property,
result-admission, authority, dependency, export, and QE-scope corrections but found
three remaining contradictions. The second correction pass:

1. separated retained calculator doubles from obsolete direct-QE-Task calculator
   fixtures, removed the instruction to grant the latter nominal membership, and
   assigned nominal-lookalike rejection to a distinct calculator fixture;
2. made the package page place live Tasks only in `WorkflowExecutionBindings`, with
   `WorkflowExecutionPlan` remaining declarative; and
3. updated the Task/colored-Petri-net page to the route-less
   `AbstractScientificTask`, explicit `AbstractInProcessScientificTask`,
   definition-only simulation, and route-distinct nested target.

The complete link, strict-Sphinx, diff, source-isolation, and Protocol-count checks were
then rerun successfully.

The follow-up review, run `a0a12706-9250-4c6d-bcfe-5808188e5bef`, confirmed all three
second-pass corrections and the remaining inventory, result, authority, dependency,
QE-scope, export, and source-boundary contracts. It found one final live-owner wording
contradiction and one nonblocking import-summary overstatement. The third correction
pass:

1. made both package-level nested-Task descriptions name the immutable child
   `WorkflowDefinition` and explicitly exclude a live `AbstractWorkflow` owner; and
2. aligned the dependency summary with the inventory: affected analysis modules add
   operator-ABC imports while operators retain no analysis dependency.

The complete local-link, strict-Sphinx, diff, and source-isolation checks were rerun
successfully after these corrections. Final independent re-review remains required.

## Gate conclusion

Independent review run `5756838a-fd7c-43a9-b009-041344bfdcd3` initially reported
`ReviewOutcome: NO_BLOCKING_FINDINGS` and found the expanded thirteen-contract
documentation gate technically ready to close. A fresh post-commit review of the
complete parent patch, run `3df10313-3b16-4599-90f2-69a32bab33e3`, subsequently found
four documentation contradictions: a separate plan input in one engine schematic,
nested execution assigned to the in-process engine, impossible QE dependency wording,
and three stale gate statuses. The correction pass removed all four.

Follow-up independent review run `09b97f2a-a6be-496f-b59f-ce91f7c7347f` reported
`ReviewOutcome: NO_BLOCKING_FINDINGS`, found no remaining issue in the corrected
surfaces, and judged them ready for a follow-up documentation commit.

The expanded documentation gate is complete. Source changes still require separate
explicit authorization. Completion establishes planning consistency only; it does not
establish software implementation, numerical verification, scientific validation,
uncertainty quantification, execution authority, human acceptance, release, or
publication readiness.
