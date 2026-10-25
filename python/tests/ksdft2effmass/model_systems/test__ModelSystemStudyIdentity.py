"""Software verification for ``ModelSystemStudyIdentity``."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.model_systems.study import (
    ModelId,
    ModelSystemStudyIdentity,
    ModelSystemStudySchemaId,
)

pytestmark = pytest.mark.software_verification
SUT = ModelSystemStudyIdentity


class TestModelSystemStudyIdentity:
    """Own software evidence for the immutable shared study identity."""

    def test_constructor__valid_values__retains_nominal_identity(self) -> None:
        identity = ModelSystemStudyIdentity(
            ModelId.piab1d,
            ModelSystemStudySchemaId.piab1d_v2,
        )

        assert identity.model_id is ModelId.piab1d
        assert identity.schema_id is ModelSystemStudySchemaId.piab1d_v2

    def test_constructor__wrong_enum_type__raises_type_error(self) -> None:
        with pytest.raises(TypeError, match="model_id"):
            ModelSystemStudyIdentity(
                "piab1d",  # type: ignore[arg-type]
                ModelSystemStudySchemaId.piab1d_v2,
            )

    def test_attribute__mutation__raises_frozen_instance_error(self) -> None:
        identity = ModelSystemStudyIdentity(
            ModelId.piab1d,
            ModelSystemStudySchemaId.piab1d_v2,
        )

        with pytest.raises(FrozenInstanceError):
            identity.model_id = ModelId.qho1d  # type: ignore[misc]
