# Quantum ESPRESSO hands-on simulation campaign

## Status and authority

This document is the execution plan requested by the human PI for every example
listed in the Pranab Das Quantum ESPRESSO hands-on category. It authorizes
planning, local workspace creation, and durable Task decomposition. It does not
by itself authorize an executable to run. Each simulation Task requires explicit
activation and a protected-execution checkpoint covering the executable,
inputs, pseudopotentials, machine, resources, expected outputs, runtime, and
retention policy.

The upstream category is
<https://pranabdas.github.io/espresso/category/hands-on/>. Source references are
pinned to `pranabdas/espresso` commit
`8d0087d05271beb13b240930d4643bf345541c7b`. The upstream repository currently
reports no declared license through the GitHub repository metadata. No upstream
file may be copied into this repository or the local simulation workspace until
reuse terms and the applicable pseudopotential licenses are resolved.

All results from this campaign are tutorial observations and software-workflow
evidence. They are not production calculations, converged project references,
scientific validation, uncertainty quantification, or acceptance evidence for
Stages 02--04.

## Evidence-grounding requirement

Any architecture or workflow probe that claims to represent tutorial-calculator
behavior must be grounded in identified outputs from an actual, explicitly authorized
scientific-executable invocation. Its retained record must identify the exact input,
executable, pseudopotential, execution attempt, process streams, native outputs, and
postprocessing used to support the claim. Synthetic fixtures and fake executors remain
permitted for isolated software or numerical verification, but they cannot substitute
for calculated data when establishing how a tutorial, calculator stage, continuation
artifact, native output, diagnostic channel, or failure actually behaves. If no
identified calculated output is available, the corresponding behavior remains
proposed or unobserved rather than being inferred from a synthetic result.

This requirement does not itself authorize execution. Every actual calculation still
requires the exact preflight and protected-execution checkpoint defined below.

## Campaign Tasks

Every executable candidate is represented by a Task whose identifier begins
with `quantumespresso.simulations.`. A page containing materially distinct
workflows is split into distinct Tasks. Each Task maps to the QE side of one
concept-first project tutorial under `examples/tutorials/<tutorial-id>/qe/`; its
paired `abinit/` directory records the corresponding implementation status rather
than asserting numerical equivalence. The layout and commit boundary are defined by
[cross-backend tutorial examples](../architecture/v2/tutorial-examples.md).

The non-scientific prerequisite `quantumespresso.simulations.integration` owns the
initial `ksdft2effmass.integration.quantumespresso` boundary and its local execution
software verification; it may not invoke a scientific executable during its own
implementation or tests. The prospective integration boundary is defined by the
versioned [Architecture v2 Quantum ESPRESSO
contract](../architecture/v2/ksdft2effmass/calculators/quantum-espresso.md).
Architecture v2 remains partially implemented and its live issue register continues
to bound any later implementation.

For the silicon DOS workflow, SCF, NSCF, and DOS are separate reusable CPN Task
definitions and separate run-scoped Task instances. Each requires its own activation,
attempt, execution grant, private workspace, process observation, result ingress, and
failure boundary. The enclosing campaign Task coordinates those operations but may not
execute them as one shell-sequence Task. Downstream stages consume admitted predecessor
results and identity-checked immutable native-state snapshots rather than sharing a
mutable `prefix`/`outdir`. Other campaign Workflows may reuse the operation definitions
only with their own exact scientific inputs and authorization.

