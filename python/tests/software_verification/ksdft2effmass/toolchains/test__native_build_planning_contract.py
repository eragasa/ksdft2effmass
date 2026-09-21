r"""Software verification of execution-free native build planning contract.

Evidence profile: routine

Bounded artifact scope: public immutable native-toolchain declarations, build
specifications, and deterministic CMake argument planning.

Facet and represented meaning

The artifact represents explicitly supplied tool paths, versions, content-evidence
limits, build roots, CMake definitions, outputs, and operational ceilings.

Intrinsic and cross-object scope

Tests cover public exports, immutable exact representation, ordering and confinement
invariants, role selection, and deterministic direct argument vectors.

VVUQ and scientific exclusions

These tests perform no path discovery, hashing, installation, compilation, executable
invocation, or scientific calculation. They establish software behavior only, not
availability, authorization, dependency adoption, numerical verification, scientific
validation, or uncertainty quantification.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from pathlib import Path, PurePosixPath

import pytest

import ksdft2effmass.toolchains as toolchains
from ksdft2effmass.toolchains import (
    NativeBuildFingerprint,
    NativeBuildFingerprinter,
    NativeBuildLimits,
    NativeBuildPlan,
    NativeBuildPlanner,
    NativeBuildRecipe,
    NativeBuildSpecification,
    NativeCMakeDefinition,
    NativeToolchainFingerprint,
    NativeToolchainFingerprinter,
    NativeToolchainSpecification,
    NativeToolContentNotPinned,
    NativeToolRole,
    NativeToolSha256ContentIdentity,
    NativeToolSpecification,
)

pytestmark = pytest.mark.software_verification


class TestNativeBuildPlanningContract:
    """Own maintained evidence for the cohesive native planning artifact."""

    @staticmethod
    def toolchain() -> NativeToolchainSpecification:
        """Construct one minimal immutable toolchain for this module's tests."""
        return NativeToolchainSpecification(
            identity="fixture-toolchain:1",
            root=Path("/fixture/opt"),
            tools=(
                NativeToolSpecification(
                    role=NativeToolRole.BUILD_SYSTEM,
                    name="cmake",
                    version="4.3.3",
                    path=Path("/fixture/opt/cmake"),
                    content_identity=NativeToolContentNotPinned(),
                ),
                NativeToolSpecification(
                    role=NativeToolRole.FORTRAN_COMPILER,
                    name="gfortran",
                    version="16.1.0",
                    path=Path("/fixture/opt/gfortran"),
                    content_identity=NativeToolSha256ContentIdentity("a" * 64),
                ),
            ),
        )

    @staticmethod
    def recipe() -> NativeBuildRecipe:
        """Construct the artifact-defining recipe independently of its paths."""
        return NativeBuildRecipe(
            identity="fixture-release",
            source_snapshot_reference="fixture-source:1",
            platform_identity="fixture-platform",
            definitions=(
                NativeCMakeDefinition("CMAKE_BUILD_TYPE", "Release"),
                NativeCMakeDefinition("QE_ENABLE_MPI", "ON"),
            ),
            target="qe_pw_exe",
            output_paths=(PurePosixPath("bin/pw.x"),),
        )

    @classmethod
    def build(cls) -> NativeBuildSpecification:
        """Construct one fingerprint-bound build specification for these tests."""
        toolchain_fingerprint = NativeToolchainFingerprinter(
            "native-toolchain-fingerprinter:1"
        ).execute(cls.toolchain())
        build_fingerprint = NativeBuildFingerprinter(
            "native-build-fingerprinter:1"
        ).execute(cls.toolchain(), toolchain_fingerprint, cls.recipe())
        return NativeBuildSpecification(
            recipe=cls.recipe(),
            toolchain_identity=toolchain_fingerprint.filesystem_identity(12),
            build_identity=build_fingerprint.filesystem_identity(12),
            source_root=Path("/fixture/source"),
            build_root=Path("/fixture/build"),
            install_prefix=Path("/fixture/install"),
            limits=NativeBuildLimits(
                maximum_parallel_jobs=8,
                wall_time_milliseconds=60_000,
                maximum_resident_bytes=1024,
                maximum_output_bytes=2048,
            ),
        )

    @staticmethod
    def planner() -> NativeBuildPlanner:
        """Construct the exact planning composition for this module's tests."""
        return NativeBuildPlanner(
            "native-build-planner:1",
            NativeToolchainFingerprinter("native-toolchain-fingerprinter:1"),
            NativeBuildFingerprinter("native-build-fingerprinter:1"),
        )

    def test_public_api__package__exports_planning_contract(self) -> None:
        """Evidence ID: SV-TOOLCHAIN-PLAN-001

        Requirement: The toolchains package deliberately exports the public planning
        records and ActionObject.

        Acceptance: Every asserted package attribute is the exact imported class.
        """
        assert toolchains.NativeBuildFingerprint is NativeBuildFingerprint
        assert toolchains.NativeBuildFingerprinter is NativeBuildFingerprinter
        assert toolchains.NativeBuildPlan is NativeBuildPlan
        assert toolchains.NativeBuildPlanner is NativeBuildPlanner
        assert toolchains.NativeBuildRecipe is NativeBuildRecipe
        assert toolchains.NativeBuildSpecification is NativeBuildSpecification
        assert toolchains.NativeToolchainFingerprint is NativeToolchainFingerprint
        assert toolchains.NativeToolchainFingerprinter is NativeToolchainFingerprinter
        assert toolchains.NativeToolchainSpecification is NativeToolchainSpecification

    def test_method__execute__emits_deterministic_direct_argument_vectors(self) -> None:
        """Evidence ID: SV-TOOLCHAIN-PLAN-002

        Requirement: Planning renders exact ordered CMake definitions and one bounded
        target build without shell syntax or ambient path selection.

        Acceptance: Both argument vectors equal the complete explicit literals and the
        returned plan retains the exact input objects.
        """
        toolchain = self.toolchain()
        build = self.build()

        result = self.planner().execute(toolchain, build)

        assert result.toolchain is toolchain
        assert result.build is build
        assert result.configure_argv == (
            "/fixture/opt/cmake",
            "-S",
            "/fixture/source",
            "-B",
            "/fixture/build",
            "-DCMAKE_INSTALL_PREFIX=/fixture/install",
            "-DCMAKE_BUILD_TYPE=Release",
            "-DQE_ENABLE_MPI=ON",
        )
        assert result.build_argv == (
            "/fixture/opt/cmake",
            "--build",
            "/fixture/build",
            "--target",
            "qe_pw_exe",
            "--parallel",
            "8",
        )
        assert result.toolchain_fingerprint.short_identity == "tc-599e904bf935"
        assert result.build_fingerprint.short_identity == "build-67457ea6b0f4"
        assert result.build_fingerprint.filesystem_identity(16) == (
            "build-67457ea6b0f4181b"
        )
        assert result.toolchain_manifest_path == Path(
            "/fixture/opt/toolchains/tc-599e904bf935/manifest.json"
        )
        assert "no installation" in result.claim_boundary[2]

    def test_method__tool_for__returns_exact_role_binding(self) -> None:
        """Evidence ID: SV-TOOLCHAIN-PLAN-003

        Requirement: A complete declaration exposes its exact role-indexed binding.

        Acceptance: Build-system lookup returns the retained first tool and an absent
        role raises ``ValueError``.
        """
        value = self.toolchain()

        assert value.tool_for(NativeToolRole.BUILD_SYSTEM) is value.tools[0]
        with pytest.raises(ValueError):
            value.tool_for(NativeToolRole.C_COMPILER)

    def test_constructor__tool_order__rejects_ambiguous_role_inventory(self) -> None:
        """Evidence ID: SV-TOOLCHAIN-PLAN-004

        Requirement: Tool roles are unique and lexically ordered so planning never
        depends on caller insertion order.

        Acceptance: Reversed and duplicate role inventories raise ``ValueError``.
        """
        tools = self.toolchain().tools
        with pytest.raises(ValueError):
            NativeToolchainSpecification(
                "reversed:1", Path("/fixture/opt"), tuple(reversed(tools))
            )
        with pytest.raises(ValueError):
            NativeToolchainSpecification(
                "duplicate:1", Path("/fixture/opt"), (tools[0], tools[0])
            )

    def test_constructor__build_root__rejects_source_tree_mutation_boundary(
        self,
    ) -> None:
        """Evidence ID: SV-TOOLCHAIN-PLAN-005

        Requirement: A proposed build root cannot equal or descend from its source
        root.

        Acceptance: A source-contained build path raises ``ValueError``.
        """
        with pytest.raises(ValueError):
            NativeBuildSpecification(
                recipe=self.recipe(),
                toolchain_identity=self.build().toolchain_identity,
                build_identity=self.build().build_identity,
                source_root=Path("/fixture/source"),
                build_root=Path("/fixture/source/build"),
                install_prefix=Path("/fixture/install"),
                limits=self.build().limits,
            )

    def test_constructor__semantic_types__rejects_implicit_coercion(self) -> None:
        """Evidence ID: SV-TOOLCHAIN-PLAN-006

        Requirement: Public numeric and collection boundaries reject booleans, numeric
        strings, and mutable collections.

        Acceptance: Each exact wrong-type case raises ``TypeError``.
        """
        with pytest.raises(TypeError):
            NativeBuildLimits(
                maximum_parallel_jobs=True,
                wall_time_milliseconds=60_000,
                maximum_resident_bytes=1024,
                maximum_output_bytes=2048,
            )
        with pytest.raises(TypeError):
            NativeToolchainSpecification(
                "invalid-tools:1",
                Path("/fixture/opt"),
                list(self.toolchain().tools),  # type: ignore[arg-type]
            )
        with pytest.raises(TypeError):
            NativeCMakeDefinition("COUNT", 8)  # type: ignore[arg-type]

    def test_method__execute__derives_root_independent_toolchain_identity(self) -> None:
        """Evidence ID: SV-TOOLCHAIN-PLAN-008

        Requirement: The runtime-toolchain identity depends on runtime roles,
        versions, relative paths, and content evidence rather than roots, labels, or
        build-system selection.

        Acceptance: Root relocation, relabeling, and a different CMake declaration
        retain the exact digest while a longer collision prefix is representable.
        """
        original = self.toolchain()
        relocated = NativeToolchainSpecification(
            identity="relabeled-toolchain:1",
            root=Path("/relocated/opt"),
            tools=(
                NativeToolSpecification(
                    role=NativeToolRole.BUILD_SYSTEM,
                    name="cmake",
                    version="5.0.0",
                    path=Path("/relocated/opt/other-cmake"),
                    content_identity=NativeToolContentNotPinned(),
                ),
                NativeToolSpecification(
                    role=NativeToolRole.FORTRAN_COMPILER,
                    name="gfortran",
                    version="16.1.0",
                    path=Path("/relocated/opt/gfortran"),
                    content_identity=NativeToolSha256ContentIdentity("a" * 64),
                ),
            ),
        )
        fingerprinter = NativeToolchainFingerprinter("native-toolchain-fingerprinter:1")

        original_fingerprint = fingerprinter.execute(original)
        relocated_fingerprint = fingerprinter.execute(relocated)

        assert original_fingerprint.digest == (
            "599e904bf935765afd3eae748e436ea5c72e727f93b327d1bcf607870a919724"
        )
        assert original_fingerprint.short_identity == "tc-599e904bf935"
        assert original_fingerprint.filesystem_identity(16) == "tc-599e904bf935765a"
        assert relocated_fingerprint == original_fingerprint

    def test_constructor__immutability__rejects_field_assignment(self) -> None:
        """Evidence ID: SV-TOOLCHAIN-PLAN-007

        Requirement: Toolchain and plan state remain immutable after construction.

        Acceptance: Ordinary field assignment raises ``FrozenInstanceError``.
        """
        plan = self.planner().execute(self.toolchain(), self.build())
        with pytest.raises(FrozenInstanceError):
            plan.configure_argv = ()  # type: ignore[misc]
