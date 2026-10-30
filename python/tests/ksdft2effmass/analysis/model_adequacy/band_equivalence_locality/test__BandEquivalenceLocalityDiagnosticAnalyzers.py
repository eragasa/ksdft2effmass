"""Contracts for independent locality diagnostic actions."""

from __future__ import annotations

import pytest
from projectkoios.physkit.units import ScalarQuantity, Unitless

from ksdft2effmass.analysis.diagnostics import BaseDiagnosticAnalyzer
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.diagnostics import (  # noqa: E501
    BandEquivalenceLocalityDiagnosticMethodEnum,
    IndependentBandMaximumDefectAnalyzer,
    IndependentParentMaximumDefectAnalyzer,
    IndependentShellPowerMaximumDefectAnalyzer,
    StoredIdentityMaximumDefectAnalyzer,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestBandEquivalenceLocalityDiagnosticAnalyzers:
    """Establish the typed diagnostic ActionObject lifecycle."""

    def test__actions__implement_the_base_diagnostic_contract(self) -> None:
        tolerance = ScalarQuantity(1.0e-10, Unitless())
        analyzers = (
            StoredIdentityMaximumDefectAnalyzer(
                ScalarQuantity(1.0e-12, Unitless()), tolerance
            ),
            IndependentParentMaximumDefectAnalyzer(
                ScalarQuantity(2.0e-12, Unitless()), tolerance
            ),
            IndependentBandMaximumDefectAnalyzer(
                ScalarQuantity(3.0e-12, Unitless()), tolerance
            ),
            IndependentShellPowerMaximumDefectAnalyzer(
                ScalarQuantity(4.0e-12, Unitless()), tolerance
            ),
        )

        assert all(
            isinstance(analyzer, BaseDiagnosticAnalyzer) for analyzer in analyzers
        )
        assert tuple(analyzer.result().value.magnitude for analyzer in analyzers) == (
            1.0e-12,
            2.0e-12,
            3.0e-12,
            4.0e-12,
        )
        assert all(analyzer.result().atol == tolerance for analyzer in analyzers)
        assert all(analyzer.result().rtol == 0.0 for analyzer in analyzers)

    def test__method_identity__uses_explicit_wire_conversion(self) -> None:
        for method in BandEquivalenceLocalityDiagnosticMethodEnum:
            assert (
                BandEquivalenceLocalityDiagnosticMethodEnum.from_wire(method.to_wire())
                is method
            )

        with pytest.raises(TypeError, match="built-in string"):
            BandEquivalenceLocalityDiagnosticMethodEnum.from_wire(1)  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="unknown diagnostic method"):
            BandEquivalenceLocalityDiagnosticMethodEnum.from_wire("unknown")
