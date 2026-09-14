# Silicon k-point-density convergence tutorial preflight

## Status and claim boundary

This document records the completed dry-run preflight and subsequent **calculated
tutorial execution** authorized by resolved checkpoint
`QE-SILICON-KPOINT-DENSITY-CONVERGENCE-RUN-HC01`. All four points were attempted
exactly once on 2026-09-08. The result is a calculated tutorial observation and
software-workflow evidence only. It does not establish a production mesh,
Brillouin-zone integration convergence, numerical verification, scientific validation,
uncertainty quantification, or scientific acceptance.

This Task is separate from wavefunction-cutoff convergence. The four candidates are
independent: a point-level failure will be retained but will not block attempts of the
other points. No point will be retried without new authorization.

## Source and local-use boundary

The scientific settings come from the Pranab Das convergence tutorial and its source
repository at pinned commit `8d0087d05271beb13b240930d4643bf345541c7b`:

- <https://pranabdas.github.io/espresso/hands-on/convergence/>;
- `src/silicon/pw.scf.silicon.in`, Git blob
  `c6c63eab0fdad886d8045cd31815c814a1a57299`, SHA-256
  `d65e0dd41d574fd75a877a0a22bb267760b0c55570a183777603ad63371ddaa9`;
- `src/silicon/si_scf_kpoints.pwtk`, Git blob
  `2d53cf6679e11aa6ea3830ae5f9d29377f7d1d80`, SHA-256
  `87bb3561853c774170a41610bb4f1edb044d0d97dfea3eb695199b95dac24278`.

The upstream repository exposes no declared repository-level license. The execution
authorization was limited to local run-only use of the identified settings. No
upstream file or script was committed or redistributed, and PWTK was not installed or
invoked. The four runtime inputs are explicit operational renderings rather than
copied upstream files.

## Exact inputs

All four points are two-atom diamond-silicon `pw.x` self-consistent calculations. They
retain `ibrav=2`, `celldm(1)=10.26` Bohr, `nat=2`, `ntyp=1`, `ecutwfc=30` Ry,
`nbnd=8`, `mixing_beta=0.6`, `verbosity='high'`, the two positions `(0,0,0)` and
`(0.25,0.25,0.25)` in `alat` coordinates, and a shifted cubic automatic mesh. The
input does not set `conv_thr`, so the QE 7.5 default remains in effect.

Only the cubic mesh size and the operationally unique prefix vary. Every shift is
`(1,1,1)`:

| Mesh | Input bytes | SHA-256 |
|---|---:|---|
| `2x2x2` | 422 | `4ac8f67200c28c0dbcd52a4a335bddf3f5a2567baaed5b51d71f8178684f01e3` |
| `4x4x4` | 422 | `5ebe5b90b98f271370d440f191e5bd28f33e0e611c5d2f464dd43d8e80c2c725` |
| `6x6x6` | 422 | `97a1bf19623156dc8016af17485ae363e1ba2b43cef545f02c8dc8cd1269d33d` |
| `8x8x8` | 422 | `361d4d56ba23216065676c24f08ed6a320a6eb1a1c4c45a7f12de1b01bcc8189` |

No value was added, removed, or changed in response to an observed trend. The four
exact input files are staged beneath external run identity
`qe-7.5-silicon-kpoint-density-convergence-20260908T040332Z`; the absolute machine path
is not a maintained identifier.

## Density convention

Let $A$ contain the primitive direct-lattice vectors as rows and let $B$ contain the
reciprocal vectors as rows. The project convention is $A B^T=2\pi I$. With
$a=10.26$ Bohr and QE `ibrav=2`, the represented direct primitive-cell volume is
$a^3/4=270.011394$ Bohr$^3$, and the reciprocal primitive-cell volume is

$$
\Omega_{\mathrm{reciprocal}}
= \frac{(2\pi)^3}{a^3/4}
= 0.9186657265374458\ \mathrm{Bohr}^{-3}.
$$

The calculator-neutral scalar abscissa is
$\rho_k=N_{\mathrm{full}}/\Omega_{\mathrm{reciprocal}}$. The dry-run values are:

| Mesh | $N_{\mathrm{full}}$ | $\rho_k$ (Bohr$^3$) |
|---|---:|---:|
| `2x2x2` | 8 | 8.708281770947195 |
| `4x4x4` | 64 | 69.66625416757756 |
| `6x6x6` | 216 | 235.12360781557425 |
| `8x8x8` | 512 | 557.3300333406205 |

