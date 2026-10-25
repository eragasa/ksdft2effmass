# Periodic 1-D higher-rank composite-band alignment and locality

**Status:** schema-free development calculation; no retained run or evidence package.

This calculation owns the one-dimensional higher-rank composition used by the Paper C development program. The selected finite ladder contains retained ranks `3, 4, 8, 16`, rotation depths `1, 2, 4, 8`, and four alignment controls: no alignment, one global alignment, pointwise complete alignment, and a known-inverse oracle.

- [`workflow/`](workflow/) owns the calculation-specific definitions, records, model composition, alignment, transport, and execution workflow.
- [`run_development.py`](run_development.py) and [`verify_analytic_controls.py`](verify_analytic_controls.py) are thin calculation entrypoints documented under [`simulations/development/`](simulations/development/README.md).
- [`analysis/development/`](analysis/development/README.md) records the future derived-analysis boundary.
- [`technical-report/technical_report.tex`](technical-report/technical_report.tex) is the calculation-facing report.

The scientific protocol remains under [`experiments/periodic-reduction/higher-rank-composite-band-alignment-and-locality/`](../../../../experiments/periodic-reduction/higher-rank-composite-band-alignment-and-locality/). Reusable matrix-field diagnostics and external numerical capabilities remain under their canonical library owners; the bounded rank/depth campaign workflow is calculation-owned here.

The current producer writes only an ignored, replaceable summary. Strict serialization, a complete producer-independent verifier, retained composition, two- and three-dimensional extensions, moving-subspace controls, complex-unitary controls, and restricted-circuit fitting remain absent.
