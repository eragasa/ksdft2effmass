# Silicon wavefunction-cutoff convergence tutorial preflight

## Status and claim boundary

This document records the completed dry-run preflight and subsequent **calculated
tutorial execution** authorized by resolved checkpoint
`QE-SILICON-CUTOFF-CONVERGENCE-RUN-HC01`. All six points were attempted exactly once
on 2026-09-08. The result is a calculated tutorial observation and software-workflow
evidence only. It does not establish a production cutoff, an infinite-basis limit,
numerical verification, scientific validation, uncertainty quantification, or
scientific acceptance.

This Task is separate from k-point-density convergence. The six candidates are
independent: a point-level failure is retained but does not block attempts of the other
points. No point is retried without new authorization.

## Source and local-use boundary

The scientific settings come from the Pranab Das convergence tutorial and its source
repository at pinned commit `8d0087d05271beb13b240930d4643bf345541c7b`:

- <https://pranabdas.github.io/espresso/hands-on/convergence/>
- `src/silicon/pw.scf.silicon.in`, Git blob
  `c6c63eab0fdad886d8045cd31815c814a1a57299`, SHA-256
  `d65e0dd41d574fd75a877a0a22bb267760b0c55570a183777603ad63371ddaa9`;
- `src/silicon/si_scf_ecutoff.pwtk`, Git blob
  `b8e104947aa773b913f12d1b14467f0dff7844ee`, SHA-256
  `dfb8b9ad0fb4fc149df427d41f9300125a86b7a7cbc4bb450e8cf740b9c906b3`.

The upstream repository exposes no declared repository-level license. The execution
authorization was limited to local run-only use of the identified settings. No
upstream file or script was committed or redistributed, and PWTK was not installed or
invoked. The six runtime inputs are explicit operational renderings rather than copied
upstream files.

## Exact inputs

All six points are two-atom diamond-silicon `pw.x` self-consistent calculations. They
retain `ibrav=2`, `celldm(1)=10.26` Bohr, `nat=2`, `ntyp=1`, `nbnd=8`,
`mixing_beta=0.6`, `verbosity='high'`, the two positions `(0,0,0)` and
`(0.25,0.25,0.25)` in `alat` coordinates, and an unshifted automatic
$6\times6\times6$ mesh. The input does not set `conv_thr`, so the QE 7.5 default
remains in effect.

Only `ecutwfc`, expressed in Ry, and the operationally unique prefix vary:

| `ecutwfc` (Ry) | Input bytes | SHA-256 |
|---:|---:|---|
| 12 | 414 | `687298c13158e420829d7669961992b582495a9a020bd5ccf6bb139dcd510ef9` |
| 16 | 414 | `9ee18d85701e2e1dccf156f018e53a3ef92c1dc968160d2bf1321ebdf23030a4` |
| 20 | 414 | `937ad2a490ad6059799a2a6f24b4b19b96fdef33170392244f09cc486822f4bf` |
| 24 | 414 | `f46f2675695b46567579a10cc35291188243f082d68582b99293d03ee83f6f20` |
| 28 | 414 | `8eac40f616dc79b52397d35cc4a374e178f42185fbf3190ae6effd1b44634b0b` |
| 32 | 414 | `9b0935e5f1586446c77993409a218a03480b0c5ecd6f9b49260b7ffea9d3edb0` |

No value is added, removed, or changed in response to an observed trend. The six exact
input files are staged beneath external run identity
`qe-7.5-silicon-cutoff-convergence-20260908T033312Z`; the absolute machine path is not
a maintained identifier.

## Executable and pseudopotential

The authorized executable was the local Quantum ESPRESSO 7.5 `pw.x` built from commit
`770a0b2d12928a67048e2f3da8d10d057e52179e`:

- 9,673,048 bytes;
- SHA-256 `87aa72158e2c103c63fce1deca977dc42ff4ba344519a9662aadb96d33eab910`;
- Mach-O arm64.

The already-local `Si.pz-vbc.UPF` is 74,552 bytes with SHA-256
`e8d933754cd51c6bb4b2a809151f89e0647e53d878bab88d26e1b5a5d68d5217`.
Its exact XML content has been used by the earlier bounded silicon tutorial runs. That
history does not establish pseudopotential suitability, convergence, or a
file-specific license. Authorization was limited to copying this exact already-local file into the six
private workspaces for local execution; it was not committed or redistributed.

## Scale and resource envelope

The local machine reports 10 logical CPUs, 24 GiB memory, and approximately 105 GiB
free storage. The proposed attempt uses:

- six sequential `pw.x` invocations;
- one local process and `OMP_NUM_THREADS=1` per point;
- no MPI launcher, scheduler, network, remote, cluster, or cloud execution;
- two minutes maximum wall time per point and ten minutes for the complete attempt;
- 250 MB resident memory per running process;
- 500 MB total new storage; and
- no automatic retry.

A comparable retained two-atom QE 7.5 SCF completed in approximately 0.7 seconds and
used about 18 MB peak memory; this was the estimate basis. The exact six-point attempt
took 2.418 seconds in the execution wrapper, with per-point wrapper times from 0.234 to
0.616 seconds. The completed external run root occupied 9.2 MiB when reviewed, below
the 500 MB envelope. Peak resident memory was not captured, so no observed memory
claim is made.

## Workspace and invocation

The dry run created six private point roots beneath the external run identity. Each
contains separate `input`, `streams`, `work`, `results`, and `records` roles. After
protected-execution authorization, the exact pseudopotential was staged in each
point-local `work/pseudo` directory. The point-local invocation is:

```text
pw.x < ../input/si.scf.in > ../streams/stdout 2> ../streams/stderr
```

Before the first invocation, execution control verified every input identity, the
executable and pseudopotential identities, path confinement, available disk, point
inventory, and independent stream destinations. No systemic stop condition occurred.
All six independent points were attempted once without retry.

## Outputs and retention

Each point produced separate stdout/stderr streams, terminal process and timing
records, before/after inventories, QEXSD and calculator-native continuation state, and
a total-energy observation. Compact postprocessing produced one point-indexed table
with:

- `ecutwfc` in Ry;
- total energy in the represented QE unit when available;
- process completion and calculator-reported electronic convergence as separate facts;
- diagnostics and failure state; and
- elapsed time and observed resource use.

Raw streams, charge density, wavefunctions, `.save` trees, and other native state
remain external and uncommitted. The reviewed compact observation, SHA-256
`413161d5dac690aba9d53e07657f0ff469576089a259a55eb55b86c5ea45eb79`, is retained at
`examples/tutorials/silicon-wavefunction-cutoff-convergence/qe/expected/qe75-calculated-observation.json`.
All processes returned zero, contained `JOB DONE.`, and reported SCF convergence after
four iterations. Every stderr stream retained the same uncharacterized QE
floating-point exception note.

## Generic-design learning

This execution exposed the following requirements for a later generic parameter-study
representation:

- immutable study identity plus an ordered candidate identity and exact varied value;
- one isolated workspace and one attempt record per independent point;
- run-all-once scheduling in which a point failure does not suppress later points;
- separate process completion, calculator-reported SCF convergence, native-document
  exit state, and cross-candidate convergence status;
- property extraction with explicit source and unit, here printed Ry and QEXSD
  Hartree total energies;
- content identities for inputs, streams, snapshots, and native restart state;
- diagnostic retention that does not infer severity from process success; and
- explicit resource instrumentation, including an honest missing-observation state
  when peak resident memory is not captured.

The six successful points did not exercise the partial-failure branch, retry policy, or
systemic-stop path. This execution does not itself accept a generic public contract.
