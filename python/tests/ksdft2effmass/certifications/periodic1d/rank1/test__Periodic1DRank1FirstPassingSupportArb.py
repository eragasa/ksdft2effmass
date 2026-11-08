"""Software tests for the optional Arb parent and mediated enclosures."""

from fractions import Fraction

import numpy as np
import pytest

pytest.importorskip("flint")
from flint import ctx

from ksdft2effmass.certifications.periodic1d.rank1.first_passing_support import (
    ExactRational,
)
from ksdft2effmass.certifications.periodic1d.rank1.first_passing_support.arb import (
    ControlledParentLowestEigenvalueArbEncloser,
    ControlledParentLowestEigenvalueEnclosure,
    MediatedMaximumErrorArbEncloser,
    MediatedMaximumErrorEnclosure,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DRank1FirstPassingSupportArb:
    """Establish local parent and mediated Arb enclosure behavior."""

    def test__parent_encloser__agrees_with_binary64_control(self) -> None:
        previous_precision = ctx.prec
        result = ControlledParentLowestEigenvalueArbEncloser(
            reduced_momentum=ExactRational(0, 1),
            working_precision_bits=128,
        ).execute()
        onsite = np.asarray(
            [
                [-1.20, 0.06, 0.00, 0.00],
                [0.06, -0.35, 0.00, 0.00],
                [0.00, 0.00, 1.00, 0.04],
                [0.00, 0.00, 0.04, 1.75],
            ],
            dtype=np.float64,
        )
        hopping = np.asarray(
            [
                [0.15, 0.00, 0.12, 0.00],
                [0.00, -0.10, 0.00, 0.10],
                [0.00, 0.00, 0.05, 0.00],
                [0.00, 0.00, 0.00, -0.04],
            ],
            dtype=np.float64,
        )
        control = float(np.linalg.eigvalsh(onsite + hopping + hopping.T)[0])
        lower = result.interval.lower.as_fraction()
        upper = result.interval.upper.as_fraction()
        midpoint = float((lower + upper) / 2)

        assert ctx.prec == previous_precision
        assert lower <= upper
        assert midpoint == pytest.approx(control, abs=1.0e-14, rel=0.0)

    def test__mediated_encloser__separates_supports_ten_and_eleven(self) -> None:
        support_ten = MediatedMaximumErrorArbEncloser(
            maximum_range=10,
            working_precision_bits=128,
        ).execute()
        support_eleven = MediatedMaximumErrorArbEncloser(
            maximum_range=11,
            working_precision_bits=128,
        ).execute()
        threshold = Fraction(1, 100_000_000)

        assert support_ten.interval.lower.as_fraction() > threshold
        assert support_eleven.interval.upper.as_fraction() <= threshold
        assert support_ten.construction_mesh_size == 256
        assert support_ten.evaluation_mesh_size == 1025
        assert support_eleven.lower_witness_index == 512
        assert support_eleven.upper_driver_index == 512

    def test__enclosure_records__round_trip_canonical_bytes(self) -> None:
        parent = ControlledParentLowestEigenvalueArbEncloser(
            reduced_momentum=ExactRational(1, 7),
            working_precision_bits=128,
        ).execute()
        mediated = MediatedMaximumErrorArbEncloser(
            maximum_range=11,
            working_precision_bits=128,
        ).execute()

        assert (
            ControlledParentLowestEigenvalueEnclosure.from_json(parent.to_json())
            == parent
        )
        assert MediatedMaximumErrorEnclosure.from_json(mediated.to_json()) == mediated
