# ABINIT 10.8.3 local installation

## Status

This record documents a **completed local dependency installation** authorized by
checkpoints `ABINIT-INSTALL-HC01` and `ABINIT-WANNIER90-HC01`. It is not a calculation
result, software-verification result for a scientific input, numerical-verification
result, scientific-validation result, or authorization to execute an ABINIT or
Wannier90 tutorial.

ABINIT was built from the official 10.8.3 production archive in an external source
and build tree and installed into a separate external prefix. After the first completed
build incorrectly omitted a required planned capability, Wannier90 3.1.0 was built from
official source and ABINIT was rebuilt in a fresh tree with its Wannier90 connector
enabled. The superseded ABINIT prefix remains external for rollback. Repository records
use the symbolic locations `${ABINIT_SOURCE_ROOT}`, `${ABINIT_PREFIX}`, and
`${WANNIER90_PREFIX}`; machine-local paths and build logs remain outside Git.

## Source and license identity

| Field | Value |
|---|---|
| Release | ABINIT 10.8.3 production release |
| Official archive | `https://forge.abinit.org/abinit-10.8.3.tar.gz` |
| Archive bytes | 166,705,042 |
| Archive SHA-256 | `cfad7f1c1bfa90c2fac3dca02f8d4d1c7aaf7d6e0d3bba24c091185d559c503b` |
| Archive structure | 13,905 entries under one `abinit-10.8.3/` root; no absolute or parent-traversal paths observed |
| Version marker | `10.8.3` |
| Archive HTTP `Last-Modified` | 2026-08-07 |
| License | The archive `COPYING` states that most source and documentation use GPL-3.0 and a small number of routines use Apache-2.0, which it describes as GPL-compatible |

Wannier90 source, license, build, executable, and library identity are owned by the
[Wannier90 3.1.0 installation record](wannier90-3.1.0-installation.md).

The ABINIT source archive, extraction and build trees, installed executables, and
complete logs remain external to the repository. The external ABINIT
`installation-result.json` has SHA-256
`afc06c2e65eba0b828471467bafe27a0aa083686239a2932a3af9bdfb64c84e2`.

## Added local dependencies

The source build used the existing compiler, MPI, FFTW, OpenBLAS, and ScaLAPACK
installations. The authorized dependency step added these Homebrew packages:

| Package | Installed version | Role |
|---|---:|---|
| LibXC | 7.1.2 | Exchange-correlation library |
| NetCDF Fortran | 4.6.4 | Fortran NetCDF interface |
| NetCDF | 4.10.1 | Installed dependency of NetCDF Fortran |
| HDF5 | 2.2.0 | Installed dependency of NetCDF |
| libaec | 1.1.7 | Compression dependency |
| pkgconf | 3.0.6 | Build-time package discovery |
| isl | 0.28 | Compiler dependency update |

Wannier90 3.1.0 was then built from official source with GNU Fortran 16.1.0,
Open MPI 5.0.9, and OpenBLAS 0.3.33. ABINIT used the same GNU Fortran MPI wrappers,
Clang/LLVM 17 for C and C++, and FFTW 3.3.11. No project Python dependency changed.

## Build configuration

The successful corrected build used:

- MPI and MPI-IO enabled;
- OpenMP and GPU support disabled;
- OpenBLAS linear algebra;
- serial HDF5 and NetCDF libraries;
- FFTW3 with double- and single-precision serial and MPI libraries;
- LibXC enabled;
- standard optimization with basic debug information; and
- the external Wannier90 3.1.0 Fortran interface enabled and detected as working.

In portable symbolic form, the essential configuration was:

```bash
CC=mpicc CXX=mpicxx FC=mpifort \
FFTW3_CPPFLAGS="-I${DEPENDENCY_PREFIX}/include" \
FFTW3_FCFLAGS="-I${DEPENDENCY_PREFIX}/include" \
FFTW3_LIBS="-L${DEPENDENCY_PREFIX}/lib -lfftw3_threads -lfftw3 -lfftw3f -lfftw3_mpi -lfftw3f_mpi" \
LINALG_FCFLAGS="-I${OPENBLAS_PREFIX}/include" \
LINALG_LIBS="-L${OPENBLAS_PREFIX}/lib -lopenblas" \
"${ABINIT_SOURCE_ROOT}/configure" \
  --prefix="${ABINIT_PREFIX}" \
  --with-optim-flavor=standard \
  --with-mpi="${DEPENDENCY_PREFIX}" \
  --enable-mpi-io \
  --with-linalg-flavor=openblas \
  --with-fftw3="${DEPENDENCY_PREFIX}" \
  --with-fft-flavor=fftw3 \
  --with-libxc="${DEPENDENCY_PREFIX}" \
  --with-hdf5="${DEPENDENCY_PREFIX}" \
  --with-netcdf="${DEPENDENCY_PREFIX}" \
  --with-netcdf-fortran="${DEPENDENCY_PREFIX}" \
  --with-wannier90="${WANNIER90_PREFIX}"
```

The connector-enabled eight-job ABINIT build took approximately 820 seconds and
reported a maximum resident set size of approximately 740 MB. The retained ABINIT
source/build tree occupied about 1.7 GB and the corrected installed prefix about
149 MB. Wannier90 build and storage details remain in its owning installation record.

## Corrected installation findings

The first link attempt failed because automatic FFTW discovery omitted the
single-precision `fftw3f` and `fftw3f_mpi` libraries required by ABINIT symbols. A
fresh build directory with explicit complete FFTW library flags linked successfully.
The initial install prefix also collided with the source archive's existing lowercase
`install` text file, so deployments use separate external prefixes.

The first completed build reported `Wannier90: no`. That build did not satisfy the
planned workflow capability and is superseded. A fresh connector-enabled ABINIT build
passed configure's Wannier90 Fortran-interface link check and reports
`HAVE_WANNIER90` and `Wannier90: yes`. The prior prefix remains available only for
rollback. No attempt ran a scientific input.

The corrected configuration retains these limitations:

- the installed LibXC bottle lacks third energy derivatives, so ABINIT reports that
  nonlinear-response features such as Raman intensities are unavailable;
- HDF5 and NetCDF are serial builds even though ABINIT and native MPI-IO are enabled;
- GPU, OpenMP, LibPSML, and XMLF90 support are disabled; and
- the linkers emitted duplicate-library warnings during executable construction.

These limitations do not establish suitability for a future tutorial or production
calculation; each execution still requires capability and input preflight.

## Executable identity and verification boundary

| Field | Value |
|---|---|
| Executable role | `${ABINIT_PREFIX}/bin/abinit` |
| Reported version | `10.8.3` |
| Build target | `arm_darwin25.5.0_gnu16.1` |
| Executable bytes | 31,574,904 |
| Executable SHA-256 | `0f5b2ddc46a166271a5a61a0d618974cc8db1b3dfb7dbe13ebf4b04396b54e82` |
| Format | Mach-O 64-bit arm64 |
| Command exposure | A user-local symbolic link exposes the connector-enabled `abinit` on `PATH` |
| Reported Wannier90 connector | `yes` |

`abinit --version` and `abinit --build` completed and reported MPI, MPI-IO, FFTW3,
OpenBLAS, HDF5, NetCDF, NetCDF Fortran, LibXC, and Wannier90. The ABINIT scientific
test suites were not run because they execute scientific inputs and were outside this
installation-only authorization. Wannier90 executable verification is recorded in its
[owning installation record](wannier90-3.1.0-installation.md). No pseudopotential,
tutorial input, or calculated output was acquired or executed.
