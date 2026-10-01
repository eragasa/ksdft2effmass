# Silicon SCF-to-NSCF-to-DOS tutorial preflight

## Status

The read-only preflight and one authorized **calculated tutorial Workflow
observation** are complete. Human decision `QE-SILICON-DOS-INPUT-HC01` preserved the
structure-optimization prerequisite; `QE-SILICON-VCRELAX-RUN-HC01` produced its
calculated QE 7.5 observation; and `QE-SILICON-DOS-GEOMETRY-HC01` selected the exact
QEXSD-derived geometry for this Workflow. Human decision `QE-SILICON-DOS-RUN-HC01`
then authorized exactly three separate local Task dispatches.

Workflow run `qe-7.5-silicon-dos-20260903T102922Z` completed once without retry. SCF,
NSCF, and DOS were independent reusable CPN Task instances with distinct activations,
attempts, execution grants, private workspaces, process observations, result
ingresses, and CPN firings. Each process exited with status 0 and printed `JOB DONE.`.
This status records observed execution behavior, not production convergence,
scientific validation, uncertainty quantification, accepted project geometry, or a
project reference DOS.

## Tutorial source identity

The source is the silicon density-of-states tutorial at
<https://pranabdas.github.io/espresso/hands-on/dos/> and its linked repository at
commit `8d0087d05271beb13b240930d4643bf345541c7b`. The public source did not expose
repository-level reuse terms during campaign intake, so no source input or
pseudopotential is copied into this repository.

| Source file | Bytes | SHA-256 |
|---|---:|---|
| `src/silicon/pw.scf.silicon_dos.in` | 449 | `f102744e1d196f0e029fbad7ff3040f7176cb50dc2c059c9e9f6515b6511bd0b` |
| `src/silicon/pw.nscf.silicon_dos.in` | 481 | `f703c0d2bd399f05f60d4a853414767803df812b24f14c8513b5e66ec8821dc6` |
| `src/silicon/pp.dos.silicon.in` | 94 | `9d1eedb8d792fddcdbf0bb6d266799cf98f36655c033a24015f48eb45230fe65` |
| `src/pseudos/Si.pz-vbc.UPF` | 74,554 | `da7386b1345863effd34d47c07894a620d12e87069a009b5eaa2a88da7ea8105` |

The source pseudopotential and the already-local historical QE tutorial artifact
(SHA-256 `e8d933754cd51c6bb4b2a809151f89e0647e53d878bab88d26e1b5a5d68d5217`,
74,552 bytes) differ only in serialization of the `PP_HEADER` XML element. Python
XML canonicalization produced byte-identical canonical forms with SHA-256
`94098cd71310b1997b47d5c5a15d71337b818d856507c8d103d228fac34c435d`.
This establishes XML-content identity, not pseudopotential suitability, convergence,
or a file-specific license.

## Exact proposed scientific inputs

The three pinned source inputs specify the following tutorial settings:

| Concern | SCF | NSCF | DOS postprocessing |
|---|---|---|---|
| Program and mode | `pw.x`, `calculation='scf'` | `pw.x`, `calculation='nscf'` | `dos.x` |
| Structure | two-atom diamond Si, `ibrav=2`, `celldm(1)=10.2076` Bohr | identical | read from native state |
| Positions | `(0,0,0)` and `(0.25,0.25,0.25)` in `alat` units | identical | read from native state |
| Plane-wave cutoff | 50 Ry | 50 Ry | read from native state |
| Bands | 8 | 8 | read from native state |
| Occupations | calculator default | `tetrahedra` | tetrahedron method expected from NSCF state |
| Sampling | automatic unshifted $8\times8\times8$ mesh | automatic unshifted $12\times12\times12$ mesh | read from native state |
| Electronic controls | `conv_thr=1e-8` Ry; `mixing_beta=0.6` | same | not applicable |
| Energy grid | not applicable | not applicable | $[-9,16]$ eV; `DeltaE` omitted |
| Continuation identity | `prefix='silicon'`, `outdir='./tmp/'` | same | same |

For the identified QE 7.5 source, omitted `DeltaE` defaults to `0.01` eV. The stated
range therefore predicts 2,501 DOS data rows. The expected non-spin-polarized output
columns are energy in eV, DOS in states/eV, and integrated DOS. These are expectations
from the exact input and QE source, not observed outputs.

The tutorial prose says to set `nosym=.TRUE.` for the NSCF stage, but the pinned NSCF
input does **not** contain that setting. An exact pinned-input run must not silently add
it. The prose also says that a larger `nbnd` may be selected, while the pinned input
uses eight bands in both stages. The irreducible k-point count is therefore an output
to observe rather than a preflight claim.

