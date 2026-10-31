"""Diagnostic actions for independent band-equivalence verification."""

from __future__ import annotations

from projectkoios.physkit.units import ScalarQuantity, Unitless

from ksdft2effmass.analysis.diagnostics import (
    BaseDiagnosticAnalyzer,
    DiagnosticObservation,
)
from ksdft2effmass.serialization import StringWireEnum


class BandEquivalenceLocalityDiagnosticMethodEnum(StringWireEnum):
    """Identify each independently verified locality diagnostic."""

    storedIdentityMaximumDefect = "stored_identity_maximum_defect"
    independentParentMaximumDefect = "independent_parent_maximum_defect"
    independentBandMaximumDefect = "independent_band_maximum_defect"
    independentShellPowerDefect = "independent_shell_power_maximum_defect"


class StoredIdentityMaximumDefectAnalyzer(
    BaseDiagnosticAnalyzer[BandEquivalenceLocalityDiagnosticMethodEnum]
):
    """Retain the maximum stored-identity defect and its threshold."""

    __slots__ = ("_atol", "_value")

    def __init__(self, value: ScalarQuantity, atol: ScalarQuantity) -> None:
        self._value = self._admit(value, "value")
        self._atol = self._admit(atol, "atol")

    @property
    def method(self) -> BandEquivalenceLocalityDiagnosticMethodEnum:
        """Return the stored-identity diagnostic identity."""
        return BandEquivalenceLocalityDiagnosticMethodEnum.storedIdentityMaximumDefect

    def result(self) -> DiagnosticObservation:
        """Return the bound stored-identity observation."""
        return DiagnosticObservation(value=self._value, atol=self._atol, rtol=0.0)

    def _admit(self, value: ScalarQuantity, name: str) -> ScalarQuantity:
        if type(value) is not ScalarQuantity:
            raise TypeError(f"{name} must be ScalarQuantity")
        if type(value.unit) is not Unitless:
            raise ValueError(f"{name} must be explicitly unitless")
        return value


class IndependentParentMaximumDefectAnalyzer(
    BaseDiagnosticAnalyzer[BandEquivalenceLocalityDiagnosticMethodEnum]
):
    """Retain the maximum independent parent-field defect and its threshold."""

    __slots__ = ("_atol", "_value")

    def __init__(self, value: ScalarQuantity, atol: ScalarQuantity) -> None:
        self._value = self._admit(value, "value")
        self._atol = self._admit(atol, "atol")

    @property
    def method(self) -> BandEquivalenceLocalityDiagnosticMethodEnum:
        """Return the independent-parent diagnostic identity."""
        return (
            BandEquivalenceLocalityDiagnosticMethodEnum.independentParentMaximumDefect
        )

    def result(self) -> DiagnosticObservation:
        """Return the bound independent-parent observation."""
        return DiagnosticObservation(value=self._value, atol=self._atol, rtol=0.0)

    def _admit(self, value: ScalarQuantity, name: str) -> ScalarQuantity:
        if type(value) is not ScalarQuantity:
            raise TypeError(f"{name} must be ScalarQuantity")
        if type(value.unit) is not Unitless:
            raise ValueError(f"{name} must be explicitly unitless")
        return value


class IndependentBandMaximumDefectAnalyzer(
    BaseDiagnosticAnalyzer[BandEquivalenceLocalityDiagnosticMethodEnum]
):
    """Retain the maximum independent sorted-band defect and its threshold."""

    __slots__ = ("_atol", "_value")

    def __init__(self, value: ScalarQuantity, atol: ScalarQuantity) -> None:
        self._value = self._admit(value, "value")
        self._atol = self._admit(atol, "atol")

    @property
    def method(self) -> BandEquivalenceLocalityDiagnosticMethodEnum:
        """Return the independent-band diagnostic identity."""
        return BandEquivalenceLocalityDiagnosticMethodEnum.independentBandMaximumDefect

    def result(self) -> DiagnosticObservation:
        """Return the bound independent-band observation."""
        return DiagnosticObservation(value=self._value, atol=self._atol, rtol=0.0)

    def _admit(self, value: ScalarQuantity, name: str) -> ScalarQuantity:
        if type(value) is not ScalarQuantity:
            raise TypeError(f"{name} must be ScalarQuantity")
        if type(value.unit) is not Unitless:
            raise ValueError(f"{name} must be explicitly unitless")
        return value


class IndependentShellPowerMaximumDefectAnalyzer(
    BaseDiagnosticAnalyzer[BandEquivalenceLocalityDiagnosticMethodEnum]
):
    """Retain the maximum independent shell-power defect and its threshold."""

    __slots__ = ("_atol", "_value")

    def __init__(self, value: ScalarQuantity, atol: ScalarQuantity) -> None:
        self._value = self._admit(value, "value")
        self._atol = self._admit(atol, "atol")

    @property
    def method(self) -> BandEquivalenceLocalityDiagnosticMethodEnum:
        """Return the independent-shell-power diagnostic identity."""
        return BandEquivalenceLocalityDiagnosticMethodEnum.independentShellPowerDefect

    def result(self) -> DiagnosticObservation:
        """Return the bound independent-shell-power observation."""
        return DiagnosticObservation(value=self._value, atol=self._atol, rtol=0.0)

    def _admit(self, value: ScalarQuantity, name: str) -> ScalarQuantity:
        if type(value) is not ScalarQuantity:
            raise TypeError(f"{name} must be ScalarQuantity")
        if type(value.unit) is not Unitless:
            raise ValueError(f"{name} must be explicitly unitless")
        return value


__all__ = [
    "BandEquivalenceLocalityDiagnosticMethodEnum",
    "IndependentBandMaximumDefectAnalyzer",
    "IndependentParentMaximumDefectAnalyzer",
    "IndependentShellPowerMaximumDefectAnalyzer",
    "StoredIdentityMaximumDefectAnalyzer",
]
