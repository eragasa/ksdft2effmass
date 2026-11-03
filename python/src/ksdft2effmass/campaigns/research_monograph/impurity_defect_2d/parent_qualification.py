"""Typed contracts for periodic-2D rank-defect parent qualification.

The qualification binds three historical scalar synthetic parents to the maintained
solid-state construction interfaces and the complete execution-free finite-domain
shape/twist inventory. It establishes represented numerical capability only. It does
not establish material validation, defect isolation, convergence, uncertainty
quantification, or authority to execute the defect campaign.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from projectkoios.physkit.units import Unitless

from ksdft2effmass.solidstate import (
    BoundaryTwistMesh,
    FiniteLatticeShape,
    LatticeDimension,
    LocalizedPerturbation,
    ScalarHoppingModel,
)


@dataclass(frozen=True, slots=True)
class ParentQualificationSourceIdentity:
    """Bind one historical source role to an exact path and SHA-256 identity."""

    role: str
    path: str
    sha256: str

    def __post_init__(self) -> None:
        """Validate nonempty identity fields and lowercase SHA-256 spelling."""
        for value, name in (
            (self.role, "role"),
            (self.path, "path"),
            (self.sha256, "sha256"),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a string")
            if not value:
                raise ValueError(f"{name} must be nonempty")
        if len(self.sha256) != 64 or any(
            character not in "0123456789abcdef" for character in self.sha256
        ):
            raise ValueError("sha256 must be 64 lowercase hexadecimal characters")


@dataclass(frozen=True, slots=True)
class ParentQualificationTolerances:
    """Retain prospective criteria for parent capability qualification."""

    hopping_hermiticity_absolute: float
    hopping_symmetry_absolute: float
    represented_hermiticity_absolute: float
    gauge_bridge_absolute: float
    reconstruction_absolute: float
    separability_absolute: float

    def __post_init__(self) -> None:
        """Require finite nonnegative built-in-float criteria."""
        for value, name in (
            (self.hopping_hermiticity_absolute, "hopping_hermiticity_absolute"),
            (self.hopping_symmetry_absolute, "hopping_symmetry_absolute"),
            (self.represented_hermiticity_absolute, "represented_hermiticity_absolute"),
            (self.gauge_bridge_absolute, "gauge_bridge_absolute"),
            (self.reconstruction_absolute, "reconstruction_absolute"),
            (self.separability_absolute, "separability_absolute"),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")


@dataclass(frozen=True, slots=True)
class ParentQualificationResourceEnvelope:
    """Retain the bounded local resource contract for qualification."""

    maximum_matrix_dimension: int
    maximum_parent_route_evaluations: int
    maximum_defect_route_evaluations: int
    maximum_runtime_seconds: int
    maximum_peak_memory_gib: float
    maximum_retained_output_mib: float
    network_access: bool
    external_executables: tuple[str, ...]
    new_dependencies: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate exact positive bounds and local-execution declarations."""
        for integer_value, name in (
            (self.maximum_matrix_dimension, "maximum_matrix_dimension"),
            (
                self.maximum_parent_route_evaluations,
                "maximum_parent_route_evaluations",
            ),
            (
                self.maximum_defect_route_evaluations,
                "maximum_defect_route_evaluations",
            ),
            (self.maximum_runtime_seconds, "maximum_runtime_seconds"),
        ):
            if type(integer_value) is not int:
                raise TypeError(f"{name} must be a built-in integer")
            if integer_value <= 0:
                raise ValueError(f"{name} must be positive")
        for float_value, name in (
            (self.maximum_peak_memory_gib, "maximum_peak_memory_gib"),
            (self.maximum_retained_output_mib, "maximum_retained_output_mib"),
        ):
            if type(float_value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(float_value) or float_value <= 0.0:
                raise ValueError(f"{name} must be finite and positive")
        if type(self.network_access) is not bool:
            raise TypeError("network_access must be a built-in bool")
        for values, name in (
            (self.external_executables, "external_executables"),
            (self.new_dependencies, "new_dependencies"),
        ):
            if type(values) is not tuple or any(
                type(value) is not str or not value for value in values
            ):
                raise TypeError(f"{name} must contain nonempty strings")


@dataclass(frozen=True, slots=True)
class ParentQualificationDefinition:
    """Retain one complete accepted-evidence parent qualification request."""

    identifier: str
    source_revision: str
    sources: tuple[ParentQualificationSourceIdentity, ...]
    isotropic_parent: ScalarHoppingModel
    isotropic_pretruncation_parent: ScalarHoppingModel
    anisotropic_lambda_x: float
    anisotropic_lambda_y: float
    anisotropic_lambda_xy: float
    plane_wave_cutoff: int
    reciprocal_mesh_size: int
    hopping_maximum_squared_radius: int
    expected_parent_digests: tuple[tuple[str, str], ...]
    shapes: tuple[FiniteLatticeShape, ...]
    twist_mesh: BoundaryTwistMesh
    perturbations: tuple[LocalizedPerturbation, ...]
    tolerances: ParentQualificationTolerances
    resource_envelope: ParentQualificationResourceEnvelope
    claim_boundary: str

    def __post_init__(self) -> None:
        """Validate identities, represented meaning, inventories, and bounds."""
        for string_value, name in (
            (self.identifier, "identifier"),
            (self.source_revision, "source_revision"),
            (self.claim_boundary, "claim_boundary"),
        ):
            if type(string_value) is not str:
                raise TypeError(f"{name} must be a string")
            if not string_value:
                raise ValueError(f"{name} must be nonempty")
        if len(self.source_revision) != 40 or any(
            character not in "0123456789abcdef" for character in self.source_revision
        ):
            raise ValueError("source_revision must be a 40-character Git identity")
        if (
            type(self.sources) is not tuple
            or not self.sources
            or any(
                type(value) is not ParentQualificationSourceIdentity
                for value in self.sources
            )
        ):
            raise TypeError("sources must contain ParentQualificationSourceIdentity")
        source_roles = tuple(value.role for value in self.sources)
        if source_roles != tuple(sorted(set(source_roles))):
            raise ValueError("source roles must be sorted and unique")
        if type(self.isotropic_parent) is not ScalarHoppingModel:
            raise TypeError("isotropic_parent must be ScalarHoppingModel")
        if type(self.isotropic_pretruncation_parent) is not ScalarHoppingModel:
            raise TypeError("isotropic_pretruncation_parent must be ScalarHoppingModel")
        for parent in (self.isotropic_parent, self.isotropic_pretruncation_parent):
            if parent.dimension is not LatticeDimension.TWO:
                raise ValueError("isotropic parents must be two-dimensional")
            if type(parent.energy_unit) is not Unitless:
                raise ValueError("qualified synthetic parents must use Unitless energy")
            if parent.basis_identifier != self.isotropic_parent.basis_identifier:
                raise ValueError("isotropic parent basis identities must agree")
            if parent.energy_reference != self.isotropic_parent.energy_reference:
                raise ValueError("isotropic parent energy references must agree")
        for float_value, name in (
            (self.anisotropic_lambda_x, "anisotropic_lambda_x"),
            (self.anisotropic_lambda_y, "anisotropic_lambda_y"),
            (self.anisotropic_lambda_xy, "anisotropic_lambda_xy"),
        ):
            if type(float_value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(float_value):
                raise ValueError(f"{name} must be finite")
        if self.anisotropic_lambda_xy != 0.0:
            raise ValueError("version-one anisotropic parent must remain separable")
        for integer_value, name in (
            (self.plane_wave_cutoff, "plane_wave_cutoff"),
            (self.reciprocal_mesh_size, "reciprocal_mesh_size"),
            (
                self.hopping_maximum_squared_radius,
                "hopping_maximum_squared_radius",
            ),
        ):
            if type(integer_value) is not int:
                raise TypeError(f"{name} must be a built-in integer")
            if integer_value <= 0:
                raise ValueError(f"{name} must be positive")
        if self.reciprocal_mesh_size % 2 == 0:
            raise ValueError("reciprocal_mesh_size must be odd")
        if type(self.expected_parent_digests) is not tuple or any(
            type(value) is not tuple
            or len(value) != 2
            or type(value[0]) is not str
            or not value[0]
            or type(value[1]) is not str
            or len(value[1]) != 64
            for value in self.expected_parent_digests
        ):
            raise TypeError("expected_parent_digests must contain identity pairs")
        parent_ids = tuple(value[0] for value in self.expected_parent_digests)
        if len(set(parent_ids)) != len(parent_ids):
            raise ValueError("expected parent identities must be unique")
        if (
            type(self.shapes) is not tuple
            or not self.shapes
            or any(type(value) is not FiniteLatticeShape for value in self.shapes)
        ):
            raise TypeError("shapes must contain FiniteLatticeShape values")
        if any(value.dimension is not LatticeDimension.TWO for value in self.shapes):
            raise ValueError("qualification shapes must be two-dimensional")
        shape_keys = tuple(value.extents for value in self.shapes)
        if len(set(shape_keys)) != len(shape_keys):
            raise ValueError("qualification shapes must be unique")
        if type(self.twist_mesh) is not BoundaryTwistMesh:
            raise TypeError("twist_mesh must be BoundaryTwistMesh")
        if self.twist_mesh.dimension is not LatticeDimension.TWO:
            raise ValueError("qualification twist mesh must be two-dimensional")
        if (
            type(self.perturbations) is not tuple
            or not self.perturbations
            or any(
                type(value) is not LocalizedPerturbation for value in self.perturbations
            )
        ):
            raise TypeError("perturbations must contain LocalizedPerturbation values")
        if any(
            value.dimension is not LatticeDimension.TWO for value in self.perturbations
        ):
            raise ValueError("qualified perturbations must be two-dimensional")
        perturbation_ids = tuple(value.identifier for value in self.perturbations)
        if len(set(perturbation_ids)) != len(perturbation_ids):
            raise ValueError("qualified perturbation identities must be unique")
        expected_unit = self.isotropic_parent.energy_unit
        expected_basis = self.isotropic_parent.basis_identifier
        expected_reference = self.isotropic_parent.energy_reference
        for perturbation in self.perturbations:
            if perturbation.energy_unit != expected_unit:
                raise ValueError("parent and perturbation energy units must agree")
            if perturbation.basis_identifier != expected_basis:
                raise ValueError("parent and perturbation basis identities must agree")
            if perturbation.energy_reference != expected_reference:
                raise ValueError("parent and perturbation energy references must agree")
        if type(self.tolerances) is not ParentQualificationTolerances:
            raise TypeError("tolerances must be ParentQualificationTolerances")
        if type(self.resource_envelope) is not ParentQualificationResourceEnvelope:
            raise TypeError(
                "resource_envelope must be ParentQualificationResourceEnvelope"
            )
        maximum_dimension = max(shape.cell_count for shape in self.shapes)
        parent_evaluations = (
            len(self.expected_parent_digests)
            * len(self.shapes)
            * self.twist_mesh.point_count
            * 2
        )
        defect_evaluations = (
            len(self.perturbations) * len(self.shapes) * self.twist_mesh.point_count * 2
        )
        if maximum_dimension > self.resource_envelope.maximum_matrix_dimension:
            raise ValueError("shape inventory exceeds the resource dimension bound")
        if parent_evaluations > self.resource_envelope.maximum_parent_route_evaluations:
            raise ValueError("parent inventory exceeds the route-evaluation bound")
        if defect_evaluations > self.resource_envelope.maximum_defect_route_evaluations:
            raise ValueError("defect inventory exceeds the route-evaluation bound")


@dataclass(frozen=True, slots=True)
class QualifiedParentMetrics:
    """Retain aggregate capability metrics for one exact parent inventory."""

    parent_identifier: str
    hopping_count: int
    hopping_digest: str
    hopping_hermiticity_maximum_absolute: float
    hopping_symmetry_maximum_absolute: float
    represented_hermiticity_maximum_absolute: float
    gauge_bridge_maximum_absolute: float
    route_evaluations: int
    inherited_truncation_maximum_absolute: float
    inherited_truncation_frobenius: float

    def __post_init__(self) -> None:
        """Validate exact identifiers, counts, and finite nonnegative metrics."""
        if type(self.parent_identifier) is not str or not self.parent_identifier:
            raise TypeError("parent_identifier must be a nonempty string")
        if type(self.hopping_count) is not int or self.hopping_count <= 0:
            raise TypeError("hopping_count must be a positive built-in integer")
        if type(self.hopping_digest) is not str or len(self.hopping_digest) != 64:
            raise TypeError("hopping_digest must be a SHA-256 string")
        if type(self.route_evaluations) is not int or self.route_evaluations <= 0:
            raise TypeError("route_evaluations must be a positive built-in integer")
        for value in (
            self.hopping_hermiticity_maximum_absolute,
            self.hopping_symmetry_maximum_absolute,
            self.represented_hermiticity_maximum_absolute,
            self.gauge_bridge_maximum_absolute,
            self.inherited_truncation_maximum_absolute,
            self.inherited_truncation_frobenius,
        ):
            if type(value) is not float:
                raise TypeError("parent metrics must be built-in floats")
            if not math.isfinite(value) or value < 0.0:
                raise ValueError("parent metrics must be finite and nonnegative")


@dataclass(frozen=True, slots=True)
class QualifiedPerturbationMetrics:
    """Retain aggregate represented metrics for one declared perturbation."""

    perturbation_identifier: str
    term_count: int
    represented_hermiticity_maximum_absolute: float
    gauge_bridge_maximum_absolute: float
    route_evaluations: int

    def __post_init__(self) -> None:
        """Validate exact identifiers, counts, and finite metrics."""
        if (
            type(self.perturbation_identifier) is not str
            or not self.perturbation_identifier
        ):
            raise TypeError("perturbation_identifier must be a nonempty string")
        if type(self.term_count) is not int or self.term_count <= 0:
            raise TypeError("term_count must be a positive built-in integer")
        if type(self.route_evaluations) is not int or self.route_evaluations <= 0:
            raise TypeError("route_evaluations must be a positive built-in integer")
        for value in (
            self.represented_hermiticity_maximum_absolute,
            self.gauge_bridge_maximum_absolute,
        ):
            if type(value) is not float:
                raise TypeError("perturbation metrics must be built-in floats")
            if not math.isfinite(value) or value < 0.0:
                raise ValueError("perturbation metrics must be finite and nonnegative")


@dataclass(frozen=True, slots=True)
class ParentQualificationResult:
    """Retain one complete parent qualification and every failed criterion name."""

    definition: ParentQualificationDefinition
    parents: tuple[QualifiedParentMetrics, ...]
    perturbations: tuple[QualifiedPerturbationMetrics, ...]
    maximum_plane_wave_separability_absolute: float
    failed_criteria: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate exact definition correlation and criterion disposition."""
        if type(self.definition) is not ParentQualificationDefinition:
            raise TypeError("definition must be ParentQualificationDefinition")
        if type(self.parents) is not tuple or any(
            type(value) is not QualifiedParentMetrics for value in self.parents
        ):
            raise TypeError("parents must contain QualifiedParentMetrics")
        expected_parent_ids = tuple(
            value[0] for value in self.definition.expected_parent_digests
        )
        if (
            tuple(value.parent_identifier for value in self.parents)
            != expected_parent_ids
        ):
            raise ValueError("qualified parents must match the definition order")
        if type(self.perturbations) is not tuple or any(
            type(value) is not QualifiedPerturbationMetrics
            for value in self.perturbations
        ):
            raise TypeError("perturbations must contain QualifiedPerturbationMetrics")
        expected_perturbations = tuple(
            value.identifier for value in self.definition.perturbations
        )
        if (
            tuple(value.perturbation_identifier for value in self.perturbations)
            != expected_perturbations
        ):
            raise ValueError("qualified perturbations must match the definition order")
        if type(self.maximum_plane_wave_separability_absolute) is not float:
            raise TypeError(
                "maximum_plane_wave_separability_absolute must be a built-in float"
            )
        if (
            not math.isfinite(self.maximum_plane_wave_separability_absolute)
            or self.maximum_plane_wave_separability_absolute < 0.0
        ):
            raise ValueError("plane-wave separability metric must be nonnegative")
        if type(self.failed_criteria) is not tuple or any(
            type(value) is not str or not value for value in self.failed_criteria
        ):
            raise TypeError("failed_criteria must contain nonempty strings")
        expected = ParentQualificationCriterionEvaluator().execute(
            self.definition,
            self.parents,
            self.perturbations,
            self.maximum_plane_wave_separability_absolute,
        )
        if self.failed_criteria != expected:
            raise ValueError("failed_criteria must match the retained metrics")

    @property
    def passes(self) -> bool:
        """Return whether every prospective parent qualification criterion passes."""
        return not self.failed_criteria


class ParentQualificationCriterionEvaluator:
    """Evaluate qualification criteria without discarding failed metrics."""

    __slots__ = ()

    def execute(
        self,
        definition: ParentQualificationDefinition,
        parents: tuple[QualifiedParentMetrics, ...],
        perturbations: tuple[QualifiedPerturbationMetrics, ...],
        maximum_plane_wave_separability_absolute: float,
    ) -> tuple[str, ...]:
        """Return ordered names of every failed exact or numerical criterion."""
        if type(definition) is not ParentQualificationDefinition:
            raise TypeError("definition must be ParentQualificationDefinition")
        tolerances = definition.tolerances
        expected_digests = dict(definition.expected_parent_digests)
        failures: list[str] = []
        for parent in parents:
            prefix = f"parent.{parent.parent_identifier}"
            if parent.hopping_digest != expected_digests[parent.parent_identifier]:
                failures.append(f"{prefix}.historical_digest")
            if (
                parent.hopping_hermiticity_maximum_absolute
                > tolerances.hopping_hermiticity_absolute
            ):
                failures.append(f"{prefix}.hopping_hermiticity")
            if (
                parent.hopping_symmetry_maximum_absolute
                > tolerances.hopping_symmetry_absolute
            ):
                failures.append(f"{prefix}.hopping_symmetry")
            if (
                parent.represented_hermiticity_maximum_absolute
                > tolerances.represented_hermiticity_absolute
            ):
                failures.append(f"{prefix}.represented_hermiticity")
            if parent.gauge_bridge_maximum_absolute > tolerances.gauge_bridge_absolute:
                failures.append(f"{prefix}.gauge_bridge")
        for perturbation in perturbations:
            prefix = f"perturbation.{perturbation.perturbation_identifier}"
            if (
                perturbation.represented_hermiticity_maximum_absolute
                > tolerances.represented_hermiticity_absolute
            ):
                failures.append(f"{prefix}.represented_hermiticity")
            if (
                perturbation.gauge_bridge_maximum_absolute
                > tolerances.gauge_bridge_absolute
            ):
                failures.append(f"{prefix}.gauge_bridge")
        if maximum_plane_wave_separability_absolute > tolerances.separability_absolute:
            failures.append("anisotropic_parent.plane_wave_separability")
        return tuple(failures)
