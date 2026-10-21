r"""Software verification of the version-two PIAB1D study definition."""

import pytest
from projectkoios.physkit.qm.piab1d import Piab1D
from projectkoios.physkit.units import UnitSystem

from ksdft2effmass.model_systems.piab1d import Piab1dStudyDefinition
from ksdft2effmass.model_systems.study import ModelSystemStudySchemaId

pytestmark = pytest.mark.software_verification
SUT = Piab1dStudyDefinition


def _model() -> Piab1D:
    return Piab1D(
        length=1.0,
        mass=1.0,
        unit_system=UnitSystem.NONDIMENSIONAL,
    )


class TestPiab1dStudyDefinition:
    """Own software evidence for ``Piab1dStudyDefinition``."""

    def test_constructor__default_quadrature__is_enabled(self) -> None:
        definition = Piab1dStudyDefinition(
            model=_model(),
            Nx_pts_interior=8,
            N_retained_eigenpairs=3,
        )

        assert definition.quadrature is True
        assert definition.schema_id is ModelSystemStudySchemaId.piab1d_v2

    def test_constructor__quadrature_type__rejects_integer(self) -> None:
        with pytest.raises(TypeError, match="quadrature"):
            Piab1dStudyDefinition(
                model=_model(),
                Nx_pts_interior=8,
                N_retained_eigenpairs=3,
                quadrature=1,  # type: ignore[arg-type]
            )

    def test_constructor__dimension_contract__rejects_oversized_retention(self) -> None:
        with pytest.raises(ValueError, match="not exceed"):
            Piab1dStudyDefinition(
                model=_model(),
                Nx_pts_interior=3,
                N_retained_eigenpairs=4,
            )
