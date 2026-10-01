# IEEE Warning OpenCL-Disabled C48 Diagnosis

**Status:** One authorized calculated diagnostic execution completed exactly once.
Disabling hwloc OpenCL discovery bypassed the previously localized MPI-startup trap,
but the same instrumented executable trapped later in Apple Accelerate while QE was
constructing initial wavefunctions. This is diagnostic software evidence, not a
completed SCF calculation, calculated physical result, numerical verification,
scientific validation, or harmlessness determination.

## Authorization and exact operation

Human response `yes` unambiguously selected
`authorize_one_opencl_disabled_instrumented_c48_scf` in
`.pi/checkpoints/bulk-silicon-convergence-ieee-opencl-disabled-diagnosis-execution.json`.
The operation reauthenticated and reused the existing instrumented QE 7.2 executable
without rebuilding:

- executable SHA-256:
  `83b2c9b77c5c5b1b7ed694145ef61035c7a6f2d7edcb723092d071589d50f979`;
- C48 input SHA-256:
  `cadb2a3024f39858f91b23bd1c1c22e2b2d0f161f2960c39ea1abf48cf00ee17`;
- Si pseudopotential SHA-256:
  `39822757f53f36e3bf3bfb779356152a8d3f21199c7db9dd5a931e5d18c45282`;
- environment: `HWLOC_COMPONENTS=-opencl` and `OMP_NUM_THREADS=1`; and
- one singleton MPI invocation with a 120-second wall-time limit.

No retry, rebuild, second environment change, underflow trap, successor activation,
network access, or remote, cluster, or cloud resource was used.

## Process result

The run root is
`~/projects/ksdft2effmass-runs/bulk-silicon-ieee-diagnostic-no-opencl-20260920T174832Z`.
The invocation began at `2026-09-21T00:04:43.792340Z` and ended at
`2026-09-21T00:04:44.140950Z` without reaching the timeout.

Observed state:

- termination: `SIGILL` (`EXC_BAD_INSTRUCTION`);
- wrapper return code: `-4`, because `/usr/bin/time` re-raised the child signal;
- QE banner and exact input: read successfully;
- OpenCL-startup trap: bypassed;
- first SCF iteration: not reached;
- `JOB DONE.`: absent;
- scratch regular files: zero;
- maximum resident set size: 39,223,296 bytes;
- peak memory footprint: 25,248,176 bytes; and
- external run-tree size after capture: 280 KiB before the compact manifest.

Stdout ends after pseudopotential, symmetry, k-point, and dense-grid initialization.
It contains no total energy, SCF residual, pressure, force, or other completed physical
observable.

## Symbolized trap

The macOS crash report and dSYM generated from the retained debug-build object files
localize the call chain to:

```text
Apple Accelerate libBLAS faulting instruction
  -> ZTRSM
  -> Apple Accelerate libLAPACK ZHEGVX
  -> LAXlib/cdiaghg.f90:143
  -> KS_Solvers/DENSE/rotate_wfc_k.f90:114
  -> KS_Solvers/DENSE/rotate_wfc.f90:93
  -> PW/src/wfcinit.f90:419
  -> PW/src/wfcinit.f90:258
  -> PW/src/init_run.f90:196
  -> PW/src/run_pwscf.f90:162
  -> PW/src/pwscf.f90:85
```

At `cdiaghg.f90:143`, QE calls `ZHEGVX` to compute the lowest generalized Hermitian
eigenpairs. This occurs while rotating the initial atomic-wavefunction subspace,
before the first SCF iteration.

The crash exception code and instruction bytes identify AArch64 instruction word
`0x1e621864`. Independent local disassembly produced:

```text
fdiv d4, d3, d2
```

Thus, after OpenCL discovery is disabled, the next enabled floating-point trap is an
actual floating-point division inside Apple Accelerate's triangular solve used by
`ZHEGVX`. Because invalid, divide-by-zero, and overflow traps were enabled together,
the single run does not establish which IEEE class fired; an `fdiv` may raise any of
those classes depending on its operands.

## Interpretation and claim boundary

The first diagnosis established one external MPI/OpenCL startup source. This follow-up
establishes a **second, later trap location** in the numerical path used to initialize
QE wavefunctions. Disabling OpenCL discovery alone therefore does not eliminate the
instrumented failure and is not sufficient to classify the retained warning as a
pure startup artifact.

The faulting implementation is Apple Accelerate rather than a QE instruction, but it
is executing QE's generalized subspace-eigenproblem. The run does not retain the
floating-point operands or identify whether the operation is a benign implementation
intermediate, a padded-lane operation, a singular intermediate, or a mathematically
material division. Underflow was not trapped. The run also cannot establish whether
the ordinary non-trapping path's final finite observables were affected.

No warning suppression, provisional-setting promotion, downstream eligibility, or
scientific acceptance follows. The selected convergence disposition and downstream
production work remain blocked. Identifying the exact IEEE class or comparing a
separately authorized non-Accelerate implementation would require a new protected
execution and, for a different BLAS/LAPACK provider, an explicit dependency decision.

## Retained identities

The external `manifest.json` has SHA-256
`f7b66ba24d12ff959dad51501ef95609c13b6c7e885fbf174990505bd36d0f16` and binds the
run artifacts and exact environment. Principal identities are:

| Artifact | SHA-256 | Bytes |
|---|---|---:|
| `output/C48.scf.out` | `f9691efc9d7d9bea275e76c0a4c4dcf0ff8aa5929844c0592f32876318a4618d` | 8,618 |
| `output/C48.scf.err` | `eec4d9584b17aeb6d493908fee7d9271e343d8f96459a1e6a6490f03d72df2bd` | 427 |
| `output/time.txt` | `38fbaab659563e8dc7a518e5823c97baf64cd200675372907d15d47a2acbebbd` | 777 |
| `output/process-result.json` | `812afbc3bab048ea47c2e7c5d38f500e4cabab5bf1aead762d79124447bcd58f` | 543 |
| `output/pw-crash-report.ips` | `0abb4fc0adb3e21085643a78b41d85da5efec4ca23bc704051da54963d99dfd2` | 12,867 |
| `output/time-crash-report.ips` | `c6c8701622ecca3858b11e417fc2a48a198a20dbfc670c2fd991f1aad97b2fd4` | 6,446 |
| `output/symbolized-backtrace.txt` | `bbe06bbf3e6178c5a25e0208c389f18cabc070f6070e39787bda8c28dbc004ad` | 1,107 |
