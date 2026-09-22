# IEEE Warning Class-Separated Non-MPI C48 Classification

**Status:** The authorized sequential class-separated diagnosis stopped after its first
invocation because the divide-by-zero-only run reproduced the exact retained OpenBLAS
trap. The matching first later trap is therefore classified as an IEEE divide-by-zero
exception. Invalid-only and overflow-only builds and invocations were not created.
This is diagnostic software evidence, not a completed SCF calculation, calculated
physical result, numerical verification, scientific validation, or harmlessness
determination.

## Authorization and stopping rule

Human response `recommendation authorized` unambiguously selected
`authorize_sequential_class_separated_nonmpi_c48_classification` in
`.pi/checkpoints/bulk-silicon-convergence-ieee-class-separated-execution.json`.
The authorized order was:

1. divide-by-zero only;
2. invalid only, if and only if the first run did not reproduce the exact prior trap;
3. overflow only, if and only if neither earlier run reproduced it.

An exact match required OpenBLAS `ztrsv_CUN+388` and AArch64 instruction word
`0x1e611802`. The sequence was required to stop at its first exact match.

## Exact build and invocation

The operation used the unchanged source snapshot at `~/projects/q-e-qe-7.2` to create
only:

`~/projects/q-e-diagnostics/qe-7.2-ieee-openblas-nonmpi-zero-20260921T010351Z/build`

The build used CMake `Debug`, Apple Clang 17.0.0, GNU Fortran 16.1.0, MPI off,
OpenMP off, ScaLAPACK off, external FFTW, and pinned OpenBLAS 0.3.33 for BLAS and
LAPACK. Its exact GNU Fortran debug flags were:

```text
-O0 -g -fbacktrace -ffpe-trap=zero
```

No invalid, overflow, or underflow trap was enabled. The executable identities were:

- divide-by-zero-only `pw.x` SHA-256:
  `ed27d31eb86fb3f931ef320d271a4ac1f1026d5cb53ffe07784581d3d70659ca`;
- `pw.x` size: 14,917,624 bytes; and
- OpenBLAS SHA-256:
  `dbd757cdfffbff1dc72fbf34983e89d5710933d04783f950441a57522fbf769d`.

`otool -L` confirmed OpenBLAS linkage and the absence of MPI and Apple Accelerate
linkage. The exact retained inputs were:

- C48 input SHA-256:
  `cadb2a3024f39858f91b23bd1c1c22e2b2d0f161f2960c39ea1abf48cf00ee17`;
  and
- Si pseudopotential SHA-256:
  `39822757f53f36e3bf3bfb779356152a8d3f21199c7db9dd5a931e5d18c45282`.

The single invocation used `OMP_NUM_THREADS=1` and a 120-second limit. It began at
`2026-09-21T01:38:10.698921Z` and ended at `2026-09-21T01:38:11.526358Z` without
reaching the timeout.

Observed state:

- QE mode: `Serial version`;
- termination: `SIGILL` (`EXC_BAD_INSTRUCTION`);
- wrapper return code: `-4`;
- first SCF iteration: not reached;
- `JOB DONE.`: absent;
- scratch regular files: zero;
- maximum resident set size: 29,671,424 bytes;
- peak memory footprint: 21,643,720 bytes; and
- external run-tree size after capture: 280 KiB.

## Exact match and classification

The macOS crash report retained:

```text
OpenBLAS ztrsv_CUN+388
  -> OpenBLAS ztrsv_+416
  -> OpenBLAS zhegs2_+1828
  -> OpenBLAS zhegst_+1164
  -> OpenBLAS zhegvx_+960
  -> QE LAXlib cdiaghg
  -> QE rotate_wfc_k / rotate_wfc
  -> QE init_wfc / wfcinit
```

The exception code again contains AArch64 instruction word `0x1e611802`, decoded as:

```text
fdiv d2, d0, d1
```

The OpenBLAS image UUID, five OpenBLAS image offsets, symbol locations, faulting
instruction word, QE logical call chain, and pre-SCF stage exactly match the combined-
trap non-MPI comparator. Because the only enabled trap class was
`-ffpe-trap=zero`, this exact matching first operation is classified as an IEEE
divide-by-zero exception.

The stopping rule was therefore satisfied after sequence position one. No invalid-only
or overflow-only build root or run root was created, and no such invocation occurred.
There was no retry.

## Interpretation and claim boundary

The evidence now distinguishes two sources encountered by the combined-trap build:

1. an external MPI/hwloc/OpenCL startup trap in Apple's AGX stack; and
2. a later divide-by-zero exception in the BLAS/LAPACK path below `ZHEGVX` during QE
   initial-wavefunction subspace diagonalization.

The second source is invariant across Apple Accelerate and OpenBLAS and, within
OpenBLAS, across singleton-MPI and true non-MPI builds. MPI initialization and one
specific BLAS provider are therefore not necessary causes of the matching later
operation.

This classification does not retain the numerator or denominator, explain why the
division occurs, establish whether its result is subsequently used, or prove that the
ordinary masked/non-trapping computation is unaffected. It does not establish that
invalid, overflow, or underflow never occur later in an ordinary complete run. The
retained production summary includes all four flags, and underflow was outside every
trapping build in this sequence.

No warning suppression, OpenBLAS production adoption, provisional-setting promotion,
downstream eligibility, or scientific acceptance follows. The selected convergence
disposition and downstream production work remain blocked pending observable-effect
and remaining-warning disposition.

## Retained identities

The external `manifest.json` has SHA-256
`f053319e67a6f20fb3192a69e5be0af05ee4f69f03c373f2982c2a78eaf0567e`.
Principal retained artifacts are:

| Artifact | SHA-256 | Bytes |
|---|---|---:|
| `output/C48.scf.out` | `396d4008666c9374a7960d7662df3f967e697e1757fa6c30ca26624f63bb60de` | 8,393 |
| `output/C48.scf.err` | `4d11bc9a04c574f64b04a208fce3da041b78f4431918ce694dc8a1933bae79bd` | 942 |
| `output/time.txt` | `b14a0374e3e2a49c8d5d2f81db0301e87c9c109323d460d7000ee693325044be` | 67 |
| `output/process-result.json` | `22db94a3e1d6023d54799ff1753c2588142b5336d1bc81be5f066581829767cc` | 655 |
| `output/executable-linkage.txt` | `9a1320a27cf72e1f048c6f1bbff9d0cfe4c131f62f9b6cc576bab2f3d8dd4537` | 619 |
| `output/preflight-identities.txt` | `c702fee806897842965f23479c0d98fed93082a6b782a1e9cd53099a2ac4cd85` | 646 |
| `output/pw-crash-report.ips` | `aa3c10df3af9141e6de17333749799c2190bec4e691e067dbb3270ac61cb2626` | 8,978 |
| `output/symbolized-backtrace.txt` | `a9d2eeffdd2def8488a7212cd4446ad5287c4b0ea53fb9a603cf07dde6fb77e9` | 1,078 |
