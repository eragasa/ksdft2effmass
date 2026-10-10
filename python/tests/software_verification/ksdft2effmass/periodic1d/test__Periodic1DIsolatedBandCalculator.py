"""Software verification of the canonical isolated-band calculator."""

from __future__ import annotations

import ast
import json
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from ksdft2effmass.analysis.model_systems import PeriodicFourierPotential1D
from ksdft2effmass.operators import (
    PhysicalUnit,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.periodic import PeriodicModelRole
from ksdft2effmass.periodic1d import (
    Periodic1DFourierHamiltonianToyModel,
    Periodic1DIsolatedBandCalculationDefinition,
    Periodic1DIsolatedBandCalculator,
    Periodic1DIsolatedBandResultJsonSerializer,
    Periodic1DIsolatedBandResultVerifier,
)

pytestmark = pytest.mark.software_verification


class TestPeriodic1DIsolatedBandCalculator:
    """Own bounded software evidence for the new M1 calculation route."""

    @staticmethod
    def definition() -> Periodic1DIsolatedBandCalculationDefinition:
        """Return inexpensive synthetic controls with distinct sample roles."""
        unit = Unitless()
        potential = PeriodicFourierPotential1D(
            period=ScalarQuantity(2.0 * np.pi, unit),
            constant_coefficient=ScalarQuantity(0.0, unit),
            cosine_coefficients=VectorQuantity(np.asarray([0.5]), unit),
            sine_coefficients=VectorQuantity(np.asarray([0.0]), unit),
        )
        parent = Periodic1DFourierHamiltonianToyModel(
            identity="cosine-parent-software-test",
            potential=potential,
            reciprocal_vector=ScalarQuantity(1.0, unit),
            recoil_energy=ScalarQuantity(1.0, unit),
            duality_absolute_tolerance=1.0e-14,
        )
        return Periodic1DIsolatedBandCalculationDefinition(
            calculation_id="isolated-band-software-test",
            parent_model=parent,
            plane_wave_cutoffs=(1, 2),
            plane_wave_reference_cutoff=3,
            production_plane_wave_cutoff=2,
            finite_difference_points=(7, 9),
            parent_sample_reduced_momenta=(-0.5, 0.0, 0.5),
            compared_band_count=2,
            reciprocal_mesh_size=8,
            hopping_ranges=(0, 1, 2),
            withheld_mesh_size=9,
            coordinate_absolute_tolerance=1.0e-14,
            reconstruction_absolute_tolerance=1.0e-12,
            hermiticity_absolute_tolerance=ScalarQuantity(1.0e-12, unit),
            parseval_absolute_tolerance=ScalarQuantity(1.0e-12, unit),
            imaginary_absolute_tolerance=ScalarQuantity(1.0e-12, unit),
        )

    def test_execute__keeps_parent_training_and_withheld_channels_separate(
        self,
    ) -> None:
        """The calculator composes maintained Actions without historical results."""
        definition = self.definition()

        result = Periodic1DIsolatedBandCalculator().execute(definition)

        assert result.definition is definition
        assert definition.parent_model.model_role is PeriodicModelRole.TOY
        assert result.parent_reference.eigenvalues.magnitude.shape == (3, 2)
        assert result.training_target.eigenvalues.magnitude.shape == (8, 1)
        assert result.withheld_target.eigenvalues.magnitude.shape == (9, 1)
        assert set(result.training_target.coordinates.magnitude).isdisjoint(
            result.withheld_target.coordinates.magnitude
        )
        assert result.complete_transform.reconstruction_passes
        assert result.hopping_hermiticity.passes
        assert tuple(item.maximum_range for item in result.range_study) == (0, 1, 2)
        assert all(item.parseval.passes for item in result.range_study)
        assert all(item.direct_fit.is_identified for item in result.range_study)
        assert all(item.band_shape.passes for item in result.range_study)
        assert all(
            item.withheld_error.target is result.withheld_target
            for item in result.range_study
        )

    def test_retained_verifier__does_not_import_the_producer_package(self) -> None:
        """The retained reconstruction script is isolated from project generators."""
        repository_root = Path(__file__).resolve().parents[5]
        verifier_path = repository_root / (
            "calculations/ICMSEP2026/conference/paper_1/isolated-band/verify_result.py"
        )
        syntax = ast.parse(verifier_path.read_text(encoding="utf-8"))
        imported_modules = {
            alias.name
            for node in ast.walk(syntax)
            if isinstance(node, ast.Import)
            for alias in node.names
        }
        imported_modules.update(
            node.module
            for node in ast.walk(syntax)
            if isinstance(node, ast.ImportFrom) and node.module is not None
        )

        assert not any(
            module == "ksdft2effmass" or module.startswith("ksdft2effmass.")
            for module in imported_modules
        )

    def test_verifier__independently_reconstructs_calculation_channels(self) -> None:
        """Verification does not call the producer Action or retained artifacts."""
        calculation = Periodic1DIsolatedBandCalculator().execute(self.definition())

        verification = Periodic1DIsolatedBandResultVerifier().execute(calculation)

        assert verification.passes
        assert verification.diagnostics_match
        assert verification.spectral_maximum_absolute_defect.magnitude < 1.0e-12
        assert verification.hopping_maximum_absolute_defect.magnitude < 1.0e-12

    def test_serializer__uses_distinct_deterministic_schema_v1(self) -> None:
        """The prospective result cannot masquerade as historical Appendix G JSON."""
        calculation = Periodic1DIsolatedBandCalculator().execute(self.definition())
        serializer = Periodic1DIsolatedBandResultJsonSerializer()

        first = serializer.serialize(calculation)
        second = serializer.serialize(calculation)
        document = json.loads(first)

        assert first == second
        assert first.endswith(b"\n")
        assert document["schema"] == (
            "ksdft2effmass.periodic1d.isolated-band-calculation-result.v1"
        )
        assert document["scope"] == {
            "external_calculator_execution_included": False,
            "localization_included": False,
            "scientific_acceptance_included": False,
        }
        assert b"wannier_localization" not in first
        assert len(document["range_study"]) == 3

    def test_execute__is_binary64_deterministic_across_fresh_calculations(
        self,
    ) -> None:
        """A fixed eigensolver seed makes separately produced documents identical."""
        calculator = Periodic1DIsolatedBandCalculator()
        serializer = Periodic1DIsolatedBandResultJsonSerializer()

        first = serializer.serialize(calculator.execute(self.definition()))
        second = serializer.serialize(calculator.execute(self.definition()))

        assert first == second

    def test_verifier__rejects_a_tampered_convergence_observation(self) -> None:
        """Independent reconstruction detects a changed retained scalar."""
        calculation = Periodic1DIsolatedBandCalculator().execute(self.definition())
        first = calculation.plane_wave_convergence[0]
        tampered_first = replace(
            first,
            maximum_absolute_error=ScalarQuantity(
                first.maximum_absolute_error.magnitude + 1.0e-3,
                first.maximum_absolute_error.unit,
            ),
        )
        tampered = replace(
            calculation,
            plane_wave_convergence=(
                tampered_first,
                *calculation.plane_wave_convergence[1:],
            ),
        )

        verification = Periodic1DIsolatedBandResultVerifier().execute(tampered)

        assert not verification.passes
        assert verification.spectral_maximum_absolute_defect.magnitude > 9.0e-4

    def test_definition__requires_squared_energy_parseval_tolerance(self) -> None:
        """Parseval residuals cannot be labeled with unsquared energy units."""
        length = PhysicalUnit("nanometer")
        reciprocal_length = PhysicalUnit("1 / nanometer")
        energy = PhysicalUnit("electron_volt")
        potential = PeriodicFourierPotential1D(
            period=ScalarQuantity(2.0 * np.pi, length),
            constant_coefficient=ScalarQuantity(0.0, energy),
            cosine_coefficients=VectorQuantity(np.asarray([0.5]), energy),
            sine_coefficients=VectorQuantity(np.asarray([0.0]), energy),
        )
        parent = Periodic1DFourierHamiltonianToyModel(
            identity="physical-unit-boundary-test",
            potential=potential,
            reciprocal_vector=ScalarQuantity(1.0, reciprocal_length),
            recoil_energy=ScalarQuantity(1.0, energy),
            duality_absolute_tolerance=1.0e-14,
        )

        with pytest.raises(ValueError, match="squared-energy"):
            Periodic1DIsolatedBandCalculationDefinition(
                calculation_id="parseval-unit-test",
                parent_model=parent,
                plane_wave_cutoffs=(1,),
                plane_wave_reference_cutoff=2,
                production_plane_wave_cutoff=1,
                finite_difference_points=(7,),
                parent_sample_reduced_momenta=(0.0,),
                compared_band_count=1,
                reciprocal_mesh_size=8,
                hopping_ranges=(0, 1),
                withheld_mesh_size=9,
                coordinate_absolute_tolerance=1.0e-14,
                reconstruction_absolute_tolerance=1.0e-12,
                hermiticity_absolute_tolerance=ScalarQuantity(1.0e-12, energy),
                parseval_absolute_tolerance=ScalarQuantity(1.0e-12, energy),
                imaginary_absolute_tolerance=ScalarQuantity(1.0e-12, energy),
            )

    def test_definition__rejects_boolean_numeric_control(self) -> None:
        """A boolean cannot masquerade as an integer reciprocal-mesh extent."""
        definition = self.definition()

        with pytest.raises(TypeError, match="reciprocal_mesh_size"):
            Periodic1DIsolatedBandCalculationDefinition(
                calculation_id=definition.calculation_id,
                parent_model=definition.parent_model,
                plane_wave_cutoffs=definition.plane_wave_cutoffs,
                plane_wave_reference_cutoff=definition.plane_wave_reference_cutoff,
                production_plane_wave_cutoff=definition.production_plane_wave_cutoff,
                finite_difference_points=definition.finite_difference_points,
                parent_sample_reduced_momenta=(0.0,),
                compared_band_count=definition.compared_band_count,
                reciprocal_mesh_size=True,
                hopping_ranges=definition.hopping_ranges,
                withheld_mesh_size=definition.withheld_mesh_size,
                coordinate_absolute_tolerance=definition.coordinate_absolute_tolerance,
                reconstruction_absolute_tolerance=(
                    definition.reconstruction_absolute_tolerance
                ),
                hermiticity_absolute_tolerance=(
                    definition.hermiticity_absolute_tolerance
                ),
                parseval_absolute_tolerance=definition.parseval_absolute_tolerance,
                imaginary_absolute_tolerance=definition.imaginary_absolute_tolerance,
            )
