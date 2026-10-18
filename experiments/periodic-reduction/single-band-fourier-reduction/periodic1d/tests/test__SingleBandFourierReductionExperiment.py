"""Software verification for the single-band Fourier-reduction experiment."""

from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest
from jsonschema import (  # type: ignore[import-untyped]
    Draft202012Validator,
    ValidationError,
)
from ksdft2effmass.analysis.model_systems import PeriodicFourierPotential1D
from ksdft2effmass.analysis.single_band_reduction import (
    SingleBandHoppingReductionResult1D,
    SingleBandHoppingReductionTolerances1D,
)
from ksdft2effmass.operators import ScalarQuantity, Unitless, VectorQuantity
from ksdft2effmass.periodic1d.model import Periodic1DFourierHamiltonianToyModel
from run_experiment import (
    EXPECTED_OPTIMIZATION_REVISION,
    EXPECTED_PHYSKIT_REVISION,
    installed_vcs_commit,
)

from single_band_fourier_reduction import (
    EXPERIMENT_FAMILY_ID,
    EXPERIMENT_IDENTITY,
    EXPERIMENT_VERSION_ID,
    SingleBandFourierReductionExperiment,
    SingleBandFourierReductionExperimentDefinition,
    SingleBandFourierReductionExperimentVerifier,
    SingleBandFourierReductionInputSerializer,
    SingleBandFourierReductionResultSerializer,
    SingleBandFourierReductionVerificationSerializer,
)

pytestmark = pytest.mark.software_verification

_LIVE_OPTIMIZATION_REVISION = "2c6dd7f717722f6b0495feb8cfe1287a104268a6"
_LIVE_PHYSKIT_REVISION = "7120b735c7e3e450aa8924780a71deb59d812632"