The mesh and shift remain explicit because the scalar density does not encode sampling
anisotropy or offset. The symmetry-reduced point count is not used to define density;
it will be retained separately as backend-observed metadata.

## Executable and pseudopotential

The authorized executable was the local Quantum ESPRESSO 7.5 `pw.x` built from commit
`770a0b2d12928a67048e2f3da8d10d057e52179e`:

- 9,673,048 bytes;
- SHA-256 `87aa72158e2c103c63fce1deca977dc42ff4ba344519a9662aadb96d33eab910`;
- Mach-O arm64.

The already-local `Si.pz-vbc.UPF` is 74,552 bytes with SHA-256
`e8d933754cd51c6bb4b2a809151f89e0647e53d878bab88d26e1b5a5d68d5217`.
Its exact XML content was used by the completed cutoff tutorial attempt. That history
does not establish pseudopotential suitability, mesh convergence, or a file-specific
license. Authorization was limited to copying this exact already-local file into the four
private workspaces for local execution; it was not committed or redistributed.

## Scale and resource envelope

The local machine reports 10 logical CPUs, 24 GiB memory, and approximately 105 GiB
free storage. The proposed attempt uses:

- four sequential `pw.x` invocations;
- one local process and `OMP_NUM_THREADS=1` per point;
- no MPI launcher, scheduler, network, remote, cluster, or cloud execution;
- two minutes maximum wall time per point and eight minutes for the complete attempt;
- 250 MB resident memory per running process;
- 500 MB total new storage; and
- no automatic retry.

The completed six-point cutoff attempt took 2.418 seconds in its execution wrapper,
with its most expensive point taking 0.616 seconds; this was the estimate basis. The
exact four-point attempt took 3.358 seconds in the execution wrapper, with per-point
wrapper times from 0.207 to 1.810 seconds. Sampled resident-memory observations ranged
from 35,600 to 42,368 KiB and may underestimate instantaneous maxima. The post-run
external tree occupied approximately 12 MiB, below the 500 MB envelope.

## Workspace and invocation

The dry run created four private point roots beneath the external run identity. Each
contains separate `input`, `streams`, `work`, `results`, and `records` roles. After
protected-execution authorization, the exact pseudopotential was staged in each
point-local `work/pseudo` directory. The point-local invocation was:

```text
pw.x < ../input/si.scf.in > ../streams/stdout 2> ../streams/stderr
```

Before the first invocation, execution control verified every input identity, the
executable and pseudopotential identities, path confinement, available disk, point
inventory, independent stream destinations, and memory observation. No systemic stop
condition occurred. All four independent points were attempted once without retry.

## Outputs and retention

Each point produced separate stdout/stderr streams, terminal process, sampled-memory
and timing records, before/after inventories, QEXSD and calculator-native continuation
state, and a total-energy observation. Compact postprocessing produced one
point-indexed table with:

- mesh and shift;
- full-grid count;
- reciprocal primitive-cell volume and full-grid point density;
- backend-observed irreducible point count when represented;
- total energy in the represented QE unit when available;
- process completion and calculator-reported electronic convergence as separate facts;
- diagnostics and failure state; and
- elapsed time and observed resource use.

Raw streams, charge density, wavefunctions, `.save` trees, and other native state
remain external and uncommitted. The reviewed compact observation, SHA-256
`bb5c7ed47eae23eec3c828684f12ff417f81f685816473cce67fbd78e06a8834`, is retained at
`examples/tutorials/silicon-k-point-density-convergence/qe/expected/qe75-calculated-observation.json`.
All processes returned zero, contained `JOB DONE.`, and reported SCF convergence after
four iterations. Every stderr stream retained the same uncharacterized QE
floating-point exception note.

## Generic-design learning

The run confirms that a scalar parameter field is insufficient for this study. A later
generic parameter-study representation must retain the structured mesh and shift as
candidate inputs while storing full-grid density as a derived quantity with its
formula, reciprocal-cell convention, units, and geometry dependency. The
symmetry-reduced count is calculator output and must not replace the full-grid count in
the density definition.

The cutoff-study requirements for independent workspaces, run-all-once scheduling,
separate process/calculator/native statuses, source-qualified quantities, diagnostics,
and content identities remained applicable. Sampled memory additionally demonstrates
that resource observations need a method label and limitation rather than an
unqualified peak-memory field. The four successful points did not exercise partial
failure, retry, or systemic-stop behavior. This execution does not itself accept a
generic public contract.
