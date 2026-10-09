"""Software evidence for lossless represented-supercell adaptation."""

import numpy as np
import pytest

from ksdft2effmass.operators import OperatorRecord
from ksdft2effmass.periodic1d import (
    Periodic1DSupercellOperatorConstructor,
    Periodic1DSupercellOperatorMetadata,
    Periodic1DSupercellOperatorProvenance,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic1DSupercellOperatorConstructor


class TestPeriodic1DSupercellOperatorConstructor:
    """Verify exact transfer into the general represented-operator record."""

    @staticmethod
    def _metadata() -> Periodic1DSupercellOperatorMetadata:
        """Return fully authored synthetic interpreting metadata."""
        return Periodic1DSupercellOperatorMetadata(
            "finite-supercell-space",
            "periodic-1d-supercell-fiber",
            "ordered-supercell-basis",
            "site-major orbital-fast orthonormal basis",
            ("site-0/orbital-0", "site-0/orbital-1"),
            ((2.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
            "embedded-supercell-geometry",
            "periodic along first cell vector",
            "Cartesian row lattice vectors",
            "dimensionless_length",
            "explicit-zero",
            "E_G",
            Periodic1DSupercellOperatorProvenance(
                "parent-model", "source-record", "construction-record", "test-fixture"
            ),
        )

    def test_method__execute__constructs_general_operator_record_losslessly(
        self,
    ) -> None:
        """Evidence ID: SV-PERIODIC-ONE-D-SUPERCELL-CONSTRUCTOR-001."""
        matrix = np.asarray([[1.0, 2.0j], [-2.0j, 3.0]], dtype=np.complex128)

        result = SUT().execute(
            "operator-record", "supercell-hamiltonian", self._metadata(), matrix
        )

        assert isinstance(result, OperatorRecord)
        assert result.state_space.identifier == "finite-supercell-space"
        assert result.basis.ordering == (
            "site-0/orbital-0",
            "site-0/orbital-1",
        )
        assert result.geometry.cell[0] == (2.0, 0.0, 0.0)
        assert result.provenance["parent_model_id"] == "parent-model"
        np.testing.assert_array_equal(result.matrix, matrix)
        assert result.matrix.flags.writeable is False

    def test_method__execute__rejects_matrix_without_one_label_per_state(self) -> None:
        """Evidence ID: SV-PERIODIC-ONE-D-SUPERCELL-CONSTRUCTOR-002."""
        with pytest.raises(ValueError, match="state-space dimension"):
            SUT().execute(
                "operator-record",
                "supercell-hamiltonian",
                self._metadata(),
                np.eye(3, dtype=np.complex128),
            )
