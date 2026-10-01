# GaAs non-SOC bands tutorial preflight

## Status and claim boundary

This document contains the completed metadata and dry-run preflight that governed one
subsequently authorized **calculated tutorial execution**. Human response `A` resolved
checkpoint `QE-GAAS-BANDS-RUN-HC01` before pseudopotential acquisition, operational
input staging, or scientific execution.

The retained result is a calculated tutorial observation with an expected-stage
failure and software-workflow evidence only. GaAs is outside the project's supported
material scope. The Workflow does not establish a validated GaAs lattice, band
structure, band gap, pseudopotential choice, numerical convergence, scientific
validation, uncertainty quantification, or scientific acceptance.

## Smallest source-defined scope

The source page presents `vc-relax`, SCF, optional NSCF, bands, and `bands.x`. This
preflight proposes the smallest source-defined bands Workflow:

1. `pw.x` SCF at the source-recorded fixed lattice parameter;
2. `pw.x` bands using an admitted copy of the SCF native state; and
3. `bands.x` using an admitted copy of the bands native state.

The GaAs `vc-relax` branch is explicitly deferred. The source already records
`celldm(1)=10.861462` Bohr for its downstream inputs, and the previously completed
silicon structure-optimization tutorial has already supplied the intended calculator
interface learning. Replaying the GaAs relaxation would not supply the hard-coded
source downstream inputs without introducing a new geometry-propagation policy.

The NSCF branch is explicitly deferred because the source says it is necessary only
for density of states, which is outside this bands Task. These deferrals are not
calculated results and make no scientific claim about the fixed geometry or omitted
sampling.

## Tutorial source and reuse boundary

The source is the Pranab Das GaAs tutorial at repository commit
`8d0087d05271beb13b240930d4643bf345541c7b`:

- <https://pranabdas.github.io/espresso/hands-on/gaas/>;
- `docs/hands-on/GaAs.md`, Git blob
  `9fc4a4ac7a8240ad49f5c4b9e61bd891a84469a4`, 1,634 bytes, SHA-256
  `9840e346ec5cd2089bb747ea7bb2ff74ae249b160ca469597dff6b0891a1af04`;
- `src/GaAs/pw.scf.GaAs.in`, Git blob
  `f69272874d61ec7fe09a468ba1891ea8ce636d04`, 531 bytes, SHA-256
  `43c8cc0db862265ea9f847420cf14ee3507bf18f1f3de156e08358a7bc8292e1`;
- `src/GaAs/pw.bands.GaAs.in`, Git blob
  `86ba84a24e1af0fafeee07c16ce3fdfa586cc0e7`, 656 bytes, SHA-256
  `929497733cf8fc265cb5869ac24661cbe3f4af6f5c019e9795eba99c2babcef7`;
- `src/GaAs/pp.bands.GaAs.in`, Git blob
  `c5df3a682cfd04a198696ef96c32a73d49efbc83`, 95 bytes, SHA-256
  `b2024a15db0cfc20733136dd710d2b5fbf2a28dd6639fb2f9cf3eac455cf6623`.

The pinned `vc-relax` and NSCF inputs remain identified in the external dry-run record
even though they are not proposed for execution.

The pinned repository's `docs/license.md`, Git blob
`0bb057148fe7ccd3c4de2efccc47be377931aa56`, declares CC BY 4.0 for the work and
excludes third-party material. The preflight reuses identified settings only and does
not commit upstream input bytes. It makes no legal conclusion about which individual
files the declaration covers. Any execution authorization is limited to local-use
operational renderings with source attribution and no redistribution.

## Pseudopotential identities and license boundary

The source names two PSlibrary 1.0.0 scalar-relativistic PBE PAW files. The official
Quantum ESPRESSO pseudopotential portal supplies the following exact bytes:

| File | Bytes | SHA-256 | Valence electrons | Header suggested cutoffs (Ry) |
|---|---:|---|---:|---:|
| `Ga.pbe-dn-kjpaw_psl.1.0.0.UPF` | 1,869,765 | `7e1db62c3e74c3cf88d7994fe857d2b156ca4d0bc00e780603642213356edceb` | 13 | 60.30665876644 / 244.4576095453 |
| `As.pbe-n-kjpaw_psl.1.0.0.UPF` | 1,113,750 | `eab4eca53545664f218f205957e8e53ae825186a622411986e8063cf26e95628` | 5 | 19.90675714583 / 103.1374553857 |

