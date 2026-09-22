"""Execution-free QE 7.2 MPI/OpenBLAS comparator build planning.

This module represents a proposed isolated replacement toolchain for a release-like
QE 7.2 MPI/OpenBLAS observable comparator and binds it to the generic native build
planner.  It emits immutable direct CMake argument vectors only.  It does not amend or
resolve the pending comparator checkpoint, inspect the non-Git source snapshot, verify
installed bytes, create the proposed hierarchy, install or adopt dependencies, invoke
CMake or a compiler, or authorize protected build or scientific execution.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from ksdft2effmass.toolchains import (
    NativeBuildLimits,
    NativeBuildPlan,
    NativeBuildPlanner,
    NativeBuildRecipe,
    NativeBuildSpecification,
    NativeCMakeDefinition,
    NativeToolchainSpecification,
    NativeToolContentNotPinned,
    NativeToolRole,
    NativeToolSha256ContentIdentity,
    NativeToolSpecification,
)

_REFERENCE_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:+-]{0,127}\Z", re.ASCII)
_WORKSPACE_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z", re.ASCII)
_OPENBLAS_SHA256 = "dbd757cdfffbff1dc72fbf34983e89d5710933d04783f950441a57522fbf769d"


@dataclass(frozen=True, slots=True)
class QuantumEspressoOpenBlasComparatorBuildRequest:
    """Request the exact execution-free QE comparator build plan.

    Parameters
    ----------
    source_snapshot_reference
        Explicit identity of the retained unchanged QE 7.2 non-Git source snapshot.
        The reference is not a tree digest and planning does not authenticate it.
    source_root
        Absolute local source root proposed by the pending checkpoint.
    toolchain_root
        Absolute local root corresponding to ``~/opt``. Immutable package prefixes
        and the toolchain manifest location are derived beneath it without ambient
        home-directory lookup or filesystem access. Modulefiles remain future
        non-authoritative views.
    build_root
        Absolute scratch root corresponding to ``~/build`` and disjoint from both the
        source and toolchain roots.
    build_workspace_name
        One portable no-parent workspace component, normally the authorized run or
        build identity. Planning never creates or reuses it.
    platform_identity
        Portable operating-system and architecture identity used in package paths and
        the build fingerprint.
    toolchain_digest_prefix_length
        Explicit runtime-toolchain digest prefix length from 12 through 64.
    build_digest_prefix_length
        Explicit build digest prefix length from 12 through 64.
    """

    source_snapshot_reference: str
    source_root: Path
    toolchain_root: Path
    build_root: Path
    build_workspace_name: str
    platform_identity: str
    toolchain_digest_prefix_length: int
    build_digest_prefix_length: int

    def __post_init__(self) -> None:
        """Validate the explicit reference and lexical local roots."""
        if type(self.source_snapshot_reference) is not str:
            raise TypeError("source_snapshot_reference must be a built-in str")
        if _REFERENCE_PATTERN.fullmatch(self.source_snapshot_reference) is None:
            raise ValueError("source_snapshot_reference must be a portable identifier")
        for value, name in (
            (self.source_root, "source_root"),
            (self.toolchain_root, "toolchain_root"),
            (self.build_root, "build_root"),
        ):
            if not isinstance(value, Path):
                raise TypeError(f"{name} must be pathlib.Path")
            if not value.is_absolute() or ".." in value.parts:
                raise ValueError(f"{name} must be absolute without parent traversal")
            if any(character in value.as_posix() for character in "\x00\t\r\n"):
                raise ValueError(
                    f"{name} must not contain NUL, tab, or line terminators"
                )
        for first, second in (
            (self.source_root, self.toolchain_root),
            (self.source_root, self.build_root),
            (self.toolchain_root, self.build_root),
        ):
            if (
                first == second
                or first.is_relative_to(second)
                or second.is_relative_to(first)
            ):
                raise ValueError("source, toolchain, and build roots must be disjoint")
        if type(self.build_workspace_name) is not str:
            raise TypeError("build_workspace_name must be a built-in str")
        if _WORKSPACE_PATTERN.fullmatch(self.build_workspace_name) is None:
            raise ValueError("build_workspace_name must be a portable path component")
        if type(self.platform_identity) is not str:
            raise TypeError("platform_identity must be a built-in str")
        if _REFERENCE_PATTERN.fullmatch(self.platform_identity) is None:
            raise ValueError("platform_identity must be a portable identifier")
        for length_value, length_name in (
            (self.toolchain_digest_prefix_length, "toolchain_digest_prefix_length"),
            (self.build_digest_prefix_length, "build_digest_prefix_length"),
        ):
            if type(length_value) is not int:
                raise TypeError(f"{length_name} must be a built-in int")
            if not 12 <= length_value <= 64:
                raise ValueError(f"{length_name} must be in the inclusive range 12..64")


@dataclass(frozen=True, slots=True)
class QuantumEspressoOpenBlasComparatorBuildPlan:
    """Record the generic native plan and its non-authoritative modulefile view.

    Parameters
    ----------
    native_build_plan
        Complete execution-free native build plan.
    modulefile_path
        Profile-, runtime-toolchain-, and build-qualified proposed Lua view path.
    """

    native_build_plan: NativeBuildPlan
    modulefile_path: Path

    def __post_init__(self) -> None:
        """Validate the exact QE modulefile view path."""
        if type(self.native_build_plan) is not NativeBuildPlan:
            raise TypeError("native_build_plan must be a NativeBuildPlan")
        if not isinstance(self.modulefile_path, Path):
            raise TypeError("modulefile_path must be pathlib.Path")
        build = self.native_build_plan.build
        expected = (
            self.native_build_plan.toolchain.root
            / "modules/qe/7.2"
            / build.recipe.identity
            / f"{build.toolchain_identity}-{build.build_identity}.lua"
        )
        if self.modulefile_path != expected:
            raise ValueError("modulefile_path must match the QE build identities")


@dataclass(frozen=True, slots=True)
class QuantumEspressoOpenBlasComparatorBuildPlanner:
    """Emit the proposed isolated QE 7.2 MPI/OpenBLAS build plan.

    Parameters
    ----------
    native_build_planner
        Explicit generic planner used only to render deterministic direct CMake
        argument vectors.

    Notes
    -----
    The selected recipe fixes CMake 4.3.3; GCC C and GNU Fortran 16.1.0; Open MPI
    5.0.9 wrappers; external FFTW 3.3.11; pinned OpenBLAS 0.3.33; MPI enabled;
    OpenMP and ScaLAPACK disabled; Release configuration; no explicit floating-point
    trap or warning-suppression flags; target ``qe_pw_exe``; at most eight jobs; and
    the comparator proposal's build resource ceilings. Independent packages and the
    QE install prefix are rooted beneath the explicit toolchain root; scratch is rooted
    beneath the separate explicit build root. The root-independent ``tc-`` identity
    covers runtime dependencies, while ``build-`` additionally covers the build
    system, source reference, platform, toolchain digest, definitions, target, and
    outputs. Declared
    versions and paths except the expected OpenBLAS digest remain unauthenticated until
    a separately authorized preparation boundary observes them.
    """

    native_build_planner: NativeBuildPlanner

    def __post_init__(self) -> None:
        """Validate the exact generic planning dependency."""
        if type(self.native_build_planner) is not NativeBuildPlanner:
            raise TypeError("native_build_planner must be a NativeBuildPlanner")

    def execute(
        self,
        request: QuantumEspressoOpenBlasComparatorBuildRequest,
    ) -> QuantumEspressoOpenBlasComparatorBuildPlan:
        """Return the deterministic unexecuted comparator build plan.

        Parameters
        ----------
        request
            Explicit retained source reference and proposed isolated local roots.

        Returns
        -------
        QuantumEspressoOpenBlasComparatorBuildPlan
            Runtime-toolchain and build fingerprints, collision-adjustable identities,
            native argument vectors, and the non-authoritative modulefile view.

        Raises
        ------
        TypeError
            If ``request`` is not the exact public request type.
        """
        if type(request) is not QuantumEspressoOpenBlasComparatorBuildRequest:
            raise TypeError(
                "request must be a QuantumEspressoOpenBlasComparatorBuildRequest"
            )
        software_root = request.toolchain_root / "software"
        platform_suffix = request.platform_identity
        cmake_path = software_root / f"cmake/4.3.3-{platform_suffix}/bin/cmake"
        gcc_prefix = software_root / f"gcc/16.1.0-{platform_suffix}"
        openmpi_prefix = software_root / f"openmpi/5.0.9-gcc16.1.0-{platform_suffix}"
        openblas_prefix = software_root / f"openblas/0.3.33-gcc16.1.0-{platform_suffix}"
        fftw_prefix = software_root / f"fftw/3.3.11-gcc16.1.0-{platform_suffix}"
        openblas_path = openblas_prefix / "lib/libopenblas.dylib"
        fftw_library_path = fftw_prefix / "lib/libfftw3.dylib"
        fftw_include_path = fftw_prefix / "include"
        c_compiler_path = gcc_prefix / "bin/gcc"
        fortran_compiler_path = gcc_prefix / "bin/gfortran"
        mpi_c_wrapper_path = openmpi_prefix / "bin/mpicc"
        mpi_fortran_wrapper_path = openmpi_prefix / "bin/mpif90"
        toolchain = NativeToolchainSpecification(
            identity="gcc16-openmpi5-openblas033-fftw3311-toolchain",
            root=request.toolchain_root,
            tools=(
                NativeToolSpecification(
                    role=NativeToolRole.BLAS_LAPACK,
                    name="openblas",
                    version="0.3.33",
                    path=openblas_path,
                    content_identity=NativeToolSha256ContentIdentity(_OPENBLAS_SHA256),
                ),
                NativeToolSpecification(
                    role=NativeToolRole.BUILD_SYSTEM,
                    name="cmake",
                    version="4.3.3",
                    path=cmake_path,
                    content_identity=NativeToolContentNotPinned(),
                ),
                NativeToolSpecification(
                    role=NativeToolRole.C_COMPILER,
                    name="gcc",
                    version="16.1.0",
                    path=c_compiler_path,
                    content_identity=NativeToolContentNotPinned(),
                ),
                NativeToolSpecification(
                    role=NativeToolRole.FFT,
                    name="fftw",
                    version="3.3.11",
                    path=fftw_library_path,
                    content_identity=NativeToolContentNotPinned(),
                ),
                NativeToolSpecification(
                    role=NativeToolRole.FORTRAN_COMPILER,
                    name="gfortran",
                    version="16.1.0",
                    path=fortran_compiler_path,
                    content_identity=NativeToolContentNotPinned(),
                ),
                NativeToolSpecification(
                    role=NativeToolRole.MPI_C_WRAPPER,
                    name="openmpi-c-wrapper",
                    version="5.0.9+GCC-16.1.0",
                    path=mpi_c_wrapper_path,
                    content_identity=NativeToolContentNotPinned(),
                ),
                NativeToolSpecification(
                    role=NativeToolRole.MPI_FORTRAN_WRAPPER,
                    name="openmpi-fortran-wrapper",
                    version="5.0.9+GNU-Fortran-16.1.0",
                    path=mpi_fortran_wrapper_path,
                    content_identity=NativeToolContentNotPinned(),
                ),
            ),
        )
        fingerprint = self.native_build_planner.toolchain_fingerprinter.execute(
            toolchain
        )
        toolchain_identity = fingerprint.filesystem_identity(
            request.toolchain_digest_prefix_length
        )
        recipe = NativeBuildRecipe(
            identity="release-nontrapping",
            source_snapshot_reference=request.source_snapshot_reference,
            platform_identity=request.platform_identity,
            definitions=(
                NativeCMakeDefinition("BLAS_LIBRARIES", openblas_path.as_posix()),
                NativeCMakeDefinition("CMAKE_BUILD_TYPE", "Release"),
                NativeCMakeDefinition(
                    "CMAKE_C_COMPILER", mpi_c_wrapper_path.as_posix()
                ),
                NativeCMakeDefinition(
                    "CMAKE_Fortran_COMPILER", mpi_fortran_wrapper_path.as_posix()
                ),
                NativeCMakeDefinition("CMAKE_POLICY_VERSION_MINIMUM", "3.5"),
                NativeCMakeDefinition("FFTW3_DOUBLE", fftw_library_path.as_posix()),
                NativeCMakeDefinition(
                    "FFTW3_INCLUDE_DIRS", fftw_include_path.as_posix()
                ),
                NativeCMakeDefinition("LAPACK_LIBRARIES", openblas_path.as_posix()),
                NativeCMakeDefinition("QE_ENABLE_MPI", "ON"),
                NativeCMakeDefinition("QE_ENABLE_OPENMP", "OFF"),
                NativeCMakeDefinition("QE_ENABLE_SCALAPACK", "OFF"),
            ),
            target="qe_pw_exe",
            output_paths=(PurePosixPath("bin/pw.x"),),
        )
        build_fingerprint = self.native_build_planner.build_fingerprinter.execute(
            toolchain, fingerprint, recipe
        )
        build_identity = build_fingerprint.filesystem_identity(
            request.build_digest_prefix_length
        )
        install_prefix = (
            software_root
            / "qe/7.2"
            / toolchain_identity
            / recipe.identity
            / build_identity
        )
        scratch_build_root = (
            request.build_root
            / "qe/7.2"
            / toolchain_identity
            / build_identity
            / request.build_workspace_name
        )
        build = NativeBuildSpecification(
            recipe=recipe,
            toolchain_identity=toolchain_identity,
            build_identity=build_identity,
            source_root=request.source_root,
            build_root=scratch_build_root,
            install_prefix=install_prefix,
            limits=NativeBuildLimits(
                maximum_parallel_jobs=8,
                wall_time_milliseconds=1_800_000,
                maximum_resident_bytes=8 * 1024**3,
                maximum_output_bytes=4 * 1024**3,
            ),
        )
        native_plan = self.native_build_planner.execute(toolchain, build)
        return QuantumEspressoOpenBlasComparatorBuildPlan(
            native_build_plan=native_plan,
            modulefile_path=(
                request.toolchain_root
                / "modules/qe/7.2"
                / recipe.identity
                / f"{toolchain_identity}-{build_identity}.lua"
            ),
        )
