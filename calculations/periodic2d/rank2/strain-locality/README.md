# Periodic 2-D rank-two synthetic-strain locality outputs

The synthetic-strain study is an experiment. Its maintained composition and analysis
entrypoints are owned by
[`experiments/model-adequacy/periodic2d/gauge-locality-under-synthetic-strain/`](../../../../experiments/model-adequacy/periodic2d/gauge-locality-under-synthetic-strain/).
This calculation directory retains calculation-facing development outputs and technical
report material; it does not own or redefine the experiment.

- `analysis/development/` holds replaceable results and figures for the development
  channels.
- `technical-report/technical-report.md` records the calculation-facing scope and
  evidence boundary.

This controlled path is not an elastic or graphene material model, and no retained
production package exists.

## Migration inventory

This README owns the complete local inventory; [`migration.md`](migration.md) owns its
distributed checklist.

| Surface | Current disposition |
|---|---|
| M0 geometry/frozen-response control | Separate development entry point and output role. |
| M1 four-state response control | Separate response channel; it must not be merged with M0. |
| M2 prescribed radial-response control | Separate nonzero synthetic response channel; not a material response model. |
| Qualification witness and parameter scan | Distinct diagnostic/scan dependencies with separate output roles. |
| Response and scan rendering | Replaceable development products, not authenticated execution figures. |
| Experiment owner | The periodic-2D experiment path retains M0/response/scan composition and analysis path contracts. |
| Cross-dimensional comparison schemas | Downstream donor/consumer surfaces for M0/M1/M2/witness/scan documents, not this family's authoritative wire owner. |
