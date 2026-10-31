"""Tests for independent parent-family momentum-refinement verification."""

from __future__ import annotations

import importlib
import math
from dataclasses import replace

import pytest
from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransporter,
)

from ksdft2effmass.periodic1d import (
    Periodic1DEmbeddedSubspaceRank2MomentumRefinementConverged,
    Periodic1DEmbeddedSubspaceRank2MomentumRefinementFamilyAnalysis,
    Periodic1DEmbeddedSubspaceRank2MomentumRefinementFamilyAnalyzer,
    Periodic1DEmbeddedSubspaceRank2MomentumRefinementFamilyIndependentVerifier,
    Periodic1DEmbeddedSubspaceRank2MomentumRefinementFamilyRequest,
    Periodic1DEmbeddedSubspaceRank2MomentumRefinementThresholds,
    Periodic1DEmbeddedSubspaceRank2ParentFamilyRequest,
    Periodic1DEmbeddedSubspaceRank2Request,
)


def _analyze() -> Periodic1DEmbeddedSubspaceRank2MomentumRefinementFamilyAnalysis:
    template = Periodic1DEmbeddedSubspaceRank2Request(
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
    thresholds = Periodic1DEmbeddedSubspaceRank2MomentumRefinementThresholds(
        maximum_parent_diagnostic_change=1.0,
        maximum_correlation_change=1.0,
        maximum_threshold_change=1.0,
        maximum_hopping_weight_change=1.0,
        maximum_hopping_power_change=1.0,
        maximum_angle_change=1.0,
        maximum_band_defect=1.0,
        maximum_reconstruction_defect=1.0,
        maximum_parseval_defect=1.0,
    )
    request = Periodic1DEmbeddedSubspaceRank2MomentumRefinementFamilyRequest(
        parent_family_request=Periodic1DEmbeddedSubspaceRank2ParentFamilyRequest(
            template_request=template,
            parent_hopping_scales=(0.0, 1.0),
        ),
        reciprocal_mesh_sizes=(8, 16),
        thresholds=thresholds,
        required_stable_refinements=1,
    )
    return Periodic1DEmbeddedSubspaceRank2MomentumRefinementFamilyAnalyzer(
        request=request,
        transporter=ClosedLoopPolarFrameTransporter(),
    ).execute()


class TestPeriodic1DEmbeddedSubspaceRank2MomentumRefinementFamilyIndependentVerifier:
    """Establish independent family reconstruction and tamper detection."""

    def test_result__passes_for_every_independently_rebuilt_member(self) -> None:
        verification = (
            Periodic1DEmbeddedSubspaceRank2MomentumRefinementFamilyIndependentVerifier(  # noqa: E501
                _analyze()
            ).result()
        )

        assert verification.passed
        assert "member_0_outcome_variant_defect" in verification.observations
        assert "member_1_refinement_0_maximum_correlation_change_absolute_defect" in (
            verification.observations
        )

    def test_result__does_not_call_production_family_or_member_analyzers(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        observed = _analyze()
        module_root = (
            "ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2"
        )
        family_module = importlib.import_module(
            f"{module_root}.momentum_refinement_family"
        )
        refinement_module = importlib.import_module(f"{module_root}.refinement")

        def forbidden(*_args: object, **_kwargs: object) -> None:
            raise AssertionError("independent verification called a production action")

        monkeypatch.setattr(
            family_module.Periodic1DEmbeddedSubspaceRank2MomentumRefinementFamilyAnalyzer,
            "execute",
            forbidden,
        )
        monkeypatch.setattr(
            refinement_module.Periodic1DEmbeddedSubspaceRank2MomentumRefinementAnalyzer,
            "execute",
            forbidden,
        )
        monkeypatch.setattr(
            refinement_module.Periodic1DEmbeddedSubspaceRank2MomentumRefinementRequest,
            "request_at",
            forbidden,
        )

        verification = (
            Periodic1DEmbeddedSubspaceRank2MomentumRefinementFamilyIndependentVerifier(  # noqa: E501
                observed
            ).result()
        )

        assert verification.passed

    def test_result__detects_a_tampered_member_refinement_metric(self) -> None:
        observed = _analyze()
        member = observed.members[0]
        assert type(member) is (
            Periodic1DEmbeddedSubspaceRank2MomentumRefinementConverged
        )
        tampered_step = replace(
            member.refinements[0],
            maximum_correlation_change=(
                member.refinements[0].maximum_correlation_change + 1.0e-5
            ),
        )
        tampered_member = replace(member, refinements=(tampered_step,))
        first_family_member = replace(
            observed.refinement_family.members[0],
            outcome=tampered_member,
        )
        tampered_family = replace(
            observed.refinement_family,
            members=(first_family_member, observed.refinement_family.members[1]),
        )
        tampered = replace(observed, refinement_family=tampered_family)

        verification = (
            Periodic1DEmbeddedSubspaceRank2MomentumRefinementFamilyIndependentVerifier(  # noqa: E501
                tampered
            ).result()
        )

        assert not verification.passed
        assert not verification.observations[
            "member_0_refinement_0_maximum_correlation_change_absolute_defect"
        ].passed
