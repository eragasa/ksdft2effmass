r"""Software verification of the finite-domain defect calculation composition.

Evidence profile: routine

The calculation entry points compose only the maintained execution-free planning
Workflow. They retain no operator result and authorize no protected execution.
"""

from __future__ import annotations

import json
import platform
import subprocess
import sys
from pathlib import Path
from typing import cast

import pytest

from ksdft2effmass.campaigns.research_monograph.impurity_defect_2d import (
    FoldingNullResult,
    FoldingNullResultJsonSerializer,
)

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestFiniteDomainEffectsCalculationComposition:
    """Own replay evidence for the maintained calculation planning package."""

    @staticmethod
    def repository_root() -> Path:
        """Return the repository root containing the calculation composition."""
        return Path(__file__).resolve().parents[7]

    @classmethod
    def calculation_root(cls) -> Path:
        """Return the maintained finite-domain defect calculation root."""
        return cls.repository_root() / "calculations/periodic2d_rank_defect"

    @classmethod
    def retained_platform(cls) -> str:
        """Return the exact platform recorded for the retained calculation."""
        path = (
            cls.calculation_root()
            / "executions/parent-qualification-v1/software-versions.json"
        )
        decoded = cast(JsonValue, json.loads(path.read_bytes()))
        if type(decoded) is not dict:
            raise AssertionError("retained software versions must be an object")
        represented = decoded.get("platform")
        if type(represented) is not str or not represented:
            raise AssertionError("retained platform identity must be a string")
        return represented

    @staticmethod
    def assert_folding_results_portably_equal(
        generated: FoldingNullResult, retained: FoldingNullResult
    ) -> None:
        """Compare exact identities and bounded binary64 replay differences."""
        assert generated.definition == retained.definition
        assert generated.failed_criteria == retained.failed_criteria
        assert len(generated.cases) == len(retained.cases)
        for generated_case, retained_case in zip(
            generated.cases, retained.cases, strict=True
        ):
            assert generated_case.case == retained_case.case
            generated_metrics = (
                generated_case.folding.unitarity_maximum_absolute_defect,
                generated_case.folding.hermiticity_maximum_absolute_defect,
                generated_case.folding.off_diagonal_maximum_absolute,
                generated_case.folding.primitive_energy_maximum_absolute_defect,
                generated_case.folding.eigenvalue_maximum_absolute_defect,
                generated_case.null_extraction.transform_unitarity_maximum_absolute_defect,
                generated_case.null_extraction.recovered_maximum_absolute_defect,
                generated_case.null_extraction.recovered_frobenius_defect,
            )
            retained_metrics = (
                retained_case.folding.unitarity_maximum_absolute_defect,
                retained_case.folding.hermiticity_maximum_absolute_defect,
                retained_case.folding.off_diagonal_maximum_absolute,
                retained_case.folding.primitive_energy_maximum_absolute_defect,
                retained_case.folding.eigenvalue_maximum_absolute_defect,
                retained_case.null_extraction.transform_unitarity_maximum_absolute_defect,
                retained_case.null_extraction.recovered_maximum_absolute_defect,
                retained_case.null_extraction.recovered_frobenius_defect,
            )
            assert generated_metrics == pytest.approx(
                retained_metrics,
                rel=0.0,
                abs=1.0e-14,
            )

    @staticmethod
    def assert_rendering_is_structurally_equivalent(
        generated: bytes, retained: bytes, suffix: str
    ) -> None:
        """Compare portable document structure without claiming byte identity."""
        if suffix == ".png":
            assert generated.startswith(b"\x89PNG\r\n\x1a\n")
            assert generated[12:16] == b"IHDR"
            assert generated[16:24] == retained[16:24]
            assert b"ksdft2effmass periodic2d_rank_defect" in generated
            assert generated.endswith(b"IEND\xaeB`\x82")
            return
        assert suffix == ".pdf"
        assert generated.startswith(b"%PDF-")
        assert generated.rstrip().endswith(b"%%EOF")
        assert generated.count(b"/Type /Page") == retained.count(b"/Type /Page")
        assert b"ksdft2effmass periodic2d_rank_defect" in generated

    def test__FiniteDomainEffectsCalculationComposition__artifact__planning_composition__reproduces_retained_package(  # noqa: E501
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-DEFECT-2D-CALCULATION-COMPOSITION-001.

        Requirement: The maintained calculation scripts reproduce and verify the
        retained execution-free planning package through public campaign APIs.

        Acceptance: Every deterministic input, result, execution, marker, and
        verification artifact is byte-identical to the retained package.
        """
        calculation_root = self.calculation_root()
        generated = tmp_path / "finite-domain-defect-planning-v1"
        subprocess.run(
            (
                sys.executable,
                str(calculation_root / "run_01_plan.py"),
                "--output-root",
                str(generated),
            ),
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            (
                sys.executable,
                str(calculation_root / "run_02_verify.py"),
                "--execution-root",
                str(generated),
            ),
            check=True,
            capture_output=True,
            text=True,
        )

        retained = calculation_root / "executions" / "finite-domain-defect-planning-v1"
        relative_paths = (
            Path("inputs/definition.json"),
            Path("results/case-inventory.json"),
            Path("execution.json"),
            Path("UNEXECUTED.md"),
            Path("verification/verification.json"),
        )
        for relative_path in relative_paths:
            assert (generated / relative_path).read_bytes() == (
                retained / relative_path
            ).read_bytes()

    def test__FiniteDomainEffectsCalculationComposition__artifact__planning_v2_composition__reproduces_small_cell_inventory(  # noqa: E501
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-DEFECT-2D-CALCULATION-COMPOSITION-004.

        Requirement: The version-2 planning scripts add 1x1 through 5x5 as explicit
        small-cell aliasing controls without modifying the retained version-1 package.

        Acceptance: Every deterministic version-2 planning and verification artifact
        is byte-identical to the retained package.
        """
        calculation_root = self.calculation_root()
        generated = tmp_path / "finite-domain-defect-planning-v2"
        subprocess.run(
            (
                sys.executable,
                str(calculation_root / "run_05_plan_finite_domain_controls.py"),
                "--output-root",
                str(generated),
            ),
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            (
                sys.executable,
                str(calculation_root / "run_06_verify_finite_domain_controls.py"),
                "--execution-root",
                str(generated),
            ),
            check=True,
            capture_output=True,
            text=True,
        )

        retained = calculation_root / "executions" / "finite-domain-defect-planning-v2"
        relative_paths = (
            Path("inputs/definition.json"),
            Path("results/case-inventory.json"),
            Path("execution.json"),
            Path("UNEXECUTED.md"),
            Path("verification/verification.json"),
        )
        for relative_path in relative_paths:
            assert (generated / relative_path).read_bytes() == (
                retained / relative_path
            ).read_bytes()

    def test__FiniteDomainEffectsCalculationComposition__artifact__folding_null_composition__reproduces_retained_package(  # noqa: E501
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-DEFECT-2D-CALCULATION-COMPOSITION-002.

        Requirement: The maintained calculation scripts reproduce and independently
        verify the authored synthetic folding/null package through public APIs.

        Acceptance: Replay on the recorded platform is byte-identical. Replay on a
        different binary64 backend preserves exact definition/case identities, passes
        independent verification, and differs from retained metrics by at most 1e-14.
        """
        calculation_root = self.calculation_root()
        generated = tmp_path / "folding-null-controls-v1"
        subprocess.run(
            (
                sys.executable,
                str(calculation_root / "run_03_folding_null_controls.py"),
                "--output-root",
                str(generated),
            ),
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            (
                sys.executable,
                str(calculation_root / "run_04_verify_folding_null_controls.py"),
                "--execution-root",
                str(generated),
            ),
            check=True,
            capture_output=True,
            text=True,
        )

        retained = calculation_root / "executions" / "folding-null-controls-v1"
        relative_paths = (
            Path("results/result.json"),
            Path("execution.json"),
            Path("UNSEALED.md"),
            Path("verification/verification.json"),
        )
        if platform.platform() == self.retained_platform():
            for relative_path in relative_paths:
                assert (generated / relative_path).read_bytes() == (
                    retained / relative_path
                ).read_bytes()
            return

        serializer = FoldingNullResultJsonSerializer()
        generated_result = serializer.deserialize(
            (generated / "results/result.json").read_bytes()
        )
        retained_result = serializer.deserialize(
            (retained / "results/result.json").read_bytes()
        )
        self.assert_folding_results_portably_equal(generated_result, retained_result)
        assert generated_result.passes
        assert (generated / "UNSEALED.md").read_bytes() == (
            retained / "UNSEALED.md"
        ).read_bytes()

    def test__FiniteDomainEffectsCalculationComposition__artifact__protocol_figure_rendering__reproduces_retained_figures(  # noqa: E501
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-DEFECT-2D-CALCULATION-COMPOSITION-003.

        Requirement: The calculation-local renderer authenticates retained scalar JSON
        evidence and creates the complete currently supportable retained/planning atlas.

        Acceptance: On the recorded rendering platform every PDF and PNG is
        byte-identical. Elsewhere each output preserves its format, dimensions/page
        count, producer identity, and complete inventory. A second invocation refuses
        to overwrite any output.
        """
        calculation_root = self.calculation_root()
        generated = tmp_path / "figures"
        command = (
            sys.executable,
            str(calculation_root / "render_research_protocol_figures.py"),
            "--output-root",
            str(generated),
        )
        subprocess.run(command, check=True, capture_output=True, text=True)

        retained = calculation_root / "figures-v3"
        stems = (
            "folding-null-residuals",
            "folding-null-metric-atlas",
            "finite-domain-inventory",
            "parent-support-collisions",
            "parent-support-equivalence-maps",
            "radius-two-core-equivalence-maps",
            "boundary-twist-mesh",
            "shape-orientation-gallery",
            "evaluation-accounting",
            "seam-oracle-phases",
            "parent-qualification-metric-atlas",
            "parent-truncation-losses",
            "parent-gauge-bridge-residuals",
            "parent-independent-reconstruction",
            "parent-resource-observation",
        )
        relative_paths = tuple(
            Path(f"{stem}.{suffix}") for stem in stems for suffix in ("pdf", "png")
        )
        for relative_path in relative_paths:
            generated_bytes = (generated / relative_path).read_bytes()
            retained_bytes = (retained / relative_path).read_bytes()
            if platform.platform() == self.retained_platform():
                assert generated_bytes == retained_bytes
            else:
                self.assert_rendering_is_structurally_equivalent(
                    generated_bytes,
                    retained_bytes,
                    relative_path.suffix,
                )

        repeated = subprocess.run(command, check=False, capture_output=True, text=True)
        assert repeated.returncode != 0
        assert "refusing to overwrite retained figure" in repeated.stderr
