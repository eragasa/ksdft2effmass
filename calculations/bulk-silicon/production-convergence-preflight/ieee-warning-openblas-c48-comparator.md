# IEEE Warning OpenBLAS C48 Comparator

**Status:** One authorized calculated diagnostic execution completed exactly once.
The OpenBLAS-linked comparator reproduced the later enabled floating-point trap in
the same QE generalized-eigenproblem path without linking Apple Accelerate. This is
diagnostic software evidence, not a completed SCF calculation, calculated physical
result, numerical verification, scientific validation, or harmlessness determination.

## Authorization and exact operation

Human response `authorized` unambiguously selected
`authorize_one_openblas_instrumented_c48_comparator` in
`.pi/checkpoints/bulk-silicon-convergence-ieee-openblas-comparator-execution.json`.
The operation used the unchanged source snapshot at `~/projects/q-e-qe-7.2` to create
only the isolated build
`~/projects/q-e-diagnostics/qe-7.2-ieee-openblas-20260921T001226Z/build`.

The build used:

- CMake `Debug` configuration;
- `/opt/homebrew/bin/mpicc` and `/opt/homebrew/bin/mpif90`;
- GNU Fortran flags `-O0 -g -fbacktrace -ffpe-trap=invalid,zero,overflow`;
- MPI enabled, OpenMP disabled, and ScaLAPACK disabled;
- external FFTW; and
- OpenBLAS 0.3.33 for both BLAS and LAPACK.

The CMake policy compatibility setting `CMAKE_POLICY_VERSION_MINIMUM=3.5` allowed the
unchanged bundled MBD source to configure with CMake 4.3.3. No source bytes were
modified. Only target `qe_pw_exe` was requested, with at most eight local jobs. The
external build tree occupied 101 MiB, below the authorized resource envelopes.

The exact identities were:

- diagnostic `pw.x` SHA-256:
  `4fe641535285a9bde81bb0b55862ccfd8bd072d354a57585ff6ded545cc13565`;
- diagnostic `pw.x` size: 15,857,256 bytes;
- OpenBLAS library SHA-256:
  `dbd757cdfffbff1dc72fbf34983e89d5710933d04783f950441a57522fbf769d`;
- C48 input SHA-256:
  `cadb2a3024f39858f91b23bd1c1c22e2b2d0f161f2960c39ea1abf48cf00ee17`;
  and
- Si pseudopotential SHA-256:
  `39822757f53f36e3bf3bfb779356152a8d3f21199c7db9dd5a931e5d18c45282`.

`otool -L` confirmed that `pw.x` resolves BLAS/LAPACK through
`/opt/homebrew/opt/openblas/lib/libopenblas.0.dylib`, whose real path is the pinned
library above. Apple Accelerate is absent from the executable's retained dynamic
linkage. OpenBLAS was neither installed nor upgraded by this operation and is not
adopted as a project or production dependency.

The comparator used `HWLOC_COMPONENTS=-opencl`, `OMP_NUM_THREADS=1`, one singleton
MPI process, and a 120-second wall-time limit. No retry, second comparator invocation,
setting promotion, successor activation, network access, or remote, cluster, or cloud
resource was used.

## Process result

The run root is
`~/projects/ksdft2effmass-runs/bulk-silicon-ieee-openblas-comparator-20260921T001226Z`.
The invocation began at `2026-09-21T00:26:37.735184Z` and ended at
`2026-09-21T00:26:38.674837Z` without reaching the timeout.

Observed state:

- termination: `SIGILL` (`EXC_BAD_INSTRUCTION`);
- wrapper return code: `-4`, because `/usr/bin/time` re-raised the child signal;
- QE banner and exact input: read successfully;
- first SCF iteration: not reached;
- `JOB DONE.`: absent;
- scratch regular files: zero;
- maximum resident set size: 42,008,576 bytes;
- peak memory footprint: 25,412,064 bytes; and
- external run-tree size after capture: 284 KiB.

Stdout ends after pseudopotential, symmetry, k-point, and dense-grid initialization.
It contains no total energy, SCF residual, pressure, force, or other completed physical
observable.

