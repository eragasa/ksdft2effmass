# Band equivalence and hopping locality along the Bain path

This aggregate owns the unit-primitive-volume periodic-3D rank-two Bain-path study,
including the common FCC-to-Bain coordinate map and the distinct M0, M1, M2, witness,
and sampled scan channels. The parent context keeps gauge alignment, frame transport,
band equivalence, hopping locality, and support truncation separate.

- [`protocol.md`](protocol.md) is the authoritative research protocol.
- `run_geometry_control.py` owns the M0 geometry/frozen-gauge locality action.
- `run_response_controls.py` owns separately labeled M1 frozen and M2 prescribed radial
  response actions.
- `run_path_scan.py` owns qualification witnesses, the 201-point base scan, and declared
  transition refinement.
- `analysis/replaceable/` holds replaceable results and figures.
- `technical-report/technical-report.md` records scope, current observations, and evidence
  boundaries.

The path is a synthetic unit-volume geometry and response control. It is not an elastic,
phase-stability, martensitic-transition, silicon, or other material calculation. No
retained production package exists. The former experiment-tree location is a legacy
forward pointer only.

## Migration inventory

This README owns the local inventory; [`migration.md`](migration.md) owns the distributed
checklist.

| Surface | Current disposition |
|---|---|
| M0 geometry/frozen-gauge control | Separate unit-volume Bain-path action and output role. |
| M1 four-state response control | Separate frozen-response channel; it is not merged with M0. |
| M2 prescribed radial-response control | Separate nonzero synthetic response; not a material phase response. |
| Common-cell qualification and scan | Distinct witness, qualification, and transition records. |
| Rendering | Replaceable development products, not authenticated execution figures. |
| Legacy experiment donor | The calculation owner holds identity and protocol authority; the legacy path points forward. |
| Cross-dimensional comparison | Downstream consumer only; it does not own these wire records or claims. |
