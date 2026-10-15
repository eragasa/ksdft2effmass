"""Software verification for the constrained admissible-set experiment."""

from __future__ import annotations

from dataclasses import replace

import numpy as np
import pytest
from ksdft2effmass.operators import (
    ComplexMatrixQuantity,
    PhysicalUnit,
    ScalarQuantity,
    Unitless,
)
from ksdft2effmass.periodic1d import (
    Periodic1DBlockHamiltonianToyModel,
    Periodic1DMultibandAlignmentCalculationDefinition,
)
from ksdft2effmass.solid_state import BlockHoppingModel1D
from projectkoios.optimization.affine.complex_quadratic import (
    ComplexAffineResidualMatrix,
    ComplexAffineResidualQuadraticTolerance,
    ComplexAffineResidualVector,
)
from projectkoios.optimization.affine.factory import (
    ComplexAffineResidualQuadraticConstructorFactory,
    ComplexAffineResidualQuadraticMethod,
)
from projectkoios.optimization.quadratic.quadratic import (
    PositiveDefiniteQuadraticLoss,
)

from constrained_admissible_sets import (
    EXPERIMENT_FAMILY_ID,
    AdmissibleSetDisposition,
    AdmissibleSetThresholds,
    ConstrainedAdmissibleSetsExperiment,
    ConstrainedAdmissibleSetsExperimentDefinition,
    ConstrainedAdmissibleSetsExperimentVerifier,
)

pytestmark = pytest.mark.software_verification


