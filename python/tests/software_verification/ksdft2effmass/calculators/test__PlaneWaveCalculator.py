r"""Software verification of ``AbstractPlaneWaveCalculator``.

Evidence profile: routine

Bounded artifact scope: backend-neutral plane-wave DFT calculator ABC ownership.

Facet and represented meaning

The nominal ABC represents typed application composition for one exact concrete
integration operation while leaving native records and effects integration-owned.

Intrinsic and cross-object scope

Tests cover backend-neutral ownership plus statically typed nominal conformance and
structural-lookalike rejection. Package export inventory, Workflow authorization,
process execution,
native diagnostics, result admission, and scientific interpretation remain separate.

VVUQ and scientific exclusions

This is synthetic software verification. It invokes no calculator and establishes no
numerical verification, scientific validation, uncertainty quantification, or
physical claim.
"""

from dataclasses import dataclass
from typing import assert_type

import pytest

from ksdft2effmass.calculators.dft.pw import AbstractPlaneWaveCalculator
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
SUT = AbstractPlaneWaveCalculator


@dataclass(frozen=True, slots=True)
class _FixtureInput:
    """Synthetic typed input used only for nominal conformance."""

    value: str


@dataclass(frozen=True, slots=True)
class _FixtureOutput:
    """Synthetic immutable output used only for nominal conformance."""

    value: str


class _FixturePlaneWaveCalculator(
    AbstractPlaneWaveCalculator[_FixtureInput, _FixtureOutput]
):
    """Deterministic nominal fixture that performs no external effect."""

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

        Acceptance: The ABC's exact defining module is calculator-owned and
        contains no Quantum ESPRESSO package name.
        """
        assert SUT.__module__ == "ksdft2effmass.calculators.dft.pw.calculator"
        assert "quantum_espresso" not in SUT.__module__

    def test_abc__rejects_method_matching_non_inheriting_lookalike(self) -> None:
        """Require explicit inheritance rather than matching method names."""

        class CalculatorLookalike:
            def execute(
                self,
                simulation_input: _FixtureInput,
                context: TaskExecutionContext,
            ) -> _FixtureOutput:
                return _FixtureOutput(simulation_input.value)

        assert not isinstance(CalculatorLookalike(), SUT)

    def test_abc__nominal_subclass__accepts_typed_executor(
        self,
    ) -> None:
        """Evidence ID: SV-PLANE-WAVE-CALCULATOR-002

        Requirement: A concretely typed integration executor satisfies the generic
        port only by explicit nominal inheritance, without plugin registration.

        Acceptance: Strict mypy assignment and ``assert_type`` retain the exact
        fixture input/output types, the nominal ABC admits the implementation,
        and execution returns the expected immutable output.
        """
        calculator: AbstractPlaneWaveCalculator[_FixtureInput, _FixtureOutput] = (
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
