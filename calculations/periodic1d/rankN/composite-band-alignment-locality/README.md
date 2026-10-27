# Periodic 1-D higher-rank composite-band alignment and locality

**Status:** schema-free development calculation; no retained run or evidence package.

This calculation owns the one-dimensional higher-rank composition used by the Paper C development program. The selected finite ladder contains retained ranks `3, 4, 8, 16`, rotation depths `1, 2, 4, 8`, and four alignment controls: no alignment, one global alignment, pointwise complete alignment, and a known-inverse oracle.

- [`workflow/`](workflow/) owns the calculation-specific definitions, records, model composition, alignment, transport, and execution workflow.
- [`run_development.py`](run_development.py) and [`verify_analytic_controls.py`](verify_analytic_controls.py) are thin calculation entrypoints documented under [`simulations/development/`](simulations/development/README.md).
- [`analysis/development/`](analysis/development/README.md) records the future derived-analysis boundary.
- [`technical-report/technical_report.tex`](technical-report/technical_report.tex) is the calculation-facing report.

The scientific protocol remains under [`experiments/periodic-reduction/higher-rank-composite-band-alignment-and-locality/`](../../../../experiments/periodic-reduction/higher-rank-composite-band-alignment-and-locality/). Reusable matrix-field diagnostics and external numerical capabilities remain under their canonical library owners; the bounded rank/depth campaign workflow is calculation-owned here.

The current producer writes only an ignored, replaceable summary. Strict serialization, a complete producer-independent verifier, retained composition, two- and three-dimensional extensions, moving-subspace controls, complex-unitary controls, and restricted-circuit fitting remain absent.

## Migration inventory

This README owns the complete local inventory; [`migration.md`](migration.md) owns its
distributed checklist.

| Surface | Current disposition |
|---|---|
| D1 P0/G0 parent and 16-case rank/depth ladder | Implemented in the calculation-local `workflow/`; outputs are replaceable and schema-free. |
| Alignment channels A0--A3 | No alignment, global, pointwise, and known-inverse oracle are implemented and remain distinct. |
| Model, Procrustes, sewing, transport, Fourier, ledger, and failure-disposition operations | Split across calculation-local modules and tests; owner extraction remains incomplete. |
| Analytic controls | A bounded sanity-check entry point exists; it is not a full independent result verifier. |
| Experiment migration source | Five tracked files under `experiments/periodic-reduction/higher-rank-composite-band-alignment-and-locality/`: protocol manuscript, README, producer, control verifier, and ignore contract. Its documented `campaigns.periodic_reduction.higher_rank_d1` path is absent and must be reconciled with this calculation-local implementation. |
| P1, G1, A4, complex-unitary, moving-subspace, 2-D, and 3-D branches | Prospective and absent; no placeholder implementation or inherited result. |
