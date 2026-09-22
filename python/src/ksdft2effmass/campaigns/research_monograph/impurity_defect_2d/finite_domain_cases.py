"""Execution-free case definitions for the defect-2D finite-domain campaign."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from ksdft2effmass.solid_state import (
    BoundaryTwistMesh,
    BoundaryTwistMeshEnumerator,
    BoundaryTwistRepresentative,
    FiniteLatticeShape,
    LatticeDimension,
)


class FiniteDomainChannel(StrEnum):
    """Nonpooled finite-domain analysis channels."""

    AREA = "area"
    SHAPE = "shape"
    ORIENTATION = "orientation"
    BOUNDARY_PHASE = "boundary_phase"


@dataclass(frozen=True, slots=True)
class FiniteDomainEffectsStudyDefinition:
    """Retain one execution-free finite-domain case-enumeration definition."""

    identifier: str
    area_shapes: tuple[FiniteLatticeShape, ...]
    shape_shapes: tuple[FiniteLatticeShape, ...]
    orientation_shape_pairs: tuple[tuple[FiniteLatticeShape, FiniteLatticeShape], ...]
    defect_identifiers: tuple[str, ...]
    twist_mesh: BoundaryTwistMesh
    isotropic_parent_identifier: str
    orientation_source_parent_identifier: str
    orientation_swapped_parent_identifier: str

    def __post_init__(self) -> None:
        """Validate exact 2D geometry, defect, mesh, and parent inventories."""
        for value, name in (
            (self.identifier, "identifier"),
            (self.isotropic_parent_identifier, "isotropic_parent_identifier"),
            (
                self.orientation_source_parent_identifier,
                "orientation_source_parent_identifier",
            ),
            (
                self.orientation_swapped_parent_identifier,
                "orientation_swapped_parent_identifier",
            ),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a string")
            if not value:
                raise ValueError(f"{name} must be nonempty")
        parent_identifiers = {
            self.isotropic_parent_identifier,
            self.orientation_source_parent_identifier,
            self.orientation_swapped_parent_identifier,
        }
        if len(parent_identifiers) != 3:
            raise ValueError("finite-domain parent identifiers must be distinct")
        for shapes, name in (
            (self.area_shapes, "area_shapes"),
            (self.shape_shapes, "shape_shapes"),
        ):
            if (
                type(shapes) is not tuple
                or not shapes
                or any(type(shape) is not FiniteLatticeShape for shape in shapes)
            ):
                raise TypeError(f"{name} must be a nonempty tuple of shapes")
            if any(shape.dimension is not LatticeDimension.TWO for shape in shapes):
                raise ValueError(f"{name} must contain only 2D shapes")
            if len(set(shapes)) != len(shapes):
                raise ValueError(f"{name} must contain unique shapes")
        if any(len(set(shape.extents)) != 1 for shape in self.area_shapes):
            raise ValueError("area-channel shapes must be square")
        area_measures = tuple(shape.cell_count for shape in self.area_shapes)
        if any(
            right <= left
            for left, right in zip(area_measures[:-1], area_measures[1:], strict=True)
        ):
            raise ValueError("area-channel measures must be strictly increasing")
        shape_measure = self.shape_shapes[0].cell_count
        if any(shape.cell_count != shape_measure for shape in self.shape_shapes):
            raise ValueError("shape-channel geometries must have fixed cell count")
        if (
            type(self.orientation_shape_pairs) is not tuple
            or not self.orientation_shape_pairs
        ):
            raise TypeError("orientation_shape_pairs must be a nonempty tuple")
        for pair in self.orientation_shape_pairs:
            if type(pair) is not tuple or len(pair) != 2:
                raise TypeError("orientation pairs must contain exactly two shapes")
            source, target = pair
            if (
                type(source) is not FiniteLatticeShape
                or type(target) is not FiniteLatticeShape
            ):
                raise TypeError("orientation pairs must contain finite shapes")
            if (
                source.dimension is not LatticeDimension.TWO
                or target.dimension is not LatticeDimension.TWO
            ):
                raise ValueError("orientation pairs must be two-dimensional")
            if target.extents != tuple(reversed(source.extents)):
                raise ValueError("orientation target must swap source extents")
            if source == target:
                raise ValueError("orientation source and target must be distinct")
        if len(set(self.orientation_shape_pairs)) != len(self.orientation_shape_pairs):
            raise ValueError("orientation shape pairs must be unique")
        if type(self.defect_identifiers) is not tuple or not self.defect_identifiers:
            raise TypeError("defect_identifiers must be a nonempty tuple")
        if any(
            type(value) is not str or not value for value in self.defect_identifiers
        ):
            raise TypeError("defect identifiers must be nonempty strings")
        if tuple(sorted(set(self.defect_identifiers))) != self.defect_identifiers:
            raise ValueError("defect identifiers must be sorted and unique")
        if type(self.twist_mesh) is not BoundaryTwistMesh:
            raise TypeError("twist_mesh must be BoundaryTwistMesh")
        if self.twist_mesh.dimension is not LatticeDimension.TWO:
            raise ValueError("finite-domain twist mesh must be two-dimensional")

    @property
    def isotropic_shapes(self) -> tuple[FiniteLatticeShape, ...]:
        """Return area shapes followed by previously unseen shape-channel geometries."""
        result = list(self.area_shapes)
        result.extend(shape for shape in self.shape_shapes if shape not in result)
        return tuple(result)


@dataclass(frozen=True, slots=True)
class IsotropicFiniteDomainCase:
    """Retain one shared isotropic operator-evaluation case and channel memberships."""

    identifier: str
    parent_identifier: str
    shape: FiniteLatticeShape
    defect_identifier: str
    twist_index: int
    twist: BoundaryTwistRepresentative
    channel_memberships: tuple[FiniteDomainChannel, ...]

    def __post_init__(self) -> None:
        """Validate exact case identity, 2D inputs, and nonpooled memberships."""
        for value, name in (
            (self.identifier, "identifier"),
            (self.parent_identifier, "parent_identifier"),
            (self.defect_identifier, "defect_identifier"),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a string")
            if not value:
                raise ValueError(f"{name} must be nonempty")
        if type(self.shape) is not FiniteLatticeShape:
            raise TypeError("shape must be FiniteLatticeShape")
        if self.shape.dimension is not LatticeDimension.TWO:
            raise ValueError("isotropic finite-domain cases must be two-dimensional")
        if type(self.twist_index) is not int or self.twist_index < 0:
            raise ValueError("twist_index must be a nonnegative built-in int")
        if type(self.twist) is not BoundaryTwistRepresentative:
            raise TypeError("twist must be BoundaryTwistRepresentative")
        if self.twist.dimension is not LatticeDimension.TWO:
            raise ValueError("isotropic case twist must be two-dimensional")
        if type(self.channel_memberships) is not tuple or any(
            type(channel) is not FiniteDomainChannel
            for channel in self.channel_memberships
        ):
            raise TypeError("channel_memberships must contain FiniteDomainChannel")
        if tuple(dict.fromkeys(self.channel_memberships)) != self.channel_memberships:
            raise ValueError("channel memberships must be ordered and unique")
        allowed = {
            FiniteDomainChannel.AREA,
            FiniteDomainChannel.SHAPE,
            FiniteDomainChannel.BOUNDARY_PHASE,
        }
        if set(self.channel_memberships) - allowed:
            raise ValueError("isotropic cases cannot belong to orientation")
        if FiniteDomainChannel.BOUNDARY_PHASE not in self.channel_memberships:
            raise ValueError(
                "every isotropic case must retain boundary-phase membership"
            )
        if not (
            FiniteDomainChannel.AREA in self.channel_memberships
            or FiniteDomainChannel.SHAPE in self.channel_memberships
        ):
            raise ValueError("isotropic case must belong to area or shape")


@dataclass(frozen=True, slots=True)
class OrientationFiniteDomainCase:
    """Retain one orientation comparison that requires three operator evaluations."""

    identifier: str
    source_parent_identifier: str
    swapped_parent_identifier: str
    source_shape: FiniteLatticeShape
    target_shape: FiniteLatticeShape
    defect_identifier: str
    twist_index: int
    source_twist: BoundaryTwistRepresentative
    target_twist: BoundaryTwistRepresentative

    def __post_init__(self) -> None:
        """Validate exact swapped geometry, twist, and parent identities."""
        for value, name in (
            (self.identifier, "identifier"),
            (self.source_parent_identifier, "source_parent_identifier"),
            (self.swapped_parent_identifier, "swapped_parent_identifier"),
            (self.defect_identifier, "defect_identifier"),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a string")
            if not value:
                raise ValueError(f"{name} must be nonempty")
        if self.source_parent_identifier == self.swapped_parent_identifier:
            raise ValueError("orientation source and swapped parents must differ")
        if (
            type(self.source_shape) is not FiniteLatticeShape
            or type(self.target_shape) is not FiniteLatticeShape
        ):
            raise TypeError("orientation shapes must be FiniteLatticeShape")
        if self.target_shape.extents != tuple(reversed(self.source_shape.extents)):
            raise ValueError("orientation target must swap source extents")
        if type(self.twist_index) is not int or self.twist_index < 0:
            raise ValueError("twist_index must be a nonnegative built-in int")
        if (
            type(self.source_twist) is not BoundaryTwistRepresentative
            or type(self.target_twist) is not BoundaryTwistRepresentative
        ):
            raise TypeError("orientation twists must be representatives")
        expected_target = tuple(reversed(self.source_twist.turns))
        if self.target_twist.turns != expected_target:
            raise ValueError("orientation target twist must swap source components")

    @property
    def operator_evaluation_count(self) -> int:
        """Return source, same-parent target, and swapped-parent target evaluations."""
        return 3


@dataclass(frozen=True, slots=True)
class FiniteDomainEffectsCaseInventory:
    """Retain separate isotropic evaluations and orientation comparison records."""

    definition: FiniteDomainEffectsStudyDefinition
    isotropic_cases: tuple[IsotropicFiniteDomainCase, ...]
    orientation_cases: tuple[OrientationFiniteDomainCase, ...]

    def __post_init__(self) -> None:
        """Validate types, unique identities, and definition-derived case counts."""
        if type(self.definition) is not FiniteDomainEffectsStudyDefinition:
            raise TypeError("definition must be FiniteDomainEffectsStudyDefinition")
        if type(self.isotropic_cases) is not tuple or any(
            type(case) is not IsotropicFiniteDomainCase for case in self.isotropic_cases
        ):
            raise TypeError("isotropic_cases must contain IsotropicFiniteDomainCase")
        if type(self.orientation_cases) is not tuple or any(
            type(case) is not OrientationFiniteDomainCase
            for case in self.orientation_cases
        ):
            raise TypeError(
                "orientation_cases must contain OrientationFiniteDomainCase"
            )
        identifiers = tuple(
            case.identifier for case in self.isotropic_cases + self.orientation_cases
        )
        if len(set(identifiers)) != len(identifiers):
            raise ValueError("finite-domain case identifiers must be unique")
        expected_isotropic = (
            len(self.definition.isotropic_shapes)
            * len(self.definition.defect_identifiers)
            * self.definition.twist_mesh.point_count
        )
        expected_orientation = (
            len(self.definition.orientation_shape_pairs)
            * len(self.definition.defect_identifiers)
            * self.definition.twist_mesh.point_count
        )
        if len(self.isotropic_cases) != expected_isotropic:
            raise ValueError("isotropic case count must match the study definition")
        if len(self.orientation_cases) != expected_orientation:
            raise ValueError("orientation case count must match the study definition")
        twists = BoundaryTwistMeshEnumerator().execute(self.definition.twist_mesh)
        isotropic_keys: set[tuple[FiniteLatticeShape, str, int]] = set()
        for isotropic_case in self.isotropic_cases:
            if (
                isotropic_case.parent_identifier
                != self.definition.isotropic_parent_identifier
            ):
                raise ValueError("isotropic case parent must match the definition")
            if isotropic_case.shape not in self.definition.isotropic_shapes:
                raise ValueError("isotropic case shape must occur in the definition")
            if (
                isotropic_case.defect_identifier
                not in self.definition.defect_identifiers
            ):
                raise ValueError("isotropic case defect must occur in the definition")
            if (
                isotropic_case.twist_index >= len(twists)
                or isotropic_case.twist != twists[isotropic_case.twist_index]
            ):
                raise ValueError("isotropic case twist must match its mesh index")
            expected_memberships: list[FiniteDomainChannel] = []
            if isotropic_case.shape in self.definition.area_shapes:
                expected_memberships.append(FiniteDomainChannel.AREA)
            if isotropic_case.shape in self.definition.shape_shapes:
                expected_memberships.append(FiniteDomainChannel.SHAPE)
            expected_memberships.append(FiniteDomainChannel.BOUNDARY_PHASE)
            if isotropic_case.channel_memberships != tuple(expected_memberships):
                raise ValueError(
                    "isotropic channel memberships must match the definition"
                )
            isotropic_key = (
                isotropic_case.shape,
                isotropic_case.defect_identifier,
                isotropic_case.twist_index,
            )
            if isotropic_key in isotropic_keys:
                raise ValueError("isotropic structural cases must be unique")
            isotropic_keys.add(isotropic_key)
        orientation_keys: set[
            tuple[FiniteLatticeShape, FiniteLatticeShape, str, int]
        ] = set()
        for orientation_case in self.orientation_cases:
            if (
                orientation_case.source_parent_identifier
                != self.definition.orientation_source_parent_identifier
                or orientation_case.swapped_parent_identifier
                != self.definition.orientation_swapped_parent_identifier
            ):
                raise ValueError("orientation case parents must match the definition")
            pair = (orientation_case.source_shape, orientation_case.target_shape)
            if pair not in self.definition.orientation_shape_pairs:
                raise ValueError("orientation shape pair must occur in the definition")
            if (
                orientation_case.defect_identifier
                not in self.definition.defect_identifiers
            ):
                raise ValueError("orientation defect must occur in the definition")
            if (
                orientation_case.twist_index >= len(twists)
                or orientation_case.source_twist != twists[orientation_case.twist_index]
            ):
                raise ValueError("orientation source twist must match its mesh index")
            orientation_key = (
                orientation_case.source_shape,
                orientation_case.target_shape,
                orientation_case.defect_identifier,
                orientation_case.twist_index,
            )
            if orientation_key in orientation_keys:
                raise ValueError("orientation structural cases must be unique")
            orientation_keys.add(orientation_key)

    @property
    def operator_evaluation_count(self) -> int:
        """Return unique isotropic plus three-per-orientation evaluations."""
        return len(self.isotropic_cases) + 3 * len(self.orientation_cases)


class FiniteDomainEffectsCaseEnumerator:
    """Enumerate one execution-free finite-domain inventory deterministically."""

    __slots__ = ()

    def execute(
        self, definition: FiniteDomainEffectsStudyDefinition
    ) -> FiniteDomainEffectsCaseInventory:
        """Return shared isotropic cases followed by orientation comparisons."""
        if type(definition) is not FiniteDomainEffectsStudyDefinition:
            raise TypeError("definition must be FiniteDomainEffectsStudyDefinition")
        twists = BoundaryTwistMeshEnumerator().execute(definition.twist_mesh)
        isotropic_cases: list[IsotropicFiniteDomainCase] = []
        for shape in definition.isotropic_shapes:
            shape_label = "x".join(str(value) for value in shape.extents)
            memberships: list[FiniteDomainChannel] = []
            if shape in definition.area_shapes:
                memberships.append(FiniteDomainChannel.AREA)
            if shape in definition.shape_shapes:
                memberships.append(FiniteDomainChannel.SHAPE)
            memberships.append(FiniteDomainChannel.BOUNDARY_PHASE)
            for defect_identifier in definition.defect_identifiers:
                for twist_index, twist in enumerate(twists):
                    isotropic_cases.append(
                        IsotropicFiniteDomainCase(
                            identifier=(
                                f"isotropic.{shape_label}.{defect_identifier}."
                                f"twist-{twist_index:03d}"
                            ),
                            parent_identifier=definition.isotropic_parent_identifier,
                            shape=shape,
                            defect_identifier=defect_identifier,
                            twist_index=twist_index,
                            twist=twist,
                            channel_memberships=tuple(memberships),
                        )
                    )
        orientation_cases: list[OrientationFiniteDomainCase] = []
        for source_shape, target_shape in definition.orientation_shape_pairs:
            source_label = "x".join(str(value) for value in source_shape.extents)
            target_label = "x".join(str(value) for value in target_shape.extents)
            for defect_identifier in definition.defect_identifiers:
                for twist_index, source_twist in enumerate(twists):
                    source_turns = source_twist.turns
                    if len(source_turns) != 2:
                        raise AssertionError("two-dimensional twist mesh was lost")
                    target_twist = BoundaryTwistRepresentative(
                        LatticeDimension.TWO,
                        (source_turns[-1], source_turns[0]),
                    )
                    orientation_cases.append(
                        OrientationFiniteDomainCase(
                            identifier=(
                                f"orientation.{source_label}-to-{target_label}."
                                f"{defect_identifier}.twist-{twist_index:03d}"
                            ),
                            source_parent_identifier=(
                                definition.orientation_source_parent_identifier
                            ),
                            swapped_parent_identifier=(
                                definition.orientation_swapped_parent_identifier
                            ),
                            source_shape=source_shape,
                            target_shape=target_shape,
                            defect_identifier=defect_identifier,
                            twist_index=twist_index,
                            source_twist=source_twist,
                            target_twist=target_twist,
                        )
                    )
        return FiniteDomainEffectsCaseInventory(
            definition, tuple(isotropic_cases), tuple(orientation_cases)
        )