### Selected geometry and adapted input identities

The source says that `celldm(1)=10.2076` Bohr came from a relaxation calculation, but
the DOS SCF input contains that value directly and consumes no relaxation artifact.
Human decision `QE-SILICON-DOS-INPUT-HC01` therefore preserved the durable dependency
on `quantumespresso.simulations.structure-optimization-silicon`, and human decision
`QE-SILICON-DOS-GEOMETRY-HC01` selected its calculated QEXSD-derived
`10.207479550732002` Bohr lattice constant for this tutorial Workflow.

The exact adapted scientific-input construction replaces the unique ASCII byte string
`celldm(1) = 10.2076` with
`celldm(1) = 10.207479550732002` in both pinned `pw.x` source inputs. Applying the same
mechanical substitution to the NSCF input is required because it repeats the same
cell definition and consumes the SCF native state. No other source-input byte changes.
The adapted identities are:

| Adapted input | Bytes | SHA-256 |
|---|---:|---|
| `pw.scf.silicon_dos.in` | 460 | `23714f9a78a1e6436b4a0b68ce58932e14141e1efa69a82eb0e2c4e950582657` |
| `pw.nscf.silicon_dos.in` | 492 | `5b0ee9fbc27f735a652845a96a122fc59d9e7d59e5d37f5e8ccda18edf5afd34` |

The unchanged source `pp.dos.silicon.in` identity remains the one listed above. Because
the public source did not expose repository-level reuse terms during intake, neither
the source nor adapted input bytes are copied into this repository. These identities
are exact staging requirements, not a project lattice reference or accepted geometry.

## Executables and local resource envelope

The proposed programs are from the completed local Quantum ESPRESSO 7.5 build at
source commit `770a0b2d12928a67048e2f3da8d10d057e52179e`.

| Executable | Bytes | SHA-256 | Format |
|---|---:|---|---|
| `build/bin/pw.x` | 9,673,048 | `87aa72158e2c103c63fce1deca977dc42ff4ba344519a9662aadb96d33eab910` | Mach-O arm64 |
| `build/bin/dos.x` | 7,885,000 | `0b5dfbbf63e0dba23771d9ddeb25991b14148f2fc9f819be61745b2d288b33f8` | Mach-O arm64 |

A previous identified two-atom QE 7.5 SCF tutorial run used about 35 MB maximum RSS
and less than 1 MB of external scratch. The denser NSCF stage was expected to cost
more. The authorized conservative limits were:

- one local process and `OMP_NUM_THREADS=1` for each sequential stage;
- five minutes and 500 MB resident memory per `pw.x` invocation;
- one minute and 250 MB resident memory for `dos.x`;
- 300 MB of new storage for the enclosing Workflow and three private Task workspaces, including identity-preserving native-state copies; and
- no network, scheduler, remote, cluster, or cloud execution.

At preflight, the machine had 10 logical CPUs, 24 GiB memory, and approximately
107 GiB free storage. The completed Task observations were:

| Task | Wrapper wall time | Maximum RSS | Principal admitted artifact |
|---|---:|---:|---|
| SCF | 1.951 s | 53,936,128 bytes | 32-file native state; tree SHA-256 `a020e7aa1ed38b2bdd259320ecbb7cc8f2770548c8eeab9e3ceb00369b6c18e7` |
| NSCF | 4.166 s | 41,844,736 bytes | 75-file native state; tree SHA-256 `775c85c0c323dfaf1c65054650d180c4482d5c2e4ecacd26f13274dc6cd6430f` |
| DOS | 5.801 s | 32,423,936 bytes | 82,588-byte `si_dos.dat`; SHA-256 `b967ed73c7d2572123dbf0b928630e38868ad2f9afbb1b3e77f140ecd53bf6df` |

The retained external Workflow contained 102,503,537 regular-file bytes before its
final compact Workflow record, within the 300 MB envelope.

## Reusable CPN Task realization

The enclosing reusable Workflow has three operation-specific CPN transitions:

```text
dft.scf -> dft.nscf -> dft.dos
```

Each transition selects one run-scoped Task instance. Each instance owns its exact
input, activation, attempt, execution grant, private workspace, process observation,
immutable result, failure boundary, result ingress, and CPN firing. The Workflow owns
the dependencies; no Task inspects the whole marking or invokes its successor.

The authorized run created one external Workflow root with portable run identity
`qe-7.5-silicon-dos-20260903T102922Z` under the ignored run area. It contains no
symbolic links and separates:

```text
<workflow-root>/
  scf-task/{work,pseudos,streams,snapshots,records,results}/
  nscf-task/{predecessor-state,work,pseudos,streams,snapshots,records,results}/
  dos-task/{predecessor-state,work,streams,snapshots,records,results}/
```

