# Periodic 3-D rank-two orthogonal band-equivalence/locality calculation

This calculation owns the simple-cubic controlled-model composition used by the Paper B
development study. The retained subspace has rank two; three-dimensional space does not
imply retained rank three.

## Installed direct lifecycle

The bounded nominal request is composed directly by:

1. `run_01_calculation.py`, which writes canonical typed request and result bytes;
2. `run_02_verification.py`, which owns the exact result bytes and reconstructs the
   decisive finite checks through the independent route; and
3. `run_03_render.py`, which readmits the stored verification and authenticated
   projection before rendering the closed figure inventory.

The scripts reserve execution identity `direct-simple-cubic-rank2-n8`. They define an
`8 x 8 x 8` construction mesh, a shifted `17 x 17 x 17` evaluation mesh, parent scales
`0` and `1`, amplitudes `0`, `pi/8`, and `pi/4`, and complete cubic metric shells through
squared radius `9`. They use module-scope composition, domain-owned `BaseTypedRecord`
lifecycle documents through `to_json()`/`from_json()`, exact canonical bytes,
no-overwrite gates, incomplete-stage directories, and atomic renames. They do not use a
Workflow, loose lifecycle mapping, custom serializer, registry, reflection, or legacy
compatibility path.

No periodic-3D execution is created or retained by this installation change. Running a
stage against this calculation root is a separate operation. The scripts do not perform
refinement, sealing, evidence promotion, publication, Quantum ESPRESSO, or Wannier90
execution.

## Development surfaces

`run_development.py` and `plot_development.py` remain replaceable development surfaces.
`analysis/development/` documents development diagnostics and generated figures;
`technical-report/technical-report.md` records the calculation-facing scope and evidence
boundary. These surfaces are not direct-stage inputs and are not authenticated execution
artifacts.

The experiment protocol remains at
[`experiments/model-adequacy/periodic3d/band-equivalence-versus-hopping-locality/`](../../../../../experiments/model-adequacy/periodic3d/band-equivalence-versus-hopping-locality/).
The direct lifecycle does not promote development outputs or establish convergence,
uncertainty quantification, material validity, or publication acceptance.

## Migration inventory

This README owns the complete local inventory; [`migration.md`](migration.md) owns its
distributed checklist.

| Surface | Current disposition |
|---|---|
| Simple-cubic nominal calculation | Typed direct calculate → independently verify → authenticated render composition installed; no execution retained. |
| Mesh refinement | Outside the direct lifecycle; development records do not establish convergence. |
| Typed ownership | Shared immutable request, result, independent-reference, verification, and visualization owners live under `python/src/ksdft2effmass/analysis/model_adequacy/band_equivalence_locality/`. |
| Plotting and technical report | Development products remain separate from authenticated direct rendering. |
| Cross-dimensional comparison | Downstream consumer only; it cannot transfer identity, normalization, tolerance policy, or evidence status. |
