"""Software verification for the higher-rank D1 analytic model construction."""

from __future__ import annotations

import numpy as np
import pytest
from projectkoios.numerics.numpy.validation import (
    validate_immutable_complex128_array,
    validate_immutable_float64_array,
)
from workflow import (
    HigherRankD1ModelConstructor,
)

pytestmark = pytest.mark.software_verification


class TestHigherRankD1ModelConstructor:
    """Establish the selected P0 parent and real noncommuting gauge attack."""

    def test_execute__rejects_noncanonical_mutable_coordinate_arrays(self) -> None:
        """The Numerics immutable-array validator rejects mutable coordinates."""
        mutable = np.asarray((-0.5, 0.0), dtype=np.float64)

        with pytest.raises(ValueError, match="must be read-only"):
            HigherRankD1ModelConstructor().execute(3, 1, mutable)

    def test_execute__constructs_isolated_parent_and_projector_preserving_attack(
        self,
    ) -> None:
        """Rank-three depth-two fields satisfy construction identities pointwise."""
        constructor = HigherRankD1ModelConstructor()
        coordinates = constructor.construction_coordinates(513)
        fields = constructor.execute(3, 2, coordinates)

        assert (
            validate_immutable_float64_array(coordinates, "coordinates") is coordinates
        )
        assert (
            validate_immutable_float64_array(
                fields.retained_energies, "retained_energies"
            )
            is fields.retained_energies
        )
        assert (
            validate_immutable_complex128_array(
                fields.candidate_frames, "candidate_frames"
            )
            is fields.candidate_frames
        )
        sampled_isolation = float(
            np.min(
                np.min(fields.exterior_energies, axis=1)
                - np.max(fields.retained_energies, axis=1)
            )
        )
        assert 2.1 < sampled_isolation < 2.1001
        identity = np.eye(3, dtype=np.complex128)
        assert (
            np.max(
                np.linalg.norm(
                    np.swapaxes(fields.gauges.conjugate(), -1, -2) @ fields.gauges
                    - identity,
                    axis=(-2, -1),
                )
            )
            < 8.0e-16
        )
        assert np.max(np.abs(np.linalg.det(fields.gauges).real - 1.0)) < 1.0e-15
        assert np.max(np.abs(np.linalg.det(fields.gauges).imag)) < 1.0e-15
        projector = fields.reference_frames @ np.swapaxes(
            fields.reference_frames.conjugate(), -1, -2
        )
        attacked_projector = fields.candidate_frames @ np.swapaxes(
            fields.candidate_frames.conjugate(), -1, -2
        )
        assert (
            np.max(np.linalg.norm(attacked_projector - projector, axis=(-2, -1)))
            < 1.0e-15
        )
        assert constructor.sampled_attack_angle_maximum(3, 2, coordinates) < (
            constructor.exact_attack_angle_bound(3)
        )
        assert constructor.exact_attack_angle_bound(3) < 0.4025
