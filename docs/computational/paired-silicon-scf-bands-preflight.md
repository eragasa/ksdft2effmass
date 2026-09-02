# Paired silicon SCF-and-bands tutorial preflight

## Status and exact shared objective

This is a **proposed same-simulation tutorial pair**, not a calculated result. Both
backends will run the same computational objective:

1. construct a self-consistent Kohn--Sham density for two-atom diamond silicon;
2. preserve that density as calculator-native continuation state;
3. evaluate eight Kohn--Sham bands at fixed density along an
   L–$\Gamma$–X–$\Gamma$ path; and
4. extract the path coordinates, eigenvalues, completion state, diagnostics, and
   native continuation relationships.

This corrects the rejected pairing of QE silicon bands with an ABINIT H$_2$ distance
scan. The replacement pair is intended to expose backend-specific realizations of one
workflow before any generic software contract is extracted. Execution awaits
checkpoint `PAIRED-SILICON-BANDS-RUN-HC01`.

“Same simulation” here means the same material, primitive-cell role, SCF-to-fixed-density
bands workflow, path topology, requested band count, and extracted observable. It does
not mean numerical equivalence: the native tutorials use different pseudopotential
artifacts, LDA parameterizations, cutoffs, lattice constants, path discretizations,
and convergence semantics. These differences are retained explicitly rather than
silently changing either upstream tutorial. No energy or band value will be compared
across backends.

## Shared and backend-specific contract

| Concern | Quantum ESPRESSO 7.5 | ABINIT 10.8.3 |
|---|---|---|
| System | Two-atom diamond-Si primitive cell | Two-atom diamond-Si primitive cell |
| Workflow | `pw.x` SCF → `pw.x` bands → `bands.x` | One `abinit` invocation with SCF dataset 1 → fixed-density bands dataset 2 |
| Continuation | Run-local `si.save` density/state | `prtden1=1`, then `getden2=-1` |
| Path | L–$\Gamma$–X–$\Gamma$, 72 expanded points in the legacy reference | L–$\Gamma$–X–$\Gamma$, 39 points |
| Bands | 8 | 8 |
| Lattice scale | 10.20 Bohr | 10.195 Bohr |
| Plane-wave cutoff | 18 Ry = 9 Hartree | 12 Hartree = 24 Ry |
| SCF sampling | 10 explicit weighted wavevectors | 4×4×4 grid with four shifts, reduced to 10 wavevectors |
| Pseudopotential | Legacy QE NC, nonrelativistic PZ-LDA UPF | PseudoDojo NC-SR v0.4 standard PW-LDA PSP8 |
| SCF stopping | `conv_thr=1.0e-8` Ry | `toldfe1=1.0e-6` Hartree |
| Band stopping | Native `pw.x` bands behavior | `tolwfr2=1.0e-12` |

The pair supports workflow-shape comparison only. In particular, Kohn--Sham
eigenvalues are not identified with the complete excitation spectrum, and neither
result becomes a production or effective-mass reference.

## Quantum ESPRESSO exact candidate

The QE side is derived from official QE 7.5
`PP/examples/example01/run_example` at source commit
`770a0b2d12928a67048e2f3da8d10d057e52179e`. The source script has SHA-256
`b261e29a0408cd97162f23f3cf9cb5eb865ce4005dae3a871164a15256b7c598`.
Only deployment paths were adapted to the isolated runtime layout.

| Item | Identity |
|---|---|
| `pw.x` | SHA-256 `87aa72158e2c103c63fce1deca977dc42ff4ba344519a9662aadb96d33eab910` |
| `bands.x` | SHA-256 `fef09fe9d9967dd432859fc6affc8f28c2acaedefc78f16409897f273488b443` |
| SCF input | SHA-256 `2cb575a14c361153623dd855b9cab526c448d63f339e9c18bc120b273416b9be` |
| Bands input | SHA-256 `811404a76486d52c86a4ddf4d782525d64adb53f83af392965c0897c8689cd04` |
| `bands.x` input | SHA-256 `c2ba35c8b003cfc5d61391fc2bc04d2525725dd7e7842cfe3fde0510c880ac8c` |
| `Si.pz-vbc.UPF` | 74,552 bytes; SHA-256 `e8d933754cd51c6bb4b2a809151f89e0647e53d878bab88d26e1b5a5d68d5217` |

