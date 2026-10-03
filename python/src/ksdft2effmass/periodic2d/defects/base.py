r"""Encapsulated finite-extent perturbations of periodic two-dimensional parents.

The software model distinguishes the translation-invariant bulk hopping model
:math:`H_0`, the finite-support perturbation :math:`\Delta H`, and their represented
finite-periodic sum :math:`H_\mathrm{def}=H_0+\Delta H`. An onsite-only
:math:`\Delta H` is a perturbation potential; directed bond terms represent the more
general finite-extent operator changes required by the campaign.
"""

from dataclasses import dataclass

from ksdft2effmass.operators import ScalarQuantity
from ksdft2effmass.solid_state import (
    BoundaryTwistLift,
    FiniteLatticeShape,
    LatticeCoordinate,
    LatticeDimension,
    LocalizedOnsiteTerm,
    LocalizedPerturbation,
    LocalizedPerturbationOperatorConstructor,
    ScalarFiniteLatticeOperator,
    ScalarFiniteLatticeOperatorAdder,
    ScalarFiniteLatticeOperatorCompatibilityAnalyzer,
    ScalarFiniteLatticeOperatorCompatibilityResult,
    ScalarHoppingModel,
    TwistedSupercellOperatorConstructor,
)

from .extraction import (
    Periodic2DDefectExtractionRequest,
    Periodic2DDefectExtractionResult,
    Periodic2DDefectPerturbationExtractor,
)
from .locality import (
    Periodic2DDefectLocalityAnalyzer,
    Periodic2DDefectLocalityRequest,
    Periodic2DDefectLocalityResult,
)


@dataclass(frozen=True, slots=True)
class Periodic2DDefectModel:
    """Encapsulate a bulk model and one finite-support perturbation.

    Parameters
    ----------
    identifier
        Nonempty identity for this bulk-plus-perturbation model.
    bulk
        Translation-invariant scalar hopping model representing the periodic parent.
    perturbation
        Finite ordered inventory of localized onsite and directed-bond changes.

    Notes
    -----
    Both components must be two-dimensional. Unit, basis, and energy-reference
    compatibility is cross-object policy owned by ``Periodic2DDefectRepresenter``.
    The model does not identify a finite matrix until a shape and boundary twist are
    supplied.
    """

    identifier: str
    bulk: ScalarHoppingModel
    perturbation: LocalizedPerturbation

    def __post_init__(self) -> None:
        """Require exact two-dimensional state and a stable identity."""
        if type(self.identifier) is not str:
            raise TypeError("identifier must be a built-in str")
        if not self.identifier:
            raise ValueError("identifier must be nonempty")
        if type(self.bulk) is not ScalarHoppingModel:
            raise TypeError("bulk must be ScalarHoppingModel")
        if type(self.perturbation) is not LocalizedPerturbation:
            raise TypeError("perturbation must be LocalizedPerturbation")
        if self.bulk.dimension is not LatticeDimension.TWO:
            raise ValueError("bulk must be two-dimensional")
        if self.perturbation.dimension is not LatticeDimension.TWO:
            raise ValueError("perturbation must be two-dimensional")

    @property
    def represents_onsite_potential(self) -> bool:
        """Return whether the perturbation contains onsite potential terms only."""
        return all(
            type(term) is LocalizedOnsiteTerm for term in self.perturbation.terms
        )


@dataclass(frozen=True, slots=True)
class Periodic2DDefectRepresentationRequest:
    """Request one finite-periodic representation of a defect model.

    Parameters
    ----------
    model
        Encapsulated two-dimensional bulk and finite-support perturbation.
    shape
        Finite two-dimensional periodic lattice shape.
    twist
        Unreduced two-dimensional boundary twist measured in turns.
    """

    model: Periodic2DDefectModel
    shape: FiniteLatticeShape
    twist: BoundaryTwistLift

    def __post_init__(self) -> None:
        """Require exact two-dimensional representation inputs."""
        if type(self.model) is not Periodic2DDefectModel:
            raise TypeError("model must be Periodic2DDefectModel")
        if type(self.shape) is not FiniteLatticeShape:
            raise TypeError("shape must be FiniteLatticeShape")
        if type(self.twist) is not BoundaryTwistLift:
            raise TypeError("twist must be BoundaryTwistLift")
        if self.shape.dimension is not LatticeDimension.TWO:
            raise ValueError("shape must be two-dimensional")
        if self.twist.dimension is not LatticeDimension.TWO:
            raise ValueError("twist must be two-dimensional")


