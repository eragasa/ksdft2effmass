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

| Cost rank | Task suffix | Project tutorial | Upstream example | System | Planned executable stages | Initial disposition |
|---:|---|---|---|---|---|---|
| 1 | `scf-silicon` | `silicon-scf` | SCF calculation | Diamond Si | `pw.x` SCF | First low-cost candidate |
| 2 | `bands-silicon` | `silicon-bands` | Bandstructure | Diamond Si | `pw.x` SCF, `pw.x` bands, `bands.x`; interactive `plotband.x` excluded | Candidate |
| 3 | `graphene` | `graphene-electronic-structure` | Graphene | Graphene | `pw.x` SCF, NSCF and bands; `dos.x`, `bands.x` | Learning-only candidate outside material scope |
| 4 | `soc-iron` | `iron-soc` | SOC, Fe branch | Bulk Fe | relativistic `pw.x` SCF and bands; `bands.x` | Learning-only candidate |
| 5 | `soc-gaas` | `gaas-soc` | SOC, GaAs branch | GaAs | relativistic `pw.x` SCF and bands; `bands.x` | Learning-only candidate |
| 6 | `spin-bands-nickel` | `nickel-spin-bands` | Ni spin-polarized bands | Bulk Ni | `pw.x` SCF and bands; two `bands.x` spin components | Learning-only candidate |
| 7 | `bands-gaas` | `gaas-bands` | GaAs | Zinc-blende GaAs | `pw.x` VC-relax, SCF, NSCF and bands; `bands.x` | Learning-only candidate outside material scope |
| 8 | `structure-optimization-silicon` | `silicon-structure-optimization` | Structure optimization | Diamond Si | `pw.x` VC-relax | Candidate |
| 9 | `dos-silicon` | `silicon-dos` | DOS calculation | Diamond Si | `pw.x` SCF, `pw.x` NSCF, `dos.x` | Candidate |
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

The exact `scf-silicon` → `bands-silicon` candidate is included in the
[paired ABINIT and QE silicon SCF-and-bands preflight](paired-silicon-scf-bands-preflight.md)
and awaits checkpoint `PAIRED-SILICON-BANDS-RUN-HC01`. The earlier proposal to pair it
with an ABINIT H$_2$ distance scan was rejected and not executed.

The cost rank is a provisional cheapest-to-most-expensive ordering for local tutorial
execution. It is not an activation order: declared prerequisites, material scope,
source and license resolution, exact resource estimates, and protected-execution
authorization take precedence.

“Candidate” does not mean activated. A Task may be explicitly deferred after
source, license, tool, resource, or scientific-scope preflight. Deferral is a
recorded campaign observation, not a failed calculation.

## Local workspace

Each Task maps to
`examples/tutorials/<project-tutorial>/qe/`. Maintained input, scripts, tests, and
README files follow the architecture commit boundary. Local execution occurs only
beneath the backend's ignored `run/<run-id>/` tree:

```text
examples/tutorials/<project-tutorial>/qe/
  README.md
  input/
  scripts/
  expected/
  run/
    <run-id>/
      input/
      stdout/
      stderr/
      work/
      results/
```

`input/` under the run is the staged execution input, `stdout/` and `stderr/` retain
separate process streams, `work/` contains native executable state, and `results/`
contains local postprocessed results. No Task may use a shared `/tmp` or reuse
another Task's mutable prefix/outdir. Tutorial paths are rewritten only as an
explicit operational adaptation without changing scientific settings. The entire
`run/` tree remains local and uncommitted.

## Runtime-output contract

Preprocessing establishes the staged input and isolated `work/` directory before an
executable starts. Simulation captures stdout and stderr separately and leaves
calculator-native output in `work/`. Postprocessing must account for every produced
stream and native file by parsing its useful content, consuming it through a typed
subsequent calculator operation, or reporting that its format is unsupported. A file
listing or checksum alone is not postprocessing.

Diagnostic directory snapshots may be produced locally when needed to understand an
unfamiliar tutorial, but they are not mandatory example content or a public tutorial
contract and are not committed. The maintained example focuses on usable inputs,
readers, and computational stage relationships.

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

The ignored `run/` workspace remains local. After review, portable sanitized input,
useful scripts, backend instructions, and small test-consumed fixtures may be promoted
to the paired project tutorial directory under the
[cross-backend tutorial example commit boundary](../architecture/v2/tutorial-examples.md).
Routine streams, generated QEXSD, wavefunctions, charge densities, restart state,
dense matrices, and other calculator-native runtime output remain uncommitted.
