# Strict mypy source baseline

## Status

**Closed.** The numerical return boundaries and workflow export ownership are
corrected without changing numerical values, eigensolver selection, workflow authority
semantics, dispatch identity, serialization, or supported public imports. The
repository-wide strict source command now passes.

## Observed baseline

On 2026-10-08 at checkpoint `37cd312dc0b3`, the command

```console
cd python
uv run mypy --strict src
```

reported five errors in five files:

```text
src/ksdft2effmass/operators/difference.py:153: error: Returning Any from function declared to return "int"  [no-any-return]
src/ksdft2effmass/operators/eigenpairs.py:140: error: Returning Any from function declared to return "int"  [no-any-return]
src/ksdft2effmass/solid_state/slater_koster.py:591: error: Returning Any from function declared to return "ndarray[tuple[Any, ...], dtype[Any]]"  [no-any-return]
src/ksdft2effmass/workflows/control/reconciliation.py:21: error: Module "ksdft2effmass.workflows.control.dispatch" does not explicitly export attribute "SimulationDispatchOutcome"  [attr-defined]
src/ksdft2effmass/workflows/control/__init__.py:20: error: Module "ksdft2effmass.workflows.control.dispatch" does not explicitly export attribute "SimulationDispatchOutcome"  [attr-defined]
Found 5 errors in 5 files (checked 427 source files)
```

These files were outside the bounded numerical correction that exposed the broad
baseline. The failures are software typing and export-ownership debt; they are not
scientific validation findings.

## Completed bounded correction

The three numerical findings are corrected at their owning boundaries:

1. `OperatorRecordDifferenceResult.matrix_dimension` returns an explicit built-in
   integer while retaining the positive square-matrix constructor contract.
2. `RealSymmetricEigenpairSolver.validate()` converts both dense NumPy and sparse SciPy
   shape metadata to a built-in integer after the existing square and exact-symmetry
   checks.
3. The silicon Bloch Fourier sum has an explicit complex128 array return type and
   validates its sample count and fixed represented matrix dimensions.

Focused software tests cover the built-in integer boundaries and the complex128 Bloch
matrix family. Focused strict mypy checks pass.

The workflow findings are also corrected at their owning boundaries:

1. Reconciliation imports `SimulationDispatchOutcome` directly from its defining
   `workflows.runs.records` owner.
2. `workflows.control` deliberately re-exports the run-owned record, preserving the
   supported control and root Workflow package surfaces.
3. The control-plane architecture documentation and public-API test record and verify
   that ownership.

## Completion evidence

On 2026-10-09, after both bounded corrections, the repository-wide command reported:

```text
Success: no issues found in 462 source files
```

Focused workflow-control tests passed with 81 tests. The exact bounded repository suite,
Ruff, configured mypy, strict Sphinx, and `git diff --check` also passed. These checks
establish bounded software consistency only; they do not establish scientific
correctness, convergence, physical adequacy, uncertainty quantification,
transferability, or acceptance.

## Boundaries

Corrections must not change matrix values, eigensolver selection, validation order,
workflow authority semantics, dispatch identity, serialization, or supported public
imports without the corresponding architecture and test updates. Do not resolve these
errors with `Any`, an unspecified `object` boundary, blanket `type: ignore`, or by
excluding files from mypy.

This debt does not weaken focused type-check results, establish scientific correctness,
or authorize workflow execution, dependency changes, publication, or calculator runs.

## Completion criteria

Satisfied: `uv run mypy --strict src` exits successfully, each correction has focused
evidence for its existing runtime contract, workflow export ownership is explicitly
documented, and no type suppression or semantic behavior change was used to obtain the
green command.
