r"""Software verification of ``PlaneWaveCalculator``.

Evidence profile: routine

Bounded artifact scope: backend-neutral plane-wave DFT calculator protocol ownership.

Facet and represented meaning

The protocol represents typed application composition for one exact concrete
integration operation while leaving native records and effects integration-owned.

Intrinsic and cross-object scope

Tests cover backend-neutral ownership plus statically typed and runtime structural
conformance. Package export inventory, Workflow authorization, process execution,
native diagnostics, result admission, and scientific interpretation remain separate.

VVUQ and scientific exclusions

This is synthetic software verification. It invokes no calculator and establishes no
numerical verification, scientific validation, uncertainty quantification, or
physical claim.
"""

from dataclasses import dataclass
from typing import assert_type

import pytest

from ksdft2effmass.calculators.dft.pw import PlaneWaveCalculator
from ksdft2effmass.workflows import (
    AttemptIdentity,
    OperationIdentity,
    TaskActivationIdentity,
    TaskExecutionContext,
    TaskInstanceIdentity,
    WorkflowIdentity,
    WorkflowRunIdentity,
)

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

    def test_protocol__ownership__is_backend_neutral(self) -> None:
        """Evidence ID: SV-PLANE-WAVE-CALCULATOR-001

        Requirement: The generic plane-wave calculator port is defined by the
        backend-neutral ``calculators.dft.pw`` package rather than an integration.

        Acceptance: The protocol's exact defining module is calculator-owned and
        contains no Quantum ESPRESSO package name.
        """
        assert SUT.__module__ == "ksdft2effmass.calculators.dft.pw._calculator"
        assert "quantum_espresso" not in SUT.__module__

    def test_protocol__runtime_checkable__accepts_typed_structural_executor(
        self,
    ) -> None:
        """Evidence ID: SV-PLANE-WAVE-CALCULATOR-002

        Requirement: A concretely typed integration executor can satisfy the generic
        port structurally without inheriting a base class or registering a plugin.

        Acceptance: Strict mypy assignment and ``assert_type`` retain the exact
        fixture input/output types, the runtime protocol admits the implementation,
        and execution returns the expected immutable output.
        """
        calculator: PlaneWaveCalculator[_FixtureInput, _FixtureOutput] = (
            _FixturePlaneWaveCalculator()
        )
        context = TaskExecutionContext(
            WorkflowIdentity("workflow.synthetic"),
            WorkflowRunIdentity("run.synthetic"),
            TaskInstanceIdentity("task.synthetic"),
            TaskActivationIdentity("activation.synthetic"),
            OperationIdentity("operation.synthetic"),
            AttemptIdentity("attempt.synthetic"),
        )
        output = calculator.execute(_FixtureInput("input.synthetic"), context)

        assert isinstance(calculator, SUT)
        assert_type(output, _FixtureOutput)
        assert output == _FixtureOutput("input.synthetic")
