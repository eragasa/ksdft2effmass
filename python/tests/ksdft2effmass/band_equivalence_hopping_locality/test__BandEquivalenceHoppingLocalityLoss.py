"""Tests for Ragasa2026a/c finite-rank loss ownership."""

from __future__ import annotations

from dataclasses import replace

import numpy as np
import pytest

from ksdft2effmass.analysis.matrix_field.diagnostics.comparison import (
    MatrixFieldErrorAnalyzer,
)
from ksdft2effmass.band_equivalence_hopping_locality import (
    loss_analysis as production_module,
)
from ksdft2effmass.band_equivalence_hopping_locality.loss import (
    BandEquivalenceHoppingLocalityComparisonIdentity,
    BandEquivalenceHoppingLocalityLossAnalyzer,
    BandEquivalenceHoppingLocalityLossDefinition,
    BandEquivalenceHoppingLocalityLossIndependentReferenceAnalyzer,
    BandEquivalenceHoppingLocalityLossVerifier,
    BandEquivalenceHoppingLocalitySampleMeasure,
)
from ksdft2effmass.band_equivalence_hopping_locality.records import (
    BandEquivalenceHoppingLocalityLossRecord,
)
from ksdft2effmass.numerical_consistency import NumericalConsistency
from ksdft2effmass.representation_equivalence import RepresentationEquivalence

pytestmark = [pytest.mark.unit, pytest.mark.numerical_verification]


