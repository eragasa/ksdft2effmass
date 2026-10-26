"""Software verification for the shared nominal model-system study boundary."""

from __future__ import annotations

import pytest
from projectkoios.physkit.qm.piab1d import Piab1D
from projectkoios.physkit.units import UnitSystem

from ksdft2effmass.model_systems.piab1d import Piab1dStudyDefinition
from ksdft2effmass.model_systems.study import (
    ModelId,
    ModelSystemStudyBase,
    ModelSystemStudyIdentity,
    ModelSystemStudySchemaId,
    model_system_study_identity,
)

pytestmark = pytest.mark.software_verification
SUT = ModelSystemStudyBase


class TestModelSystemStudyBase:
    """Own software evidence for the shared nominal study boundary."""

    @staticmethod
    def piab1d_definition() -> Piab1dStudyDefinition:
        return Piab1dStudyDefinition(
            model=Piab1D(
                length=1.0,
                mass=1.0,
                unit_system=UnitSystem.NONDIMENSIONAL,
            ),
            Nx_pts_interior=4,
            N_retained_eigenpairs=2,
        )

    def test_method__study_identity__supports_piab1d(self) -> None:
        piab1d = self.piab1d_definition()

        assert isinstance(piab1d, ModelSystemStudyBase)
        assert model_system_study_identity(piab1d) == ModelSystemStudyIdentity(
            ModelId.piab1d,
            ModelSystemStudySchemaId.piab1d_v2,
        )
