# Periodic 3-D rank-two synthetic-strain locality calculation

This calculation owns the bounded volume-preserving FCC-to-BCC Bain synthetic-strain controls used by the Paper B development study.

- Root `run_development.py`, `run_response_development.py`, and
  `run_scan_development.py` are the M0 geometry, M1/M2 response, and scan workflow
  entrypoints.
- `analysis/development/` owns replaceable results and figures for the three development channels.
- `technical-report/technical-report.md` records the calculation-facing scope and evidence boundary.

The experiment specification remains at [`experiments/model-adequacy/periodic3d/gauge-locality-under-synthetic-strain/`](../../../../experiments/model-adequacy/periodic3d/gauge-locality-under-synthetic-strain/). This controlled path is not a phase-stability or bulk-silicon calculation, and no retained production package exists.
