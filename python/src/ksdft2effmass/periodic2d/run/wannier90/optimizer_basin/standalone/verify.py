"""Repository-portable verification of the standalone optimizer study."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from ksdft2effmass.serialization.json import StrictJsonDecoder

from .authentication import Periodic2DOptimizerStandaloneSourceAuthenticator
from .correlation import Periodic2DOptimizerStandaloneCorrelator
from .decode import Periodic2DOptimizerStandaloneDocumentDecoder
from .encoded_documents import Periodic2DOptimizerStandaloneEncodedDocuments


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerStandaloneCampaignVerificationRequest:
    """Request bounded verification of one retained standalone optimizer study.

    Parameters
    ----------
    encoded_documents
        Exact proposal, deterministic-start design, and result wires.
    repository_root
        Absolute repository root used for confined compact-source authentication.

    Raises
    ------
    TypeError
        If either field has an incompatible exact type.
    ValueError
        If ``repository_root`` is relative.
    """

    encoded_documents: Periodic2DOptimizerStandaloneEncodedDocuments
    repository_root: Path

    def __post_init__(self) -> None:
        """Delegate document-owner and repository-root validation."""
        self._check_args_encoded_documents()
        self._check_args_repository_root()

    def _check_args_encoded_documents(self) -> None:
        """Require the exact row-055 encoded-document owner."""
        if (
            type(self.encoded_documents)
            is not Periodic2DOptimizerStandaloneEncodedDocuments
        ):
            raise TypeError(
                "encoded_documents must be "
                "Periodic2DOptimizerStandaloneEncodedDocuments"
            )

    def _check_args_repository_root(self) -> None:
        """Require an absolute pathlib repository root without string coercion."""
        if not isinstance(self.repository_root, Path):
            raise TypeError("repository_root must be pathlib.Path")
        if not self.repository_root.is_absolute():
            raise ValueError("repository_root must be absolute")


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerStandaloneCampaignVerificationResult:
    """Report bounded source authentication and structural reconstruction.

    Parameters
    ----------
    source_authentication_passed, structural_reconstruction_passed
        Exact built-in pass indicators derived by the verifier Action.
    endpoint_count, continuation_count
        Exact nonnegative reconstructed process and continuation counts.
    effective_converged_count, final_nonconverged_count
        Exact nonnegative reconstructed effective-outcome counts.
    retained_result_sha256
        Lowercase SHA-256 identity of exact retained result bytes.

    Raises
    ------
    TypeError
        If a flag, count, or digest has an incompatible exact representation.
    ValueError
        If a count is negative or the digest is malformed.
    """

    source_authentication_passed: bool
    structural_reconstruction_passed: bool
    endpoint_count: int
    continuation_count: int
    effective_converged_count: int
    final_nonconverged_count: int
    retained_result_sha256: str

    def __post_init__(self) -> None:
        """Delegate intrinsic flag, count, and digest validation."""
        self._check_args_flags()
        self._check_args_counts()
        self._check_args_retained_result_sha256()

    def _check_args_flags(self) -> None:
        """Require exact built-in Boolean pass indicators."""
        if type(self.source_authentication_passed) is not bool:
            raise TypeError("source_authentication_passed must be bool")
        if type(self.structural_reconstruction_passed) is not bool:
            raise TypeError("structural_reconstruction_passed must be bool")

    def _check_args_counts(self) -> None:
        """Require exact nonnegative built-in integer counts."""
        for name, value in (
            ("endpoint_count", self.endpoint_count),
            ("continuation_count", self.continuation_count),
            ("effective_converged_count", self.effective_converged_count),
            ("final_nonconverged_count", self.final_nonconverged_count),
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
        """Return the conjunction of the two bounded pass indicators.

        Returns
        -------
        bool
            ``True`` exactly when authentication and reconstruction passed.
        """
        return (
            self.source_authentication_passed and self.structural_reconstruction_passed
        )


class Periodic2DOptimizerStandaloneCampaignVerifier:
    """Compose typed Actions for portable standalone-study verification.

    This Action owns orchestration only. Decoding, direct source authentication,
    endpoint arithmetic, and aggregate correlation remain separate instantiated owners.
    It never opens an external native run root or imports a calculation script.
    """

    __slots__ = ("correlator", "decoder", "source_authenticator")

    def __init__(self) -> None:
        """Create one request-scoped verifier with explicit collaborators."""
        self.decoder = Periodic2DOptimizerStandaloneDocumentDecoder()
        self.source_authenticator = Periodic2DOptimizerStandaloneSourceAuthenticator()
        self.correlator = Periodic2DOptimizerStandaloneCorrelator()

    def execute(
        self, request: Periodic2DOptimizerStandaloneCampaignVerificationRequest
    ) -> Periodic2DOptimizerStandaloneCampaignVerificationResult:
        """Authenticate and reconstruct the retained finite standalone design.

        Parameters
        ----------
        request
            Exact encoded documents and absolute repository root.

        Returns
        -------
        Periodic2DOptimizerStandaloneCampaignVerificationResult
            Immutable reconstructed counts, result identity, and bounded pass flags.

        Raises
        ------
        TypeError
            If a request, wire, or field has an incompatible exact representation.
        ValueError
            If JSON, a digest, finite value, extended real, or path is invalid.
        OverflowError
            If a consumed integer cannot be represented in binary64.
        KeyError
            If a required verifier-owned field is absent.
        OSError
            If a confined maintained compact source cannot be read.
        AssertionError
            If authentication, transitions, aggregates, basins, controls, or claim
            boundaries disagree.
        MemoryError
            If decoding or immutable record construction cannot allocate state.
        RecursionError
            If a retained document exceeds parser or validation recursion depth.

        Notes
        -----
        Passing establishes bounded software and arithmetic consistency only. It does
        not authenticate external native files, prove a global optimum or general
        Wannier90 convergence, establish scientific validation or uncertainty
        quantification, or record acceptance.
        """
        if (
            type(request)
            is not Periodic2DOptimizerStandaloneCampaignVerificationRequest
        ):
            raise TypeError(
                "request must be "
                "Periodic2DOptimizerStandaloneCampaignVerificationRequest"
            )
        decoded = self.decoder.execute(request.encoded_documents)
        self.source_authenticator.execute(
            request.encoded_documents,
            decoded.gauge_design,
            decoded.result,
            request.repository_root,
        )
        reconstruction = self.correlator.execute(decoded)
        return Periodic2DOptimizerStandaloneCampaignVerificationResult(
            source_authentication_passed=True,
            structural_reconstruction_passed=True,
            endpoint_count=reconstruction.endpoint_count,
            continuation_count=reconstruction.continuation_count,
            effective_converged_count=reconstruction.effective_converged_count,
            final_nonconverged_count=reconstruction.final_nonconverged_count,
            retained_result_sha256=hashlib.sha256(
                request.encoded_documents.result_payload
            ).hexdigest(),
        )
