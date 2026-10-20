"""Software verification for ``ModelSystemStudyIdentity``."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest
from ksdft2effmass.model_systems.study import ModelSystemStudyIdentity

pytestmark = pytest.mark.software_verification
SUT = ModelSystemStudyIdentity


class TestModelSystemStudyIdentity:
    """Own software evidence for the immutable shared study identity."""

    def test_constructor__valid_values__retains_nominal_identity(self) -> None:
        """The value preserves one nonempty identifier and evidence status."""
        identity = ModelSystemStudyIdentity(
            "qho1d.test.v1", "illustrative numerical experiment"
        )

        assert identity.study_id == "qho1d.test.v1"
        assert identity.evidence_status == "illustrative numerical experiment"

    def test_constructor__empty_value__raises_value_error(self) -> None:
        """Empty identity fields are rejected at construction."""
        with pytest.raises(ValueError, match="study_id must be nonempty"):
            ModelSystemStudyIdentity("", "illustrative numerical experiment")

    def test_attribute__mutation__raises_frozen_instance_error(self) -> None:
        """The nominal identity has immutable value semantics."""
        identity = ModelSystemStudyIdentity(
            "qho1d.test.v1", "illustrative numerical experiment"
        )

        with pytest.raises(FrozenInstanceError):
            identity.study_id = "changed"  # type: ignore[misc]
