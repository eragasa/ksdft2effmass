# IEEE Warning Instrumented C48 Diagnosis

**Status:** One authorized calculated diagnostic execution completed exactly once.
The instrumented process trapped during Open MPI startup, before the QE banner, input
parsing, or scientific computation. This is diagnostic software evidence, not a
calculated physical result, numerical verification, scientific validation, or proof
that later QE operations cannot independently raise floating-point flags.

## Authorization and limits

Human response `authorize_one_instrumented_c48_scf` selected the exact protected
operation in
`.pi/checkpoints/bulk-silicon-convergence-ieee-instrumented-diagnosis-execution.json`.
The authorized operation comprised one isolated debug/trapping QE 7.2 build and one
C48 SCF invocation. No retry, QE 7.5 execution, underflow trap, successor activation,
network access, or remote, cluster, or cloud resource was authorized or used.

The invocation used:

- retained C48 input SHA-256:
  `cadb2a3024f39858f91b23bd1c1c22e2b2d0f161f2960c39ea1abf48cf00ee17`;
- retained Si pseudopotential SHA-256:
  `39822757f53f36e3bf3bfb779356152a8d3f21199c7db9dd5a931e5d18c45282`;
- two Si atoms, 48/192 Ry cutoffs, and a shifted $8\times8\times8$ mesh;
- one singleton MPI process and `OMP_NUM_THREADS=1`; and
- a 120-second wall-time limit.

## Isolated diagnostic build

The unchanged, non-Git source snapshot at `~/projects/q-e-qe-7.2` was configured into
`~/projects/q-e-diagnostics/qe-7.2-ieee-20260920T173542Z/build`. The first configure
attempt stopped before compilation because CMake 4.3 required an explicit legacy
policy minimum for bundled MBD. Configuration was then completed in the same
isolated build with `CMAKE_POLICY_VERSION_MINIMUM=3.5`; this correction did not invoke
QE or alter source bytes.

The successful build retained MPI, FFTW, and Apple Accelerate linkage, disabled
OpenMP and ScaLAPACK, and compiled the QE modules, PW library, and PW main program
with:

```text
-fallow-argument-mismatch -O0 -g -fbacktrace \
-ffpe-trap=invalid,zero,overflow
```

The resulting executable has:

- SHA-256: `83b2c9b77c5c5b1b7ed694145ef61035c7a6f2d7edcb723092d071589d50f979`;
- size: 15,851,832 bytes; and
- Mach-O UUID: `d018b832-32f6-3ee6-9d49-a9710a16298b`.

The complete external diagnostic build occupies 103,492 KiB. Its configure and build
logs, CMake cache, exact flags, exact link command, compiler metadata, and Mach-O
load dependencies remain in that external build directory.

## Single invocation result

The external run root is
`~/projects/ksdft2effmass-runs/bulk-silicon-ieee-diagnostic-20260920T173542Z`.
The exact invocation count is one. It began at `2026-09-20T17:42:20.086549Z` and ended
at `2026-09-20T17:42:20.967650Z` without reaching the timeout.

Observed process state:

- termination: `SIGILL` (`EXC_BAD_INSTRUCTION` in the macOS crash report);
- wrapper return code: `-4`, because `/usr/bin/time` re-raised the child signal;
- stdout: empty;
- `JOB DONE.`: absent;
- scratch regular files: zero;
- maximum resident set size: 21,463,040 bytes;
- peak memory footprint: 7,389,712 bytes; and
- external run-tree size after capture: 268 KiB.

GNU Fortran's text backtrace contained only addresses and reported that it could not
symbolize the executable. The macOS crash report supplied the symbolized faulting
stack.

## First-trap localization

The fault occurred in the following startup path:

```text
Apple AGX Metal sampler-state initialization
  -> Metal/OpenCL device registration
  -> clGetDeviceIDs
  -> hwloc_opencl_discover
  -> hwloc_topology_load
  -> PMIx_Init
  -> Open MPI initialization
  -> MPI_Init
  -> QE mp_world_start
  -> QE mp_startup
  -> PWSCF MAIN
```

The faulting thread is the Metal device-dispatch queue. The faulting image is Apple's
`AGXMetalG16G_B0` driver, not `pw.x`, libgfortran, FFTW, or Apple Accelerate. The
faulting instruction stream consists of floating-point instructions, and the process
was compiled to trap invalid, divide-by-zero, and overflow conditions globally.
The trap occurred before QE printed its banner, read the C48 input, allocated a
calculation scratch state, or evaluated a physical observable.

This localizes the **first instrumented fatal trap** to Open MPI's PMIx/hwloc OpenCL
device discovery and Apple Metal driver initialization. It supplies a concrete
external-runtime source consistent with the otherwise successful QE 7.2 and QE 7.5
runs accumulating sticky flags before GNU Fortran reports them at normal `STOP`.

