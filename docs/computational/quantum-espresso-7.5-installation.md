# Quantum ESPRESSO 7.5 local installation

## Status

This record documents a **completed local dependency installation**. It is not a
calculation result, numerical-verification result, scientific-validation result,
or authorization to run Quantum ESPRESSO.

The installation was authorized by the human response `ok install 7.5`, retained
in `.pi/checkpoints/quantum-espresso-7.5-side-by-side-installation.json`. Quantum
ESPRESSO 7.2 remains installed for reproduction of the accepted tutorial records.

## Source identity

| Field | Value |
|---|---|
| Repository | `https://github.com/QEF/q-e.git` |
| Annotated tag | `qe-7.5` |
| Tag object | `17975e6f2ba19aec6f50d99c1fc677361d7c8b3a` |
| Commit | `770a0b2d12928a67048e2f3da8d10d057e52179e` |
| Local source | Dedicated external QE 7.5 source tree (`${QE75_SOURCE_ROOT}` below) |
| Signature status | The annotated Git tag is unsigned |

The `external/d3q` submodule contains both `LICENSE` and `License`. Those names
collide on the local case-insensitive filesystem. Local Git configuration ignores
that submodule worktree discrepancy when reporting the superproject source identity;
the default build did not require a D3Q executable for the retained `pw.x` and
`pw2wannier90.x` outputs.

## Build configuration

| Field | Value |
|---|---|
| Build directory | `${QE75_SOURCE_ROOT}/build` |
| Build type | `Release` |
| CMake | 4.3.4 |
| C compiler wrapper | `mpicc` from the local package manager |
| Fortran compiler wrapper | `mpif90` from the local package manager |
| GNU Fortran | 16.1.0 |
| Open MPI | 5.0.9; MPI and Fortran MPI module enabled |
| FFTW | Locally packaged FFTW 3.3.11 shared library |
| BLAS/LAPACK | Apple Accelerate |
| OpenMP | disabled |
| ScaLAPACK | disabled |
| QE tests | configured but not executed |
| Installed tree size | approximately 2.6 GiB |

Configuration and compilation used:

```bash
QE75_SOURCE_ROOT=/path/to/external/q-e-qe-7.5
cmake -S "${QE75_SOURCE_ROOT}" \
  -B "${QE75_SOURCE_ROOT}/build" \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_C_COMPILER=mpicc \
  -DCMAKE_Fortran_COMPILER=mpif90 \
  -DQE_ENABLE_MPI=ON \
  -DQE_ENABLE_OPENMP=OFF \
  -DQE_ENABLE_SCALAPACK=OFF \
  -DQE_ENABLE_TEST=ON
cmake --build "${QE75_SOURCE_ROOT}/build" --parallel 8
```

External build logs are retained outside the repository.

## Executable identities

| Executable | SHA-256 | Bytes | Format |
|---|---|---:|---|
| `${QE75_SOURCE_ROOT}/build/bin/pw.x` | `87aa72158e2c103c63fce1deca977dc42ff4ba344519a9662aadb96d33eab910` | 9,673,048 | Mach-O 64-bit arm64 |
| `${QE75_SOURCE_ROOT}/build/bin/pw2wannier90.x` | `61c8255b0745df2a5dec3c55e600b1f8b87039b564004997ac45cfee42cf2c8c` | 8,379,632 | Mach-O 64-bit arm64 |

The built source header identifies version `7.5`, and the generated Git revision
header identifies commit `770a0b2d12928a67048e2f3da8d10d057e52179e` without a dirty suffix.

## Verification boundary and limitations

Compilation completed successfully. The compiler emitted upstream legacy-format,
argument-shape/type, and duplicate-link-library warnings in several optional QE
components; they were not interpreted as failures or correctness findings.

A version-banner probe supplied `--version`, but these executables entered their
ordinary no-input startup path rather than treating it as a version-only option.
They printed QE 7.5 banners, then stopped with missing-namelist errors. No scientific
input was supplied during installation verification.

A separately authorized, isolated silicon SCF tutorial smoke test was subsequently
run once. Its calculated observations and mechanical comparison with QE 7.2 are
retained in
[`execution-comparison.json`](../../calculations/bulk-silicon/qe-7.5-si-scf-smoke-comparison/execution-comparison.json).
The run completed and exposed QEXSD 25.05.21. The canonical project parser was
subsequently extended to accept that exact format while preserving support for the
retained QEXSD 23.03.10 artifact; unlisted versions still fail closed. No QE test
suite, production convergence study, numerical verification, scientific validation,
uncertainty quantification, or QE--Wannier90 interface smoke test has been run
against this installation.
