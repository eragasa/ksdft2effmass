"""Tests for independent exact-byte composite-alignment verification."""

import hashlib
from dataclasses import replace

import numpy as np
import pytest
from projectkoios.physkit.units import ComplexMatrixQuantity, MatrixQuantity, Unitless

from ksdft2effmass.periodic1d.rank2.band_alignment.composite import (
    Periodic1DCompositeBandAlignmentAnalyzer,
    Periodic1DCompositeBandAlignmentCalculationResult,
    Periodic1DCompositeBandAlignmentIndependentReferenceAnalyzer,
    Periodic1DCompositeBandAlignmentIndependentReferenceRequest,
    Periodic1DCompositeBandAlignmentVerification,
    Periodic1DCompositeBandAlignmentVerifier,
    Periodic1DCompositeBandAlignmentVisualizationPlotEnum,
    Periodic1DCompositeBandAlignmentVisualizer,
)

pytestmark = [pytest.mark.integration, pytest.mark.numerical_verification]


class TestPeriodic1DCompositeBandAlignmentVerifier:
    """Establish independent reconstruction, readmission, and authenticated PNGs."""

    def test__result__authenticates_independently_reconstructed_values(
        self,
        composite_result: Periodic1DCompositeBandAlignmentCalculationResult,
    ) -> None:
        wire = composite_result.to_json()

        verified = Periodic1DCompositeBandAlignmentVerifier(result_wire=wire).result()

        assert verified.verification.passed
        assert {
            "construction_parent_spectrum",
            "reference_frames",
            "pointwise_rotations",
            "global_rotation",
            "transform_attacked_hopping_blocks",
            "transform_attacked_cyclic_conversion_power",
            "transform_attacked_evaluation_interpolation_errors",
            "range_values",
            "diagnostic_values",
            "closure_eigenphases",
        } <= set(verified.verification.checks)
        assert verified.verification.subject_sha256 == hashlib.sha256(wire).hexdigest()
        assert max(verified.verification.checks.values()) < 2.0e-13
        assert (
            Periodic1DCompositeBandAlignmentVerification.from_json(
                verified.verification.to_json()
            ).to_json()
            == verified.verification.to_json()
        )

    def test__admit_stored__rejects_tampered_visualization_projection(
        self,
        composite_result: Periodic1DCompositeBandAlignmentCalculationResult,
    ) -> None:
        verifier = Periodic1DCompositeBandAlignmentVerifier(
            result_wire=composite_result.to_json()
        )
        verified = verifier.result()
        values = verified.visualization_data.evaluation_parent_spectrum.magnitude.copy()
        values[0, 0] += 1.0e-6
        tampered = replace(
            verified.visualization_data,
            evaluation_parent_spectrum=MatrixQuantity(values, Unitless()),
        )

        with pytest.raises(ValueError, match="visualization"):
            verifier.admit_stored(
                verification=verified.verification,
                visualization_data=tampered,
            )

    def test__independent_verifier__detects_mutated_hopping_block(
        self,
        composite_result: Periodic1DCompositeBandAlignmentCalculationResult,
    ) -> None:
        verified = Periodic1DCompositeBandAlignmentVerifier(
            result_wire=composite_result.to_json()
        ).result()
        transform = composite_result.transforms[0]
        blocks = list(transform.hopping_blocks)
        changed = blocks[0].magnitude.copy()
        changed[0, 0] += 1.0e-6
        blocks[0] = ComplexMatrixQuantity(changed, Unitless())
        mutated_transform = replace(transform, hopping_blocks=tuple(blocks))
        mutated = replace(
            composite_result,
            transforms=(mutated_transform, *composite_result.transforms[1:]),
        )

        request = Periodic1DCompositeBandAlignmentIndependentReferenceRequest(
            mutated,
            verified.visualization_data,
        )
        independent = Periodic1DCompositeBandAlignmentIndependentReferenceAnalyzer(
            request
        )
        comparisons = independent.execute().comparisons

        assert independent.request is request

        assert not comparisons["transform_reference_hopping_blocks"].result().passed

    def test__result__does_not_invoke_production_analyzer(
        self,
        composite_result: Periodic1DCompositeBandAlignmentCalculationResult,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        def forbidden(*_args: object, **_kwargs: object) -> None:
            raise AssertionError("production analyzer must not run during verification")

        monkeypatch.setattr(
            Periodic1DCompositeBandAlignmentAnalyzer,
            "execute",
            forbidden,
        )

        verified = Periodic1DCompositeBandAlignmentVerifier(
            result_wire=composite_result.to_json()
        ).result()

        assert np.isfinite(tuple(verified.verification.checks.values())).all()

    def test__visualize__returns_complete_authenticated_png_inventory(
        self,
        composite_result: Periodic1DCompositeBandAlignmentCalculationResult,
    ) -> None:
        verified = Periodic1DCompositeBandAlignmentVerifier(
            result_wire=composite_result.to_json()
        ).result()

        visualizations = Periodic1DCompositeBandAlignmentVisualizer(
            data=verified.visualization_data,
            verification=verified.verification,
            dpi=80,
        ).visualize()

        assert {value.plot for value in visualizations} == set(
            Periodic1DCompositeBandAlignmentVisualizationPlotEnum
        )
        assert all(
            value.png.startswith(b"\x89PNG\r\n\x1a\n") for value in visualizations
        )

    def test__visualize__rejects_unrelated_projection_digest(
        self,
        composite_result: Periodic1DCompositeBandAlignmentCalculationResult,
    ) -> None:
        verified = Periodic1DCompositeBandAlignmentVerifier(
            result_wire=composite_result.to_json()
        ).result()
        unrelated = replace(
            verified.verification,
            visualization_data_sha256="0" * 64,
        )

        with pytest.raises(ValueError, match="visualization"):
            Periodic1DCompositeBandAlignmentVisualizer(
                data=verified.visualization_data,
                verification=unrelated,
            )
