"""Contracts for the typed 2D/3D representation-equivalence projection."""

from dataclasses import FrozenInstanceError, replace

import pytest

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality import (
    BandEquivalenceLocalityRepresentationEquivalenceAnalysis,
)
from ksdft2effmass.representation_equivalence import RepresentationEquivalence
from ksdft2effmass.serialization import BaseTypedRecord

pytestmark = pytest.mark.software_verification


def _applicable_result() -> BandEquivalenceLocalityRepresentationEquivalenceAnalysis:
    return BandEquivalenceLocalityRepresentationEquivalenceAnalysis(
        spatial_dimension=2,
        retained_rank=2,
        maximum_direct_band_defect=0.0,
        maximum_covariant_defect=0.0,
        alignment_applicable=True,
        alignment_inapplicable_reason=None,
        restricted_global_rotation_angle=0.25,
        restricted_global_rotation_degenerate=False,
        splitting_scale=1.0,
        finite_mesh_maximum_correlation=0.75,
        analytic_flat_correlation=None,
        analytic_correlation_remainder_bound=None,
        correlation_quadrature_defect=None,
        minimum_operator_threshold=0.5,
        exact_spectrum_joint_operator_threshold=0.75,
        minimum_operator_threshold_over_sqrt_splitting=0.5,
        exact_spectrum_joint_threshold_over_sqrt_splitting=0.75,
        normalized_squared_operator_residual=0.25,
    )


class TestBandEquivalenceLocalityRepresentationEquivalenceAnalysis:
    """Keep equivalence ownership immutable, strict, and serialization-free."""

    def test_result__has_nominal_owner_without_wire_behavior(self) -> None:
        result = _applicable_result()

        assert isinstance(result, RepresentationEquivalence)
        assert not isinstance(result, BaseTypedRecord)
        assert not hasattr(result, "to_json")
        with pytest.raises(FrozenInstanceError):
            result.maximum_direct_band_defect = 1.0  # type: ignore[misc]

    def test_result__rejects_invalid_state_space_and_partial_analytic_bundle(
        self,
    ) -> None:
        with pytest.raises(TypeError, match="spatial_dimension"):
            replace(_applicable_result(), spatial_dimension=True)
        with pytest.raises(ValueError, match="retained_rank"):
            replace(_applicable_result(), retained_rank=3)
        with pytest.raises(TypeError, match="maximum_direct_band_defect"):
            replace(
                _applicable_result(),
                maximum_direct_band_defect=True,
            )
        with pytest.raises(ValueError, match=r"\[-1, 1\]"):
            replace(
                _applicable_result(),
                finite_mesh_maximum_correlation=1.01,
            )
        with pytest.raises(ValueError, match="all-or-none"):
            replace(
                _applicable_result(),
                analytic_flat_correlation=0.75,
            )

    def test_result__enforces_closed_alignment_applicability_bundle(self) -> None:
        with pytest.raises(ValueError, match="prohibits"):
            replace(
                _applicable_result(),
                alignment_applicable=False,
                alignment_inapplicable_reason="zero splitting scale",
            )

        inapplicable = replace(
            _applicable_result(),
            alignment_applicable=False,
            alignment_inapplicable_reason=(
                "zero splitting scale: normalized correlation is undefined"
            ),
            restricted_global_rotation_angle=None,
            restricted_global_rotation_degenerate=True,
            splitting_scale=0.0,
            finite_mesh_maximum_correlation=None,
            minimum_operator_threshold=0.0,
            exact_spectrum_joint_operator_threshold=0.0,
            minimum_operator_threshold_over_sqrt_splitting=None,
            exact_spectrum_joint_threshold_over_sqrt_splitting=None,
            normalized_squared_operator_residual=None,
        )

        assert not inapplicable.alignment_applicable
        assert inapplicable.finite_mesh_maximum_correlation is None
