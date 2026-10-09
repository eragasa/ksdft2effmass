"""Finite design construction for retained optimizer convergence regression."""

import math

from .records import (
    OptimizerRegressionDecodedDocuments,
    OptimizerRegressionDesign,
)

_START_COUNT = 16
_EXPECTED_OBSERVATION_COUNT = 256
_EXPECTED_CONVERGED_COUNT = 196
_EXPECTED_CENSORED_COUNT = 60
_EXPECTED_PARAMETER_COUNT = 32
_EVIDENCE_STATUS = (
    "post-hoc exploratory censored regression of calculated synthetic non-DFT "
    "trajectories"
)
_CLAIM_BOUNDARY = (
    "This post-hoc model summarizes the retained finite trajectories. It does not "
    "alter native convergence, establish causality, prove optimizer convergence, or "
    "predict DFT behavior."
)
_MODEL_FIELDS = (
    "log-normal accelerated-failure-time",
    "total optimizer iterations to native convergence",
    "right-censored at the retained final iteration for trajectories without the "
    "native convergence statement",
    "configuration-by-optimizer group",
    "fixed effect for each deterministic start",
    "fixed_c31_p4_n23:baseline_preconditioned",
    "identity",
    "exploratory model-based 95% sandwich intervals clustered by the 16 deterministic "
    "starts; they have no population-sampling or physical-uncertainty interpretation",
    "time ratios above one indicate more iterations to native convergence; estimates "
    "are descriptive and not causal",
)