class TestBandEquivalenceHoppingLocalityLoss:
    """Establish typed identity, finite-rank arithmetic, and independent retention."""

    @staticmethod
    def _rank_two_fields() -> tuple[np.ndarray, np.ndarray]:
        reference = np.array(
            (
                (
                    ((0.0, 0.0), (0.0, 2.0)),
                    ((0.0, 0.0), (0.0, 2.0)),
                ),
            ),
            dtype=np.complex128,
        )
        approximation = np.array(
            (
                (
                    ((1.0, 0.0), (0.0, 2.0)),
                    ((1.0, -1.0j), (1.0j, 1.0)),
                ),
            ),
            dtype=np.complex128,
        )
        return reference, approximation

    @staticmethod
    def _definition(
        *,
        spatial_dimension: int = 2,
        retained_rank: int = 2,
        sample_shape: tuple[int, ...] = (1, 2),
        sample_weights: tuple[float, ...] = (0.25, 0.75),
        norm_energy_scale: float = 2.0,
        sample_inventory_identifier: str = "square-q-grid-n1x2-c-order-v1",
        retained_basis_identifier: str = "rank-two-orthonormal-basis-v1",
        retained_space_identifier: str = "same-retained-space-v1",
        gauge_identifier: str = "declared-comparison-gauge-v1",
        geometry_identifier: str = "square-direct-lattice-v1",
        energy_unit_identifier: str = "dimensionless-model-energy-v1",
        energy_reference_identifier: str = "declared-common-energy-zero-v1",
    ) -> BandEquivalenceHoppingLocalityLossDefinition:
        return BandEquivalenceHoppingLocalityLossDefinition(
            retained_rank=retained_rank,
            sample_measure=BandEquivalenceHoppingLocalitySampleMeasure(
                spatial_dimension=spatial_dimension,
                sample_shape=sample_shape,
                sample_weights=sample_weights,
                sample_inventory_identifier=sample_inventory_identifier,
            ),
            comparison_identity=BandEquivalenceHoppingLocalityComparisonIdentity(
                retained_basis_identifier=retained_basis_identifier,
                retained_space_identifier=retained_space_identifier,
                gauge_identifier=gauge_identifier,
                geometry_identifier=geometry_identifier,
                energy_unit_identifier=energy_unit_identifier,
                energy_reference_identifier=energy_reference_identifier,
            ),
            norm_energy_scale=norm_energy_scale,
        )

    @classmethod
    def _production_analyzer(cls) -> BandEquivalenceHoppingLocalityLossAnalyzer:
        reference, approximation = cls._rank_two_fields()
        return BandEquivalenceHoppingLocalityLossAnalyzer(
            reference=reference,
            approximation=approximation,
            definition=cls._definition(),
        )

    @classmethod
    def _independent_analyzer(
        cls,
    ) -> BandEquivalenceHoppingLocalityLossIndependentReferenceAnalyzer:
        reference, approximation = cls._rank_two_fields()
        return BandEquivalenceHoppingLocalityLossIndependentReferenceAnalyzer(
            reference=reference,
            approximation=approximation,
            definition=cls._definition(),
        )

    def test_rank_two_specialization_preserves_ragasa2026a_values(self) -> None:
        result = self._production_analyzer().execute()

        assert isinstance(result, RepresentationEquivalence)
        assert result.retained_rank == 2
        assert result.sample_shape == (1, 2)
        assert result.operator_loss == pytest.approx(0.40625, abs=1.0e-15)
        assert result.spectral_loss == pytest.approx(0.03125, abs=1.0e-15)

    def test_rank_three_uses_ragasa2026c_cross_rank_normalization(self) -> None:
        reference = np.zeros((1, 1, 3, 3), dtype=np.complex128)
        approximation = np.zeros_like(reference)
        approximation[0, 0] = np.diag((1.0, 2.0, 3.0))
        definition = self._definition(
            retained_rank=3,
            sample_shape=(1, 1),
            sample_weights=(1.0,),
            retained_basis_identifier="rank-three-orthonormal-basis-v1",
            sample_inventory_identifier="square-q-grid-n1x1-c-order-v1",
        )
        production = BandEquivalenceHoppingLocalityLossAnalyzer(
            reference=reference,
            approximation=approximation,
            definition=definition,
        ).execute()
        independent = BandEquivalenceHoppingLocalityLossIndependentReferenceAnalyzer(
            reference=reference,
            approximation=approximation,
            definition=definition,
        ).execute()

        assert production.retained_rank == 3
        assert production.operator_loss == pytest.approx(7.0 / 6.0, abs=1.0e-15)
        assert production.spectral_loss == pytest.approx(7.0 / 6.0, abs=1.0e-15)
        assert (
            BandEquivalenceHoppingLocalityLossVerifier(
                production=production,
                independent=independent,
            )
            .result()
            .passed
        )

    def test_supports_declared_finite_rank_above_three(self) -> None:
        retained_rank = 5
        reference = np.zeros((1, 1, retained_rank, retained_rank), dtype=np.complex128)
        approximation = np.broadcast_to(
            np.eye(retained_rank, dtype=np.complex128),
            reference.shape,
        ).copy()
        result = BandEquivalenceHoppingLocalityLossAnalyzer(
            reference=reference,
            approximation=approximation,
            definition=self._definition(
                retained_rank=retained_rank,
                sample_shape=(1, 1),
                sample_weights=(1.0,),
                retained_basis_identifier="rank-five-orthonormal-basis-v1",
                sample_inventory_identifier="square-q-grid-n1x1-c-order-v1",
            ),
        ).execute()

        assert result.retained_rank == 5
        assert result.operator_loss == pytest.approx(0.25, abs=1.0e-15)
        assert result.spectral_loss == pytest.approx(0.25, abs=1.0e-15)

    def test_independent_route_does_not_call_production_arithmetic(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        def forbidden_normalization(_rank: int, _scale: float) -> float:
            raise AssertionError("independent route called production normalization")

        monkeypatch.setattr(
            production_module,
            "_loss_normalization",
            forbidden_normalization,
        )
        independent = self._independent_analyzer().execute()
        monkeypatch.undo()
        production = self._production_analyzer().execute()
        verification = BandEquivalenceHoppingLocalityLossVerifier(
            production=production,
            independent=independent,
        ).result()

        assert isinstance(verification, NumericalConsistency)
        assert verification.passed
        assert set(verification.observations) == {
            "operator_loss",
            "spectral_loss",
        }
        assert all(
            observation.tolerance.magnitude == 1.0e-10
            for observation in verification.observations.values()
        )

    @pytest.mark.parametrize(
        ("identity_field", "different_value"),
        (
            ("gauge_identifier", "different-comparison-gauge-v1"),
            ("geometry_identifier", "different-direct-lattice-v1"),
            ("energy_reference_identifier", "different-energy-zero-v1"),
        ),
    )
    def test_verifier_rejects_comparison_identity_mismatch(
        self,
        identity_field: str,
        different_value: str,
    ) -> None:
        production = self._production_analyzer().execute()
        independent = self._independent_analyzer().execute()
        identity = replace(
            independent.definition.comparison_identity,
            **{identity_field: different_value},
        )
        mismatched = replace(
            independent,
            definition=replace(independent.definition, comparison_identity=identity),
        )

        with pytest.raises(ValueError, match="loss definitions differ"):
            BandEquivalenceHoppingLocalityLossVerifier(
                production=production,
                independent=mismatched,
            )

    def test_verifier_rejects_sample_inventory_identity_mismatch(self) -> None:
        production = self._production_analyzer().execute()
        independent = self._independent_analyzer().execute()
        sample_measure = replace(
            independent.definition.sample_measure,
            sample_inventory_identifier="different-q-grid-v1",
        )
        mismatched = replace(
            independent,
            definition=replace(independent.definition, sample_measure=sample_measure),
        )

        with pytest.raises(ValueError, match="loss definitions differ"):
            BandEquivalenceHoppingLocalityLossVerifier(
                production=production,
                independent=mismatched,
            )

    def test_uniform_rank_two_weights_match_squared_normalized_rms(self) -> None:
        reference, approximation = self._rank_two_fields()
        definition = self._definition(sample_weights=(0.5, 0.5))
        loss = BandEquivalenceHoppingLocalityLossAnalyzer(
            reference=reference,
            approximation=approximation,
            definition=definition,
        ).execute()
        errors = MatrixFieldErrorAnalyzer(
            reference=reference,
            approximation=approximation,
            norm_energy_scale=definition.norm_energy_scale,
        ).result()

        assert loss.operator_loss == pytest.approx(
            errors.normalized_matrix_frobenius_rms**2,
            abs=1.0e-15,
        )
        assert loss.spectral_loss == pytest.approx(
            errors.normalized_ordered_spectrum_l2_rms**2,
            abs=1.0e-15,
        )

    def test_record_round_trip_preserves_typed_definition(self) -> None:
        analysis = self._production_analyzer().execute()
        record = BandEquivalenceHoppingLocalityLossRecord.from_analysis(analysis)
        restored = BandEquivalenceHoppingLocalityLossRecord.from_json(record.to_json())

        assert restored == record
        assert restored.to_analysis() == analysis
        assert restored.retained_rank == 2
        assert restored.norm_energy_scale == 2.0
        assert restored.sample_inventory_identifier == "square-q-grid-n1x2-c-order-v1"
        assert restored.retained_space_identifier == "same-retained-space-v1"
        assert restored.energy_reference_identifier == "declared-common-energy-zero-v1"
        assert restored.sample_weights == (0.25, 0.75)

    def test_supports_three_dimensional_sample_inventory(self) -> None:
        reference, approximation = self._rank_two_fields()
        result = BandEquivalenceHoppingLocalityLossAnalyzer(
            reference=reference.reshape(1, 1, 2, 2, 2),
            approximation=approximation.reshape(1, 1, 2, 2, 2),
            definition=self._definition(
                spatial_dimension=3,
                sample_shape=(1, 1, 2),
                sample_inventory_identifier="simple-cubic-q-grid-n1x1x2-c-order-v1",
                geometry_identifier="simple-cubic-direct-lattice-v1",
            ),
        ).execute()

        assert result.spatial_dimension == 3
        assert result.sample_shape == (1, 1, 2)
        assert result.operator_loss == pytest.approx(0.40625, abs=1.0e-15)

    @pytest.mark.parametrize(
        ("retained_rank", "error"), ((True, TypeError), (1, ValueError))
    )
    def test_rejects_invalid_rank_types_and_values(
        self,
        retained_rank: int,
        error: type[Exception],
    ) -> None:
        with pytest.raises(error):
            self._definition(retained_rank=retained_rank)

    def test_rejects_nonexact_weight_types_and_invalid_identities(self) -> None:
        with pytest.raises(TypeError, match="built-in floats"):
            self._definition(sample_weights=(0.25, np.float64(0.75)))
        with pytest.raises(ValueError, match="nonnegative"):
            self._definition(sample_weights=(-0.25, 1.25))
        with pytest.raises(ValueError, match="energy_reference_identifier"):
            self._definition(energy_reference_identifier="")

    @pytest.mark.parametrize(
        "analyzer_type",
        (
            BandEquivalenceHoppingLocalityLossAnalyzer,
            BandEquivalenceHoppingLocalityLossIndependentReferenceAnalyzer,
        ),
    )
    def test_rejects_nonhermitian_matrix_fields(
        self,
        analyzer_type: type[
            BandEquivalenceHoppingLocalityLossAnalyzer
            | BandEquivalenceHoppingLocalityLossIndependentReferenceAnalyzer
        ],
    ) -> None:
        reference, approximation = self._rank_two_fields()
        nonhermitian = approximation.copy()
        nonhermitian[0, 1, 0, 1] = 2.0j

        with pytest.raises(ValueError, match="exactly Hermitian"):
            analyzer_type(
                reference=reference,
                approximation=nonhermitian,
                definition=self._definition(),
            )

    @pytest.mark.parametrize(
        "analyzer_type",
        (
            BandEquivalenceHoppingLocalityLossAnalyzer,
            BandEquivalenceHoppingLocalityLossIndependentReferenceAnalyzer,
        ),
    )
    def test_reports_binary64_finite_sum_overflow(
        self,
        analyzer_type: type[
            BandEquivalenceHoppingLocalityLossAnalyzer
            | BandEquivalenceHoppingLocalityLossIndependentReferenceAnalyzer
        ],
    ) -> None:
        reference = np.zeros((1, 1, 2, 2), dtype=np.complex128)
        approximation = np.zeros_like(reference)
        approximation[0, 0] = np.diag((1.0e308, -1.0e308))
        analyzer = analyzer_type(
            reference=reference,
            approximation=approximation,
            definition=self._definition(
                sample_shape=(1, 1),
                sample_weights=(1.0,),
                sample_inventory_identifier="square-q-grid-n1x1-c-order-v1",
            ),
        )

        with pytest.raises(FloatingPointError, match="overflow"):
            analyzer.execute()

    @pytest.mark.parametrize(
        "analyzer_type",
        (
            BandEquivalenceHoppingLocalityLossAnalyzer,
            BandEquivalenceHoppingLocalityLossIndependentReferenceAnalyzer,
        ),
    )
    def test_reports_binary64_squared_term_underflow(
        self,
        analyzer_type: type[
            BandEquivalenceHoppingLocalityLossAnalyzer
            | BandEquivalenceHoppingLocalityLossIndependentReferenceAnalyzer
        ],
    ) -> None:
        reference = np.zeros((1, 1, 2, 2), dtype=np.complex128)
        approximation = np.zeros_like(reference)
        approximation[0, 0, 0, 0] = 1.0e-200
        analyzer = analyzer_type(
            reference=reference,
            approximation=approximation,
            definition=self._definition(
                sample_shape=(1, 1),
                sample_weights=(1.0,),
                sample_inventory_identifier="square-q-grid-n1x1-c-order-v1",
            ),
        )

        with pytest.raises(FloatingPointError, match="underflow"):
            analyzer.execute()

    @pytest.mark.parametrize(
        "analyzer_type",
        (
            BandEquivalenceHoppingLocalityLossAnalyzer,
            BandEquivalenceHoppingLocalityLossIndependentReferenceAnalyzer,
        ),
    )
    @pytest.mark.parametrize(
        ("matrix_entry", "sample_weights", "norm_energy_scale", "message"),
        (
            (1.0e-160, (1.0e-100, 1.0), 1.0, "weighted term"),
            (3.0e-162, (1.0, 0.0), 2.0, "normalized operator loss"),
        ),
    )
    def test_reports_weighted_or_normalized_loss_underflow(
        self,
        analyzer_type: type[
            BandEquivalenceHoppingLocalityLossAnalyzer
            | BandEquivalenceHoppingLocalityLossIndependentReferenceAnalyzer
        ],
        matrix_entry: float,
        sample_weights: tuple[float, ...],
        norm_energy_scale: float,
        message: str,
    ) -> None:
        reference = np.zeros((1, 2, 2, 2), dtype=np.complex128)
        approximation = np.zeros_like(reference)
        approximation[0, 0, 0, 0] = matrix_entry
        analyzer = analyzer_type(
            reference=reference,
            approximation=approximation,
            definition=self._definition(
                sample_weights=sample_weights,
                norm_energy_scale=norm_energy_scale,
            ),
        )

        with pytest.raises(FloatingPointError, match=message):
            analyzer.execute()

    @pytest.mark.parametrize(
        ("norm_energy_scale", "message"),
        ((1.0e308, "overflowed"), (1.0e-308, "underflowed")),
    )
    def test_definition_reports_binary64_normalization_range_failure(
        self,
        norm_energy_scale: float,
        message: str,
    ) -> None:
        with pytest.raises(FloatingPointError, match=message):
            self._definition(norm_energy_scale=norm_energy_scale)

    def test_rejects_approximately_normalized_weights_without_mutating_them(
        self,
    ) -> None:
        with pytest.raises(ValueError, match="sum exactly to one"):
            self._definition(
                sample_shape=(1, 1),
                sample_weights=(1.0000000000005,),
            )

    def test_rejects_matrix_shape_that_disagrees_with_definition(self) -> None:
        reference, approximation = self._rank_two_fields()
        definition = self._definition(
            sample_shape=(2, 1),
            sample_inventory_identifier="square-q-grid-n2x1-c-order-v1",
        )

        with pytest.raises(ValueError, match="sample shape|loss definition"):
            BandEquivalenceHoppingLocalityLossAnalyzer(
                reference=reference,
                approximation=approximation,
                definition=definition,
            )

    def test_rejects_subnormal_nonhermitian_defect_even_when_norm_underflows(
        self,
    ) -> None:
        reference = np.zeros((1, 1, 2, 2), dtype=np.complex128)
        approximation = reference.copy()
        approximation[0, 0, 0, 1] = np.nextafter(0.0, 1.0)

        for analyzer_type in (
            BandEquivalenceHoppingLocalityLossAnalyzer,
            BandEquivalenceHoppingLocalityLossIndependentReferenceAnalyzer,
        ):
            with pytest.raises(ValueError, match="exactly Hermitian"):
                analyzer_type(
                    reference=reference,
                    approximation=approximation,
                    definition=self._definition(
                        sample_shape=(1, 1),
                        sample_weights=(1.0,),
                        sample_inventory_identifier="square-q-grid-n1x1-c-order-v1",
                    ),
                )