Both headers report PAW, scalar relativity, PBE, nonlinear core correction, no
spin-orbit data, and generation with the QE 6.3 atomic code by A. Dal Corso. These are
source metadata, not suitability or convergence evidence.

At PSlibrary repository commit
`835dd6477c90fa9d59524914de50901d4be73e36`, `AAREADME` states that all material in
the distribution is under GNU GPL version 2 or, at the user's option, any later
version. Its SHA-256 is
`d8ef440b00242b0d20e7a00e3b33e76f8638ab47eea1df2051e3b0f9223fa519`.
The included GPLv2 text has SHA-256
`204d8eff92f95aac4df6c8122bc1505f468f3a901e5a4cc08940e0ede1938994`.

Checkpoint `QE-GAAS-BANDS-RUN-HC01` asks the human to authorize exact local
acquisition, staging, and execution under that declared license boundary. No
pseudopotential will be committed or redistributed.

## Exact scientific settings

The two-atom zinc-blende primitive cell uses QE `ibrav=2`,
`celldm(1)=10.861462` Bohr, Ga at `(0,0,0)`, and As at `(0.25,0.25,0.25)` in default
`alat` coordinates. Both `pw.x` stages retain:

- `ecutwfc=60 Ry` and `ecutrho=244 Ry`;
- plain mixing with `mixing_beta=0.7`;
- `conv_thr=1e-8 Ry`; and
- the exact scalar-relativistic PBE PAW pair above.

The tutorial cutoffs are slightly below the Ga header suggestions. They will not be
changed, and neither convergence nor pseudopotential suitability will be claimed.

The SCF stage uses an unshifted automatic `8x8x8` mesh. Its source input contains
`wf_collect=.true.`; QE 7.5 `INPUT_PW.def` marks that keyword obsolete and no longer
implemented. The source token will be retained, and any calculator treatment will be
captured rather than predicted.

The bands stage requests 16 bands and a `crystal_b` path through source-labeled
$L$, $\Gamma$, $X$, $K/U$, and $\Gamma$ vertices with listed coordinates
`(0,0.5,0)`, `(0,0,0)`, `(-0.5,0,-0.5)`, `(-0.375,0,-0.675)`, and
`(0,0,-1)`. The source requests interpolation counts 20, 30, 10, 30, and 20. The
actual generated path-point count and QE-transformed coordinates will be observed
rather than assumed. `bands.x` retains `lsym=.true.` for symmetry classification.

## Operational inputs and workspace plan

Execution, if authorized, will render three explicit operational inputs. Path-only
adaptations replace the source's shared `/tmp` and `../pseudos` locations with private
stage-local `./scratch`, `./pseudo`, and `../results` roles. Scientific settings remain
unchanged.

| Stage | Executable | Operational bytes | Operational SHA-256 |
|---|---|---:|---|
| SCF | `pw.x` | 534 | `28a88d5d08a146d78a3e77b33bd5f325506982c95bc424bd6a81e53b5db4766b` |
| Bands | `pw.x` | 659 | `cf3c14449cf81578932d289aa5ecc1972e11d0f69ed6331560129e73049a6c1d` |
| Bands postprocessing | `bands.x` | 111 | `ccb0e6ec20ca60db67d2783329871a9847cc36e74a6259edf8aa902e9bd2f83a` |

The metadata-only preflight identity is
`qe-7.5-gaas-bands-preflight-20260908T130223Z`. No operational input or
pseudopotential is staged there.

An authorized execution will create a new external Workflow root with private
`01-scf`, `02-bands`, and `03-bands-post` stage roots. Every stage will have distinct
inputs, streams, results, process records, and before/after snapshots. The bands stage
receives an identity-checked copy of the admitted SCF `GaAs.save` tree. `bands.x`
receives a separate identity-checked copy of the admitted bands state. No mutable
`outdir` is shared.

## Executables, scale, and resource envelope

The proposed local QE 7.5 executables are:

