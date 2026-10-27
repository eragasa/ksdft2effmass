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

Calculation channels include the flat analytic benchmark, the dispersive four-state
parent, the bounded parent homotopy, momentum refinement, dense ordinary-lattice range
truncation, and threshold-adjacent truncation refinement. The results directory also
contains a derived diagnostic catalog and sampled range-decision table produced only
after the 14 source tables pass their declared schema and cross-table checks. Shared
inputs do not merge their scientific channels or evidence statuses.

The extracted entrypoints preserve their development status and write deterministic CSV
summaries under `development/results/`. Strict development serializers and independent
reconstruction checks now exist for the nonflat and truncation records, but the
entrypoints still combine calculation and tabulation and are not a separated versioned
lifecycle. No retained run directory or retained execution identity is created until the
maintained configuration, wire, acceptance, and provenance contracts are selected.
