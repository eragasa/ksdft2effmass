# Quantum ESPRESSO 7.2 bundled examples campaign

## Purpose

This inventory defines inactive Tasks for the runnable examples discovered in the locally inspected Quantum ESPRESSO 7.2 source snapshot. It is an inventory and proposed-work record, not evidence that any example was executed or that any bundled setting is suitable for project production calculations.

The generic parent is [`quantumespresso.simulations`](../../tasks/simulation/quantumespresso.simulations.json). The authoritative campaign record is [`quantumespresso.simulations.qe_examples`](../../tasks/simulation/quantumespresso.simulations.qe_examples.json).

## Inspected source identity

- Inspected local source root: `/Users/eugene/projects/q-e-qe-7.2` (external to this repository).
- Version declaration: `include/qe_version.h` reports `7.2`.
- Version-header SHA-256: `d82a82f1ae1c97923343304ed8a8cd4629d5c6643c4aed5b63083b238dc62316`.
- Top-level `License` SHA-256: `204d8eff92f95aac4df6c8122bc1505f468f3a901e5a4cc08940e0ede1938994`; the inspected text is GNU GPL version 2.
- Discovered script count: **149**.
- Runnable task-group count: **134**.
- Component count: **13**.
- SHA-256 over sorted `source-relative-path\0file-sha256\n` entries: `5d7f657b55aa21195ad2f6af95b377054586c17b8fde0525e68471596a72ddcf`.

The extracted source directory is not a Git checkout, so no commit identity is available. Every child therefore remains blocked on exact source-identity confirmation during its own preflight. Pseudopotentials, downloaded inputs, and other separately distributed assets require their own identities and reuse terms; the top-level QE license is not treated as covering them automatically.

## Grouping rule

One Task owns the cohesive scripts within one example directory. Multiple related `run_example*` variants in the same directory remain one Task to avoid artificial micro-tasks. Root-level XSpectra scripts represent separately named examples and therefore receive separate Tasks. The single FFTXlib root-level script receives one Task. This yields 134 runnable groups for 149 scripts.

## Component summary

| Component | Runnable groups | Scripts |
|---|---:|---:|
| `CPV` | 12 | 12 |
| `FFTXlib` | 1 | 1 |
| `GWW` | 6 | 6 |
| `HP` | 10 | 10 |
| `KCW` | 3 | 3 |
| `NEB` | 2 | 5 |
| `PHonon` | 26 | 32 |
| `PP` | 21 | 21 |
| `PW` | 24 | 30 |
| `PWCOND` | 3 | 3 |
| `QEHeat` | 3 | 3 |
| `TDDFPT` | 19 | 19 |
| `XSpectra` | 4 | 4 |

## Runnable-group task inventory

