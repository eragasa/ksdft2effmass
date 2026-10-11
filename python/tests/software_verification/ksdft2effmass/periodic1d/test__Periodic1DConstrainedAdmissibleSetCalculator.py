"""Software verification for the executable M3 admissible-set calculation."""

from __future__ import annotations

import ast
import json
import shutil
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from ksdft2effmass.operators import ComplexMatrixQuantity, ScalarQuantity, Unitless
from ksdft2effmass.periodic1d import (
    Periodic1DAdmissibleSetDisposition,
    Periodic1DAdmissibleSetThresholds,
    Periodic1DBlockHamiltonianToyModel,
    Periodic1DConstrainedAdmissibleSetCalculationDefinition,
    Periodic1DConstrainedAdmissibleSetCalculator,
    Periodic1DConstrainedAdmissibleSetResultJsonSerializer,
    Periodic1DConstrainedAdmissibleSetResultVerifier,
    Periodic1DMultibandAlignmentCalculationDefinition,
)
from ksdft2effmass.solid_state import BlockHoppingModel1D

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DConstrainedAdmissibleSetCalculator:
    """Verify M3 composition, certificates, encoding, and retained evidence."""

    @staticmethod
    def baseline_definition() -> Periodic1DMultibandAlignmentCalculationDefinition:
        """Return a compact controlled rank-two M2 definition."""
        unit = Unitless()
        onsite = np.asarray(
            [
                [-1.20, 0.06, 0.00, 0.00],
                [0.06, -0.35, 0.00, 0.00],
                [0.00, 0.00, 1.00, 0.04],
                [0.00, 0.00, 0.04, 1.75],
            ],
            dtype=np.complex128,
        )
        positive = np.asarray(
            [
                [0.15, 0.00, 0.12, 0.00],
                [0.00, -0.10, 0.00, 0.10],
                [0.00, 0.00, 0.05, 0.00],
                [0.00, 0.00, 0.00, -0.04],
            ],
            dtype=np.complex128,
        )
        parent = Periodic1DBlockHamiltonianToyModel(
            "test.periodic1d.gapped-composite",
            BlockHoppingModel1D(
                ScalarQuantity(1.0, unit),
                (-1, 0, 1),
                (
                    ComplexMatrixQuantity(positive.conj().T, unit),
                    ComplexMatrixQuantity(onsite, unit),
                    ComplexMatrixQuantity(positive, unit),
                ),
            ),
            ScalarQuantity(1.0e-12, unit),
        )
        return Periodic1DMultibandAlignmentCalculationDefinition(
            calculation_id="m2-test",
            parent_model=parent,
            retained_rank=2,
            reciprocal_mesh_size=16,
            withheld_mesh_size=33,
            hopping_ranges=(0, 1, 2, 3),
            attack_constant_angle=0.30,
            attack_sine_coefficients=(0.65, 0.30),
            external_gap_lower_bound=ScalarQuantity(0.5, unit),
            overlap_singular_value_threshold=0.8,
            orthonormality_absolute_tolerance=1.0e-12,
            coordinate_absolute_tolerance=1.0e-14,
            reconstruction_absolute_tolerance=1.0e-12,
            hermiticity_absolute_tolerance=ScalarQuantity(1.0e-12, unit),
            verification_absolute_tolerance=1.0e-11,
        )

    @classmethod
    def definition(
        cls,
    ) -> Periodic1DConstrainedAdmissibleSetCalculationDefinition:
        """Return the compact M3 definition."""
        return Periodic1DConstrainedAdmissibleSetCalculationDefinition(
            calculation_id="m3-test",
            multiband_baseline=cls.baseline_definition(),
            energy_shift_ratio_bounds=(-0.25, 0.25),
            splitting_scale_bounds=(0.4, 1.2),
            alignment_angles=(-1.2, -0.9, -0.6, -0.3, 0.0, 0.3, 0.6, 0.9, 1.2),
            loss_energy_scale=ScalarQuantity(1.0, Unitless()),
            compatible_thresholds=Periodic1DAdmissibleSetThresholds(
                "compatible", 0.03, 0.33
            ),
            separated_thresholds=Periodic1DAdmissibleSetThresholds(
                "separated", 0.03, 0.31
            ),
            compatible_witness=(0.0, 1.0),
            locality_ranges=(0, 1, 2, 3),
            separation_resolution=0.05,
            quadratic_absolute_tolerance=1.0e-12,
            verification_absolute_tolerance=1.0e-11,
        )

    @staticmethod
    def retained_directory() -> Path:
        """Return the retained M3 package directory."""
        return (
            Path(__file__).resolve().parents[5]
            / "calculations/ICMSEP2026/conference/paper_1"
            / "constrained-admissible-sets"
        )

    def test_construction__composes_rank_two_m2_definition(self) -> None:
        """M3 composes an exact rank-two M2 definition rather than subclassing it."""
        definition = self.definition()

        assert definition.parent_model is definition.multiband_baseline.parent_model
        assert 0.3 in definition.alignment_angles
        assert definition.contains(definition.compatible_witness)

    def test_construction__composed_baseline_rejects_non_rank_two(self) -> None:
        """The composed M2 contract already closes the rank-two boundary."""
        with pytest.raises(ValueError, match="rank-two"):
            replace(self.baseline_definition(), retained_rank=1)

    def test_execution__retains_compatible_and_certified_separated_cases(
        self,
    ) -> None:
        """M3 retains a nonidentity common witness and a separation certificate."""
        result = Periodic1DConstrainedAdmissibleSetCalculator().execute(
            self.definition()
        )

        compatible, separated = result.cases
        assert compatible.disposition is (
            Periodic1DAdmissibleSetDisposition.COMPATIBLE_WITNESS
        )
        assert compatible.common_witness is not None
        assert compatible.common_witness.parameter == (0.0, 1.0)
        assert compatible.common_witness.selected_alignment_angle != 0.0
        assert separated.disposition is (
            Periodic1DAdmissibleSetDisposition.CERTIFIED_SEPARATED
        )
        assert separated.common_witness is None
        assert separated.separation_lower_bound > separated.separation_resolution
        assert separated.separation_lower_bound <= separated.separation_upper_bound

    def test_verification__independent_reconstruction_passes(self) -> None:
        """The library verifier reconstructs quadratics, witnesses, and bounds."""
        result = Periodic1DConstrainedAdmissibleSetCalculator().execute(
            self.definition()
        )

        verification = Periodic1DConstrainedAdmissibleSetResultVerifier().execute(
            result
        )

        assert verification.passes
        assert verification.dimensionless_maximum_absolute_defect < 1.0e-11
        assert verification.energy_maximum_absolute_defect.magnitude < 1.0e-11

    def test_verification__detects_tampered_withheld_diagnostic(self) -> None:
        """Evaluation-only withheld diagnostics remain independently checked."""
        result = Periodic1DConstrainedAdmissibleSetCalculator().execute(
            self.definition()
        )
        compatible = result.cases[0]
        assert compatible.common_witness is not None
        changed_witness = replace(
            compatible.common_witness,
            withheld_operator_rms_loss=(
                compatible.common_witness.withheld_operator_rms_loss + 1.0e-3
            ),
        )
        changed_case = replace(
            compatible,
            common_witness=changed_witness,
            spectral_certificate_point=changed_witness,
            operator_certificate_point=changed_witness,
        )
        tampered = replace(result, cases=(changed_case, result.cases[1]))

        verification = Periodic1DConstrainedAdmissibleSetResultVerifier().execute(
            tampered
        )

        assert not verification.passes
        assert verification.dimensionless_maximum_absolute_defect > 9.0e-4

    def test_verification__detects_tampered_evaluation_role(self) -> None:
        """Evaluation roles remain part of the independently verified contract."""
        result = Periodic1DConstrainedAdmissibleSetCalculator().execute(
            self.definition()
        )
        compatible = result.cases[0]
        assert compatible.common_witness is not None
        changed_witness = replace(compatible.common_witness, role="wrong-role")
        changed_case = replace(
            compatible,
            common_witness=changed_witness,
            spectral_certificate_point=changed_witness,
            operator_certificate_point=changed_witness,
        )
        tampered = replace(result, cases=(changed_case, result.cases[1]))

        verification = Periodic1DConstrainedAdmissibleSetResultVerifier().execute(
            tampered
        )

        assert not verification.passes
        assert verification.dimensionless_maximum_absolute_defect == 1.0

    def test_result__rejects_tampered_training_quadratic_correlation(self) -> None:
        """Result construction binds retained training values to the quadratics."""
        result = Periodic1DConstrainedAdmissibleSetCalculator().execute(
            self.definition()
        )
        separated = result.cases[1]
        changed = replace(
            separated.spectral_certificate_point,
            training_spectral_rms_loss=(
                separated.spectral_certificate_point.training_spectral_rms_loss + 1.0e-3
            ),
        )
        changed_case = replace(separated, spectral_certificate_point=changed)

        with pytest.raises(ValueError, match="training diagnostics"):
            replace(result, cases=(result.cases[0], changed_case))

    def test_result__rejects_tampered_locality_inventory(self) -> None:
        """Every parameter evaluation binds the frozen locality ranges."""
        result = Periodic1DConstrainedAdmissibleSetCalculator().execute(
            self.definition()
        )
        separated = result.cases[1]
        changed = replace(
            separated.operator_certificate_point,
            locality=separated.operator_certificate_point.locality[:-1],
        )
        changed_case = replace(separated, operator_certificate_point=changed)

        with pytest.raises(ValueError, match="locality diagnostics"):
            replace(result, cases=(result.cases[0], changed_case))

    def test_serialization__is_deterministic_and_distinct(self) -> None:
        """M3 has a deterministic schema distinct from M1 and M2."""
        result = Periodic1DConstrainedAdmissibleSetCalculator().execute(
            self.definition()
        )
        serializer = Periodic1DConstrainedAdmissibleSetResultJsonSerializer()

        first = serializer.serialize(result)
        second = serializer.serialize(result)

        assert first == second
        assert b"ksdft2effmass.periodic1d.constrained-admissible-set-result.v1" in first
        assert b'"unit":"1"' in first
        assert b'"unit":"dimensionless"' not in first

    def test_thresholds__reject_boolean(self) -> None:
        """A Boolean cannot masquerade as a numerical design threshold."""
        with pytest.raises(TypeError, match="spectral_rms_threshold"):
            Periodic1DAdmissibleSetThresholds("invalid", True, 0.31)

    def test_definition__contains_rejects_boolean_parameter(self) -> None:
        """The public domain predicate rejects Boolean numeric impostors."""
        with pytest.raises(TypeError, match=r"parameter\[0\]"):
            self.definition().contains((False, 1.0))

    def test_quadratic_loss__rejects_boolean_matrix_entry(self) -> None:
        """A Boolean cannot masquerade as a quadratic-matrix entry."""
        result = Periodic1DConstrainedAdmissibleSetCalculator().execute(
            self.definition()
        )

        with pytest.raises(TypeError, match="quadratic_matrix"):
            replace(
                result.spectral_loss,
                quadratic_matrix=((True, 0.0), (0.0, 1.0)),
            )

    def test_configuration__materializes_the_retained_input(self) -> None:
        """The human-readable configuration exactly generates input.json."""
        completed = subprocess.run(
            [sys.executable, "build_input.py", "--check"],
            cwd=self.retained_directory(),
            check=False,
            capture_output=True,
            text=True,
        )

        assert completed.returncode == 0, completed.stderr
        assert "m3_input_configuration=PASS" in completed.stdout

    def test_retained_verifier__does_not_import_producer_modules(self) -> None:
        """Standalone retained verification bypasses ksdft2effmass producers."""
        tree = ast.parse((self.retained_directory() / "verify_result.py").read_text())
        imports = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.Import | ast.ImportFrom)
        ]

        assert all(
            not (
                isinstance(node, ast.ImportFrom)
                and node.module is not None
                and node.module.startswith("ksdft2effmass")
            )
            and not (
                isinstance(node, ast.Import)
                and any(alias.name.startswith("ksdft2effmass") for alias in node.names)
            )
            for node in imports
        )

    @pytest.mark.parametrize(
        "tamper",
        (
            "definition",
            "scope",
            "threshold",
            "withheld",
            "unit",
            "quadratic-tolerance",
        ),
    )
    def test_retained_verifier__rejects_contract_tampering(
        self, tmp_path: Path, tamper: str
    ) -> None:
        """The standalone verifier binds controls, evidence roles, and units."""
        source = self.retained_directory()
        for name in ("input.json", "result.json", "verify_result.py"):
            shutil.copy2(source / name, tmp_path / name)
        input_document = json.loads((tmp_path / "input.json").read_text())
        result_document = json.loads((tmp_path / "result.json").read_text())
        if tamper == "definition":
            result_document["definition"]["alignment_angles"][0] -= 0.01
        elif tamper == "scope":
            result_document["scope"]["material_validation_included"] = True
        elif tamper == "threshold":
            input_document["separated_thresholds"]["operator_rms_threshold"] = 0.32
            result_document["definition"]["separated_thresholds"][
                "operator_rms_threshold"
            ] = 0.32
        elif tamper == "withheld":
            result_document["cases"][0]["common_witness"][
                "withheld_operator_rms_loss"
            ] += 1.0e-3
        elif tamper == "unit":
            input_document["loss_energy_scale"]["unit"] = "dimensionless"
            result_document["definition"]["loss_energy_scale"]["unit"] = "dimensionless"
        else:
            input_document["quadratic_absolute_tolerance"] = -1.0
            result_document["definition"]["quadratic_absolute_tolerance"] = -1.0
        (tmp_path / "input.json").write_text(
            json.dumps(input_document, sort_keys=True, separators=(",", ":")) + "\n"
        )
        (tmp_path / "result.json").write_text(
            json.dumps(result_document, sort_keys=True, separators=(",", ":")) + "\n"
        )

        completed = subprocess.run(
            [sys.executable, "verify_result.py"],
            cwd=tmp_path,
            check=False,
            capture_output=True,
            text=True,
        )

        assert completed.returncode != 0
        assert "ValueError" in completed.stderr
