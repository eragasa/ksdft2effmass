"""Repository-portable verification of optimizer-basin reanalysis."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from ksdft2effmass.serialization.json import StrictJsonDecoder

from .authentication import Periodic2DOptimizerReanalysisSourceAuthenticator
from .correlation import Periodic2DOptimizerReanalysisCorrelator
from .decode import Periodic2DOptimizerReanalysisDocumentDecoder
from .encoded_documents import Periodic2DOptimizerReanalysisEncodedDocuments
from .refinement import (
    OptimizerReanalysisRefinementVerificationRequest,
    OptimizerReanalysisRefinementVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerReanalysisCampaignVerificationRequest:
    """Request portable verification of one retained offline reanalysis.

    Parameters
    ----------
    encoded_documents
        Exact source-result and reanalysis-result wires.
    repository_root
        Absolute repository root used only for confined compact-source and maintained
        estimator-fixture authentication.

    Raises
    ------
    TypeError
        If either argument has an incompatible representation.
    ValueError
        If ``repository_root`` is not absolute.
    """

    encoded_documents: Periodic2DOptimizerReanalysisEncodedDocuments
    repository_root: Path

    def __post_init__(self) -> None:
        """Validate exact document ownership and root location."""
        self._check_args_documents()
        self._check_args_repository_root()

    def _check_args_documents(self) -> None:
        """Require the exact row-053 encoded-document type."""
        if (
            type(self.encoded_documents)
            is not Periodic2DOptimizerReanalysisEncodedDocuments
        ):
            raise TypeError(
                "encoded_documents must be "
                "Periodic2DOptimizerReanalysisEncodedDocuments"
            )

    def _check_args_repository_root(self) -> None:
        """Require one absolute pathlib repository root."""
        if not isinstance(self.repository_root, Path):
            raise TypeError("repository_root must be pathlib.Path")
        if not self.repository_root.is_absolute():
            raise ValueError("repository_root must be absolute")


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerReanalysisCampaignVerificationResult:
    """Report bounded spread, basin, trace, and refinement reconstruction.

    Parameters
    ----------
    source_authentication_passed
        Exact Boolean outcome for directly authenticated compact sources.
    structural_reconstruction_passed
        Exact Boolean outcome for the portable structural/numerical checks.
    endpoint_count
        Nonnegative exact built-in integer number of correlated endpoints.
    refinement_case_count
        Nonnegative exact built-in integer number of correlated refinement cases.
    retained_result_sha256
        Lowercase SHA-256 identity of exact reanalysis-result bytes.

    Raises
    ------
    TypeError
        If flags, counts, or digest use incompatible exact representations.
    ValueError
        If a count is negative or the digest is not lowercase SHA-256 hexadecimal.

    Notes
    -----
    Direct construction validates intrinsic immutable state only; it does not prove the
    verifier Action executed. A passing Action-produced result does not authenticate
    external native files, rerun Wannier90, prove optimizer completeness or global
    optimality, establish scientific validation, quantify uncertainty, or record
    acceptance.
    """

    source_authentication_passed: bool
    structural_reconstruction_passed: bool
    endpoint_count: int
    refinement_case_count: int
    retained_result_sha256: str

    def __post_init__(self) -> None:
        """Validate exact intrinsic scalar representations and ranges."""
        self._check_args_flags()
        self._check_args_counts()
        StrictJsonDecoder().sha256(
            self.retained_result_sha256, "retained_result_sha256"
        )

    def _check_args_flags(self) -> None:
        """Require exact built-in Boolean pass indicators."""
        for name, value in (
            ("source_authentication_passed", self.source_authentication_passed),
            ("structural_reconstruction_passed", self.structural_reconstruction_passed),
        ):
            if type(value) is not bool:
                raise TypeError(f"{name} must be a built-in bool")

    def _check_args_counts(self) -> None:
        """Require nonnegative exact built-in endpoint and refinement counts."""
        for name, value in (
            ("endpoint_count", self.endpoint_count),
            ("refinement_case_count", self.refinement_case_count),
        ):
            if type(value) is not int:
                raise TypeError(f"{name} must be an integer")
            if value < 0:
                raise ValueError(f"{name} must be nonnegative")

    @property
    def passes(self) -> bool:
        """Return the conjunction of the two bounded pass indicators.

        Returns
        -------
        bool
            ``True`` exactly when authentication and structural reconstruction passed.
        """
        return (
            self.source_authentication_passed and self.structural_reconstruction_passed
        )


class Periodic2DOptimizerReanalysisCampaignVerifier:
    """Compose typed Actions for bounded portable reanalysis verification.

    The verifier owns orchestration only. Schema adaptation, compact-source
    authentication, source/endpoint/basin correlation, and common-estimator refinement
    are delegated to cohesive instantiated Actions. No collaborator accesses the
    unavailable external native tree or invokes Wannier90.
    """

    __slots__ = ("correlator", "decoder", "refinement_verifier", "source_authenticator")

    def __init__(self) -> None:
        """Create one verifier with request-scoped cohesive collaborators."""
        self.correlator = Periodic2DOptimizerReanalysisCorrelator()
        self.decoder = Periodic2DOptimizerReanalysisDocumentDecoder()
        self.refinement_verifier = OptimizerReanalysisRefinementVerifier()
        self.source_authenticator = Periodic2DOptimizerReanalysisSourceAuthenticator()

    def execute(
        self, request: Periodic2DOptimizerReanalysisCampaignVerificationRequest
    ) -> Periodic2DOptimizerReanalysisCampaignVerificationResult:
        """Authenticate compact sources and reconstruct bounded retained diagnostics.

        Parameters
        ----------
        request
            Exact encoded documents and an absolute repository root.

        Returns
        -------
        Periodic2DOptimizerReanalysisCampaignVerificationResult
            Immutable counts and bounded pass indicators after every check succeeds.

        Raises
        ------
        TypeError
            If a decoded field has an incompatible exact representation.
        ValueError
            If strict JSON, finite-real, digest, root, coordinate, or path-confinement
            contracts fail.
        OverflowError
            If a JSON integer converted to binary64 lies outside its finite range.
        KeyError
            If a required verifier-owned field is absent.
        OSError
            If a confined compact source or maintained estimator fixture cannot be read.
        AssertionError
            If source correlation, identities, arithmetic, classifications, basin
            partitions, or refinement diagnostics disagree.
        MemoryError
            If decoding, immutable adaptation, canonical comparison, or dense
            permutation matching cannot allocate required state.
        RecursionError
            If a retained document exceeds parser or immutable-adapter recursion depth.

        Notes
        -----
        Center matching scales factorially with retained rank. No arbitrary rank cap is
        imposed; this retained campaign has rank three. Passing establishes software
        consistency only, not scientific validation or historical native-execution
        authenticity.
        """
        request_type = Periodic2DOptimizerReanalysisCampaignVerificationRequest
        if type(request) is not request_type:
            raise TypeError(
                "request must be "
                "Periodic2DOptimizerReanalysisCampaignVerificationRequest"
            )
        decoded = self.decoder.execute(request.encoded_documents)
        self.source_authenticator.execute(
            request.encoded_documents,
            decoded.reanalysis_result.provenance,
            request.repository_root,
        )
        correlation = self.correlator.execute(decoded)
        refinement_count = self.refinement_verifier.execute(
            OptimizerReanalysisRefinementVerificationRequest(
                result=decoded.reanalysis_result,
                correlated_endpoints=correlation.endpoints,
                repository_root=request.repository_root,
            )
        )
        return Periodic2DOptimizerReanalysisCampaignVerificationResult(
            source_authentication_passed=True,
            structural_reconstruction_passed=True,
            endpoint_count=len(correlation.endpoints),
            refinement_case_count=refinement_count,
            retained_result_sha256=hashlib.sha256(
                request.encoded_documents.result_payload
            ).hexdigest(),
        )