## Symbolized trap

The macOS crash report localizes the triggered thread to:

```text
OpenBLAS ztrsv_CUN+388
  -> OpenBLAS ztrsv_+416
  -> OpenBLAS zhegs2_+1828
  -> OpenBLAS zhegst_+1164
  -> OpenBLAS zhegvx_+960
  -> QE LAXlib cdiaghg
  -> QE KS_Solvers/DENSE rotate_wfc_k
  -> QE PW rotate_wfc
  -> QE init_wfc / wfcinit
  -> QE init_run / run_pwscf / pwscf
```

As in the Apple Accelerate run, the QE call site is `LAXlib/cdiaghg.f90:143`, where
QE calls `ZHEGVX` to compute the lowest generalized Hermitian eigenpairs while
rotating the initial atomic-wavefunction subspace. The crash occurred before the
first SCF iteration.

The exception code contains AArch64 instruction word `0x1e611802`. Its scalar
floating-point register fields and opcode decode as:

```text
fdiv d2, d0, d1
```

The OpenBLAS and Apple Accelerate comparators therefore both first trap on a
floating-point division below `ZHEGVX`, although their internal triangular-reduction
implementations and destination/source registers differ. Because invalid,
divide-by-zero, and overflow traps were enabled together, an `fdiv` still does not
establish which one of those IEEE classes fired. Underflow was not trapped.

## Comparator interpretation and claim boundary

This result refutes the narrow hypothesis that the later trap is specific to Apple
Accelerate. Replacing Apple Accelerate with the pinned OpenBLAS implementation did
not eliminate it: both implementations reach the same QE generalized subspace
eigenproblem and terminate on an enabled floating-point division before SCF.

The result does not establish that OpenBLAS and Apple Accelerate execute identical
intermediate arithmetic, that the same IEEE class fired, or that the underlying
operands have the same values. Neither run retained the faulting floating-point
operands or the floating-point status register. The result therefore does not decide
whether the operation is a benign implementation intermediate, a singular or
ill-conditioned overlap-matrix intermediate, or a mathematically material division.
It also does not establish whether ordinary non-trapping final observables are
affected.

No warning suppression, OpenBLAS production adoption, provisional-setting promotion,
downstream eligibility, or scientific acceptance follows. The selected convergence
disposition and downstream production work remain blocked. A separately authorized
debugger-controlled invocation could retain the first faulting operands and status
register without changing the scientific input, but that protected execution is
outside this authorization.

## Retained identities

The external `manifest.json` has SHA-256
`119a93f75a77386b2cf26a60aed021f07d3b71e49e2d50772a2ffbadbeb8beae` and binds the
run artifacts, exact linkage, and environment. Principal identities are:

| Artifact | SHA-256 | Bytes |
|---|---|---:|
| `output/C48.scf.out` | `9aa7513b06f2f04471ae067e0613361f27362fda27733b99a6411f0922dab2cc` | 8,594 |
| `output/C48.scf.err` | `776877ac3c43aba95f15d79fd228c58f453625f127b595e1d10e3c17bbf3c1f7` | 1,007 |
| `output/time.txt` | `c5cdd1a7191788f07b5f377f673fa3fdedb19d8e14a54e14532cfa210fe810e1` | 67 |
| `output/process-result.json` | `aaef33353b6dece1022066a717de2bee5b75e748abcd840f328dd86df9f33377` | 597 |
| `output/executable-linkage.txt` | `b11de131d78c74824525e09f4cb09a94383db04e5cc92300d55a75baea2028b5` | 1,053 |
| `output/preflight-identities.txt` | `92277d83c7aa355bc2ac1b85fe1093e5beb185535fbbfe0b7314ae1d1efbbb8a` | 632 |
| `output/pw-crash-report.ips` | `4e836d0d18671eaea825f272e9da3553ec8b404aa66273a8ee4d9f67da14e0dd` | 13,342 |
| `output/symbolized-backtrace.txt` | `0e0a1402d6ac82997e529ac89fe337aba7337fe6d7cb6d45bf7c3fd54e26068b` | 988 |
