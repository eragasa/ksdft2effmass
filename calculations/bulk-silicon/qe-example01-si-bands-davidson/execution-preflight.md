# QE example01 silicon Davidson bands execution preflight

**Status:** Complete and awaiting explicit execution authorization. Quantum
ESPRESSO has not been invoked.

## Candidate

This candidate evaluates the fixed converged Kohn–Sham operator

$$
\hat H_{\mathrm{KS}}[n_{\mathrm{SCF}}]
\psi_{n\mathbf k}
=
\epsilon_{n\mathbf k}\psi_{n\mathbf k},
\qquad
\mathbf k\in\mathcal K_{\mathrm{tutorial}}.
$$

It is the QE 7.2 bundled `PW/examples/example01` silicon Davidson bands stage:
`calculation='bands'`, `prefix='silicon'`, `nbnd=8`, and 28 ordered bare
`K_POINTS` in QE's default `tpiba` convention. The delta, sigma, and lambda
names are tutorial descriptions. This preflight does not establish a canonical
modern silicon high-symmetry path. Eight bands are a tutorial setting, not a
production band-window decision. This is not an effective-mass, Wannier, or
tight-binding dataset.

## Identities

- Input: `si.band.david.in`, 1,071 bytes, SHA-256
  `f071479456e5ec6a272f86033045967659c757c6080c11dbf85ea74de85496ab`.
  The repository and execution copies are byte-identical. Only `pseudo_dir` and
  `outdir` were expanded to isolated absolute paths; all scientific values equal
  the pinned QE 7.2 example here-document.
- Executable: `/Users/eugene/projects/q-e-qe-7.2/build/bin/pw.x`, 9,889,576
  bytes, SHA-256
  `6e8720e74cbafa7c7f07ee61ec6f5944c15d59bffa8ee8423fae14364f21c8ca`,
  mode `0755`. It was not executed or probed. The accepted SCF provenance
  identifies it as QE PWSCF 7.2, Mach-O arm64, MPI build.
- Pseudopotential: `Si.pz-vbc.UPF`, 74,552 bytes, SHA-256
  `e8d933754cd51c6bb4b2a809151f89e0647e53d878bab88d26e1b5a5d68d5217`.
  Source and execution copy agree exactly with the previously accepted UPF
  2.0.1 silicon norm-conserving, nonrelativistic Perdew–Zunger LDA artifact.
- Comparison target: bundled `reference/si.band.david.out`, 12,117 bytes,
  SHA-256
  `6e9ef8559ac533882684bdded6c04d874131aa0a2e782565d64cb573178a5c34`.
  It is a legacy PWSCF 6.0 observational tutorial target. No numerical
  comparison tolerance has been accepted.

## Isolated restart state

The accepted source is the read-only authority at
`/Users/eugene/projects/q-e-qe-7.2/tempdir/silicon.save`. Before and after the
copy it contained 13 regular files totaling 467,988 bytes, one directory, and
no symbolic links. The complete pre-copy and post-copy manifests agree exactly.

The disposable copy contains only the three restart files required by this QE
7.2 bands mode: `charge-density.dat`, `data-file-schema.xml`, and
`Si.pz-vbc.UPF`. They total 206,260 bytes and agree with their accepted-source
paths in size and SHA-256. The ten accepted SCF `wfc*.dat` files were not copied:
the tutorial does not set `startingwfc='file'`; the bundled reference reports
eight randomized atomic starting wavefunctions on the new path.

QE bands mode forces `startingpot='file'`, reads the copied accepted charge
density, and recalculates the fixed Kohn–Sham potential from it. It does not
read a separately stored potential or consume the accepted SCF wavefunctions.
An authorized run is expected to rewrite run-local QEXSD metadata and create
run-local path wavefunctions. The accepted source remains outside the run root
and must not be modified.

Complete accepted and copied manifests, including every directory, regular file,
and symbolic-link check, are embedded in `execution-preflight.json`.

## Workspace and scale

The isolated external root is
`/Users/eugene/projects/ksdft2effmass-runs/qe-example01-si-bands-davidson-20260812T223246Z`.
It is outside both the repository and accepted SCF scratch tree. No repository
control database, SQLite WAL/SHM/journal, staging, backup, or unrelated database
artifact is present. Expected runtime is seconds and conservatively less than
one minute on the previously identified local arm64 host. Expected additional
storage is in the low-megabyte range; reserve 10 MiB.

## Proposed command — not executed

```sh
cd -- '/Users/eugene/projects/ksdft2effmass-runs/qe-example01-si-bands-davidson-20260812T223246Z' && '/Users/eugene/projects/q-e-qe-7.2/build/bin/pw.x' < '/Users/eugene/projects/ksdft2effmass-runs/qe-example01-si-bands-davidson-20260812T223246Z/input/si.band.david.in' > '/Users/eugene/projects/ksdft2effmass-runs/qe-example01-si-bands-davidson-20260812T223246Z/output/si.band.david.out' 2> '/Users/eugene/projects/ksdft2effmass-runs/qe-example01-si-bands-davidson-20260812T223246Z/output/si.band.david.err'
```

The command uses one process, absolute paths, the explicit isolated working
directory, separate stdout and stderr, and requires no network access. Do not
run the bundled `run_example`; it reruns SCF and deletes `silicon*` scratch.

## Review finding

Independent planning-diff review found one deterministic stale count in the
bootstrap page: the new Task made ten linked Tasks and nine main-path Tasks.
That prose was corrected from nine/eight to ten/nine. Consolidated preflight
review then passed with no remaining material finding.

## Claim limits and decision

The preflight establishes identity, isolation, copy agreement, and execution
readiness only. It does not establish production convergence, a production
pseudopotential or path, numerical verification, scientific validation,
uncertainty quantification, or suitability for effective-mass, Wannier, or
tight-binding use. The accepted SCF IEEE warning remains observed and
unresolved; recurrence requires diagnosis rather than an assumption that it is
harmless or fatal.

Choose exactly one:

- **A — Execute exactly the prepared one-process tutorial bands command.**
- **B — Revise the input, workspace, or execution boundary.**
- **C — Defer execution.**
