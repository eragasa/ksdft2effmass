# First paired QE and ABINIT tutorial batch preflight

## Status and purpose

This is a **rejected protected-execution batch**, not a calculated result. Checkpoint
`QE-ABINIT-TUTORIAL-BATCH01-HC01` resolved as option B after the human required both
calculators to run the same simulation before generic behavior is extracted. No
scientific executable was invoked. The rejected candidates had been chosen as:

1. a three-stage Quantum ESPRESSO silicon SCF → bands → `bands.x` flow; and
2. the ABINIT basic1 stage-2 21-dataset H$_2$ bond-distance scan.

The candidates would have exposed inter-executable continuation and postprocessing on
the QE side and within-invocation dataset chaining on the ABINIT side. Because they do
not represent the same physical system, their external staging is retained but must
not be executed. The replacement same-simulation candidate is documented in the
[paired silicon SCF-and-bands preflight](paired-silicon-scf-bands-preflight.md).

## Quantum ESPRESSO candidate

### Sources and exact identities

The candidate is derived from the official QE 7.5
`PP/examples/example01/run_example` at source commit
`770a0b2d12928a67048e2f3da8d10d057e52179e`. Its source-script SHA-256 is
`b261e29a0408cd97162f23f3cf9cb5eb865ce4005dae3a871164a15256b7c598`.
Only deployment paths were adapted to the isolated runtime layout.

| Item | Identity |
|---|---|
| `pw.x` 7.5 | SHA-256 `87aa72158e2c103c63fce1deca977dc42ff4ba344519a9662aadb96d33eab910` |
| `bands.x` 7.5 | SHA-256 `fef09fe9d9967dd432859fc6affc8f28c2acaedefc78f16409897f273488b443` |
| Staged SCF input | SHA-256 `2cb575a14c361153623dd855b9cab526c448d63f339e9c18bc120b273416b9be` |
| Staged bands input | SHA-256 `811404a76486d52c86a4ddf4d782525d64adb53f83af392965c0897c8689cd04` |
| Staged `bands.x` input | SHA-256 `c2ba35c8b003cfc5d61391fc2bc04d2525725dd7e7842cfe3fde0510c880ac8c` |
| `Si.pz-vbc.UPF` | 74,552 bytes; SHA-256 `e8d933754cd51c6bb4b2a809151f89e0647e53d878bab88d26e1b5a5d68d5217` |

The pseudopotential is the already retained historical QE example artifact: UPF 2.0.1,
norm-conserving, nonrelativistic Perdew--Zunger LDA. Its available metadata does not
identify an author, generation version, or file-specific license. The proposed local
run neither reacquires nor redistributes it and does not select it for production use.

### Scientific and computational scale

The unchanged tutorial settings use two silicon atoms in the diamond primitive cell,
`celldm(1)=10.20` Bohr, an 18 Ry wavefunction cutoff, ten weighted SCF wavevectors,
and `conv_thr=1.0e-8`. The bands stage requests eight Kohn--Sham bands along the
source's five `tpiba_b` path vertices; the legacy reference expands this to 72 path
points. `bands.x` writes symmetry-labeled plain-text band data with `lsym=.true.`.
Interactive `plotband.x` and all plotting are excluded.

The stages run sequentially with direct one-process invocations. The bands stage
consumes the fresh SCF density through the shared run-local `si.save`; `bands.x`
consumes that completed bands state. A failed stage stops its dependents. Based on the
QE reference outputs and the earlier QE 7.5 SCF smoke test, the batch is expected to
finish in seconds; the conservative limit is one minute per stage, 250 MB resident
memory per process, and 25 MB total new storage.

Expected useful outputs include per-stage stdout/stderr/timing/exit records, QEXSD
`data-file-schema.xml`, charge density, path wavefunctions, `sibands.dat`, and
`sibands.dat.rap`. Postprocessing will extract SCF completion and energy, ordered path
coordinates and eigenvalues, band/symmetry records, warnings, and stage dependencies.
QEXSD will be parsed under the existing exact version contract. Native density and
wavefunction state remains external.

## ABINIT candidate

### Sources and exact identities

The candidate is the byte-identical official ABINIT 10.8.3
`tests/tutorial/Input/tbase1_2.abi` input. It uses the same bundled PseudoDojo hydrogen
PSP8 as the completed stage-1 run.

| Item | Identity |
|---|---|
| ABINIT 10.8.3 | SHA-256 `0f5b2ddc46a166271a5a61a0d618974cc8db1b3dfb7dbe13ebf4b04396b54e82` |
| `tbase1_2.abi` | SHA-256 `a9fddbcc1f704cc1b87014518ff908665ea45f8201c6f5407585593f44afb437` |
| PseudoDojo `H.psp8` | 75,139 bytes; SHA-256 `af415463efe6cbd281cad1b3fda928016408ec401b0f2c671275fa8f19594983` |

The tutorial input remains external because it has no file-specific license notice.
The PseudoDojo artifact is attributed under CC BY 4.0 and is not committed.

### Scientific and computational scale

One direct serial ABINIT invocation contains 21 datasets. The H$_2$ half-separation
starts at 0.5 Bohr and increases by 0.025 Bohr per dataset, so the bond distance spans
1.0 through 2.0 Bohr. Every dataset uses one occupied band, a 10 Hartree cutoff,
Gamma-only sampling, at most ten SCF steps, and `toldfe=1.0e-6` Hartree. `getwfk=-1`
requests each dataset's starting wavefunction from its immediate predecessor.

The upstream ABINIT 10.5.8.2 reference completed in 3.8 seconds, estimated less than
8.7 MB calculation memory per dataset, and reported completion for all 21 datasets.
It also reported 120 warnings, which are an expectation requiring inspection rather
than an accepted error threshold. The proposed conservative limit is one minute,
150 MB resident memory, and 25 MB new storage.

Expected outputs include the main `.abo` and stdout log, per-dataset GSR/EIG/OUT
NetCDF content, density and wavefunction state, derivative databases, and the internal
wavefunction continuation chain. Postprocessing will extract all 21 bond distances,
energies, forces, convergence reports, diagnostics, and NetCDF cross-output content;
it will locate the minimum only as an observed discrete tutorial-scan value, not as a
validated equilibrium geometry.

## Isolated workspaces and execution boundary

Dry-run staging created two new external roots identified by:

- `qe-7.5-silicon-bands-tutorial-20260902T064837Z`; and
- `abinit-10.8.3-basic1-stage2-20260902T064837Z`.

Both roots are outside the repository, contain no symbolic links, and have separate
input, pseudopotential, work, stream, result, and record roles. About 119 GiB was
available before execution. No remote, cluster, cloud, scheduler, network, or
scientific executable was used during staging.

If option A is authorized, each exact invocation runs once with no automatic retry and
no scientific-setting change. Raw streams, QEXSD, NetCDF, density, wavefunction,
derivative, and band files remain external. The repository may retain only compact
calculated observations, useful scripts, and architecture findings under the existing
tutorial commit boundary.

Successful process exits or input-specific convergence reports will establish only
observed tutorial execution. They will not establish production convergence, numerical
verification, scientific validation, uncertainty quantification, aligned QE--ABINIT
physics, or acceptance.
