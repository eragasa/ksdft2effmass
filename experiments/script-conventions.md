# Experiment script conventions

This document records the transitional common shape of executable Python composition
roots under `experiments/`. Every such root is being migrated to its distributed
calculation owner and the applicable mechanics are being integrated into the
Architecture v3 calculation contract. This document does not create a generic
experiment framework or transfer scientific policy between families. Each family
continues to own its controls, tolerances, statuses, schemas, evidence policy, and
interpretation during migration.

## Inventory and migration boundary

The current tree has 36 executable Python scripts in these roles:

| Role | Count | Current boundary |
|---|---:|---|
| Periodic-1D exploratory analysis and plotting | 9 | Pre-version development utilities |
| Dimension-specific band-equivalence calculation, refinement, and plotting | 16 | Replaceable bounded development composition |
| Synthetic-strain calculation, response, and scan composition | 6 | Replaceable bounded development composition |
| Cross-family dimensional plotting and decision-landscape composition | 2 | Development comparison only; not an experiment identity |
| Single-band retained producer and package verifier | 2 | Immutable version-one evidence tooling |
| Higher-rank analytic-control sampler | 1 | Pre-execution development sanity check |

All 36 inventoried entry points satisfy the mechanical `main() -> int` and `SystemExit`
contract below. Their calculation-side migration is tracked by the family-local
`migration.md` files and by the four-file shared ledger at
`calculations/periodic/multiband/migration.md`. The retained single-band version-one
scripts remain frozen with their retained source manifest and are not rewritten for
style. Conformance of prospective and pre-version scripts does not promote their
outputs.

## Required executable shape

A new or migrated script must:

1. begin with a module docstring that states its role and evidence boundary;
2. use an import-safe `main() -> int` composition root;
3. return `0` only after every required verification and write completes;
4. invoke the root with `raise SystemExit(main())`;
5. allow exceptions to produce a nonzero process status rather than printing success;
6. derive repository or experiment paths from `Path(__file__).resolve()`, never the
   caller's working directory;
7. avoid `chdir`, `sys.path` mutation, implicit network access, and import-time
   calculation or file writes; and
8. remain directly runnable with the repository-selected Python environment.

The normal footer is:

```python
def main() -> int:
    """Compose the declared action and return success after all gates pass."""
    # Construct typed controls, execute, verify, then write.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

A package console entry point may call the same `main`; it does not replace the typed
experiment action or become an experiment identity.

## Script roles

Use names that disclose effects:

- `run_development.py` writes replaceable development calculation artifacts;
- `verify_development.py` independently verifies existing development artifacts;
- `plot_development.py` reads or reconstructs typed development results and writes
  replaceable figures;
- `run_experiment.py` is reserved for an immutable-version producer with no-overwrite
  run semantics;
- `verify_package.py` verifies an existing retained package without invoking its
  producer; and
- `verify_<control>.py` or `sample_<control>.py` is a bounded analytic-control utility,
  not an experiment run.

An executable module may expose import-safe typed definitions or pure composition
functions when a neighboring refinement script needs them. Importing it must never
execute `main`. If the shared composition becomes nontrivial, move it to a cohesive
family-owned module and add the corresponding architecture documentation; do not create
a generic `Helper`, `Manager`, or experiment-runner abstraction.

## Controls and command-line arguments

Outcome-relevant scientific controls belong in immutable typed definitions or in
schema-validated input documents. They must not be silently overridden through
environment variables, the working directory, or undocumented command-line defaults.

`argparse` is appropriate for bounded utility controls such as the density of a
non-evidentiary formula sample. A command-line option that changes an experiment case,
mesh, tolerance, alignment family, dependency binding, output identity, or evidence
status requires an explicit protocol and serialization contract. Booleans, numeric
strings at typed API boundaries, nonfinite values, and ambiguous sentinels remain
forbidden unless a wire contract explicitly defines their parsing.

## Calculation, verification, and writing order

A calculation script follows this order:

1. materialize the family-owned typed definition;
2. authenticate required dependency revisions when the version contract requires it;
3. execute the producer action;
4. execute the independent verifier through its separate route;
5. fail closed if verification is not qualified;
6. serialize and validate canonical artifacts;
7. write only to the lifecycle-appropriate destination; and
8. print a concise final summary.

Do not create an output directory before cheap control and dependency checks. Retained
producers use a fixed run identity and `exist_ok=False`. Development producers write
only beneath a documented replaceable development directory and must not call that
output a run or evidence package.

A package verifier reads existing bytes, validates digests and schemas, reconstructs
required facts without calling the producer, and exits nonzero on any mismatch.
Serialized status labels are not verification oracles.

## Outcome hierarchy

The complete diagnostic ledger is not a list of equally important findings. Each
protocol and typed result must keep these roles distinct:

1. **qualification gates** decide whether a case is interpretable;
2. **primary outcomes** answer prespecified scientific comparisons;
3. **control channels** check constructions, conventions, and oracle routes;
4. **explanatory diagnostics** characterize mechanisms or bound primary errors; and
5. **refinement checks** test whether outcomes are stable against the declared numerical
   discretization.

Scripts must not select noteworthy channels after inspecting their numerical values. A
claim-oriented summary reports prespecified primary outcomes only after all applicable
gates pass and labels control or explanatory values by their narrower roles. The full
ledger remains available for audit, including qualified null results and failed gates.

## Output and logging

Human-readable output should use stable `key=value` fields where practical. At minimum,
a calculation summary identifies the family or version, lifecycle (`development` or
`retained`), verification disposition, and output path. Avoid bare booleans whose
meaning depends on prose or print order. Large calculations should emit a concise
claim-oriented summary separately from their complete diagnostic artifacts.

Scripts do not suppress tracebacks from unexpected failures. A verifier may add one
concise failure line on standard error, but it must still raise or return a nonzero
status. Logging must not expose credentials, private paths beyond declared local
provenance, or unpublished data.

## Scientific and retention boundary

A consistent script shape establishes neither numerical convergence nor scientific
validity. It does not authorize production Quantum ESPRESSO or Wannier90 execution,
remote computation, a retained run, evidence promotion, or publication use. Those gates
remain family- and version-specific.
