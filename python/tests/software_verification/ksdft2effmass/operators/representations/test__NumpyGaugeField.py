"""Software verification for :class:`NumpyGaugeField`."""

from __future__ import annotations

import numpy as np
import pytest
from projectkoios.numerics.finite_periodic.meshes import CenteredUniformMesh

from ksdft2effmass.operators.representations.domains import (
    FiniteMomentumMeshDomain,
    MomentumSampleRole,
)
from ksdft2effmass.operators.representations.fields import (
    GaugeFieldABC,
    NumpyGaugeField,
)

pytestmark = pytest.mark.software_verification


class TestNumpyGaugeField:
    """Establish gauge-role semantics without inferred unitarity."""

    def test_construction__accepts_nonunitary_role_data(self) -> None:
        """A zero matrix field is valid storage and not promoted to a unitary map."""
        domain = FiniteMomentumMeshDomain(
            "mesh",
            CenteredUniformMesh(1, 3, (0.0,)),
            "centered-reduced-reciprocal.v1",
            MomentumSampleRole.general,
        )
        field = NumpyGaugeField(domain, np.zeros((3, 2, 2), dtype=np.complex128))

        assert isinstance(field, GaugeFieldABC)
        assert field.source_dimension == field.target_dimension == 2
        assert np.count_nonzero(field.values) == 0
