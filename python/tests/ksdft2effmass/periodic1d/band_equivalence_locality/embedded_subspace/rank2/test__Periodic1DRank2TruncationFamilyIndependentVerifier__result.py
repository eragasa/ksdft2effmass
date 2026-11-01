"""Tests for independent parent-family truncation verification."""

from __future__ import annotations

import importlib
import math
from dataclasses import replace

import pytest
from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransporter,
)

from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.parent_family.analysis import (  # noqa: E501
    Periodic1DRank2ParentFamilyRequest,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.parent_scale.request import (  # noqa: E501
    Periodic1DRank2Request,
)
from ksdft2effmass.periodic1d.rank2.support_truncation.family import (
    Periodic1DRank2TruncationFamilyAnalysis,
    Periodic1DRank2TruncationFamilyAnalyzer,
    Periodic1DRank2TruncationFamilyRequest,
)
from ksdft2effmass.periodic1d.rank2.support_truncation.family_verification import (
    Periodic1DRank2TruncationFamilyIndependentVerifier,
)
from ksdft2effmass.periodic1d.rank2.support_truncation.results import (
    Periodic1DRank2TruncationCompleted,
    Periodic1DRank2TruncationRange,
)
from ksdft2effmass.real_space_support_truncation import (
    MinimumToleranceSatisfyingSupport,
)

pytestmark = [pytest.mark.integration, pytest.mark.numerical_verification]


def _analyze() -> Periodic1DRank2TruncationFamilyAnalysis:
    template = Periodic1DRank2Request(
        reciprocal_mesh_size=8,
        amplitudes=(0.0, 0.2, math.pi / 4.0),
        parent_hopping_scale=1.0,
        minimum_external_gap=0.1,
        minimum_transport_singular_value=0.8,
        frame_absolute_tolerance=1.0e-10,
        transport_rank_relative_tolerance=1.0e-12,
        transport_validation_relative_tolerance=1.0e-10,
        harmonic_absolute_degeneracy_tolerance=1.0e-14,
        harmonic_relative_degeneracy_tolerance=1.0e-12,
    )
    request = Periodic1DRank2TruncationFamilyRequest.every_integer_through(
        parent_family_request=Periodic1DRank2ParentFamilyRequest(
            template_request=template,
            parent_hopping_scales=(0.0, 1.0),
        ),
        maximum_range=3,
        evaluation_mesh_size=17,
        support_tolerance=1.0,
    )
    return Periodic1DRank2TruncationFamilyAnalyzer(
        request=request,
        transporter=ClosedLoopPolarFrameTransporter(),
    ).execute()


def _replace_error(
    range_result: Periodic1DRank2TruncationRange,
    name: str,
    value: float,
) -> Periodic1DRank2TruncationRange:
    if name == "reference_truncation_hamiltonian_maximum_error":
        return replace(
            range_result,
            reference_truncation_hamiltonian_maximum_error=value,
        )
    if name == "reference_truncation_spectral_maximum_error":
        return replace(
            range_result,
            reference_truncation_spectral_maximum_error=value,
        )
    if name == "comparison_total_hamiltonian_maximum_error":
        return replace(
            range_result,
            comparison_total_hamiltonian_maximum_error=value,
        )
    if name == "comparison_total_spectral_maximum_error":
        return replace(
            range_result,
            comparison_total_spectral_maximum_error=value,
        )
    raise ValueError("unsupported test error channel")


class TestPeriodic1DRank2TruncationFamilyIndependentVerifier:
    """Establish independent member and support-decision reconstruction."""

    def test_result__passes_for_members_and_derived_support_decisions(self) -> None:
        verification = Periodic1DRank2TruncationFamilyIndependentVerifier(
            _analyze()
        ).result()

        assert verification.passed
        assert "member_0_outcome_variant_defect" in verification.observations
        assert (
            "member_1_point_2_comparison_matrix_frobenius_maximum"
            "_support_selection_defect"
        ) in verification.observations

    def test_result__does_not_call_production_family_or_member_analyzers(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        observed = _analyze()
        module_root = "ksdft2effmass.periodic1d.rank2.support_truncation"
        family_module = importlib.import_module(f"{module_root}.family")
        truncation_module = importlib.import_module(f"{module_root}.analysis")
        tolerance_module = importlib.import_module(f"{module_root}.tolerance_selection")
        generic_tolerance_module = importlib.import_module(
            "ksdft2effmass.real_space_support_truncation.tolerance_selection"
        )

        def forbidden(*_args: object, **_kwargs: object) -> None:
            raise AssertionError("independent verification called a production action")

        monkeypatch.setattr(
            family_module.Periodic1DRank2TruncationFamilyAnalyzer,
            "execute",
            forbidden,
        )
        monkeypatch.setattr(
            truncation_module.Periodic1DRank2TruncationAnalyzer,
            "execute",
            forbidden,
        )
        monkeypatch.setattr(
            family_module.Periodic1DRank2TruncationFamilyRequest,
            "request_at",
            forbidden,
        )
        monkeypatch.setattr(
            tolerance_module.Periodic1DRank2TruncationToleranceSelector,
            "execute",
            forbidden,
        )
        monkeypatch.setattr(
            generic_tolerance_module.RealSpaceSupportTruncationToleranceSelector,
            "execute",
            forbidden,
        )

        verification = Periodic1DRank2TruncationFamilyIndependentVerifier(
            observed
        ).result()

        assert verification.passed

    @pytest.mark.parametrize(
        (
            "model_name",
            "outcome_name",
            "range_error_name",
            "observation_channel",
        ),
        (
            (
                "reference_model",
                "matrix_frobenius_maximum_error",
                "reference_truncation_hamiltonian_maximum_error",
                "reference_matrix_frobenius_maximum",
            ),
            (
                "reference_model",
                "ordered_eigenvalue_maximum_absolute_error",
                "reference_truncation_spectral_maximum_error",
                "reference_ordered_eigenvalue_maximum_absolute",
            ),
            (
                "comparison_model",
                "matrix_frobenius_maximum_error",
                "comparison_total_hamiltonian_maximum_error",
                "comparison_matrix_frobenius_maximum",
            ),
            (
                "comparison_model",
                "ordered_eigenvalue_maximum_absolute_error",
                "comparison_total_spectral_maximum_error",
                "comparison_ordered_eigenvalue_maximum_absolute",
            ),
        ),
    )
    def test_result__detects_tampered_error_and_changed_support_decision(
        self,
        model_name: str,
        outcome_name: str,
        range_error_name: str,
        observation_channel: str,
    ) -> None:
        observed = _analyze()
        member = observed.members[0]
        assert type(member) is Periodic1DRank2TruncationCompleted
        point_index = len(member.points) - 1
        point = member.points[point_index]
        selection = observed.support_tolerance_selections_by_member[0][point_index]
        selected = getattr(getattr(selection, model_name), outcome_name)
        if type(selected) is MinimumToleranceSatisfyingSupport:
            range_index = selected.comparison_index
            changed_error = observed.request.support_tolerance + 10.0
        else:
            range_index = 0
            changed_error = 0.0
        range_result = point.ranges[range_index]
        tampered_range = _replace_error(
            range_result,
            range_error_name,
            changed_error,
        )
        tampered_point = replace(
            point,
            ranges=(
                *point.ranges[:range_index],
                tampered_range,
                *point.ranges[range_index + 1 :],
            ),
        )
        if model_name == "reference_model":
            tampered_points = tuple(
                replace(
                    candidate_point,
                    ranges=(
                        *candidate_point.ranges[:range_index],
                        _replace_error(
                            candidate_point.ranges[range_index],
                            range_error_name,
                            changed_error,
                        ),
                        *candidate_point.ranges[range_index + 1 :],
                    ),
                )
                for candidate_point in member.points
            )
        else:
            tampered_points = (
                *member.points[:point_index],
                tampered_point,
            )
        tampered_member = replace(member, points=tampered_points)
        first_family_member = replace(
            observed.truncation_family.members[0],
            outcome=tampered_member,
        )
        tampered_family = replace(
            observed.truncation_family,
            members=(
                first_family_member,
                observed.truncation_family.members[1],
            ),
        )
        tampered = Periodic1DRank2TruncationFamilyAnalysis(
            request=observed.request,
            truncation_family=tampered_family,
        )

        verification = Periodic1DRank2TruncationFamilyIndependentVerifier(
            tampered
        ).result()

        assert not verification.passed
        assert not verification.observations[
            "member_0_range_scalar_maximum_absolute_defect"
        ].passed
        decision_name = (
            f"member_0_point_{point_index}_{observation_channel}"
            "_support_selection_defect"
        )
        assert not verification.observations[decision_name].passed
