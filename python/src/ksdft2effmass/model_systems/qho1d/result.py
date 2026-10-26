"""Typed result aggregates for direct QHO1D calculations."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self, cast

import numpy as np
from projectkoios.physkit.units import (
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from .case_sections import (
    Qho1dHamiltonianComparisonResult,
    Qho1dResidualResult,
    Qho1dSampledStateAlignmentResult,
    Qho1dSpatialRepresentationResult,
)
from .configuration import Qho1dConfiguration


def _require_unitless(
    value: ScalarQuantity | VectorQuantity | MatrixQuantity, name: str
) -> None:
    if not isinstance(value.unit, Unitless):
        raise ValueError(f"{name} must use Unitless")


def _decoded_quantity[QuantityT: (ScalarQuantity, VectorQuantity, MatrixQuantity)](
    values: Mapping[str, SerializableValue],
    name: str,
    quantity_type: type[QuantityT],
) -> QuantityT:
    value = values[name]
    if not isinstance(value, quantity_type):
        raise TypeError(f"{name} must decode to {quantity_type.__name__}")
    return value


@dataclass(frozen=True, slots=True, eq=False)
class Qho1dCaseResult(BaseTypedRecord):
    """Retain one common-coordinate QHO1D comparison.

    Parameters
    ----------
    representation
        Finite spatial representation and its authored controls.
    alignment
        Sampled-state coordinate alignment and map diagnostics.
    hamiltonian_comparison
        Hamiltonians and discrepancy values in common retained coordinates.
    residual
        Full-space intertwining residual diagnostic.

    Raises
    ------
    TypeError
        A scalar, dimension, or quantity has the wrong semantic type.
    ValueError
        Units, shapes, positivity, ordering, or the signed-difference invariant fails.
    """

    representation: Qho1dSpatialRepresentationResult
    alignment: Qho1dSampledStateAlignmentResult
    hamiltonian_comparison: Qho1dHamiltonianComparisonResult
    residual: Qho1dResidualResult
    _wire_layout: str = "nested"

    def __post_init__(self) -> None:
        section_types = (
            ("representation", Qho1dSpatialRepresentationResult),
            ("alignment", Qho1dSampledStateAlignmentResult),
            ("hamiltonian_comparison", Qho1dHamiltonianComparisonResult),
            ("residual", Qho1dResidualResult),
        )
        for name, expected_type in section_types:
            if not isinstance(getattr(self, name), expected_type):
                raise TypeError(f"{name} must be {expected_type.__name__}")
        if self._wire_layout not in {"flat", "nested"}:
            raise ValueError("_wire_layout must be flat or nested")
        for name in (
            "box_half_width",
            "requested_grid_spacing",
            "grid_spacing",
            "grid_coordinates",
            "injection",
            "gram_matrix",
            "gram_inverse_square_root",
            "pulled_back_hamiltonian",
            "reference_hamiltonian",
            "difference",
            "gram_deviation",
            "gram_condition_number",
            "injection_isometry_error",
            "absolute_discrepancy",
            "relative_discrepancy",
            "diagonal_discrepancy",
            "off_diagonal_discrepancy",
            "residual_frobenius",
        ):
            _require_unitless(getattr(self, name), name)

        retained = self.representation.retained_dimension
        points = self.representation.interior_points
        shapes = {
            "injection": (points, retained),
            "gram_matrix": (retained, retained),
            "gram_inverse_square_root": (retained, retained),
            "pulled_back_hamiltonian": (retained, retained),
            "reference_hamiltonian": (retained, retained),
            "difference": (retained, retained),
        }
        for name, shape in shapes.items():
            if name in {
                "injection",
                "gram_matrix",
                "gram_inverse_square_root",
            }:
                value = getattr(self.alignment, name)
            else:
                value = getattr(self.hamiltonian_comparison, name)
            if value.magnitude.shape != shape:
                raise ValueError(f"{name} shape does not match the declared spaces")

    @property
    def key(self) -> tuple[float, float, int]:
        """Return the authored sweep key for this case.

        Returns
        -------
        tuple[float, float, int]
            Box half-width, requested grid spacing, and retained dimension.
        """
        return (
            self.box_half_width.magnitude,
            self.requested_grid_spacing.magnitude,
            self.retained_dimension,
        )

    @property
    def box_half_width(self) -> ScalarQuantity:
        """Return the finite-domain half-width."""
        return self.representation.box_half_width

    @property
    def requested_grid_spacing(self) -> ScalarQuantity:
        """Return the authored grid-spacing control."""
        return self.representation.requested_grid_spacing

    @property
    def grid_spacing(self) -> ScalarQuantity:
        """Return the realized grid spacing."""
        return self.representation.grid_spacing

    @property
    def retained_dimension(self) -> int:
        """Return the retained number-state dimension."""
        return self.representation.retained_dimension

    @property
    def interior_points(self) -> int:
        """Return the finite spatial dimension."""
        return self.representation.interior_points

    @property
    def grid_coordinates(self) -> VectorQuantity:
        """Return the ordered interior grid coordinates."""
        return self.representation.grid_coordinates

    @property
    def injection(self) -> MatrixQuantity:
        """Return the retained-to-spatial coordinate injection."""
        return self.alignment.injection

    @property
    def gram_matrix(self) -> MatrixQuantity:
        """Return the sampled-state Gram matrix."""
        return self.alignment.gram_matrix

    @property
    def gram_inverse_square_root(self) -> MatrixQuantity:
        """Return the symmetric Gram inverse square root."""
        return self.alignment.gram_inverse_square_root

    @property
    def gram_deviation(self) -> ScalarQuantity:
        """Return the sampled-state Gram deviation."""
        return self.alignment.gram_deviation

    @property
    def gram_condition_number(self) -> ScalarQuantity:
        """Return the sampled-state Gram condition number."""
        return self.alignment.gram_condition_number

    @property
    def injection_isometry_error(self) -> ScalarQuantity:
        """Return the injection-isometry discrepancy."""
        return self.alignment.injection_isometry_error

    @property
    def pulled_back_hamiltonian(self) -> MatrixQuantity:
        """Return the finite Hamiltonian in retained coordinates."""
        return self.hamiltonian_comparison.pulled_back_hamiltonian

    @property
    def reference_hamiltonian(self) -> MatrixQuantity:
        """Return the exact retained number-state Hamiltonian."""
        return self.hamiltonian_comparison.reference_hamiltonian

    @property
    def difference(self) -> MatrixQuantity:
        """Return pullback minus reference in common coordinates."""
        return self.hamiltonian_comparison.difference

    @property
    def absolute_discrepancy(self) -> ScalarQuantity:
        """Return the absolute Hamiltonian discrepancy."""
        return self.hamiltonian_comparison.absolute_discrepancy

    @property
    def relative_discrepancy(self) -> ScalarQuantity:
        """Return the reference-normalized Hamiltonian discrepancy."""
        return self.hamiltonian_comparison.relative_discrepancy

    @property
    def diagonal_discrepancy(self) -> ScalarQuantity:
        """Return the diagonal discrepancy component."""
        return self.hamiltonian_comparison.diagonal_discrepancy

    @property
    def off_diagonal_discrepancy(self) -> ScalarQuantity:
        """Return the off-diagonal discrepancy component."""
        return self.hamiltonian_comparison.off_diagonal_discrepancy

    @property
    def residual_frobenius(self) -> ScalarQuantity:
        """Return the full-space intertwining residual norm."""
        return self.residual.frobenius

    def _flat_mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "box_half_width": self.box_half_width,
            "requested_grid_spacing": self.requested_grid_spacing,
            "grid_spacing": self.grid_spacing,
            "retained_dimension": self.retained_dimension,
            "interior_points": self.interior_points,
            "grid_coordinates": self.grid_coordinates,
            "injection": self.injection,
            "gram_matrix": self.gram_matrix,
            "gram_inverse_square_root": self.gram_inverse_square_root,
            "pulled_back_hamiltonian": self.pulled_back_hamiltonian,
            "reference_hamiltonian": self.reference_hamiltonian,
            "difference": self.difference,
            "gram_deviation": self.gram_deviation,
            "gram_condition_number": self.gram_condition_number,
            "injection_isometry_error": self.injection_isometry_error,
            "absolute_discrepancy": self.absolute_discrepancy,
            "relative_discrepancy": self.relative_discrepancy,
            "diagonal_discrepancy": self.diagonal_discrepancy,
            "off_diagonal_discrepancy": self.off_diagonal_discrepancy,
            "residual_frobenius": self.residual_frobenius,
        }

    def _mapping(self) -> Mapping[str, SerializableValue]:
        if self._wire_layout == "flat":
            return self._flat_mapping()
        return {
            "representation": self.representation,
            "alignment": self.alignment,
            "hamiltonian_comparison": self.hamiltonian_comparison,
            "residual": self.residual,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        nested_fields = {
            "representation",
            "alignment",
            "hamiltonian_comparison",
            "residual",
        }
        if set(values) == nested_fields:
            representation_value = values["representation"]
            alignment_value = values["alignment"]
            hamiltonian_value = values["hamiltonian_comparison"]
            residual_value = values["residual"]
            if not isinstance(representation_value, Mapping):
                raise TypeError("representation must decode to a mapping")
            if not isinstance(alignment_value, Mapping):
                raise TypeError("alignment must decode to a mapping")
            if not isinstance(hamiltonian_value, Mapping):
                raise TypeError("hamiltonian_comparison must decode to a mapping")
            if not isinstance(residual_value, Mapping):
                raise TypeError("residual must decode to a mapping")
            return cls(
                representation=Qho1dSpatialRepresentationResult.from_dict(
                    representation_value
                ),
                alignment=Qho1dSampledStateAlignmentResult.from_dict(alignment_value),
                hamiltonian_comparison=Qho1dHamiltonianComparisonResult.from_dict(
                    hamiltonian_value
                ),
                residual=Qho1dResidualResult.from_dict(residual_value),
            )

        flat_fields = set(cls._flat_field_names())
        if set(values) != flat_fields:
            raise ValueError("QHO1D case fields do not match")
        retained_dimension = values["retained_dimension"]
        interior_points = values["interior_points"]
        if type(retained_dimension) is not int or type(interior_points) is not int:
            raise TypeError("QHO1D case dimensions must decode to built-in ints")
        return cls(
            representation=Qho1dSpatialRepresentationResult(
                box_half_width=_decoded_quantity(
                    values, "box_half_width", ScalarQuantity
                ),
                requested_grid_spacing=_decoded_quantity(
                    values, "requested_grid_spacing", ScalarQuantity
                ),
                grid_spacing=_decoded_quantity(values, "grid_spacing", ScalarQuantity),
                retained_dimension=retained_dimension,
                interior_points=interior_points,
                grid_coordinates=_decoded_quantity(
                    values, "grid_coordinates", VectorQuantity
                ),
            ),
            alignment=Qho1dSampledStateAlignmentResult(
                injection=_decoded_quantity(values, "injection", MatrixQuantity),
                gram_matrix=_decoded_quantity(values, "gram_matrix", MatrixQuantity),
                gram_inverse_square_root=_decoded_quantity(
                    values, "gram_inverse_square_root", MatrixQuantity
                ),
                gram_deviation=_decoded_quantity(
                    values, "gram_deviation", ScalarQuantity
                ),
                gram_condition_number=_decoded_quantity(
                    values, "gram_condition_number", ScalarQuantity
                ),
                injection_isometry_error=_decoded_quantity(
                    values, "injection_isometry_error", ScalarQuantity
                ),
            ),
            hamiltonian_comparison=Qho1dHamiltonianComparisonResult(
                pulled_back_hamiltonian=_decoded_quantity(
                    values, "pulled_back_hamiltonian", MatrixQuantity
                ),
                reference_hamiltonian=_decoded_quantity(
                    values, "reference_hamiltonian", MatrixQuantity
                ),
                difference=_decoded_quantity(values, "difference", MatrixQuantity),
                absolute_discrepancy=_decoded_quantity(
                    values, "absolute_discrepancy", ScalarQuantity
                ),
                relative_discrepancy=_decoded_quantity(
                    values, "relative_discrepancy", ScalarQuantity
                ),
                diagonal_discrepancy=_decoded_quantity(
                    values, "diagonal_discrepancy", ScalarQuantity
                ),
                off_diagonal_discrepancy=_decoded_quantity(
                    values, "off_diagonal_discrepancy", ScalarQuantity
                ),
            ),
            residual=Qho1dResidualResult(
                frobenius=_decoded_quantity(
                    values, "residual_frobenius", ScalarQuantity
                )
            ),
            _wire_layout="flat",
        )

    @staticmethod
    def _flat_field_names() -> tuple[str, ...]:
        return (
            "box_half_width",
            "requested_grid_spacing",
            "grid_spacing",
            "retained_dimension",
            "interior_points",
            "grid_coordinates",
            "injection",
            "gram_matrix",
            "gram_inverse_square_root",
            "pulled_back_hamiltonian",
            "reference_hamiltonian",
            "difference",
            "gram_deviation",
            "gram_condition_number",
            "injection_isometry_error",
            "absolute_discrepancy",
            "relative_discrepancy",
            "diagonal_discrepancy",
            "off_diagonal_discrepancy",
            "residual_frobenius",
        )


@dataclass(frozen=True, slots=True, eq=False)
class Qho1dStateComparisonResult(BaseTypedRecord):
    """Retain state-resolved values for the selected sweep case.

    Parameters
    ----------
    box_half_width, grid_spacing
        Selected realized finite-domain controls.
    retained_dimension, displayed_states
        Selected retained dimension and displayed prefix length.
    coordinates
        Ordered interior finite-grid coordinates.
    analytical_wavefunctions, finite_wavefunctions
        Column-ordered analytical and sign-aligned finite eigenstates.
    analytical_energies, finite_energies
        Corresponding retained spectra.

    Raises
    ------
    TypeError
        A field has the wrong semantic type.
    ValueError
        Units, shapes, positivity, or displayed-state bounds are invalid.
    """

    box_half_width: ScalarQuantity
    grid_spacing: ScalarQuantity
    retained_dimension: int
    displayed_states: int
    coordinates: VectorQuantity
    analytical_wavefunctions: MatrixQuantity
    finite_wavefunctions: MatrixQuantity
    analytical_energies: VectorQuantity
    finite_energies: VectorQuantity

    def __post_init__(self) -> None:
        for name in ("box_half_width", "grid_spacing"):
            value = getattr(self, name)
            if not isinstance(value, ScalarQuantity):
                raise TypeError(f"{name} must be ScalarQuantity")
            _require_unitless(value, name)
            if value.magnitude <= 0.0:
                raise ValueError(f"{name} must be positive")
        for name in ("retained_dimension", "displayed_states"):
            value = getattr(self, name)
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in int")
            if value <= 0:
                raise ValueError(f"{name} must be positive")
        if self.displayed_states > self.retained_dimension:
            raise ValueError("displayed_states exceeds retained_dimension")
        if not isinstance(self.coordinates, VectorQuantity):
            raise TypeError("coordinates must be VectorQuantity")
        _require_unitless(self.coordinates, "coordinates")
        points = self.coordinates.magnitude.size
        if points < self.retained_dimension or not np.all(
            np.diff(self.coordinates.magnitude) > 0.0
        ):
            raise ValueError("coordinates do not define the selected finite space")
        for name in ("analytical_wavefunctions", "finite_wavefunctions"):
            value = getattr(self, name)
            if not isinstance(value, MatrixQuantity):
                raise TypeError(f"{name} must be MatrixQuantity")
            _require_unitless(value, name)
            if value.magnitude.shape != (points, self.retained_dimension):
                raise ValueError(f"{name} shape does not match selected spaces")
        for name in ("analytical_energies", "finite_energies"):
            value = getattr(self, name)
            if not isinstance(value, VectorQuantity):
                raise TypeError(f"{name} must be VectorQuantity")
            _require_unitless(value, name)
            if value.magnitude.shape != (self.retained_dimension,):
                raise ValueError(f"{name} shape does not match retained_dimension")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {name: getattr(self, name) for name in self.__dataclass_fields__}

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != set(cls.__dataclass_fields__):
            raise ValueError("QHO1D state-comparison fields do not match")
        retained_dimension = values["retained_dimension"]
        displayed_states = values["displayed_states"]
        if type(retained_dimension) is not int or type(displayed_states) is not int:
            raise TypeError("state-comparison dimensions must decode to ints")
        return cls(
            box_half_width=_decoded_quantity(values, "box_half_width", ScalarQuantity),
            grid_spacing=_decoded_quantity(values, "grid_spacing", ScalarQuantity),
            retained_dimension=retained_dimension,
            displayed_states=displayed_states,
            coordinates=_decoded_quantity(values, "coordinates", VectorQuantity),
            analytical_wavefunctions=_decoded_quantity(
                values, "analytical_wavefunctions", MatrixQuantity
            ),
            finite_wavefunctions=_decoded_quantity(
                values, "finite_wavefunctions", MatrixQuantity
            ),
            analytical_energies=_decoded_quantity(
                values, "analytical_energies", VectorQuantity
            ),
            finite_energies=_decoded_quantity(
                values, "finite_energies", VectorQuantity
            ),
        )


@dataclass(frozen=True, slots=True, eq=False)
class Qho1dCalculationResult(BaseTypedRecord):
    """Compose one complete direct QHO1D calculation result.

    Parameters
    ----------
    calculation_family, execution_id, evidence_status, claim_boundary
        Stable family identity, concrete execution identity, status, and bounded claim.
    configuration
        Exact authored direct-calculation configuration.
    cases
        Ordered Cartesian product of every declared sweep control.
    selected_state_comparison
        State-resolved values for the declared selected case.

    Raises
    ------
    TypeError
        Metadata, configuration, or result collections have the wrong type.
    ValueError
        Metadata is empty or cases do not equal the configured ordered sweep.
    """

    calculation_family: str
    execution_id: str
    evidence_status: str
    claim_boundary: str
    configuration: Qho1dConfiguration
    cases: tuple[Qho1dCaseResult, ...]
    selected_state_comparison: Qho1dStateComparisonResult

    def __post_init__(self) -> None:
        for name in (
            "calculation_family",
            "execution_id",
            "evidence_status",
            "claim_boundary",
        ):
            value = getattr(self, name)
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in string")
            if not value:
                raise ValueError(f"{name} must be nonempty")
        if not isinstance(self.configuration, Qho1dConfiguration):
            raise TypeError("configuration must be Qho1dConfiguration")
        if not isinstance(self.cases, tuple) or any(
            not isinstance(case, Qho1dCaseResult) for case in self.cases
        ):
            raise TypeError("cases must be a tuple of Qho1dCaseResult")
        expected = tuple(
            (box, spacing, retained)
            for box in self.configuration.box_half_widths
            for spacing in self.configuration.grid_spacings
            for retained in self.configuration.retained_dimensions
        )
        if tuple(case.key for case in self.cases) != expected:
            raise ValueError("cases must equal the configured ordered sweep")
        if not isinstance(self.selected_state_comparison, Qho1dStateComparisonResult):
            raise TypeError(
                "selected_state_comparison must be Qho1dStateComparisonResult"
            )
        selected = self.selected_state_comparison
        if (
            selected.box_half_width.magnitude
            != self.configuration.selected_box_half_width
            or selected.retained_dimension
            != self.configuration.selected_retained_dimension
            or selected.displayed_states != self.configuration.displayed_states
        ):
            raise ValueError("selected state comparison differs from configuration")
        selected_case = tuple(
            case
            for case in self.cases
            if case.key
            == (
                self.configuration.selected_box_half_width,
                self.configuration.selected_grid_spacing,
                self.configuration.selected_retained_dimension,
            )
        )
        if len(selected_case) != 1:
            raise ValueError("selected configuration must identify one comparison case")
        if selected.grid_spacing != selected_case[0].grid_spacing:
            raise ValueError("selected state and comparison grid spacings differ")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "calculation_family": self.calculation_family,
            "execution_id": self.execution_id,
            "evidence_status": self.evidence_status,
            "claim_boundary": self.claim_boundary,
            "configuration": self.configuration,
            "cases": self.cases,
            "selected_state_comparison": self.selected_state_comparison,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        fields = {
            "calculation_family",
            "execution_id",
            "evidence_status",
            "claim_boundary",
            "configuration",
            "cases",
            "selected_state_comparison",
        }
        if set(values) != fields:
            raise ValueError("QHO1D calculation-result fields do not match")
        metadata = tuple(
            values[name]
            for name in (
                "calculation_family",
                "execution_id",
                "evidence_status",
                "claim_boundary",
            )
        )
        if any(type(value) is not str for value in metadata):
            raise TypeError("QHO1D result metadata must decode to strings")
        configuration_value = values["configuration"]
        cases_value = values["cases"]
        state_value = values["selected_state_comparison"]
        if not isinstance(configuration_value, Mapping):
            raise TypeError("configuration must decode to a mapping")
        if not isinstance(cases_value, tuple) or any(
            not isinstance(case, Mapping) for case in cases_value
        ):
            raise TypeError("cases must decode to a tuple of mappings")
        if not isinstance(state_value, Mapping):
            raise TypeError("selected_state_comparison must decode to a mapping")
        return cls(
            calculation_family=cast(str, metadata[0]),
            execution_id=cast(str, metadata[1]),
            evidence_status=cast(str, metadata[2]),
            claim_boundary=cast(str, metadata[3]),
            configuration=Qho1dConfiguration.from_dict(configuration_value),
            cases=tuple(Qho1dCaseResult.from_dict(case) for case in cases_value),
            selected_state_comparison=Qho1dStateComparisonResult.from_dict(state_value),
        )
