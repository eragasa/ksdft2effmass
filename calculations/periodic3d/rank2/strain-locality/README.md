# Periodic 3-D rank-two synthetic-strain locality outputs

The synthetic-strain study retains its identity and scientific interpretation under
[`experiments/model-adequacy/periodic3d/gauge-locality-under-synthetic-strain/`](../../../../experiments/model-adequacy/periodic3d/gauge-locality-under-synthetic-strain/).
This calculation directory owns its executable M0, M1/M2, and scan composition plus
calculation-facing development outputs and technical-report material.

- `run_development.py`, `run_response_development.py`, and
  `run_scan_development.py` are the maintained development entrypoints.
- `analysis/development/` holds replaceable results and figures for the development
  channels.
- `technical-report/technical-report.md` records the calculation-facing scope and
  evidence boundary.

This controlled path is not a phase-stability or bulk-silicon calculation, and no
retained production package exists.

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
| Experiment owner | The periodic-3D experiment path retains identity and protocol interpretation; duplicate entrypoints and output-path contracts are retired. |
| Cross-dimensional comparison schemas | Downstream donor/consumer surfaces for M0/M1/M2/witness/scan documents, not this family's authoritative wire owner. |
