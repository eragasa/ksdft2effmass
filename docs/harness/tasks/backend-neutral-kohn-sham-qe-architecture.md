<!-- Generated from SQLite control state; do not edit. -->
# Backend-neutral Kohn–Sham DFT and Quantum ESPRESSO architecture

[Task index](index.md) · [Previous](./backend-neutral-cpn-workflow-architecture.md) · [Next](./bulk-silicon.artifacts.qe.inventory.md)

## Status

`legacy_recorded`: Architecture approved and recorded by human decision on 2026-08-03. Its scientific object, adapter, artifact, convention, gate-split, PAW, PhysKit, and execution-checkpoint decisions remain authoritative. Its linear/DAG-like workflow sequencing and A–H task program are prospectively superseded, without historical rewriting, by `.pi/tasks/backend-neutral-cpn-workflow-architecture.md` and the P0–P11 CPN task program. No implementation was launched and no production execution is authorized.

## Objective

Architecture approved and recorded by human decision on 2026-08-03. Its scientific object, adapter, artifact, convention, gate-split, PAW, PhysKit, and execution-checkpoint decisions remain authoritative. Its linear/DAG-like workflow sequencing and A–H task program are prospectively superseded, without historical rewriting, by `.pi/tasks/backend-neutral-cpn-workflow-architecture.md` and the P0–P11 CPN task program. No implementation was launched and no production execution is authorized.

## Parent and prerequisites

None.

## Authority references

- .pi-subagents/artifacts/18b37c02_ksdft2effmass.ksdft2effmass-integration-reviewer_0_output.md
- .pi/chains/backend-neutral-kohn-sham-qe.chain.json
- dft/paw.py
- docs/architecture/periodic-electronic-structure-integration.md
- docs/publications/conferences/ICMSEP2026/ksdft2effmass.ksdft_fanout.md
- harness/archive/task-control-v1/tasks/backend-neutral-kohn-sham-qe-architecture.md

## Authorized scope

- record the approved package and object boundaries;
- split the input mapper from the result adapter;
- classify `KohnShamDataset`, `QuantumEspressoExecutionResult`, and `SCFConvergenceResult` as immutable ResultObjects;
- record the static acyclic Python import direction;
- separate portable artifact identity from deployment location;
- record PAW, PhysKit, G01a/G01b, G02/Stage-03, unit, indexing, and fan-out decisions;
- create bounded implementation task records A–H and an unlaunched chain;
- update control-plane and Sphinx architecture references;
- perform read-only architecture and integration review.
- production source or test implementation;
- public wire schemas or fixtures;
- copied or adapted PhysKit code;
- dependency changes;
- pseudopotential selection;
- QE/Wannier execution;
- manifests for a real calculation;
- convergence acceptance;
- scientific validation or uncertainty quantification.

## Completion criteria

- architecture task and chain agree;
- G01a/G01b, G02, and Stage 03 are acyclic and consistent;
- the prospective static import direction is feasible and has no provenance/DFT cycle;
- neutral packages do not import QE;
- input and result adaptation remain separate;
- `logical_path_or_uri` and `dft/paw.py` are absent from the approved contract;
- no PhysKit dependency or copied code is introduced;
- no production run is authorized;
- historical records are preserved;
- Sphinx/control-plane references agree;
- independent architecture and integration reviews report no unresolved administrative inconsistency.

## Exclusions

- production source or test implementation;
- public wire schemas or fixtures;
- copied or adapted PhysKit code;
- dependency changes;
- pseudopotential selection;
- QE/Wannier execution;
- manifests for a real calculation;
- convergence acceptance;
- scientific validation or uncertainty quantification.

## Historical source

`harness/archive/task-control-v1/tasks/backend-neutral-kohn-sham-qe-architecture.md` (`sha256:30252588d5cce5ea14b57aef4e07f990b4cb86881afe5c061387928246da0263`)
