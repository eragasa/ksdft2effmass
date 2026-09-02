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
and small test-consumed fixtures may be committed. Generated calculations belong only
under the backend's ignored `run/` directory. Routine streams, scratch and restart
state, wavefunctions, charge densities, generated XML or NetCDF files, executables,
pseudopotentials without verified redistribution terms, and machine-local paths are
not committed.

The presence of an example does not activate a HarnessTask or authorize QE, ABINIT,
Wannier90, or another scientific executable. Execution requires separate preflight and
human authorization where project policy requires it.

The authoritative layout and comparison boundaries are documented in
[`docs/architecture/v2/tutorial-examples.md`](../../docs/architecture/v2/tutorial-examples.md).
Materialized tutorials:

- [`silicon-scf/`](silicon-scf/) — implemented QE input-construction example; ABINIT planned.
- [`hydrogen-molecule-scf/`](hydrogen-molecule-scf/) — one observed ABINIT tutorial execution and compact calculated observation; QE planned.

Campaign mappings are maintained in:

- [`docs/computational/quantum-espresso-tutorial-simulations.md`](../../docs/computational/quantum-espresso-tutorial-simulations.md)
- [`docs/computational/abinit-tutorial-correspondence.md`](../../docs/computational/abinit-tutorial-correspondence.md)
