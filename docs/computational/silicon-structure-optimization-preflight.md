# Silicon structure-optimization tutorial preflight

## Status

This document contains the completed preflight and the bounded outcome of one
subsequently authorized **calculated tutorial execution**. It is not production
convergence, numerical verification, scientific validation, uncertainty
quantification, or acceptance of a project geometry. A later human decision selected
its QEXSD-derived geometry only for the bounded tutorial DOS Workflow.

Human decision `QE-SILICON-DOS-INPUT-HC01` selected preservation of the
structure-optimization prerequisite for the silicon DOS Workflow. Checkpoint
`QE-SILICON-VCRELAX-RUN-HC01` then authorized one independent CPN Task invocation,
which completed once without retry. Its result did not automatically become the
governing DOS geometry. Human decision `QE-SILICON-DOS-GEOMETRY-HC01` subsequently
selected it for the bounded tutorial DOS Workflow without promoting it to a project
lattice reference.

## Source and input identity

The source is the silicon structure-optimization tutorial at
<https://pranabdas.github.io/espresso/hands-on/structure-optimization/> and its linked
repository at commit `8d0087d05271beb13b240930d4643bf345541c7b`.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `src/silicon/si_relax.in` | 470 | `431deda61591cd14a72763b801bd1648fbba17699cad2ffa8d36115a9348f2ec` |
| Already-local `Si.pz-vbc.UPF` | 74,552 | `e8d933754cd51c6bb4b2a809151f89e0647e53d878bab88d26e1b5a5d68d5217` |

The already-local pseudopotential differs bytewise from the pinned source copy but has
the byte-identical XML canonical form recorded in the
[SCF-to-NSCF-to-DOS preflight](silicon-scf-nscf-dos-preflight.md). That establishes
represented XML-content identity only. It does not establish pseudopotential
suitability, convergence, validation, or a file-specific license.

The upstream repository exposes no repository-level reuse terms in the campaign
record. The proposed authorization is therefore limited to local run-only staging of
the exact input and already-local pseudopotential, with no redistribution.

## Exact proposed scientific settings

The pinned input specifies:

- `pw.x` with `calculation='vc-relax'`;
- two-atom diamond silicon with `ibrav=2` and initial `celldm(1)=14` Bohr;
- fixed fractional atomic positions at `(0,0,0)` and `(0.25,0.25,0.25)` through zero
  movement flags;
- `cell_dofree='ibrav'`, allowing cell changes while retaining consistency with the
  initial Bravais-lattice choice;
- 30 Ry wavefunction cutoff;
- an automatic shifted $6\times6\times6$ k-point mesh with shift `(1,1,1)`;
- electronic `conv_thr=1e-8` Ry;
- ionic `etot_conv_thr=1e-5` atomic units and `forc_conv_thr=1e-4` atomic units;
- the QE default pressure convergence threshold because `press_conv_thr` is omitted;
  QE 7.5 documents that default as `0.5` kbar; and
- `prefix='silicon'`, `outdir='./tmp/'`, and `pseudo_dir='./pseudos/'`.

The tutorial reports a final lattice constant of `10.2076` Bohr and gives printed
final-coordinate and enthalpy excerpts. Those are upstream tutorial reference values
to inspect, not acceptance thresholds and not observations from the proposed QE 7.5
run.

No scientific setting may be changed or retried automatically. In particular, the
initial 14 Bohr cell, cutoff, mesh, atomic constraints, convergence thresholds, cell
degrees of freedom, and pseudopotential identity remain exact.

## Executable, scale, and resources

The proposed executable is the completed local Quantum ESPRESSO 7.5 `build/bin/pw.x`
from source commit `770a0b2d12928a67048e2f3da8d10d057e52179e`:

- 9,673,048 bytes;
- SHA-256 `87aa72158e2c103c63fce1deca977dc42ff4ba344519a9662aadb96d33eab910`;
- Mach-O arm64.

The input is a two-atom primitive cell with one varying cell degree family and fixed
atomic positions. The number of ionic/cell steps is an output to observe. Based only
on the previously observed sub-second two-atom QE 7.5 SCF scale, this tutorial is
expected to finish locally within minutes, but no runtime for this exact relaxation has
been observed.

The conservative envelope is:

- one local process with `OMP_NUM_THREADS=1`;
- ten minutes wall time;
- 500 MB resident memory;
- 100 MB new storage;
- no network, scheduler, remote, cluster, or cloud execution; and
- exactly one invocation with no automatic retry.