@dataclass(frozen=True, slots=True)
class Periodic2DDefectRepresentationResult:
    """Retain separate bulk, perturbation, and composed defect operators.

    Parameters
    ----------
    bulk_operator
        Finite-periodic representation of the translation-invariant parent.
    perturbation_operator
        Finite-periodic representation of the finite-support change.
    compatibility
        Complete compatibility finding for direct represented addition.
    defect_operator
        Sparse represented sum of bulk and perturbation operators.
    """

    bulk_operator: ScalarFiniteLatticeOperator
    perturbation_operator: ScalarFiniteLatticeOperator
    compatibility: ScalarFiniteLatticeOperatorCompatibilityResult
    defect_operator: ScalarFiniteLatticeOperator

    def __post_init__(self) -> None:
        """Require exact correlated operators and successful composition evidence."""
        if type(self.bulk_operator) is not ScalarFiniteLatticeOperator:
            raise TypeError("bulk_operator must be ScalarFiniteLatticeOperator")
        if type(self.perturbation_operator) is not ScalarFiniteLatticeOperator:
            raise TypeError("perturbation_operator must be ScalarFiniteLatticeOperator")
        if (
            type(self.compatibility)
            is not ScalarFiniteLatticeOperatorCompatibilityResult
        ):
            raise TypeError("compatibility uses the wrong AbstractResultObject type")
        if type(self.defect_operator) is not ScalarFiniteLatticeOperator:
            raise TypeError("defect_operator must be ScalarFiniteLatticeOperator")
        if self.compatibility.left is not self.bulk_operator:
            raise ValueError("compatibility must retain the exact bulk operator")
        if self.compatibility.right is not self.perturbation_operator:
            raise ValueError(
                "compatibility must retain the exact perturbation operator"
            )
        if not self.compatibility.compatible:
            raise ValueError("represented bulk and perturbation must be compatible")
        if self.defect_operator.shape != self.bulk_operator.shape:
            raise ValueError("defect and bulk represented shapes must agree")
        if self.defect_operator.twist_fiber != self.bulk_operator.twist_fiber:
            raise ValueError("defect and bulk twist fibers must agree")
        if self.defect_operator.basis_identifier != self.bulk_operator.basis_identifier:
            raise ValueError("defect and bulk bases must agree")
        if self.defect_operator.energy_reference != self.bulk_operator.energy_reference:
            raise ValueError("defect and bulk energy references must agree")
        if self.defect_operator.matrix.unit != self.bulk_operator.matrix.unit:
            raise ValueError("defect and bulk energy units must agree")


class Periodic2DDefectRepresenter:
    """Construct and compose compatible sparse bulk and defect representations."""

    __slots__ = ()

    bulk_constructor = TwistedSupercellOperatorConstructor()
    perturbation_constructor = LocalizedPerturbationOperatorConstructor()
    compatibility_analyzer = ScalarFiniteLatticeOperatorCompatibilityAnalyzer()
    operator_adder = ScalarFiniteLatticeOperatorAdder()

    def execute(
        self, request: Periodic2DDefectRepresentationRequest
    ) -> Periodic2DDefectRepresentationResult:
        r"""Represent :math:`H_0`, :math:`\Delta H`, and their compatible sum.

        Parameters
        ----------
        request
            Exact model, finite shape, and boundary twist.

        Returns
        -------
        Periodic2DDefectRepresentationResult
            Separate sparse parent and perturbation operators, compatibility evidence,
            and their sparse represented sum.

        Raises
        ------
        TypeError
            If ``request`` has the wrong exact semantic type.
        ValueError
            If units, basis, energy reference, geometry, or boundary phase are
            incompatible for represented addition.
        """
        if type(request) is not Periodic2DDefectRepresentationRequest:
            raise TypeError("request must be Periodic2DDefectRepresentationRequest")
        model = request.model
        bulk_operator = self.bulk_constructor.execute(
            f"{model.identifier}.bulk",
            model.bulk,
            request.shape,
            request.twist,
        )
        perturbation_operator = self.perturbation_constructor.execute(
            f"{model.identifier}.perturbation",
            model.perturbation,
            request.shape,
            request.twist,
        )
        compatibility = self.compatibility_analyzer.execute(
            bulk_operator, perturbation_operator
        )
        defect_operator = self.operator_adder.execute(
            f"{model.identifier}.defect",
            bulk_operator,
            perturbation_operator,
            compatibility,
        )
        return Periodic2DDefectRepresentationResult(
            bulk_operator,
            perturbation_operator,
            compatibility,
            defect_operator,
        )


