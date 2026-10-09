"""Closed immutable records for optimizer convergence-regression verification."""

import math
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OptimizerRegressionSourceEndpoint:
    """Represent one source endpoint used by the censored regression.

    Parameters
    ----------
    configuration_id, arm
        Exact retained configuration and optimizer-arm identities.
    start_index, start_id
        Exact deterministic-start index and identity.
    effective_total_iterations
        Positive retained iteration count used as event or censoring time.
    effective_native_converged
        Native convergence indicator; ``False`` denotes right censoring.
    """

    configuration_id: str
    arm: str
    start_index: int
    start_id: str
    effective_total_iterations: float
    effective_native_converged: bool


@dataclass(frozen=True, slots=True)
class OptimizerRegressionSourceResult:
    """Represent verifier-owned fields from the standalone source result.

    Parameters
    ----------
    schema_version
        Exact retained source schema version.
    endpoints
        Immutable endpoint sequence in retained order.
    """

    schema_version: int
    endpoints: tuple[OptimizerRegressionSourceEndpoint, ...]


@dataclass(frozen=True, slots=True)
class OptimizerRegressionModel:
    """Represent declared statistical-model identity and interpretation fields.

    Parameters
    ----------
    family, response, censoring
        Exact retained model family, response, and censoring declarations.
    category_effects, start_adjustment
        Exact retained design-column declarations.
    reference_group, reference_start
        Explicit reference identities; neither is inferred from ordering.
    intervals, interpretation
        Exact retained limitations and coefficient interpretation.
    """

    family: str
    response: str
    censoring: str
    category_effects: str
    start_adjustment: str
    reference_group: str
    reference_start: str
    intervals: str
    interpretation: str


@dataclass(frozen=True, slots=True)
class OptimizerRegressionParameter:
    """Represent one named finite fitted parameter.

    Parameters
    ----------
    name
        Exact retained parameter identity.
    value
        Finite binary64 parameter value.
    """

    name: str
    value: float


@dataclass(frozen=True, slots=True)
class OptimizerRegressionProbability:
    """Represent one finite-iteration convergence probability.

    Parameters
    ----------
    iterations
        Positive iteration checkpoint.
    probability
        Finite retained probability at that checkpoint.
    """

    iterations: int
    probability: float


@dataclass(frozen=True, slots=True)
class OptimizerRegressionCategoryEstimate:
    """Represent retained diagnostics for one configuration/optimizer group.

    Parameters
    ----------
    group_key, label
        Exact retained group identity and display label.
    converged_count, right_censored_count
        Retained event and censoring counts.
    log_time_ratio, clustered_standard_error, time_ratio
        Finite fitted coefficient diagnostics.
    time_ratio_95_percent_interval
        Exact two-bound exploratory model interval.
    adjusted_median_iterations
        Finite adjusted median iteration count.
    predicted_convergence_probability
        Ordered finite-checkpoint probability records.
    """

    group_key: str
    label: str
    converged_count: int
    right_censored_count: int
    log_time_ratio: float
    clustered_standard_error: float
    time_ratio: float
    time_ratio_95_percent_interval: tuple[float, float]
    adjusted_median_iterations: float
    predicted_convergence_probability: tuple[OptimizerRegressionProbability, ...]


@dataclass(frozen=True, slots=True)
class OptimizerRegressionResult:
    """Represent verifier-owned retained regression fields.

    Parameters
    ----------
    schema_version
        Exact retained regression schema version.
    evidence_status
        Exact retained exploratory-evidence status.
    source_result_path
        Preserved source path declaration; not filesystem authority.
    source_result_sha256
        Declared identity of the encapsulated source-result bytes.
    model
        Explicit statistical-model declaration.
    observation_count, converged_count, right_censored_count, parameter_count
        Retained aggregate counts.
    parameters
        Ordered named fitted parameters.
    negative_log_likelihood, gradient_infinity_norm, hessian_condition_number
        Finite retained reconstruction diagnostics.
    log_time_scale, time_scale
        Finite retained scale parameter in logarithmic and direct forms.
    category_estimates
        Ordered retained category diagnostics.
    claim_boundary
        Exact retained scientific limitation statement.
    """

    schema_version: int
    evidence_status: str
    source_result_path: str
    source_result_sha256: str
    model: OptimizerRegressionModel
    observation_count: int
    converged_count: int
    right_censored_count: int
    parameter_count: int
    parameters: tuple[OptimizerRegressionParameter, ...]
    negative_log_likelihood: float
    gradient_infinity_norm: float
    hessian_condition_number: float
    log_time_scale: float
    time_scale: float
    category_estimates: tuple[OptimizerRegressionCategoryEstimate, ...]
    claim_boundary: str


