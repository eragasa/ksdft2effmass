"""Canonical JSON serialization for periodic-2D parent qualification."""

from __future__ import annotations

import json
from typing import cast

from projectkoios.physkit.units import Unitless

from ksdft2effmass.serialization import JsonCodec
from ksdft2effmass.solidstate import (
    BoundaryTwistMesh,
    FiniteLatticeShape,
    LatticeCoordinate,
    LatticeDimension,
    LatticeDisplacement,
    LocalizedBondTerm,
    LocalizedOnsiteTerm,
    LocalizedPerturbation,
    ScalarHoppingModel,
    ScalarHoppingTerm,
)

from .parent_qualification import (
    ParentQualificationDefinition,
    ParentQualificationResourceEnvelope,
    ParentQualificationResult,
    ParentQualificationSourceIdentity,
    ParentQualificationTolerances,
    QualifiedParentMetrics,
    QualifiedPerturbationMetrics,
)

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type JsonObject = dict[str, JsonValue]


class _ParentQualificationWire:
    """Own strict version-one parent-qualification wire mechanics."""

    __slots__ = ()

    @staticmethod
    def definition_payload(definition: ParentQualificationDefinition) -> JsonObject:
        """Return one complete parent qualification definition payload."""
        return {
            "identifier": definition.identifier,
            "source_revision": definition.source_revision,
            "sources": [
                {
                    "role": source.role,
                    "path": source.path,
                    "sha256": source.sha256,
                }
                for source in definition.sources
            ],
            "isotropic_parent": _ParentQualificationWire.model_payload(
                definition.isotropic_parent
            ),
            "isotropic_pretruncation_parent": (
                _ParentQualificationWire.model_payload(
                    definition.isotropic_pretruncation_parent
                )
            ),
            "anisotropic_parent": {
                "lambda_x": definition.anisotropic_lambda_x,
                "lambda_y": definition.anisotropic_lambda_y,
                "lambda_xy": definition.anisotropic_lambda_xy,
                "plane_wave_cutoff": definition.plane_wave_cutoff,
                "reciprocal_mesh_size": definition.reciprocal_mesh_size,
                "hopping_maximum_squared_radius": (
                    definition.hopping_maximum_squared_radius
                ),
            },
            "expected_parent_digests": [
                {"parent_identifier": identifier, "sha256": digest}
                for identifier, digest in definition.expected_parent_digests
            ],
            "shapes": [list(shape.extents) for shape in definition.shapes],
            "twist_mesh_counts": list(definition.twist_mesh.counts),
            "perturbations": [
                _ParentQualificationWire.perturbation_payload(perturbation)
                for perturbation in definition.perturbations
            ],
            "tolerances": {
                "hopping_hermiticity_absolute": (
                    definition.tolerances.hopping_hermiticity_absolute
                ),
                "hopping_symmetry_absolute": (
                    definition.tolerances.hopping_symmetry_absolute
                ),
                "represented_hermiticity_absolute": (
                    definition.tolerances.represented_hermiticity_absolute
                ),
                "gauge_bridge_absolute": (definition.tolerances.gauge_bridge_absolute),
                "reconstruction_absolute": (
                    definition.tolerances.reconstruction_absolute
                ),
                "separability_absolute": (definition.tolerances.separability_absolute),
            },
            "resource_envelope": {
                "maximum_matrix_dimension": (
                    definition.resource_envelope.maximum_matrix_dimension
                ),
                "maximum_parent_route_evaluations": (
                    definition.resource_envelope.maximum_parent_route_evaluations
                ),
                "maximum_defect_route_evaluations": (
                    definition.resource_envelope.maximum_defect_route_evaluations
                ),
                "maximum_runtime_seconds": (
                    definition.resource_envelope.maximum_runtime_seconds
                ),
                "maximum_peak_memory_gib": (
                    definition.resource_envelope.maximum_peak_memory_gib
                ),
                "maximum_retained_output_mib": (
                    definition.resource_envelope.maximum_retained_output_mib
                ),
                "network_access": definition.resource_envelope.network_access,
                "external_executables": list(
                    definition.resource_envelope.external_executables
                ),
                "new_dependencies": list(definition.resource_envelope.new_dependencies),
            },
            "claim_boundary": definition.claim_boundary,
        }

    @staticmethod
    def model_payload(model: ScalarHoppingModel) -> JsonObject:
        """Return one unitless scalar hopping model payload."""
        return {
            "identifier": model.identifier,
            "basis_identifier": model.basis_identifier,
            "energy_reference": model.energy_reference,
            "energy_unit": "unitless",
            "terms": [
                {
                    "displacement": list(term.displacement.components),
                    "real": term.real,
                    "imaginary": term.imaginary,
                }
                for term in model.terms
            ],
        }

    @staticmethod
    def perturbation_payload(perturbation: LocalizedPerturbation) -> JsonObject:
        """Return one unitless localized perturbation payload."""
        terms: list[JsonValue] = []
        for term in perturbation.terms:
            if type(term) is LocalizedOnsiteTerm:
                terms.append(
                    {
                        "kind": "onsite",
                        "site": list(term.site.components),
                        "real": term.real,
                        "imaginary": term.imaginary,
                    }
                )
            elif type(term) is LocalizedBondTerm:
                terms.append(
                    {
                        "kind": "bond",
                        "start": list(term.start.components),
                        "displacement": list(term.displacement.components),
                        "real": term.real,
                        "imaginary": term.imaginary,
                    }
                )
            else:
                raise AssertionError("validated localized term type was lost")
        return {
            "identifier": perturbation.identifier,
            "basis_identifier": perturbation.basis_identifier,
            "energy_reference": perturbation.energy_reference,
            "energy_unit": "unitless",
            "terms": terms,
        }

    @classmethod
    def definition_from_payload(
        cls, payload: JsonObject
    ) -> ParentQualificationDefinition:
        """Reconstruct one complete parent qualification definition."""
        cls.require_keys(
            payload,
            {
                "identifier",
                "source_revision",
                "sources",
                "isotropic_parent",
                "isotropic_pretruncation_parent",
                "anisotropic_parent",
                "expected_parent_digests",
                "shapes",
                "twist_mesh_counts",
                "perturbations",
                "tolerances",
                "resource_envelope",
                "claim_boundary",
            },
            "definition",
        )
        source_values = cls.require_list(payload["sources"], "sources")
        sources: list[ParentQualificationSourceIdentity] = []
        for index, value in enumerate(source_values):
            source = cls.require_object(value, f"sources[{index}]")
            cls.require_keys(source, {"role", "path", "sha256"}, f"sources[{index}]")
            sources.append(
                ParentQualificationSourceIdentity(
                    cls.require_string(source["role"], "source role"),
                    cls.require_string(source["path"], "source path"),
                    cls.require_string(source["sha256"], "source sha256"),
                )
            )
        anisotropic = cls.require_object(
            payload["anisotropic_parent"], "anisotropic_parent"
        )
        cls.require_keys(
            anisotropic,
            {
                "lambda_x",
                "lambda_y",
                "lambda_xy",
                "plane_wave_cutoff",
                "reciprocal_mesh_size",
                "hopping_maximum_squared_radius",
            },
            "anisotropic_parent",
        )
        digest_values = cls.require_list(
            payload["expected_parent_digests"], "expected_parent_digests"
        )
        digests: list[tuple[str, str]] = []
        for index, value in enumerate(digest_values):
            record = cls.require_object(value, f"expected_parent_digests[{index}]")
            cls.require_keys(
                record,
                {"parent_identifier", "sha256"},
                f"expected_parent_digests[{index}]",
            )
            digests.append(
                (
                    cls.require_string(
                        record["parent_identifier"], "parent_identifier"
                    ),
                    cls.require_string(record["sha256"], "sha256"),
                )
            )
        shape_values = cls.require_list(payload["shapes"], "shapes")
        shapes = tuple(
            FiniteLatticeShape(
                LatticeDimension.TWO,
                cls.integer_pair(value, f"shapes[{index}]"),
            )
            for index, value in enumerate(shape_values)
        )
        mesh_counts = cls.integer_pair(
            payload["twist_mesh_counts"], "twist_mesh_counts"
        )
        perturbation_values = cls.require_list(
            payload["perturbations"], "perturbations"
        )
        perturbations = tuple(
            cls.perturbation_from_payload(
                cls.require_object(value, f"perturbations[{index}]")
            )
            for index, value in enumerate(perturbation_values)
        )
        tolerances = cls.require_object(payload["tolerances"], "tolerances")
        cls.require_keys(
            tolerances,
            {
                "hopping_hermiticity_absolute",
                "hopping_symmetry_absolute",
                "represented_hermiticity_absolute",
                "gauge_bridge_absolute",
                "reconstruction_absolute",
                "separability_absolute",
            },
            "tolerances",
        )
        resources = cls.require_object(
            payload["resource_envelope"], "resource_envelope"
        )
        cls.require_keys(
            resources,
            {
                "maximum_matrix_dimension",
                "maximum_parent_route_evaluations",
                "maximum_defect_route_evaluations",
                "maximum_runtime_seconds",
                "maximum_peak_memory_gib",
                "maximum_retained_output_mib",
                "network_access",
                "external_executables",
                "new_dependencies",
            },
            "resource_envelope",
        )
        return ParentQualificationDefinition(
            identifier=cls.require_string(payload["identifier"], "identifier"),
            source_revision=cls.require_string(
                payload["source_revision"], "source_revision"
            ),
            sources=tuple(sources),
            isotropic_parent=cls.model_from_payload(
                cls.require_object(payload["isotropic_parent"], "isotropic_parent")
            ),
            isotropic_pretruncation_parent=cls.model_from_payload(
                cls.require_object(
                    payload["isotropic_pretruncation_parent"],
                    "isotropic_pretruncation_parent",
                )
            ),
            anisotropic_lambda_x=cls.require_float(anisotropic["lambda_x"], "lambda_x"),
            anisotropic_lambda_y=cls.require_float(anisotropic["lambda_y"], "lambda_y"),
            anisotropic_lambda_xy=cls.require_float(
                anisotropic["lambda_xy"], "lambda_xy"
            ),
            plane_wave_cutoff=cls.require_int(
                anisotropic["plane_wave_cutoff"], "plane_wave_cutoff"
            ),
            reciprocal_mesh_size=cls.require_int(
                anisotropic["reciprocal_mesh_size"], "reciprocal_mesh_size"
            ),
            hopping_maximum_squared_radius=cls.require_int(
                anisotropic["hopping_maximum_squared_radius"],
                "hopping_maximum_squared_radius",
            ),
            expected_parent_digests=tuple(digests),
            shapes=shapes,
            twist_mesh=BoundaryTwistMesh(LatticeDimension.TWO, mesh_counts),
            perturbations=perturbations,
            tolerances=ParentQualificationTolerances(
                cls.require_float(
                    tolerances["hopping_hermiticity_absolute"],
                    "hopping_hermiticity_absolute",
                ),
                cls.require_float(
                    tolerances["hopping_symmetry_absolute"],
                    "hopping_symmetry_absolute",
                ),
                cls.require_float(
                    tolerances["represented_hermiticity_absolute"],
                    "represented_hermiticity_absolute",
                ),
                cls.require_float(
                    tolerances["gauge_bridge_absolute"], "gauge_bridge_absolute"
                ),
                cls.require_float(
                    tolerances["reconstruction_absolute"],
                    "reconstruction_absolute",
                ),
                cls.require_float(
                    tolerances["separability_absolute"], "separability_absolute"
                ),
            ),
            resource_envelope=ParentQualificationResourceEnvelope(
                cls.require_int(
                    resources["maximum_matrix_dimension"],
                    "maximum_matrix_dimension",
                ),
                cls.require_int(
                    resources["maximum_parent_route_evaluations"],
                    "maximum_parent_route_evaluations",
                ),
                cls.require_int(
                    resources["maximum_defect_route_evaluations"],
                    "maximum_defect_route_evaluations",
                ),
                cls.require_int(
                    resources["maximum_runtime_seconds"],
                    "maximum_runtime_seconds",
                ),
                cls.require_float(
                    resources["maximum_peak_memory_gib"],
                    "maximum_peak_memory_gib",
                ),
                cls.require_float(
                    resources["maximum_retained_output_mib"],
                    "maximum_retained_output_mib",
                ),
                cls.require_bool(resources["network_access"], "network_access"),
                cls.string_tuple(
                    resources["external_executables"], "external_executables"
                ),
                cls.string_tuple(resources["new_dependencies"], "new_dependencies"),
            ),
            claim_boundary=cls.require_string(
                payload["claim_boundary"], "claim_boundary"
            ),
        )

    @classmethod
    def model_from_payload(cls, payload: JsonObject) -> ScalarHoppingModel:
        """Reconstruct one unitless scalar hopping model."""
        cls.require_keys(
            payload,
            {
                "identifier",
                "basis_identifier",
                "energy_reference",
                "energy_unit",
                "terms",
            },
            "model",
        )
        if cls.require_string(payload["energy_unit"], "energy_unit") != "unitless":
            raise ValueError("qualified parent energy_unit must equal unitless")
        term_values = cls.require_list(payload["terms"], "terms")
        terms: list[ScalarHoppingTerm] = []
        for index, value in enumerate(term_values):
            term = cls.require_object(value, f"terms[{index}]")
            cls.require_keys(
                term,
                {"displacement", "real", "imaginary"},
                f"terms[{index}]",
            )
            terms.append(
                ScalarHoppingTerm(
                    LatticeDisplacement(
                        LatticeDimension.TWO,
                        cls.integer_pair(
                            term["displacement"], f"terms[{index}].displacement"
                        ),
                    ),
                    cls.require_float(term["real"], f"terms[{index}].real"),
                    cls.require_float(term["imaginary"], f"terms[{index}].imaginary"),
                )
            )
        return ScalarHoppingModel(
            cls.require_string(payload["identifier"], "identifier"),
            LatticeDimension.TWO,
            tuple(terms),
            Unitless(),
            cls.require_string(payload["energy_reference"], "energy_reference"),
            cls.require_string(payload["basis_identifier"], "basis_identifier"),
        )

    @classmethod
    def perturbation_from_payload(cls, payload: JsonObject) -> LocalizedPerturbation:
        """Reconstruct one unitless localized perturbation."""
        cls.require_keys(
            payload,
            {
                "identifier",
                "basis_identifier",
                "energy_reference",
                "energy_unit",
                "terms",
            },
            "perturbation",
        )
        if cls.require_string(payload["energy_unit"], "energy_unit") != "unitless":
            raise ValueError("qualified perturbation energy_unit must equal unitless")
        term_values = cls.require_list(payload["terms"], "perturbation terms")
        terms: list[LocalizedOnsiteTerm | LocalizedBondTerm] = []
        for index, value in enumerate(term_values):
            term = cls.require_object(value, f"perturbation terms[{index}]")
            kind = cls.require_string(term.get("kind"), "term kind")
            if kind == "onsite":
                cls.require_keys(
                    term,
                    {"kind", "site", "real", "imaginary"},
                    f"perturbation terms[{index}]",
                )
                terms.append(
                    LocalizedOnsiteTerm(
                        LatticeCoordinate(
                            LatticeDimension.TWO,
                            cls.integer_pair(term["site"], "site"),
                        ),
                        cls.require_float(term["real"], "real"),
                        cls.require_float(term["imaginary"], "imaginary"),
                    )
                )
            elif kind == "bond":
                cls.require_keys(
                    term,
                    {"kind", "start", "displacement", "real", "imaginary"},
                    f"perturbation terms[{index}]",
                )
                terms.append(
                    LocalizedBondTerm(
                        LatticeCoordinate(
                            LatticeDimension.TWO,
                            cls.integer_pair(term["start"], "start"),
                        ),
                        LatticeDisplacement(
                            LatticeDimension.TWO,
                            cls.integer_pair(term["displacement"], "displacement"),
                        ),
                        cls.require_float(term["real"], "real"),
                        cls.require_float(term["imaginary"], "imaginary"),
                    )
                )
            else:
                raise ValueError("localized term kind is not supported")
        return LocalizedPerturbation(
            cls.require_string(payload["identifier"], "identifier"),
            LatticeDimension.TWO,
            tuple(terms),
            Unitless(),
            cls.require_string(payload["energy_reference"], "energy_reference"),
            cls.require_string(payload["basis_identifier"], "basis_identifier"),
        )

    @classmethod
    def decode(cls, payload: bytes) -> JsonObject:
        """Decode one strict duplicate-free UTF-8 JSON object."""
        if type(payload) is not bytes:
            raise TypeError("payload must be bytes")
        try:
            decoded: object = json.loads(
                payload.decode("utf-8"), object_pairs_hook=cls.object_pairs
            )
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError("payload must be valid UTF-8 JSON") from error
        return cls.require_object(cls.normalize(decoded), "payload")

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
    def object_pairs(pairs: list[tuple[str, object]]) -> tuple[tuple[str, object], ...]:
        """Retain object pairs so duplicate names can be rejected."""
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
        """Require one nonempty JSON string."""
        if type(value) is not str or not value:
            raise ValueError(f"{name} must be a nonempty string")
        return value

    @staticmethod
    def require_int(value: JsonValue, name: str) -> int:
        """Require one built-in integer without admitting booleans."""
        if type(value) is not int:
            raise ValueError(f"{name} must be an integer")
        return value

    @staticmethod
    def require_float(value: JsonValue, name: str) -> float:
        """Require one built-in JSON float without numeric coercion."""
        if type(value) is not float:
            raise ValueError(f"{name} must be a float")
        return value

    @staticmethod
    def require_bool(value: JsonValue, name: str) -> bool:
        """Require one built-in JSON boolean."""
        if type(value) is not bool:
            raise ValueError(f"{name} must be a boolean")
        return value

    @classmethod
    def integer_pair(cls, value: JsonValue, name: str) -> tuple[int, int]:
        """Require one exact two-integer array."""
        values = cls.require_list(value, name)
        if len(values) != 2:
            raise ValueError(f"{name} must contain two integers")
        return (
            cls.require_int(values[0], f"{name}[0]"),
            cls.require_int(values[1], f"{name}[1]"),
        )

    @classmethod
    def string_tuple(cls, value: JsonValue, name: str) -> tuple[str, ...]:
        """Require one string array."""
        values = cls.require_list(value, name)
        return tuple(
            cls.require_string(item, f"{name}[{index}]")
            for index, item in enumerate(values)
        )

    @staticmethod
    def require_keys(value: JsonObject, expected: set[str], name: str) -> None:
        """Require an exact versioned field set."""
        if set(value) != expected:
            raise ValueError(f"{name} fields do not match schema version 1")

    @staticmethod
    def encode(payload: JsonObject) -> bytes:
        """Return sorted, indented, newline-terminated canonical UTF-8 JSON."""
        return (
            json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
        ).encode("utf-8")


