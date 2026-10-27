# Periodic 3-D rank-two synthetic-strain locality calculation

This calculation owns the bounded volume-preserving FCC-to-BCC Bain synthetic-strain controls used by the Paper B development study.

- Root `run_development.py`, `run_response_development.py`, and
  `run_scan_development.py` are the M0 geometry, M1/M2 response, and scan workflow
  entrypoints.
- `analysis/development/` owns replaceable results and figures for the three development channels.
- `technical-report/technical-report.md` records the calculation-facing scope and evidence boundary.

The experiment specification remains at [`experiments/model-adequacy/periodic3d/gauge-locality-under-synthetic-strain/`](../../../../experiments/model-adequacy/periodic3d/gauge-locality-under-synthetic-strain/). This controlled path is not a phase-stability or bulk-silicon calculation, and no retained production package exists.

## Migration inventory

This README owns the complete local inventory; [`migration.md`](migration.md) owns its
distributed checklist.

| Surface | Current disposition |
|---|---|
| M0 geometry/frozen-response control | Separate unit-volume Bain-path development channel. |
| M1 four-state response control | Separate response channel; it must not be merged with M0. |
| M2 prescribed radial-response control | Separate nonzero synthetic response channel; not a material phase response. |
| Common-cell qualification witness and parameter scan | Distinct diagnostic/scan dependencies with separate output roles. |
| Response and scan rendering | Replaceable development products, not authenticated execution figures. |
| Experiment migration source | Nine tracked files under the periodic-3D strain experiment path contain M0/response/scan composition and analysis path contracts; all must move here or receive a provenance-only disposition. |
| Cross-dimensional comparison schemas | Downstream donor/consumer surfaces for M0/M1/M2/witness/scan documents, not this family's authoritative wire owner. |
