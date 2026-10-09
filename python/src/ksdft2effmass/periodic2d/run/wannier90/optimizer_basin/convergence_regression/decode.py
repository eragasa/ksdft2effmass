"""Schema adaptation for optimizer convergence-regression documents."""

import json
import math
from typing import cast

from ksdft2effmass.serialization.json import StrictJsonDecoder

from .encoded_documents import Periodic2DOptimizerRegressionEncodedDocuments
from .records import (
    OptimizerRegressionCategoryEstimate,
    OptimizerRegressionDecodedDocuments,
    OptimizerRegressionModel,
    OptimizerRegressionParameter,
    OptimizerRegressionProbability,
    OptimizerRegressionResult,
    OptimizerRegressionSourceEndpoint,
    OptimizerRegressionSourceResult,
)

_SCHEMA_VERSION = 1

type LegacyOptimizerJsonValue = (
    None
    | bool
    | int
    | float
    | str
    | list[LegacyOptimizerJsonValue]
    | dict[str, LegacyOptimizerJsonValue]
)


class OptimizerRegressionLegacySourceDecoder:
    """Decode the retained source wire with its historical Infinity extension.

    The exact historical standalone result contains ``Infinity`` only in fields outside
    the row-054 endpoint contract. This decoder preserves that wire identity, rejects
    duplicate keys, and requires finite values for every endpoint field consumed by the
    regression. It does not reinterpret or expose the unconsumed nonfinite fields.
    """

    __slots__ = ("decoder",)

    def __init__(self) -> None:
        """Create one legacy adapter with strict primitive validation."""
        self.decoder = StrictJsonDecoder()

    def execute(self, payload: bytes) -> OptimizerRegressionSourceResult:
        """Return typed finite endpoint fields from the historical source wire.

        Parameters
        ----------
        payload
            Exact nonempty retained standalone-result bytes.

        Returns
        -------
        OptimizerRegressionSourceResult
            Closed immutable finite endpoint records.

        Raises
        ------
        TypeError
            If the wire, root, endpoint, or consumed field has an incompatible type.
        ValueError
            If UTF-8/JSON is malformed, keys repeat, or a consumed real is nonfinite.
        OverflowError
            If a consumed integer-to-binary64 conversion is not finite.
        KeyError
            If a required consumed field is absent.
        AssertionError
            If the source schema version is unsupported.
        MemoryError
            If parsing or record construction cannot allocate state.
        RecursionError
            If the historical document exceeds parser recursion depth.
        """
        if type(payload) is not bytes:
            raise TypeError("payload must be exact bytes")
        try:
            raw = cast(
                LegacyOptimizerJsonValue,
                json.loads(
                    payload.decode("utf-8"),
                    object_pairs_hook=self.object_from_pairs,
                    parse_constant=self.nonfinite_constant,
                ),
            )
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError("payload must be valid UTF-8 historical JSON") from error
        if type(raw) is not dict:
            raise TypeError("source root must be a JSON object")
        source_schema = self.decoder.integer(
            raw["schema_version"], "source.schema_version"
        )
        if source_schema != _SCHEMA_VERSION:
            raise AssertionError("source schema changed")
        endpoint_values = raw["endpoints"]
        if type(endpoint_values) is not list:
            raise TypeError("source.endpoints must be a JSON array")
        endpoints: list[OptimizerRegressionSourceEndpoint] = []
        for index, endpoint_value in enumerate(endpoint_values):
            if type(endpoint_value) is not dict:
                raise TypeError(f"source.endpoints[{index}] must be a JSON object")
            label = f"source.endpoints[{index}]"
            endpoints.append(
                OptimizerRegressionSourceEndpoint(
                    configuration_id=self.decoder.nonempty_string(
                        endpoint_value["configuration_id"],
                        f"{label}.configuration_id",
                    ),
                    arm=self.decoder.nonempty_string(
                        endpoint_value["arm"], f"{label}.arm"
                    ),
                    start_index=self.decoder.integer(
                        endpoint_value["start_index"], f"{label}.start_index"
                    ),
                    start_id=self.decoder.nonempty_string(
                        endpoint_value["start_id"], f"{label}.start_id"
                    ),
                    effective_total_iterations=self.decoder.real(
                        endpoint_value["effective_total_iterations"],
                        f"{label}.effective_total_iterations",
                    ),
                    effective_native_converged=self.decoder.boolean(
                        endpoint_value["effective_native_converged"],
                        f"{label}.effective_native_converged",
                    ),
                )
            )
        return OptimizerRegressionSourceResult(source_schema, tuple(endpoints))

    def object_from_pairs(
        self, pairs: list[tuple[str, LegacyOptimizerJsonValue]]
    ) -> dict[str, LegacyOptimizerJsonValue]:
        """Construct one historical object while rejecting duplicate keys.

        Parameters
        ----------
        pairs
            Parser-supplied ordered key/value pairs.

        Returns
        -------
        dict[str, LegacyOptimizerJsonValue]
            Unique-key historical object.

        Raises
        ------
        ValueError
            If a key occurs more than once.
        """
        result: dict[str, LegacyOptimizerJsonValue] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    def nonfinite_constant(self, value: str) -> float:
        """Map only historical Python-JSON nonfinite tokens for unconsumed fields.

        Parameters
        ----------
        value
            Parser-supplied ``Infinity``, ``-Infinity``, or ``NaN`` token.

        Returns
        -------
        float
            Corresponding nonfinite marker retained only in the temporary parse tree.

        Raises
        ------
        ValueError
            If the parser supplies another token.
        """
        if value == "Infinity":
            return math.inf
        if value == "-Infinity":
            return -math.inf
        if value == "NaN":
            return math.nan
        raise ValueError(f"unsupported historical constant: {value}")