| Task | Source group | Candidate scripts |
|---|---|---|
| [`quantumespresso.simulations.qe_examples.cpv.autopilot-example`](../../tasks/simulation/quantumespresso.simulations.qe_examples.cpv.autopilot-example.json) | `CPV/examples/autopilot-example` | `CPV/examples/autopilot-example/run_example_water` |
| [`quantumespresso.simulations.qe_examples.cpv.example01`](../../tasks/simulation/quantumespresso.simulations.qe_examples.cpv.example01.json) | `CPV/examples/example01` | `CPV/examples/example01/run_example` |
| [`quantumespresso.simulations.qe_examples.cpv.example02`](../../tasks/simulation/quantumespresso.simulations.qe_examples.cpv.example02.json) | `CPV/examples/example02` | `CPV/examples/example02/run_example` |
| [`quantumespresso.simulations.qe_examples.cpv.example03`](../../tasks/simulation/quantumespresso.simulations.qe_examples.cpv.example03.json) | `CPV/examples/example03` | `CPV/examples/example03/run_example` |
| [`quantumespresso.simulations.qe_examples.cpv.example04`](../../tasks/simulation/quantumespresso.simulations.qe_examples.cpv.example04.json) | `CPV/examples/example04` | `CPV/examples/example04/run_example` |
| [`quantumespresso.simulations.qe_examples.cpv.example05`](../../tasks/simulation/quantumespresso.simulations.qe_examples.cpv.example05.json) | `CPV/examples/example05` | `CPV/examples/example05/run_example` |
| [`quantumespresso.simulations.qe_examples.cpv.example06`](../../tasks/simulation/quantumespresso.simulations.qe_examples.cpv.example06.json) | `CPV/examples/example06` | `CPV/examples/example06/run_example` |
| [`quantumespresso.simulations.qe_examples.cpv.example07`](../../tasks/simulation/quantumespresso.simulations.qe_examples.cpv.example07.json) | `CPV/examples/example07` | `CPV/examples/example07/run_example` |
| [`quantumespresso.simulations.qe_examples.cpv.example08`](../../tasks/simulation/quantumespresso.simulations.qe_examples.cpv.example08.json) | `CPV/examples/example08` | `CPV/examples/example08/run_example` |
| [`quantumespresso.simulations.qe_examples.cpv.example09`](../../tasks/simulation/quantumespresso.simulations.qe_examples.cpv.example09.json) | `CPV/examples/example09` | `CPV/examples/example09/run_example` |
| [`quantumespresso.simulations.qe_examples.cpv.extffield-example`](../../tasks/simulation/quantumespresso.simulations.qe_examples.cpv.extffield-example.json) | `CPV/examples/Extffield_example` | `CPV/examples/Extffield_example/run_example` |
| [`quantumespresso.simulations.qe_examples.cpv.restart-example`](../../tasks/simulation/quantumespresso.simulations.qe_examples.cpv.restart-example.json) | `CPV/examples/Restart_example` | `CPV/examples/Restart_example/run_example` |
| [`quantumespresso.simulations.qe_examples.fftxlib.root`](../../tasks/simulation/quantumespresso.simulations.qe_examples.fftxlib.root.json) | `FFTXlib/examples` | `FFTXlib/examples/run_example` |
| [`quantumespresso.simulations.qe_examples.gww.example01`](../../tasks/simulation/quantumespresso.simulations.qe_examples.gww.example01.json) | `GWW/examples/example01` | `GWW/examples/example01/run_example` |
| [`quantumespresso.simulations.qe_examples.gww.example02`](../../tasks/simulation/quantumespresso.simulations.qe_examples.gww.example02.json) | `GWW/examples/example02` | `GWW/examples/example02/run_example` |
| [`quantumespresso.simulations.qe_examples.gww.example03`](../../tasks/simulation/quantumespresso.simulations.qe_examples.gww.example03.json) | `GWW/examples/example03` | `GWW/examples/example03/run_example` |
| [`quantumespresso.simulations.qe_examples.gww.example04`](../../tasks/simulation/quantumespresso.simulations.qe_examples.gww.example04.json) | `GWW/examples/example04` | `GWW/examples/example04/run_example` |
| [`quantumespresso.simulations.qe_examples.gww.example05`](../../tasks/simulation/quantumespresso.simulations.qe_examples.gww.example05.json) | `GWW/examples/example05` | `GWW/examples/example05/run_example` |
| [`quantumespresso.simulations.qe_examples.gww.example06`](../../tasks/simulation/quantumespresso.simulations.qe_examples.gww.example06.json) | `GWW/examples/example06` | `GWW/examples/example06/run_example` |
| [`quantumespresso.simulations.qe_examples.hp.example01`](../../tasks/simulation/quantumespresso.simulations.qe_examples.hp.example01.json) | `HP/examples/example01` | `HP/examples/example01/run_example` |
| [`quantumespresso.simulations.qe_examples.hp.example02`](../../tasks/simulation/quantumespresso.simulations.qe_examples.hp.example02.json) | `HP/examples/example02` | `HP/examples/example02/run_example` |
| [`quantumespresso.simulations.qe_examples.hp.example03`](../../tasks/simulation/quantumespresso.simulations.qe_examples.hp.example03.json) | `HP/examples/example03` | `HP/examples/example03/run_example` |
| [`quantumespresso.simulations.qe_examples.hp.example04`](../../tasks/simulation/quantumespresso.simulations.qe_examples.hp.example04.json) | `HP/examples/example04` | `HP/examples/example04/run_example` |
| [`quantumespresso.simulations.qe_examples.hp.example05`](../../tasks/simulation/quantumespresso.simulations.qe_examples.hp.example05.json) | `HP/examples/example05` | `HP/examples/example05/run_example` |
| [`quantumespresso.simulations.qe_examples.hp.example06`](../../tasks/simulation/quantumespresso.simulations.qe_examples.hp.example06.json) | `HP/examples/example06` | `HP/examples/example06/run_example` |
| [`quantumespresso.simulations.qe_examples.hp.example07`](../../tasks/simulation/quantumespresso.simulations.qe_examples.hp.example07.json) | `HP/examples/example07` | `HP/examples/example07/run_example` |
| [`quantumespresso.simulations.qe_examples.hp.example08`](../../tasks/simulation/quantumespresso.simulations.qe_examples.hp.example08.json) | `HP/examples/example08` | `HP/examples/example08/run_example` |
| [`quantumespresso.simulations.qe_examples.hp.example09`](../../tasks/simulation/quantumespresso.simulations.qe_examples.hp.example09.json) | `HP/examples/example09` | `HP/examples/example09/run_example` |
| [`quantumespresso.simulations.qe_examples.hp.example10`](../../tasks/simulation/quantumespresso.simulations.qe_examples.hp.example10.json) | `HP/examples/example10` | `HP/examples/example10/run_example` |
| [`quantumespresso.simulations.qe_examples.kcw.example01`](../../tasks/simulation/quantumespresso.simulations.qe_examples.kcw.example01.json) | `KCW/examples/example01` | `KCW/examples/example01/run_example` |
| [`quantumespresso.simulations.qe_examples.kcw.example02`](../../tasks/simulation/quantumespresso.simulations.qe_examples.kcw.example02.json) | `KCW/examples/example02` | `KCW/examples/example02/run_example` |
| [`quantumespresso.simulations.qe_examples.kcw.example03`](../../tasks/simulation/quantumespresso.simulations.qe_examples.kcw.example03.json) | `KCW/examples/example03` | `KCW/examples/example03/run_example` |
| [`quantumespresso.simulations.qe_examples.neb.esm-example`](../../tasks/simulation/quantumespresso.simulations.qe_examples.neb.esm-example.json) | `NEB/examples/ESM_example` | `NEB/examples/ESM_example/run_example`<br>`NEB/examples/ESM_example/run_example_ESM`<br>`NEB/examples/ESM_example/run_example_FCP`<br>`NEB/examples/ESM_example/run_example_GCSCF` |
| [`quantumespresso.simulations.qe_examples.neb.example01`](../../tasks/simulation/quantumespresso.simulations.qe_examples.neb.example01.json) | `NEB/examples/example01` | `NEB/examples/example01/run_example` |
| [`quantumespresso.simulations.qe_examples.phonon.example01`](../../tasks/simulation/quantumespresso.simulations.qe_examples.phonon.example01.json) | `PHonon/examples/example01` | `PHonon/examples/example01/run_example` |
| [`quantumespresso.simulations.qe_examples.phonon.example014`](../../tasks/simulation/quantumespresso.simulations.qe_examples.phonon.example014.json) | `PHonon/examples/example014` | `PHonon/examples/example014/run_example_ep_simple` |
| [`quantumespresso.simulations.qe_examples.phonon.example02`](../../tasks/simulation/quantumespresso.simulations.qe_examples.phonon.example02.json) | `PHonon/examples/example02` | `PHonon/examples/example02/run_example` |
| [`quantumespresso.simulations.qe_examples.phonon.example03`](../../tasks/simulation/quantumespresso.simulations.qe_examples.phonon.example03.json) | `PHonon/examples/example03` | `PHonon/examples/example03/run_example` |
| [`quantumespresso.simulations.qe_examples.phonon.example04`](../../tasks/simulation/quantumespresso.simulations.qe_examples.phonon.example04.json) | `PHonon/examples/example04` | `PHonon/examples/example04/run_example` |
| [`quantumespresso.simulations.qe_examples.phonon.example05`](../../tasks/simulation/quantumespresso.simulations.qe_examples.phonon.example05.json) | `PHonon/examples/example05` | `PHonon/examples/example05/run_example` |
| [`quantumespresso.simulations.qe_examples.phonon.example06`](../../tasks/simulation/quantumespresso.simulations.qe_examples.phonon.example06.json) | `PHonon/examples/example06` | `PHonon/examples/example06/run_example` |
| [`quantumespresso.simulations.qe_examples.phonon.example07`](../../tasks/simulation/quantumespresso.simulations.qe_examples.phonon.example07.json) | `PHonon/examples/example07` | `PHonon/examples/example07/run_example` |
| [`quantumespresso.simulations.qe_examples.phonon.example08`](../../tasks/simulation/quantumespresso.simulations.qe_examples.phonon.example08.json) | `PHonon/examples/example08` | `PHonon/examples/example08/run_example` |
| [`quantumespresso.simulations.qe_examples.phonon.example09`](../../tasks/simulation/quantumespresso.simulations.qe_examples.phonon.example09.json) | `PHonon/examples/example09` | `PHonon/examples/example09/run_example` |
| [`quantumespresso.simulations.qe_examples.phonon.example10`](../../tasks/simulation/quantumespresso.simulations.qe_examples.phonon.example10.json) | `PHonon/examples/example10` | `PHonon/examples/example10/run_example` |
| [`quantumespresso.simulations.qe_examples.phonon.example11`](../../tasks/simulation/quantumespresso.simulations.qe_examples.phonon.example11.json) | `PHonon/examples/example11` | `PHonon/examples/example11/run_example` |
| [`quantumespresso.simulations.qe_examples.phonon.example12`](../../tasks/simulation/quantumespresso.simulations.qe_examples.phonon.example12.json) | `PHonon/examples/example12` | `PHonon/examples/example12/run_example` |
| [`quantumespresso.simulations.qe_examples.phonon.example13`](../../tasks/simulation/quantumespresso.simulations.qe_examples.phonon.example13.json) | `PHonon/examples/example13` | `PHonon/examples/example13/run_example` |
| [`quantumespresso.simulations.qe_examples.phonon.example14`](../../tasks/simulation/quantumespresso.simulations.qe_examples.phonon.example14.json) | `PHonon/examples/example14` | `PHonon/examples/example14/run_example` |
| [`quantumespresso.simulations.qe_examples.phonon.example15`](../../tasks/simulation/quantumespresso.simulations.qe_examples.phonon.example15.json) | `PHonon/examples/example15` | `PHonon/examples/example15/run_example` |
| [`quantumespresso.simulations.qe_examples.phonon.example16`](../../tasks/simulation/quantumespresso.simulations.qe_examples.phonon.example16.json) | `PHonon/examples/example16` | `PHonon/examples/example16/run_example` |
| [`quantumespresso.simulations.qe_examples.phonon.example17`](../../tasks/simulation/quantumespresso.simulations.qe_examples.phonon.example17.json) | `PHonon/examples/example17` | `PHonon/examples/example17/run_example` |
| [`quantumespresso.simulations.qe_examples.phonon.example18`](../../tasks/simulation/quantumespresso.simulations.qe_examples.phonon.example18.json) | `PHonon/examples/example18` | `PHonon/examples/example18/run_example` |
| [`quantumespresso.simulations.qe_examples.phonon.example19`](../../tasks/simulation/quantumespresso.simulations.qe_examples.phonon.example19.json) | `PHonon/examples/example19` | `PHonon/examples/example19/run_example` |
| [`quantumespresso.simulations.qe_examples.phonon.grid-example`](../../tasks/simulation/quantumespresso.simulations.qe_examples.phonon.grid-example.json) | `PHonon/examples/GRID_example` | `PHonon/examples/GRID_example/run_example`<br>`PHonon/examples/GRID_example/run_example_1`<br>`PHonon/examples/GRID_example/run_example_2`<br>`PHonon/examples/GRID_example/run_example_3` |
| [`quantumespresso.simulations.qe_examples.phonon.grid-recover-example`](../../tasks/simulation/quantumespresso.simulations.qe_examples.phonon.grid-recover-example.json) | `PHonon/examples/GRID_recover_example` | `PHonon/examples/GRID_recover_example/run_example`<br>`PHonon/examples/GRID_recover_example/run_example_2` |
| [`quantumespresso.simulations.qe_examples.phonon.image-example`](../../tasks/simulation/quantumespresso.simulations.qe_examples.phonon.image-example.json) | `PHonon/examples/Image_example` | `PHonon/examples/Image_example/run_example`<br>`PHonon/examples/Image_example/run_example_1` |
| [`quantumespresso.simulations.qe_examples.phonon.partial-example`](../../tasks/simulation/quantumespresso.simulations.qe_examples.phonon.partial-example.json) | `PHonon/examples/Partial_example` | `PHonon/examples/Partial_example/run_example` |
| [`quantumespresso.simulations.qe_examples.phonon.recover-example`](../../tasks/simulation/quantumespresso.simulations.qe_examples.phonon.recover-example.json) | `PHonon/examples/Recover_example` | `PHonon/examples/Recover_example/run_example`<br>`PHonon/examples/Recover_example/run_example_1` |
| [`quantumespresso.simulations.qe_examples.phonon.tetra-example`](../../tasks/simulation/quantumespresso.simulations.qe_examples.phonon.tetra-example.json) | `PHonon/examples/tetra_example` | `PHonon/examples/tetra_example/run_example` |
| [`quantumespresso.simulations.qe_examples.pp.acf-example`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pp.acf-example.json) | `PP/examples/ACF_example` | `PP/examples/ACF_example/run_example` |
| [`quantumespresso.simulations.qe_examples.pp.bgw-example`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pp.bgw-example.json) | `PP/examples/BGW_example` | `PP/examples/BGW_example/run_example` |
| [`quantumespresso.simulations.qe_examples.pp.cls-fs-example`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pp.cls-fs-example.json) | `PP/examples/CLS_FS_example` | `PP/examples/CLS_FS_example/run_example` |
| [`quantumespresso.simulations.qe_examples.pp.cls-is-example`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pp.cls-is-example.json) | `PP/examples/CLS_IS_example` | `PP/examples/CLS_IS_example/run_example` |
| [`quantumespresso.simulations.qe_examples.pp.dipole-example`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pp.dipole-example.json) | `PP/examples/dipole_example` | `PP/examples/dipole_example/run_example` |
| [`quantumespresso.simulations.qe_examples.pp.example01`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pp.example01.json) | `PP/examples/example01` | `PP/examples/example01/run_example` |
| [`quantumespresso.simulations.qe_examples.pp.example02`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pp.example02.json) | `PP/examples/example02` | `PP/examples/example02/run_example` |
| [`quantumespresso.simulations.qe_examples.pp.example03`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pp.example03.json) | `PP/examples/example03` | `PP/examples/example03/run_example` |
| [`quantumespresso.simulations.qe_examples.pp.example04`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pp.example04.json) | `PP/examples/example04` | `PP/examples/example04/run_example` |
| [`quantumespresso.simulations.qe_examples.pp.example05`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pp.example05.json) | `PP/examples/example05` | `PP/examples/example05/run_example` |
| [`quantumespresso.simulations.qe_examples.pp.example06`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pp.example06.json) | `PP/examples/example06` | `PP/examples/example06/run_example` |
| [`quantumespresso.simulations.qe_examples.pp.exx-scf-bands-example`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pp.exx-scf-bands-example.json) | `PP/examples/exx_scf_bands_example` | `PP/examples/exx_scf_bands_example/run_example` |
| [`quantumespresso.simulations.qe_examples.pp.fermisurf-example`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pp.fermisurf-example.json) | `PP/examples/fermisurf_example` | `PP/examples/fermisurf_example/run_example` |
| [`quantumespresso.simulations.qe_examples.pp.force-theorem-example`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pp.force-theorem-example.json) | `PP/examples/ForceTheorem_example` | `PP/examples/ForceTheorem_example/run_example` |
| [`quantumespresso.simulations.qe_examples.pp.mol-dos-example`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pp.mol-dos-example.json) | `PP/examples/MolDos_example` | `PP/examples/MolDos_example/run_example` |
| [`quantumespresso.simulations.qe_examples.pp.projected-bands-example`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pp.projected-bands-example.json) | `PP/examples/projected_bands_example` | `PP/examples/projected_bands_example/run_example` |
| [`quantumespresso.simulations.qe_examples.pp.pw2gw-example`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pp.pw2gw-example.json) | `PP/examples/pw2gw_example` | `PP/examples/pw2gw_example/run_example` |
| [`quantumespresso.simulations.qe_examples.pp.w90-open-grid-example`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pp.w90-open-grid-example.json) | `PP/examples/W90_open_grid_example` | `PP/examples/W90_open_grid_example/run_example` |
| [`quantumespresso.simulations.qe_examples.pp.wan90-example`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pp.wan90-example.json) | `PP/examples/WAN90_example` | `PP/examples/WAN90_example/run_example` |
| [`quantumespresso.simulations.qe_examples.pp.wannier-ham-example`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pp.wannier-ham-example.json) | `PP/examples/WannierHam_example` | `PP/examples/WannierHam_example/run_example` |
| [`quantumespresso.simulations.qe_examples.pp.work-fct-example`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pp.work-fct-example.json) | `PP/examples/WorkFct_example` | `PP/examples/WorkFct_example/run_example` |
| [`quantumespresso.simulations.qe_examples.pw.cluster-example`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pw.cluster-example.json) | `PW/examples/cluster_example` | `PW/examples/cluster_example/run_example` |
| [`quantumespresso.simulations.qe_examples.pw.dftd3-example`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pw.dftd3-example.json) | `PW/examples/dftd3_example` | `PW/examples/dftd3_example/run_example` |
| [`quantumespresso.simulations.qe_examples.pw.esm-example`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pw.esm-example.json) | `PW/examples/ESM_example` | `PW/examples/ESM_example/run_example`<br>`PW/examples/ESM_example/run_example_ESM`<br>`PW/examples/ESM_example/run_example_FCP`<br>`PW/examples/ESM_example/run_example_GCSCF` |
| [`quantumespresso.simulations.qe_examples.pw.example01`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pw.example01.json) | `PW/examples/example01` | `PW/examples/example01/run_example` |
| [`quantumespresso.simulations.qe_examples.pw.example02`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pw.example02.json) | `PW/examples/example02` | `PW/examples/example02/run_example` |
| [`quantumespresso.simulations.qe_examples.pw.example03`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pw.example03.json) | `PW/examples/example03` | `PW/examples/example03/run_example` |
| [`quantumespresso.simulations.qe_examples.pw.example04`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pw.example04.json) | `PW/examples/example04` | `PW/examples/example04/run_example` |
| [`quantumespresso.simulations.qe_examples.pw.example05`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pw.example05.json) | `PW/examples/example05` | `PW/examples/example05/run_example` |
| [`quantumespresso.simulations.qe_examples.pw.example06`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pw.example06.json) | `PW/examples/example06` | `PW/examples/example06/run_example` |
| [`quantumespresso.simulations.qe_examples.pw.example07`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pw.example07.json) | `PW/examples/example07` | `PW/examples/example07/run_example` |
| [`quantumespresso.simulations.qe_examples.pw.example08`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pw.example08.json) | `PW/examples/example08` | `PW/examples/example08/run_example` |
| [`quantumespresso.simulations.qe_examples.pw.example09`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pw.example09.json) | `PW/examples/example09` | `PW/examples/example09/run_example` |
| [`quantumespresso.simulations.qe_examples.pw.example10`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pw.example10.json) | `PW/examples/example10` | `PW/examples/example10/run_example` |
| [`quantumespresso.simulations.qe_examples.pw.example11`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pw.example11.json) | `PW/examples/example11` | `PW/examples/example11/run_example` |
| [`quantumespresso.simulations.qe_examples.pw.example12`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pw.example12.json) | `PW/examples/example12` | `PW/examples/example12/run_example` |
| [`quantumespresso.simulations.qe_examples.pw.example13`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pw.example13.json) | `PW/examples/example13` | `PW/examples/example13/run_example` |
| [`quantumespresso.simulations.qe_examples.pw.example14`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pw.example14.json) | `PW/examples/example14` | `PW/examples/example14/run_example` |
| [`quantumespresso.simulations.qe_examples.pw.extffield-example`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pw.extffield-example.json) | `PW/examples/Extffield_example` | `PW/examples/Extffield_example/run_example` |
| [`quantumespresso.simulations.qe_examples.pw.exx-example`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pw.exx-example.json) | `PW/examples/EXX_example` | `PW/examples/EXX_example/run_example` |
| [`quantumespresso.simulations.qe_examples.pw.gamma-dft-example`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pw.gamma-dft-example.json) | `PW/examples/gammaDFT_example` | `PW/examples/gammaDFT_example/run_example` |
| [`quantumespresso.simulations.qe_examples.pw.gatefield`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pw.gatefield.json) | `PW/examples/gatefield` | `PW/examples/gatefield/run_example` |
| [`quantumespresso.simulations.qe_examples.pw.rism-example`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pw.rism-example.json) | `PW/examples/RISM_example` | `PW/examples/RISM_example/run_example`<br>`PW/examples/RISM_example/run_example_3D-RISM`<br>`PW/examples/RISM_example/run_example_ESM-RISM` |
| [`quantumespresso.simulations.qe_examples.pw.vcsexample`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pw.vcsexample.json) | `PW/examples/VCSexample` | `PW/examples/VCSexample/run_example` |
| [`quantumespresso.simulations.qe_examples.pw.vdw-df-example`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pw.vdw-df-example.json) | `PW/examples/vdwDF_example` | `PW/examples/vdwDF_example/run_example`<br>`PW/examples/vdwDF_example/run_example_delta_scf` |
| [`quantumespresso.simulations.qe_examples.pwcond.example01`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pwcond.example01.json) | `PWCOND/examples/example01` | `PWCOND/examples/example01/run_example` |
| [`quantumespresso.simulations.qe_examples.pwcond.example02`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pwcond.example02.json) | `PWCOND/examples/example02` | `PWCOND/examples/example02/run_example` |
| [`quantumespresso.simulations.qe_examples.pwcond.example03`](../../tasks/simulation/quantumespresso.simulations.qe_examples.pwcond.example03.json) | `PWCOND/examples/example03` | `PWCOND/examples/example03/run_example` |
| [`quantumespresso.simulations.qe_examples.qeheat.example-h2-o-trajectory`](../../tasks/simulation/quantumespresso.simulations.qe_examples.qeheat.example-h2-o-trajectory.json) | `QEHeat/examples/example_H2O_trajectory` | `QEHeat/examples/example_H2O_trajectory/run_example.sh` |
| [`quantumespresso.simulations.qe_examples.qeheat.example-si-o2-single`](../../tasks/simulation/quantumespresso.simulations.qe_examples.qeheat.example-si-o2-single.json) | `QEHeat/examples/example_SiO2_single` | `QEHeat/examples/example_SiO2_single/run_example.sh` |
| [`quantumespresso.simulations.qe_examples.qeheat.example-small-h20-trajectory`](../../tasks/simulation/quantumespresso.simulations.qe_examples.qeheat.example-small-h20-trajectory.json) | `QEHeat/examples/example_small_H20_trajectory` | `QEHeat/examples/example_small_H20_trajectory/run_example_water` |
| [`quantumespresso.simulations.qe_examples.tddfpt.example01`](../../tasks/simulation/quantumespresso.simulations.qe_examples.tddfpt.example01.json) | `TDDFPT/examples/example01` | `TDDFPT/examples/example01/run_example` |
| [`quantumespresso.simulations.qe_examples.tddfpt.example02`](../../tasks/simulation/quantumespresso.simulations.qe_examples.tddfpt.example02.json) | `TDDFPT/examples/example02` | `TDDFPT/examples/example02/run_example` |
| [`quantumespresso.simulations.qe_examples.tddfpt.example03`](../../tasks/simulation/quantumespresso.simulations.qe_examples.tddfpt.example03.json) | `TDDFPT/examples/example03` | `TDDFPT/examples/example03/run_example` |
| [`quantumespresso.simulations.qe_examples.tddfpt.example04`](../../tasks/simulation/quantumespresso.simulations.qe_examples.tddfpt.example04.json) | `TDDFPT/examples/example04` | `TDDFPT/examples/example04/run_example` |
| [`quantumespresso.simulations.qe_examples.tddfpt.example05`](../../tasks/simulation/quantumespresso.simulations.qe_examples.tddfpt.example05.json) | `TDDFPT/examples/example05` | `TDDFPT/examples/example05/run_example` |
| [`quantumespresso.simulations.qe_examples.tddfpt.example06`](../../tasks/simulation/quantumespresso.simulations.qe_examples.tddfpt.example06.json) | `TDDFPT/examples/example06` | `TDDFPT/examples/example06/run_example` |
| [`quantumespresso.simulations.qe_examples.tddfpt.example07`](../../tasks/simulation/quantumespresso.simulations.qe_examples.tddfpt.example07.json) | `TDDFPT/examples/example07` | `TDDFPT/examples/example07/run_example` |
| [`quantumespresso.simulations.qe_examples.tddfpt.example08`](../../tasks/simulation/quantumespresso.simulations.qe_examples.tddfpt.example08.json) | `TDDFPT/examples/example08` | `TDDFPT/examples/example08/run_example` |
| [`quantumespresso.simulations.qe_examples.tddfpt.example09`](../../tasks/simulation/quantumespresso.simulations.qe_examples.tddfpt.example09.json) | `TDDFPT/examples/example09` | `TDDFPT/examples/example09/run_example` |
| [`quantumespresso.simulations.qe_examples.tddfpt.example10`](../../tasks/simulation/quantumespresso.simulations.qe_examples.tddfpt.example10.json) | `TDDFPT/examples/example10` | `TDDFPT/examples/example10/run_example` |
| [`quantumespresso.simulations.qe_examples.tddfpt.example11`](../../tasks/simulation/quantumespresso.simulations.qe_examples.tddfpt.example11.json) | `TDDFPT/examples/example11` | `TDDFPT/examples/example11/run_example` |
| [`quantumespresso.simulations.qe_examples.tddfpt.example12`](../../tasks/simulation/quantumespresso.simulations.qe_examples.tddfpt.example12.json) | `TDDFPT/examples/example12` | `TDDFPT/examples/example12/run_example` |
| [`quantumespresso.simulations.qe_examples.tddfpt.example13`](../../tasks/simulation/quantumespresso.simulations.qe_examples.tddfpt.example13.json) | `TDDFPT/examples/example13` | `TDDFPT/examples/example13/run_example` |
| [`quantumespresso.simulations.qe_examples.tddfpt.example14`](../../tasks/simulation/quantumespresso.simulations.qe_examples.tddfpt.example14.json) | `TDDFPT/examples/example14` | `TDDFPT/examples/example14/run_example` |
| [`quantumespresso.simulations.qe_examples.tddfpt.example15`](../../tasks/simulation/quantumespresso.simulations.qe_examples.tddfpt.example15.json) | `TDDFPT/examples/example15` | `TDDFPT/examples/example15/run_example` |
| [`quantumespresso.simulations.qe_examples.tddfpt.example16`](../../tasks/simulation/quantumespresso.simulations.qe_examples.tddfpt.example16.json) | `TDDFPT/examples/example16` | `TDDFPT/examples/example16/run_example` |
| [`quantumespresso.simulations.qe_examples.tddfpt.example17`](../../tasks/simulation/quantumespresso.simulations.qe_examples.tddfpt.example17.json) | `TDDFPT/examples/example17` | `TDDFPT/examples/example17/run_example` |
| [`quantumespresso.simulations.qe_examples.tddfpt.example18`](../../tasks/simulation/quantumespresso.simulations.qe_examples.tddfpt.example18.json) | `TDDFPT/examples/example18` | `TDDFPT/examples/example18/run_example` |
| [`quantumespresso.simulations.qe_examples.tddfpt.example19`](../../tasks/simulation/quantumespresso.simulations.qe_examples.tddfpt.example19.json) | `TDDFPT/examples/example19` | `TDDFPT/examples/example19/run_example` |
| [`quantumespresso.simulations.qe_examples.xspectra.cu-l23`](../../tasks/simulation/quantumespresso.simulations.qe_examples.xspectra.cu-l23.json) | `XSpectra/examples/Cu_L23` | `XSpectra/examples/run_example_Cu_L23` |
| [`quantumespresso.simulations.qe_examples.xspectra.diamond`](../../tasks/simulation/quantumespresso.simulations.qe_examples.xspectra.diamond.json) | `XSpectra/examples/diamond` | `XSpectra/examples/run_example_diamond` |
| [`quantumespresso.simulations.qe_examples.xspectra.ni-o`](../../tasks/simulation/quantumespresso.simulations.qe_examples.xspectra.ni-o.json) | `XSpectra/examples/NiO` | `XSpectra/examples/run_example_NiO` |
| [`quantumespresso.simulations.qe_examples.xspectra.si-o2-uspp`](../../tasks/simulation/quantumespresso.simulations.qe_examples.xspectra.si-o2-uspp.json) | `XSpectra/examples/SiO2_USPP` | `XSpectra/examples/run_example_SiO2_USPP` |

