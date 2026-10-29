"""Software verification of reusable finite-probability tail selection."""

from __future__ import annotations

import numpy as np
import pytest
from projectkoios.physkit.units import Unitless, VectorQuantity

from ksdft2effmass.analysis import (
    TailProbabilitySelection,
    TailProbabilitySelectionRequest,
    TailProbabilitySelector,
)
from ksdft2effmass.serialization import TypedJsonValueCodec

pytestmark = pytest.mark.software_verification
SUT = TailProbabilitySelector


class TestTailProbabilitySelector:
    """Own first-passing finite cumulative-tail selection behavior."""

    def test_execute__normalized_probabilities__selects_first_passing_prefix(
        self,
    ) -> None:
        probabilities = VectorQuantity(
            np.asarray([0.7, 0.2, 0.09, 0.01]),
            Unitless(),
        )

        request = TailProbabilitySelectionRequest(probabilities, 0.1)
        selector = SUT(request)

        result = selector.execute()

        assert selector.request is request
        assert result.selected_count == 2
        assert np.allclose(
            result.omitted_probabilities.magnitude,
            np.asarray([0.3, 0.1, 0.01, 0.0]),
            rtol=0.0,
            atol=1.0e-15,
        )
        codec = TypedJsonValueCodec()
        decoded = codec.deserialize_bytes(codec.serialize_bytes(result))
        assert isinstance(decoded, dict)
        reconstructed = TailProbabilitySelection.from_dict(decoded)
        assert reconstructed.selected_count == result.selected_count

    def test_execute__boolean_tolerance__rejects_non_float_boundary(self) -> None:
        probabilities = VectorQuantity(np.asarray([0.75, 0.25]), Unitless())

        with pytest.raises(TypeError, match="built-in float"):
            TailProbabilitySelectionRequest(probabilities, True)

    def test_execute__nonnormalized_or_negative_probabilities__rejects(self) -> None:
        with pytest.raises(ValueError, match="sum to one"):
            TailProbabilitySelectionRequest(
                VectorQuantity(np.asarray([0.5, 0.4]), Unitless()),
                0.1,
            )
        with pytest.raises(ValueError, match="nonnegative"):
            TailProbabilitySelectionRequest(
                VectorQuantity(np.asarray([1.1, -0.1]), Unitless()),
                0.1,
            )

    def test_result__inconsistent_tails__rejects_direct_construction(self) -> None:
        with pytest.raises(ValueError, match="cumulative probability tails"):
            TailProbabilitySelection(
                probabilities=VectorQuantity(np.asarray([0.75, 0.25]), Unitless()),
                omitted_probabilities=VectorQuantity(
                    np.asarray([0.20, 0.0]), Unitless()
                ),
                tolerance=0.3,
                selected_count=1,
            )

    def test_from_dict__nonmapping__rejects_before_field_access(self) -> None:
        with pytest.raises(TypeError, match="must be a mapping"):
            TailProbabilitySelection.from_dict([])  # type: ignore[arg-type]
