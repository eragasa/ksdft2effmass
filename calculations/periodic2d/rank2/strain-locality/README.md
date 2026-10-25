# Periodic 2-D rank-two synthetic-strain locality calculation

This calculation owns the bounded area-preserving rhombic triangular-to-square synthetic-strain controls used by the Paper B development study.

- Root `run_development.py`, `run_response_development.py`, and
  `run_scan_development.py` are the M0 geometry, M1/M2 response, and scan workflow
  entrypoints.
- `analysis/development/` owns replaceable results and figures for the three development channels.
- `technical-report/technical-report.md` records the calculation-facing scope and evidence boundary.

The experiment specification remains at [`experiments/model-adequacy/periodic2d/gauge-locality-under-synthetic-strain/`](../../../../experiments/model-adequacy/periodic2d/gauge-locality-under-synthetic-strain/). This controlled path is not an elastic or graphene material model, and no retained production package exists.