| Cost rank | Task suffix | Project tutorial | Upstream example | System | Executable stages | Current disposition |
|---:|---|---|---|---|---|---|
| 1 | `scf-silicon` | `silicon-scf` | SCF calculation | Diamond Si | `pw.x` SCF | Calculated observation retained; Task deliberately deferred without rerun because the stage-specific after-SCF snapshot is unavailable |
| 2 | `bands-silicon` | `silicon-bands` | Bandstructure | Diamond Si | `pw.x` SCF, `pw.x` bands, `bands.x`; interactive `plotband.x` excluded | Calculated observation retained; Task deliberately deferred without rerun because per-stage before/after snapshots are unavailable |
| 3 | `graphene` | `graphene-electronic-structure` | Graphene | Graphene | `pw.x` SCF, NSCF and bands; `dos.x`, `bands.x` | Learning-only candidate outside material scope |
| 4 | `soc-iron` | `iron-soc` | SOC, Fe branch | Bulk Fe | relativistic `pw.x` SCF and bands; `bands.x` | Learning-only candidate |
| 5 | `soc-gaas` | `gaas-soc` | SOC, GaAs branch | GaAs | relativistic `pw.x` SCF and bands; `bands.x` | Learning-only candidate |
| 6 | `spin-bands-nickel` | `nickel-spin-bands` | Ni spin-polarized bands | Bulk Ni | `pw.x` SCF and bands; two `bands.x` spin components | Learning-only candidate |
| 7 | `bands-gaas` | `gaas-bands` | GaAs | Zinc-blende GaAs | `pw.x` VC-relax, SCF, NSCF and bands; `bands.x` | Learning-only candidate outside material scope |
| 8 | `structure-optimization-silicon` | `silicon-structure-optimization` | Structure optimization | Diamond Si | `pw.x` VC-relax | Calculated QE 7.5 tutorial observation retained and selected for the bounded DOS tutorial Workflow; not a project geometry |
| 9 | `dos-silicon` | `silicon-dos` | DOS calculation | Diamond Si | independent reusable `pw.x` SCF, `pw.x` NSCF, and `dos.x` CPN Tasks | One authorized QE 7.5 three-Task calculated tutorial observation completed without retry; not a project reference DOS |
| 10 | `wannier-silicon` | `silicon-wannier` | Wannier method | Diamond Si | `pw.x` SCF/NSCF, `kmesh.pl`, `wannier90.x -pp`, `pw2wannier90.x`, `wannier90.x` | Candidate only after separate Wannier authorization |
| 11 | `dielectric-silicon` | `silicon-dielectric` | Dielectric constant | Diamond Si | `pw.x` SCF/optional NSCF, `epsilon.x` | Candidate; unconverged tutorial behavior only |
| 12 | `jdos-silicon` | `silicon-jdos` | JDOS branch | Diamond Si | `pw.x` SCF and NSCF, `epsilon.x` JDOS | Candidate after dielectric preflight |
| 13 | `kresolved-dos-silicon` | `silicon-k-resolved-dos` | k-resolved DOS | Diamond Si | `pw.x` SCF and bands, `projwfc.x` | Candidate |
| 14 | `pdos-aluminum` | `aluminum-pdos` | P-DOS | FCC Al | `pw.x` SCF and NSCF, `projwfc.x`; optional `sumpdos.x` | Candidate after aluminum preflight |
| 15 | `aluminum-metal` | `aluminum-metal` | Al (metal) | FCC Al | `pw.x` VC-relax, SCF, NSCF and bands; `dos.x`, `bands.x` | Candidate; dense NSCF requires estimate |
| 16 | `convergence-silicon` | `silicon-convergence` | Convergence testing | Diamond Si | repeated `pw.x` SCF sweeps; PWTK branch only if separately approved | Candidate after baseline SCF |
| 17 | `magnetism-iron` | `iron-magnetism` | Fe (magnetic) | Bulk Fe | FM/AFM `pw.x`; optional convergence sweeps; `dos.x`, `projwfc.x` | Learning-only; likely defer expensive sweep |
| 18 | `fermi-surface-copper` | `copper-fermi-surface` | Fermi surface | FCC Cu | `pw.x` SCF and dense-grid bands, `fs.x`; XCrySDen excluded | Learning-only candidate; dense-grid estimate required |
| 19 | `smearing-convergence-aluminum` | `aluminum-smearing-convergence` | Al smearing convergence branch | FCC Al | PWTK-controlled repeated `pw.x` runs over k meshes, smearing functions, and degauss values | Learning-only; enumerate cost and authorize PWTK separately |
| 20 | `dftu-feo` | `feo-dftu` | DFT+U | FeO | DFT and DFT+U `pw.x`, NSCF, `projwfc.x`; optional `hp.x` iteration | High-risk learning candidate; default defer `hp.x` loop |
| 21 | `molecular-dynamics-water` | `water-molecular-dynamics` | Molecular dynamics | Isolated H2O in a periodic box | prerequisite relaxation, then 100-step `pw.x` MD | Learning-only candidate outside material scope |
| 22 | `bi2se3` | `bi2se3-electronic-structure` | Bi2Se3 topological insulator | Bulk and slab Bi2Se3 | three SCF/bands branches, NSCF, `bands.x`, `dos.x` | High-cost candidate; explicit resource review required |
| 23 | `phonons-gaas` | `gaas-phonons` | Phonon dispersion | GaAs | `pw.x`, `ph.x`, `q2r.x`, `matdyn.x` | Default defer: source reports about one day on four cores |

The exact `scf-silicon` → `bands-silicon` realization and its calculated outcome are
included in the [paired ABINIT and QE silicon SCF-and-bands preflight](paired-silicon-scf-bands-preflight.md).
Checkpoint `PAIRED-SILICON-BANDS-RUN-HC01` authorized one exact run; all three QE
processes completed with exit 0. Only workflow-level pre/post inventories were retained,
not the per-stage before/after snapshots required by both QE Tasks. The calculated
observation is retained. Both QE Tasks are deliberately deferred without rerun, and no
repeat of either execution is authorized.
The earlier proposal to pair it with an ABINIT H$_2$ distance scan was rejected and not
executed.

The cost rank is a provisional cheapest-to-most-expensive ordering for local tutorial
execution. It is not an activation order: declared prerequisites, material scope,
source and license resolution, exact resource estimates, and protected-execution
authorization take precedence.

