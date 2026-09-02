# ABINIT 10.8.3 local installation

## Status

This record documents a **completed local dependency installation** authorized by
checkpoint `ABINIT-INSTALL-HC01`. It is not a calculation result, software-verification
result for a scientific input, numerical-verification result, scientific-validation
result, or authorization to execute an ABINIT tutorial.

ABINIT was built from the official 10.8.3 production archive in an external source
and build tree and installed into a separate external prefix. Repository records use
the symbolic locations `${ABINIT_SOURCE_ROOT}` and `${ABINIT_PREFIX}`; machine-local
paths and build logs remain outside Git.

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

The source archive, extraction, build trees, installed executables, and complete logs
remain external to the repository. The external compact record
`installation-result.json` has SHA-256
`ed0bc279a150c136ab1fb43227d8dee5f3dfc9451f7cce390137dbcfdb21df5a`.

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

The build used GNU Fortran 16.1.0 through Open MPI 5.0.9 wrappers, Clang/LLVM 17 for
C and C++, FFTW 3.3.11, and OpenBLAS 0.3.33. No project Python dependency changed.

## Build configuration

The successful corrected build used:

- MPI and MPI-IO enabled;
- OpenMP and GPU support disabled;
- OpenBLAS linear algebra;
- serial HDF5 and NetCDF libraries;
- FFTW3 with double- and single-precision serial and MPI libraries;
- LibXC enabled;
- standard optimization with basic debug information; and
- Wannier90 integration disabled.

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
  --with-netcdf-fortran="${DEPENDENCY_PREFIX}"
```

The successful eight-job build took approximately 345 seconds and reported a maximum
resident set size of approximately 725 MB. The final source/build tree occupied about
1.3 GB and the installed prefix about 145 MB.

## Corrected installation findings

The first link attempt failed because automatic FFTW discovery omitted the
single-precision `fftw3f` and `fftw3f_mpi` libraries required by ABINIT symbols. A
fresh build directory with explicit complete FFTW library flags linked successfully.
The initial install prefix also collided with the source archive's existing lowercase
`install` text file. Installation was repeated with a separate external prefix and
completed successfully. Neither failed attempt ran a scientific input.

The successful configuration retained these limitations:

- the installed LibXC bottle lacks third energy derivatives, so ABINIT reports that
  nonlinear-response features such as Raman intensities are unavailable;
- HDF5 and NetCDF are serial builds even though ABINIT and native MPI-IO are enabled;
- Wannier90, GPU, OpenMP, LibPSML, and XMLF90 support are disabled; and
- the linker emitted duplicate-library warnings during executable construction.

These limitations do not establish suitability for a future tutorial or production
calculation; each execution still requires capability and input preflight.

## Executable identity and verification boundary

| Field | Value |
|---|---|
| Executable role | `${ABINIT_PREFIX}/bin/abinit` |
| Reported version | `10.8.3` |
| Build target | `arm_darwin25.5.0_gnu16.1` |
| Executable bytes | 30,011,784 |
| Executable SHA-256 | `92f685345f7ff4c99085e72dd8e1a2964b20c70e0675c8468e42057d240ce431` |
| Format | Mach-O 64-bit arm64 |
| Command exposure | A user-local symbolic link exposes `abinit` on `PATH` |

`abinit --version` and `abinit --build` completed and reported the configured MPI,
MPI-IO, FFTW3, OpenBLAS, HDF5, NetCDF, NetCDF Fortran, and LibXC capabilities. The
ABINIT quick and full test suites were not run because they execute scientific test
inputs and were outside this installation-only authorization. No pseudopotential,
tutorial input, or calculated output was acquired or executed.
