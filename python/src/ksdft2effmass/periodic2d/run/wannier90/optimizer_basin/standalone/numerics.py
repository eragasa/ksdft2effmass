"""Independent endpoint arithmetic for the standalone optimizer study."""

from .records import OptimizerStandaloneEndpoint, OptimizerStandaloneNativeEndpoint

_SPREAD_ABSOLUTE_TOLERANCE = 2.0e-8


class OptimizerStandaloneEndpointEvaluator:
    """Reconstruct one endpoint transition and terminal diagnostic class."""

    __slots__ = ()

    def execute(self, endpoint: OptimizerStandaloneEndpoint) -> str:
        """Validate retained spread algebra and return the reconstructed class.

        Parameters
        ----------
        endpoint
            One typed initial/continuation/effective endpoint transition.

        Returns
        -------
        str
            Reconstructed native-converged or exploratory terminal-trace class.

        Raises
        ------
        TypeError
            If ``endpoint`` is not the exact immutable endpoint record.
        AssertionError
            If spread algebra, route selection, iteration accumulation, or diagnostic
            classification disagrees with the retained fields.
        """
        if type(endpoint) is not OptimizerStandaloneEndpoint:
            raise TypeError("endpoint must be OptimizerStandaloneEndpoint")
        if not endpoint.initial_process_completed:
            raise AssertionError("incomplete initial process")
        self._check_spread_algebra(endpoint.initial_native_endpoint)
        self._check_spread_algebra(endpoint.effective_native_endpoint)
        if endpoint.continuation_applied == endpoint.initial_native_converged:
            raise AssertionError("continuation selection disagrees")
        if endpoint.continuation_applied:
            continuation = endpoint.continuation_native_endpoint
            if continuation is None or endpoint.continuation_native_converged is None:
                raise AssertionError("continued endpoint record is incomplete")
            self._check_spread_algebra(continuation)
            if continuation != endpoint.effective_native_endpoint:
                raise AssertionError("effective endpoint is not the continuation")
            if (
                endpoint.continuation_native_converged
                != endpoint.effective_native_converged
            ):
                raise AssertionError("continuation convergence status changed")
            expected_iterations = (
                endpoint.initial_native_endpoint.iterations + continuation.iterations
            )
        else:
            if (
                endpoint.continuation_native_endpoint is not None
                or endpoint.continuation_native_converged is not None
            ):
                raise AssertionError("unexpected continuation record")
            if endpoint.initial_native_endpoint != endpoint.effective_native_endpoint:
                raise AssertionError("effective endpoint is not the initial endpoint")
            expected_iterations = endpoint.initial_native_endpoint.iterations
        if endpoint.effective_total_iterations != expected_iterations:
            raise AssertionError("effective iteration accumulation disagrees")
        classification = self._classification(endpoint)
        if (
            classification
            != endpoint.effective_native_endpoint.diagnostic_classification
        ):
            raise AssertionError("diagnostic classification disagrees")
        return classification

    def _check_spread_algebra(
        self, endpoint: OptimizerStandaloneNativeEndpoint
    ) -> None:
        """Require retained total and gauge-dependent spread decompositions."""
        omega_tilde = endpoint.omega_d_cell_squared + endpoint.omega_od_cell_squared
        if (
            abs(endpoint.omega_tilde_cell_squared - omega_tilde)
            > _SPREAD_ABSOLUTE_TOLERANCE
        ):
            raise AssertionError("omega tilde decomposition disagrees")
        omega_total = endpoint.omega_i_cell_squared + omega_tilde
        if (
            abs(endpoint.omega_total_cell_squared - omega_total)
            > _SPREAD_ABSOLUTE_TOLERANCE
        ):
            raise AssertionError("omega total decomposition disagrees")

    def _classification(self, endpoint: OptimizerStandaloneEndpoint) -> str:
        """Apply the retained exploratory terminal-trace decision sequence."""
        if endpoint.effective_native_converged:
            return "native_converged"
        native = endpoint.effective_native_endpoint
        if (
            native.terminal_median_absolute_delta_spread <= 1.0e-8
            and native.terminal_median_rms_gradient <= 1.0e-3
        ):
            return "near_stationary_without_window_convergence"
        if native.terminal_spread_slope_per_iteration < -1.0e-8:
            return "continuing_descent_at_iteration_limit"
        if native.terminal_detrended_spread_rms > 1.0e-5:
            return "oscillatory_or_stalled"
        return "stalled_or_nondescent"
