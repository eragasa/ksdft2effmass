"""Fail-closed ownership checks for periodic-3D rank-N protocols."""

from __future__ import annotations

from pathlib import Path

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestPeriodic3DRankNProtocols:
    """Keep the periodic-3D calculation and software boundaries fail-closed."""

    def test_calculation_owned_decision_register_is_dimension_specific(
        self,
        repository_root: Path,
    ) -> None:
        record = (
            repository_root
            / "calculations"
            / "periodic3d"
            / "rankN"
            / "protocol-selection.md"
        ).read_text(encoding="utf-8")

        for phrase in (
            "AGGREGATE VERIFICATION INSTALLED",
            "VISUALIZATION AND LIFECYCLE PENDING",
            "EXECUTION NOT AUTHORIZED",
            "`3`, `4`, and `8`",
            "`1`, `2`, and `4`",
            "UNSELECTED",
            "No execution is\nauthorized",
            "Rank four remains a value of rank-N",
            "2 * retained_rank",
            "complete global-unitary Procrustes",
            "`Periodic3DRank2...` operation owners then refine",
            "does not inherit rank-two calculation policy",
            "INSTALLED WITH TYPED AGGREGATE VERIFICATION",
            "Visualization projection",
            "VISUALIZATION-BOUND SCHEMAS PENDING",
            "Periodic3DRankN",
        ):
            assert phrase in record
        assert "three primitive neighbor directions" in record.lower()
        assert "all three primitive-axis-pair plaquette families" in record.lower()

    def test_recommended_baseline_defines_rank_general_analytic_controls(
        self,
        repository_root: Path,
    ) -> None:
        record = (
            repository_root
            / "calculations"
            / "periodic3d"
            / "rankN"
            / "recommended-baseline.md"
        ).read_text(encoding="utf-8")

        for phrase in (
            "AUTHORIZED SOFTWARE BASELINE",
            "IMPLEMENTATION IN PROGRESS; EXECUTION NOT AUTHORIZED",
            "external-gap lower bound `1.9`",
            "global-unitary",
            "pointwise-unitary",
            "known-inverse-oracle",
            "`Periodic3DRank2...` operation owners refine them",
            "does not transfer rank-two calculation policy",
            "does not authorize execution or retained evidence",
            "construction size `8`",
            "evaluation size `17`",
            "all three primitive-axis-pair plaquette",
        ):
            assert phrase in record
        assert "2 * retained_rank" not in record

    def test_package_namespace_installs_reviewed_aggregate_foundation(
        self,
        repository_root: Path,
    ) -> None:
        rank_root = (
            repository_root
            / "python"
            / "src"
            / "ksdft2effmass"
            / "periodic3d"
            / "rankN"
        )
        initializer = (rank_root / "__init__.py").read_text(encoding="utf-8")

        assert initializer.strip().startswith('"""')
        assert "import " not in initializer
        assert "class " not in initializer
        assert (rank_root / "gauge_alignment" / "procrustes" / "analysis.py").is_file()
        assert (
            rank_root / "band_alignment" / "frame_transport" / "analysis.py"
        ).is_file()
        assert (rank_root / "hopping_locality" / "analysis.py").is_file()
        assert (rank_root / "support_truncation" / "analysis.py").is_file()
        assert (rank_root / "bain_quotient_admission.py").is_file()
        aggregate_root = rank_root / "band_equivalence_hopping_locality"
        for filename in (
            "case.py",
            "request.py",
            "analysis.py",
            "result.py",
            "reference.py",
            "fourier_reference.py",
            "verification.py",
        ):
            assert (aggregate_root / filename).is_file()
        assert not (aggregate_root / "case_expansion.py").exists()
        assert not (aggregate_root / "model.py").exists()
        assert not (aggregate_root / "parent.py").exists()
        assert not (aggregate_root / "lifecycle.py").exists()
        assert (
            repository_root
            / "python"
            / "tests"
            / "periodic3d_rankn_analytic_case_support.py"
        ).is_file()

    def test_bain_context_records_geometry_and_blockers_without_execution(
        self,
        repository_root: Path,
    ) -> None:
        context = repository_root / "calculations" / "periodic3d_rankN_bain_path"
        required_directories = (
            "gauge_alignment",
            "frame_transport",
            "band_equivalence",
            "hopping_locality",
            "support_truncation",
            "band_equivalence_hopping_locality",
        )
        decision_record = (context / "protocol-selection.md").read_text(
            encoding="utf-8"
        )
        geometry_record = (context / "geometry-common-state-space.md").read_text(
            encoding="utf-8"
        )
        m0_record = (context / "m0-geometry-only-control.md").read_text(
            encoding="utf-8"
        )
        tex_protocol = (context / "research-protocol.tex").read_text(encoding="utf-8")

        assert (context / "README.md").is_file()
        for directory in required_directories:
            assert (context / directory / "README.md").is_file()

        for phrase in (
            "FULL SCIENTIFIC PROTOCOL UNSELECTED",
            "M1N — frozen `2r`-state analytic-parent response control",
            "m1n-frozen-2r-state-analytic-parent",
            "Rank-two M1 retains\nits four-state identity",
            "`(3, 4, 8)`",
            "`(1, 2, 4)`",
            "Resource envelope",
            "Visualization projection",
            "No-overwrite identity",
            "N2 = N3",
            "N1` dividing `N2",
            "actual period triple",
            "must contain no calculation",
        ):
            assert phrase in decision_record

        for phrase in (
            "SELECTED GEOMETRY/STATE-SPACE SUBPROTOCOL",
            "synthetic-bain-direct-length-v1",
            "s\\in[0,1]",
            "\\det A_B(s)=\\ell_0^3",
            "A_B(0)=A_FU",
            "\\det U=1",
            "\\mathbf q_B=U^\\mathsf T\\mathbf q_F",
            "U\\tau_B^\\alpha=\\tau_F^\\alpha",
            "without sign canonicalization",
            "\\ell^2(\\mathbb Z^3)\\otimes\\mathbb C^{2r}",
            "FINITE_QUOTIENT_INCOMPATIBLE",
            "projectkoios-formal` PR 58",
            "b98d23fe23bb5bc940c6be4cfcbc79c3569c45e7",
            "bainMixedModuliAdmissionCertificate_iff",
            "N_2=N_3",
            "N_1\\mid N_2",
            "(2,6,6)",
            "(4,6,6)",
            "does not select a mesh",
            "COMMON_STATE_SPACE_IDENTITY_FAILED",
        ):
            assert phrase in geometry_record

        for phrase in (
            "SELECTED SCIENTIFIC SUBPROTOCOL",
            "shared `2r` flat specialization",
            "parameter-free `lambda=0` specialization",
            "=2.7-0.4=2.3",
            "M0_FROZEN_OPERATOR_IDENTITY_FAILED",
            "INAPPLICABLE_NO_ADMITTED_M0_CASE",
            "INAPPLICABLE_POLICY_NOT_SELECTED",
        ):
            assert phrase in m0_record

        for phrase in (
            "\\documentclass[11pt]{article}",
            "Periodic-3D rank-N synthetic Bain geometry",
            "synthetic-bain-direct-length-v1",
            "=2.7-0.4=2.3",
            "Selected M1N frozen-parent control",
            "bainMixedModuliAdmissionCertificate",
            "b98d23fe23bb5bc940c6be4cfcbc79c3569c45e7",
            "does not select or authenticate a mesh",
            "does not select M2",
            "no execution authority",
        ):
            assert phrase in tex_protocol

        assert not list(context.rglob("*.py"))
        assert not list(context.rglob("*.json"))
        assert not list(context.rglob("*.pdf"))
        assert not list(context.rglob("*.png"))
        for forbidden_directory in ("analysis", "simulations", "executions"):
            assert not (context / forbidden_directory).exists()

        rankn_index = (
            repository_root / "calculations" / "periodic3d" / "rankN" / "README.md"
        ).read_text(encoding="utf-8")
        assert "periodic3d_rankN_bain_path" in rankn_index
        assert "does **not** select a continuous synthetic-strain" in rankn_index
        assert "proof obligation also remains fail-closed" not in (
            context / "README.md"
        ).read_text(encoding="utf-8")

    def test_calculation_root_has_no_direct_entrypoints_or_rank4_namespace(
        self,
        repository_root: Path,
    ) -> None:
        calculation_root = repository_root / "calculations" / "periodic3d" / "rankN"

        assert calculation_root.is_dir()
        assert not list(calculation_root.rglob("run_01_calculation.py"))
        assert not list(calculation_root.rglob("run_02_verification.py"))
        assert not list(calculation_root.rglob("run_03_render.py"))
        assert not (repository_root / "calculations" / "periodic3d" / "rank4").exists()
        assert not (
            repository_root
            / "python"
            / "src"
            / "ksdft2effmass"
            / "periodic3d"
            / "rank4"
        ).exists()
