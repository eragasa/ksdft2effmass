"""Software evidence for explicit periodic-1D supercell operator metadata."""

from typing import cast

import pytest

from ksdft2effmass.periodic1d import (
    Periodic1DSupercellOperatorMetadata,
    Periodic1DSupercellOperatorProvenance,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic1DSupercellOperatorMetadata


def _provenance() -> Periodic1DSupercellOperatorProvenance:
    """Return explicit synthetic provenance with no physical claim."""
    return Periodic1DSupercellOperatorProvenance(
        "parent-model", "source-record", "construction-record", "test-fixture"
    )


class TestPeriodic1DSupercellOperatorMetadata:
    """Verify mandatory cell vectors, labels, and structured provenance."""

    def test_constructor__metadata__accepts_complete_explicit_contract(self) -> None:
        """Evidence ID: SV-PERIODIC-ONE-D-SUPERCELL-METADATA-001."""
        metadata = SUT(
            "finite-supercell-space",
            "periodic-1d-supercell-fiber",
            "site-orbital-spin-basis",
            "ordered orthonormal site-orbital-spin basis",
            ("site-0/orbital-0", "site-0/orbital-1"),
            ((2.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
            "two-cell-embedded-geometry",
            "periodic along first cell vector",
            "Cartesian row lattice vectors",
            "dimensionless_length",
            "explicit-zero",
            "E_G",
            _provenance(),
        )

        assert metadata.ordered_state_labels[1] == "site-0/orbital-1"
        assert metadata.cell_vectors[0] == (2.0, 0.0, 0.0)

    def test_constructor__metadata__rejects_non_tuple_ordered_labels(self) -> None:
        """Evidence ID: SV-PERIODIC-ONE-D-SUPERCELL-METADATA-002."""
        with pytest.raises(TypeError, match="exact tuple"):
            SUT(
                "finite-supercell-space",
                "periodic-1d-supercell-fiber",
                "basis",
                "basis-kind",
                cast(tuple[str, ...], ["state-0"]),
                ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
                "geometry",
                "periodic",
                "Cartesian rows",
                "dimensionless_length",
                "zero",
                "E_G",
                _provenance(),
            )
