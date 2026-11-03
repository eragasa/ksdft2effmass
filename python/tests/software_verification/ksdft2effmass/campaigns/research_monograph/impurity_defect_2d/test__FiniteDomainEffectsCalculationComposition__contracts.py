r"""Software verification of the finite-domain defect calculation composition.

Evidence profile: routine

The calculation entry points compose only the maintained execution-free planning
Workflow. They retain no operator result and authorize no protected execution.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

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

        Acceptance: Result, execution, marker, and verification artifacts are
        byte-identical to the retained no-overwrite package.
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
        for relative_path in relative_paths:
            assert (generated / relative_path).read_bytes() == (
                retained / relative_path
            ).read_bytes()

    def test__FiniteDomainEffectsCalculationComposition__artifact__protocol_figure_rendering__reproduces_retained_figures(  # noqa: E501
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-DEFECT-2D-CALCULATION-COMPOSITION-003.

        Requirement: The calculation-local renderer authenticates retained scalar JSON
        evidence and creates the complete currently supportable retained/planning atlas.

        Acceptance: Every version-three PDF and PNG is byte-identical to the retained
        rendering, and a second invocation refuses to overwrite them.
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
            assert (generated / relative_path).read_bytes() == (
                retained / relative_path
            ).read_bytes()

        repeated = subprocess.run(command, check=False, capture_output=True, text=True)
        assert repeated.returncode != 0
        assert "refusing to overwrite retained figure" in repeated.stderr
