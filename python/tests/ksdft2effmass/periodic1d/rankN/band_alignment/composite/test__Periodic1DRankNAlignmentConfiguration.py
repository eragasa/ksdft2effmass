"""Tests for the frozen higher-rank alignment configuration section."""

from dataclasses import replace

import numpy as np
import pytest
from projectkoios.optimization.alignment.procrustes import (
    ComplexUnitaryProcrustesRankCutoffRule,
)
from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransportPrincipalPhaseBranch,
)

from ksdft2effmass.periodic1d.rankN.band_alignment.configuration import (
    Periodic1DRankNAlignmentConfiguration,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


def _configuration() -> Periodic1DRankNAlignmentConfiguration:
    return Periodic1DRankNAlignmentConfiguration.frozen()


class TestPeriodic1DRankNAlignmentConfiguration:
    """Establish exact controls, typed-wire behavior, and fail-closed validation."""

    def test__frozen__returns_the_complete_authoritative_configuration(self) -> None:
        configuration = Periodic1DRankNAlignmentConfiguration.frozen()

        assert configuration.retained_ranks == configuration.RETAINED_RANKS
        assert (
            configuration.frame_rotation_action is configuration.FRAME_ROTATION_ACTION
        )
        assert (
            configuration.principal_phase_branch is configuration.PRINCIPAL_PHASE_BRANCH
        )
        assert configuration.to_json() == _configuration().to_json()

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

    def test__configuration__owns_declared_construction_coordinates(self) -> None:
        configuration = _configuration()

        construction = configuration.construction_coordinates(513)
        selection = configuration.global_unitary_selection_coordinates()

        assert construction.shape == (513,)
        assert construction[0] == -0.5
        assert construction[-1] == pytest.approx(0.5 - 1.0 / 513.0)
        assert not construction.flags.writeable
        assert np.array_equal(
            selection,
            configuration.construction_coordinates(2049),
        )
        with pytest.raises(TypeError, match="built-in integer"):
            configuration.construction_coordinates(True)
        with pytest.raises(ValueError, match="construction-mesh inventory"):
            configuration.construction_coordinates(511)

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
        old_key = dict(_configuration().to_dict())
        old_key["channels"] = old_key.pop("gauge_alignments")

        with pytest.raises(ValueError, match="fields do not match"):
            Periodic1DRankNAlignmentConfiguration.from_dict(old_key)

        for old_value in ("A0", "A1", "A2", "A3"):
            old_alignment = dict(_configuration().to_dict())
            gauge_alignments = old_alignment["gauge_alignments"]
            assert isinstance(gauge_alignments, tuple)
            old_alignment["gauge_alignments"] = (
                old_value,
                *gauge_alignments[1:],
            )
            with pytest.raises(
                ValueError,
                match="unsupported Periodic1DRankNGaugeAlignment",
            ):
                Periodic1DRankNAlignmentConfiguration.from_dict(old_alignment)

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
