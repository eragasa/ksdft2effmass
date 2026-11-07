"""Software verification of the abstract scientific sewing categories."""

from __future__ import annotations

from inspect import isabstract

import pytest

from ksdft2effmass.sewing import (
    EmbeddedPositionReciprocalSewing,
    FiniteBoundarySewing,
    IdentityReciprocalSewing,
    PermutationPhaseReciprocalSewing,
    PlaneWaveIndexSewing,
    ProjectedSubspaceSewing,
    SymmetrySewing,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]

type SewingCategory = (
    IdentityReciprocalSewing
    | EmbeddedPositionReciprocalSewing
    | PermutationPhaseReciprocalSewing
    | PlaneWaveIndexSewing
    | ProjectedSubspaceSewing
    | SymmetrySewing
    | FiniteBoundarySewing
)


class TestSewing:
    """Preserve each sewing problem as a separate abstract class."""

    @pytest.mark.parametrize(
        "sewing_type",
        (
            IdentityReciprocalSewing,
            EmbeddedPositionReciprocalSewing,
            PermutationPhaseReciprocalSewing,
            PlaneWaveIndexSewing,
            ProjectedSubspaceSewing,
            SymmetrySewing,
            FiniteBoundarySewing,
        ),
    )
    def test__category__is_abstract(self, sewing_type: type[SewingCategory]) -> None:
        """Require each scientific sewing category to remain non-instantiable.

        Parameters
        ----------
        sewing_type
            Exact sewing category under verification.

        """
        assert isabstract(sewing_type)

        with pytest.raises(TypeError, match="abstract"):
            sewing_type()