class ParentQualificationRequestJsonSerializer(
    JsonCodec[ParentQualificationDefinition, bytes]
):
    """Round-trip one closed parent qualification request."""

    __slots__ = ()

    def serialize(self, definition: ParentQualificationDefinition) -> bytes:
        """Return canonical version-one request bytes."""
        if type(definition) is not ParentQualificationDefinition:
            raise TypeError("definition must be ParentQualificationDefinition")
        return _ParentQualificationWire.encode(
            {
                "schema_version": 1,
                "record_type": "periodic2d_rank_defect_parent_qualification_request",
                "evidence_status": "accepted_historical_synthetic_parent_projection",
                "definition": _ParentQualificationWire.definition_payload(definition),
            }
        )

    def deserialize(self, payload: bytes) -> ParentQualificationDefinition:
        """Parse and reconstruct one canonical version-one request."""
        root = _ParentQualificationWire.decode(payload)
        _ParentQualificationWire.require_keys(
            root,
            {"schema_version", "record_type", "evidence_status", "definition"},
            "payload",
        )
        if (
            _ParentQualificationWire.require_int(
                root["schema_version"], "schema_version"
            )
            != 1
        ):
            raise ValueError("schema_version must equal 1")
        if (
            _ParentQualificationWire.require_string(root["record_type"], "record_type")
            != "periodic2d_rank_defect_parent_qualification_request"
        ):
            raise ValueError("record_type is not supported")
        if (
            _ParentQualificationWire.require_string(
                root["evidence_status"], "evidence_status"
            )
            != "accepted_historical_synthetic_parent_projection"
        ):
            raise ValueError("evidence_status is not supported")
        result = _ParentQualificationWire.definition_from_payload(
            _ParentQualificationWire.require_object(root["definition"], "definition")
        )
        if self.serialize(result) != payload:
            raise ValueError("payload is not the canonical request representation")
        return result


