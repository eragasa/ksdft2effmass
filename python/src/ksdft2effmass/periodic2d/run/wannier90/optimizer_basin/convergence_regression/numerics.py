"""Independent dense numerics for retained censored convergence regression."""

import math

import numpy as np
from scipy.special import log_ndtr  # type: ignore[import-untyped]

from .records import (
    OptimizerRegressionEvaluationRequest,
    OptimizerRegressionLikelihood,
    OptimizerRegressionNumericalReconstruction,
)

_HESSIAN_RELATIVE_STEP = 1.0e-5
_PSEUDOINVERSE_RELATIVE_CUTOFF = 1.0e-12


class CensoredLogNormalObservationScoreEvaluator:
    """Evaluate per-observation scores for the declared log-normal model."""

    __slots__ = ()

    def execute(
        self, request: OptimizerRegressionEvaluationRequest
    ) -> tuple[tuple[float, ...], ...]:
        """Return one finite score row per retained observation.

        Parameters
        ----------
        request
            Immutable design and aligned finite parameter vector.

        Returns
        -------
        tuple[tuple[float, ...], ...]
            Dense finite score matrix in observation/parameter order.

        Raises
        ------
        TypeError
            If ``request`` has an incompatible exact type.
        OverflowError
            If exponential or score arithmetic leaves finite binary64 range.
        MemoryError
            If dense arrays cannot be allocated.

        Notes
        -----
        Storage scales as :math:`O(np)` for ``n`` observations and ``p`` parameters.
        No arbitrary size cap is imposed.
        """
        if type(request) is not OptimizerRegressionEvaluationRequest:
            raise TypeError("request must be OptimizerRegressionEvaluationRequest")
        design = np.asarray(request.design.design_rows, dtype=np.float64)
        log_times = np.asarray(request.design.log_times, dtype=np.float64)
        converged = np.asarray(request.design.converged, dtype=np.bool_)
        parameters = np.asarray(request.parameters, dtype=np.float64)
        try:
            scale = math.exp(float(parameters[-1]))
        except OverflowError as error:
            raise OverflowError("log-time scale left binary64 range") from error
        residual = (log_times - design @ parameters[:-1]) / scale
        rows = np.zeros((len(log_times), len(parameters)), dtype=np.float64)
        rows[converged, :-1] = -residual[converged, None] * design[converged] / scale
        rows[converged, -1] = 1.0 - residual[converged] ** 2
        censored = residual[~converged]
        mills = np.exp(
            -0.5 * censored**2 - 0.5 * math.log(2.0 * math.pi) - log_ndtr(-censored)
        )
        rows[~converged, :-1] = -mills[:, None] * design[~converged] / scale
        rows[~converged, -1] = -mills * censored
        if not bool(np.all(np.isfinite(rows))):
            raise OverflowError("observation scores must remain finite")
        return tuple(tuple(float(value) for value in row) for row in rows)


class CensoredLogNormalLikelihoodEvaluator:
    """Evaluate the right-censored negative likelihood and gradient."""

    __slots__ = ("score_evaluator",)

    def __init__(self) -> None:
        """Create one evaluator with an instantiated score collaborator."""
        self.score_evaluator = CensoredLogNormalObservationScoreEvaluator()

    def execute(
        self, request: OptimizerRegressionEvaluationRequest
    ) -> OptimizerRegressionLikelihood:
        """Return the finite negative log likelihood and score sum.

        Parameters
        ----------
        request
            Immutable design and aligned finite parameter vector.

        Returns
        -------
        OptimizerRegressionLikelihood
            Finite scalar loss and parameter-order gradient.

        Raises
        ------
        TypeError
            If ``request`` has an incompatible exact type.
        OverflowError
            If scale, likelihood, or score arithmetic becomes nonfinite.
        MemoryError
            If dense arrays cannot be allocated.

        Notes
        -----
        Dense evaluation scales as :math:`O(np)` in time and storage.
        """
        if type(request) is not OptimizerRegressionEvaluationRequest:
            raise TypeError("request must be OptimizerRegressionEvaluationRequest")
        design = np.asarray(request.design.design_rows, dtype=np.float64)
        log_times = np.asarray(request.design.log_times, dtype=np.float64)
        converged = np.asarray(request.design.converged, dtype=np.bool_)
        parameters = np.asarray(request.parameters, dtype=np.float64)
        try:
            scale = math.exp(float(parameters[-1]))
        except OverflowError as error:
            raise OverflowError("log-time scale left binary64 range") from error
        residual = (log_times - design @ parameters[:-1]) / scale
        event_loss = (
            float(parameters[-1])
            + 0.5 * residual[converged] ** 2
            + 0.5 * math.log(2.0 * math.pi)
        )
        censored_loss = -log_ndtr(-residual[~converged])
        loss = float(np.sum(event_loss) + np.sum(censored_loss))
        scores = np.asarray(self.score_evaluator.execute(request), dtype=np.float64)
        gradient = np.asarray(np.sum(scores, axis=0), dtype=np.float64)
        if not math.isfinite(loss) or not bool(np.all(np.isfinite(gradient))):
            raise OverflowError("likelihood evaluation must remain finite")
        return OptimizerRegressionLikelihood(
            negative_log_likelihood=loss,
            gradient=tuple(float(value) for value in gradient),
        )


