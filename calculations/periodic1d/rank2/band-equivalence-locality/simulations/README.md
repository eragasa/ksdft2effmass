# Simulations

**Status:** extracted replaceable development producers and outputs; no versioned or
retained simulation has been executed from this directory.

The calculation-root `run_*_development.py` entrypoints compose the local
[`workflow/`](../workflow/) package and write into the `development/` subtree. They do
not duplicate generic numerical implementation from `python/src` or external owners.

The migration source was:

```text
experiments/model-adequacy/periodic1d/
  band-equivalence-versus-hopping-locality/
```

Expected calculation channels include the flat analytic benchmark, the dispersive
four-state parent, the bounded parent homotopy, momentum refinement, and ordinary-lattice
range truncation. They may share declared inputs, but their results and evidence statuses
must remain distinguishable.

The extracted entrypoints preserve their development status and write deterministic CSV
summaries under `development/results/`. They combine calculation and tabulation and are
not yet the separated versioned five-stage workflow. No `run_01_experiment.py`,
`run_02_experiment_verification.py`, closed schema, or retained run directory is created
until the maintained version and wire contracts are selected.
