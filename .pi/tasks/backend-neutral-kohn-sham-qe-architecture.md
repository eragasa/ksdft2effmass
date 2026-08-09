# Backend-neutral Kohn–Sham DFT and Quantum ESPRESSO architecture

## Status

Architecture approved and recorded by human decision on 2026-08-03. Its scientific object, adapter, artifact, convention, gate-split, PAW, PhysKit, and execution-checkpoint decisions remain authoritative. Its linear/DAG-like workflow sequencing and A–H task program are prospectively superseded, without historical rewriting, by `.pi/tasks/backend-neutral-cpn-workflow-architecture.md` and the P0–P11 CPN task program. No implementation was launched and no production execution is authorized.

This record preserves the original decision chronology. Its historical `KohnSham*` prospective names are refined for active future contracts by `.pi/tasks/backend-neutral-cpn-workflow-architecture.md` and `docs/architecture/periodic-electronic-structure-integration.md`: the domain is periodic KS/GKS electronic structure for crystalline solids, and active names use `PeriodicElectronicStructure*`. Historical names below remain chronology rather than current naming authority. The corrected scientific/computational workflow is a stateful project-owned Colored Petri Net; acyclic dependency direction applies only to static Python imports and planning projections.

## Authorized scope of this control-plane correction

- record the approved package and object boundaries;
- split the input mapper from the result adapter;
- classify `KohnShamDataset`, `QuantumEspressoExecutionResult`, and `SCFConvergenceResult` as immutable ResultObjects;
- record the static acyclic Python import direction;
- separate portable artifact identity from deployment location;
- record PAW, PhysKit, G01a/G01b, G02/Stage-03, unit, indexing, and fan-out decisions;
- create bounded implementation task records A–H and an unlaunched chain;
- update control-plane and Sphinx architecture references;
- perform read-only architecture and integration review.

Excluded from this correction:

- production source or test implementation;
- public wire schemas or fixtures;
- copied or adapted PhysKit code;
- dependency changes;
- pseudopotential selection;
- QE/Wannier execution;
- manifests for a real calculation;
- convergence acceptance;
- scientific validation or uncertainty quantification.

## Human decisions

1. `QuantumEspressoInputMapper` maps `KohnShamCalculationSpecification` plus `QuantumEspressoNumericalOptions` to `QuantumEspressoInputRecord`. `QuantumEspressoResultAdapter` maps parsed QE output/save records plus the accepted calculation specification and execution/manifest identity to `KohnShamDataset`. Neither object owns both directions.
2. `QuantumEspressoInputSerializer` owns only deterministic text rendering. `QuantumEspressoOutputParser` and `QuantumEspressoSaveParser` own only mechanical parsing.
3. `KohnShamDataset`, `QuantumEspressoExecutionResult`, and `SCFConvergenceResult` are immutable ResultObjects. Nested scientific/configuration records remain immutable DataObjects where appropriate.
4. `dft.structure`, `dft.pseudopotentials`, and `provenance.records` are parallel foundations. `provenance.records` imports no scientific or backend domain. Neutral DFT imports no QE module. TB and Wannier consume neutral datasets and never parse QE files.
5. `ArtifactReference` carries portable content identity and logical role. Deployment location is separate as `ArtifactLocation` or through a resolver. No `logical_path_or_uri` field is authorized.
6. PAW is a `PseudopotentialFormalism` value only. No `dft/paw.py` or execution-support claim is authorized absent PAW-specific operations and validation.
7. The first pseudopotential execution lane remains undecided pending audit of the actual Si artifact, provenance, formalism, XC compatibility, relativity, and Wannier suitability.
8. Historical `G01` is prospectively split into `G01a` computational foundation and `G01b` composed synthetic scientific workflows. `G02` depends on `G01a`, not alignment. Historical evidence is preserved.
9. G02 owns the accepted SCF parent and bulk-validation path/diagnostic NSCF products. Stage 03 owns a Wannier-compatible uniform-grid NSCF child selected after band/window/grid approval and linked to the G02 SCF parent manifest.
10. Neutral units/conventions are Å, eV, QE cutoffs in Ry, row direct-lattice vectors, `B = 2π C^{-T}`, fractional direct site coordinates, fractional reciprocal primary k coordinates, zero-based bands, `(spin, k, band)` arrays, and `exp(+i k·R)` Fourier phase. Occupation capacity and spin degeneracy are explicit.
11. Initial validated scientific scope is non-spin-polarized bulk silicon. Future spin modes may be representable but are not claimed implemented or validated.
12. `KohnShamDataset` version 1 is a compact result with identities, realized structure, sampling, spin/relativistic convention, bands, occupations, electron count, Fermi/chemical-potential representation, energy convention, optional symmetry, manifest identity, and typed artifact references. Large density, wavefunction, `.save`, FFT, restart, and bridge payloads remain external. Generic operators and projectors are excluded.
13. The direct branch is direct spectral DFT-to-TB fitting. Operator fitting requires an explicit common operator representation. The Wannier branch also consumes retained wavefunctions and `.nnkp`, `.amn`, `.mmn`, and `.eig`; Wannier90 is a separate backend.
14. PhysKit use is contractual reimplementation with no runtime dependency or shared package. Only later focused k-path adaptation may be considered with exact MIT provenance and repository-native evidence. No PhysKit code is copied now.
15. A separate human checkpoint is mandatory before a real QE run and records the environment, executable, pseudopotential, resources, roots, runtime, retention, and transfer policy. Synthetic boundaries remain eligible within separately approved implementation tasks.

