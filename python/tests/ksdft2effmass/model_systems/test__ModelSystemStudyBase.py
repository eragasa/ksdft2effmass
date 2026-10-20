"""Software verification for the shared nominal model-system study boundary."""

from __future__ import annotations

import pytest
from ksdft2effmass.model_systems.piab1d import Piab1dStudyDefinition
from ksdft2effmass.model_systems.qho1d import (
    QHO1DNondimensionalizer,
    QHO1DStudyDefinition,
)
from ksdft2effmass.model_systems.study import (
    ModelSystemStudyBase,
    ModelSystemStudyIdentity,
    model_system_study_identity,
)

pytestmark = pytest.mark.software_verification
SUT = ModelSystemStudyBase


class TestModelSystemStudyBase:
    """Own software evidence for the shared nominal study boundary."""

    @staticmethod
    def qho1d_definition() -> QHO1DStudyDefinition:
        """Return one valid concrete QHO1D study definition."""
        return QHO1DStudyDefinition(
            study_id="qho1d.test.v1",
            evidence_status="illustrative numerical experiment",
            parameters=QHO1DNondimensionalizer().execute(1.0, 1.0, 1.0),
            box_half_widths=(4.0,),
            grid_spacings=(0.1,),
            retained_dimensions=(2,),
            spatial_representation="finite Dirichlet grid",
            comparison_map="sampled-state injection",
        )

    @staticmethod
    def piab1d_definition() -> Piab1dStudyDefinition:
        """Return one valid concrete PIAB1D study definition."""
        return Piab1dStudyDefinition(
            schema_version=1,
            experiment_id="piab1d.test.v1",
            evidence_status="illustrative numerical experiment",
            length=1.0,
            mass=1.0,
            hbar=1.0,
            interior_points=4,
            retained_dimension=2,
            boundary_kind="cyclic closure on the same finite coordinate space",
            boundary_interpretation=(
                "Declared comparison reference only; not a "
                "representation-independent continuum potential."
            ),
        )

    def test_method__study_identity__supports_qho1d_and_piab1d(self) -> None:
        """Both maintained controlled systems implement the nominal contract."""
        qho1d = self.qho1d_definition()
        piab1d = self.piab1d_definition()

        assert isinstance(qho1d, ModelSystemStudyBase)
        assert isinstance(piab1d, ModelSystemStudyBase)
        assert model_system_study_identity(qho1d) == ModelSystemStudyIdentity(
            "qho1d.test.v1", "illustrative numerical experiment"
        )
        assert model_system_study_identity(piab1d) == ModelSystemStudyIdentity(
            "piab1d.test.v1", "illustrative numerical experiment"
        )
