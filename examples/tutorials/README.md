# Computational tutorial examples

Examples are organized by computational concept and then by calculator backend:

```text
<tutorial-id>/
  README.md
  qe/
  abinit/
```

Each materialized tutorial contains both backend directories. A backend README states
whether that realization is implemented, planned, blocked, or not applicable. Missing
calculator behavior is never represented by fabricated input or output.

Portable inputs, deterministic construction or postprocessing scripts, documentation,
and small test-consumed fixtures may be committed. Generated calculations belong in
either the backend's ignored `run/` directory or an isolated external run root declared
by an exact execution preflight. External roots use the same runtime roles and are
referenced only by portable run identities; machine-local absolute paths are not
committed. Routine streams, scratch and restart state, wavefunctions, charge densities,
generated XML or NetCDF files, executables, pseudopotentials without verified
redistribution terms, and machine-local paths are not committed.

The presence of an example does not activate a HarnessTask or authorize QE, ABINIT,
Wannier90, or another scientific executable. Execution requires separate preflight and
human authorization where project policy requires it. Synthetic fixtures may test
isolated software or numerical behavior, but tutorial-derived claims about actual
calculator stages, artifacts, diagnostics, continuation, or failures require
identified outputs from an authorized scientific-executable invocation.

The authoritative layout and comparison boundaries are documented in
[`docs/architecture/v2/tutorial-examples.md`](../../docs/architecture/v2/tutorial-examples.md).
Materialized tutorials:

- [`silicon-scf/`](silicon-scf/) — implemented QE input-construction example; an ABINIT SCF dataset was observed as part of the paired bands workflow.
- [`silicon-bands/`](silicon-bands/) — completed paired QE and ABINIT SCF-to-fixed-density-bands tutorial observations.
- [`silicon-structure-optimization/`](silicon-structure-optimization/) — one calculated QE 7.5 variable-cell-relaxation tutorial observation; ABINIT proposed.
- [`silicon-dos/`](silicon-dos/) — one calculated QE 7.5 three-Task SCF-to-NSCF-to-DOS tutorial observation; ABINIT deferred.
- [`hydrogen-molecule-scf/`](hydrogen-molecule-scf/) — one observed ABINIT tutorial execution and compact calculated observation; QE planned.

Campaign mappings are maintained in:

- [`docs/computational/quantum-espresso-tutorial-simulations.md`](../../docs/computational/quantum-espresso-tutorial-simulations.md)
- [`docs/computational/abinit-tutorial-correspondence.md`](../../docs/computational/abinit-tutorial-correspondence.md)
