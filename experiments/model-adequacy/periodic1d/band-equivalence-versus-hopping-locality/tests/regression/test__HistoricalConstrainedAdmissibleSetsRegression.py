"""Software regression for the historical finite-angle calculation."""

from __future__ import annotations

import hashlib
import json
from dataclasses import replace
from pathlib import Path

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

from band_equivalence_hopping_locality import EXPERIMENT_FAMILY_ID
from band_equivalence_hopping_locality.regression import (
    AdmissibleSetDisposition,
    AdmissibleSetThresholds,
    ConstrainedAdmissibleSetsExperiment,
    ConstrainedAdmissibleSetsExperimentDefinition,
    ConstrainedAdmissibleSetsExperimentVerifier,
)

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]

pytestmark = pytest.mark.software_verification


class TestConstrainedAdmissibleSetsExperiment:
    """Establish parent composition, owner integration, and verification."""

    @staticmethod
    def baseline_definition(
        *,
        physical_energy: bool = False,
        reciprocal_mesh_size: int = 16,
        withheld_mesh_size: int = 33,
        hopping_ranges: tuple[int, ...] = (0, 1, 2, 3),
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
            reciprocal_mesh_size=reciprocal_mesh_size,
            withheld_mesh_size=withheld_mesh_size,
            hopping_ranges=hopping_ranges,
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
            locality_ranges=(0, 1, 2, 3),
            separation_resolution=0.05,
            owner_absolute_tolerance=1.0e-12,
            verification_absolute_tolerance=1.0e-11,
        )

    @classmethod
    def historical_parity_definition(
        cls,
    ) -> ConstrainedAdmissibleSetsExperimentDefinition:
        """Return the exact pre-migration numerical controls.

        Returns
        -------
        ConstrainedAdmissibleSetsExperimentDefinition
            Non-decisive controls numerically matching the historical calculation.
        """
        baseline = cls.baseline_definition(
            reciprocal_mesh_size=64,
            withheld_mesh_size=257,
            hopping_ranges=(0, 1, 2, 3, 4, 6, 8),
        )
        return ConstrainedAdmissibleSetsExperimentDefinition(
            multiband_baseline=baseline,
            energy_shift_ratio_bounds=(-0.25, 0.25),
            splitting_scale_bounds=(0.4, 1.2),
            alignment_angles=(-1.2, -0.9, -0.6, -0.3, 0.0, 0.3, 0.6, 0.9, 1.2),
            loss_energy_scale=ScalarQuantity(1.0, Unitless()),
            compatible_thresholds=AdmissibleSetThresholds("compatible", 0.03, 0.33),
            separated_thresholds=AdmissibleSetThresholds("separated", 0.03, 0.31),
            compatible_witness=(0.0, 1.0),
            locality_ranges=(0, 1, 2, 3, 4, 6, 8),
            separation_resolution=0.05,
            owner_absolute_tolerance=1.0e-12,
            verification_absolute_tolerance=1.0e-11,
        )

    @staticmethod
    def experiment_root() -> Path:
        """Return the experiment root containing the isolated regression.

        Returns
        -------
        pathlib.Path
            Absolute experiment directory containing schemas and source.
        """
        return Path(__file__).resolve().parents[2]

    @classmethod
    def historical_result_document(cls) -> dict[str, JsonValue]:
        """Load the immutable pre-migration result document.

        Returns
        -------
        dict[str, JsonValue]
            Decoded historical result used only as a parity oracle.
        """
        path = (
            cls.experiment_root().parents[3]
            / "calculations/ICMSEP2026/conference/paper_1"
            / "constrained-admissible-sets/result.json"
        )
        value: JsonValue = json.loads(path.read_text(encoding="utf-8"))
        if type(value) is not dict:
            raise TypeError("historical result root must be a built-in dict")
        return value

    @staticmethod
    def mapping(value: JsonValue, context: str) -> dict[str, JsonValue]:
        """Narrow one JSON mapping.

        Parameters
        ----------
        value
            Recursive JSON value to narrow.
        context
            Human-readable failure location.

        Returns
        -------
        dict[str, JsonValue]
            Exact built-in mapping.
        """
        if type(value) is not dict:
            raise TypeError(f"{context} must be a built-in dict")
        return value

    @staticmethod
    def array(value: JsonValue, context: str) -> list[JsonValue]:
        """Narrow one JSON array.

        Parameters
        ----------
        value
            Recursive JSON value to narrow.
        context
            Human-readable failure location.

        Returns
        -------
        list[JsonValue]
            Exact built-in list.
        """
        if type(value) is not list:
            raise TypeError(f"{context} must be a built-in list")
        return value

    @staticmethod
    def number(value: JsonValue, context: str) -> float:
        """Narrow one non-Boolean JSON number.

        Parameters
        ----------
        value
            Recursive JSON value to narrow.
        context
            Human-readable failure location.

        Returns
        -------
        float
            Numeric value converted to a built-in float.
        """
        if type(value) is int:
            return float(value)
        if type(value) is float:
            return value
        raise TypeError(f"{context} must be numeric")

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
        assert compatible.common_witness.objective_evaluation_operator_rms_loss >= 0.0
        assert (
            tuple(item.maximum_range for item in compatible.common_witness.locality)
            == definition.locality_ranges
        )

    def test_historical_parity__matches_every_retained_numerical_channel(self) -> None:
        """The regression recovers all historical computational channels."""
        result = ConstrainedAdmissibleSetsExperiment().execute(
            self.historical_parity_definition()
        )
        historical = self.historical_result_document()
        defects: list[float] = []
        summary = self.mapping(historical["baseline_summary"], "baseline summary")
        gap = self.mapping(summary["external_gap_minimum"], "external gap")
        defects.extend(
            (
                abs(
                    result.multiband_baseline.diagnostics.external_gap_minimum.magnitude
                    - self.number(gap["magnitude"], "external gap magnitude")
                ),
                abs(
                    result.multiband_baseline.diagnostics.transport.minimum_overlap_singular_value
                    - self.number(
                        summary["minimum_neighbor_or_closure_overlap_singular_value"],
                        "minimum overlap",
                    )
                ),
                abs(
                    result.multiband_baseline.diagnostics.pointwise_alignment.projector_maximum_frobenius_defect
                    - self.number(
                        summary["projector_maximum_frobenius_defect"],
                        "projector defect",
                    )
                ),
            )
        )
        historical_losses = self.mapping(
            historical["training_quadratic_losses"], "quadratic losses"
        )
        expected_losses = (
            self.mapping(historical_losses["spectral"], "spectral loss"),
            *(
                self.mapping(value, "operator loss")
                for value in self.array(
                    historical_losses["operator_components"], "operator losses"
                )
            ),
        )
        retained_losses = (result.spectral_loss, *result.operator_losses)
        assert len(retained_losses) == len(expected_losses)
        for retained, expected in zip(retained_losses, expected_losses, strict=True):
            expected_angle = expected["alignment_angle"]
            if expected_angle is None:
                assert retained.alignment_angle is None
                assert retained.channel_id == ("spectral-objective-construction-rms-v1")
            else:
                angle = self.number(expected_angle, "alignment angle")
                assert retained.alignment_angle == angle
                assert retained.channel_id == (
                    f"operator-objective-construction-rms-angle-{angle:.17g}"
                )
            expected_center = self.array(expected["center"], "loss center")
            expected_matrix = self.array(
                expected["quadratic_matrix"], "quadratic matrix"
            )
            defects.extend(
                abs(retained.center[index] - self.number(value, "center value"))
                for index, value in enumerate(expected_center)
            )
            for row_index, row_value in enumerate(expected_matrix):
                row = self.array(row_value, "quadratic row")
                defects.extend(
                    abs(
                        retained.quadratic_matrix[row_index][column_index]
                        - self.number(value, "quadratic value")
                    )
                    for column_index, value in enumerate(row)
                )
            defects.append(
                abs(
                    retained.minimum_squared_loss
                    - self.number(
                        expected["minimum_squared_loss"], "minimum squared loss"
                    )
                )
            )
        historical_cases = self.array(historical["cases"], "cases")
        assert len(historical_cases) == len(result.cases)
        for retained_case, case_value in zip(
            result.cases, historical_cases, strict=True
        ):
            expected_case = self.mapping(case_value, "case")
            assert retained_case.disposition.value == expected_case["disposition"]
            expected_angles = self.array(
                expected_case["feasible_operator_component_angles"],
                "feasible angles",
            )
            assert retained_case.feasible_operator_component_angles == tuple(
                self.number(value, "feasible angle") for value in expected_angles
            )
            defects.extend(
                (
                    abs(
                        retained_case.separation_lower_bound
                        - self.number(
                            expected_case["separation_lower_bound"], "lower bound"
                        )
                    ),
                    abs(
                        retained_case.separation_upper_bound
                        - self.number(
                            expected_case["separation_upper_bound"], "upper bound"
                        )
                    ),
                    abs(
                        retained_case.separation_resolution
                        - self.number(
                            expected_case["separation_resolution"], "resolution"
                        )
                    ),
                )
            )
            retained_evaluations = (
                retained_case.spectral_certificate_point,
                retained_case.operator_certificate_point,
            )
            expected_evaluations = (
                self.mapping(
                    expected_case["spectral_certificate_point"], "spectral point"
                ),
                self.mapping(
                    expected_case["operator_certificate_point"], "operator point"
                ),
            )
            for retained_evaluation, expected_evaluation in zip(
                retained_evaluations, expected_evaluations, strict=True
            ):
                assert retained_evaluation.role == expected_evaluation["role"]
                parameter = self.array(
                    expected_evaluation["parameter"], "evaluation parameter"
                )
                defects.extend(
                    abs(
                        retained_evaluation.parameter[index]
                        - self.number(value, "parameter value")
                    )
                    for index, value in enumerate(parameter)
                )
                defects.extend(
                    (
                        abs(
                            retained_evaluation.selected_alignment_angle
                            - self.number(
                                expected_evaluation["selected_alignment_angle"],
                                "selected angle",
                            )
                        ),
                        abs(
                            retained_evaluation.objective_construction_spectral_rms_loss
                            - self.number(
                                expected_evaluation["training_spectral_rms_loss"],
                                "construction spectral loss",
                            )
                        ),
                        abs(
                            retained_evaluation.objective_construction_operator_rms_loss
                            - self.number(
                                expected_evaluation["training_operator_rms_loss"],
                                "construction operator loss",
                            )
                        ),
                        abs(
                            retained_evaluation.objective_evaluation_spectral_rms_loss
                            - self.number(
                                expected_evaluation["withheld_spectral_rms_loss"],
                                "evaluation spectral loss",
                            )
                        ),
                        abs(
                            retained_evaluation.objective_evaluation_operator_rms_loss
                            - self.number(
                                expected_evaluation["withheld_operator_rms_loss"],
                                "evaluation operator loss",
                            )
                        ),
                    )
                )
                expected_locality = self.array(
                    expected_evaluation["locality"], "locality"
                )
                assert len(retained_evaluation.locality) == len(expected_locality)
                for retained_item, item_value in zip(
                    retained_evaluation.locality, expected_locality, strict=True
                ):
                    expected_item = self.mapping(item_value, "locality item")
                    assert retained_item.maximum_range == self.number(
                        expected_item["maximum_range"], "maximum range"
                    )
                    for retained_value, key in (
                        (
                            retained_item.reference_omitted_block_l2_norm,
                            "reference_omitted_block_l2_norm",
                        ),
                        (
                            retained_item.attacked_omitted_block_l2_norm,
                            "attacked_omitted_block_l2_norm",
                        ),
                        (
                            retained_item.candidate_omitted_block_l2_norm,
                            "candidate_omitted_block_l2_norm",
                        ),
                    ):
                        defects.append(
                            abs(retained_value - self.number(expected_item[key], key))
                        )
        assert max(defects) <= 1.0e-11

    def test_regression_baseline__binds_historical_files_without_version_claim(
        self,
    ) -> None:
        """Bind immutable historical evidence without assigning a successor version."""
        experiment = self.experiment_root()
        repository = experiment.parents[3]
        baseline_path = experiment / "regression/historical-64-257/baseline.json"
        baseline_value: JsonValue = json.loads(
            baseline_path.read_text(encoding="utf-8")
        )
        baseline = self.mapping(baseline_value, "regression baseline")
        assert baseline["schema"] == (
            "ksdft2effmass.campaign.model-adequacy.periodic1d."
            "band-equivalence-versus-hopping-locality."
            "historical-regression-baseline.v1"
        )
        assert "version_id" not in baseline
        assert "version_source" not in baseline
        assert "evidence_package_identity" not in baseline
        relative_root = baseline["repository_relative_path"]
        assert type(relative_root) is str
        assert baseline["excluded_family"] != relative_root
        digests = self.mapping(baseline["sha256"], "historical digests")
        for name, expected in digests.items():
            assert type(expected) is str
            assert (
                hashlib.sha256(
                    (repository / relative_root / name).read_bytes()
                ).hexdigest()
                == expected
            )

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

    def test_verifier__detects_tampered_evaluation_diagnostic(self) -> None:
        """Evaluation-only losses are independently reconstructed and checked."""
        result = ConstrainedAdmissibleSetsExperiment().execute(self.definition())
        compatible, separated = result.cases
        assert compatible.common_witness is not None
        changed = replace(
            compatible.common_witness,
            objective_evaluation_operator_rms_loss=(
                compatible.common_witness.objective_evaluation_operator_rms_loss
                + 1.0e-3
            ),
        )
        changed_case = replace(
            compatible,
            common_witness=changed,
            spectral_certificate_point=changed,
            operator_certificate_point=changed,
        )
        tampered = replace(result, cases=(changed_case, separated))

        verification = ConstrainedAdmissibleSetsExperimentVerifier().execute(tampered)

        assert not verification.passes
        assert verification.dimensionless_maximum_absolute_defect > 9.0e-4

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
            "band-equivalence-versus-hopping-locality"
        )
        assert "paper" not in EXPERIMENT_FAMILY_ID
        assert "m3" not in EXPERIMENT_FAMILY_ID

    def test_definition__rejects_boolean_resolution(self) -> None:
        """Boolean values cannot masquerade as scientific numeric controls."""
        definition = self.definition()

        with pytest.raises(TypeError, match="separation_resolution"):
            replace(definition, separation_resolution=True)
