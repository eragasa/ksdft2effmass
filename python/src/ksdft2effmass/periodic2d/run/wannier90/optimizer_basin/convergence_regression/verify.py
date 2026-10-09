"""Repository-portable verification of censored optimizer regression."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from ksdft2effmass.serialization.json import StrictJsonDecoder

from .authentication import Periodic2DOptimizerRegressionSourceAuthenticator
from .correlation import Periodic2DOptimizerRegressionCorrelator
from .decode import Periodic2DOptimizerRegressionDocumentDecoder
from .encoded_documents import Periodic2DOptimizerRegressionEncodedDocuments


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerRegressionCampaignVerificationRequest:
    """Request portable verification of one retained censored regression.

    Parameters
    ----------
    encoded_documents
        Exact source-result, analyzer, and regression-result wires.
    repository_root
        Absolute repository root used for confined maintained-file authentication.

    Raises
    ------
    TypeError
        If either field has an incompatible exact type.
    ValueError
        If ``repository_root`` is relative.
    """

    encoded_documents: Periodic2DOptimizerRegressionEncodedDocuments
    repository_root: Path

    def __post_init__(self) -> None:
        """Delegate exact document and repository-root checks."""
        self._check_args_encoded_documents()
        self._check_args_repository_root()

    def _check_args_encoded_documents(self) -> None:
        """Require the exact encoded-document owner."""
        document_type = Periodic2DOptimizerRegressionEncodedDocuments
        if type(self.encoded_documents) is not document_type:
            raise TypeError(
                "encoded_documents must be "
                "Periodic2DOptimizerRegressionEncodedDocuments"
            )

    def _check_args_repository_root(self) -> None:
        """Require an absolute pathlib repository root."""
        if not isinstance(self.repository_root, Path):
            raise TypeError("repository_root must be pathlib.Path")
        if not self.repository_root.is_absolute():
            raise ValueError("repository_root must be absolute")


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerRegressionCampaignVerificationResult:
    """Report bounded authentication and numerical reconstruction diagnostics.

    Parameters
    ----------
    source_authentication_passed, numerical_reconstruction_passed
        Exact built-in pass indicators derived by the verifier Action.
    observation_count, converged_count, right_censored_count, parameter_count
        Exact nonnegative reconstructed counts.
    retained_result_sha256
        Lowercase SHA-256 identity of exact retained regression bytes.

    Raises
    ------
    TypeError
        If a flag, count, or digest has an incompatible exact representation.
    ValueError
        If a count is negative or the digest is malformed.
    """

    source_authentication_passed: bool
    numerical_reconstruction_passed: bool
    observation_count: int
    converged_count: int
    right_censored_count: int
    parameter_count: int
    retained_result_sha256: str

    def __post_init__(self) -> None:
        """Delegate intrinsic flag, count, and digest checks."""
        self._check_args_flags()
        self._check_args_counts()
        self._check_args_retained_result_sha256()

    def _check_args_flags(self) -> None:
        """Require exact built-in Boolean pass indicators."""
        if type(self.source_authentication_passed) is not bool:
            raise TypeError("source_authentication_passed must be bool")
        if type(self.numerical_reconstruction_passed) is not bool:
            raise TypeError("numerical_reconstruction_passed must be bool")

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

    def _check_args_retained_result_sha256(self) -> None:
        """Require strict lowercase SHA-256 syntax."""
        StrictJsonDecoder().sha256(
            self.retained_result_sha256, "retained_result_sha256"
        )

    @property
    def passes(self) -> bool:
        """Return the conjunction of bounded pass indicators.

        Returns
        -------
        bool
            ``True`` exactly when source authentication and reconstruction passed.
        """
        return (
            self.source_authentication_passed and self.numerical_reconstruction_passed
        )


class Periodic2DOptimizerRegressionCampaignVerifier:
    """Compose typed Actions for bounded portable regression verification.

    The verifier owns orchestration only. Strict schema adaptation, repository source
    authentication, design construction, and numerical correlation remain with cohesive
    instantiated Actions. No Action imports or executes the retained analyzer.
    """

    __slots__ = ("correlator", "decoder", "source_authenticator")

    def __init__(self) -> None:
        """Create one request-scoped verifier with explicit collaborators."""
        self.decoder = Periodic2DOptimizerRegressionDocumentDecoder()
        self.source_authenticator = Periodic2DOptimizerRegressionSourceAuthenticator()
        self.correlator = Periodic2DOptimizerRegressionCorrelator()

    def execute(
        self, request: Periodic2DOptimizerRegressionCampaignVerificationRequest
    ) -> Periodic2DOptimizerRegressionCampaignVerificationResult:
        """Authenticate and reconstruct one retained exploratory regression.

        Parameters
        ----------
        request
            Exact encoded documents and absolute repository root.

        Returns
        -------
        Periodic2DOptimizerRegressionCampaignVerificationResult
            Immutable counts, digest, and bounded pass indicators.

        Raises
        ------
        TypeError
            If a request, wire, or field has an incompatible exact representation.
        ValueError
            If JSON, finite values, counts, probabilities, or paths are invalid.
        OverflowError
            If binary64 numerical reconstruction becomes nonfinite.
        KeyError
            If a required verifier-owned field is absent.
        OSError
            If a confined maintained source cannot be read.
        AssertionError
            If authentication, identities, counts, metadata, or numerics disagree.
        numpy.linalg.LinAlgError
            If dense pseudoinversion or condition estimation fails.
        MemoryError
            If strict decoding or dense numerical reconstruction cannot allocate state.
        RecursionError
            If a retained document exceeds strict-parser recursion depth.

        Notes
        -----
        Dense regression work scales as documented by the numerical Actions. Passing
        establishes bounded software and numerical consistency only; it does not prove
        optimizer convergence, causality, population inference, physical uncertainty,
        DFT behavior, scientific validation, or acceptance.
        """
        request_type = Periodic2DOptimizerRegressionCampaignVerificationRequest
        if type(request) is not request_type:
            raise TypeError(
                "request must be "
                "Periodic2DOptimizerRegressionCampaignVerificationRequest"
            )
        decoded = self.decoder.execute(request.encoded_documents)
        self.source_authenticator.execute(
            request.encoded_documents,
            decoded.regression_result,
            request.repository_root,
        )
        correlation = self.correlator.execute(decoded)
        return Periodic2DOptimizerRegressionCampaignVerificationResult(
            source_authentication_passed=True,
            numerical_reconstruction_passed=True,
            observation_count=correlation.observation_count,
            converged_count=correlation.converged_count,
            right_censored_count=correlation.right_censored_count,
            parameter_count=correlation.parameter_count,
            retained_result_sha256=hashlib.sha256(
                request.encoded_documents.regression_payload
            ).hexdigest(),
        )