class Periodic2DOptimizerRegressionDocumentDecoder:
    """Adapt strict JSON wires to closed immutable regression records."""

    __slots__ = ("decoder", "source_decoder")

    def __init__(self) -> None:
        """Create strict regression and historical source adapters."""
        self.decoder = StrictJsonDecoder()
        self.source_decoder = OptimizerRegressionLegacySourceDecoder()

    def execute(
        self, documents: Periodic2DOptimizerRegressionEncodedDocuments
    ) -> OptimizerRegressionDecodedDocuments:
        """Decode exact source and regression wires into immutable records.

        Parameters
        ----------
        documents
            Exact standalone-result and convergence-regression wires.

        Returns
        -------
        OptimizerRegressionDecodedDocuments
            Closed immutable records containing verifier-owned fields.

        Raises
        ------
        TypeError
            If a wire or field has an incompatible exact representation.
        ValueError
            If JSON, finite-real, nonempty-string, or digest syntax is invalid.
        OverflowError
            If an integer-to-binary64 conversion is not finite.
        KeyError
            If a required verifier-owned field is absent.
        AssertionError
            If either document declares an unsupported schema version.
        MemoryError
            If decoding or record adaptation cannot allocate required state.
        RecursionError
            If a document exceeds parser recursion depth.
        """
        if type(documents) is not Periodic2DOptimizerRegressionEncodedDocuments:
            raise TypeError(
                "documents must be Periodic2DOptimizerRegressionEncodedDocuments"
            )
        source_result = self.source_decoder.execute(documents.standalone_result_payload)
        regression = self.decoder.document(documents.regression_payload)
        regression_schema = self.decoder.integer(
            regression["schema_version"], "regression.schema_version"
        )
        if regression_schema != _SCHEMA_VERSION:
            raise AssertionError("regression schema changed")

        model_value = regression["model"]
        if type(model_value) is not dict:
            raise TypeError("regression.model must be a JSON object")
        model = OptimizerRegressionModel(
            family=self.decoder.nonempty_string(
                model_value["family"], "regression.model.family"
            ),
            response=self.decoder.nonempty_string(
                model_value["response"], "regression.model.response"
            ),
            censoring=self.decoder.nonempty_string(
                model_value["censoring"], "regression.model.censoring"
            ),
            category_effects=self.decoder.nonempty_string(
                model_value["category_effects"],
                "regression.model.category_effects",
            ),
            start_adjustment=self.decoder.nonempty_string(
                model_value["start_adjustment"],
                "regression.model.start_adjustment",
            ),
            reference_group=self.decoder.nonempty_string(
                model_value["reference_group"], "regression.model.reference_group"
            ),
            reference_start=self.decoder.nonempty_string(
                model_value["reference_start"], "regression.model.reference_start"
            ),
            intervals=self.decoder.nonempty_string(
                model_value["intervals"], "regression.model.intervals"
            ),
            interpretation=self.decoder.nonempty_string(
                model_value["interpretation"], "regression.model.interpretation"
            ),
        )

        parameter_values = regression["parameters"]
        if type(parameter_values) is not list:
            raise TypeError("regression.parameters must be a JSON array")
        parameters: list[OptimizerRegressionParameter] = []
        for index, parameter_value in enumerate(parameter_values):
            if type(parameter_value) is not dict:
                raise TypeError(f"regression.parameters[{index}] must be a JSON object")
            label = f"regression.parameters[{index}]"
            parameters.append(
                OptimizerRegressionParameter(
                    name=self.decoder.nonempty_string(
                        parameter_value["name"], f"{label}.name"
                    ),
                    value=self.decoder.real(parameter_value["value"], f"{label}.value"),
                )
            )

        category_values = regression["category_estimates"]
        if type(category_values) is not list:
            raise TypeError("regression.category_estimates must be a JSON array")
        categories: list[OptimizerRegressionCategoryEstimate] = []
        for category_index, category_value in enumerate(category_values):
            if type(category_value) is not dict:
                raise TypeError(
                    "regression.category_estimates"
                    f"[{category_index}] must be a JSON object"
                )
            label = f"regression.category_estimates[{category_index}]"
            interval_value = category_value["time_ratio_95_percent_interval"]
            if type(interval_value) is not list:
                raise TypeError(
                    f"{label}.time_ratio_95_percent_interval must be an array"
                )
            interval = tuple(
                self.decoder.real(item, f"{label}.time_ratio_95_percent_interval")
                for item in interval_value
            )
            if len(interval) != 2:
                raise ValueError(
                    f"{label}.time_ratio_95_percent_interval must contain two values"
                )
            probability_values = category_value["predicted_convergence_probability"]
            if type(probability_values) is not list:
                raise TypeError(
                    f"{label}.predicted_convergence_probability must be an array"
                )
            probabilities: list[OptimizerRegressionProbability] = []
            for probability_index, probability_value in enumerate(probability_values):
                if type(probability_value) is not dict:
                    raise TypeError(
                        f"{label}.predicted_convergence_probability"
                        f"[{probability_index}] must be an object"
                    )
                probability_label = (
                    f"{label}.predicted_convergence_probability[{probability_index}]"
                )
                probabilities.append(
                    OptimizerRegressionProbability(
                        iterations=self.decoder.integer(
                            probability_value["iterations"],
                            f"{probability_label}.iterations",
                        ),
                        probability=self.decoder.real(
                            probability_value["probability"],
                            f"{probability_label}.probability",
                        ),
                    )
                )
            categories.append(
                OptimizerRegressionCategoryEstimate(
                    group_key=self.decoder.nonempty_string(
                        category_value["group_key"], f"{label}.group_key"
                    ),
                    label=self.decoder.nonempty_string(
                        category_value["label"], f"{label}.label"
                    ),
                    converged_count=self.decoder.integer(
                        category_value["converged_count"],
                        f"{label}.converged_count",
                    ),
                    right_censored_count=self.decoder.integer(
                        category_value["right_censored_count"],
                        f"{label}.right_censored_count",
                    ),
                    log_time_ratio=self.decoder.real(
                        category_value["log_time_ratio"],
                        f"{label}.log_time_ratio",
                    ),
                    clustered_standard_error=self.decoder.real(
                        category_value["clustered_standard_error"],
                        f"{label}.clustered_standard_error",
                    ),
                    time_ratio=self.decoder.real(
                        category_value["time_ratio"], f"{label}.time_ratio"
                    ),
                    time_ratio_95_percent_interval=(interval[0], interval[1]),
                    adjusted_median_iterations=self.decoder.real(
                        category_value["adjusted_median_iterations"],
                        f"{label}.adjusted_median_iterations",
                    ),
                    predicted_convergence_probability=tuple(probabilities),
                )
            )

        result = OptimizerRegressionResult(
            schema_version=regression_schema,
            evidence_status=self.decoder.nonempty_string(
                regression["evidence_status"], "regression.evidence_status"
            ),
            source_result_path=self.decoder.nonempty_string(
                regression["source_result_path"], "regression.source_result_path"
            ),
            source_result_sha256=self.decoder.sha256(
                regression["source_result_sha256"],
                "regression.source_result_sha256",
            ),
            model=model,
            observation_count=self.decoder.integer(
                regression["observation_count"], "regression.observation_count"
            ),
            converged_count=self.decoder.integer(
                regression["converged_count"], "regression.converged_count"
            ),
            right_censored_count=self.decoder.integer(
                regression["right_censored_count"],
                "regression.right_censored_count",
            ),
            parameter_count=self.decoder.integer(
                regression["parameter_count"], "regression.parameter_count"
            ),
            parameters=tuple(parameters),
            negative_log_likelihood=self.decoder.real(
                regression["negative_log_likelihood"],
                "regression.negative_log_likelihood",
            ),
            gradient_infinity_norm=self.decoder.real(
                regression["gradient_infinity_norm"],
                "regression.gradient_infinity_norm",
            ),
            hessian_condition_number=self.decoder.real(
                regression["hessian_condition_number"],
                "regression.hessian_condition_number",
            ),
            log_time_scale=self.decoder.real(
                regression["log_time_scale"], "regression.log_time_scale"
            ),
            time_scale=self.decoder.real(
                regression["time_scale"], "regression.time_scale"
            ),
            category_estimates=tuple(categories),
            claim_boundary=self.decoder.nonempty_string(
                regression["claim_boundary"], "regression.claim_boundary"
            ),
        )
        return OptimizerRegressionDecodedDocuments(
            source_result=source_result,
            regression_result=result,
        )
