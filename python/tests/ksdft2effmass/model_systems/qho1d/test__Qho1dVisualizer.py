"""Authenticated-rendering tests for direct QHO1D results."""

from dataclasses import replace

import pytest

from ksdft2effmass.model_systems.analysis import ModelAnalysisVerificationResult
from ksdft2effmass.model_systems.qho1d import (
    Qho1dAnalysisRequest,
    Qho1dAnalyzer,
    Qho1dConfiguration,
    Qho1dVerification,
    Qho1dVerifier,
    Qho1dVisualizationData,
    Qho1dVisualizer,
)


class TestQho1dVisualizer:
    """Verify the closed inventory and authenticated projection boundary."""

    @staticmethod
    def verified_result() -> ModelAnalysisVerificationResult[
        Qho1dVerification, Qho1dVisualizationData
    ]:
        """Return one independently verified visualization projection."""
        configuration = Qho1dConfiguration(
            hbar=1.0,
            mass=1.0,
            omega=1.0,
            box_half_widths=(4.0, 6.0, 8.0),
            grid_spacings=(0.2, 0.1, 0.05),
            retained_dimensions=(2, 4, 6),
            selected_box_half_width=8.0,
            selected_grid_spacing=0.05,
            selected_retained_dimension=6,
            displayed_states=4,
        )
        result = Qho1dAnalyzer(
            Qho1dAnalysisRequest(
                configuration=configuration,
                calculation_family="qho1d-spatial-truncation",
                execution_id="test-direct",
                evidence_status="illustrative numerical experiment",
                claim_boundary="test fixture; no scientific-validation claim",
            )
        ).execute()
        wire = result.to_json()
        return Qho1dVerifier(result_wire=wire).result()

    def test_method__visualize__returns_closed_valid_png_inventory(self) -> None:
        """Every declared plot produces one validated PNG byte value."""
        verified = self.verified_result()

        visualizer = Qho1dVisualizer(
            data=verified.visualization_data,
            verification=verified.verification,
        )
        visualizations = visualizer.visualize()

        assert {item.plot for item in visualizations} == set(visualizer.plots)
        assert {item.filename for item in visualizations} == {
            "qho1d-eigenstates.png",
            "qho1d-eigenstate-distortion.png",
            "qho1d-diagnostics.png",
        }
        assert all(item.png.startswith(b"\x89PNG\r\n\x1a\n") for item in visualizations)

    def test_method__visualize__rejects_unauthenticated_projection(self) -> None:
        """Rendering fails before plotting when the projection digest differs."""
        verified = self.verified_result()
        altered_verification = replace(
            verified.verification,
            visualization_data_sha256="0" * 64,
        )

        with pytest.raises(
            ValueError,
            match="verification authenticates different visualization data",
        ):
            Qho1dVisualizer(
                data=verified.visualization_data,
                verification=altered_verification,
            ).visualize()
