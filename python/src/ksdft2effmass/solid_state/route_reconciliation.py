"""Reusable uniform-link and quotient-seam reconciliation for one scalar case."""

from __future__ import annotations

import math
from dataclasses import dataclass

from .boundary_phases import BoundaryTwistLift
from .gauge_bridges import (
    TwistGaugeBridgeConstructor,
    TwistGaugeBridgeResult,
    TwistGaugeEquivalenceAnalyzer,
    TwistGaugeEquivalenceResult,
)
from .geometry import FiniteLatticeShape
from .lattice_models import LocalizedPerturbation, ScalarHoppingModel
from .operator_composition import (
    ScalarFiniteLatticeOperatorAdder,
    ScalarFiniteLatticeOperatorCompatibilityAnalyzer,
)
from .operator_construction import (
    LocalizedPerturbationOperatorConstructor,
    TwistedSupercellOperatorConstructor,
)
from .quotient_seam import QuotientSeamOperatorConstructor
from .represented_operators import ScalarFiniteLatticeOperator


@dataclass(frozen=True, slots=True)
class ScalarFiniteLatticeRouteReconciliationResult:
    """Retain both gauge routes and their parent, perturbation, and full comparisons."""

    identifier: str
    uniform_parent: ScalarFiniteLatticeOperator
    uniform_perturbation: ScalarFiniteLatticeOperator
    uniform_full: ScalarFiniteLatticeOperator
    seam_parent: ScalarFiniteLatticeOperator
    seam_perturbation: ScalarFiniteLatticeOperator
    seam_full: ScalarFiniteLatticeOperator
    bridge: TwistGaugeBridgeResult
    parent_equivalence: TwistGaugeEquivalenceResult
    perturbation_equivalence: TwistGaugeEquivalenceResult
    full_equivalence: TwistGaugeEquivalenceResult

    def __post_init__(self) -> None:
        """Validate exact retained types and comparison correlations."""
        if type(self.identifier) is not str:
            raise TypeError("identifier must be a string")
        if not self.identifier:
            raise ValueError("identifier must be nonempty")
        operators = (
            self.uniform_parent,
            self.uniform_perturbation,
            self.uniform_full,
            self.seam_parent,
            self.seam_perturbation,
            self.seam_full,
        )
        if any(
            type(operator) is not ScalarFiniteLatticeOperator for operator in operators
        ):
            raise TypeError("route operators must be ScalarFiniteLatticeOperator")
        if type(self.bridge) is not TwistGaugeBridgeResult:
            raise TypeError("bridge must be TwistGaugeBridgeResult")
        equivalences = (
            self.parent_equivalence,
            self.perturbation_equivalence,
            self.full_equivalence,
        )
        if any(
            type(result) is not TwistGaugeEquivalenceResult for result in equivalences
        ):
            raise TypeError("equivalence results must be TwistGaugeEquivalenceResult")
        expected_pairs = (
            (self.parent_equivalence, self.uniform_parent, self.seam_parent),
            (
                self.perturbation_equivalence,
                self.uniform_perturbation,
                self.seam_perturbation,
            ),
            (self.full_equivalence, self.uniform_full, self.seam_full),
        )
        for result, source, target in expected_pairs:
            if result.source is not source or result.target is not target:
                raise ValueError(
                    "equivalence result must correlate exact route operators"
                )
            if result.bridge is not self.bridge:
                raise ValueError("equivalence results must share the retained bridge")
        tolerances = {
            result.absolute_tolerance
            for result in (
                self.parent_equivalence,
                self.perturbation_equivalence,
                self.full_equivalence,
            )
        }
        if len(tolerances) != 1:
            raise ValueError("route equivalence results must share one tolerance")

    @property
    def is_reconciled(self) -> bool:
        """Return whether parent, perturbation, and full routes all pass."""
        return (
            self.parent_equivalence.is_equivalent
            and self.perturbation_equivalence.is_equivalent
            and self.full_equivalence.is_equivalent
        )


class ScalarFiniteLatticeRouteReconciliationWorkflow:
    """Construct and reconcile both supported gauges for one scalar finite case."""

    __slots__ = ()

    def execute(
        self,
        identifier: str,
        model: ScalarHoppingModel,
        perturbation: LocalizedPerturbation,
        shape: FiniteLatticeShape,
        twist: BoundaryTwistLift,
        *,
        absolute_tolerance: float,
    ) -> ScalarFiniteLatticeRouteReconciliationResult:
        """Return both sparse routes and three explicit gauge comparisons."""
        if type(identifier) is not str:
            raise TypeError("identifier must be a string")
        if not identifier:
            raise ValueError("identifier must be nonempty")
        if type(model) is not ScalarHoppingModel:
            raise TypeError("model must be ScalarHoppingModel")
        if type(perturbation) is not LocalizedPerturbation:
            raise TypeError("perturbation must be LocalizedPerturbation")
        if type(shape) is not FiniteLatticeShape:
            raise TypeError("shape must be FiniteLatticeShape")
        if type(twist) is not BoundaryTwistLift:
            raise TypeError("twist must be BoundaryTwistLift")
        if type(absolute_tolerance) is not float:
            raise TypeError("absolute_tolerance must be a built-in float")
        if not math.isfinite(absolute_tolerance) or absolute_tolerance < 0.0:
            raise ValueError("absolute_tolerance must be finite and nonnegative")

        uniform_parent = TwistedSupercellOperatorConstructor().execute(
            f"{identifier}.uniform.parent", model, shape, twist
        )
        uniform_perturbation = LocalizedPerturbationOperatorConstructor().execute(
            f"{identifier}.uniform.perturbation", perturbation, shape, twist
        )
        seam_constructor = QuotientSeamOperatorConstructor()
        seam_parent = seam_constructor.execute_hopping(
            f"{identifier}.seam.parent", model, shape, twist
        )
        seam_perturbation = seam_constructor.execute_perturbation(
            f"{identifier}.seam.perturbation", perturbation, shape, twist
        )
        compatibility_analyzer = ScalarFiniteLatticeOperatorCompatibilityAnalyzer()
        adder = ScalarFiniteLatticeOperatorAdder()
        uniform_full = adder.execute(
            f"{identifier}.uniform.full",
            uniform_parent,
            uniform_perturbation,
            compatibility_analyzer.execute(uniform_parent, uniform_perturbation),
        )
        seam_full = adder.execute(
            f"{identifier}.seam.full",
            seam_parent,
            seam_perturbation,
            compatibility_analyzer.execute(seam_parent, seam_perturbation),
        )
        bridge = TwistGaugeBridgeConstructor().execute(
            shape, uniform_parent.twist_fiber
        )
        equivalence_analyzer = TwistGaugeEquivalenceAnalyzer()
        parent_equivalence = equivalence_analyzer.execute(
            uniform_parent,
            seam_parent,
            bridge,
            absolute_tolerance=absolute_tolerance,
        )
        perturbation_equivalence = equivalence_analyzer.execute(
            uniform_perturbation,
            seam_perturbation,
            bridge,
            absolute_tolerance=absolute_tolerance,
        )
        full_equivalence = equivalence_analyzer.execute(
            uniform_full,
            seam_full,
            bridge,
            absolute_tolerance=absolute_tolerance,
        )
        return ScalarFiniteLatticeRouteReconciliationResult(
            identifier,
            uniform_parent,
            uniform_perturbation,
            uniform_full,
            seam_parent,
            seam_perturbation,
            seam_full,
            bridge,
            parent_equivalence,
            perturbation_equivalence,
            full_equivalence,
        )
