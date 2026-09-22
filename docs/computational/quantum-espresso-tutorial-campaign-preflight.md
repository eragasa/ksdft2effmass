# Quantum ESPRESSO tutorial campaign read-only preflight

## Status

This record captures the campaign-wide read-only preflight performed at
`2026-09-21T18:57:54Z`. It covers the Quantum ESPRESSO 7.2 bundled-example
inventory and the Pranab Das hands-on inventory. No Task was activated, no run
workspace was created, no scientific executable was entered, and no execution
grant was issued.

The checks below establish only local inventory and candidate readiness. They
do not establish that a tutorial is scientifically appropriate, numerically
verified, validated, or authorized to run.

## Campaign frontier

The repository contains 159 Quantum ESPRESSO leaf Task records:

| Campaign | Leaf records | Current dispositions |
|---|---:|---|
| QE 7.2 bundled examples | 134 | 134 blocked |
| Pranab Das hands-on tutorials | 25 | 16 blocked, 6 completed, 2 deliberately deferred, 1 superseded |

The superseded combined silicon-convergence Task is not an execution candidate.
Its cutoff and k-point-density successors are complete tutorial observations.
There are therefore 158 current leaf Tasks. Of those, 142 remain blocked rather
than having an execution or deliberate-deferral disposition.

The completed Pranab Das observations are GaAs bands, silicon cutoff
convergence, silicon k-point-density convergence, silicon DOS, nickel spin
bands, and silicon structure optimization. Silicon SCF and silicon bands are
deliberately deferred without rerun because their retained observations lack
the required stage-specific snapshots.

## Local installations

The inspected QE 7.2 source header remains byte-identical to the campaign
inventory:

- source root: `/Users/eugene/projects/q-e-qe-7.2`;
- `include/qe_version.h` SHA-256:
  `d82a82f1ae1c97923343304ed8a8cd4629d5c6643c4aed5b63083b238dc62316`;
- isolated `build/bin/pw.x` SHA-256:
  `6e8720e74cbafa7c7f07ee61ec6f5944c15d59bffa8ee8423fae14364f21c8ca`;
- executable files in `build/bin`: 13; and
- executable files in the examples' configured `${QE_SOURCE_ROOT}/bin`: 0.

The side-by-side QE 7.5 build contains 107 executable files. Its `pw.x` and
`pw2wannier90.x` identities agree with the installation record:

- `pw.x` SHA-256:
  `87aa72158e2c103c63fce1deca977dc42ff4ba344519a9662aadb96d33eab910`;
- `pw2wannier90.x` SHA-256:
  `61c8255b0745df2a5dec3c55e600b1f8b87039b564004997ac45cfee42cf2c8c`.

The QE 7.5 installation does not satisfy a QE 7.2 Task identity. Any use of 7.5
requires a separate manifest, source/executable correlation, preflight, and
grant.

The local machine has `mpirun`, `curl`, and `wget`. It does not have `gnuplot`
or PWTK on `PATH`. Tool availability is not permission to invoke a tool or to
access the network.

## QE 7.2 bundled examples

A static scan covered all 149 scripts in all 134 runnable groups. The scan
recognized executable names referenced through `BIN_DIR` and pseudopotential
filenames written literally in the scripts. It found:

| Static requirement | Distinct names | Present in the QE 7.2 local location |
|---|---:|---:|
| QE executables referenced through `BIN_DIR` | 54 | 2 (`pw.x`, `sumpdos.x`) |
| Pseudopotential filenames | 106 | 8 |

The QE 7.2 `pseudo/` directory contains 19 pseudopotential-like artifacts plus
the `clean_ps` script. Ninety-eight statically referenced pseudopotential names
are absent. The common examples environment attempts to download missing
pseudopotentials, but network acquisition is not authorized and would not
establish license, content identity, format admission, or scientific selection.

Only three groups pass the narrow static intersection of locally available
`BIN_DIR` executables and literally referenced pseudopotentials:

