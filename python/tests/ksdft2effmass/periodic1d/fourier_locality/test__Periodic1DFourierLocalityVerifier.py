"""Tests for exact-byte independent Fourier-locality verification."""

import hashlib
from dataclasses import replace

import numpy as np
import pytest
from projectkoios.physkit.units import Unitless, VectorQuantity

from ksdft2effmass.periodic1d.fourier_locality import (
    Periodic1DFourierLocalityAnalyzer,
    Periodic1DFourierLocalityConfiguration,
    Periodic1DFourierLocalityIndependentVerifier,
    Periodic1DFourierLocalityVerification,
    Periodic1DFourierLocalityVerifier,
    Periodic1DFourierLocalityVisualizationPlotEnum,
    Periodic1DFourierLocalityVisualizer,
)


class TestPeriodic1DFourierLocalityVerifier:
    """Establish independent reconstruction, authentication, and readmission."""

    @staticmethod
    def configuration() -> Periodic1DFourierLocalityConfiguration:
        return Periodic1DFourierLocalityConfiguration(
            parent_identity=(
                "ksdft2effmass.periodic1d.controlled-four-state-parent.v1"
            ),
            onsite_numerators=(
                (-120, 6, 0, 0),
                (6, -35, 0, 0),
                (0, 0, 100, 4),
                (0, 0, 4, 175),
            ),
            positive_hopping_numerators=(
                (15, 0, 12, 0),
                (0, -10, 0, 10),
                (0, 0, 5, 0),
                (0, 0, 0, -4),
            ),
            coefficient_denominator=100,
            construction_mesh_sizes=(4, 8),
            production_construction_size=8,
            evaluation_size=3,
            evaluation_shift_numerator=1,
            evaluation_shift_denominator=3,
            maximum_ranges=(0, 1),
            sampled_gap_threshold=0.25,
            energy_absolute_tolerance=1.0e-12,
            relative_tolerance=1.0e-12,
            squared_energy_absolute_tolerance=1.0e-12,
            dimensionless_absolute_tolerance=1.0e-12,
            refinement_tolerance=1.0e-10,
            application_threshold=1.0e-8,
        )

    def test__result__authenticates_independently_reconstructed_values(self) -> None:
        result = Periodic1DFourierLocalityAnalyzer().execute(self.configuration())
        wire = result.to_json()

        verified = Periodic1DFourierLocalityVerifier(result_wire=wire).result()

        assert verified.verification.passed
        assert {
            "parent_identity_binding",
            "refinement_channel_names",
            "mesh_8_nondominated_mask",
            "mesh_8_near_tie_mask",
            "mesh_8_first_joint_pass",
            "mesh_8_sustained_after_first_pass",
            "mesh_8_maximum_triangle",
            "mesh_8_rms_triangle",
            "gap_minimizing_role",
            "gap_minimizing_index",
            "gap_minimizing_reduced_momentum",
            "sampled_gap_threshold_side",
            "finite_qualification_disposition",
        } <= set(verified.verification.checks)
        assert verified.verification.subject_sha256 == hashlib.sha256(wire).hexdigest()
        readmitted = Periodic1DFourierLocalityVerifier(result_wire=wire).admit_stored(
            verification=verified.verification,
            visualization_data=verified.visualization_data,
        )
        assert readmitted.verification.to_json() == verified.verification.to_json()
        assert (
            Periodic1DFourierLocalityVerification.from_json(
                verified.verification.to_json()
            ).to_json()
            == verified.verification.to_json()
        )

    def test__admit_stored__rejects_tampered_visualization_projection(self) -> None:
        result = Periodic1DFourierLocalityAnalyzer().execute(self.configuration())
        verifier = Periodic1DFourierLocalityVerifier(result_wire=result.to_json())
        verified = verifier.result()
        values = verified.visualization_data.evaluation_lowest_energies.magnitude.copy()
        values[0] += 1.0e-6
        tampered = replace(
            verified.visualization_data,
            evaluation_lowest_energies=VectorQuantity(values, Unitless()),
        )

        with pytest.raises(ValueError, match="visualization"):
            verifier.admit_stored(
                verification=verified.verification,
                visualization_data=tampered,
            )

    def test__independent_verifier__detects_mutated_decision_inventory(self) -> None:
        result = Periodic1DFourierLocalityAnalyzer().execute(self.configuration())
        verified = Periodic1DFourierLocalityVerifier(
            result_wire=result.to_json()
        ).result()
        mesh = result.meshes[-1]
        mutated = (not mesh.near_tie_mask[0], *mesh.near_tie_mask[1:])
        object.__setattr__(mesh, "near_tie_mask", mutated)

        comparisons = (
            Periodic1DFourierLocalityIndependentVerifier()
            .execute(
                result,
                verified.visualization_data,
            )
            .comparisons
        )

        assert not comparisons["mesh_8_near_tie_mask"].result().passed

    def test__result__does_not_invoke_production_analyzer(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        result = Periodic1DFourierLocalityAnalyzer().execute(self.configuration())

        def forbidden(*_args: object, **_kwargs: object) -> None:
            raise AssertionError("production analyzer must not run during verification")

        monkeypatch.setattr(Periodic1DFourierLocalityAnalyzer, "execute", forbidden)

        verified = Periodic1DFourierLocalityVerifier(
            result_wire=result.to_json()
        ).result()

        assert np.isfinite(tuple(verified.verification.checks.values())).all()

    def test__visualize__returns_complete_authenticated_png_inventory(self) -> None:
        result = Periodic1DFourierLocalityAnalyzer().execute(self.configuration())
        verified = Periodic1DFourierLocalityVerifier(
            result_wire=result.to_json()
        ).result()

        visualizations = Periodic1DFourierLocalityVisualizer(
            data=verified.visualization_data,
            verification=verified.verification,
        ).visualize()

        assert {value.plot for value in visualizations} == {
            Periodic1DFourierLocalityVisualizationPlotEnum.fourier_locality,
            Periodic1DFourierLocalityVisualizationPlotEnum.route_agreement,
        }
        assert all(
            value.png.startswith(b"\x89PNG\r\n\x1a\n") for value in visualizations
        )

    def test__visualize__rejects_unrelated_projection_digest(self) -> None:
        result = Periodic1DFourierLocalityAnalyzer().execute(self.configuration())
        verified = Periodic1DFourierLocalityVerifier(
            result_wire=result.to_json()
        ).result()
        unrelated = replace(
            verified.verification,
            visualization_data_sha256="0" * 64,
        )

        with pytest.raises(ValueError, match="visualization"):
            Periodic1DFourierLocalityVisualizer(
                data=verified.visualization_data,
                verification=unrelated,
            ).visualize()
