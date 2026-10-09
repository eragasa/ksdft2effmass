# Strict mypy source baseline

## Status

**Numerical return boundaries corrected; workflow export ownership remains.** The
represented-difference dimension, dense and sparse eigenpair dimensions, and silicon
Bloch Fourier-sum return boundary now pass focused strict mypy checks without changing
numerical values or solver selection. The repository-wide source command still reports
two workflow export-ownership errors and must not yet be reported as passing.

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
matrix family. Focused strict mypy checks pass. The repository-wide strict command now
reports only the two workflow export-ownership errors below.

## Deferred work

1. Reconcile ownership of `SimulationDispatchOutcome`. Internal consumers should
   import it from its defining `workflows.runs.records` owner unless
   `workflows.control.dispatch` is deliberately documented and tested as a supported
   re-export.
2. Keep `workflows.control.__init__` consistent with that ownership decision and retain
   focused public-import tests for the supported surface.
3. Rerun the broad strict source command after the workflow correction.

## Boundaries

Corrections must not change matrix values, eigensolver selection, validation order,
workflow authority semantics, dispatch identity, serialization, or supported public
imports without the corresponding architecture and test updates. Do not resolve these
errors with `Any`, an unspecified `object` boundary, blanket `type: ignore`, or by
excluding files from mypy.

This debt does not weaken focused type-check results, establish scientific correctness,
or authorize workflow execution, dependency changes, publication, or calculator runs.

## Completion criteria

This debt is complete when `uv run mypy --strict src` exits successfully, each change
has focused evidence for its existing runtime contract, workflow export ownership is
explicitly documented, and no type suppression or semantic behavior change was used
merely to obtain a green command.