class CensoredLogNormalClusteredCovarianceConstructor:
    """Construct the retained start-clustered sandwich covariance independently."""

    __slots__ = ("likelihood_evaluator", "score_evaluator")

    def __init__(self) -> None:
        """Create one constructor with likelihood and score collaborators."""
        self.likelihood_evaluator = CensoredLogNormalLikelihoodEvaluator()
        self.score_evaluator = CensoredLogNormalObservationScoreEvaluator()

    def execute(
        self, request: OptimizerRegressionEvaluationRequest
    ) -> OptimizerRegressionNumericalReconstruction:
        """Reconstruct likelihood, finite-difference Hessian, and covariance.

        Parameters
        ----------
        request
            Immutable design and retained fitted parameter vector.

        Returns
        -------
        OptimizerRegressionNumericalReconstruction
            Finite likelihood, gradient, covariance, and Hessian condition number.

        Raises
        ------
        TypeError
            If ``request`` has an incompatible exact type.
        ValueError
            If cluster or finite-sample dimensions make the correction undefined.
        OverflowError
            If finite-difference or matrix arithmetic becomes nonfinite.
        numpy.linalg.LinAlgError
            If pseudoinversion or condition estimation fails.
        MemoryError
            If dense Hessian, score, or covariance arrays cannot be allocated.

        Notes
        -----
        For ``n`` observations and ``p`` parameters, dense storage scales as
        :math:`O(np+p^2)` and repeated gradient evaluation scales as
        :math:`O(np^2)`. No arbitrary size cap is imposed.
        """
        if type(request) is not OptimizerRegressionEvaluationRequest:
            raise TypeError("request must be OptimizerRegressionEvaluationRequest")
        parameters = np.asarray(request.parameters, dtype=np.float64)
        dimension = len(parameters)
        hessian = np.empty((dimension, dimension), dtype=np.float64)
        for column in range(dimension):
            step = _HESSIAN_RELATIVE_STEP * max(1.0, abs(float(parameters[column])))
            plus = parameters.copy()
            minus = parameters.copy()
            plus[column] += step
            minus[column] -= step
            plus_likelihood = self.likelihood_evaluator.execute(
                OptimizerRegressionEvaluationRequest(
                    request.design, tuple(float(value) for value in plus)
                )
            )
            minus_likelihood = self.likelihood_evaluator.execute(
                OptimizerRegressionEvaluationRequest(
                    request.design, tuple(float(value) for value in minus)
                )
            )
            hessian[:, column] = (
                np.asarray(plus_likelihood.gradient, dtype=np.float64)
                - np.asarray(minus_likelihood.gradient, dtype=np.float64)
            ) / (2.0 * step)
        hessian = 0.5 * (hessian + hessian.T)
        inverse = np.linalg.pinv(hessian, rcond=_PSEUDOINVERSE_RELATIVE_CUTOFF)
        scores = np.asarray(self.score_evaluator.execute(request), dtype=np.float64)
        cluster_ids = np.asarray(request.design.cluster_ids, dtype=np.int64)
        cluster_values = np.unique(cluster_ids)
        clusters = np.stack(
            [
                np.sum(scores[cluster_ids == cluster], axis=0)
                for cluster in cluster_values
            ]
        )
        cluster_count = clusters.shape[0]
        observation_count = len(request.design.log_times)
        if cluster_count <= 1 or observation_count <= dimension:
            raise ValueError("clustered covariance correction is undefined")
        correction = (cluster_count / (cluster_count - 1.0)) * (
            (observation_count - 1.0) / (observation_count - dimension)
        )
        covariance = correction * inverse @ (clusters.T @ clusters) @ inverse
        condition = float(np.linalg.cond(hessian))
        retained_likelihood = self.likelihood_evaluator.execute(request)
        if not bool(np.all(np.isfinite(covariance))) or not math.isfinite(condition):
            raise OverflowError("covariance reconstruction must remain finite")
        return OptimizerRegressionNumericalReconstruction(
            negative_log_likelihood=retained_likelihood.negative_log_likelihood,
            gradient=retained_likelihood.gradient,
            covariance=tuple(
                tuple(float(value) for value in row) for row in covariance
            ),
            hessian_condition_number=condition,
        )
