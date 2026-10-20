"""Software verification for :class:`NumpyFrameField`."""

from __future__ import annotations

import numpy as np
import pytest
from projectkoios.numerics.finite_periodic.meshes import CenteredUniformMesh

from ksdft2effmass.operators.representations.domains import (
    FiniteMomentumMeshDomain,
    MomentumSampleRole,
)
from ksdft2effmass.operators.representations.fields import (
    FrameFieldABC,
    NumpyFrameField,
)

pytestmark = pytest.mark.software_verification


class TestNumpyFrameField:
    """Establish rectangular target-row/source-column orientation."""

    def test_construction__retains_source_and_target_dimensions(self) -> None:
        """Frame columns are source coordinates and rows are target coordinates."""
        domain = FiniteMomentumMeshDomain(
            "mesh",
            CenteredUniformMesh(1, 3, (0.0,)),
            "centered-reduced-reciprocal.v1",
            MomentumSampleRole.general,
        )
        field = NumpyFrameField(domain, np.zeros((3, 5, 2), dtype=np.complex128))

        assert isinstance(field, FrameFieldABC)
        assert field.source_dimension == 2
        assert field.target_dimension == 5
