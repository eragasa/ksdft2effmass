"""Canonical version-one JSON serialization for folding/null results."""

from __future__ import annotations

import json
from typing import cast

from projectkoios.physkit.units import Unitless

from ksdft2effmass.serialization import JsonCodec
from ksdft2effmass.solidstate import (
    BoundaryTwistLift,
    FiniteLatticeShape,
    LatticeDimension,
    LatticeDisplacement,
    ScalarHoppingModel,
    ScalarHoppingTerm,
)

from .folding_null import (
    FoldingMetrics,
    FoldingNullAlignmentAttack,
    FoldingNullCase,
    FoldingNullCaseResult,
    FoldingNullResult,
    FoldingNullStudyDefinition,
    FoldingNullTolerances,
    NullAlignmentMetrics,
)

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type JsonObject = dict[str, JsonValue]


class FoldingNullResultJsonSerializer(JsonCodec[FoldingNullResult, bytes]):
    """Round-trip one immutable folding/null-control result as canonical UTF-8 JSON."""

    __slots__ = ()

    def serialize(self, result: FoldingNullResult) -> bytes:
        """Return sorted, indented, newline-terminated version-one bytes."""
        if type(result) is not FoldingNullResult:
            raise TypeError("result must be FoldingNullResult")
        payload: JsonObject = {
            "schema_version": 1,
            "record_type": "periodic2d_rank_defect_folding_null_result",
            "evidence_status": "authored_synthetic_numerical_verification",
            "calculation_status": "calculated_synthetic_result",
            "definition": self._definition_payload(result.definition),
            "cases": [self._case_payload(case) for case in result.cases],
            "failed_criteria": list(result.failed_criteria),
        }
        return (
            json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
        ).encode("utf-8")

    def deserialize(self, payload: bytes) -> FoldingNullResult:
        """Parse and reconstruct one version-one folding/null result."""
        if type(payload) is not bytes:
            raise TypeError("payload must be bytes")
        try:
            decoded: object = json.loads(
                payload.decode("utf-8"), object_pairs_hook=self._object_pairs
            )
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError("payload must be valid UTF-8 JSON") from error
        root = self._require_object(self._normalize(decoded), "payload")
        self._require_keys(
            root,
            {
                "schema_version",
                "record_type",
                "evidence_status",
                "calculation_status",
                "definition",
                "cases",
                "failed_criteria",
            },
            "payload",
        )
        if self._require_int(root["schema_version"], "schema_version") != 1:
            raise ValueError("schema_version must equal 1")
        if (
            self._require_string(root["record_type"], "record_type")
            != "periodic2d_rank_defect_folding_null_result"
        ):
            raise ValueError("record_type is not supported")
        if (
            self._require_string(root["evidence_status"], "evidence_status")
            != "authored_synthetic_numerical_verification"
        ):
            raise ValueError("evidence_status is not supported")
        if (
            self._require_string(root["calculation_status"], "calculation_status")
            != "calculated_synthetic_result"
        ):
            raise ValueError("calculation_status is not supported")
        definition = self._definition_from_payload(
            self._require_object(root["definition"], "definition")
        )
        case_values = self._require_list(root["cases"], "cases")
        if len(case_values) != len(definition.cases):
            raise ValueError(
                "case count must match the folding/null-control definition"
            )
        cases = tuple(
            self._case_from_payload(
                self._require_object(value, f"cases[{index}]"),
                definition.cases[index],
            )
            for index, value in enumerate(case_values)
        )
        failure_values = self._require_list(root["failed_criteria"], "failed_criteria")
        failures = tuple(
            self._require_string(value, f"failed_criteria[{index}]")
            for index, value in enumerate(failure_values)
        )
        result = FoldingNullResult(definition, cases, failures)
        if self.serialize(result) != payload:
            raise ValueError("payload is not the canonical folding/null representation")
        return result

    @staticmethod
    def _definition_payload(definition: FoldingNullStudyDefinition) -> JsonObject:
        """Represent one complete folding/null-control definition."""
        return {
            "identifier": definition.identifier,
            "parent": {
                "identifier": definition.parent.identifier,
                "basis_identifier": definition.parent.basis_identifier,
                "energy_reference": definition.parent.energy_reference,
                "energy_unit": "unitless",
                "terms": [
                    {
                        "displacement": list(term.displacement.components),
                        "real": term.real,
                        "imaginary": term.imaginary,
                    }
                    for term in definition.parent.terms
                ],
            },
            "cases": [
                {
                    "identifier": case.identifier,
                    "shape": list(case.shape.extents),
                    "twist_turns": list(case.twist.turns),
                }
                for case in definition.cases
            ],
            "null_attack": {
                "translation_cells": list(definition.null_attack.translation_cells),
                "site_phase_steps_radians": list(
                    definition.null_attack.site_phase_steps_radians
                ),
                "energy_reference_shift": (
                    definition.null_attack.energy_reference_shift
                ),
            },
            "tolerances": {
                "algebraic_absolute": definition.tolerances.algebraic_absolute,
                "folding_unitarity": definition.tolerances.folding_unitarity,
            },
        }

    def _definition_from_payload(
        self, payload: JsonObject
    ) -> FoldingNullStudyDefinition:
        """Reconstruct one complete folding/null-control definition."""
        self._require_keys(
            payload,
            {"identifier", "parent", "cases", "null_attack", "tolerances"},
            "definition",
        )
        parent_payload = self._require_object(payload["parent"], "parent")
        self._require_keys(
            parent_payload,
            {
                "identifier",
                "basis_identifier",
                "energy_reference",
                "energy_unit",
                "terms",
            },
            "parent",
        )
        if self._require_string(parent_payload["energy_unit"], "energy_unit") != (
            "unitless"
        ):
            raise ValueError(
                "folding/null-control parent energy_unit must equal unitless"
            )
        terms_payload = self._require_list(parent_payload["terms"], "terms")
        terms: list[ScalarHoppingTerm] = []
        for index, value in enumerate(terms_payload):
            term = self._require_object(value, f"terms[{index}]")
            self._require_keys(
                term,
                {"displacement", "real", "imaginary"},
                f"terms[{index}]",
            )
            displacement = self._integer_pair(
                term["displacement"], f"terms[{index}].displacement"
            )
            terms.append(
                ScalarHoppingTerm(
                    LatticeDisplacement(LatticeDimension.TWO, displacement),
                    self._require_float(term["real"], f"terms[{index}].real"),
                    self._require_float(term["imaginary"], f"terms[{index}].imaginary"),
                )
            )
        parent = ScalarHoppingModel(
            identifier=self._require_string(parent_payload["identifier"], "identifier"),
            dimension=LatticeDimension.TWO,
            terms=tuple(terms),
            energy_unit=Unitless(),
            energy_reference=self._require_string(
                parent_payload["energy_reference"], "energy_reference"
            ),
            basis_identifier=self._require_string(
                parent_payload["basis_identifier"], "basis_identifier"
            ),
        )
        cases_payload = self._require_list(payload["cases"], "cases")
        cases: list[FoldingNullCase] = []
        for index, value in enumerate(cases_payload):
            case = self._require_object(value, f"cases[{index}]")
            self._require_keys(
                case,
                {"identifier", "shape", "twist_turns"},
                f"cases[{index}]",
            )
            cases.append(
                FoldingNullCase(
                    identifier=self._require_string(
                        case["identifier"], f"cases[{index}].identifier"
                    ),
                    shape=FiniteLatticeShape(
                        LatticeDimension.TWO,
                        self._integer_pair(case["shape"], f"cases[{index}].shape"),
                    ),
                    twist=BoundaryTwistLift(
                        LatticeDimension.TWO,
                        self._float_pair(
                            case["twist_turns"], f"cases[{index}].twist_turns"
                        ),
                    ),
                )
            )
        attack_payload = self._require_object(payload["null_attack"], "null_attack")
        self._require_keys(
            attack_payload,
            {
                "translation_cells",
                "site_phase_steps_radians",
                "energy_reference_shift",
            },
            "null_attack",
        )
        attack = FoldingNullAlignmentAttack(
            translation_cells=self._integer_pair(
                attack_payload["translation_cells"], "translation_cells"
            ),
            site_phase_steps_radians=self._float_pair(
                attack_payload["site_phase_steps_radians"],
                "site_phase_steps_radians",
            ),
            energy_reference_shift=self._require_float(
                attack_payload["energy_reference_shift"],
                "energy_reference_shift",
            ),
        )
        tolerances_payload = self._require_object(payload["tolerances"], "tolerances")
        self._require_keys(
            tolerances_payload,
            {"algebraic_absolute", "folding_unitarity"},
            "tolerances",
        )
        tolerances = FoldingNullTolerances(
            algebraic_absolute=self._require_float(
                tolerances_payload["algebraic_absolute"], "algebraic_absolute"
            ),
            folding_unitarity=self._require_float(
                tolerances_payload["folding_unitarity"], "folding_unitarity"
            ),
        )
        return FoldingNullStudyDefinition(
            self._require_string(payload["identifier"], "identifier"),
            parent,
            tuple(cases),
            attack,
            tolerances,
        )

    @staticmethod
    def _case_payload(case: FoldingNullCaseResult) -> JsonObject:
        """Represent one correlated folding/null-control case result."""
        return {
            "identifier": case.case.identifier,
            "folding": {
                "unitarity_maximum_absolute_defect": (
                    case.folding.unitarity_maximum_absolute_defect
                ),
                "hermiticity_maximum_absolute_defect": (
                    case.folding.hermiticity_maximum_absolute_defect
                ),
                "off_diagonal_maximum_absolute": (
                    case.folding.off_diagonal_maximum_absolute
                ),
                "primitive_energy_maximum_absolute_defect": (
                    case.folding.primitive_energy_maximum_absolute_defect
                ),
                "eigenvalue_maximum_absolute_defect": (
                    case.folding.eigenvalue_maximum_absolute_defect
                ),
            },
            "null_extraction": {
                "transform_unitarity_maximum_absolute_defect": (
                    case.null_extraction.transform_unitarity_maximum_absolute_defect
                ),
                "recovered_maximum_absolute_defect": (
                    case.null_extraction.recovered_maximum_absolute_defect
                ),
                "recovered_frobenius_defect": (
                    case.null_extraction.recovered_frobenius_defect
                ),
            },
        }

    def _case_from_payload(
        self, payload: JsonObject, expected_case: FoldingNullCase
    ) -> FoldingNullCaseResult:
        """Reconstruct one result and bind it to its definition case."""
        self._require_keys(
            payload, {"identifier", "folding", "null_extraction"}, "case"
        )
        if self._require_string(payload["identifier"], "identifier") != (
            expected_case.identifier
        ):
            raise ValueError("result case identifier does not match the definition")
        folding = self._require_object(payload["folding"], "folding")
        self._require_keys(
            folding,
            {
                "unitarity_maximum_absolute_defect",
                "hermiticity_maximum_absolute_defect",
                "off_diagonal_maximum_absolute",
                "primitive_energy_maximum_absolute_defect",
                "eigenvalue_maximum_absolute_defect",
            },
            "folding",
        )
        null = self._require_object(payload["null_extraction"], "null_extraction")
        self._require_keys(
            null,
            {
                "transform_unitarity_maximum_absolute_defect",
                "recovered_maximum_absolute_defect",
                "recovered_frobenius_defect",
            },
            "null_extraction",
        )
        return FoldingNullCaseResult(
            expected_case,
            FoldingMetrics(
                self._require_float(
                    folding["unitarity_maximum_absolute_defect"],
                    "unitarity_maximum_absolute_defect",
                ),
                self._require_float(
                    folding["hermiticity_maximum_absolute_defect"],
                    "hermiticity_maximum_absolute_defect",
                ),
                self._require_float(
                    folding["off_diagonal_maximum_absolute"],
                    "off_diagonal_maximum_absolute",
                ),
                self._require_float(
                    folding["primitive_energy_maximum_absolute_defect"],
                    "primitive_energy_maximum_absolute_defect",
                ),
                self._require_float(
                    folding["eigenvalue_maximum_absolute_defect"],
                    "eigenvalue_maximum_absolute_defect",
                ),
            ),
            NullAlignmentMetrics(
                self._require_float(
                    null["transform_unitarity_maximum_absolute_defect"],
                    "transform_unitarity_maximum_absolute_defect",
                ),
                self._require_float(
                    null["recovered_maximum_absolute_defect"],
                    "recovered_maximum_absolute_defect",
                ),
                self._require_float(
                    null["recovered_frobenius_defect"],
                    "recovered_frobenius_defect",
                ),
            ),
        )

    @classmethod
    def _normalize(cls, value: object) -> JsonValue:
        """Convert decoded JSON into the closed recursive wire representation."""
        if value is None or type(value) in {bool, int, float, str}:
            return cast(None | bool | int | float | str, value)
        if type(value) is list:
            return [cls._normalize(item) for item in value]
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
                result[key] = cls._normalize(item)
            return result
        raise ValueError("payload contains an unsupported JSON value")

    @staticmethod
    def _object_pairs(
        pairs: list[tuple[str, object]],
    ) -> tuple[tuple[str, object], ...]:
        """Preserve JSON object pairs so duplicate names can be rejected."""
        return tuple(pairs)

    @staticmethod
    def _require_object(value: JsonValue, name: str) -> JsonObject:
        """Require one JSON object."""
        if type(value) is not dict:
            raise ValueError(f"{name} must be an object")
        return value

    @staticmethod
    def _require_list(value: JsonValue, name: str) -> list[JsonValue]:
        """Require one JSON array."""
        if type(value) is not list:
            raise ValueError(f"{name} must be an array")
        return value

    @staticmethod
    def _require_string(value: JsonValue, name: str) -> str:
        """Require one nonempty string."""
        if type(value) is not str or not value:
            raise ValueError(f"{name} must be a nonempty string")
        return value

    @staticmethod
    def _require_int(value: JsonValue, name: str) -> int:
        """Require one integer without admitting booleans."""
        if type(value) is not int:
            raise ValueError(f"{name} must be an integer")
        return value

    @staticmethod
    def _require_float(value: JsonValue, name: str) -> float:
        """Require one built-in JSON float without numeric coercion."""
        if type(value) is not float:
            raise ValueError(f"{name} must be a float")
        return value

    def _integer_pair(self, value: JsonValue, name: str) -> tuple[int, int]:
        """Require one exact two-integer array."""
        values = self._require_list(value, name)
        if len(values) != 2:
            raise ValueError(f"{name} must contain two integers")
        return (
            self._require_int(values[0], f"{name}[0]"),
            self._require_int(values[1], f"{name}[1]"),
        )

    def _float_pair(self, value: JsonValue, name: str) -> tuple[float, float]:
        """Require one exact two-float array."""
        values = self._require_list(value, name)
        if len(values) != 2:
            raise ValueError(f"{name} must contain two floats")
        return (
            self._require_float(values[0], f"{name}[0]"),
            self._require_float(values[1], f"{name}[1]"),
        )

    @staticmethod
    def _require_keys(value: JsonObject, expected: set[str], name: str) -> None:
        """Require one exact versioned object key set."""
        if set(value) != expected:
            raise ValueError(f"{name} fields do not match schema version 1")
