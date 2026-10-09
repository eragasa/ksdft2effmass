"""Common-estimator refinement verification for optimizer reanalysis."""

from dataclasses import dataclass
from pathlib import Path

from .authentication import (
    OptimizerReanalysisRepositorySourceAuthenticationRequest,
    OptimizerReanalysisRepositorySourceAuthenticator,
)
from .numerics import PeriodicCenterSetComparator, PeriodicCenterSetComparisonRequest
from .records import OptimizerReanalysisEndpoint, OptimizerReanalysisResult

_FFT_REFINEMENT_SIZES = (256, 512, 1024)
_REFINEMENT_TOLERANCE = 1.0e-15
_RELATIVE_ERROR_DENOMINATOR_FLOOR = 1.0e-15
_ESTIMATOR_FIXTURE_DIRECTORY = (
    "calculations/research-monograph/periodic-2d-optimizer-basin/estimator-inputs"
)


@dataclass(frozen=True, slots=True)
class OptimizerReanalysisRefinementVerificationRequest:
    """Request retained common-estimator refinement verification.

    Parameters
    ----------
    result
        Exact decoded offline-reanalysis result.
    correlated_endpoints
        Immutable endpoints already correlated with the source result.
    repository_root
        Absolute root containing maintained estimator fixtures.
    """

    result: OptimizerReanalysisResult
    correlated_endpoints: tuple[OptimizerReanalysisEndpoint, ...]
    repository_root: Path

    def __post_init__(self) -> None:
        """Validate exact decoded ownership, immutable endpoints, and root location."""
        self._check_args_records()
        self._check_args_repository_root()

    def _check_args_records(self) -> None:
        """Require exact result ownership and an immutable endpoint tuple."""
        if type(self.result) is not OptimizerReanalysisResult:
            raise TypeError("result must be an exact optimizer reanalysis result")
        if type(self.correlated_endpoints) is not tuple:
            raise TypeError("correlated_endpoints must be an exact tuple")
        if any(
            type(value) is not OptimizerReanalysisEndpoint
            for value in self.correlated_endpoints
        ):
            raise TypeError(
                "correlated_endpoints must contain exact reanalysis endpoint records"
            )

    def _check_args_repository_root(self) -> None:
        """Require an absolute pathlib repository root."""
        if not isinstance(self.repository_root, Path):
            raise TypeError("repository_root must be pathlib.Path")
        if not self.repository_root.is_absolute():
            raise ValueError("repository_root must be absolute")


class OptimizerReanalysisRefinementVerifier:
    """Authenticate maintained fixtures and reconstruct retained refinements."""

    __slots__ = ("center_comparator", "source_authenticator")

    def __init__(self) -> None:
        """Create one verifier with center and source-authentication Actions."""
        self.center_comparator = PeriodicCenterSetComparator()
        self.source_authenticator = OptimizerReanalysisRepositorySourceAuthenticator()

    def execute(self, request: OptimizerReanalysisRefinementVerificationRequest) -> int:
        """Verify all retained refinement cases and return their exact count.

        Parameters
        ----------
        request
            Validated result, source-correlated endpoints, and absolute repository root.

        Returns
        -------
        int
            Exact number of successfully reconstructed retained refinement cases.

        Raises
        ------
        TypeError
            If ``request`` has an incompatible exact type.
        ValueError
            If a logical fixture name is absent or resolves outside the maintained
            repository fixture directory.
        OSError
            If a confined maintained fixture cannot be read.
        AssertionError
            If identities, sizes, fixture bytes, endpoint status, or reconstructed
            refinement values disagree.
        MemoryError
            If dense periodic center matching cannot allocate required state.
        """
        if type(request) is not OptimizerReanalysisRefinementVerificationRequest:
            raise TypeError(
                "request must be OptimizerReanalysisRefinementVerificationRequest"
            )
        refinements = request.result.common_estimator_refinement
        case_ids = tuple(refinement.case_id for refinement in refinements)
        if len(case_ids) != len(set(case_ids)):
            raise AssertionError("refinement cases must have unique identities")
        endpoint_by_identity = {
            (endpoint.configuration_id, endpoint.gauge_id): endpoint
            for endpoint in request.correlated_endpoints
        }
        resolved_root = request.repository_root.resolve()
        fixture_root = (resolved_root / _ESTIMATOR_FIXTURE_DIRECTORY).resolve()
        if not fixture_root.is_relative_to(resolved_root):
            raise ValueError(
                "estimator fixture root must resolve within repository_root"
            )

        for refinement in refinements:
            identity = (refinement.configuration_id, refinement.gauge_id)
            endpoint = endpoint_by_identity.get(identity)
            if endpoint is None:
                raise AssertionError("refinement endpoint identity is unavailable")
            if (
                refinement.convergence_criterion_satisfied
                != endpoint.convergence_criterion_satisfied
            ):
                raise AssertionError("refinement endpoint convergence changed")

            observed_sizes = tuple(size.fft_size for size in refinement.sizes)
            if observed_sizes != _FFT_REFINEMENT_SIZES:
                raise AssertionError("unexpected FFT refinement sizes")
            if request.result.method.common_estimator_fft_sizes != observed_sizes:
                raise AssertionError("method and refinement FFT sizes disagree")

            for size in refinement.sizes:
                # External paths are unavailable. The portable adapter binds only the
                # declared logical basename to a maintained repository fixture.
                logical_name = Path(size.input_path).name
                if not logical_name:
                    raise ValueError("refinement input_path must have a basename")
                self.source_authenticator.execute(
                    OptimizerReanalysisRepositorySourceAuthenticationRequest(
                        repository_root=fixture_root,
                        declared_path=logical_name,
                        expected_sha256=size.input_sha256,
                        label=logical_name,
                    )
                )

            lower, upper = refinement.sizes[1], refinement.sizes[2]
            relative_difference = abs(
                lower.common_total_spread_cell_squared
                - upper.common_total_spread_cell_squared
            ) / max(
                abs(upper.common_total_spread_cell_squared),
                _RELATIVE_ERROR_DENOMINATOR_FLOOR,
            )
            if (
                abs(relative_difference - refinement.relative_total_spread_difference)
                > _REFINEMENT_TOLERANCE
            ):
                raise AssertionError("refinement spread changed")
            center_distance = self.center_comparator.execute(
                PeriodicCenterSetComparisonRequest(
                    first=lower.common_centers_modulo_cell,
                    second=upper.common_centers_modulo_cell,
                    include_square_lattice_symmetry=False,
                )
            )
            if (
                abs(center_distance - refinement.center_set_periodic_distance)
                > _REFINEMENT_TOLERANCE
            ):
                raise AssertionError("refinement centers changed")
        return len(refinements)
