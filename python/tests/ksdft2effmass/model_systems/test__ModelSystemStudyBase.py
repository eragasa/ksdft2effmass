"""Software verification for the shared nominal model-system study boundary."""

from __future__ import annotations

import pytest
from projectkoios.physkit.qm.piab1d import Piab1D
from projectkoios.physkit.units import UnitSystem

from ksdft2effmass.model_systems.piab1d import Piab1dStudyDefinition
from ksdft2effmass.model_systems.qho1d import (
    Qho1dNondimensionalizer,
    Qho1dStudyDefinition,
)
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
    def qho1d_definition() -> Qho1dStudyDefinition:
        return Qho1dStudyDefinition(
            experiment_id="qho1d.development.v1",
            evidence_status="illustrative numerical experiment",
            parameters=Qho1dNondimensionalizer().execute(1.0, 1.0, 1.0),
            box_half_widths=(4.0,),
            grid_spacings=(0.1,),
            retained_dimensions=(2,),
            spatial_representation="finite Dirichlet grid",
            comparison_map="sampled-state injection",
        )

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

    def test_method__study_identity__supports_qho1d_and_piab1d(self) -> None:
        qho1d = self.qho1d_definition()
        piab1d = self.piab1d_definition()

        assert isinstance(qho1d, ModelSystemStudyBase)
        assert isinstance(piab1d, ModelSystemStudyBase)
        assert model_system_study_identity(qho1d) == ModelSystemStudyIdentity(
            ModelId.qho1d,
            ModelSystemStudySchemaId.qho1d_v1,
        )
        assert model_system_study_identity(piab1d) == ModelSystemStudyIdentity(
            ModelId.piab1d,
            ModelSystemStudySchemaId.piab1d_v2,
        )