At preflight, the machine had 10 logical CPUs, 24 GiB memory, and approximately
107 GiB free storage.

## Independent CPN Task and workspace

The operation is one reusable `QuantumEspressoVcRelaxTask` role and one run-scoped CPN
Task instance. The name is prospective and private, not a stabilized public API. The
Task owns one activation, attempt, execution grant, isolated workspace, process
observation, ResultObject, result ingress, and failure boundary.

If authorized, create one external run root named
`qe-7.5-silicon-vcrelax-<UTC timestamp>` under the ignored run area with no symbolic
links:

```text
<run-root>/
  work/
    si_relax.in
    pseudos/Si.pz-vbc.UPF
    tmp/
  streams/
  snapshots/
  records/
  results/
```

Running from `work/` preserves all source-relative paths without modifying the input
bytes. The exact proposed scientific invocation is:

```text
pw.x < si_relax.in > ../streams/stdout 2> ../streams/stderr
```

A wrapper records start/end UTC timestamps, wall time, resource usage, and exit state.
The Task must capture complete `before` and `after` inventories with relative path,
object type, byte count, modification time, and SHA-256 for regular files.

A nonzero exit, missing `JOB DONE.`, calculator error, timeout, resource-limit breach,
or artifact-identity mismatch produces no successful result ingress. There is no
second attempt without a new authorization.

## Outputs and retained observations

The Task is expected to produce calculator-native continuation state under
`work/tmp/silicon.save`, standard streams, and printed final-coordinate information.
Postprocessing must record, when present:

- process completion and exact diagnostics;
- calculator-reported relaxation and electronic-convergence states separately;
- cell/ionic step counts;
- initial and final cell representations with units;
- final atomic positions and their constraint flags;
- final volume, pressure, enthalpy, forces, and stress only when represented;
- QEXSD and native continuation-artifact identities; and
- agreement or disagreement with the upstream printed excerpt as a mechanical
  comparison, not an acceptance test.

Large native state remains outside Git. Compact repository evidence may retain exact
identities and bounded parsed summaries.

## Claim boundary and downstream disposition

The completed run is one **calculated tutorial observation** of QE 7.5 variable-cell
relaxation behavior for the exact input. It does not establish a production-converged
lattice, pseudopotential suitability, numerical verification, scientific validation,
uncertainty quantification, or acceptance as a project geometry.

Human decision `QE-SILICON-DOS-GEOMETRY-HC01` selected the exact observed QEXSD-derived
geometry for the bounded tutorial DOS Workflow. The choice was explicit and was not
inferred from numerical proximity to the pinned `10.2076` Bohr value.

## Calculated tutorial outcome

The exact authorized QE 7.5 `pw.x` invocation ran once on 2026-09-03 in external run
`qe-7.5-silicon-vcrelax-20260903T070455Z`.

- Exit status was 0, timeout did not occur, and `JOB DONE.` was present.
- Wrapper wall time was approximately 15.78 seconds; `/usr/bin/time` reported
  59,195,392 bytes maximum resident set size.
- QE reported BFGS convergence after 14 SCF cycles and 12 BFGS steps.
- The printed BFGS final enthalpy was `-15.8536258899` Ry.
- The printed final volume was `265.88606` Bohr$^3$ and the QEXSD final cell implies a
  conventional cubic lattice constant of `10.207479550732002` Bohr.
- QE's distinct post-relaxation final SCF reported convergence in six iterations,
  printed total energy `-15.85238670` Ry, and pressure `-1.22` kbar. These are not the
  preceding BFGS enthalpy and terminal optimization pressure.
- Standard output retained six BFGS curvature-condition warnings and fourteen
  `c_bands` messages reporting one unconverged eigenvalue during intermediate work.
  Standard error retained the recurring IEEE floating-point exception flags. These
  diagnostics were not silently classified as harmless or fatal.
- QEXSD 25.05.21, charge density, 28 wavefunction files, snapshots, streams, and the
  native-state tree remain external. The native-state manifest contains 31 files with
  tree identity SHA-256
  `eecf12a8096e83a2e16411f8258667bd85e88ec521f2621659166e7febf7a6ab`.

The compact calculated observation is retained at
`examples/tutorials/silicon-structure-optimization/qe/expected/qe75-calculated-observation.json`.
Checkpoint `QE-SILICON-DOS-GEOMETRY-HC01` records the later selection of this
calculated geometry for the bounded tutorial DOS Workflow. That Workflow completed
under separate checkpoint `QE-SILICON-DOS-RUN-HC01`; neither result is a project
lattice reference.
