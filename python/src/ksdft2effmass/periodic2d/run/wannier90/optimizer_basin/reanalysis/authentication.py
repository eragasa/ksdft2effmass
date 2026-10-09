"""Confined compact-source authentication for optimizer reanalysis."""

import hashlib
from dataclasses import dataclass
from pathlib import Path

from ksdft2effmass.serialization.json import StrictJsonDecoder

from .encoded_documents import Periodic2DOptimizerReanalysisEncodedDocuments
from .records import OptimizerReanalysisProvenance


@dataclass(frozen=True, slots=True)
class OptimizerReanalysisRepositorySourceAuthenticationRequest:
    """Request authentication of one directly declared repository source.

    Parameters
    ----------
    repository_root
        Absolute root that confines source resolution.
    declared_path
        Exact path declaration resolved beneath ``repository_root``.
    expected_sha256
        Strict lowercase SHA-256 identity of expected source bytes.
    label
        Nonempty diagnostic name used in failure messages.
    """

    repository_root: Path
    declared_path: str
    expected_sha256: str
    label: str

    def __post_init__(self) -> None:
        """Validate exact location, digest, and diagnostic-label fields."""
        self._check_args_location()
        self._check_args_identity()

    def _check_args_location(self) -> None:
        """Require an absolute pathlib root and exact nonempty path text."""
        if not isinstance(self.repository_root, Path):
            raise TypeError("repository_root must be pathlib.Path")
        if not self.repository_root.is_absolute():
            raise ValueError("repository_root must be absolute")
        for name, value in (
            ("declared_path", self.declared_path),
            ("label", self.label),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a string")
            if not value:
                raise ValueError(f"{name} must be nonempty")

    def _check_args_identity(self) -> None:
        """Require strict lowercase SHA-256 syntax for expected content identity."""
        StrictJsonDecoder().sha256(self.expected_sha256, "expected_sha256")


class OptimizerReanalysisRepositorySourceAuthenticator:
    """Resolve and authenticate one directly declared confined source file."""

    __slots__ = ()

    def execute(
        self, request: OptimizerReanalysisRepositorySourceAuthenticationRequest
    ) -> Path:
        """Return a confined path after exact SHA-256 authentication.

        Parameters
        ----------
        request
            Explicit repository root, declared path, digest, and diagnostic label.

        Returns
        -------
        pathlib.Path
            Resolved authenticated path beneath the resolved repository root.

        Raises
        ------
        TypeError
            If ``request`` has an incompatible exact type.
        ValueError
            If the declared path resolves outside the repository root.
        OSError
            If the confined source cannot be read.
        AssertionError
            If the exact source bytes disagree with the declared digest.
        """
        request_type = OptimizerReanalysisRepositorySourceAuthenticationRequest
        if type(request) is not request_type:
            raise TypeError(
                "request must be "
                "OptimizerReanalysisRepositorySourceAuthenticationRequest"
            )
        resolved_root = request.repository_root.resolve()
        candidate = (resolved_root / Path(request.declared_path)).resolve()
        if not candidate.is_relative_to(resolved_root):
            raise ValueError(f"{request.label} must resolve within repository_root")
        actual_sha256 = hashlib.sha256(candidate.read_bytes()).hexdigest()
        if actual_sha256 != request.expected_sha256:
            raise AssertionError(f"{request.label} identity mismatch")
        return candidate


class Periodic2DOptimizerReanalysisSourceAuthenticator:
    """Authenticate encapsulated source bytes and direct compact source files."""

    __slots__ = ("repository_source_authenticator",)

    def __init__(self) -> None:
        """Create one authenticator with a confined-source collaborator."""
        self.repository_source_authenticator = (
            OptimizerReanalysisRepositorySourceAuthenticator()
        )

    def execute(
        self,
        documents: Periodic2DOptimizerReanalysisEncodedDocuments,
        provenance: OptimizerReanalysisProvenance,
        repository_root: Path,
    ) -> None:
        """Authenticate all compact sources owned by the portable contract.

        Parameters
        ----------
        documents
            Exact encapsulated source/result wires.
        provenance
            Strictly decoded compact-source declarations.
        repository_root
            Absolute repository root used for confined path resolution.

        Raises
        ------
        TypeError
            If documents, provenance, or repository root has an incompatible type.
        ValueError
            If the root is relative or a declared path resolves outside it.
        OSError
            If a confined compact source cannot be read.
        AssertionError
            If encapsulated or repository bytes disagree with a declared digest.
        """
        if type(documents) is not Periodic2DOptimizerReanalysisEncodedDocuments:
            raise TypeError(
                "documents must be Periodic2DOptimizerReanalysisEncodedDocuments"
            )
        if type(provenance) is not OptimizerReanalysisProvenance:
            raise TypeError("provenance must be OptimizerReanalysisProvenance")
        if not isinstance(repository_root, Path):
            raise TypeError("repository_root must be pathlib.Path")
        if not repository_root.is_absolute():
            raise ValueError("repository_root must be absolute")
        source_digest = hashlib.sha256(documents.source_result_payload).hexdigest()
        if source_digest != provenance.source_result_sha256:
            raise AssertionError("source result identity mismatch")

        declarations = (
            (
                provenance.reanalyzer_path,
                provenance.reanalyzer_sha256,
                "reanalyzer_path",
            ),
            (
                provenance.base_extractor_path,
                provenance.base_extractor_sha256,
                "base_extractor_path",
            ),
        )
        for declared_path, expected_sha256, label in declarations:
            self.repository_source_authenticator.execute(
                OptimizerReanalysisRepositorySourceAuthenticationRequest(
                    repository_root=repository_root,
                    declared_path=declared_path,
                    expected_sha256=expected_sha256,
                    label=label,
                )
            )