class TestConstrainedAdmissibleSetsExperiment:
    """Establish parent composition, owner integration, and verification."""

    @staticmethod
    def baseline_definition(
        *, physical_energy: bool = False
    ) -> Periodic1DMultibandAlignmentCalculationDefinition:
        """Return a compact controlled rank-two baseline."""
        unit = PhysicalUnit("electron_volt") if physical_energy else Unitless()
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
            "constrained-sets-rank-two-parent",
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
            calculation_id="constrained-sets-baseline-software-test",
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
        cls, *, physical_energy: bool = False
    ) -> ConstrainedAdmissibleSetsExperimentDefinition:
        """Return bounded controls with compatible and separated cases."""
        baseline = cls.baseline_definition(physical_energy=physical_energy)
        energy_unit = baseline.parent_model.hopping_model.hopping_blocks[0].unit
        return ConstrainedAdmissibleSetsExperimentDefinition(
            multiband_baseline=baseline,
            energy_shift_ratio_bounds=(-0.25, 0.25),
            splitting_scale_bounds=(0.4, 1.2),
            alignment_angles=(-1.2, -0.9, -0.6, -0.3, 0.0, 0.3, 0.6, 0.9, 1.2),
            loss_energy_scale=ScalarQuantity(1.0, energy_unit),
            compatible_thresholds=AdmissibleSetThresholds("compatible", 0.03, 0.33),
            separated_thresholds=AdmissibleSetThresholds("separated", 0.03, 0.31),
            compatible_witness=(0.0, 1.0),
            separation_resolution=0.05,
            owner_absolute_tolerance=1.0e-12,
            verification_absolute_tolerance=1.0e-11,
        )

    def test_execute__derives_losses_and_retains_both_dispositions(self) -> None:
        """The experiment derives its quadratics instead of accepting them as input."""
        definition = self.definition()

        result = ConstrainedAdmissibleSetsExperiment().execute(definition)

        assert result.multiband_baseline.definition is definition.multiband_baseline
        assert result.spectral_loss.alignment_angle is None
        assert tuple(loss.alignment_angle for loss in result.operator_losses) == (
            definition.alignment_angles
        )
        compatible, separated = result.cases
        assert compatible.disposition is AdmissibleSetDisposition.COMPATIBLE_WITNESS
        assert compatible.common_witness is not None
        assert compatible.common_witness.parameter == (0.0, 1.0)
        assert compatible.common_witness.selected_alignment_angle == 0.3
        assert separated.disposition is AdmissibleSetDisposition.CERTIFIED_SEPARATED
        assert separated.feasible_operator_component_angles == (0.3,)
        assert separated.separation_lower_bound > definition.separation_resolution
        assert separated.separation_lower_bound <= separated.separation_upper_bound

    def test_quadratic_adapter__forwards_complex_observations_and_raw_weights(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """KSD owns flattening, sign, normalization, labels, and tolerance mapping."""

        class RecordingConstructor:
            design_matrix: ComplexAffineResidualMatrix | None = None
            target_vector: ComplexAffineResidualVector | None = None
            weights: tuple[float, ...] | None = None

            def construct(
                self,
                design_matrix: ComplexAffineResidualMatrix,
                target_vector: ComplexAffineResidualVector,
                /,
                *,
                weights: tuple[float, ...] | None = None,
            ) -> PositiveDefiniteQuadraticLoss:
                self.design_matrix = design_matrix
                self.target_vector = target_vector
                self.weights = weights
                return PositiveDefiniteQuadraticLoss(
                    (0.25, -0.5),
                    ((1.0, 0.0), (0.0, 2.0)),
                    0.125,
                )

        constructor = RecordingConstructor()
        factory_arguments: list[
            tuple[
                ComplexAffineResidualQuadraticMethod,
                ComplexAffineResidualQuadraticTolerance,
            ]
        ] = []

        def create(
            method: ComplexAffineResidualQuadraticMethod,
            /,
            *,
            tolerance: ComplexAffineResidualQuadraticTolerance,
        ) -> RecordingConstructor:
            factory_arguments.append((method, tolerance))
            return constructor

        monkeypatch.setattr(
            ComplexAffineResidualQuadraticConstructorFactory,
            "create",
            staticmethod(create),
        )
        features = np.asarray(
            (((1.0 + 1.0j, 2.0), (3.0, 4.0 - 1.0j)),),
            dtype=np.complex128,
        )
        offset = np.asarray(((0.5 - 0.25j, -1.0 + 2.0j),))

        result = ConstrainedAdmissibleSetsExperiment._quadratic(
            "adapter-test",
            0.3,
            features,
            offset,
            2.0,
            1.0e-9,
        )

        assert constructor.design_matrix == (
            (1.0 + 1.0j, 2.0 + 0.0j),
            (3.0 + 0.0j, 4.0 - 1.0j),
        )
        assert constructor.target_vector == (-0.5 + 0.25j, 1.0 - 2.0j)
        assert constructor.weights == (0.125, 0.125)
        assert factory_arguments == [
            (
                ComplexAffineResidualQuadraticMethod.NUMPY_DENSE,
                ComplexAffineResidualQuadraticTolerance(
                    absolute=1.0e-9,
                    relative=0.0,
                ),
            )
        ]
        assert result.channel_id == "adapter-test"
        assert result.alignment_angle == 0.3
        assert result.center == (0.25, -0.5)
        assert result.quadratic_matrix == ((1.0, 0.0), (0.0, 2.0))
        assert result.minimum_squared_loss == 0.125

    def test_verifier__independently_reconstructs_parent_losses_and_geometry(
        self,
    ) -> None:
        """Independent formulas agree with the composed owner-backed producer."""
        result = ConstrainedAdmissibleSetsExperiment().execute(self.definition())

        verification = ConstrainedAdmissibleSetsExperimentVerifier().execute(result)

        assert verification.passes
        assert verification.dimensionless_maximum_absolute_defect < 1.0e-11
        assert verification.energy_maximum_absolute_defect.magnitude < 1.0e-11

    def test_verifier__retains_physical_parent_energy_defect_unit(self) -> None:
        """Energy defects remain separate from dimensionless geometry defects."""
        result = ConstrainedAdmissibleSetsExperiment().execute(
            self.definition(physical_energy=True)
        )

        verification = ConstrainedAdmissibleSetsExperimentVerifier().execute(result)

        assert verification.passes
        assert verification.energy_maximum_absolute_defect.unit == PhysicalUnit(
            "electron_volt"
        )
        assert verification.dimensionless_maximum_absolute_defect < 1.0e-11
        assert verification.energy_maximum_absolute_defect.magnitude < 1.0e-11

    def test_verifier__detects_tampered_point_role(self) -> None:
        """Role identity remains independently verified experiment evidence."""
        result = ConstrainedAdmissibleSetsExperiment().execute(self.definition())
        compatible, separated = result.cases
        assert compatible.common_witness is not None
        changed = replace(compatible.common_witness, role="wrong-role")
        changed_case = replace(
            compatible,
            common_witness=changed,
            spectral_certificate_point=changed,
            operator_certificate_point=changed,
        )
        tampered = replace(result, cases=(changed_case, separated))

        verification = ConstrainedAdmissibleSetsExperimentVerifier().execute(tampered)

        assert not verification.passes
        assert verification.dimensionless_maximum_absolute_defect == 1.0

    def test_identity__is_publication_independent(self) -> None:
        """The experiment family contains no manuscript or milestone alias."""
        assert EXPERIMENT_FAMILY_ID == (
            "ksdft2effmass.campaign.model-adequacy.periodic1d."
            "constrained-admissible-sets"
        )
        assert "paper" not in EXPERIMENT_FAMILY_ID
        assert "m3" not in EXPERIMENT_FAMILY_ID

    def test_definition__rejects_boolean_resolution(self) -> None:
        """Boolean values cannot masquerade as scientific numeric controls."""
        definition = self.definition()

        with pytest.raises(TypeError, match="separation_resolution"):
            replace(definition, separation_resolution=True)
