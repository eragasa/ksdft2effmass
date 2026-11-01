"""Tests for the frozen higher-rank alignment configuration section."""

import json
from dataclasses import replace

import pytest
from projectkoios.optimization.alignment.procrustes import (
    ComplexUnitaryProcrustesRankCutoffRule,
)
from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransportPrincipalPhaseBranch,
    EndpointSewingAction,
    FrameRotationAction,
)

from ksdft2effmass.periodic1d.rankN.band_alignment.composite import (
    Periodic1DRankNAlignmentConfiguration,
    Periodic1DRankNGaugeAlignment,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


def _configuration() -> Periodic1DRankNAlignmentConfiguration:
    return Periodic1DRankNAlignmentConfiguration(
        family_identity=Periodic1DRankNAlignmentConfiguration.FAMILY_IDENTITY,
        version_identity=Periodic1DRankNAlignmentConfiguration.VERSION_IDENTITY,
        retained_ranks=(3, 4, 8, 16),
        circuit_depths=(1, 2, 4, 8),
        construction_mesh_sizes=(513, 1025, 2049),
        final_construction_mesh_size=2049,
        global_unitary_selection_mesh_size=2049,
        evaluation_mesh_size=8191,
        evaluation_shift_numerator=1,
        evaluation_shift_denominator=2,
        gauge_alignments=(
            Periodic1DRankNGaugeAlignment.IDENTITY,
            Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY,
            Periodic1DRankNGaugeAlignment.POINTWISE_UNITARY,
            Periodic1DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE,
        ),
        frame_rotation_action=FrameRotationAction.RIGHT,
        endpoint_sewing_action=EndpointSewingAction.LEFT_AMBIENT,
        principal_phase_branch=(
            ClosedLoopPolarFrameTransportPrincipalPhaseBranch.negative_pi_open
        ),
        rank_cutoff_rule=ComplexUnitaryProcrustesRankCutoffRule.MAXIMUM,
        rank_absolute_tolerance=1.0e-12,
        rank_relative_tolerance=1.0e-10,
        backend_validation_absolute_tolerance=1.0e-12,
        backend_validation_relative_tolerance=1.0e-10,
        endpoint_and_primitive_closure_tolerance=1.0e-11,
        maximum_closure_phase_tolerance=1.0e-10,
    )


class TestPeriodic1DRankNAlignmentConfiguration:
    """Establish exact controls, typed-wire behavior, and fail-closed validation."""

    def test__configuration__exposes_case_order_and_owner_tolerance(self) -> None:
        configuration = _configuration()

        assert len(configuration.case_order) == 16
        assert configuration.case_order[:5] == (
            "r03-L01",
            "r03-L02",
            "r03-L04",
            "r03-L08",
            "r04-L01",
        )
        assert configuration.case_order[-1] == "r16-L08"
        assert configuration.ambient_dimension(8) == 16
        tolerance = configuration.owner_transport_tolerance()
        assert tolerance.rank_absolute == 1.0e-12
        assert tolerance.rank_relative == 1.0e-10
        assert tolerance.validation_absolute == 1.0e-12
        assert tolerance.validation_relative == 1.0e-10
        assert tolerance.rank_cutoff_rule is (
            ComplexUnitaryProcrustesRankCutoffRule.MAXIMUM
        )

    def test__configuration__round_trips_through_the_canonical_typed_wire(self) -> None:
        configuration = _configuration()

        wire = configuration.to_json()
        geometry = configuration.reduced_lattice_geometry
        reconstructed = Periodic1DRankNAlignmentConfiguration.from_json(wire)

        assert geometry.lattice_period == 1.0
        assert configuration.to_json() == wire
        assert reconstructed == configuration
        assert reconstructed.to_json() == wire
        assert b'"principal_phase_branch": "(-pi, pi]"' in wire
        assert b'"global_unitary_selection_mesh_size": 2049' in wire
        assert b'"gauge_alignments"' in wire
        assert b'"identity"' in wire
        assert b'"global-unitary"' in wire
        assert b'"pointwise-unitary"' in wire
        assert b'"known-inverse-oracle"' in wire
        assert b'"channel"' not in wire
        assert all(
            old_value not in wire for old_value in (b'"A0"', b'"A1"', b'"A2"', b'"A3"')
        )

    def test__configuration_wire__rejects_old_keys_and_alignment_values(self) -> None:
        decoded = json.loads(_configuration().to_json())
        old_key = dict(decoded)
        old_key["channels"] = old_key.pop("gauge_alignments")
        old_key_wire = (json.dumps(old_key, indent=2, sort_keys=True) + "\n").encode()

        with pytest.raises(ValueError, match="fields do not match"):
            Periodic1DRankNAlignmentConfiguration.from_json(old_key_wire)

        for old_value in ("A0", "A1", "A2", "A3"):
            old_alignment = json.loads(_configuration().to_json())
            old_alignment["gauge_alignments"]["items"][0] = old_value
            old_alignment_wire = (
                json.dumps(old_alignment, indent=2, sort_keys=True) + "\n"
            ).encode()
            with pytest.raises(ValueError, match="unsupported gauge alignment"):
                Periodic1DRankNAlignmentConfiguration.from_json(old_alignment_wire)

    @pytest.mark.parametrize(
        ("field", "value", "error"),
        (
            ("retained_ranks", (3, 4, 8), ValueError),
            ("retained_ranks", (3, 4, 8, True), TypeError),
            ("construction_mesh_sizes", (513, 1024, 2049), ValueError),
            ("final_construction_mesh_size", True, TypeError),
            ("global_unitary_selection_mesh_size", 1025, ValueError),
            ("global_unitary_selection_mesh_size", True, TypeError),
            ("evaluation_mesh_size", "8191", TypeError),
            (
                "principal_phase_branch",
                ClosedLoopPolarFrameTransportPrincipalPhaseBranch.positive_pi_open,
                ValueError,
            ),
            (
                "rank_cutoff_rule",
                ComplexUnitaryProcrustesRankCutoffRule.ADDITIVE,
                ValueError,
            ),
            ("rank_absolute_tolerance", 1, TypeError),
            ("rank_relative_tolerance", 1.0e-9, ValueError),
        ),
    )
    def test__configuration__rejects_unsupported_alternatives(
        self,
        field: str,
        value: (
            tuple[int | bool, ...]
            | bool
            | int
            | str
            | float
            | ClosedLoopPolarFrameTransportPrincipalPhaseBranch
            | ComplexUnitaryProcrustesRankCutoffRule
        ),
        error: type[Exception],
    ) -> None:
        with pytest.raises(error):
            replace(_configuration(), **{field: value})  # type: ignore[arg-type]

    def test__ambient_dimension__rejects_unselected_rank_and_boolean(self) -> None:
        configuration = _configuration()

        with pytest.raises(ValueError, match="not in the frozen inventory"):
            configuration.ambient_dimension(5)
        with pytest.raises(TypeError, match="built-in integer"):
            configuration.ambient_dimension(True)
