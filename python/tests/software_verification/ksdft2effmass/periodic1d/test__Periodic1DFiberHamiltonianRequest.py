"""Software evidence for shared periodic-1D fiber identity qualification."""

from typing import assert_type

import numpy as np
import pytest

from ksdft2effmass.analysis.model_systems import PeriodicFourierPotential1D
from ksdft2effmass.operators import ScalarQuantity, Unitless, VectorQuantity
from ksdft2effmass.periodic import PeriodicOperatorReference
from ksdft2effmass.periodic1d import (
    Periodic1DFiberHamiltonianRequest,
    Periodic1DFourierHamiltonianToyModel,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic1DFiberHamiltonianRequest


class TestPeriodic1DFiberHamiltonianRequest:
    """Verify stable parent, operator, and finite-state-space identity binding."""

    @staticmethod
    def _parent() -> Periodic1DFourierHamiltonianToyModel:
        """Return a complete synthetic parent with no scientific claim."""
        potential = PeriodicFourierPotential1D(
            ScalarQuantity(1.0, Unitless()),
            ScalarQuantity(0.0, Unitless()),
            VectorQuantity(np.asarray([]), Unitless()),
            VectorQuantity(np.asarray([]), Unitless()),
        )
        return Periodic1DFourierHamiltonianToyModel(
            "parent-model",
            "untruncated-space",
            "reduced-zone",
            potential,
            ScalarQuantity(1.0, Unitless()),
        )

    def test_constructor__identity__retains_all_explicit_stable_identities(
        self,
    ) -> None:
        """Evidence ID: SV-PERIODIC-ONE-D-FIBER-REQUEST-001."""
        parent = self._parent()
        request = SUT(
            "finite-representation",
            parent,
            PeriodicOperatorReference(
                parent.model_id, "finite-operator", "finite-space", 1
            ),
            0.125,
            "synthetic-provenance",
        )

        assert_type(request, Periodic1DFiberHamiltonianRequest)
        assert request.model_id == "parent-model"
        assert request.operator_id == "finite-operator"
        assert request.state_space_id == "finite-space"
        assert request.provenance_id == "synthetic-provenance"

    def test_constructor__identity__rejects_parent_model_mismatch(self) -> None:
        """Evidence ID: SV-PERIODIC-ONE-D-FIBER-REQUEST-002."""
        parent = self._parent()

        with pytest.raises(ValueError, match="identify the parent model"):
            SUT(
                "finite-representation",
                parent,
                PeriodicOperatorReference(
                    "different-parent", "finite-operator", "finite-space", 1
                ),
                0.0,
                "synthetic-provenance",
            )

    def test_constructor__identity__rejects_untruncated_space_as_finite_space(
        self,
    ) -> None:
        """Evidence ID: SV-PERIODIC-ONE-D-FIBER-REQUEST-003."""
        parent = self._parent()

        with pytest.raises(ValueError, match="must remain distinct"):
            SUT(
                "finite-representation",
                parent,
                PeriodicOperatorReference(
                    parent.model_id,
                    "finite-operator",
                    parent.state_space_id,
                    1,
                ),
                0.0,
                "synthetic-provenance",
            )
