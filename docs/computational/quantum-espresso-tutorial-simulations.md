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
workflows is split into distinct Tasks. The non-scientific prerequisite
`quantumespresso.simulations.integration` owns the initial
`ksdft2effmass.integration.quantumespresso` boundary and its local execution
software verification; it may not invoke a scientific executable during its
own implementation or tests. The prospective integration boundary is defined by the versioned
[Architecture v2 Quantum ESPRESSO contract](../architecture/v2/ksdft2effmass/calculators/quantum-espresso.md).
Architecture v2 remains unimplemented and its live issue register continues to
bound any later implementation.

| Task suffix | Upstream example | System | Planned executable stages | Initial disposition |
|---|---|---|---|---|
| `scf-silicon` | SCF calculation | Diamond Si | `pw.x` SCF | First low-cost candidate |
| `convergence-silicon` | Convergence testing | Diamond Si | repeated `pw.x` SCF sweeps; PWTK branch only if separately approved | Candidate after baseline SCF |
| `structure-optimization-silicon` | Structure optimization | Diamond Si | `pw.x` VC-relax | Candidate |
| `dos-silicon` | DOS calculation | Diamond Si | `pw.x` SCF, `pw.x` NSCF, `dos.x` | Candidate |
| `bands-silicon` | Bandstructure | Diamond Si | `pw.x` SCF, `pw.x` bands, `bands.x`; interactive `plotband.x` excluded | Candidate |
| `aluminum-metal` | Al (metal) | FCC Al | `pw.x` VC-relax, SCF, NSCF and bands; `dos.x`, `bands.x` | Candidate; dense NSCF requires estimate |
| `smearing-convergence-aluminum` | Al smearing convergence branch | FCC Al | PWTK-controlled repeated `pw.x` runs over k meshes, smearing functions, and degauss values | Learning-only; enumerate cost and authorize PWTK separately |
| `pdos-aluminum` | P-DOS | FCC Al | `pw.x` SCF and NSCF, `projwfc.x`; optional `sumpdos.x` | Candidate after aluminum preflight |
| `kresolved-dos-silicon` | k-resolved DOS | Diamond Si | `pw.x` SCF and bands, `projwfc.x` | Candidate |
| `graphene` | Graphene | Graphene | `pw.x` SCF, NSCF and bands; `dos.x`, `bands.x` | Learning-only candidate outside material scope |
| `bands-gaas` | GaAs | Zinc-blende GaAs | `pw.x` VC-relax, SCF, NSCF and bands; `bands.x` | Learning-only candidate outside material scope |
| `magnetism-iron` | Fe (magnetic) | Bulk Fe | FM/AFM `pw.x`; optional convergence sweeps; `dos.x`, `projwfc.x` | Learning-only; likely defer expensive sweep |
| `spin-bands-nickel` | Ni spin-polarized bands | Bulk Ni | `pw.x` SCF and bands; two `bands.x` spin components | Learning-only candidate |
| `dftu-feo` | DFT+U | FeO | DFT and DFT+U `pw.x`, NSCF, `projwfc.x`; optional `hp.x` iteration | High-risk learning candidate; default defer `hp.x` loop |
| `soc-iron` | SOC, Fe branch | Bulk Fe | relativistic `pw.x` SCF and bands; `bands.x` | Learning-only candidate |
| `soc-gaas` | SOC, GaAs branch | GaAs | relativistic `pw.x` SCF and bands; `bands.x` | Learning-only candidate |
| `bi2se3` | Bi2Se3 topological insulator | Bulk and slab Bi2Se3 | three SCF/bands branches, NSCF, `bands.x`, `dos.x` | High-cost candidate; explicit resource review required |
| `dielectric-silicon` | Dielectric constant | Diamond Si | `pw.x` SCF/optional NSCF, `epsilon.x` | Candidate; unconverged tutorial behavior only |
| `jdos-silicon` | JDOS branch | Diamond Si | `pw.x` SCF and NSCF, `epsilon.x` JDOS | Candidate after dielectric preflight |
| `fermi-surface-copper` | Fermi surface | FCC Cu | `pw.x` SCF and dense-grid bands, `fs.x`; XCrySDen excluded | Learning-only candidate; dense-grid estimate required |
| `phonons-gaas` | Phonon dispersion | GaAs | `pw.x`, `ph.x`, `q2r.x`, `matdyn.x` | Default defer: source reports about one day on four cores |
| `wannier-silicon` | Wannier method | Diamond Si | `pw.x` SCF/NSCF, `kmesh.pl`, `wannier90.x -pp`, `pw2wannier90.x`, `wannier90.x` | Candidate only after separate Wannier authorization |
| `molecular-dynamics-water` | Molecular dynamics | Isolated H2O in a periodic box | prerequisite relaxation, then 100-step `pw.x` MD | Learning-only candidate outside material scope |

