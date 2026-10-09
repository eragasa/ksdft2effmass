"""Software evidence for explicit supercell-operator provenance metadata."""

from typing import assert_type

import pytest

from ksdft2effmass.periodic1d import Periodic1DSupercellOperatorProvenance

pytestmark = pytest.mark.software_verification
SUT = Periodic1DSupercellOperatorProvenance


class TestPeriodic1DSupercellOperatorProvenance:
    """Verify the closed structured provenance identity contract."""

    def test_constructor__provenance__retains_closed_explicit_identities(self) -> None:
        """Evidence ID: SV-PERIODIC-ONE-D-SUPERCELL-PROVENANCE-001."""
        provenance = SUT(
            "parent-model",
            "authenticated-source-record",
            "construction-record",
            "producing-operation",
        )

        assert_type(provenance, Periodic1DSupercellOperatorProvenance)
        assert provenance.as_operator_record_mapping() == {
            "parent_model_id": "parent-model",
            "source_record_id": "authenticated-source-record",
            "construction_record_id": "construction-record",
            "producer_id": "producing-operation",
        }

    def test_constructor__provenance__rejects_empty_identity(self) -> None:
        """Evidence ID: SV-PERIODIC-ONE-D-SUPERCELL-PROVENANCE-002."""
        with pytest.raises(ValueError, match="parent_model_id must be nonempty"):
            SUT("", "source", "construction", "producer")
