# Superseded combined silicon convergence tutorial preflight

## Status and claim boundary

This combined 21-point preflight is **superseded without execution**. The human split
its wavefunction-cutoff and k-point-density studies into separate Tasks and separate
tutorial directory spaces. The lattice-parameter energy scan was removed from the
convergence scope; structural optimization remains the separate silicon
variable-cell-relaxation tutorial. No scientific executable was invoked under this
preflight, and checkpoint `QE-SILICON-CONVERGENCE-RUN-HC01` authorizes no execution.

The retained text records the abandoned combined proposal only. New execution requires
separate exact preflights and protected-execution checkpoints for
`quantumespresso.simulations.pranab_das.convergence-silicon-cutoff` and
`quantumespresso.simulations.pranab_das.convergence-silicon-kpoint-density`. Any later result is a
calculated tutorial observation and software-workflow evidence only; it is not a
production cutoff or mesh, numerical-verification result, scientific-validation
result, uncertainty quantification, or scientific acceptance.

## Source and reuse boundary

The tutorial source is the Pranab Das convergence page and its repository at pinned
commit `8d0087d05271beb13b240930d4643bf345541c7b`:

- <https://pranabdas.github.io/espresso/hands-on/convergence/>
- `src/silicon/pw.scf.silicon.in`
- `src/silicon/si_scf_ecutoff.pwtk`
- `src/silicon/si_scf_kpoints.pwtk`
- `src/silicon/si_scf_alat.pwtk`

The pinned source identities are:

| Source | Git blob | SHA-256 |
|---|---|---|
| `pw.scf.silicon.in` | `c6c63eab0fdad886d8045cd31815c814a1a57299` | `d65e0dd41d574fd75a877a0a22bb267760b0c55570a183777603ad63371ddaa9` |
| `si_scf_ecutoff.pwtk` | `b8e104947aa773b913f12d1b14467f0dff7844ee` | `dfb8b9ad0fb4fc149df427d41f9300125a86b7a7cbc4bb450e8cf740b9c906b3` |
| `si_scf_kpoints.pwtk` | `2d53cf6679e11aa6ea3830ae5f9d29377f7d1d80` | `87bb3561853c774170a41610bb4f1edb044d0d97dfea3eb695199b95dac24278` |
| `si_scf_alat.pwtk` | `cc8e75f985f9dbd8275360d1859feef17eb7255c` | `aea14c884b7cfdb0a3b0afc993ca0a3faac5834ee838cc1d69a625492c336ceb` |

The upstream repository exposes no declared repository-level license. Authorization is
therefore requested only for local run-only use of the identified settings. No
upstream input or script will be committed or redistributed. PWTK will not be
installed or invoked.

## Exact proposed calculations

All points are two-atom diamond-silicon `pw.x` self-consistent calculations. Except for
the named study variable and operational path/prefix adaptation, the pinned base input
is retained: `ibrav=2`, two silicon atoms at `(0,0,0)` and
`(0.25,0.25,0.25)` in `alat` coordinates, one atomic type, `nbnd=8`,
`mixing_beta=0.6`, and `verbosity='high'`. The input does not set `conv_thr`, so the
QE 7.5 default remains in effect.

The 21 independent points reproduce the three PWTK-script parameter sequences through
explicitly rendered `pw.x` inputs:

1. **Wavefunction-cutoff sweep:** `ecutwfc = {12, 16, 20, 24, 28, 32}` Ry;
   `celldm(1)=10.26` Bohr and the base unshifted $6\times6\times6$ mesh remain fixed.
2. **k-mesh sweep:** cubic meshes `{2, 4, 6, 8}` with shift `(1,1,1)`;
   `ecutwfc=30` Ry and `celldm(1)=10.26` Bohr remain fixed.
3. **Lattice-parameter sweep:** `celldm(1) = {9.7, 9.8, 9.9, 10.0, 10.1,
   10.2, 10.3, 10.4, 10.5, 10.6, 10.7}` Bohr; `ecutwfc=30` Ry and a shifted
   $6\times6\times6$ mesh remain fixed.

No trend-based extension, tolerance adjustment, automatic retry, or production setting
selection is permitted. Each point receives a unique prefix and isolated workspace.

## Executable, pseudopotential, and machine

The proposed executable is the local Quantum ESPRESSO 7.5 `pw.x` built from commit
`770a0b2d12928a67048e2f3da8d10d057e52179e`:

- 9,673,048 bytes;
- SHA-256 `87aa72158e2c103c63fce1deca977dc42ff4ba344519a9662aadb96d33eab910`;
- Mach-O arm64.

The already-local `Si.pz-vbc.UPF` is 74,552 bytes with SHA-256
`e8d933754cd51c6bb4b2a809151f89e0647e53d878bab88d26e1b5a5d68d5217`.
Its local run-only use was previously authorized for the silicon tutorial calculations.
The file is not proposed for repository retention or redistribution; its use here does
not establish suitability or convergence.

The local machine reports 10 logical CPUs, 24 GiB memory, and approximately 105 GiB
free storage. The proposed envelope is:

- 21 sequential invocations, each with one local process and `OMP_NUM_THREADS=1`;
- no MPI launcher, scheduler, network, remote, cluster, or cloud execution;
- two minutes maximum wall time per point and 20 minutes for the complete attempt;
- 250 MB resident memory per running process;
- 1 GiB total new storage;
- every independent point is attempted even if another point fails; and
- no automatic retry.

A comparable retained two-atom QE 7.5 SCF completed in approximately 0.7 seconds and
used about 18 MB peak memory. That is only an estimate basis; runtime and resource use
for these 21 exact points have not been observed.

## Workspace, command, and stopping rules

One new external run root named
`qe-7.5-silicon-convergence-<UTC timestamp>` will be created under the established
local tutorial-run area. Every point has separate `input`, `pseudo`, `streams`,
`work`, `results`, and `records` roles. Before execution, a dry run will verify the
rendered input identity, executable and pseudopotential identity, path confinement,
stream destinations, available storage, and complete 21-point inventory.

Each stage invokes the executable directly from its own work directory:

```text
pw.x < input.in > stdout 2> stderr
```

Standard output and standard error remain separate. A point-level nonzero exit,
timeout, missing `JOB DONE.`, or calculator diagnostic is recorded for that point but
does not block the other independent points. The batch stops only for a systemic
preflight or execution-control failure that prevents trustworthy independent attempts,
such as an executable or pseudopotential identity mismatch, path-confinement failure,
insufficient resource envelope, or broken stream/snapshot capture. Failed, attempted,
and systemically unattempted points remain explicit. No point is retried without new
authorization.

## Expected outputs and retention

Each attempted point is expected to produce separate streams, a process exit/timing
record, before/after workspace inventories, QEXSD/native continuation state, and a
total-energy observation. Compact postprocessing will produce three point-indexed
energy tables and retain diagnostics without classifying them as harmless or fatal.

Raw streams, charge density, wavefunctions, `.save` trees, and other native state
remain external and uncommitted. Only compact provenance, bounded observations, and
workflow lessons may later be proposed for repository retention after review.

## Generic-design questions grounded by the run

The attempt is intended to observe, rather than pre-decide, how a generic layer should
represent a parameter-study revision, per-point immutable input identity, independent
execution attempts, QoI extraction, partial failure, native-state retention, and the
distinction between process completion, electronic convergence, and cross-point
parameter convergence.