| Executable | Bytes | SHA-256 |
|---|---:|---|
| `pw.x` | 9,673,048 | `87aa72158e2c103c63fce1deca977dc42ff4ba344519a9662aadb96d33eab910` |
| `bands.x` | 8,018,632 | `fef09fe9d9967dd432859fc6affc8f28c2acaedefc78f16409897f273488b443` |

The local machine reports 10 logical CPUs, 24 GiB memory, and approximately 102 GiB
free storage. The proposed attempt will use:

- three sequential invocations, one local process and `OMP_NUM_THREADS=1` each;
- no MPI launcher, scheduler, remote, cluster, or cloud execution;
- five minutes each for SCF and bands, two minutes for `bands.x`, and a 15-minute
  complete-Workflow envelope;
- 1 GiB sampled resident-memory observation boundary;
- 1 GiB total new-storage envelope; and
- no automatic retry.

The system has two atoms, 18 pseudopotential valence electrons, an `8x8x8` SCF mesh,
16 requested bands, and a four-segment band path. The envelope is a conservative
estimate, not an observed runtime or memory result.

## Dependencies, failures, and expected outputs

SCF is required by bands, and bands is required by `bands.x`. A failed, timed-out,
diagnostically incomplete, or unadmitted predecessor leaves its successors explicitly
unattempted. No stage is retried without new authorization. A systemic identity,
confinement, storage, memory-capture, stream-capture, snapshot-capture, or batch-time
failure stops trustworthy further execution.

Expected bounded observations include:

- SCF total energy, occupied-state reference, convergence facts, and QEXSD state;
- bands-stage path coordinates, dimensions, eigenvalues, and native state;
- `bands.x` process output, symmetry labels, and `filband` artifacts;
- agreement checks between the postprocessor artifact and admitted bands state; and
- executable, input, pseudopotential, stream, snapshot, native-state, and admitted-copy
  identities plus timing and sampled resource observations.

Raw streams, pseudopotential bytes, charge density, wavefunctions, QEXSD trees, and
calculator artifacts will remain external and uncommitted. A compact calculated
observation will be proposed for retention only after result review.

## Recorded execution outcome

The authorized external run `qe-7.5-gaas-bands-20260911T004955Z` attempted each
eligible stage once. The SCF process returned zero, contained `JOB DONE.`, and reported
convergence in 27 iterations. Its native `GaAs.save` tree was admitted into the bands
stage through a 34-entry, 15,026,206-byte content-identical copy.

The bands process generated 91 path points, then printed nine `c_bands`
eigenvalue-nonconvergence diagnostics and stopped with `Error in routine c_bands (1):
too many bands are not converged`. It returned 1 and did not print `JOB DONE.`. Its
MPI-linked one-process executable emitted an `MPI_ABORT` stderr diagnostic even though
no `mpirun` or multi-process launch was used. The admitted native-state identity
remained unchanged, so no bands QEXSD result or bands artifact was admitted.

Under the authorized no-retry policy, `bands.x` remained explicitly unattempted because
its predecessor result was not admitted. The Workflow ended with an expected-stage
failure rather than a systemic identity, confinement, capture, memory, storage, or
batch-time failure. The attempted stages stayed within the resource envelopes and the
complete Workflow ended after approximately 68.9 seconds.

The compact calculated failure observation is retained at
`examples/tutorials/gaas-bands/qe/expected/qe75-calculated-observation.json`, SHA-256
`5670b50067599e1725fd7d9872cc0a21065f679cbe025d9aacd03a7224049c21`.
Raw operational inputs, pseudopotential bytes, streams, native state, and calculator
artifacts remain external and uncommitted. No retry or scientific-setting change is
authorized by this result.

## Relationship to the later SOC task

Completing this Task satisfies the declared Task-graph prerequisite for
`quantumespresso.simulations.soc-gaas`, but it does not create a controlled numerical
SOC baseline. The main GaAs tutorial here uses scalar-relativistic PBE PAW
pseudopotentials and `ibrav=2`. The separate SOC page uses a PBEsol ultrasoft
scalar/full-relativistic pair, an explicit `ibrav=0` cell, different sampling, and a
separate no-SOC branch. Direct subtraction or attribution of differences to SOC is
therefore prohibited unless a later owning specification establishes aligned geometry,
pseudopotential-family, basis, spin, energy-reference, and path conventions.