## Run identity convention

Each created bundled-example run uses this portable identity:

```text
TASK-ID.vMAJOR-MINOR[-PATCH].YYYYMMDDTHHMMSSZ
```

`TASK-ID` is the exact canonical leaf simulation Task identity. The release uses
canonical decimal components, with dots replaced by hyphens in the `v...` segment.
The final segment is the explicit UTC workspace-creation time at whole-second
precision.

For example, separate QE 7.2 and QE 7.5 executions of PW example01 would use
identities of the following form:

```text
quantumespresso.simulations.qe_examples.pw.example01.v7-2.20260921T014018Z
quantumespresso.simulations.qe_examples.pw.example01.v7-5.20260921T021500Z
```

The corresponding external workspace is rooted beneath the Workflow simulation and
tool owners while retaining the remaining Task hierarchy:

```text
/Users/eugene/projects/ksdft2effmass-runs/
  simulations/
    quantumespresso/
      qe_examples/
        <component>/
          <example>/
            vMAJOR-MINOR[-PATCH]/
              YYYYMMDDTHHMMSSZ/
```

The first identity above therefore maps to
`simulations/quantumespresso/qe_examples/pw/example01/v7-2/20260921T014018Z/`.
The identity becomes immutable when the workspace is created; an existing identity
or path is a collision and must stop creation rather than be reused or overwritten.
Absolute machine paths, executable and input hashes, scientific settings, resource
limits, and attempt identities remain in the run manifest rather than the portable
identity.

A version regression uses one separately authorized run identity per release. A
comparison record references the exact run identities; similarity of names does not
establish compatible inputs, pseudopotentials, basis, geometry, energy reference,
or represented results. This naming convention creates no workspace and grants no
execution or comparison authority.

## Execution boundary

- No Task in this campaign is activated by this inventory.
- Each child requires an exact source/input/pseudopotential/dependency/resource preflight and separate protected-execution authorization.
- Runs must use isolated ignored workspaces rather than mutating the upstream source tree.
- Automatic retries, concurrent campaign execution, remote execution, and successor activation remain prohibited.
- Outcomes are bundled-example learning evidence only; they do not establish project production readiness, numerical verification, scientific validation, uncertainty quantification, or human acceptance.

## Review

The campaign review is [`quantumespresso.simulations.qe_examples.review`](../../tasks/simulation/quantumespresso.simulations.qe_examples.review.json). It remains blocked until every runnable group has an explicit evidence-backed disposition.
