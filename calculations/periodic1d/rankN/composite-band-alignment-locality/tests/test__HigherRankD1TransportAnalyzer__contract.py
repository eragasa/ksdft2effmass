"""Software verification for higher-rank D1 sequential transport dispositions."""

from __future__ import annotations

import math

import numpy as np
import pytest
from projectkoios.numerics.numpy.validation import immutable_complex128_array
from workflow import (
    HigherRankD1ModelConstructor,
    HigherRankD1TransportAnalyzer,
    HigherRankD1TransportBackendError,
    HigherRankD1TransportDiagnostics,
    HigherRankD1TransportLinkRankDeficientDiagnostics,
)

pytestmark = pytest.mark.software_verification


class TestHigherRankD1TransportAnalyzer:
    """Establish qualified transport and fail-closed route dispositions."""

    def test_execute__rejects_noncanonical_mutable_frame_arrays(self) -> None:
        """The Numerics immutable-array validator rejects mutable inputs."""
        frames = np.zeros((3, 6, 3), dtype=np.complex128)
        endpoint = np.zeros((6, 3), dtype=np.complex128)

        with pytest.raises(ValueError, match="must be read-only"):
            HigherRankD1TransportAnalyzer().execute(frames, endpoint)

    def test_execute__returns_rank_deficiency_without_closure_payload(self) -> None:
        """Sequential transport stops at the first deficient required link."""
        analyzer = HigherRankD1TransportAnalyzer()
        frame = np.eye(6, 3, dtype=np.complex128)
        frames = immutable_complex128_array(
            np.broadcast_to(frame, (3, 6, 3)).copy(), "frames"
        )
        endpoint = immutable_complex128_array(
            np.zeros((6, 3), dtype=np.complex128), "endpoint"
        )

        result = analyzer.execute(frames, endpoint)

        assert isinstance(result, HigherRankD1TransportLinkRankDeficientDiagnostics)
        assert result.status == "transport-link-rank-deficient"
        assert result.deficient_link_indices == (2,)
        assert result.unattempted_link_indices == ()
        assert not hasattr(result, "closure_eigenphases")

    def test_execute__throws_backend_failure_with_route_context(self) -> None:
        """Backend nonresolution leaves transport with exact stopped-link context."""
        huge = immutable_complex128_array(
            np.full((3, 6, 3), 1.0e308 + 0.0j, dtype=np.complex128),
            "huge",
        )

        with pytest.raises(HigherRankD1TransportBackendError) as captured:
            HigherRankD1TransportAnalyzer().execute(huge, huge[0])

        assert captured.value.stage == "link"
        assert captured.value.attempted_link_count == 1
        assert isinstance(captured.value.backend_exception, FloatingPointError)

    def test_execute__uses_part2_sequence_and_distributed_closure(self) -> None:
        """P0 still traverses every neighbor and endpoint link."""
        constructor = HigherRankD1ModelConstructor()
        coordinates = constructor.construction_coordinates(513)
        fields = constructor.execute(3, 1, coordinates)
        endpoint = constructor.execute(
            3,
            1,
            constructor.positive_endpoint_coordinates(),
        ).reference_frames[0]

        diagnostics = HigherRankD1TransportAnalyzer().execute(
            fields.reference_frames,
            endpoint,
        )

        assert isinstance(diagnostics, HigherRankD1TransportDiagnostics)
        assert diagnostics.mesh_size == 513
        assert diagnostics.deficient_link_indices == ()
        assert diagnostics.minimum_link_singular_value == pytest.approx(1.0)
        assert diagnostics.minimum_rank_margin == pytest.approx(1.0 - 1.0e-10)
        assert diagnostics.endpoint_sewing.frame_defect == 0.0
        assert diagnostics.endpoint_sewing.projector_defect == 0.0
        assert diagnostics.primitive_closure_defect < 2.0e-15
        assert diagnostics.closure_unitarity_defect < 2.0e-15
        assert max(abs(value) for value in diagnostics.closure_eigenphases) < 2.0e-15
        assert math.isfinite(diagnostics.maximum_normalized_link_residual)
