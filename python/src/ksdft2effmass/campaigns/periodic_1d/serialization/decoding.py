"""Typed JSON decoding mechanics for periodic-1D campaign serializers."""

from __future__ import annotations

import numpy as np

from ksdft2effmass.campaigns.serialization import CampaignJsonDecoder, JsonValue
from ksdft2effmass.operators import ScalarQuantity, Unitless, VectorQuantity


class Periodic1DCampaignJsonDecoder(CampaignJsonDecoder):
    """Extend shared campaign JSON decoding with unitless quantities."""

    __slots__ = ()

    def scalar(self, value: JsonValue, name: str) -> ScalarQuantity:
        """Return one explicitly unitless scalar quantity."""
        return ScalarQuantity(self.real(value, name), Unitless())

    def vector(self, value: JsonValue, name: str) -> VectorQuantity:
        """Return one explicitly unitless binary64 vector quantity."""
        return VectorQuantity(
            np.asarray(
                [self.real(item, name) for item in self.array(value, name)],
                dtype=np.float64,
            ),
            Unitless(),
        )
