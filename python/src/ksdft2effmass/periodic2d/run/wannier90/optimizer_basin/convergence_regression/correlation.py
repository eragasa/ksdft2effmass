"""Structural and numerical correlation for optimizer convergence regression."""

import math
from dataclasses import dataclass

from scipy.special import ndtr  # type: ignore[import-untyped]

from .design import OptimizerRegressionDesignConstructor
from .numerics import CensoredLogNormalClusteredCovarianceConstructor
from .records import (
    OptimizerRegressionDecodedDocuments,
    OptimizerRegressionEvaluationRequest,
)

_LIKELIHOOD_TOLERANCE = 1.0e-9
_GRADIENT_TOLERANCE = 1.0e-9
_MAXIMUM_RETAINED_GRADIENT_NORM = 2.0e-4
_CONDITION_TOLERANCE = 1.0e-7
_SCALE_TOLERANCE = 1.0e-12
_RATIO_TOLERANCE = 1.0e-12
_ESTIMATE_TOLERANCE = 1.0e-9
_PROBABILITY_TOLERANCE = 1.0e-12
_PROBABILITY_CHECKPOINTS = (500, 1000, 2500, 5000, 10000, 20000)


@dataclass(frozen=True, slots=True)
class OptimizerRegressionCorrelationResult:
    """Report exact aggregate counts after successful correlation.

    Parameters
    ----------
    observation_count, converged_count, right_censored_count, parameter_count
        Exact nonnegative retained counts reconstructed from typed source records.

    Raises
    ------
    TypeError
        If a count is not an exact built-in integer.
    ValueError
        If a count is negative.
    """

    observation_count: int
    converged_count: int
    right_censored_count: int
    parameter_count: int

    def __post_init__(self) -> None:
        """Delegate exact integer and nonnegative checks."""
        self._check_args_counts()

    def _check_args_counts(self) -> None:
        """Require exact nonnegative built-in integer counts."""
        for name, value in (
            ("observation_count", self.observation_count),
            ("converged_count", self.converged_count),
            ("right_censored_count", self.right_censored_count),
            ("parameter_count", self.parameter_count),
        ):
            if type(value) is not int:
                raise TypeError(f"{name} must be an integer")
            if value < 0:
                raise ValueError(f"{name} must be nonnegative")


