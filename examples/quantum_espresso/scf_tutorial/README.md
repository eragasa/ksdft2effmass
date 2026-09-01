# Quantum ESPRESSO silicon SCF tutorial input

This software example reconstructs the retained QE 7.2 `example01` silicon
Davidson SCF input using upstream-selected grouping tags, `QePwInputFile`, and
`QePwInputFileWriter`.

Run the example test from the repository root:

```bash
uv run --project python --extra dev pytest -q \
  examples/quantum_espresso/scf_tutorial/test_scf_tutorial.py
```

The test writes no files and does not invoke Quantum ESPRESSO. The portable input
uses `./pseudo/` and `./scratch/` instead of the original machine-local paths.
The original retained input and execution record remain at
`calculations/bulk-silicon/qe-example01-si-scf-davidson/`; this example introduces
no provenance schema or duplicate provenance record.