@dataclass(frozen=True, slots=True)
class OptimizerRegressionDecodedDocuments:
    """Pair typed source and regression records from exact encoded wires.

    Parameters
    ----------
    source_result
        Typed verifier-owned standalone-result fields.
    regression_result
        Typed verifier-owned convergence-regression fields.
    """

    source_result: OptimizerRegressionSourceResult
    regression_result: OptimizerRegressionResult


@dataclass(frozen=True, slots=True)
class OptimizerRegressionDesign:
    """Represent the immutable finite regression design and observations.

    Parameters
    ----------
    parameter_names, parameters
        Exact ordered parameter identities and finite values.
    design_rows
        Immutable dense design rows.
    log_times
        Natural logarithms of positive effective iteration counts.
    converged
        Native event indicators aligned with rows.
    cluster_ids
        Deterministic-start cluster indices aligned with rows.
    group_keys
        First-occurrence ordered configuration/optimizer identities.
    """

    parameter_names: tuple[str, ...]
    parameters: tuple[float, ...]
    design_rows: tuple[tuple[float, ...], ...]
    log_times: tuple[float, ...]
    converged: tuple[bool, ...]
    cluster_ids: tuple[int, ...]
    group_keys: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class OptimizerRegressionEvaluationRequest:
    """Request numerical evaluation at one finite parameter vector.

    Parameters
    ----------
    design
        Immutable retained finite design.
    parameters
        Finite binary64 vector aligned with design columns plus log scale.

    Raises
    ------
    TypeError
        If either field has an incompatible exact representation.
    ValueError
        If parameter length differs or a value is nonfinite.
    """

    design: OptimizerRegressionDesign
    parameters: tuple[float, ...]

    def __post_init__(self) -> None:
        """Delegate exact type, shape, and finite-value checks."""
        self._check_args_design()
        self._check_args_parameters()

    def _check_args_design(self) -> None:
        """Require the exact immutable design record."""
        if type(self.design) is not OptimizerRegressionDesign:
            raise TypeError("design must be OptimizerRegressionDesign")

    def _check_args_parameters(self) -> None:
        """Require an aligned exact tuple of finite binary64 values."""
        if type(self.parameters) is not tuple:
            raise TypeError("parameters must be an exact tuple")
        if any(type(value) is not float for value in self.parameters):
            raise TypeError("parameters must contain exact binary64 floats")
        if any(not math.isfinite(value) for value in self.parameters):
            raise ValueError("parameters must be finite")
        if len(self.parameters) != len(self.design.parameters):
            raise ValueError("parameter count must match the design")


@dataclass(frozen=True, slots=True)
class OptimizerRegressionLikelihood:
    """Represent one reconstructed likelihood and score sum.

    Parameters
    ----------
    negative_log_likelihood
        Finite reconstructed negative log likelihood.
    gradient
        Finite reconstructed score-sum vector.
    """

    negative_log_likelihood: float
    gradient: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class OptimizerRegressionNumericalReconstruction:
    """Represent independently reconstructed likelihood and covariance values.

    Parameters
    ----------
    negative_log_likelihood
        Reconstructed finite negative log likelihood.
    gradient
        Reconstructed finite score-sum vector.
    covariance
        Reconstructed finite start-clustered sandwich covariance matrix.
    hessian_condition_number
        Reconstructed finite Hessian condition number.
    """

    negative_log_likelihood: float
    gradient: tuple[float, ...]
    covariance: tuple[tuple[float, ...], ...]
    hessian_condition_number: float
