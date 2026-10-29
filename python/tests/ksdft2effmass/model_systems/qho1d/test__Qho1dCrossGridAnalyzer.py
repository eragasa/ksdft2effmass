"""Software verification for direct QHO1D adjacent-grid diagnostics."""

from dataclasses import replace

import pytest
from projectkoios.physkit.linalg.matrix.norm import FrobeniusMatrixNorm
from projectkoios.physkit.units import MatrixQuantity, ScalarQuantity

from ksdft2effmass.model_systems.qho1d import (
    Qho1dAnalysisRequest,
    Qho1dAnalyzer,
    Qho1dCalculationResult,
    Qho1dConfiguration,
    Qho1dCrossGridAnalysisRequest,
    Qho1dCrossGridAnalysisResult,
    Qho1dCrossGridAnalyzer,
    Qho1dCrossGridVerifier,
)


class TestQho1dCrossGridAnalyzer:
    """Verify typed adjacent-grid analysis without legacy study dependencies."""

    @staticmethod
    def configuration(
        grid_spacings: tuple[float, ...] = (0.2, 0.1, 0.05),
    ) -> Qho1dConfiguration:
        """Return a compact direct configuration with explicit adjacent grids."""
        return Qho1dConfiguration(
            hbar=1.0,
            mass=1.0,
            omega=1.0,
            box_half_widths=(4.0,),
            grid_spacings=grid_spacings,
            retained_dimensions=(2, 4),
            selected_box_half_width=4.0,
            selected_grid_spacing=grid_spacings[-1],
            selected_retained_dimension=4,
            displayed_states=2,
        )

    @classmethod
    def calculation(
        cls,
        grid_spacings: tuple[float, ...] = (0.2, 0.1, 0.05),
    ) -> Qho1dCalculationResult:
        """Return one direct calculation for the compact configuration."""
        return Qho1dAnalyzer(
            Qho1dAnalysisRequest(
                configuration=cls.configuration(grid_spacings),
                calculation_family="qho1d-spatial-truncation",
                execution_id="cross-grid-test",
                evidence_status="illustrative numerical experiment",
                claim_boundary="test fixture; no continuum-convergence claim",
            )
        ).execute()

    def test_method__execute__calculates_ordered_adjacent_grid_norms(self) -> None:
        """Every fixed-box, fixed-dimension adjacent pair is compared once."""
        calculation = self.calculation()
        request = Qho1dCrossGridAnalysisRequest(calculation)
        analyzer = Qho1dCrossGridAnalyzer(request)
        analysis = analyzer.execute()

        assert analyzer.request is request
        assert len(analysis.comparisons) == 4
        assert tuple(value.key for value in analysis.comparisons) == (
            (4.0, 2, 0.2, 0.1),
            (4.0, 2, 0.1, 0.05),
            (4.0, 4, 0.2, 0.1),
            (4.0, 4, 0.1, 0.05),
        )
        coarse = calculation.cases[0]
        fine = calculation.cases[2]
        difference = MatrixQuantity(
            coarse.pulled_back_hamiltonian.magnitude
            - fine.pulled_back_hamiltonian.magnitude,
            coarse.pulled_back_hamiltonian.unit,
        )
        expected = FrobeniusMatrixNorm(difference).result().magnitude
        assert analysis.comparisons[0].coarse_minus_fine_frobenius.magnitude == (
            expected
        )

    def test_representation__typed_json__round_trips_exact_bytes(self) -> None:
        """The diagnostic aggregate uses the shared typed serialization boundary."""
        analysis = Qho1dCrossGridAnalyzer(
            Qho1dCrossGridAnalysisRequest(self.calculation())
        ).execute()
        wire = analysis.to_json()

        reconstructed = Qho1dCrossGridAnalysisResult.from_json(wire)

        assert reconstructed.to_json() == wire
        assert tuple(value.key for value in reconstructed.comparisons) == tuple(
            value.key for value in analysis.comparisons
        )

    def test_method__verifier__detects_changed_derived_norm(self) -> None:
        """Verification recomputes each norm from authoritative case matrices."""
        calculation = self.calculation()
        analysis = Qho1dCrossGridAnalyzer(
            Qho1dCrossGridAnalysisRequest(calculation)
        ).execute()
        verification = Qho1dCrossGridVerifier().execute(calculation, analysis)
        first = analysis.comparisons[0]
        changed_first = replace(
            first,
            coarse_minus_fine_frobenius=ScalarQuantity(
                first.coarse_minus_fine_frobenius.magnitude + 1.0e-6,
                first.coarse_minus_fine_frobenius.unit,
            ),
        )
        changed = replace(
            analysis,
            comparisons=(changed_first, *analysis.comparisons[1:]),
        )

        changed_verification = Qho1dCrossGridVerifier().execute(calculation, changed)

        assert verification.passed
        assert len(verification.observations) == 20
        assert not changed_verification.passed

    def test_method__execute__rejects_a_sweep_without_adjacent_grids(self) -> None:
        """One grid cannot define a coarse/fine diagnostic."""
        calculation = self.calculation((0.1,))

        with pytest.raises(
            ValueError,
            match="cross-grid analysis requires at least two grid spacings",
        ):
            Qho1dCrossGridAnalyzer(Qho1dCrossGridAnalysisRequest(calculation)).execute()