The **SCF Task** runs from `scf-task/work/`. Its private `tmp/` receives the native
`silicon.save` state. After confirmed result ingress, that state is frozen as an
identified immutable artifact tree; the mutable workspace is not exposed to another
Task.

The **NSCF Task** consumes the admitted SCF ResultObject and exact frozen-state
identity. Before invocation, it stages and verifies a copy at
`nscf-task/work/tmp/silicon.save`. Running from `nscf-task/work/` preserves the pinned
`outdir='./tmp/'` and `pseudo_dir='../pseudos/'` values without further editing the
exact adapted scientific-input bytes. Its returned ResultObject identifies a newly frozen post-NSCF native-state
tree.

The **DOS Task** consumes the admitted NSCF ResultObject and exact post-NSCF state
identity. It stages and verifies a copy at `dos-task/work/tmp/silicon.save`, runs only
`dos.x`, and returns a ResultObject identifying `si_dos.dat` and its mechanical process
record. It does not mutate the NSCF Task's workspace.

The three separately granted Task invocations were:

```text
# from scf-task/work/
pw.x < pw.scf.silicon_dos.in > ../streams/stdout 2> ../streams/stderr

# from nscf-task/work/
pw.x < pw.nscf.silicon_dos.in > ../streams/stdout 2> ../streams/stderr

# from dos-task/work/
dos.x < pp.dos.silicon.in > ../streams/stdout 2> ../streams/stderr
```

Each Task command has a separate timing and exit record and separate before/after
workspace snapshots. There was no automatic retry. During initial staging, successor
control identities were preallocated and their records were prematurely labeled as
activated and reserved. Before either successor process, those records were
deterministically corrected to planned/not-activated/not-reserved. NSCF and DOS were
then explicitly activated and granted only after their predecessor result ingresses;
no successor grant had been claimed and no successor process had run before the
correction.

The retained failure rule is unchanged: a nonzero exit, missing calculator completion
marker, calculator error, missing required continuation state, failed result ingress,
or identity mismatch produces no success token and prevents the dependent Task from
becoming enabled.

## Artifact and observations

Each Task inventory records relative paths, byte counts, modification times, and
SHA-256 for regular files. Before each downstream invocation, the Workflow verified
both an immutable predecessor-state copy and the separate staged work copy against the
admitted predecessor tree identity. The predecessor copies remained unchanged after
the downstream processes.

1. **SCF Task:** QE reported convergence in six iterations, 29 irreducible k-points,
   8 Kohn--Sham states, total energy `-15.85328336` Ry, and printed occupied/unoccupied
   levels of 6.2071 and 6.7525 eV. These are calculator observations, not a convergence
   study or accepted physical result.
2. **NSCF Task:** QE reported 72 irreducible k-points with the tetrahedron method and
   8 Kohn--Sham states. The exact input retained the pinned omission of `nosym`. The
   admitted post-NSCF state identity is the one in the resource table above.
3. **DOS Task:** QE reported `Tetrahedra used`. The admitted `si_dos.dat` has one
   header and 2,501 finite three-column data rows from −9 to 16 eV with a uniform
   0.01 eV step. Its header reports a Fermi energy of 6.642 eV; the final integrated
   DOS column is 16.0. These values are parsed observations, not independent
   scientific validation.

The SCF and NSCF stderr streams each retained the same reported IEEE invalid,
divide-by-zero, overflow, and underflow flags. The DOS stderr retained an IEEE overflow
flag. Their cause and scientific significance remain uncharacterized.

The compact repository observation is
`examples/tutorials/silicon-dos/qe/expected/qe75-calculated-observation.json`. Full
scratch trees, wavefunctions, charge densities, streams, snapshots, and the DOS file
remain in the identified external run.

## Claim boundary and disposition

The completed run is one **calculated tutorial observation** of QE 7.5 continuation
and DOS artifact behavior for the exact authorized inputs. It does not establish
production convergence, pseudopotential suitability, an accepted project silicon
geometry, a project reference DOS, numerical verification, scientific validation,
uncertainty quantification, QE--ABINIT equivalence, or a complete many-body excitation
spectrum.

Software-verification evidence
`SV-DFT-SCF-NSCF-DOS-CPN-001`--`SV-DFT-SCF-NSCF-DOS-CPN-004` covers only the
private reusable Task identities and effect-free CPN composition;
`SV-DFT-NSCF-DOS-001`--`SV-DFT-NSCF-DOS-006` covers private QE operation records.
The identified external process and artifact records, rather than those synthetic
software tests, ground the calculator-behavior observations above. No additional
execution or retry is authorized.
