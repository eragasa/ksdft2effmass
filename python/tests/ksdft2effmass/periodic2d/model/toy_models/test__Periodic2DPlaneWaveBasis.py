"""Software verification for the periodic2d plane-wave basis."""

import pytest

from ksdft2effmass.periodic2d.model.toy_models import (
    Periodic2DPlaneWaveBasis,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic2DPlaneWaveBasis:
    """Own finite reciprocal-basis ordering and invariant evidence."""

    def test_properties_expose_deterministic_square_basis(self) -> None:
        """A symmetric cutoff produces one deterministic square basis."""
        basis = Periodic2DPlaneWaveBasis(1)

        assert basis.ordering == "p_outer_q_inner"
        assert basis.represented_dimension == 9
        assert basis.reciprocal_indices[0] == (-1, -1)
        assert basis.reciprocal_indices[-1] == (1, 1)
        assert len(set(basis.reciprocal_indices)) == basis.represented_dimension

    def test_init_rejects_boolean_and_negative_cutoffs(self) -> None:
        """Only nonnegative built-in integer cutoffs define a basis."""
        with pytest.raises(TypeError, match="cutoff"):
            Periodic2DPlaneWaveBasis(True)
        with pytest.raises(ValueError, match="nonnegative"):
            Periodic2DPlaneWaveBasis(-1)