class ParentQualificationResultJsonSerializer(
    JsonCodec[ParentQualificationResult, bytes]
):
    """Round-trip one closed parent qualification result."""

    __slots__ = ()

    def serialize(self, result: ParentQualificationResult) -> bytes:
        """Return canonical version-one result bytes."""
        if type(result) is not ParentQualificationResult:
            raise TypeError("result must be ParentQualificationResult")
        return _ParentQualificationWire.encode(
            {
                "schema_version": 1,
                "record_type": "periodic2d_rank_defect_parent_qualification_result",
                "evidence_status": "accepted_parent_numerical_capability_qualification",
                "calculation_status": "calculated_local_parent_qualification",
                "definition": _ParentQualificationWire.definition_payload(
                    result.definition
                ),
                "parents": [
                    {
                        "parent_identifier": value.parent_identifier,
                        "hopping_count": value.hopping_count,
                        "hopping_digest": value.hopping_digest,
                        "hopping_hermiticity_maximum_absolute": (
                            value.hopping_hermiticity_maximum_absolute
                        ),
                        "hopping_symmetry_maximum_absolute": (
                            value.hopping_symmetry_maximum_absolute
                        ),
                        "represented_hermiticity_maximum_absolute": (
                            value.represented_hermiticity_maximum_absolute
                        ),
                        "gauge_bridge_maximum_absolute": (
                            value.gauge_bridge_maximum_absolute
                        ),
                        "route_evaluations": value.route_evaluations,
                        "inherited_truncation_maximum_absolute": (
                            value.inherited_truncation_maximum_absolute
                        ),
                        "inherited_truncation_frobenius": (
                            value.inherited_truncation_frobenius
                        ),
                    }
                    for value in result.parents
                ],
                "perturbations": [
                    {
                        "perturbation_identifier": value.perturbation_identifier,
                        "term_count": value.term_count,
                        "represented_hermiticity_maximum_absolute": (
                            value.represented_hermiticity_maximum_absolute
                        ),
                        "gauge_bridge_maximum_absolute": (
                            value.gauge_bridge_maximum_absolute
                        ),
                        "route_evaluations": value.route_evaluations,
                    }
                    for value in result.perturbations
                ],
                "maximum_plane_wave_separability_absolute": (
                    result.maximum_plane_wave_separability_absolute
                ),
                "failed_criteria": list(result.failed_criteria),
            }
        )

    def deserialize(self, payload: bytes) -> ParentQualificationResult:
        """Parse and reconstruct one canonical version-one result."""
        root = _ParentQualificationWire.decode(payload)
        _ParentQualificationWire.require_keys(
            root,
            {
                "schema_version",
                "record_type",
                "evidence_status",
                "calculation_status",
                "definition",
                "parents",
                "perturbations",
                "maximum_plane_wave_separability_absolute",
                "failed_criteria",
            },
            "payload",
        )
        if (
            _ParentQualificationWire.require_int(
                root["schema_version"], "schema_version"
            )
            != 1
        ):
            raise ValueError("schema_version must equal 1")
        if (
            _ParentQualificationWire.require_string(root["record_type"], "record_type")
            != "periodic2d_rank_defect_parent_qualification_result"
        ):
            raise ValueError("record_type is not supported")
        if (
            _ParentQualificationWire.require_string(
                root["evidence_status"], "evidence_status"
            )
            != "accepted_parent_numerical_capability_qualification"
        ):
            raise ValueError("evidence_status is not supported")
        if (
            _ParentQualificationWire.require_string(
                root["calculation_status"], "calculation_status"
            )
            != "calculated_local_parent_qualification"
        ):
            raise ValueError("calculation_status is not supported")
        definition = _ParentQualificationWire.definition_from_payload(
            _ParentQualificationWire.require_object(root["definition"], "definition")
        )
        parent_values = _ParentQualificationWire.require_list(
            root["parents"], "parents"
        )
        parents: list[QualifiedParentMetrics] = []
        for index, value in enumerate(parent_values):
            record = _ParentQualificationWire.require_object(value, f"parents[{index}]")
            _ParentQualificationWire.require_keys(
                record,
                {
                    "parent_identifier",
                    "hopping_count",
                    "hopping_digest",
                    "hopping_hermiticity_maximum_absolute",
                    "hopping_symmetry_maximum_absolute",
                    "represented_hermiticity_maximum_absolute",
                    "gauge_bridge_maximum_absolute",
                    "route_evaluations",
                    "inherited_truncation_maximum_absolute",
                    "inherited_truncation_frobenius",
                },
                f"parents[{index}]",
            )
            parents.append(
                QualifiedParentMetrics(
                    _ParentQualificationWire.require_string(
                        record["parent_identifier"], "parent_identifier"
                    ),
                    _ParentQualificationWire.require_int(
                        record["hopping_count"], "hopping_count"
                    ),
                    _ParentQualificationWire.require_string(
                        record["hopping_digest"], "hopping_digest"
                    ),
                    _ParentQualificationWire.require_float(
                        record["hopping_hermiticity_maximum_absolute"],
                        "hopping_hermiticity_maximum_absolute",
                    ),
                    _ParentQualificationWire.require_float(
                        record["hopping_symmetry_maximum_absolute"],
                        "hopping_symmetry_maximum_absolute",
                    ),
                    _ParentQualificationWire.require_float(
                        record["represented_hermiticity_maximum_absolute"],
                        "represented_hermiticity_maximum_absolute",
                    ),
                    _ParentQualificationWire.require_float(
                        record["gauge_bridge_maximum_absolute"],
                        "gauge_bridge_maximum_absolute",
                    ),
                    _ParentQualificationWire.require_int(
                        record["route_evaluations"], "route_evaluations"
                    ),
                    _ParentQualificationWire.require_float(
                        record["inherited_truncation_maximum_absolute"],
                        "inherited_truncation_maximum_absolute",
                    ),
                    _ParentQualificationWire.require_float(
                        record["inherited_truncation_frobenius"],
                        "inherited_truncation_frobenius",
                    ),
                )
            )
        perturbation_values = _ParentQualificationWire.require_list(
            root["perturbations"], "perturbations"
        )
        perturbations: list[QualifiedPerturbationMetrics] = []
        for index, value in enumerate(perturbation_values):
            record = _ParentQualificationWire.require_object(
                value, f"perturbations[{index}]"
            )
            _ParentQualificationWire.require_keys(
                record,
                {
                    "perturbation_identifier",
                    "term_count",
                    "represented_hermiticity_maximum_absolute",
                    "gauge_bridge_maximum_absolute",
                    "route_evaluations",
                },
                f"perturbations[{index}]",
            )
            perturbations.append(
                QualifiedPerturbationMetrics(
                    _ParentQualificationWire.require_string(
                        record["perturbation_identifier"],
                        "perturbation_identifier",
                    ),
                    _ParentQualificationWire.require_int(
                        record["term_count"], "term_count"
                    ),
                    _ParentQualificationWire.require_float(
                        record["represented_hermiticity_maximum_absolute"],
                        "represented_hermiticity_maximum_absolute",
                    ),
                    _ParentQualificationWire.require_float(
                        record["gauge_bridge_maximum_absolute"],
                        "gauge_bridge_maximum_absolute",
                    ),
                    _ParentQualificationWire.require_int(
                        record["route_evaluations"], "route_evaluations"
                    ),
                )
            )
        failure_values = _ParentQualificationWire.require_list(
            root["failed_criteria"], "failed_criteria"
        )
        result = ParentQualificationResult(
            definition,
            tuple(parents),
            tuple(perturbations),
            _ParentQualificationWire.require_float(
                root["maximum_plane_wave_separability_absolute"],
                "maximum_plane_wave_separability_absolute",
            ),
            tuple(
                _ParentQualificationWire.require_string(
                    value, f"failed_criteria[{index}]"
                )
                for index, value in enumerate(failure_values)
            ),
        )
        if self.serialize(result) != payload:
            raise ValueError("payload is not the canonical result representation")
        return result
