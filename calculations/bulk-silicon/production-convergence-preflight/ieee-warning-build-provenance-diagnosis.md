# IEEE Warning Build-Provenance Diagnosis

**Status:** Read-only diagnostic result. The message emitter is localized to the GNU
Fortran runtime at normal Fortran `STOP`; the operation or library that first set each
floating-point status flag remains unlocalized. This record does not establish
harmlessness or authorize a rebuild or executable invocation.

## Authorization and scope

The human response `recoemmendation authorized` authorized the recommended read-only
inspection of the exact QE executable's build, compiler/runtime configuration, and
link metadata. The inspection read the existing executable, Mach-O load commands,
CMake records, link/flag records, linked runtime, QE termination source, and one
co-located example result. It did not execute `pw.x`, a compiler, MPI, or another
scientific program; modify the QE tree; rebuild software; inspect dense calculation
artifacts; or submit external work.

The exact retained campaign executable was reauthenticated as:

- path: `~/projects/q-e-qe-7.2/build/bin/pw.x`;
- SHA-256: `6e8720e74cbafa7c7f07ee61ec6f5944c15d59bffa8ee8423fae14364f21c8ca`;
- size: 9,889,576 bytes;
- format: Mach-O 64-bit arm64;
- file modification time: `2026-06-19T14:26:02Z`.

## Build and link observations

The co-located CMake records identify:

- Release build with Fortran `-O3 -fallow-argument-mismatch`;
- GNU Fortran 16.1.0 through `/opt/homebrew/bin/mpif90`;
- AppleClang C 17.0.0 through `/opt/homebrew/bin/mpicc`;
- MPI enabled through Open MPI 5.0.9;
- OpenMP, CUDA, and sanitizer support disabled;
- external FFTW3 and Apple Accelerate BLAS/LAPACK; and
- no explicit `-ffpe-trap` or `-ffpe-summary` option in the inspected CMake cache,
  target flags, or exact `pw.x` link command.

The exact executable's Mach-O load commands dynamically reference FFTW, Open MPI,
Apple Accelerate, `libgfortran.5.dylib`, `libquadmath.0.dylib`, and `libSystem`.
Embedded runtime search paths identify the GCC 16.1.0 Homebrew installation. The
currently resolved GNU Fortran runtime has:

- path: `/opt/homebrew/opt/gcc/lib/gcc/current/libgfortran.5.dylib`;
- SHA-256: `44ff7844add7eb8b73fdef0b6d601e176f124dc032f8c325ad305a478ba986ed`;
- size: 2,216,112 bytes; and
- modification time: `2026-06-19T14:16:14Z`.

The exact diagnostic sentence and all four reported flag labels occur in that
`libgfortran` binary. The sentence does not occur in the inspected `pw.x` strings or
QE source tree. The exact executable imports GNU Fortran runtime setup and `STOP`
routines.

The inspected QE 7.2 main program calls `stop_run(exit_status)`, then
`do_stop(exit_status)`. For successful `exit_status == 0`, `do_stop` executes a
Fortran `STOP`. This matches the retained ordering: QE writes `JOB DONE.` to stdout,
then the GNU Fortran runtime writes the flag summary to stderr, then
`/usr/bin/time -l` appends resource accounting.

A co-located silicon example receipt,
`PW/examples/example01/results/si.scf.david.err`, contains the same exact runtime
message, while its stdout contains `JOB DONE.`. This is supporting local-build
context, not an independently authenticated execution of the retained production
input.

## Compact build-record identities

| Artifact | SHA-256 |
|---|---|
| `build/CMakeCache.txt` | `325c7ac672f199592ceb87dea66ee09c0c6821e1eb98bfe9a186ed1e570dff95` |
| `build/CMakeFiles/4.3.3/CMakeFortranCompiler.cmake` | `7db831cd6267cdc0a1a6aad7e0c73bec5a9b8695e8655c8e5f3ea67a6916a477` |
| `build/PW/CMakeFiles/qe_pw_exe.dir/link.txt` | `9320148bae589cc482fdc2220dac362c51c9e353b0d2af4a2b1a0a04f79aa8b2` |
| `build/PW/CMakeFiles/qe_pw_exe.dir/flags.make` | `234a00edd8eb95d44efc9d06948e6b409caf87ab736050f2211d26b60bc5d4c8` |
| `PW/src/pwscf.f90` | `dc583c5bdeccfff4529062ee918ff99a0d20e33eaf28a24b319927c6a3ef20ea` |
| `PW/src/stop_run.f90` | `a5c60c0407cb6f35fe8d5aa7d344d406a4cd4bfb2b31cac3d59ff0a2604af4f3` |

The original execution provenance did not retain a separate runtime-library checksum
or these build-record identities. Their current timestamps and contents are coherent
with the exact executable, but they are present-day read-only observations rather
than execution-time cryptographic provenance. The CMake cache also reports project
version 7.1 while the exact executable identifies itself as PWSCF 7.2; therefore the
cache version field is not used as release identity.

## QE 7.5 comparison

The retained, separately authorized QE 7.5 silicon smoke-test record directly rejects
the hypothesis that the existing local QE 7.5 build eliminates this report:

- executable: PWSCF 7.5 at source commit
  `770a0b2d12928a67048e2f3da8d10d057e52179e`;
- executable SHA-256:
  `87aa72158e2c103c63fce1deca977dc42ff4ba344519a9662aadb96d33eab910`;
- execution: one process, exit zero, SCF converged, and `JOB DONE.` present;
- stderr: the same exact 139-byte IEEE report;
- stderr SHA-256:
  `f382ec8367e667a70bf57907b4d4298dc573e3a6569c53218739fdb92f87b99e`;
- comparison: stderr was byte-identical to the retained QE 7.2 tutorial stderr.

The QE 7.5 installation record identifies the same GNU Fortran 16.1.0, Open MPI
5.0.9, Release configuration, FFTW, and Apple Accelerate toolchain family. Therefore
switching from the existing QE 7.2 binary to the existing QE 7.5 binary does not, by
itself, remove or diagnose the warning. This is a statement about the two exact local
builds and retained runs, not every possible QE 7.5 build or platform.

## Interpretation

The warning **emitter and timing are localized**: GNU Fortran reports accumulated
floating-point status flags when QE reaches its normal successful `STOP`. QE does not
emit the diagnostic sentence itself, and the build did not request immediate trapping
or a backtrace at the first raising operation.

This explains why all runs can return zero, print `JOB DONE.`, and still show the same
summary. It does not identify whether QE code, FFTW, Accelerate, MPI, libgfortran, or
another linked component first raised each flag, nor whether a flagged intermediate
quantity affected a retained observable. Uniformity across SCF and NSCF inputs reduces
the plausibility of a cutoff- or mesh-specific failure but is not evidence of
harmlessness.

## Disposition and next boundary

The read-only build diagnosis is **partially conclusive**:

- message emitter: GNU Fortran runtime;
- emission point: normal Fortran `STOP` after QE finalization;
- first flag-raising operation: not localized;
- effect on retained observables: not established;
- existing local QE 7.5 build: same exact report, so version substitution is not a
  demonstrated remedy.

The selected `block_pending_diagnosis` disposition remains in force. Localizing the
first raising operation now requires an instrumented diagnostic build or equivalent
runtime checkpoints. Any rebuild, changed compiler flags, or QE invocation is new
protected execution and requires exact human authorization for executable/build
identity, one selected input, resources, workspace, and retained outputs before it is
performed.
