# Analysis

**Status:** extracted replaceable development analysis; no versioned or retained
analysis result exists.

The `development/` subtree now owns the calculation-local plotting code, narrative, and
available figures extracted from the publication-independent experiment. Its inputs are
the tables under `../simulations/development/results/`. It includes flat-parent,
dispersive-parent, parent-homotopy, momentum-refinement, and truncation studies.

Some figures referenced by `Ragasa2026a` v3 currently exist only in a dirty development
checkout and therefore are not yet reconstructed or commit-bound evidence.

The maintained successor analysis must:

1. read a verified versioned simulation result rather than rerun the simulation;
2. retain sampled and analytic channels separately;
3. verify first-passing cutoff decisions independently;
4. preserve interpolation, conversion, truncation, and total-error semantics;
5. write machine-readable analysis before plotting; and
6. label all outputs as development unless a later retained-evidence contract says
   otherwise.

No `run_03_analysis.py`, `run_04_analysis_verification.py`, or `run_05_plots.py` is added
until its input and output contracts are closed.