@dataclass(frozen=True, slots=True)
class Periodic2DDefect:
    """Encapsulate a periodic parent modified by one finite-extent perturbation."""

    model: Periodic2DDefectModel

    def __post_init__(self) -> None:
        """Require the exact immutable defect-model type."""
        if type(self.model) is not Periodic2DDefectModel:
            raise TypeError("model must be Periodic2DDefectModel")

    def represent(
        self, *, shape: FiniteLatticeShape, twist: BoundaryTwistLift
    ) -> Periodic2DDefectRepresentationResult:
        """Return one finite-periodic sparse representation.

        Parameters
        ----------
        shape
            Two-dimensional finite-periodic lattice shape.
        twist
            Two-dimensional unreduced boundary twist in turns.

        Returns
        -------
        Periodic2DDefectRepresentationResult
            Separate bulk and finite-support perturbation operators together with the
            compatible represented defect operator.
        """
        return Periodic2DDefectRepresenter().execute(
            Periodic2DDefectRepresentationRequest(self.model, shape, twist)
        )

    def extract(
        self,
        *,
        bulk_operator: ScalarFiniteLatticeOperator,
        defect_operator: ScalarFiniteLatticeOperator,
    ) -> Periodic2DDefectExtractionResult:
        r"""Extract :math:`\Delta H` from compatible represented operators.

        Parameters
        ----------
        bulk_operator
            Periodic parent represented in the intended common conventions.
        defect_operator
            Modified operator represented in those same conventions.

        Returns
        -------
        Periodic2DDefectExtractionResult
            Compatibility evidence and the sparse represented difference.

        Notes
        -----
        This operation does not align bases, gauges, geometries, or energy references.
        Those conventions must already agree explicitly.
        """
        return Periodic2DDefectPerturbationExtractor().execute(
            Periodic2DDefectExtractionRequest(bulk_operator, defect_operator)
        )

    def analyze_locality(
        self,
        *,
        bulk_operator: ScalarFiniteLatticeOperator,
        defect_operator: ScalarFiniteLatticeOperator,
        origin: LatticeCoordinate,
        core_radius: int,
        exterior_frobenius_tolerance: ScalarQuantity,
        core_exterior_frobenius_tolerance: ScalarQuantity,
    ) -> Periodic2DDefectLocalityResult:
        """Assess whether the represented perturbation is confined to a core.

        Parameters
        ----------
        bulk_operator
            Periodic parent represented in the intended common conventions.
        defect_operator
            Modified operator represented in those same conventions.
        origin
            Canonical finite-lattice coordinate defining the defect center.
        core_radius
            Nonnegative minimum-image Chebyshev radius in lattice-cell units.
        exterior_frobenius_tolerance
            Maximum accepted perturbation norm wholly outside the core.
        core_exterior_frobenius_tolerance
            Maximum accepted perturbation norm coupling core and exterior.

        Returns
        -------
        Periodic2DDefectLocalityResult
            Partition-resolved residuals and an explicit finite-extent disposition.
        """
        return Periodic2DDefectLocalityAnalyzer().execute(
            Periodic2DDefectLocalityRequest(
                bulk_operator,
                defect_operator,
                origin,
                core_radius,
                exterior_frobenius_tolerance,
                core_exterior_frobenius_tolerance,
            )
        )