## Web corroboration

The following sources were accessed on **2026-09-20**. They support software-runtime
interpretation only; they do not establish the correctness of this project's retained
scientific observables.

- The [GNU Fortran debugging-options manual](https://gcc.gnu.org/onlinedocs/gfortran/Debugging-Options.html)
  states that `-ffpe-summary` prints accumulated flag status to `ERROR_UNIT` when
  `STOP` or `ERROR STOP` is invoked, with all exceptions except `inexact` included by
  default. It recommends traps for `invalid`, `zero`, and `overflow` because those
  conditions often indicate serious errors. This matches both the retained
  termination-time summary and the chosen trap set.
- The official [hwloc components documentation](https://hwloc.readthedocs.io/en/latest/doxygen/html/plugins.html)
  identifies `opencl` as the component that calls OpenCL to create device objects and
  documents prefixing a component with `-` in `HWLOC_COMPONENTS` to prevent loading
  it. The official [hwloc FAQ](https://www-lb.open-mpi.org/projects/hwloc/doc/v2.12.2/faq.html)
  explicitly gives `HWLOC_COMPONENTS=-opencl,...` as the runtime mechanism for
  disabling OpenCL discovery.
- An independent 2021 [Apple-Silicon MPI diagnostic](https://kirija.github.io/blog-post-1/)
  reports an almost identical `EXC_BAD_INSTRUCTION` stack: an `fmul` in an Apple AGX
  Metal driver, then Metal/OpenCL, `clGetDeviceIDs`, `hwloc_opencl_discover`, Open MPI,
  `MPI_Init`, and the application main program. That report concerns Meso-NH rather
  than QE and is not authoritative project evidence, but it strongly corroborates
  the platform/runtime path observed here. It reported that launching through
  `mpirun` avoided its singleton path; this project has not tested that workaround.
- In a [QE-users response](https://lists.quantum-espresso.org/pipermail/users/2020-April/044431.html),
  Paolo Giannozzi reported that he could not reproduce a user's divide-by-zero flag,
  observed only underflow in his test, and pointed to the compiler, libraries, or
  runtime environment rather than a known QE division by zero. This is consistent
  with the present runtime localization but does not prove the retained calculations
  harmless.
- Older QE community messages describe underflow or denormal summaries as non-errors,
  and a [Quantum Mobile issue](https://github.com/marvel-nccr/quantum-mobile/issues/52)
  suggests `-ffpe-summary=none` to hide them. Suppressing the summary is not adopted
  here because it would remove reporting without identifying or excluding later
  flag-setting operations, and the retained report includes invalid, divide-by-zero,
  and overflow in addition to underflow.

The web evidence therefore supports the pending follow-up's narrow use of
`HWLOC_COMPONENTS=-opencl`. It does not support suppressing the warning or accepting
the scientific outputs solely because QE reached `JOB DONE.`.

## Claim boundary

The single trapping run does not identify which one of invalid, divide-by-zero, or
overflow caused the first trap because all three were enabled together. Underflow was
not trapped. Because execution stopped during MPI initialization, this run also cannot
exclude additional independent flag-setting operations later in QE, FFTW, Accelerate,
or another linked component. It therefore does not by itself establish that all four
retained flags are external to QE or that retained scientific observables are
unaffected.

The exact authorized execution is complete and will not be retried automatically. A
further run that disables hwloc OpenCL discovery or introduces post-MPI flag
checkpoints is a distinct protected operation requiring a new exact human decision.
Until the evidence disposition is decided, the selected convergence Task and all
downstream production work remain blocked.

## Retained identities

The external `manifest.json` has SHA-256
`c7585524560999fc3ee65732b8f62fabbbb85b140e0b24489e7378b743d4d68b` and binds the
build and run artifacts. Principal run-artifact identities are:

| Artifact | SHA-256 | Bytes |
|---|---|---:|
| `output/C48.scf.out` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `output/C48.scf.err` | `53d1ea2f5e7ef051c5caee3ee281fefa4596c0ab9c71200be20aef095931c4ee` | 492 |
| `output/time.txt` | `b2a484e91936512c7294dee8ecc721ded64dd0110b12b53da40665ecbdf867db` | 777 |
| `output/process-result.json` | `81bcc739bc9e4f48a5588a8489b89d53ed64e92b963b3af58b59e0a19949273e` | 471 |
| `output/pw-crash-report.ips` | `b343e2a5b2841ab28781c1f6e731b0c1ee3f637d97d12ab7281f2fdcbb0866d1` | 18,401 |
| `output/time-crash-report.ips` | `427732fc2d9e949bd948999ee6b09c0f742517a74615f870af36d319f32766d4` | 6,436 |