- `quantumespresso.simulations.qe_examples.pp.cls-fs-example`;
- `quantumespresso.simulations.qe_examples.pw.example03`; and
- `quantumespresso.simulations.qe_examples.pw.exx-example`.

This is not an execution-ready finding. The first uses Rh and a core-excited Rh
pseudopotential, the second runs three molecular-dynamics calculations, and the
third performs a multi-branch hybrid-functional study. Each is outside the
current silicon-impurity production path or requires a materially larger
resource and scientific-scope review.

The three QEHeat scripts appeared dependency-free under the narrow `BIN_DIR`
scan, but inspection rejected that result: they invoke a source-relative
`all_currents.x`, and at least one script requests twelve MPI ranks. They are
not ready under the local QE 7.2 build or the current authorization.

No bundled `run_example` script may be invoked directly. The scripts write
`results/` beneath the retained source tree, point `TMP_DIR` into the source
tree, delete matching temporary state, and can download missing
pseudopotentials. A future attempt must extract exact constituent commands into
an isolated manifest and pass the protected Workflow lifecycle.

PW example01 remains only partially observed. The isolated silicon SCF
constituent has a retained calculated observation, but the complete bundled
group still lacks the Al, Cu, and Ni pseudopotentials and has no complete-group
disposition.

## Pranab Das hands-on tutorials

All 16 blocked current Tasks still require exact source/input reuse resolution,
pseudopotential identity and terms, resource estimates, native-output
retention, and one-attempt authority. The QE 7.5 build has the principal QE
executables named by the campaign, including `pw.x`, `bands.x`, `dos.x`,
`projwfc.x`, `epsilon.x`, `fs.x`, `ph.x`, `q2r.x`, `matdyn.x`, `hp.x`, and
`pw2wannier90.x`. A local Wannier90 executable is also present. This is tool
inventory only; the required executable identities and compatibility must be
bound separately for each Task.

The blocked frontier separates into:

- silicon-relevant candidates: dielectric response, JDOS, k-resolved DOS, and
  Wannier construction; and
- learning-only or currently out-of-scope candidates: graphene, Fe and GaAs
  spin-orbit examples, aluminum workflows, copper Fermi surface, iron
  magnetism, FeO DFT+U, water molecular dynamics, Bi2Se3, and GaAs phonons.

The phonon campaign remains outside the authorized project research scope.
Inventory does not authorize `ph.x`, `q2r.x`, or `matdyn.x` execution. The
Wannier tutorial remains deferred until the separately controlled Wannier phase.
The PWTK-controlled aluminum sweep also lacks its orchestration dependency.

## Recommended traversal order

1. Finish the reusable confirmed-outcome assembler and atomic terminal-ingress
   Workflow owners. The currently retained fixture proves the lifecycle but the
   post-dispatch composition is still test-owned.
2. Resolve the pinned tutorial source/reuse boundary and exact input identity
   before copying or adapting any remaining Pranab Das input.
3. Preflight `dielectric-silicon` first because it is the lowest-ranked blocked
   silicon candidate and is a prerequisite for a defensible JDOS attempt.
4. Preflight `jdos-silicon`, then `kresolved-dos-silicon`, one Task and one grant
   at a time. A failed or indeterminate attempt does not activate its successor.
5. Keep `wannier-silicon` for the separately authorized Wannier phase.
6. Request an explicit scientific-scope disposition before preparing any
   non-silicon, molecular-dynamics, DFT+U, topological-insulator, or phonon
   attempt.
7. Traverse the 134 bundled groups by explicit execution-or-deferral
   disposition rather than invoking their scripts. Start with PW groups whose
   constituent mechanics are relevant to the project; defer unavailable or
   out-of-scope components with recorded evidence instead of installing or
   downloading dependencies implicitly.

A future execution request must identify the exact Task, QE release and
executable hash, input and pseudopotential bytes, isolated root, process count,
thread count, memory, disk, runtime ceiling, expected outputs, retention policy,
and one-dispatch grant. This preflight supplies none of those grants.
