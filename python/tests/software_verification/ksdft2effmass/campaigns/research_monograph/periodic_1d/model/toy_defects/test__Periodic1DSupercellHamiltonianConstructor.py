r"""Software verification of ``Periodic1DSupercellHamiltonianConstructor``.

Evidence profile: claim_bearing

The tests establish the finite hopping and explicit boundary-phase software contract
for a controlled toy parent. They do not establish a material Hamiltonian.
"""

import numpy as np
import pytest

from ksdft2effmass.campaigns.research_monograph.periodic_1d.model.toy_defects import (
    Periodic1DFiniteHoppingToyModel,
    Periodic1DHoppingBlock,
    Periodic1DSupercellHamiltonianConstructor,
    Periodic1DSupercellHamiltonianRequest,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic1DSupercellHamiltonianConstructor


class TestPeriodic1DSupercellHamiltonianConstructor:
    """Own finite-hopping twisted-supercell construction evidence."""

    @staticmethod
    def _model() -> Periodic1DFiniteHoppingToyModel:
        return Periodic1DFiniteHoppingToyModel(
            (
                Periodic1DHoppingBlock(-1, np.asarray([[-1.0]], dtype=np.complex128)),
                Periodic1DHoppingBlock(0, np.asarray([[0.5]], dtype=np.complex128)),
                Periodic1DHoppingBlock(1, np.asarray([[-1.0]], dtype=np.complex128)),
            ),
            "dimensionless",
            1.0e-14,
        )

    def test_method__execute__places_boundary_crossing_phases(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-TOY-001.

        Requirement: Only hopping terms that cross the finite seam receive the
        authored supercell twist phase.

        Method: Construct a three-cell scalar nearest-neighbor model at a nonzero
        reduced momentum.

        Oracle: Directly authored matrix entries under the documented phase
        convention.

        Acceptance: Every complex matrix entry agrees to roundoff.

        Interpretation: A pass establishes represented supercell mechanics.

        Limitations: This is synthetic one-orbital software verification.
        """
        momentum = 0.125
        phase = np.exp(2j * np.pi * momentum * 3)
        expected = np.asarray(
            [
                [0.5, -1.0, -phase.conjugate()],
                [-1.0, 0.5, -1.0],
                [-phase, -1.0, 0.5],
            ],
            dtype=np.complex128,
        )

        result = SUT().execute(
            Periodic1DSupercellHamiltonianRequest(self._model(), 3, momentum)
        )

        np.testing.assert_allclose(result.matrix, expected, rtol=0.0, atol=1.0e-15)
        assert not result.matrix.flags.writeable

    def test_method__request__rejects_boolean_cell_count(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-TOY-002.

        Requirement: Public numeric contracts reject booleans as integer counts.

        Method: Construct a request with ``True`` as the cell count.

        Oracle: Exact semantic ``TypeError``.

        Acceptance: Construction stops before numerical execution.

        Interpretation: A pass establishes strict runtime typing.

        Limitations: Other value invariants are exercised by their owning records.
        """
        with pytest.raises(TypeError, match="cell_count must be an integer"):
            Periodic1DSupercellHamiltonianRequest(self._model(), True, 0.0)
