"""Lossless scalar QoI result values for the injected Workflow codec boundary.

``qoi-result-value:1`` supports exactly scalar success and scalar evaluation failure,
including their complete definitions and correlations. Canonical ASCII JSON uses
explicit record/nominal tags and hexadecimal finite floats (including signed zero).
It performs no numerical evaluation, unit conversion, native I/O, execution, replay
or scientific validation. It does not encode arbitrary ResultObject implementations.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from typing import Literal, Never, cast

from ksdft2effmass.workflows.model import ResultObject, ResultObjectIdentity
from ksdft2effmass.workflows.persistence import (
    WorkflowEncodedResultValue,
    WorkflowPersistenceFailure,
    WorkflowPersistenceFailureCode,
    WorkflowResultValueDecodeResult,
    WorkflowResultValueEncodeResult,
)
from ksdft2effmass.workflows.runs.identities import (
    ResultObjectContentIdentity,
    ResultObjectDomainIdentity,
    ResultObjectTypeIdentity,
)

from .qoi import (
    NormalizedObservationRequirementIdentity,
    QuantityOfInterestCompleteness,
    QuantityOfInterestConventionIdentity,
    QuantityOfInterestEvaluationFailureCode,
    QuantityOfInterestEvaluatorIdentity,
    QuantityOfInterestIdentity,
    QuantityOfInterestStateSpaceIdentity,
    QuantityOfInterestSubjectIdentity,
    ScalarQuantityOfInterestDefinition,
    ScalarQuantityOfInterestEvaluationFailure,
    ScalarQuantityOfInterestValue,
)

type _JsonValue = None | bool | str | list[_JsonValue] | dict[str, _JsonValue]
type _ScalarResult = (
    ScalarQuantityOfInterestValue | ScalarQuantityOfInterestEvaluationFailure
)


@dataclass(frozen=True, slots=True)
class QuantityOfInterestResultValueSerializer:
    """Effect-free codec for two exact scalar result contracts, wire version 1.

    Notes
    -----
    Supported type labels are the public import name followed by ``:1``; the domain
    is ``ksdft2effmass.analysis`` and schema is ``qoi-result-value:1``. Every declared
    field is retained. Content identity is ``qoi-result-value:1:sha256:<digest>`` of
    the canonical complete payload. Evaluator labels remain data, not discovered
    implementations. Unknown versions are incompatible, not successful substitutes.
    No mutable dependencies, cache, registry, or native-data access is used.
    """

    def encode(self, value: ResultObject) -> WorkflowResultValueEncodeResult:
        """Encode one supported concrete scalar result without coercion.

        Parameters
        ----------
        value
            Workflow-facing result. Only the two exact supported classes encode;
            subclasses and other protocol implementations return incompatible.

        Returns
        -------
        WorkflowResultValueEncodeResult
            Complete envelope, or structured incompatible/invalid/error evidence.

        Raises
        ------
        TypeError
            Input does not expose an exact nominal ResultObject identity.
        """
        if (
            not isinstance(value, ResultObject)
            or type(value.identity) is not ResultObjectIdentity
        ):
            raise TypeError("value must expose an exact ResultObjectIdentity")
        if (
            type(value) is not ScalarQuantityOfInterestValue
            and type(value) is not ScalarQuantityOfInterestEvaluationFailure
        ):
            return WorkflowResultValueEncodeResult(
                status="incompatible",
                failure=self._failure(
                    "encode",
                    WorkflowPersistenceFailureCode.UNSUPPORTED_TYPE,
                    (value.identity.value,),
                ),
            )
        try:
            payload = self._payload(value)
            digest = hashlib.sha256(payload).hexdigest()
            label = (
                "ksdft2effmass.analysis.ScalarQuantityOfInterestValue:1"
                if type(value) is ScalarQuantityOfInterestValue
                else (
                    "ksdft2effmass.analysis.ScalarQuantityOfInterestEvaluationFailure:1"
                )
            )
            encoded = WorkflowEncodedResultValue(
                result_identity=value.identity,
                concrete_type_identity=ResultObjectTypeIdentity(label),
                owning_domain_identity=ResultObjectDomainIdentity(
                    "ksdft2effmass.analysis"
                ),
                schema_identity="qoi-result-value:1",
                content_identity=ResultObjectContentIdentity(
                    f"qoi-result-value:1:sha256:{digest}"
                ),
                payload=payload,
                payload_digest=digest,
            )
            return WorkflowResultValueEncodeResult(status="encoded", encoded=encoded)
        except MemoryError, RecursionError:
            status: Literal["invalid", "error"] = "error"
            code = WorkflowPersistenceFailureCode.REPRESENTATION_LIMIT
        except TypeError, ValueError, OverflowError:
            status = "invalid"
            code = WorkflowPersistenceFailureCode.INVARIANT_VIOLATION
        except Exception:
            status = "error"
            code = WorkflowPersistenceFailureCode.CODEC_ERROR
        return WorkflowResultValueEncodeResult(
            status=status,
            failure=self._failure("encode", code, (value.identity.value,)),
        )

    def decode(
        self, value: WorkflowEncodedResultValue
    ) -> WorkflowResultValueDecodeResult:
        """Reconstruct an exact concrete result after full envelope binding.

        Parameters
        ----------
        value
            Complete byte-bound envelope. Exact known schema and type are required.

        Returns
        -------
        WorkflowResultValueDecodeResult
            Concrete immutable result, or incompatible/corrupt/error evidence.
            No failure contains a partial result. Extra/missing fields, duplicate
            members, noncanonical bytes and constructor violations are corrupt.

        Raises
        ------
        TypeError
            Input is not an exact WorkflowEncodedResultValue.
        """
        if type(value) is not WorkflowEncodedResultValue:
            raise TypeError("value must be WorkflowEncodedResultValue")
        inputs = (
            value.result_identity.value,
            value.schema_identity,
            value.concrete_type_identity.value,
        )
        if value.schema_identity != "qoi-result-value:1":
            return WorkflowResultValueDecodeResult(
                status="incompatible",
                failure=self._failure(
                    "decode", WorkflowPersistenceFailureCode.UNSUPPORTED_VERSION, inputs
                ),
            )
        if value.concrete_type_identity.value not in (
            "ksdft2effmass.analysis.ScalarQuantityOfInterestValue:1",
            "ksdft2effmass.analysis.ScalarQuantityOfInterestEvaluationFailure:1",
        ):
            return WorkflowResultValueDecodeResult(
                status="incompatible",
                failure=self._failure(
                    "decode", WorkflowPersistenceFailureCode.UNSUPPORTED_TYPE, inputs
                ),
            )
        try:
            if value.owning_domain_identity.value != "ksdft2effmass.analysis":
                return WorkflowResultValueDecodeResult(
                    status="corrupt",
                    failure=self._failure(
                        "decode",
                        WorkflowPersistenceFailureCode.IDENTITY_MISMATCH,
                        inputs,
                    ),
                )
            digest = hashlib.sha256(value.payload).hexdigest()
            if (
                value.payload_digest != digest
                or value.content_identity.value != f"qoi-result-value:1:sha256:{digest}"
            ):
                return WorkflowResultValueDecodeResult(
                    status="corrupt",
                    failure=self._failure(
                        "decode",
                        WorkflowPersistenceFailureCode.CONTENT_MISMATCH,
                        inputs,
                    ),
                )
            # json's exact callbacks restrict the decoded representation to this
            # closed union; raw numeric tokens are not members of the wire grammar.
            wire = cast(
                _JsonValue,
                json.loads(
                    value.payload.decode("ascii"),
                    object_pairs_hook=self._unique_object,
                    parse_int=self._reject_number,
                    parse_float=self._reject_number,
                    parse_constant=self._reject_number,
                ),
            )
            tag = (
                "ScalarQuantityOfInterestValue"
                if value.concrete_type_identity.value
                == "ksdft2effmass.analysis.ScalarQuantityOfInterestValue:1"
                else "ScalarQuantityOfInterestEvaluationFailure"
            )
            result = self._decode_result(wire, tag)
            if result.identity != value.result_identity:
                return WorkflowResultValueDecodeResult(
                    status="corrupt",
                    failure=self._failure(
                        "decode",
                        WorkflowPersistenceFailureCode.IDENTITY_MISMATCH,
                        inputs,
                    ),
                )
            if self._payload(result) != value.payload:
                raise ValueError("noncanonical complete payload")
            return WorkflowResultValueDecodeResult(status="decoded", value=result)
        except MemoryError, RecursionError:
            status: Literal["corrupt", "error"] = "error"
            code = WorkflowPersistenceFailureCode.REPRESENTATION_LIMIT
        except TypeError, ValueError, OverflowError, KeyError:
            status = "corrupt"
            code = WorkflowPersistenceFailureCode.MALFORMED_REPRESENTATION
        except Exception:
            status = "error"
            code = WorkflowPersistenceFailureCode.CODEC_ERROR
        return WorkflowResultValueDecodeResult(
            status=status, failure=self._failure("decode", code, inputs)
        )

    @staticmethod
    def _failure(
        phase: str, code: WorkflowPersistenceFailureCode, identities: tuple[str, ...]
    ) -> WorkflowPersistenceFailure:
        return WorkflowPersistenceFailure(
            implementation_identity="ksdft2effmass.analysis.QuantityOfInterestResultValueSerializer:1",
            phase=phase,
            code=code,
            input_identities=identities,
            expected="complete canonical supported scalar result and matching envelope",
            observed=code.value,
            diagnostic="scalar result codec did not produce a complete value",
            claim_boundary=(
                "represented software failure only; no scientific or execution claim"
            ),
        )

    @staticmethod
    def _unique_object(pairs: list[tuple[str, _JsonValue]]) -> dict[str, _JsonValue]:
        """Own json's object-pairs hook and reject duplicate members."""
        result: dict[str, _JsonValue] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate member")
            result[key] = value
        return result

    @staticmethod
    def _reject_number(token: str) -> Never:
        """Own json's number hooks; scalars use explicit tagged hex strings."""
        raise ValueError("untagged numeric token")

    @staticmethod
    def _record(tag: str, fields: dict[str, _JsonValue]) -> _JsonValue:
        return {"type": tag, "fields": fields}

    @classmethod
    def _nominal(cls, tag: str, value: str) -> _JsonValue:
        return cls._record(tag, {"value": value})

    @classmethod
    def _payload(cls, value: _ScalarResult) -> bytes:
        quantity = value.quantity
        definition = cls._record(
            "ScalarQuantityOfInterestDefinition",
            {
                "identity": cls._nominal(
                    "QuantityOfInterestIdentity", quantity.identity.value
                ),
                "subject_identity": cls._nominal(
                    "QuantityOfInterestSubjectIdentity", quantity.subject_identity.value
                ),
                "state_space_identity": None
                if quantity.state_space_identity is None
                else cls._nominal(
                    "QuantityOfInterestStateSpaceIdentity",
                    quantity.state_space_identity.value,
                ),
                "convention_identity": cls._nominal(
                    "QuantityOfInterestConventionIdentity",
                    quantity.convention_identity.value,
                ),
                "evaluator_identity": cls._nominal(
                    "QuantityOfInterestEvaluatorIdentity",
                    quantity.evaluator_identity.value,
                ),
                "observation_requirement_identities": [
                    cls._nominal("NormalizedObservationRequirementIdentity", item.value)
                    for item in quantity.observation_requirement_identities
                ],
                "completeness": cls._nominal(
                    "QuantityOfInterestCompleteness", quantity.completeness.value
                ),
                "unit": quantity.unit,
            },
        )
        fields: dict[str, _JsonValue] = {
            "identity": cls._nominal("ResultObjectIdentity", value.identity.value),
            "quantity": definition,
            "source_observation_set_result_identity": cls._nominal(
                "ResultObjectIdentity",
                value.source_observation_set_result_identity.value,
            ),
            "evaluator_identity": cls._nominal(
                "QuantityOfInterestEvaluatorIdentity", value.evaluator_identity.value
            ),
        }
        if type(value) is ScalarQuantityOfInterestValue:
            if type(value.value) is not float or not math.isfinite(value.value):
                raise ValueError("value must remain a finite built-in float")
            fields["value"] = cls._nominal("float", value.value.hex())
            tag = "ScalarQuantityOfInterestValue"
        elif type(value) is ScalarQuantityOfInterestEvaluationFailure:
            fields["code"] = cls._nominal(
                "QuantityOfInterestEvaluationFailureCode", value.code.value
            )
            fields["detail"] = value.detail
            tag = "ScalarQuantityOfInterestEvaluationFailure"
        else:
            raise TypeError("unsupported exact scalar result type")
        return json.dumps(
            cls._record(tag, fields),
            ensure_ascii=True,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("ascii")

    @staticmethod
    def _fields(
        value: _JsonValue, tag: str, names: tuple[str, ...]
    ) -> dict[str, _JsonValue]:
        if (
            not isinstance(value, dict)
            or set(value) != {"type", "fields"}
            or value["type"] != tag
        ):
            raise ValueError("wrong record shape or tag")
        fields = value["fields"]
        if not isinstance(fields, dict) or set(fields) != set(names):
            raise ValueError("wrong field inventory")
        return fields

    @staticmethod
    def _string(value: _JsonValue) -> str:
        if type(value) is not str:
            raise TypeError("expected exact string")
        return value

    @classmethod
    def _label(cls, value: _JsonValue, tag: str) -> str:
        return cls._string(cls._fields(value, tag, ("value",))["value"])

    @classmethod
    def _decode_definition(
        cls, value: _JsonValue
    ) -> ScalarQuantityOfInterestDefinition:
        fields = cls._fields(
            value,
            "ScalarQuantityOfInterestDefinition",
            (
                "identity",
                "subject_identity",
                "state_space_identity",
                "convention_identity",
                "evaluator_identity",
                "observation_requirement_identities",
                "completeness",
                "unit",
            ),
        )
        requirements = fields["observation_requirement_identities"]
        if not isinstance(requirements, list):
            raise TypeError("requirements must be an ordered array")
        state = fields["state_space_identity"]
        return ScalarQuantityOfInterestDefinition(
            identity=QuantityOfInterestIdentity(
                cls._label(fields["identity"], "QuantityOfInterestIdentity")
            ),
            subject_identity=QuantityOfInterestSubjectIdentity(
                cls._label(
                    fields["subject_identity"], "QuantityOfInterestSubjectIdentity"
                )
            ),
            state_space_identity=None
            if state is None
            else QuantityOfInterestStateSpaceIdentity(
                cls._label(state, "QuantityOfInterestStateSpaceIdentity")
            ),
            convention_identity=QuantityOfInterestConventionIdentity(
                cls._label(
                    fields["convention_identity"],
                    "QuantityOfInterestConventionIdentity",
                )
            ),
            evaluator_identity=QuantityOfInterestEvaluatorIdentity(
                cls._label(
                    fields["evaluator_identity"], "QuantityOfInterestEvaluatorIdentity"
                )
            ),
            observation_requirement_identities=tuple(
                NormalizedObservationRequirementIdentity(
                    cls._label(item, "NormalizedObservationRequirementIdentity")
                )
                for item in requirements
            ),
            completeness=QuantityOfInterestCompleteness(
                cls._label(fields["completeness"], "QuantityOfInterestCompleteness")
            ),
            unit=cls._string(fields["unit"]),
        )

    @classmethod
    def _decode_result(cls, value: _JsonValue, tag: str) -> _ScalarResult:
        names = (
            "identity",
            "quantity",
            "source_observation_set_result_identity",
            "evaluator_identity",
        )
        fields = cls._fields(
            value,
            tag,
            names
            + (
                ("value",)
                if tag == "ScalarQuantityOfInterestValue"
                else ("code", "detail")
            ),
        )
        identity = ResultObjectIdentity(
            cls._label(fields["identity"], "ResultObjectIdentity")
        )
        quantity = cls._decode_definition(fields["quantity"])
        source = ResultObjectIdentity(
            cls._label(
                fields["source_observation_set_result_identity"], "ResultObjectIdentity"
            )
        )
        evaluator = QuantityOfInterestEvaluatorIdentity(
            cls._label(
                fields["evaluator_identity"], "QuantityOfInterestEvaluatorIdentity"
            )
        )
        if tag == "ScalarQuantityOfInterestValue":
            return ScalarQuantityOfInterestValue(
                identity,
                quantity,
                source,
                evaluator,
                float.fromhex(cls._label(fields["value"], "float")),
            )
        return ScalarQuantityOfInterestEvaluationFailure(
            identity,
            quantity,
            source,
            evaluator,
            QuantityOfInterestEvaluationFailureCode(
                cls._label(fields["code"], "QuantityOfInterestEvaluationFailureCode")
            ),
            cls._string(fields["detail"]),
        )
