"""Ownership tests for periodic-1D finite-rank represented fields."""

from importlib.util import find_spec

import pytest

from ksdft2effmass.periodic1d.rankN.represented_fields import (
    Periodic1DRankNRepresentedFieldConstructionRequest,
    Periodic1DRankNRepresentedFieldConstructor,
    Periodic1DRankNRepresentedFieldEvaluationRequest,
    Periodic1DRankNRepresentedFieldEvaluator,
    Periodic1DRankNRepresentedFields,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DRankNRepresentedFieldsOwnership:
    """Keep represented fields separate from gauge-alignment actions."""

    def test__types__belong_to_the_represented_field_owner(self) -> None:
        """Require construction, values, and evaluation to share one owner."""
        for value in (
            Periodic1DRankNRepresentedFieldConstructionRequest,
            Periodic1DRankNRepresentedFieldConstructor,
            Periodic1DRankNRepresentedFieldEvaluationRequest,
            Periodic1DRankNRepresentedFieldEvaluator,
            Periodic1DRankNRepresentedFields,
        ):
            assert value.__module__.endswith(".rankN.represented_fields")

    def test__obsolete_gauge_alignment_owner__is_absent(self) -> None:
        """Do not retain an alias at the former integrated field path."""
        assert (
            find_spec("ksdft2effmass.periodic1d.rankN.gauge_alignment.fields") is None
        )

    def test__analytic_case_composition__is_not_source_owned(self) -> None:
        """Keep analytic study composition in calculation or verification support."""
        assert (
            find_spec(
                "ksdft2effmass.periodic1d.rankN."
                "band_equivalence_hopping_locality.case"
            )
            is None
        )
