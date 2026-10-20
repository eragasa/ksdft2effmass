"""Software verification for :class:`NumpyFourierBlockField`."""

from __future__ import annotations

from typing import cast

import numpy as np
import pytest
from projectkoios.numerics.finite_periodic.meshes import CenteredUniformMesh

from ksdft2effmass.operators.representations.domains import (
    FiniteMomentumMeshDomain,
    FiniteTranslationDomain,
    MomentumSampleRole,
)
from ksdft2effmass.operators.representations.fields import (
    FourierBlockFieldABC,
    NumpyFourierBlockField,
)

pytestmark = pytest.mark.software_verification


class TestNumpyFourierBlockField:
    """Establish ordered translation correlation and exact domain type."""

    def test_construction__requires_translation_domain_and_retains_order(self) -> None:
        """Fourier blocks correlate only with the declared translation inventory."""
        domain = FiniteTranslationDomain(
            "symmetric-r1", ((-1,), (0,), (1,)), "integer-cell-translation.v1"
        )
        values = np.zeros((3, 2, 2), dtype=np.complex128)
        field = NumpyFourierBlockField(domain, values)

        assert isinstance(field, FourierBlockFieldABC)
        assert field.domain.translations == ((-1,), (0,), (1,))
        assert field.dimension == 2

        momentum = FiniteMomentumMeshDomain(
            "mesh",
            CenteredUniformMesh(1, 3, (0.0,)),
            "centered-reduced-reciprocal.v1",
            MomentumSampleRole.general,
        )
        with pytest.raises(TypeError, match="FiniteTranslationDomain"):
            NumpyFourierBlockField(
                cast(FiniteTranslationDomain, momentum),
                values,
            )
