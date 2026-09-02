# Wannier90 3.1.0 local installation

## Status

This record documents a **completed local dependency installation** authorized by
checkpoint `ABINIT-WANNIER90-HC01`. It is not a Wannierization result, scientific-input
software-verification result, numerical-verification result, scientific-validation
result, or execution authorization.

Wannier90 3.1.0 was selected because ABINIT 10.8.3 identifies it as the current
Wannier90 fallback and the official ABINIT Homebrew formula selects the same release.
It was built from the official Wannier90 source archive in an isolated external tree.
Repository records use `${WANNIER90_SOURCE_ROOT}` and `${WANNIER90_PREFIX}` rather than
machine-local paths.

## Source and license identity

| Field | Value |
|---|---|
| Release | Wannier90 3.1.0 |
| Official release | `https://github.com/wannier-developers/wannier90/releases/tag/v3.1.0` |
| Official archive | `https://github.com/wannier-developers/wannier90/archive/v3.1.0.tar.gz` |
| Archive bytes | 101,211,573 |
| Archive SHA-256 | `40651a9832eb93dec20a8360dd535262c261c34e13c41b6755fa6915c936b254` |
| Archive structure | 1,434 entries under one `wannier90-3.1.0/` root; no absolute or parent-traversal paths observed |
| Version marker | `3.1.0` in `src/io.F90` |
| License | GPL-2.0-or-later, as stated in the source header and reproduced license |

The source, build tree, installed prefix, and complete logs remain external. The
external `installation-result.json` has SHA-256
`a29053ecbbebcf6f2102d340f681b35a254ae9c8b2b735c466d343e321cd923c`.

## Build and installation

The build used GNU Fortran 16.1.0, Open MPI 5.0.9, and OpenBLAS 0.3.33. It enabled MPI
for the main and postprocessing executables and produced the static library required by
the ABINIT Fortran connector. In portable symbolic form, its material configuration
was:

```makefile
F90 = gfortran
CC = clang
COMMS = mpi
MPIF90 = mpifort
FCOPTS = -O2 -fallow-argument-mismatch -ffree-line-length-none
LDOPTS = -O2
LIBS = -L${OPENBLAS_PREFIX}/lib -lopenblas
```

The eight-job build took approximately 11 seconds and reported a maximum resident set
size of approximately 262 MB. The source/build tree occupied about 173 MB and the
installed prefix about 4.8 MB. Installation produced:

- `wannier90.x`;
- `postw90.x`;
- `w90chk2chk.x`;
- `w90spn2spn.x`;
- `w90pov`;
- `w90vdw.x`; and
- `libwannier.a`, with a `libwannier90.a` compatibility alias for ABINIT's default
  linker name.

User-local symbolic links expose these executables on `PATH` without committing their
machine locations.

## Identity and verification boundary

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `${WANNIER90_PREFIX}/bin/wannier90.x` | 891,048 | `c826f817f807cf069e16d6e529a52ddc15d2f677101065908bcb2030d7f7d1dd` |
| `${WANNIER90_PREFIX}/bin/postw90.x` | 889,384 | `6ebea4c227f94b4877c07d60a3197ca9a1b0e8d0db07ab41137a15fc49fda686` |
| `${WANNIER90_PREFIX}/lib/libwannier.a` | 1,296,704 | `c86799643ffca4d3ab59f2a96a793d5edb5709bae8c4d9348c727390b2980664` |

`wannier90.x --version` and `postw90.x --version` both reported 3.1.0 and exited
successfully. Both also printed an `IEEE_OVERFLOW_FLAG` notice, which remains a
build-probe limitation until its relevance is investigated under an authorized input.
No Wannier90 scientific test suite or example was run.

The [ABINIT 10.8.3 installation](abinit-10.8.3-installation.md) was rebuilt against
this static library. ABINIT configure reported that the Wannier90 Fortran interface
works, and the resulting `abinit --build` reports `Wannier90: yes`. This establishes
installation and link capability only; it does not establish QE–Wannier90 or
ABINIT–Wannier90 scientific-input compatibility.