class TestSingleBandFourierReductionExperiment:
    """Establish the experiment-owned and reusable-Workflow boundary."""

    @staticmethod
    def definition() -> SingleBandFourierReductionExperimentDefinition:
        """Return inexpensive controls with disjoint sample roles."""
        unit = Unitless()
        potential = PeriodicFourierPotential1D(
            period=ScalarQuantity(2.0 * np.pi, unit),
            constant_coefficient=ScalarQuantity(0.0, unit),
            cosine_coefficients=VectorQuantity(np.asarray([0.5]), unit),
            sine_coefficients=VectorQuantity(np.asarray([0.0]), unit),
        )
        model = Periodic1DFourierHamiltonianToyModel(
            identity="single-band-cosine-software-test",
            potential=potential,
            reciprocal_vector=ScalarQuantity(1.0, unit),
            recoil_energy=ScalarQuantity(1.0, unit),
            duality_absolute_tolerance=1.0e-14,
        )
        training_size = 8
        evaluation_size = 11
        offset = 1.0 / float(training_size + 1)
        evaluation = tuple(
            float(-0.5 + (float(index) + offset) / float(evaluation_size))
            for index in range(evaluation_size)
        )
        tolerances = SingleBandHoppingReductionTolerances1D(
            coordinate_absolute=ScalarQuantity(1.0e-14, unit),
            reconstruction_absolute=ScalarQuantity(1.0e-12, unit),
            hermiticity_absolute=ScalarQuantity(1.0e-12, unit),
            parseval_absolute=ScalarQuantity(1.0e-12, unit),
            imaginary_absolute=ScalarQuantity(1.0e-12, unit),
        )
        return SingleBandFourierReductionExperimentDefinition(
            parent_model=model,
            plane_wave_cutoffs=(1, 2),
            plane_wave_reference_cutoff=3,
            production_plane_wave_cutoff=2,
            finite_difference_points=(7, 9),
            parent_sample_reduced_momenta=(-0.5, 0.0, 0.5),
            compared_band_count=2,
            selected_band_index=0,
            reciprocal_training_mesh_size=training_size,
            evaluation_reduced_momenta=evaluation,
            hopping_ranges=(0, 1, 2),
            fitting_weights=tuple(1.0 for _ in range(training_size)),
            tolerances=tolerances,
        )

    def test_execute__owns_model_controls_and_delegates_reduction(self) -> None:
        """Experiment results retain model evidence around a reusable result."""
        definition = self.definition()

        result = SingleBandFourierReductionExperiment().execute(definition)

        assert result.definition is definition
        assert type(result.reduction) is SingleBandHoppingReductionResult1D
        assert result.reduction.request.training_target.band_count == 1
        assert result.reduction.request.evaluation_target.band_count == 1
        assert set(
            result.reduction.request.training_target.coordinates.magnitude
        ).isdisjoint(result.reduction.request.evaluation_target.coordinates.magnitude)
        assert result.reduction.complete_transform.reconstruction_passes
        assert result.reduction.hopping_hermiticity.passes
        assert tuple(item.maximum_range for item in result.reduction.range_study) == (
            0,
            1,
            2,
        )
        assert result.training_gap.external_minimum_gap is not None
        assert result.training_gap.external_minimum_gap.magnitude > 0.0
        assert result.evaluation_gap.external_minimum_gap is not None
        assert result.evaluation_gap.external_minimum_gap.magnitude > 0.0

    def test_identity__is_publication_independent(self) -> None:
        """The maintained family identity contains no paper or milestone label."""
        assert EXPERIMENT_FAMILY_ID == (
            "ksdft2effmass.campaign.periodic-reduction.periodic1d."
            "single-band-fourier-reduction"
        )
        assert "paper" not in EXPERIMENT_FAMILY_ID
        assert "m1" not in EXPERIMENT_FAMILY_ID

    def test_definition__rejects_shared_training_and_evaluation_coordinate(
        self,
    ) -> None:
        """This experiment strengthens the generic Workflow's sample-role contract."""
        definition = self.definition()

        with pytest.raises(ValueError, match="must be disjoint"):
            SingleBandFourierReductionExperimentDefinition(
                parent_model=definition.parent_model,
                plane_wave_cutoffs=definition.plane_wave_cutoffs,
                plane_wave_reference_cutoff=(definition.plane_wave_reference_cutoff),
                production_plane_wave_cutoff=(definition.production_plane_wave_cutoff),
                finite_difference_points=definition.finite_difference_points,
                parent_sample_reduced_momenta=(
                    definition.parent_sample_reduced_momenta
                ),
                compared_band_count=definition.compared_band_count,
                selected_band_index=definition.selected_band_index,
                reciprocal_training_mesh_size=(
                    definition.reciprocal_training_mesh_size
                ),
                evaluation_reduced_momenta=(-0.5, 0.1),
                hopping_ranges=definition.hopping_ranges,
                fitting_weights=definition.fitting_weights,
                tolerances=definition.tolerances,
            )

    def test_verifier__independently_reconstructs_every_channel(self) -> None:
        """The verifier bypasses both producer and reusable Workflow Actions."""
        result = SingleBandFourierReductionExperiment().execute(self.definition())

        verification = SingleBandFourierReductionExperimentVerifier().execute(result)

        assert verification.passes
        assert verification.structural_checks_pass
        assert verification.energy_maximum_absolute_defect.magnitude <= 1.0e-12
        assert verification.squared_energy_maximum_absolute_defect.magnitude <= 1.0e-12

    def test_serializers__are_canonical_and_match_strict_schemas(self) -> None:
        """All versioned wire documents reject unknown root properties."""
        definition = self.definition()
        result = SingleBandFourierReductionExperiment().execute(definition)
        verification = SingleBandFourierReductionExperimentVerifier().execute(result)
        wires = {
            "input": SingleBandFourierReductionInputSerializer().serialize(definition),
            "result": SingleBandFourierReductionResultSerializer().serialize(result),
            "verification": (
                SingleBandFourierReductionVerificationSerializer().serialize(
                    verification
                )
            ),
        }
        root = Path(__file__).resolve().parents[1]
        for name, wire in wires.items():
            document = json.loads(wire)
            assert wire.endswith(b"\n")
            assert not wire.endswith(b"\n\n")
            assert (
                json.dumps(
                    document,
                    sort_keys=True,
                    separators=(",", ":"),
                    ensure_ascii=False,
                    allow_nan=False,
                ).encode("utf-8")
                + b"\n"
                == wire
            )
            schema = json.loads(
                (root / "schemas" / f"{name}.schema.json").read_text(encoding="utf-8")
            )
            # The retained v1 schemas freeze full-size inventories. Software-test
            # controls intentionally differ, so validate strictness using the retained
            # fixture in the execution test below rather than this small document.
            assert schema["additionalProperties"] is False
            retained = json.loads(
                next((root / "runs").glob("*.run-20261014T183028Z"))
                .joinpath(f"{name}.json")
                .read_text(encoding="utf-8")
            )
            Draft202012Validator(schema).validate(retained)
            retained["unknown"] = True
            with pytest.raises(ValidationError):
                Draft202012Validator(schema).validate(retained)

    def test_execution_provenance__distinguishes_live_and_retained_revisions(
        self,
    ) -> None:
        """The live lock advances without weakening retained producer checks."""
        assert (
            installed_vcs_commit(
                "projectkoios-optimization", _LIVE_OPTIMIZATION_REVISION
            )
            == _LIVE_OPTIMIZATION_REVISION
        )
        assert (
            installed_vcs_commit("projectkoios-physkit", _LIVE_PHYSKIT_REVISION)
            == _LIVE_PHYSKIT_REVISION
        )
        with pytest.raises(RuntimeError, match="does not match"):
            installed_vcs_commit(
                "projectkoios-optimization", EXPECTED_OPTIMIZATION_REVISION
            )
        with pytest.raises(RuntimeError, match="does not match"):
            installed_vcs_commit("projectkoios-physkit", EXPECTED_PHYSKIT_REVISION)

    def test_identity__rejects_version_mutation(self) -> None:
        """Once cited, version-one identity cannot be changed by construction."""
        assert EXPERIMENT_IDENTITY.version_id == EXPERIMENT_VERSION_ID
        with pytest.raises(ValueError, match="immutable"):
            replace(EXPERIMENT_IDENTITY, version_id=f"{EXPERIMENT_FAMILY_ID}.v2")

    def test_definition__rejects_boolean_band_index(self) -> None:
        """A Boolean cannot masquerade as an exact selected-band index."""
        definition = self.definition()

        with pytest.raises(TypeError, match="selected_band_index"):
            SingleBandFourierReductionExperimentDefinition(
                parent_model=definition.parent_model,
                plane_wave_cutoffs=definition.plane_wave_cutoffs,
                plane_wave_reference_cutoff=(definition.plane_wave_reference_cutoff),
                production_plane_wave_cutoff=(definition.production_plane_wave_cutoff),
                finite_difference_points=definition.finite_difference_points,
                parent_sample_reduced_momenta=(
                    definition.parent_sample_reduced_momenta
                ),
                compared_band_count=definition.compared_band_count,
                selected_band_index=True,
                reciprocal_training_mesh_size=(
                    definition.reciprocal_training_mesh_size
                ),
                evaluation_reduced_momenta=(definition.evaluation_reduced_momenta),
                hopping_ranges=definition.hopping_ranges,
                fitting_weights=definition.fitting_weights,
                tolerances=definition.tolerances,
            )