class OptimizerRegressionDesignConstructor:
    """Construct the declared finite design without inferring reference identities."""

    __slots__ = ()

    def execute(
        self, documents: OptimizerRegressionDecodedDocuments
    ) -> OptimizerRegressionDesign:
        """Validate retained identities and construct the immutable dense design.

        Parameters
        ----------
        documents
            Typed source and regression records.

        Returns
        -------
        OptimizerRegressionDesign
            Immutable aligned design rows, observations, clusters, and parameters.

        Raises
        ------
        TypeError
            If ``documents`` has an incompatible exact type.
        ValueError
            If an iteration time is nonpositive or a retained count is negative.
        AssertionError
            If identities, declared model metadata, counts, or design coverage differ.
        OverflowError
            If logarithm or finite arithmetic leaves binary64 range.
        MemoryError
            If Python cannot allocate the dense immutable design.
        """
        if type(documents) is not OptimizerRegressionDecodedDocuments:
            raise TypeError("documents must be OptimizerRegressionDecodedDocuments")
        source = documents.source_result
        regression = documents.regression_result
        model = regression.model
        if regression.evidence_status != _EVIDENCE_STATUS:
            raise AssertionError("regression evidence status changed")
        if regression.claim_boundary != _CLAIM_BOUNDARY:
            raise AssertionError("regression claim boundary changed")
        observed_model_fields = (
            model.family,
            model.response,
            model.censoring,
            model.category_effects,
            model.start_adjustment,
            model.reference_group,
            model.reference_start,
            model.intervals,
            model.interpretation,
        )
        if observed_model_fields != _MODEL_FIELDS:
            raise AssertionError("regression model declaration changed")

        endpoints = source.endpoints
        if len(endpoints) != _EXPECTED_OBSERVATION_COUNT:
            raise AssertionError("observation count changed")
        endpoint_identities = tuple(
            (item.configuration_id, item.arm, item.start_index, item.start_id)
            for item in endpoints
        )
        if len(endpoint_identities) != len(set(endpoint_identities)):
            raise AssertionError("endpoint identities must be unique")

        start_by_index: dict[int, str] = {}
        observed_group_keys: set[str] = set()
        for endpoint in endpoints:
            prior = start_by_index.setdefault(endpoint.start_index, endpoint.start_id)
            if prior != endpoint.start_id:
                raise AssertionError("start index and identity disagree")
            observed_group_keys.add(f"{endpoint.configuration_id}:{endpoint.arm}")
        category_keys = tuple(item.group_key for item in regression.category_estimates)
        if len(category_keys) != len(set(category_keys)):
            raise AssertionError("category identities must be unique")
        if set(category_keys) != observed_group_keys:
            raise AssertionError("category identities must match source groups")
        group_keys = category_keys
        expected_starts = tuple(range(_START_COUNT))
        if tuple(sorted(start_by_index)) != expected_starts:
            raise AssertionError("deterministic start indices changed")
        ordered_starts = tuple(start_by_index[index] for index in expected_starts)
        if len(ordered_starts) != len(set(ordered_starts)):
            raise AssertionError("deterministic start identities must be unique")
        if model.reference_group not in group_keys:
            raise AssertionError("declared reference group is unavailable")
        if model.reference_start not in ordered_starts:
            raise AssertionError("declared reference start is unavailable")

        expected_identity_set = {
            (group_key, index, start_id)
            for group_key in group_keys
            for index, start_id in enumerate(ordered_starts)
        }
        observed_identity_set = {
            (
                f"{endpoint.configuration_id}:{endpoint.arm}",
                endpoint.start_index,
                endpoint.start_id,
            )
            for endpoint in endpoints
        }
        if observed_identity_set != expected_identity_set:
            raise AssertionError("each group must contain every deterministic start")

        names = tuple(parameter.name for parameter in regression.parameters)
        expected_names = (
            "intercept",
            *(f"group:{key}" for key in group_keys if key != model.reference_group),
            *(
                f"start:{start_id}"
                for start_id in ordered_starts
                if start_id != model.reference_start
            ),
            "log_scale",
        )
        if names != expected_names or len(names) != len(set(names)):
            raise AssertionError("parameter identities or ordering changed")
        if len(names) != _EXPECTED_PARAMETER_COUNT:
            raise AssertionError("parameter count changed")
        parameters = tuple(parameter.value for parameter in regression.parameters)
        name_to_column = {name: index for index, name in enumerate(names[:-1])}
        start_to_cluster = {
            start_id: index for index, start_id in enumerate(ordered_starts)
        }

        rows: list[tuple[float, ...]] = []
        log_times: list[float] = []
        converged: list[bool] = []
        cluster_ids: list[int] = []
        for endpoint in endpoints:
            if endpoint.effective_total_iterations <= 0.0:
                raise ValueError("effective iteration counts must be positive")
            row = [0.0] * (len(parameters) - 1)
            row[0] = 1.0
            group_name = f"group:{endpoint.configuration_id}:{endpoint.arm}"
            start_name = f"start:{endpoint.start_id}"
            group_column = name_to_column.get(group_name)
            start_column = name_to_column.get(start_name)
            if group_column is not None:
                row[group_column] = 1.0
            if start_column is not None:
                row[start_column] = 1.0
            logged = math.log(endpoint.effective_total_iterations)
            if not math.isfinite(logged):
                raise OverflowError("log iteration count must be finite")
            rows.append(tuple(row))
            log_times.append(logged)
            converged.append(endpoint.effective_native_converged)
            cluster_ids.append(start_to_cluster[endpoint.start_id])

        converged_count = sum(converged)
        censored_count = len(converged) - converged_count
        declared_counts = (
            regression.observation_count,
            regression.converged_count,
            regression.right_censored_count,
            regression.parameter_count,
        )
        if any(type(value) is not int for value in declared_counts):
            raise TypeError("regression counts must be exact integers")
        if any(value < 0 for value in declared_counts):
            raise ValueError("regression counts must be nonnegative")
        if declared_counts != (
            _EXPECTED_OBSERVATION_COUNT,
            _EXPECTED_CONVERGED_COUNT,
            _EXPECTED_CENSORED_COUNT,
            _EXPECTED_PARAMETER_COUNT,
        ):
            raise AssertionError("retained aggregate counts changed")
        if converged_count != _EXPECTED_CONVERGED_COUNT:
            raise AssertionError("source converged count changed")
        if censored_count != _EXPECTED_CENSORED_COUNT:
            raise AssertionError("source right-censored count changed")

        return OptimizerRegressionDesign(
            parameter_names=names,
            parameters=parameters,
            design_rows=tuple(rows),
            log_times=tuple(log_times),
            converged=tuple(converged),
            cluster_ids=tuple(cluster_ids),
            group_keys=tuple(group_keys),
        )