“Candidate” does not mean activated. A Task may be explicitly deferred after
source, license, tool, resource, or scientific-scope preflight. Deferral is a
recorded campaign observation, not a failed calculation.

## Local workspace

The campaign root is `/simulations/` at the repository root. The entire tree is
Git-ignored because it may contain large native outputs, restart files, licensed
pseudopotentials, and machine-specific state.

Each attempt uses this layout:

```text
simulations/
  <task-id>/
    <run-id>/
      request.json
      provenance.json
      source/
      input/
      workspace/
      logs/
        001-<stage>.stdout
        001-<stage>.stderr
        001-<stage>.exit.json
      snapshots/
        000-before.json
        001-after-<stage>.json
        ...
        final-after.json
        diff.json
```

`source/` contains only material whose reuse terms have been resolved. `input/`
is a frozen pre-execution byte snapshot of the exact sanitized inputs used.
`workspace/` contains native executable state. No Task may use a shared `/tmp`
or reuse another Task's mutable prefix/outdir; tutorial paths are rewritten only
as an explicitly recorded operational adaptation, without changing scientific
settings.

## Snapshot contract

A snapshot is a deterministic filesystem manifest, not a duplicate copy of
large calculation data. It records, relative to the run root:

- path and file type;
- byte size;
- SHA-256 for each regular file;
- symlink target when applicable;
- executable bit;
- diagnostic modification time; and
- any unreadable or concurrently changing path as an explicit finding.

Snapshot scope is exactly `source/`, `input/`, and `workspace/`. It excludes
`logs/`, `snapshots/`, `request.json`, and `provenance.json`, preventing control
records and snapshot manifests from hashing themselves or creating a terminal
record/snapshot cycle.

The `000-before.json` manifest is written atomically after staging and validating
inputs but before process creation. If it cannot be completed, the executable is
not invoked. After process termination or process-creation failure, the
integration closes both streams and attempts an after-manifest over the same
scope. `diff.json` records created, removed, and byte-changed paths between
available manifests. `final-after.json` is a separately identified final run
manifest when the run contains multiple stages.

## Command and stream capture

Every executable stage is invoked directly by the future campaign runner. Shell
pipelines and merged output streams are prohibited. Conceptually:

```text
<launcher-and-executable> <arguments>
  stdout -> logs/NNN-<stage>.stdout
  stderr -> logs/NNN-<stage>.stderr
  exit   -> logs/NNN-<stage>.exit.json
```

The terminal exit record is written atomically after the after-manifest attempt.
It contains the exact argument vector, executable identity, launcher identity
when present, start/end timestamps, elapsed time, exit status, termination
signal, working directory, and available before/after manifest content
identities. Standard output and standard error remain separate even when a stage
fails. A failure stops dependent stages.

If process creation, stream handling, or after-manifest generation fails, the
terminal failure record contains the identities that are available, an explicit
null for each unavailable identity, and structured findings describing why it
is unavailable. The contract never claims that an after-manifest exists when
snapshot generation itself failed.

## Preflight required for each Task

Before execution, report and approve:

1. pinned tutorial page and source identities;
2. independently reviewed exact input files;
3. QE/Wannier/PWTK executable names, versions, paths, and checksums where
   practicable;
4. pseudopotential source, filename, format, functional, relativistic/core
   treatment, checksum, and license;
5. system size, cutoffs, meshes, stage count, MPI/OpenMP layout, memory, disk,
   and estimated runtime;
6. expected native outputs and retained/disposable classification;
7. local machine and workspace root;
8. confirmation that no remote, cluster, or cloud execution is involved unless
   separately authorized; and
9. the protected-execution checkpoint authorizing that exact attempt.

A dry-run validates staging, path confinement, command construction, independent
stdout/stderr targets, snapshot destinations, and available disk space without
starting a scientific executable.

## Review and learning disposition

After each attempt, record only observed facts with provenance:

- stage outcomes and runtimes;
- actual artifact inventory and snapshot diff;
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

## Compact retained provenance

The ignored workspace remains local. After review, only separately authorized,
sanitary, compact records may be proposed for version control: exact input text
when licensing permits, source and executable identities, pseudopotential
checksums and external locations, command records, compact artifact manifests,
and conclusions explicitly labeled as tutorial software behavior. Large native
outputs, wavefunctions, charge densities, restart state, and dense matrices are
never committed.
