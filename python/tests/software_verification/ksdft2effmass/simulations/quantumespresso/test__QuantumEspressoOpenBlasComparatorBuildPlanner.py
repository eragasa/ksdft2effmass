r"""Software verification of ``QuantumEspressoOpenBlasComparatorBuildPlanner``.

Evidence profile: routine

Bounded artifact scope: the execution-free QE 7.2 release-like MPI/OpenBLAS comparator
recipe, flat HPC package prefixes, digest-bound install view, and isolated build root.

Facet and represented meaning

The planner represents the proposed compiler, MPI, BLAS/LAPACK, FFTW, QE, profile,
CMake arguments, target, outputs, and build resource ceilings.

Intrinsic and cross-object scope

Tests cover public export, flat package paths, root-independent toolchain fingerprint,
declared versions and OpenBLAS digest, configuration switches, absence of explicit
trap or warning suppression, deterministic arguments, and root separation.

VVUQ and scientific exclusions

These tests use synthetic path values and invoke no tool. They establish software
behavior only, not local availability, content verification, compilation success,
dependency adoption, protected-execution authorization, numerical verification,
scientific validation, or uncertainty quantification.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

import ksdft2effmass.simulations.quantumespresso as qe_simulations
from ksdft2effmass.simulations.quantumespresso import (
    QuantumEspressoOpenBlasComparatorBuildPlan,
    QuantumEspressoOpenBlasComparatorBuildPlanner,
    QuantumEspressoOpenBlasComparatorBuildRequest,
)
from ksdft2effmass.toolchains import (
    NativeBuildFingerprinter,
    NativeBuildPlanner,
    NativeToolchainFingerprinter,
    NativeToolRole,
    NativeToolSha256ContentIdentity,
)

pytestmark = pytest.mark.software_verification
SUT = QuantumEspressoOpenBlasComparatorBuildPlanner


class TestQuantumEspressoOpenBlasComparatorBuildPlanner:
    """Own software evidence for the execution-free QE comparator recipe."""

    @staticmethod
    def request() -> QuantumEspressoOpenBlasComparatorBuildRequest:
        """Construct the exact proposed local roots without touching them."""
        return QuantumEspressoOpenBlasComparatorBuildRequest(
            source_snapshot_reference="qe-7.2-unchanged-non-git-source-snapshot",
            source_root=Path("/Users/eugene/projects/q-e-qe-7.2"),
            toolchain_root=Path("/Users/eugene/opt"),
            build_root=Path("/Users/eugene/build"),
            build_workspace_name="20260921T014018Z",
            platform_identity="darwin-arm64",
            toolchain_digest_prefix_length=12,
            build_digest_prefix_length=12,
        )

    @staticmethod
    def planner() -> QuantumEspressoOpenBlasComparatorBuildPlanner:
        """Construct the exact generic and QE planning composition."""
        return QuantumEspressoOpenBlasComparatorBuildPlanner(
            NativeBuildPlanner(
                "native-build-planner:1",
                NativeToolchainFingerprinter("native-toolchain-fingerprinter:1"),
                NativeBuildFingerprinter("native-build-fingerprinter:1"),
            )
        )

    def test_public_api__package__exports_planner_and_request(self) -> None:
        """Evidence ID: SV-QE-TOOLCHAIN-001

        Requirement: The QE Workflow simulation package exports its recipe request and
        planner without moving generic toolchain behavior into the QE integration.

        Acceptance: All package attributes are the exact defining public classes.
        """
        assert (
            qe_simulations.QuantumEspressoOpenBlasComparatorBuildPlan
            is QuantumEspressoOpenBlasComparatorBuildPlan
        )
        assert qe_simulations.QuantumEspressoOpenBlasComparatorBuildPlanner is SUT
        assert (
            qe_simulations.QuantumEspressoOpenBlasComparatorBuildRequest
            is QuantumEspressoOpenBlasComparatorBuildRequest
        )
        assert SUT.__module__ == ("ksdft2effmass.simulations.quantumespresso.toolchain")

    def test_method__execute__maps_flat_hpc_package_prefixes(self) -> None:
        """Evidence ID: SV-QE-TOOLCHAIN-002

        Requirement: One explicit ``~/opt`` root maps independent packages into flat
        HPC-style prefixes while the digest-bound QE install and isolated scratch roots
        retain the complete toolchain identity.

        Acceptance: Every tool, fingerprint, install prefix, and scratch build root
        equals its complete literal, while root relocation preserves both digests.
        """
        result = self.planner().execute(self.request())
        native = result.native_build_plan
        assert native.toolchain.tool_for(NativeToolRole.BUILD_SYSTEM).path == Path(
            "/Users/eugene/opt/software/cmake/4.3.3-darwin-arm64/bin/cmake"
        )
        assert native.toolchain.tool_for(NativeToolRole.C_COMPILER).path == Path(
            "/Users/eugene/opt/software/gcc/16.1.0-darwin-arm64/bin/gcc"
        )
        assert native.toolchain.tool_for(NativeToolRole.FORTRAN_COMPILER).path == Path(
            "/Users/eugene/opt/software/gcc/16.1.0-darwin-arm64/bin/gfortran"
        )
        assert native.toolchain.tool_for(NativeToolRole.MPI_C_WRAPPER).path == Path(
            "/Users/eugene/opt/software/openmpi/5.0.9-gcc16.1.0-darwin-arm64/bin/mpicc"
        )
        assert native.toolchain.tool_for(
            NativeToolRole.MPI_FORTRAN_WRAPPER
        ).path == Path(
            "/Users/eugene/opt/software/openmpi/5.0.9-gcc16.1.0-darwin-arm64/bin/mpif90"
        )
        assert native.toolchain.tool_for(NativeToolRole.BLAS_LAPACK).path == Path(
            "/Users/eugene/opt/software/openblas/"
            "0.3.33-gcc16.1.0-darwin-arm64/lib/libopenblas.dylib"
        )
        assert native.toolchain.tool_for(NativeToolRole.FFT).path == Path(
            "/Users/eugene/opt/software/fftw/"
            "3.3.11-gcc16.1.0-darwin-arm64/lib/libfftw3.dylib"
        )
        assert native.toolchain_fingerprint.digest == (
            "209554acf35707dd399ce23b63cc32df7637dea42559cc9fdb209a5ef71ed53a"
        )
        assert native.toolchain_fingerprint.short_identity == "tc-209554acf357"
        assert native.build_fingerprint.digest == (
            "4d16ca31ba0f9bfa07043a7771a45a3a61bf4f54b2a53084303169e2d10de0c1"
        )
        assert native.build_fingerprint.short_identity == "build-4d16ca31ba0f"
        assert native.toolchain_manifest_path == Path(
            "/Users/eugene/opt/toolchains/tc-209554acf357/manifest.json"
        )
        assert native.build.install_prefix == Path(
            "/Users/eugene/opt/software/qe/7.2/tc-209554acf357/"
            "release-nontrapping/build-4d16ca31ba0f"
        )
        assert native.build.build_root == Path(
            "/Users/eugene/build/qe/7.2/tc-209554acf357/"
            "build-4d16ca31ba0f/20260921T014018Z"
        )
        assert result.modulefile_path == Path(
            "/Users/eugene/opt/modules/qe/7.2/release-nontrapping/"
            "tc-209554acf357-build-4d16ca31ba0f.lua"
        )

        relocated = (
            self.planner()
            .execute(
                replace(
                    self.request(),
                    toolchain_root=Path("/Volumes/opt"),
                    build_root=Path("/Volumes/build"),
                )
            )
            .native_build_plan
        )
        assert relocated.toolchain_fingerprint == native.toolchain_fingerprint
        assert relocated.build_fingerprint == native.build_fingerprint

    def test_method__execute__retains_exact_versions_and_openblas_digest(self) -> None:
        """Evidence ID: SV-QE-TOOLCHAIN-003

        Requirement: The recipe retains every selected tool version and the checkpoint
        OpenBLAS byte-identity expectation without claiming other bytes are pinned.

        Acceptance: Role-indexed versions and the OpenBLAS digest equal the explicit
        retained values.
        """
        toolchain = self.planner().execute(self.request()).native_build_plan.toolchain
        openblas = toolchain.tool_for(NativeToolRole.BLAS_LAPACK)

        assert toolchain.tool_for(NativeToolRole.BUILD_SYSTEM).version == "4.3.3"
        assert toolchain.tool_for(NativeToolRole.C_COMPILER).version == "16.1.0"
        assert toolchain.tool_for(NativeToolRole.FORTRAN_COMPILER).version == "16.1.0"
        assert toolchain.tool_for(NativeToolRole.MPI_C_WRAPPER).version == (
            "5.0.9+GCC-16.1.0"
        )
        assert toolchain.tool_for(NativeToolRole.MPI_FORTRAN_WRAPPER).version == (
            "5.0.9+GNU-Fortran-16.1.0"
        )
        assert openblas.version == "0.3.33"
        assert isinstance(openblas.content_identity, NativeToolSha256ContentIdentity)
        assert openblas.content_identity.digest == (
            "dbd757cdfffbff1dc72fbf34983e89d5710933d04783f950441a57522fbf769d"
        )
        assert toolchain.tool_for(NativeToolRole.FFT).version == "3.3.11"

    def test_method__execute__emits_release_nontrapping_mpi_plan(self) -> None:
        """Evidence ID: SV-QE-TOOLCHAIN-004

        Requirement: The planned QE build is Release, MPI-enabled, OpenMP- and
        ScaLAPACK-disabled, external-FFTW/OpenBLAS-linked, and contains no explicit
        floating-point trap or warning-suppression flag.

        Acceptance: Exact definitions, target, output, jobs, and resource ceilings
        agree, while no argument contains ``ffpe`` or ``summary``.
        """
        result = self.planner().execute(self.request()).native_build_plan
        arguments = result.configure_argv

        assert "-DCMAKE_BUILD_TYPE=Release" in arguments
        assert (
            "-DCMAKE_C_COMPILER=/Users/eugene/opt/software/openmpi/"
            "5.0.9-gcc16.1.0-darwin-arm64/bin/mpicc"
        ) in arguments
        assert (
            "-DCMAKE_Fortran_COMPILER=/Users/eugene/opt/software/openmpi/"
            "5.0.9-gcc16.1.0-darwin-arm64/bin/mpif90"
        ) in arguments
        assert (
            "-DCMAKE_INSTALL_PREFIX=/Users/eugene/opt/software/qe/7.2/"
            "tc-209554acf357/release-nontrapping/build-4d16ca31ba0f"
        ) in arguments
        assert "-DQE_ENABLE_MPI=ON" in arguments
        assert "-DQE_ENABLE_OPENMP=OFF" in arguments
        assert "-DQE_ENABLE_SCALAPACK=OFF" in arguments
        assert not any("ffpe" in argument.lower() for argument in arguments)
        assert not any("summary" in argument.lower() for argument in arguments)
        assert result.build.recipe.target == "qe_pw_exe"
        assert tuple(path.as_posix() for path in result.build.recipe.output_paths) == (
            "bin/pw.x",
        )
        assert result.build.limits.maximum_parallel_jobs == 8
        assert result.build.limits.wall_time_milliseconds == 1_800_000
        assert result.build.limits.maximum_resident_bytes == 8 * 1024**3
        assert result.build.limits.maximum_output_bytes == 4 * 1024**3

    def test_constructor__toolchain_root__rejects_source_tree_nesting(self) -> None:
        """Evidence ID: SV-QE-TOOLCHAIN-005

        Requirement: The maintained toolchain root cannot equal or descend from the
        retained QE source tree.

        Acceptance: A source-contained toolchain root raises ``ValueError``.
        """
        with pytest.raises(ValueError):
            QuantumEspressoOpenBlasComparatorBuildRequest(
                source_snapshot_reference="qe-source:1",
                source_root=Path("/Users/eugene/projects/q-e-qe-7.2"),
                toolchain_root=Path("/Users/eugene/projects/q-e-qe-7.2/toolchain"),
                build_root=Path("/Users/eugene/build"),
                build_workspace_name="20260921T014018Z",
                platform_identity="darwin-arm64",
                toolchain_digest_prefix_length=12,
                build_digest_prefix_length=12,
            )

    def test_method__execute__retains_execution_free_claim_boundary(self) -> None:
        """Evidence ID: SV-QE-TOOLCHAIN-006

        Requirement: Emitting the comparator plan cannot represent installation,
        compilation, dependency adoption, authorization, or scientific evidence.

        Acceptance: The returned claim boundary names all prohibited interpretations.
        """
        claim_boundary = (
            self.planner().execute(self.request()).native_build_plan.claim_boundary
        )

        assert any("no installation" in claim for claim in claim_boundary)
        assert any("no execution authorization" in claim for claim in claim_boundary)
        assert any("no numerical verification" in claim for claim in claim_boundary)
