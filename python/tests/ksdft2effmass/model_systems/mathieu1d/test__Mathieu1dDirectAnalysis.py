"""Software verification of direct Mathieu1D analysis owners."""

from __future__ import annotations

import ast
import hashlib
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest
from projectkoios.physkit.units import (
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.model_systems.mathieu1d.analysis import Mathieu1dAnalyzer
from ksdft2effmass.model_systems.mathieu1d.configuration import (
    Mathieu1dConfiguration,
)
from ksdft2effmass.model_systems.mathieu1d.result import (
    Mathieu1dCalculationResult,
)
from ksdft2effmass.model_systems.mathieu1d.verification import Mathieu1dVerifier
from ksdft2effmass.model_systems.mathieu1d.visualizations import Mathieu1dVisualizer
from ksdft2effmass.visualizations import PngVisualization

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestMathieu1dDirectAnalysis:
    """Verify typed calculate, byte-owning verification, and rendering behavior."""

    def test_source__successor_modules__import_no_legacy_or_calculation_code(
        self,
    ) -> None:
        """Successor source consumes installed owners without predecessor imports."""
        source_directory = (
            Path(__file__).resolve().parents[5]
            / "python"
            / "src"
            / ("ksdft2effmass/model_systems/mathieu1d")
        )
        source_files = [
            source_directory / name
            for name in (
                "__init__.py",
                "analysis.py",
                "configuration.py",
                "result.py",
                "verification.py",
                "verification_values.py",
            )
        ]
        source_files.extend(sorted((source_directory / "visualizations").rglob("*.py")))
        for source_file in source_files:
            tree = ast.parse(source_file.read_text(encoding="utf-8"))
            imported_modules = {
                node.module
                for node in ast.walk(tree)
                if isinstance(node, ast.ImportFrom) and node.module is not None
            }
            imported_modules.update(
                alias.name
                for node in ast.walk(tree)
                if isinstance(node, ast.Import)
                for alias in node.names
            )
            assert not any(".study" in module for module in imported_modules)
            assert not any(
                "single_band_fourier_reduction" in module for module in imported_modules
            )
            assert not any(
                module.startswith("calculations") for module in imported_modules
            )

    def test_configuration__invalid_boolean_numeric__is_rejected(self) -> None:
        """The public numeric boundary rejects booleans rather than coercing them."""
        with pytest.raises(TypeError, match="recoil_energy"):
            replace(self._configuration(), recoil_energy=True)

    def test_calculate__typed_result__round_trips_and_retains_closed_ranges(
        self,
    ) -> None:
        """The direct analyzer returns one immutable typed finite result."""
        result = self._calculate(self._configuration())
        wire = result.to_json()
        decoded = Mathieu1dCalculationResult.from_json(wire)

        assert decoded.to_json() == wire
        assert decoded.calculation_family == "mathieu1d-finite-reduction"
        assert decoded.execution_id == "test-direct"
        assert decoded.evidence_status == "illustrative numerical experiment"
        assert decoded.claim_boundary == "test fixture; no scientific-validation claim"
        assert tuple(value.maximum_range for value in decoded.ranges) == (0, 1, 2)
        assert decoded.transform.reconstruction_passes
        assert decoded.transform.hermiticity_passes
        assert all(value.parseval_passes for value in decoded.ranges)
        assert all(value.direct_is_identified for value in decoded.ranges)
        assert all(value.band_shape_passes for value in decoded.ranges)

    def test_result__configuration_correlations__reject_mismatched_sections(
        self,
    ) -> None:
        """The typed aggregate rejects independently valid inconsistent sections."""
        result = self._calculate(self._configuration())
        shifted_training = replace(
            result.bands,
            training_reduced_momenta=VectorQuantity(
                result.bands.training_reduced_momenta.magnitude + 1.0e-4,
                Unitless(),
            ),
        )
        with pytest.raises(ValueError, match="training coordinates"):
            replace(result, bands=shifted_training)

        reduced_spectrum = replace(
            result.refinement,
            parent_reference_energies=MatrixQuantity(
                result.refinement.parent_reference_energies.magnitude[:, :1],
                Unitless(),
            ),
        )
        with pytest.raises(ValueError, match="parent spectrum"):
            replace(result, refinement=reduced_spectrum)

        altered_transform = replace(
            result.transform,
            reconstruction_absolute_tolerance=ScalarQuantity(
                2.0 * result.configuration.reconstruction_absolute_tolerance,
                Unitless(),
            ),
        )
        with pytest.raises(ValueError, match="reconstruction tolerance"):
            replace(result, transform=altered_transform)

        altered_range = replace(
            result.ranges[0],
            imaginary_absolute_tolerance=ScalarQuantity(
                2.0 * result.configuration.imaginary_absolute_tolerance,
                Unitless(),
            ),
        )
        with pytest.raises(ValueError, match="range imaginary tolerance"):
            replace(result, ranges=(altered_range, *result.ranges[1:]))

    def test_verify_and_render__exact_subject_bytes__authenticate_png(self) -> None:
        """Verification owns exact bytes and rendering admits only its projection."""
        result = self._calculate(self._configuration())
        wire = result.to_json() + b"\n"
        verified = Mathieu1dVerifier(result_wire=wire).result()

        assert verified.verification.passed
        assert verified.verification.subject_sha256 == hashlib.sha256(wire).hexdigest()
        assert len(verified.verification.checks) > 100
        visualizations = Mathieu1dVisualizer(
            data=verified.visualization_data,
            verification=verified.verification,
        ).visualize()
        assert {value.filename for value in visualizations} == {
            "mathieu1d-finite-reduction.png",
            "mathieu1d-publication-summary.png",
        }
        assert all(type(value) is PngVisualization for value in visualizations)
        assert all(
            image.png.startswith(b"\x89PNG\r\n\x1a\n") for image in visualizations
        )

        altered_data = replace(
            verified.visualization_data,
            plane_wave_maximum_errors=VectorQuantity(
                verified.visualization_data.plane_wave_maximum_errors.magnitude
                + 1.0e-6,
                Unitless(),
            ),
        )
        with pytest.raises(ValueError, match="digest"):
            Mathieu1dVisualizer(
                data=altered_data,
                verification=verified.verification,
            ).visualize()

    def test_verify__positive_nonuniform_weights__matches_independent_fit(
        self,
    ) -> None:
        """The independent route reproduces the declared weighted objective."""
        configuration = replace(
            self._configuration(),
            fitting_weights=tuple(1.0 + float(index) / 20.0 for index in range(16)),
        )
        result = self._calculate(configuration)
        verification = Mathieu1dVerifier(result_wire=result.to_json()).result()

        assert verification.verification.passed

    def test_verify__modified_authoritative_value__fails_independent_check(
        self,
    ) -> None:
        """A self-consistent typed wire cannot bypass independent reconstruction."""
        result = self._calculate(self._configuration())
        first = result.ranges[0]
        altered_first = replace(
            first,
            bandwidth=ScalarQuantity(
                first.bandwidth.magnitude + 1.0e-5,
                Unitless(),
            ),
        )
        altered_result = replace(
            result,
            ranges=(altered_first, *result.ranges[1:]),
        )
        verification = (
            Mathieu1dVerifier(result_wire=altered_result.to_json())
            .result()
            .verification
        )

        assert not verification.passed
        assert verification.checks["result.ranges[0].bandwidth"] == pytest.approx(
            1.0e-5
        )

    @staticmethod
    def _calculate(
        configuration: Mathieu1dConfiguration,
    ) -> Mathieu1dCalculationResult:
        return Mathieu1dAnalyzer().calculate(
            configuration,
            calculation_family="mathieu1d-finite-reduction",
            execution_id="test-direct",
            evidence_status="illustrative numerical experiment",
            claim_boundary="test fixture; no scientific-validation claim",
        )

    @staticmethod
    def _configuration() -> Mathieu1dConfiguration:
        return Mathieu1dConfiguration(
            period=float(2.0 * np.pi),
            reciprocal_vector=1.0,
            recoil_energy=1.0,
            constant_coefficient=0.0,
            cosine_amplitude=0.5,
            duality_absolute_tolerance=1.0e-14,
            plane_wave_cutoffs=(2, 3),
            plane_wave_reference_cutoff=4,
            production_plane_wave_cutoff=3,
            finite_difference_points=(15, 31),
            parent_reduced_momenta=(-0.5, 0.0, 0.5),
            compared_band_count=2,
            selected_band_index=0,
            reciprocal_training_mesh_size=16,
            evaluation_reduced_momenta=tuple(
                float(-0.5 + (index + 0.3) / 33.0) for index in range(33)
            ),
            hopping_ranges=(0, 1, 2),
            fitting_weights=(1.0,) * 16,
            coordinate_absolute_tolerance=1.0e-14,
            reconstruction_absolute_tolerance=1.0e-10,
            hermiticity_absolute_tolerance=1.0e-10,
            parseval_absolute_tolerance=1.0e-10,
            imaginary_absolute_tolerance=1.0e-10,
        )