The UPF is the already retained historical QE tutorial artifact. Its available
metadata identifies a norm-conserving, nonrelativistic Perdew--Zunger LDA form but no
file-specific author, generation version, or license. The proposed run neither
reacquires nor redistributes it and does not select it for production use.

The three direct one-process stages run sequentially. Failure of SCF blocks bands;
failure of bands blocks `bands.x`. Expected outputs include separate stream, timing,
and exit records for every stage, QEXSD, charge density, wavefunctions,
`sibands.dat`, and `sibands.dat.rap`. Postprocessing will use the existing exact QEXSD
version boundary and parse ordered path/eigenvalue and symmetry-label content.
Interactive `plotband.x` and plotting are excluded.

## ABINIT exact candidate

The ABINIT side is the byte-identical official 10.8.3
`tests/tutorial/Input/tbase3_5.abi` input. It contains two datasets and therefore keeps
its native SCF-to-bands dependency inside one process invocation.

| Item | Identity |
|---|---|
| `abinit` | SHA-256 `0f5b2ddc46a166271a5a61a0d618974cc8db1b3dfb7dbe13ebf4b04396b54e82` |
| `tbase3_5.abi` | SHA-256 `a6090f4af1b57e7c3801bed1ff0bda8f944a4f1f928d7c24a1541917671a8fb6` |
| PseudoDojo `Si.psp8` | 280,042 bytes; SHA-256 `fd82ea59b952bec14d40a201e52eb39ae66ef3fa885e0fb9fef7fd2cc8209966` |

The input is staged but not copied into this repository because it has no
file-specific license notice. The PseudoDojo artifact is attributed under CC BY 4.0
and remains external.

Expected outputs include separate stdout, stderr, timing, and exit records; the main
`.abo`; dataset-specific GSR/EIG/OUT NetCDF content; density and wavefunction state;
and the derivative database. Postprocessing will extract both dataset outcomes, the
`getden2=-1` continuation event, SCF and band convergence reports, all 39 path points
and eight eigenvalues per point, and diagnostics. The upstream ABINIT 10.5.8.2
reference reports 2.9 seconds wall time, less than 6.3 MB estimated calculation memory,
and two warnings; these are expectations to inspect, not acceptance thresholds.

## Scale, workspaces, and claim boundary

Dry-run staging created two new external run roots:

- `qe-7.5-silicon-scf-bands-paired-20260902T065631Z`; and
- `abinit-10.8.3-silicon-scf-bands-paired-20260902T065631Z`.

They are outside the repository, contain no symbolic links, and separate inputs,
pseudopotentials, work state, streams, results, and records. No scientific executable,
network access, remote resource, cluster, cloud service, or scheduler was used during
staging.

Each executable will use one local process and one OpenMP thread. Conservative limits
are one minute per invocation, 250 MB resident memory per process, and 25 MB new
storage per backend. About 119 GiB was available at preflight.

If authorized, the exact staged invocations run once without automatic retry or
scientific-setting changes. Native QEXSD, NetCDF, density, wavefunction, derivative,
band, and stream files remain external. Maintained records will distinguish:

- preprocessing readiness;
- process completion;
- calculator-reported SCF or band convergence;
- native continuation success;
- useful output extraction; and
- unsupported or warning-bearing outputs.

This pair may inform a later generic workflow contract, but it does not authorize that
contract to erase backend-specific semantics. Successful runs will be tutorial
calculated observations, not production convergence, numerical verification,
scientific validation, uncertainty quantification, cross-backend agreement, or human
acceptance.
