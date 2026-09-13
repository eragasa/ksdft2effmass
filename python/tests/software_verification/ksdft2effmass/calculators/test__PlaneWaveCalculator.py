r"""Software verification of ``PlaneWaveCalculator``.

Evidence profile: routine

Bounded artifact scope: backend-neutral plane-wave DFT calculator protocol ownership.

Facet and represented meaning

The protocol represents typed application composition for one exact concrete
integration operation while leaving native records and effects integration-owned.

Intrinsic and cross-object scope

Tests cover public export and structural conformance only. Workflow authorization,
process execution, native diagnostics, result admission, and scientific interpretation
remain separate.

VVUQ and scientific exclusions

This is synthetic software verification. It invokes no calculator and establishes no
numerical verification, scientific validation, uncertainty quantification, or
physical claim.
"""

from dataclasses import dataclass

import pytest

import ksdft2effmass.calculators.dft.pw as plane_wave
from ksdft2effmass.calculators.dft.pw import PlaneWaveCalculator
from ksdft2effmass.workflows import TaskExecutionContext

pytestmark = pytest.mark.software_verification
SUT = PlaneWaveCalculator


@dataclass(frozen=True, slots=True)
class _FixtureInput:
    """Synthetic typed input used only for structural conformance."""

    value: str


@dataclass(frozen=True, slots=True)
class _FixtureOutput:
    """Synthetic immutable output used only for structural conformance."""

    value: str


class _FixturePlaneWaveCalculator:
    """Deterministic protocol fixture that performs no external effect."""

    def execute(
        self,
        simulation_input: _FixtureInput,
        context: TaskExecutionContext,
    ) -> _FixtureOutput:
        """Return a new synthetic output without using the execution context."""
        return _FixtureOutput(simulation_input.value)


class TestPlaneWaveCalculator:
    """Own software verification of the generic calculator port."""

    def test_public_api__package__exports_backend_neutral_port(self) -> None:
        """Evidence ID: SV-PLANE-WAVE-CALCULATOR-001

        Requirement: The generic plane-wave calculator port is public only from the
        backend-neutral ``calculators.dft.pw`` package.

        Acceptance: The package root exports the exact protocol and its defining
        module contains no Quantum ESPRESSO package name.
        """
        assert plane_wave.PlaneWaveCalculator is SUT
        assert "PlaneWaveCalculator" in plane_wave.__all__
        assert "quantum_espresso" not in SUT.__module__

    def test_protocol__runtime_checkable__accepts_typed_structural_executor(
        self,
    ) -> None:
        """Evidence ID: SV-PLANE-WAVE-CALCULATOR-002

        Requirement: A concretely typed integration executor can satisfy the generic
        port structurally without inheriting a base class or registering a plugin.

        Acceptance: The deterministic local fixture is recognized by the
        runtime-checkable protocol.
        """
        assert isinstance(_FixturePlaneWaveCalculator(), SUT)
