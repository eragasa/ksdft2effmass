# Quantum ESPRESSO silicon SCF backend

**Status: implemented software example.**

This example reconstructs the retained QE 7.2 `example01` silicon Davidson SCF input
using upstream-selected grouping tags, `QePwInputFile`, and `QePwInputFileWriter`. The
same portable input has also completed one separately authorized QE 7.5 smoke test;
that observation does not establish production convergence or scientific validation.

Run the deterministic software test from the repository root:

```bash
uv run --project python --extra dev pytest -q \
  examples/tutorials/silicon-scf/qe/test_silicon_scf.py
```

The test writes no files and does not invoke Quantum ESPRESSO. The maintained input in
`input/si.scf.david.in` uses `./pseudo/` and `./scratch/` rather than machine-local
paths. A separately authorized execution must stage required external data and write
all generated files beneath the ignored `run/` directory.

The retained QE 7.2 input and execution record remain at
`calculations/bulk-silicon/qe-example01-si-scf-davidson/`. The QE 7.5 smoke-test
comparison remains at
`calculations/bulk-silicon/qe-7.5-si-scf-smoke-comparison/`. This example introduces no
provenance schema or duplicate calculated-result record.
