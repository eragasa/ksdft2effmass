"""Software verification for periodic2d isolated-band input serialization."""

from pathlib import Path

import pytest

from ksdft2effmass.periodic2d.campaign.nbands_1 import (
    Periodic2DIsolatedBandCampaignJsonSerializer,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic2DIsolatedBandCampaignJsonSerializer:
    """Own strict decoding and deterministic canonical encoding evidence."""

    @staticmethod
    def payload() -> bytes:
        """Return the retained version-one input bytes."""
        root = Path(__file__).resolve().parents[7]
        return root.joinpath(
            "calculations/research-monograph/periodic-2d/input.json"
        ).read_bytes()

    def test_deserialize_serialize__retained_input__round_trips_semantically(
        self,
    ) -> None:
        """Every retained control survives deterministic canonical reconstruction."""
        serializer = Periodic2DIsolatedBandCampaignJsonSerializer()
        definition = serializer.deserialize(self.payload())

        encoded = serializer.serialize(definition)
        reconstructed = serializer.deserialize(encoded)

        assert encoded == serializer.serialize(definition)
        assert encoded.endswith(b"\n")
        assert reconstructed == definition
        assert reconstructed.coupling_sequence == (0.0, 0.05, 0.15, 0.3)
        assert reconstructed.finite_difference_points == (9, 13, 17, 25)

    def test_deserialize__duplicate_key__raises_value_error(self) -> None:
        """Duplicate object members fail before a partial record can be returned."""
        with pytest.raises(ValueError, match="duplicate JSON key"):
            Periodic2DIsolatedBandCampaignJsonSerializer().deserialize(
                b'{"schema_version":1,"schema_version":1}'
            )

    def test_deserialize__integer_float_field__raises_type_error(self) -> None:
        """Integer syntax is not coerced into a documented floating-point control."""
        payload = self.payload().replace(b"6.283185307179586", b"6", 1)

        with pytest.raises(TypeError, match="JSON floating-point number"):
            Periodic2DIsolatedBandCampaignJsonSerializer().deserialize(payload)

    def test_deserialize__extra_nested_field__raises_value_error(self) -> None:
        """Nested objects are closed rather than silently discarding unknown data."""
        marker = b'"chern_integer_defect": 1e-10'
        payload = self.payload().replace(
            marker,
            marker + b',\n    "unknown": 0.0',
            1,
        )

        with pytest.raises(ValueError, match="fields must match schema version one"):
            Periodic2DIsolatedBandCampaignJsonSerializer().deserialize(payload)
