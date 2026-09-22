"""Sparse centered-uniform-link construction for scalar finite lattice models."""

from __future__ import annotations

import cmath
import math

import numpy as np
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.operators import ComplexSparseMatrixQuantity

from .boundary_phases import (
    BoundaryTwistLift,
    BoundaryTwistReducer,
    TwistFiber,
    TwistGaugeRepresentation,
)
from .geometry import (
    FiniteLatticeCoordinateResolver,
    FiniteLatticeIndexer,
    FiniteLatticeShape,
    LatticeCoordinate,
    LatticeIntegerComponents,
    PeriodicImageResolver,
)
from .lattice_models import (
    LocalizedBondTerm,
    LocalizedOnsiteTerm,
    LocalizedPerturbation,
    ScalarHoppingModel,
)
from .represented_operators import ScalarFiniteLatticeOperator


class TwistedSupercellOperatorConstructor:
    r"""Construct a sparse scalar parent operator in centered uniform-link gauge.

    For each source cell ``r`` and hopping displacement ``R``, the represented row is
    ``r``, the column is ``r + R`` reduced periodically, and the matrix contribution is

    .. math::

       h_R\exp\!\left(2\pi i\sum_a \phi_a R_a/N_a\right),

    where ``phi`` is the unreduced twist lift and ``N`` is the finite shape. Assembly
    uses sparse COO accumulation followed by canonical complex128 CSR conversion. It
    never materializes a dense matrix.

    This ActionObject constructs only the translation-invariant scalar parent. A
    localized perturbation constructor, quotient-seam verifier, and gauge bridge are
    separate owners.
    """

    __slots__ = ()

    def execute(
        self,
        identifier: str,
        model: ScalarHoppingModel,
        shape: FiniteLatticeShape,
        twist: BoundaryTwistLift,
    ) -> ScalarFiniteLatticeOperator:
        """Return one represented sparse parent operator.

        Parameters
        ----------
        identifier
            Nonempty represented-operator identity.
        model
            Canonical scalar hopping inventory.
        shape
            Finite periodic shape with matching dimension.
        twist
            Unreduced boundary-twist lift with matching dimension.
        """
        if type(identifier) is not str:
            raise TypeError("identifier must be a string")
        if not identifier:
            raise ValueError("identifier must be nonempty")
        if type(model) is not ScalarHoppingModel:
            raise TypeError("model must be ScalarHoppingModel")
        if type(shape) is not FiniteLatticeShape:
            raise TypeError("shape must be FiniteLatticeShape")
        if type(twist) is not BoundaryTwistLift:
            raise TypeError("twist must be BoundaryTwistLift")
        if model.dimension is not shape.dimension:
            raise ValueError("model and finite-lattice dimensions must agree")
        if twist.dimension is not shape.dimension:
            raise ValueError("twist and finite-lattice dimensions must agree")

        indexer = FiniteLatticeIndexer()
        coordinate_resolver = FiniteLatticeCoordinateResolver()
        periodic_resolver = PeriodicImageResolver()
        rows: list[int] = []
        columns: list[int] = []
        values: list[complex] = []
        for row in range(shape.cell_count):
            source = coordinate_resolver.execute(shape, row)
            for term in model.terms:
                target_components = tuple(
                    source.components[axis] + term.displacement.components[axis]
                    for axis in range(shape.dimension.value)
                )
                closed_target: LatticeIntegerComponents
                if shape.dimension.value == 1:
                    closed_target = (target_components[0],)
                elif shape.dimension.value == 2:
                    closed_target = (target_components[0], target_components[1])
                else:
                    closed_target = (
                        target_components[0],
                        target_components[1],
                        target_components[2],
                    )
                target = LatticeCoordinate(shape.dimension, closed_target)
                periodic_target = periodic_resolver.execute(shape, target).coordinate
                column = indexer.execute(shape, periodic_target)
                phase_turns = math.fsum(
                    twist.turns[axis]
                    * float(term.displacement.components[axis])
                    / float(shape.extents[axis])
                    for axis in range(shape.dimension.value)
                )
                rows.append(row)
                columns.append(column)
                values.append(term.value * cmath.exp(2.0j * math.pi * phase_turns))
        assembled = sparse.coo_array(
            (
                np.asarray(values, dtype=np.complex128),
                (
                    np.asarray(rows, dtype=np.int64),
                    np.asarray(columns, dtype=np.int64),
                ),
            ),
            shape=(shape.cell_count, shape.cell_count),
            dtype=np.complex128,
        )
        matrix = ComplexSparseMatrixQuantity.from_csr(assembled, model.energy_unit)
        reduction = BoundaryTwistReducer().execute(twist)
        fiber = TwistFiber(reduction, TwistGaugeRepresentation.CENTERED_UNIFORM_LINK)
        provenance = (
            ("constructor", type(self).__name__),
            ("source_model", model.identifier),
        )
        return ScalarFiniteLatticeOperator(
            identifier,
            matrix,
            shape,
            fiber,
            model.basis_identifier,
            model.energy_reference,
            provenance,
        )


