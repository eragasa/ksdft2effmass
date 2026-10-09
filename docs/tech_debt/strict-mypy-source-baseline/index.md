# Strict mypy source baseline

## Status

**Safe to defer outside the currently touched numerical classes.** The focused strict
mypy checks for the Wigner–Seitz and Löwdin-quadratic changes pass, but the
repository-wide source command is not yet green. This record preserves that distinction;
it does not authorize reporting the broad command as passing.

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

## Deferred work

1. In `operators/difference.py`, return an explicitly typed Python integer for the
   represented matrix dimension without weakening the public positive-dimension
   contract.
2. In `operators/eigenpairs.py`, preserve dense and sparse validation order while
   converting shape metadata to an explicit integer rather than leaking an
   untyped third-party shape value.
3. In `solid_state/slater_koster.py`, give the Bloch Fourier sum an explicit complex
   array return boundary and verify its sample and matrix dimensions without adding
   `Any`, an unspecified `object` boundary, or a broad suppression.
4. Reconcile ownership of `SimulationDispatchOutcome`. Internal consumers should
   import it from its defining `workflows.runs.records` owner unless
   `workflows.control.dispatch` is deliberately documented and tested as a supported
   re-export. Keep `workflows.control.__init__` consistent with that decision.
5. Add or retain focused tests for each corrected public contract, then rerun the broad
   strict source command.

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
