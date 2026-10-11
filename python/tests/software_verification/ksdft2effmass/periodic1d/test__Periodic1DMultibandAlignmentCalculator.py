"""Software verification for the executable M2 calculation."""

from __future__ import annotations

import ast
import json
import shutil
import subprocess
import sys
from dataclasses import FrozenInstanceError, replace
from pathlib import Path

import numpy as np
import pytest

from ksdft2effmass.operators import ComplexMatrixQuantity, ScalarQuantity, Unitless
from ksdft2effmass.periodic1d import (
    Periodic1DBlockHamiltonianToyModel,
    Periodic1DMultibandAlignmentCalculationDefinition,
    Periodic1DMultibandAlignmentCalculator,
    Periodic1DMultibandAlignmentResultJsonSerializer,
    Periodic1DMultibandAlignmentResultVerifier,
)
from ksdft2effmass.solid_state import BlockHoppingModel1D

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DMultibandAlignmentCalculator:
    """Verify executable M2 calculation and retained-evidence contracts."""

    @staticmethod
    def definition() -> Periodic1DMultibandAlignmentCalculationDefinition:
        """Return the compact controlled rank-two M2 definition."""
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
        parent_hoppings = BlockHoppingModel1D(
            ScalarQuantity(1.0, unit),
            (-1, 0, 1),
            (
                ComplexMatrixQuantity(positive.conj().T, unit),
                ComplexMatrixQuantity(onsite, unit),
                ComplexMatrixQuantity(positive, unit),
            ),
        )
        parent = Periodic1DBlockHamiltonianToyModel(
            "test.periodic1d.gapped-composite",
            parent_hoppings,
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

    def test_execution__m2__separates_pointwise_and_global_alignment(self) -> None:
        """Pointwise recovery succeeds while one global unitary remains limited."""
        result = Periodic1DMultibandAlignmentCalculator().execute(self.definition())

        assert result.diagnostics.external_gap_minimum.magnitude > 0.5
        assert result.diagnostics.attack_frame_maximum_frobenius_defect > 0.5
        assert (
            result.diagnostics.pointwise_alignment.frame_maximum_frobenius_defect
            < 1.0e-12
        )
        assert (
            result.diagnostics.pointwise_rotation_recovery_maximum_frobenius_defect
            < 1.0e-12
        )
        assert result.diagnostics.constrained_frame_maximum_frobenius_defect > 0.5
        assert (
            result.range_study[-1].attacked_truncation.omitted_block_l2_norm
            > result.range_study[-1].reference_truncation.omitted_block_l2_norm
        )

    def test_verification__m2__independent_reconstruction_passes(self) -> None:
        """The independent M2 verifier reconstructs every retained channel."""
        result = Periodic1DMultibandAlignmentCalculator().execute(self.definition())

        verification = Periodic1DMultibandAlignmentResultVerifier().execute(result)

        assert verification.passes
        assert verification.dimensionless_maximum_absolute_defect < 1.0e-11
        assert verification.energy_maximum_absolute_defect.magnitude < 1.0e-11

    def test_serialization__m2__is_deterministic_and_distinct(self) -> None:
        """M2 uses its own deterministic result identity."""
        result = Periodic1DMultibandAlignmentCalculator().execute(self.definition())
        serializer = Periodic1DMultibandAlignmentResultJsonSerializer()

        first = serializer.serialize(result)
        second = serializer.serialize(result)

        assert first == second
        assert (
            b"ksdft2effmass.periodic1d.multiband-alignment-calculation-result.v1"
            in first
        )

    def test_execution__m2__is_binary64_deterministic(self) -> None:
        """Separately produced M2 documents are byte-identical."""
        serializer = Periodic1DMultibandAlignmentResultJsonSerializer()
        calculator = Periodic1DMultibandAlignmentCalculator()

        first = serializer.serialize(calculator.execute(self.definition()))
        second = serializer.serialize(calculator.execute(self.definition()))

        assert first == second

    def test_verification__m2__detects_tampered_alignment_diagnostic(self) -> None:
        """Independent reconstruction detects a changed retained frame value."""
        result = Periodic1DMultibandAlignmentCalculator().execute(self.definition())
        diagnostics = replace(
            result.diagnostics,
            constrained_frame_maximum_frobenius_defect=(
                result.diagnostics.constrained_frame_maximum_frobenius_defect + 1.0e-3
            ),
        )
        tampered = replace(result, diagnostics=diagnostics)

        verification = Periodic1DMultibandAlignmentResultVerifier().execute(tampered)

        assert not verification.passes
        assert verification.dimensionless_maximum_absolute_defect > 9.0e-4

    def test_verification__m2__detects_tampered_hermiticity(self) -> None:
        """The library verifier reconstructs every retained Hermiticity channel."""
        result = Periodic1DMultibandAlignmentCalculator().execute(self.definition())
        diagnostic = result.reference_hermiticity
        changed = replace(
            diagnostic,
            maximum_frobenius_defect=ScalarQuantity(1.0e-3, Unitless()),
            passes=False,
        )
        tampered = replace(result, reference_hermiticity=changed)

        verification = Periodic1DMultibandAlignmentResultVerifier().execute(tampered)

        assert not verification.passes
        assert verification.energy_maximum_absolute_defect.magnitude > 9.0e-4

    def test_retained_verifier__m2__does_not_import_producer_modules(self) -> None:
        """Standalone retained verification bypasses ksdft2effmass producers."""
        path = (
            Path(__file__).resolve().parents[5]
            / "calculations/ICMSEP2026/conference/paper_1/multiband-alignment"
            / "verify_result.py"
        )
        tree = ast.parse(path.read_text())
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
        ("definition", "external-gap", "overlap", "hermiticity"),
    )
    def test_retained_verifier__m2__rejects_contract_tampering(
        self, tmp_path: Path, tamper: str
    ) -> None:
        """The standalone verifier binds frozen controls and Hermiticity evidence."""
        source = (
            Path(__file__).resolve().parents[5]
            / "calculations/ICMSEP2026/conference/paper_1/multiband-alignment"
        )
        for name in ("input.json", "result.json", "verify_result.py"):
            shutil.copy2(source / name, tmp_path / name)
        input_document = json.loads((tmp_path / "input.json").read_text())
        result_document = json.loads((tmp_path / "result.json").read_text())
        definition = result_document["definition"]
        if tamper == "definition":
            definition["reciprocal_mesh_size"] += 1
        elif tamper == "external-gap":
            input_document["external_gap_lower_bound"]["magnitude"] = 2.0
            definition["external_gap_lower_bound"]["magnitude"] = 2.0
        elif tamper == "overlap":
            input_document["overlap_singular_value_threshold"] = 0.99999
            definition["overlap_singular_value_threshold"] = 0.99999
        else:
            hermiticity = result_document["complete_transforms"]["reference"][
                "hermiticity"
            ]
            hermiticity["maximum_frobenius_defect"]["magnitude"] = 1.0e-3
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

    def test_definition__m2__permits_identity_attack_for_generic_use(self) -> None:
        """Only the retained M2 instance, not the generic type, claims nonidentity."""
        definition = replace(
            self.definition(),
            attack_constant_angle=0.0,
            attack_sine_coefficients=(0.0, 0.0),
        )

        assert definition.attack_constant_angle == 0.0
        assert definition.attack_sine_coefficients == (0.0, 0.0)

    def test_construction__m2_result__binds_transport_threshold(self) -> None:
        """Manually assembled results must preserve definition correlations."""
        result = Periodic1DMultibandAlignmentCalculator().execute(self.definition())
        transport = replace(
            result.diagnostics.transport,
            overlap_singular_value_threshold=0.7,
        )
        diagnostics = replace(result.diagnostics, transport=transport)

        with pytest.raises(ValueError, match="overlap threshold does not match"):
            replace(result, diagnostics=diagnostics)

    def test_definition__m2__rejects_boolean_mesh_extent(self) -> None:
        """A Boolean cannot masquerade as a reciprocal-mesh integer."""
        definition = self.definition()

        with pytest.raises(TypeError, match="reciprocal_mesh_size"):
            replace(definition, reciprocal_mesh_size=True)

    def test_mutation__m2_definition__raises_frozen_instance_error(self) -> None:
        """The prospectively frozen calculation definition is immutable."""
        definition = self.definition()

        with pytest.raises(FrozenInstanceError):
            definition.calculation_id = "changed"  # type: ignore[misc]
