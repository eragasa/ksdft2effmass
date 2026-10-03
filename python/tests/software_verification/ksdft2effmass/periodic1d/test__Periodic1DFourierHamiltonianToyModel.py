"""Software verification of ``Periodic1DFourierHamiltonianToyModel``.

Evidence profile: routine

Facet and represented meaning
-----------------------------
The class represents an identified untruncated quadratic-kinetic periodic Fourier toy
parent rather than a finite matrix representation.

Intrinsic and cross-object scope
--------------------------------
Exact nominal membership, role, component identities, positive recoil scale, and unit
compatibility are covered using public records.

VVUQ and scientific exclusions
------------------------------
Inputs are synthetic. Passing establishes software behavior only, not numerical
verification, material realism, scientific validation, or uncertainty quantification.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis.model_systems import PeriodicFourierPotential1D
from ksdft2effmass.operators import (
    PhysicalUnit,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.periodic import (
    Periodic1DModel,
    PeriodicModelRole,
    PeriodicToyModelCatalog,
)
from ksdft2effmass.periodic1d import Periodic1DFourierHamiltonianToyModel

pytestmark = pytest.mark.software_verification


class TestPeriodic1DFourierHamiltonianToyModel:
    """Own software evidence for the complete periodic Fourier toy parent."""

    @staticmethod
    def make_potential() -> PeriodicFourierPotential1D:
        """Return one synthetic dimensionless cosine potential."""
        return PeriodicFourierPotential1D(
            ScalarQuantity(2.0 * np.pi, Unitless()),
            ScalarQuantity(0.0, Unitless()),
            VectorQuantity(np.asarray([0.5], dtype=np.float64), Unitless()),
            VectorQuantity(np.asarray([0.0], dtype=np.float64), Unitless()),
        )

    @classmethod
    def make_model(cls) -> Periodic1DFourierHamiltonianToyModel:
        """Return one complete synthetic parent."""
        return Periodic1DFourierHamiltonianToyModel(
            "test.periodic1d.fourier-parent",
            "test.periodic1d.bloch-state-space",
            "test.periodic1d.primitive-reduced-zone",
            cls.make_potential(),
            ScalarQuantity(1.0, Unitless()),
        )

    def test_construction__parent__binds_complete_nominal_toy_identity(self) -> None:
        """Evidence ID: SV-PERIODIC1D-FOURIER-MODEL-001

        Requirement: The complete parent binds stable model, state-space, reciprocal
        domain, potential, and recoil identities with nominal one-dimensional toy role.

        Acceptance: Every exact public field and hierarchy value equals the authored
        contract and the general toy catalog accepts the model.
        """
        model = self.make_model()

        assert isinstance(model, Periodic1DModel)
        assert model.model_id == "test.periodic1d.fourier-parent"
        assert model.state_space_id == "test.periodic1d.bloch-state-space"
        assert model.reciprocal_domain_id == "test.periodic1d.primitive-reduced-zone"
        assert model.model_role is PeriodicModelRole.TOY
        assert model.spatial_dimension == 1
        assert type(model.potential) is PeriodicFourierPotential1D
        assert model.potential.period == ScalarQuantity(2.0 * np.pi, Unitless())
        assert model.recoil_energy == ScalarQuantity(1.0, Unitless())
        assert PeriodicToyModelCatalog((model,)).model_ids == (model.model_id,)

    def test_construction__identity__rejects_empty_parent_identity(self) -> None:
        """Evidence ID: SV-PERIODIC1D-FOURIER-MODEL-002

        Requirement: A complete scientific parent has a nonempty stable model identity.

        Acceptance: Empty model identity raises ``ValueError``.
        """
        with pytest.raises(ValueError, match="model_id must be nonempty"):
            Periodic1DFourierHamiltonianToyModel(
                "",
                "state-space",
                "reciprocal-domain",
                self.make_potential(),
                ScalarQuantity(1.0, Unitless()),
            )

    def test_construction__recoil_energy__rejects_nonpositive_scale(self) -> None:
        """Evidence ID: SV-PERIODIC1D-FOURIER-MODEL-003

        Requirement: The quadratic kinetic law has a strictly positive recoil scale.

        Acceptance: Exact zero recoil energy raises ``ValueError``.
        """
        with pytest.raises(ValueError, match="recoil_energy must be positive"):
            Periodic1DFourierHamiltonianToyModel(
                "model",
                "state-space",
                "reciprocal-domain",
                self.make_potential(),
                ScalarQuantity(0.0, Unitless()),
            )

    def test_construction__units__rejects_incompatible_kinetic_and_potential_energy(
        self,
    ) -> None:
        """Evidence ID: SV-PERIODIC1D-FOURIER-MODEL-004

        Requirement: Potential coefficients and kinetic recoil scale use dimensionally
        compatible energy conventions.

        Acceptance: Unitless potential with physical energy scale raises ``ValueError``.
        """
        with pytest.raises(ValueError, match="units must be compatible"):
            Periodic1DFourierHamiltonianToyModel(
                "model",
                "state-space",
                "reciprocal-domain",
                self.make_potential(),
                ScalarQuantity(1.0, PhysicalUnit("electron_volt")),
            )