class LocalizedPerturbationOperatorConstructor:
    r"""Construct a sparse localized perturbation in centered uniform-link gauge.

    Onsite terms contribute directly to one wrapped site. Each directed bond from
    ``r`` through displacement ``R`` contributes

    .. math::

       v_{r,R}\exp\!\left(2\pi i\sum_a \phi_a R_a/N_a\right)

    to the wrapped row ``r`` and column ``r + R``. Reverse bonds are never invented;
    a Hermitian perturbation inventory must declare them explicitly.
    """

    __slots__ = ()

    def execute(
        self,
        identifier: str,
        perturbation: LocalizedPerturbation,
        shape: FiniteLatticeShape,
        twist: BoundaryTwistLift,
    ) -> ScalarFiniteLatticeOperator:
        """Return one represented sparse localized perturbation."""
        if type(identifier) is not str:
            raise TypeError("identifier must be a string")
        if not identifier:
            raise ValueError("identifier must be nonempty")
        if type(perturbation) is not LocalizedPerturbation:
            raise TypeError("perturbation must be LocalizedPerturbation")
        if type(shape) is not FiniteLatticeShape:
            raise TypeError("shape must be FiniteLatticeShape")
        if type(twist) is not BoundaryTwistLift:
            raise TypeError("twist must be BoundaryTwistLift")
        if perturbation.dimension is not shape.dimension:
            raise ValueError("perturbation and finite-lattice dimensions must agree")
        if twist.dimension is not shape.dimension:
            raise ValueError("twist and finite-lattice dimensions must agree")

        indexer = FiniteLatticeIndexer()
        periodic_resolver = PeriodicImageResolver()
        rows: list[int] = []
        columns: list[int] = []
        values: list[complex] = []
        for term in perturbation.terms:
            if type(term) is LocalizedOnsiteTerm:
                site = periodic_resolver.execute(shape, term.site).coordinate
                index = indexer.execute(shape, site)
                rows.append(index)
                columns.append(index)
                values.append(term.value)
            elif type(term) is LocalizedBondTerm:
                source = periodic_resolver.execute(shape, term.start).coordinate
                target_components = tuple(
                    term.start.components[axis] + term.displacement.components[axis]
                    for axis in range(shape.dimension.value)
                )
                closed_target: LatticeIntegerComponents
                if shape.dimension.value == 1:
                    closed_target = (target_components[0],)
                elif shape.dimension.value == 2:
                    closed_target = (target_components[0], target_components[1])
                else:
                    closed_target = (
                        target_components[0],
                        target_components[1],
                        target_components[2],
                    )
                target = periodic_resolver.execute(
                    shape, LatticeCoordinate(shape.dimension, closed_target)
                ).coordinate
                phase_turns = math.fsum(
                    twist.turns[axis]
                    * float(term.displacement.components[axis])
                    / float(shape.extents[axis])
                    for axis in range(shape.dimension.value)
                )
                rows.append(indexer.execute(shape, source))
                columns.append(indexer.execute(shape, target))
                values.append(term.value * cmath.exp(2.0j * math.pi * phase_turns))
            else:
                raise AssertionError("validated localized term type was lost")
        assembled = sparse.coo_array(
            (
                np.asarray(values, dtype=np.complex128),
                (
                    np.asarray(rows, dtype=np.int64),
                    np.asarray(columns, dtype=np.int64),
                ),
            ),
            shape=(shape.cell_count, shape.cell_count),
            dtype=np.complex128,
        )
        matrix = ComplexSparseMatrixQuantity.from_csr(
            assembled, perturbation.energy_unit
        )
        fiber = TwistFiber(
            BoundaryTwistReducer().execute(twist),
            TwistGaugeRepresentation.CENTERED_UNIFORM_LINK,
        )
        provenance = (
            ("constructor", type(self).__name__),
            ("source_perturbation", perturbation.identifier),
        )
        return ScalarFiniteLatticeOperator(
            identifier,
            matrix,
            shape,
            fiber,
            perturbation.basis_identifier,
            perturbation.energy_reference,
            provenance,
        )