“Candidate” does not mean activated. A Task may be explicitly deferred after
source, license, tool, resource, or scientific-scope preflight. Deferral is a
recorded campaign observation, not a failed calculation.

## Local workspace

Each campaign Task maps to
`examples/tutorials/<project-tutorial>/qe/`. Maintained input, scripts, tests, and
README files follow the architecture commit boundary. A single-stage Task uses one
isolated run root; a multi-stage Workflow uses one enclosing run root with one private
sub-root per run-scoped CPN Task instance. The root is either beneath the backend's
ignored `run/<run-id>/` tree or an external run root declared by the exact execution
preflight:

```text
<workflow-run-root>/
  scf-task/
    input/
    pseudo/
    streams/
    work/
    results/
    records/
  nscf-task/
    predecessor-state/
    input/
    pseudo/
    streams/
    work/
    results/
    records/
  dos-task/
    predecessor-state/
    input/
    streams/
    work/
    results/
    records/
```

Backend-specific names such as `input-source/` or separate `stdout/` and `stderr/`
directories are permitted when roles remain explicit. Inputs and dependencies are
staged separately, process streams remain distinct, `work/` contains only that Task
instance's mutable native executable state, `results/` contains local postprocessed
results, and `records/` contains compact execution and processing records. No Task may
use a shared `/tmp`, mutate another Task's workspace, or reuse another Task's mutable
prefix/outdir. A downstream Task may stage an identity-checked copy of an admitted
predecessor's immutable native-state artifact. Tutorial paths are rewritten only as an
explicit operational adaptation without changing scientific settings. The run root
remains local and uncommitted; maintained records use its portable run identity rather
than an absolute machine path.

## Runtime-output contract

Preprocessing establishes the staged input and isolated `work/` directory before an
executable starts. Simulation captures stdout and stderr separately and leaves
calculator-native output in `work/`. Postprocessing must account for every produced
stream and native file by parsing its useful content, consuming it through a typed
subsequent calculator operation, or reporting that its format is unsupported. A file
listing or checksum alone is not postprocessing.

Diagnostic directory snapshots are retained locally when a Task's completion criteria
require them. They are runtime records, not mandatory committed example content or a
public tutorial contract. The maintained example focuses on usable inputs, readers,
and computational stage relationships.

## Command and stream capture

Every executable stage is invoked directly by the future campaign runner. Shell
pipelines and merged output streams are prohibited. Conceptually:

```text
<launcher-and-executable> <arguments>
  stdout -> stdout/NNN-<stage>.stdout
  stderr -> stderr/NNN-<stage>.stderr
  exit   -> results/NNN-<stage>.exit.json
```

The terminal exit record contains the invoked argument vector, start and end time,
elapsed time, exit status or termination signal, and working directory. Standard
output and standard error remain separate even when a stage fails. A failure stops
dependent stages. Process-creation or stream-capture failures are reported directly
without fabricating calculator output.

## Preflight required for each Task

Before execution, report and approve:

1. pinned tutorial page and source identities;
2. independently reviewed exact input files;
3. QE/Wannier/PWTK executable names, versions, and paths;
4. pseudopotential source, filename, format, functional, relativistic/core
   treatment, and license;
5. system size, cutoffs, meshes, stage count, MPI/OpenMP layout, memory, disk,
   and estimated runtime;
6. expected native outputs and retained/disposable classification;
7. local machine and workspace root;
8. confirmation that no remote, cluster, or cloud execution is involved unless
   separately authorized; and
9. the protected-execution checkpoint authorizing that exact attempt.

A dry-run validates staging, path confinement, command construction, independent
stdout/stderr targets, runtime destinations, and available disk space without
starting a scientific executable.

## Review and learning disposition

After each attempt, record only observed facts:

- stage outcomes and runtimes;
- produced streams and files and the readers or subsequent operations that consumed
  them;
- parser or interface opportunities;
- restart and failure behavior;
- operational adaptations needed to isolate the tutorial;
- discrepancies between page, pinned source, and installed executable version;
- whether the tutorial is useful for this project's silicon/QE/Wannier path; and
- execute-again, retain-as-fixture-candidate, or defer disposition.

Do not compare energies or derived properties across tutorials until basis,
pseudopotential, functional, geometry, units, k-point, and energy-reference
compatibility has been established. Numerical agreement with a tutorial page is
not a scientific acceptance criterion.

## Maintained example promotion

The ignored or external run root remains local. After review, portable sanitized input,
useful scripts, backend instructions, and small test-consumed fixtures may be promoted
to the paired project tutorial directory under the
[cross-backend tutorial example commit boundary](../architecture/v2/tutorial-examples.md).
Routine streams, generated QEXSD, wavefunctions, charge densities, restart state,
dense matrices, and other calculator-native runtime output remain uncommitted.