class Periodic2DOptimizerRegressionCorrelator:
    """Reconstruct and correlate all retained finite regression diagnostics."""

    __slots__ = ("covariance_constructor", "design_constructor")

    def __init__(self) -> None:
        """Create one correlator with explicit design and numerical Actions."""
        self.design_constructor = OptimizerRegressionDesignConstructor()
        self.covariance_constructor = CensoredLogNormalClusteredCovarianceConstructor()

    def execute(
        self, documents: OptimizerRegressionDecodedDocuments
    ) -> OptimizerRegressionCorrelationResult:
        """Verify retained likelihood, covariance, category, and probability values.

        Parameters
        ----------
        documents
            Typed source and regression records.

        Returns
        -------
        OptimizerRegressionCorrelationResult
            Reconstructed exact aggregate counts.

        Raises
        ------
        TypeError
            If ``documents`` has an incompatible exact type.
        ValueError
            If probability, interval, or covariance dimensions are invalid.
        AssertionError
            If any retained identity, count, or numerical diagnostic disagrees.
        OverflowError
            If exponential or numerical reconstruction leaves binary64 range.
        numpy.linalg.LinAlgError
            If dense pseudoinversion or condition estimation fails.
        MemoryError
            If dense regression arrays cannot be allocated.
        """
        if type(documents) is not OptimizerRegressionDecodedDocuments:
            raise TypeError("documents must be OptimizerRegressionDecodedDocuments")
        design = self.design_constructor.execute(documents)
        regression = documents.regression_result
        source = documents.source_result
        reconstruction = self.covariance_constructor.execute(
            OptimizerRegressionEvaluationRequest(design, design.parameters)
        )
        if (
            abs(
                reconstruction.negative_log_likelihood
                - regression.negative_log_likelihood
            )
            > _LIKELIHOOD_TOLERANCE
        ):
            raise AssertionError("negative log likelihood changed")
        gradient_norm = max(abs(value) for value in reconstruction.gradient)
        if abs(gradient_norm - regression.gradient_infinity_norm) > _GRADIENT_TOLERANCE:
            raise AssertionError("gradient infinity norm changed")
        if gradient_norm > _MAXIMUM_RETAINED_GRADIENT_NORM:
            raise AssertionError("regression gradient is too large")
        if (
            abs(
                reconstruction.hessian_condition_number
                - regression.hessian_condition_number
            )
            > _CONDITION_TOLERANCE
        ):
            raise AssertionError("Hessian condition number changed")

        log_scale = design.parameters[-1]
        if abs(log_scale - regression.log_time_scale) > _SCALE_TOLERANCE:
            raise AssertionError("log-time scale changed")
        try:
            scale = math.exp(log_scale)
        except OverflowError as error:
            raise OverflowError("time scale left binary64 range") from error
        if abs(scale - regression.time_scale) > _SCALE_TOLERANCE:
            raise AssertionError("time scale changed")

        name_to_column = {
            name: index for index, name in enumerate(design.parameter_names[:-1])
        }
        start_effects = [
            design.parameters[index]
            for name, index in name_to_column.items()
            if name.startswith("start:")
        ]
        mean_start_effect = sum(start_effects) / 16.0
        covariance = reconstruction.covariance
        endpoints = source.endpoints
        for estimate in regression.category_estimates:
            coefficient_index = name_to_column.get(f"group:{estimate.group_key}")
            log_ratio = (
                0.0
                if coefficient_index is None
                else design.parameters[coefficient_index]
            )
            if abs(estimate.log_time_ratio - log_ratio) > _RATIO_TOLERANCE:
                raise AssertionError("log time ratio changed")
            try:
                time_ratio = math.exp(log_ratio)
            except OverflowError as error:
                raise OverflowError("time ratio left binary64 range") from error
            if abs(estimate.time_ratio - time_ratio) > _RATIO_TOLERANCE:
                raise AssertionError("time ratio changed")
            standard_error = (
                0.0
                if coefficient_index is None
                else math.sqrt(
                    max(covariance[coefficient_index][coefficient_index], 0.0)
                )
            )
            if (
                abs(estimate.clustered_standard_error - standard_error)
                > _ESTIMATE_TOLERANCE
            ):
                raise AssertionError("clustered standard error changed")
            lower = math.exp(log_ratio - 1.96 * standard_error)
            upper = math.exp(log_ratio + 1.96 * standard_error)
            retained_lower, retained_upper = estimate.time_ratio_95_percent_interval
            if abs(retained_lower - lower) > _ESTIMATE_TOLERANCE:
                raise AssertionError("time-ratio lower interval changed")
            if abs(retained_upper - upper) > _ESTIMATE_TOLERANCE:
                raise AssertionError("time-ratio upper interval changed")

            selected = tuple(
                endpoint
                for endpoint in endpoints
                if f"{endpoint.configuration_id}:{endpoint.arm}" == estimate.group_key
            )
            converged_count = sum(
                endpoint.effective_native_converged for endpoint in selected
            )
            censored_count = len(selected) - converged_count
            if estimate.converged_count != converged_count:
                raise AssertionError("category converged count changed")
            if estimate.right_censored_count != censored_count:
                raise AssertionError("category right-censored count changed")
            adjusted = design.parameters[0] + log_ratio + mean_start_effect
            adjusted_median = math.exp(adjusted)
            if (
                abs(estimate.adjusted_median_iterations - adjusted_median)
                > _ESTIMATE_TOLERANCE
            ):
                raise AssertionError("adjusted median iterations changed")
            checkpoints = tuple(
                probability.iterations
                for probability in estimate.predicted_convergence_probability
            )
            if checkpoints != _PROBABILITY_CHECKPOINTS:
                raise AssertionError("probability checkpoints changed")
            for probability in estimate.predicted_convergence_probability:
                if not 0.0 <= probability.probability <= 1.0:
                    raise ValueError("retained probability must lie in [0, 1]")
                expected = float(
                    ndtr((math.log(probability.iterations) - adjusted) / scale)
                )
                if abs(probability.probability - expected) > _PROBABILITY_TOLERANCE:
                    raise AssertionError("predicted convergence probability changed")

        converged_count = sum(
            endpoint.effective_native_converged for endpoint in endpoints
        )
        return OptimizerRegressionCorrelationResult(
            observation_count=len(endpoints),
            converged_count=converged_count,
            right_censored_count=len(endpoints) - converged_count,
            parameter_count=len(design.parameters),
        )
