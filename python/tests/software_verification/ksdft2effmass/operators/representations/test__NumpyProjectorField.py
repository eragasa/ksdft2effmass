"""Software verification for :class:`NumpyProjectorField`."""

from __future__ import annotations

import numpy as np
import pytest
from projectkoios.numerics.finite_periodic.meshes import CenteredUniformMesh

from ksdft2effmass.operators.representations.domains import (
    FiniteMomentumMeshDomain,
    MomentumSampleRole,
)
from ksdft2effmass.operators.representations.fields import (
    NumpyProjectorField,
    ProjectorFieldABC,
)

pytestmark = pytest.mark.software_verification


class TestNumpyProjectorField:
    """Establish projector-role semantics without inferred projector identities."""

    def test_construction__accepts_nonprojector_role_data(self) -> None:
        """The class declares intended role but does not infer idempotency."""
        domain = FiniteMomentumMeshDomain(
            "mesh",
            CenteredUniformMesh(1, 3, (0.0,)),
            "centered-reduced-reciprocal.v1",
            MomentumSampleRole.general,
        )
        values = np.full((3, 2, 2), 2.0 + 0.0j, dtype=np.complex128)
        field = NumpyProjectorField(domain, values)

        assert isinstance(field, ProjectorFieldABC)
        assert field.source_dimension == field.target_dimension == 2
        assert field.values[0, 0, 0] == 2.0
