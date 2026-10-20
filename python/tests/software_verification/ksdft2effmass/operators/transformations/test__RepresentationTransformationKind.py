"""Software verification for :class:`RepresentationTransformationKind`."""

from __future__ import annotations

import pytest

from ksdft2effmass.operators.transformations.identities import (
    RepresentationTransformationKind,
)

pytestmark = pytest.mark.software_verification


class TestRepresentationTransformationKind:
    """Establish the explicit nontext derivation-edge kind inventory."""

    def test_members__cover_the_declared_representation_transformations(self) -> None:
        """Every supported edge kind is a visible snake-case enum choice."""
        assert tuple(RepresentationTransformationKind) == (
            RepresentationTransformationKind.frame_compression,
            RepresentationTransformationKind.gauge_conjugation,
            RepresentationTransformationKind.alignment,
            RepresentationTransformationKind.finite_fourier_conversion,
            RepresentationTransformationKind.support_truncation,
            RepresentationTransformationKind.fourier_reconstruction,
        )
        assert all(
            not isinstance(member.value, str)
            for member in RepresentationTransformationKind
        )
