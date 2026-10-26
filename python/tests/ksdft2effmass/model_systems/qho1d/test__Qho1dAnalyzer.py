"""Software verification for the direct typed QHO1D analyzer."""

from pathlib import Path

import numpy as np

from ksdft2effmass.model_systems.qho1d import (
    Qho1dAnalyzer,
    Qho1dCalculationResult,
    Qho1dConfiguration,
)
from ksdft2effmass.serialization import TypedJsonMappingDeserializer


class TestQho1dAnalyzer:
    """Verify direct calculation composition and shared JSON ownership."""

    @staticmethod
    def configuration() -> Qho1dConfiguration:
        """Return the maintained direct-sweep configuration."""
        return Qho1dConfiguration(
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

    @classmethod
    def result(cls) -> Qho1dCalculationResult:
        """Return one complete maintained direct result."""
        return Qho1dAnalyzer().execute(
            cls.configuration(),
            calculation_family="qho1d-spatial-truncation",
            execution_id="test-direct",
            evidence_status="illustrative numerical experiment",
            claim_boundary="test fixture; no scientific-validation claim",
        )

    def test_method__execute__composes_ordered_typed_sweep(self) -> None:
        """The analyzer retains all 27 cases and their common-space invariant."""
        result = self.result()

        assert len(result.cases) == 27
        assert result.cases[0].key == (4.0, 0.2, 2)
        assert result.cases[-1].key == (8.0, 0.05, 6)
        for case in result.cases:
            np.testing.assert_array_equal(
                case.difference.magnitude,
                case.pulled_back_hamiltonian.magnitude
                - case.reference_hamiltonian.magnitude,
            )
            assert case.residual_frobenius.magnitude >= 0.0

    def test_case__constructor__owns_four_semantic_sections(self) -> None:
        """Each case stores semantic sections while projections remain convenient."""
        case = self.result().cases[0]

        assert tuple(case.__dataclass_fields__) == (
            "representation",
            "alignment",
            "hamiltonian_comparison",
            "residual",
            "_wire_layout",
        )
        assert case.grid_coordinates is case.representation.grid_coordinates
        assert case.injection is case.alignment.injection
        assert (
            case.pulled_back_hamiltonian
            is case.hamiltonian_comparison.pulled_back_hamiltonian
        )
        assert case.residual_frobenius is case.residual.frobenius

    def test_representation__shared_typed_json__round_trips_exact_bytes(self) -> None:
        """The root record uses the generic final JSON boundary without data loss."""
        result = self.result()
        wire = result.to_json()
        reconstructed = Qho1dCalculationResult.from_json(wire)
        mapping = TypedJsonMappingDeserializer().deserialize(wire)
        cases_value = mapping["cases"]
        assert isinstance(cases_value, tuple)
        assert isinstance(cases_value[0], dict)
        assert set(cases_value[0]) == {
            "representation",
            "alignment",
            "hamiltonian_comparison",
            "residual",
        }

        assert reconstructed.to_json() == wire
        assert len(reconstructed.cases) == 27
        np.testing.assert_array_equal(
            reconstructed.selected_state_comparison.finite_wavefunctions.magnitude,
            result.selected_state_comparison.finite_wavefunctions.magnitude,
        )

    def test_source__matrix_norms__separate_production_and_verification_routes(
        self,
    ) -> None:
        """Production uses PhysKit while independent verification retains NumPy."""
        source_root = Path(__file__).resolve().parents[4] / "src" / "ksdft2effmass"
        production_paths = (
            source_root / "model_systems" / "qho1d" / "analysis.py",
            source_root / "model_systems" / "qho1d" / "comparison.py",
            source_root / "model_systems" / "qho1d" / "cross_grid.py",
        )
        for path in production_paths:
            source = path.read_text(encoding="utf-8")
            assert "FrobeniusMatrixNorm" in source
            assert "np.linalg.norm" not in source
        verification_source = (
            source_root / "model_systems" / "qho1d" / "verification.py"
        ).read_text(encoding="utf-8")
        assert "np.linalg.norm" in verification_source
        assert "FrobeniusMatrixNorm" not in verification_source

    def test_source__successor_modules__contain_no_custom_json_transport(self) -> None:
        """Successor domain modules delegate array transport to shared serialization."""
        source_root = Path(__file__).resolve().parents[4] / "src" / "ksdft2effmass"
        paths = (
            source_root / "model_systems" / "qho1d" / "configuration.py",
            source_root / "model_systems" / "qho1d" / "case_sections.py",
            source_root / "model_systems" / "qho1d" / "result.py",
            source_root / "model_systems" / "qho1d" / "analysis.py",
            source_root / "model_systems" / "qho1d" / "cross_grid.py",
            source_root / "model_systems" / "qho1d" / "verification.py",
            source_root / "model_systems" / "qho1d" / "visualization.py",
        )
        for path in paths:
            source = path.read_text(encoding="utf-8")
            assert ".tolist(" not in source
            assert "import json" not in source
