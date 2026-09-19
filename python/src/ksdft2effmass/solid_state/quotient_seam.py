r"""Independent sparse quotient-seam construction for scalar lattice operators."""

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
    LatticeDimension,
    LatticeDisplacement,
    LatticeIntegerComponents,
)
from .lattice_models import (
    LocalizedBondTerm,
    LocalizedOnsiteTerm,
    LocalizedPerturbation,
    ScalarHoppingModel,
    SolidStateUnit,
)
from .represented_operators import ScalarFiniteLatticeOperator


class QuotientSeamOperatorConstructor:
    r"""Construct scalar hopping and localized operators directly in seam gauge.

    This ActionObject does not call uniform-link construction or a gauge bridge. For a
    directed term, it independently resolves source and target periodic images and uses

    .. math::

       \exp\!\left(2\pi i\sum_a(q_{t,a}-q_{s,a})\phi_a\right),

    where ``q_s`` and ``q_t`` are their quotient-image integers.
    """

    __slots__ = ()

    @staticmethod
    def _coordinate(components: tuple[int, ...]) -> LatticeIntegerComponents:
        """Close validated one-, two-, or three-dimensional integer components."""
        if len(components) == 1:
            return (components[0],)
        if len(components) == 2:
            return (components[0], components[1])
        if len(components) == 3:
            return (components[0], components[1], components[2])
        raise AssertionError("supported lattice dimension was lost")

    @classmethod
    def _image(
        cls, shape: FiniteLatticeShape, coordinate: LatticeCoordinate
    ) -> tuple[LatticeCoordinate, LatticeDisplacement]:
        """Resolve one periodic image directly through Euclidean integer division."""
        quotients: list[int] = []
        remainders: list[int] = []
        for component, extent in zip(coordinate.components, shape.extents, strict=True):
            quotient, remainder = divmod(component, extent)
            quotients.append(quotient)
            remainders.append(remainder)
        return (
            LatticeCoordinate(shape.dimension, cls._coordinate(tuple(remainders))),
            LatticeDisplacement(shape.dimension, cls._coordinate(tuple(quotients))),
        )

    def execute_hopping(
        self,
        identifier: str,
        model: ScalarHoppingModel,
        shape: FiniteLatticeShape,
        twist: BoundaryTwistLift,
    ) -> ScalarFiniteLatticeOperator:
        """Return a translation-invariant scalar hopping operator in seam gauge."""
        if type(model) is not ScalarHoppingModel:
            raise TypeError("model must be ScalarHoppingModel")
        self._validate_inputs(identifier, model.dimension, shape, twist)
        coordinate_resolver = FiniteLatticeCoordinateResolver()
        indexer = FiniteLatticeIndexer()
        rows: list[int] = []
        columns: list[int] = []
        values: list[complex] = []
        for row in range(shape.cell_count):
            source = coordinate_resolver.execute(shape, row)
            for term in model.terms:
                raw_target = tuple(
                    source.components[axis] + term.displacement.components[axis]
                    for axis in range(shape.dimension.value)
                )
                target, target_quotient = self._image(
                    shape,
                    LatticeCoordinate(shape.dimension, self._coordinate(raw_target)),
                )
                phase_turns = math.fsum(
                    float(target_quotient.components[axis]) * twist.turns[axis]
                    for axis in range(shape.dimension.value)
                )
                rows.append(row)
                columns.append(indexer.execute(shape, target))
                values.append(term.value * cmath.exp(2.0j * math.pi * phase_turns))
        return self._represented(
            identifier,
            rows,
            columns,
            values,
            shape,
            twist,
            model.energy_unit,
            model.basis_identifier,
            model.energy_reference,
            ("source_model", model.identifier),
        )

    def execute_perturbation(
        self,
        identifier: str,
        perturbation: LocalizedPerturbation,
        shape: FiniteLatticeShape,
        twist: BoundaryTwistLift,
    ) -> ScalarFiniteLatticeOperator:
        """Return a localized scalar perturbation directly in seam gauge."""
        if type(perturbation) is not LocalizedPerturbation:
            raise TypeError("perturbation must be LocalizedPerturbation")
        self._validate_inputs(identifier, perturbation.dimension, shape, twist)
        indexer = FiniteLatticeIndexer()
        rows: list[int] = []
        columns: list[int] = []
        values: list[complex] = []
        for term in perturbation.terms:
            if type(term) is LocalizedOnsiteTerm:
                site, _ = self._image(shape, term.site)
                index = indexer.execute(shape, site)
                rows.append(index)
                columns.append(index)
                values.append(term.value)
            elif type(term) is LocalizedBondTerm:
                source, source_quotient = self._image(shape, term.start)
                raw_target = tuple(
                    term.start.components[axis] + term.displacement.components[axis]
                    for axis in range(shape.dimension.value)
                )
                target, target_quotient = self._image(
                    shape,
                    LatticeCoordinate(shape.dimension, self._coordinate(raw_target)),
                )
                phase_turns = math.fsum(
                    float(
                        target_quotient.components[axis]
                        - source_quotient.components[axis]
                    )
                    * twist.turns[axis]
                    for axis in range(shape.dimension.value)
                )
                rows.append(indexer.execute(shape, source))
                columns.append(indexer.execute(shape, target))
                values.append(term.value * cmath.exp(2.0j * math.pi * phase_turns))
            else:
                raise AssertionError("validated localized term type was lost")
        return self._represented(
            identifier,
            rows,
            columns,
            values,
            shape,
            twist,
            perturbation.energy_unit,
            perturbation.basis_identifier,
            perturbation.energy_reference,
            ("source_perturbation", perturbation.identifier),
        )

    @staticmethod
    def _validate_inputs(
        identifier: str,
        dimension: LatticeDimension,
        shape: FiniteLatticeShape,
        twist: BoundaryTwistLift,
    ) -> None:
        """Validate shared exact construction inputs."""
        if type(identifier) is not str:
            raise TypeError("identifier must be a string")
        if not identifier:
            raise ValueError("identifier must be nonempty")
        if type(shape) is not FiniteLatticeShape:
            raise TypeError("shape must be FiniteLatticeShape")
        if type(twist) is not BoundaryTwistLift:
            raise TypeError("twist must be BoundaryTwistLift")
        if dimension is not shape.dimension:
            raise ValueError("source and finite-lattice dimensions must agree")
        if twist.dimension is not shape.dimension:
            raise ValueError("twist and finite-lattice dimensions must agree")

    @staticmethod
    def _represented(
        identifier: str,
        rows: list[int],
        columns: list[int],
        values: list[complex],
        shape: FiniteLatticeShape,
        twist: BoundaryTwistLift,
        energy_unit: SolidStateUnit,
        basis_identifier: str,
        energy_reference: str,
        source_provenance: tuple[str, str],
    ) -> ScalarFiniteLatticeOperator:
        """Assemble canonical sparse storage and correlated seam metadata."""
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
        matrix = ComplexSparseMatrixQuantity.from_csr(assembled, energy_unit)
        fiber = TwistFiber(
            BoundaryTwistReducer().execute(twist),
            TwistGaugeRepresentation.QUOTIENT_SEAM,
        )
        return ScalarFiniteLatticeOperator(
            identifier,
            matrix,
            shape,
            fiber,
            basis_identifier,
            energy_reference,
            (("constructor", "QuotientSeamOperatorConstructor"), source_provenance),
        )