## Bounded implementation task records

| ID | Record | Status |
|---|---|---|
| A | `.pi/tasks/backend-neutral-kohn-sham-qe-A-contract.md` | Approved architecture; not launched |
| B | `.pi/tasks/backend-neutral-kohn-sham-qe-B-provenance.md` | Blocked by accepted A |
| C | `.pi/tasks/backend-neutral-kohn-sham-qe-C-neutral-dft.md` | Blocked by accepted A and B |
| D | `.pi/tasks/backend-neutral-kohn-sham-qe-D-qe-io.md` | Blocked by accepted A |
| E | `.pi/tasks/backend-neutral-kohn-sham-qe-E-qe-mapping.md` | Blocked by accepted B, C, and D |
| F | `.pi/tasks/backend-neutral-kohn-sham-qe-F-execution.md` | Blocked by accepted B, D, and E |
| G | `.pi/tasks/backend-neutral-kohn-sham-qe-G-direct-tb.md` | Blocked by accepted C and E |
| H | `.pi/tasks/backend-neutral-kohn-sham-qe-H-wannier-bridge.md` | Blocked by accepted B, C, D, and E |

Each task must independently complete implementation, tests, documentation, read-only review, parent verification, and human acceptance. Acceptance of this architecture does not launch Task A and does not authorize later tasks automatically.

## Chain supersession

`.pi/chains/backend-neutral-kohn-sham-qe.chain.json` now records the prospective P0–P11 CPN-oriented task program and retains A–H only as a superseded mapping. It remains unlaunched. The CPN marking, rather than a chain/DAG node, is the future authoritative workflow state.

## Validation requirements for this record

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

## Historical read-only review and parent verification

These reviews accepted the pre-CPN scientific object/adapter architecture. They do not review or accept the later CPN workflow correction, whose reviews are recorded separately in `.pi/tasks/backend-neutral-cpn-workflow-architecture.md`.

Final architecture review: **PASS**. It confirmed the approved object ownership,
input/result adapter split, artifact identity/location separation, conventions,
PAW and PhysKit limits, compact dataset boundary, static acyclic imports, G01a/G01b
split, G02/Stage-03 ownership, and nonauthorization of implementation or
execution. Review run: `f92d3fa9`.

Final integration/control-plane review: **PASS** with no blocking or non-blocking
administrative inconsistency in the authorized scope. It confirmed exact A–H
task/chain prerequisites and gates, historical evidence preservation, leaf-task
inventory and links, Sphinx/control-plane synchronization, zero unresolved
checkpoints, and absence of production source, dependencies, copied code, or run
authorization. Review run: `18b37c02`; artifact:
`.pi-subagents/artifacts/18b37c02_ksdft2effmass.ksdft2effmass-integration-reviewer_0_output.md`.

Parent verification passed: chain JSON parsing, A–H and prospective static-import
cycle audits, G01a/G01b graph assertions, checkpoint validation, stale G01 scans,
forbidden-contract scans, `git diff --check`, and Sphinx warnings-as-errors.
These checks are control-plane/software documentation evidence only.

The unrelated pre-existing untracked file
`docs/publications/conferences/ICMSEP2026/ksdft2effmass.ksdft_fanout.md` was preserved
unchanged and excluded from this task's acceptance scope. Its simplified diagram
is not authoritative for the approved adapter ownership.

## Remaining checkpoint

Production execution environment and pseudopotential selection are unresolved. A real QE run remains prohibited until the separate authorization checkpoint described in the architecture document is recorded and approved.
