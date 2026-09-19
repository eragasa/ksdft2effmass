"""Version-one JSON serialization for execution-free finite-domain inventories."""

from __future__ import annotations

import hashlib
import json
from typing import cast

from ksdft2effmass.solid_state import (
    BoundaryTwistMesh,
    FiniteLatticeShape,
    LatticeDimension,
)

from .finite_domain_cases import (
    FiniteDomainChannel,
    FiniteDomainEffectsCaseEnumerator,
    FiniteDomainEffectsCaseInventory,
    FiniteDomainEffectsStudyDefinition,
)

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type JsonObject = dict[str, JsonValue]


class FiniteDomainEffectsCaseInventoryJsonSerializer:
    """Round-trip one deterministic execution-free inventory as canonical JSON."""

    __slots__ = ()

    def serialize(self, inventory: FiniteDomainEffectsCaseInventory) -> bytes:
        """Return sorted, newline-terminated version-one UTF-8 JSON bytes."""
        if type(inventory) is not FiniteDomainEffectsCaseInventory:
            raise TypeError("inventory must be FiniteDomainEffectsCaseInventory")
        payload: JsonObject = {
            "schema_version": 1,
            "record_type": "finite_domain_effects_case_inventory",
            "execution_status": "not_executed",
            "channels": [channel.value for channel in FiniteDomainChannel],
            "definition": self.definition_payload(inventory.definition),
            "inventory_summary": {
                "isotropic_case_count": len(inventory.isotropic_cases),
                "orientation_case_count": len(inventory.orientation_cases),
                "operator_evaluation_count": inventory.operator_evaluation_count,
                "content_sha256": self.inventory_sha256(inventory),
            },
        }
        return (
            json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
        ).encode("utf-8")

    def deserialize(self, payload: bytes) -> FiniteDomainEffectsCaseInventory:
        """Parse, reconstruct, and authenticate one version-one inventory."""
        if type(payload) is not bytes:
            raise TypeError("payload must be bytes")
        try:
            decoded: object = json.loads(
                payload.decode("utf-8"), object_pairs_hook=self.object_pairs
            )
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError("payload must be valid UTF-8 JSON") from error
        root = self.require_object(self.normalize(decoded), "payload")
        self.require_keys(
            root,
            {
                "schema_version",
                "record_type",
                "execution_status",
                "channels",
                "definition",
                "inventory_summary",
            },
            "payload",
        )
        if self.require_int(root["schema_version"], "schema_version") != 1:
            raise ValueError("schema_version must equal 1")
        if (
            self.require_string(root["record_type"], "record_type")
            != "finite_domain_effects_case_inventory"
        ):
            raise ValueError("record_type is not supported")
        if (
            self.require_string(root["execution_status"], "execution_status")
            != "not_executed"
        ):
            raise ValueError("execution_status must equal not_executed")
        channels = self.require_list(root["channels"], "channels")
        expected_channels = [channel.value for channel in FiniteDomainChannel]
        if [
            self.require_string(value, "channel") for value in channels
        ] != expected_channels:
            raise ValueError("channels must retain the exact nonpooled channel order")
        definition = self.definition_from_payload(
            self.require_object(root["definition"], "definition")
        )
        inventory = FiniteDomainEffectsCaseEnumerator().execute(definition)
        summary = self.require_object(root["inventory_summary"], "inventory_summary")
        self.require_keys(
            summary,
            {
                "isotropic_case_count",
                "orientation_case_count",
                "operator_evaluation_count",
                "content_sha256",
            },
            "inventory_summary",
        )
        expected_counts = (
            len(inventory.isotropic_cases),
            len(inventory.orientation_cases),
            inventory.operator_evaluation_count,
        )
        retained_counts = (
            self.require_int(summary["isotropic_case_count"], "isotropic_case_count"),
            self.require_int(
                summary["orientation_case_count"], "orientation_case_count"
            ),
            self.require_int(
                summary["operator_evaluation_count"], "operator_evaluation_count"
            ),
        )
        if retained_counts != expected_counts:
            raise ValueError(
                "inventory counts do not match the reconstructed definition"
            )
        retained_sha256 = self.require_string(
            summary["content_sha256"], "content_sha256"
        )
        if retained_sha256 != self.inventory_sha256(inventory):
            raise ValueError("inventory content SHA-256 does not match reconstruction")
        return inventory

    @staticmethod
    def definition_payload(
        definition: FiniteDomainEffectsStudyDefinition,
    ) -> JsonObject:
        """Represent one study definition in the version-one wire contract."""
        return {
            "identifier": definition.identifier,
            "area_shapes": [list(shape.extents) for shape in definition.area_shapes],
            "shape_shapes": [list(shape.extents) for shape in definition.shape_shapes],
            "orientation_shape_pairs": [
                [list(source.extents), list(target.extents)]
                for source, target in definition.orientation_shape_pairs
            ],
            "defect_identifiers": list(definition.defect_identifiers),
            "twist_mesh_counts": list(definition.twist_mesh.counts),
            "isotropic_parent_identifier": definition.isotropic_parent_identifier,
            "orientation_source_parent_identifier": (
                definition.orientation_source_parent_identifier
            ),
            "orientation_swapped_parent_identifier": (
                definition.orientation_swapped_parent_identifier
            ),
            "spatial_dimension": 2,
            "ordering": "last_axis_fastest",
        }

    def definition_from_payload(
        self, payload: JsonObject
    ) -> FiniteDomainEffectsStudyDefinition:
        """Decode one exact version-one finite-domain definition."""
        self.require_keys(
            payload,
            {
                "identifier",
                "area_shapes",
                "shape_shapes",
                "orientation_shape_pairs",
                "defect_identifiers",
                "twist_mesh_counts",
                "isotropic_parent_identifier",
                "orientation_source_parent_identifier",
                "orientation_swapped_parent_identifier",
                "spatial_dimension",
                "ordering",
            },
            "definition",
        )
        if self.require_int(payload["spatial_dimension"], "spatial_dimension") != 2:
            raise ValueError("spatial_dimension must equal 2")
        if self.require_string(payload["ordering"], "ordering") != "last_axis_fastest":
            raise ValueError("ordering must equal last_axis_fastest")
        area_shapes = self.shapes(payload["area_shapes"], "area_shapes")
        shape_shapes = self.shapes(payload["shape_shapes"], "shape_shapes")
        orientation_values = self.require_list(
            payload["orientation_shape_pairs"], "orientation_shape_pairs"
        )
        orientation_pairs: list[tuple[FiniteLatticeShape, FiniteLatticeShape]] = []
        for index, value in enumerate(orientation_values):
            pair = self.require_list(value, f"orientation_shape_pairs[{index}]")
            if len(pair) != 2:
                raise ValueError("orientation shape pairs must contain two shapes")
            orientation_pairs.append(
                (
                    self.shape(pair[0], f"orientation_shape_pairs[{index}][0]"),
                    self.shape(pair[1], f"orientation_shape_pairs[{index}][1]"),
                )
            )
        defects = self.require_list(payload["defect_identifiers"], "defect_identifiers")
        defect_identifiers = tuple(
            self.require_string(value, f"defect_identifiers[{index}]")
            for index, value in enumerate(defects)
        )
        mesh_counts = self.require_list(
            payload["twist_mesh_counts"], "twist_mesh_counts"
        )
        if len(mesh_counts) != 2:
            raise ValueError("twist_mesh_counts must contain two values")
        counts = (
            self.require_int(mesh_counts[0], "twist_mesh_counts[0]"),
            self.require_int(mesh_counts[1], "twist_mesh_counts[1]"),
        )
        return FiniteDomainEffectsStudyDefinition(
            identifier=self.require_string(payload["identifier"], "identifier"),
            area_shapes=area_shapes,
            shape_shapes=shape_shapes,
            orientation_shape_pairs=tuple(orientation_pairs),
            defect_identifiers=defect_identifiers,
            twist_mesh=BoundaryTwistMesh(LatticeDimension.TWO, counts),
            isotropic_parent_identifier=self.require_string(
                payload["isotropic_parent_identifier"], "isotropic_parent_identifier"
            ),
            orientation_source_parent_identifier=self.require_string(
                payload["orientation_source_parent_identifier"],
                "orientation_source_parent_identifier",
            ),
            orientation_swapped_parent_identifier=self.require_string(
                payload["orientation_swapped_parent_identifier"],
                "orientation_swapped_parent_identifier",
            ),
        )

    def shapes(self, value: JsonValue, name: str) -> tuple[FiniteLatticeShape, ...]:
        """Decode a list of two-dimensional finite shapes."""
        values = self.require_list(value, name)
        return tuple(
            self.shape(item, f"{name}[{index}]") for index, item in enumerate(values)
        )

    def shape(self, value: JsonValue, name: str) -> FiniteLatticeShape:
        """Decode one two-dimensional finite shape."""
        extents = self.require_list(value, name)
        if len(extents) != 2:
            raise ValueError(f"{name} must contain two extents")
        return FiniteLatticeShape(
            LatticeDimension.TWO,
            (
                self.require_int(extents[0], f"{name}[0]"),
                self.require_int(extents[1], f"{name}[1]"),
            ),
        )

    @staticmethod
    def inventory_sha256(inventory: FiniteDomainEffectsCaseInventory) -> str:
        """Hash the complete deterministic case content as canonical JSON."""
        cases: list[JsonValue] = []
        for isotropic_case in inventory.isotropic_cases:
            cases.append(
                {
                    "kind": "isotropic",
                    "identifier": isotropic_case.identifier,
                    "parent_identifier": isotropic_case.parent_identifier,
                    "shape": list(isotropic_case.shape.extents),
                    "defect_identifier": isotropic_case.defect_identifier,
                    "twist_index": isotropic_case.twist_index,
                    "twist_turns": list(isotropic_case.twist.turns),
                    "channel_memberships": [
                        channel.value for channel in isotropic_case.channel_memberships
                    ],
                }
            )
        for orientation_case in inventory.orientation_cases:
            cases.append(
                {
                    "kind": "orientation",
                    "identifier": orientation_case.identifier,
                    "source_parent_identifier": (
                        orientation_case.source_parent_identifier
                    ),
                    "swapped_parent_identifier": (
                        orientation_case.swapped_parent_identifier
                    ),
                    "source_shape": list(orientation_case.source_shape.extents),
                    "target_shape": list(orientation_case.target_shape.extents),
                    "defect_identifier": orientation_case.defect_identifier,
                    "twist_index": orientation_case.twist_index,
                    "source_twist_turns": list(orientation_case.source_twist.turns),
                    "target_twist_turns": list(orientation_case.target_twist.turns),
                    "operator_evaluation_count": (
                        orientation_case.operator_evaluation_count
                    ),
                }
            )
        encoded = json.dumps(
            cases, sort_keys=True, separators=(",", ":"), allow_nan=False
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    @classmethod
    def normalize(cls, value: object) -> JsonValue:
        """Convert decoded JSON into the closed recursive wire representation."""
        if value is None or type(value) in {bool, int, float, str}:
            return cast(None | bool | int | float | str, value)
        if type(value) is list:
            return [cls.normalize(item) for item in value]
        if type(value) is tuple:
            result: JsonObject = {}
            for member in value:
                if type(member) is not tuple or len(member) != 2:
                    raise ValueError("decoded JSON object member is invalid")
                key, item = member
                if type(key) is not str:
                    raise ValueError("JSON object names must be strings")
                if key in result:
                    raise ValueError(f"duplicate JSON object name: {key}")
                result[key] = cls.normalize(item)
            return result
        raise ValueError("payload contains an unsupported JSON value")

    @staticmethod
    def object_pairs(
        pairs: list[tuple[str, object]],
    ) -> tuple[tuple[str, object], ...]:
        """Preserve JSON object pairs so duplicate names can be rejected."""
        return tuple(pairs)

    @staticmethod
    def require_object(value: JsonValue, name: str) -> JsonObject:
        """Require one JSON object."""
        if type(value) is not dict:
            raise ValueError(f"{name} must be an object")
        return value

    @staticmethod
    def require_list(value: JsonValue, name: str) -> list[JsonValue]:
        """Require one JSON array."""
        if type(value) is not list:
            raise ValueError(f"{name} must be an array")
        return value

    @staticmethod
    def require_string(value: JsonValue, name: str) -> str:
        """Require one JSON string."""
        if type(value) is not str or not value:
            raise ValueError(f"{name} must be a nonempty string")
        return value

    @staticmethod
    def require_int(value: JsonValue, name: str) -> int:
        """Require one JSON integer without admitting booleans."""
        if type(value) is not int:
            raise ValueError(f"{name} must be an integer")
        return value

    @staticmethod
    def require_keys(value: JsonObject, expected: set[str], name: str) -> None:
        """Require one exact versioned object key set."""
        if set(value) != expected:
            raise ValueError(f"{name} fields do not match schema version 1")
