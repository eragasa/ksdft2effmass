# IEEE Warning OpenBLAS Non-MPI C48 Comparator

**Status:** One authorized calculated diagnostic execution completed exactly once.
The true MPI-off/OpenBLAS comparator reproduced the same later enabled
floating-point trap below `ZHEGVX`. This is diagnostic software evidence, not a
completed SCF calculation, calculated physical result, numerical verification,
scientific validation, or harmlessness determination.

## Authorization and exact operation

Human response `recommendation authorized` unambiguously selected
`authorize_one_nonmpi_openblas_c48_comparator` in
`.pi/checkpoints/bulk-silicon-convergence-ieee-nonmpi-comparator-execution.json`.
The operation used the unchanged source snapshot at `~/projects/q-e-qe-7.2` to create
only the isolated build
`~/projects/q-e-diagnostics/qe-7.2-ieee-openblas-nonmpi-20260921T005103Z/build`.

The build used:

- CMake `Debug` configuration;
- Apple Clang 17.0.0 and GNU Fortran 16.1.0;
- GNU Fortran flags `-O0 -g -fbacktrace -ffpe-trap=invalid,zero,overflow`;
- MPI disabled, OpenMP disabled, and ScaLAPACK disabled;
- external FFTW; and
- OpenBLAS 0.3.33 for both BLAS and LAPACK.

The CMake policy compatibility setting `CMAKE_POLICY_VERSION_MINIMUM=3.5` allowed the
unchanged bundled MBD source to configure with CMake 4.3.3. No source bytes were
modified. Only target `qe_pw_exe` was requested, with at most eight local jobs. The
external build tree occupied 98 MiB.

The exact identities were:

- non-MPI diagnostic `pw.x` SHA-256:
  `f7509393bdff8aea7ead2766025ef76037b41d6d53674b86dbe819f50aef04e6`;
- non-MPI diagnostic `pw.x` size: 14,914,680 bytes;
- OpenBLAS library SHA-256:
  `dbd757cdfffbff1dc72fbf34983e89d5710933d04783f950441a57522fbf769d`;
- C48 input SHA-256:
  `cadb2a3024f39858f91b23bd1c1c22e2b2d0f161f2960c39ea1abf48cf00ee17`;
  and
- Si pseudopotential SHA-256:
  `39822757f53f36e3bf3bfb779356152a8d3f21199c7db9dd5a931e5d18c45282`.

`otool -L` confirmed OpenBLAS linkage and the absence of Open MPI, PMIx, hwloc, and
Apple Accelerate linkage. OpenBLAS was neither installed nor upgraded by this
operation and is not adopted as a project or production dependency.

The comparator used `OMP_NUM_THREADS=1` and a 120-second wall-time limit. No retry,
MPI-enabled invocation, debugger, trap alteration, setting promotion, successor
activation, network access, or remote, cluster, or cloud resource was used.

## Process result

The run root is
`~/projects/ksdft2effmass-runs/bulk-silicon-ieee-openblas-nonmpi-20260921T005103Z`.
The invocation began at `2026-09-21T01:01:02.107406Z` and ended at
`2026-09-21T01:01:02.878557Z` without reaching the timeout.

Observed state:

- QE mode: `Serial version`;
- termination: `SIGILL` (`EXC_BAD_INSTRUCTION`);
- wrapper return code: `-4`, because `/usr/bin/time` re-raised the child signal;
- QE banner and exact input: read successfully;
- first SCF iteration: not reached;
- `JOB DONE.`: absent;
- scratch regular files: zero;
- maximum resident set size: 29,605,888 bytes;
- peak memory footprint: 21,578,184 bytes; and
- external run-tree size after capture: 280 KiB.

Stdout ends after pseudopotential, symmetry, k-point, and dense-grid initialization.
It contains no total energy, SCF residual, pressure, force, or other completed physical
observable.

## Symbolized trap and exact comparator match

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

The exception code contains AArch64 instruction word `0x1e611802`, which decodes as:

```text
fdiv d2, d0, d1
```

The OpenBLAS image UUID, the five OpenBLAS image offsets, every retained OpenBLAS
symbol location above, and the faulting instruction word are identical to the prior
singleton-MPI OpenBLAS comparator. QE executable offsets differ because the MPI-off
binary is a different build, but the logical QE call chain and C48 initialization
stage are the same.

## Comparator interpretation and claim boundary

This result excludes Open MPI, PMIx, hwloc, and MPI initialization as necessary causes
of the later first enabled trap. A true serial executable with no MPI linkage reaches
the same OpenBLAS instruction below the same `ZHEGVX` call and terminates before SCF.
The earlier OpenCL/AGX startup trap remains a separate MPI-runtime source, but removing
that runtime does not remove the later scientific-path trap.

Together, the Apple Accelerate, singleton-MPI OpenBLAS, and non-MPI OpenBLAS results
localize the later first enabled trap to the generalized initial-wavefunction
subspace-eigenproblem rather than to one BLAS provider or to MPI startup. They do not
establish that all implementations execute identical intermediate arithmetic or that
the operation is mathematically material.

Because invalid, divide-by-zero, and overflow traps were still enabled together, the
non-MPI result does not identify which IEEE class fired. Underflow was not trapped.
No run retained the faulting floating-point operands, and the failed LLDB attempt
captured no target state. The effect on ordinary non-trapping final observables
therefore remains unresolved.

No warning suppression, OpenBLAS production adoption, provisional-setting promotion,
downstream eligibility, or scientific acceptance follows. The selected convergence
disposition and downstream production work remain blocked. Class-separated trapping
would require a new protected-execution decision.

## Retained identities

The external `manifest.json` has SHA-256
`66739aa4164cfa48cc1d36aec2292b1a9d991944f23307b17e72791544afc755`.
Principal retained artifacts are:

| Artifact | SHA-256 | Bytes |
|---|---|---:|
| `output/C48.scf.out` | `629547f3bdc17ff59933cde8ccb65650713bf3bebcc17e80ce73405ec4dd4f73` | 8,393 |
| `output/C48.scf.err` | `85788e3f3d37125dace908b831de31afdc0c3c7526390d6ac5cfbfde4d6b42bc` | 942 |
| `output/time.txt` | `bdd298ab351b837dd43989fea9eb8ed4dd44a806cfc40b7509c2a25861c12d55` | 67 |
| `output/process-result.json` | `1c74f8e769f8b63d21ac09d3a2b2ca87cef1044009e37eb64fdc4ed798154b15` | 565 |
| `output/executable-linkage.txt` | `a48e2ed8fd29361eaeaeb0e510ce8251166b18c7078f3b420c5d931a2a1b0c02` | 614 |
| `output/preflight-identities.txt` | `1cf6a536f5c7a410b15a576365f943f54b0ff95b5db3977fdcef2807b697cd46` | 631 |
| `output/pw-crash-report.ips` | `59a78e5989d7ee3c57e044b292385c7b74075c016026542e3b0579d24a9148f3` | 8,967 |
| `output/symbolized-backtrace.txt` | `0ce5df6660c074259527f48254b6b7208330e66d60cca435f47d0cd7901dae1d` | 987 |
