"""Encapsulating façade and campaign-level route-reconciliation Actions."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from ksdft2effmass.periodic1d.campaign.serialization import (
    Periodic1DCampaignJsonDecoder,
)
from ksdft2effmass.serialization.json import JsonValue

from .encoded_documents import RouteReconciliationEncodedDocuments
from .result_documents import RouteReconciliationCampaignResultDocument
from .verification import (
    RouteReconciliationCampaignVerifier,
    RouteReconciliationVerificationRequest,
    RouteReconciliationVerificationResult,
)
from .workflow import (
    RouteReconciliationBaselineLoader,
    RouteReconciliationCampaignInputDeserializer,
    RouteReconciliationCampaignWorkflow,
    RouteReconciliationProvenance,
)


@dataclass(frozen=True, slots=True)
class RouteReconciliationCalculationRequest:
    """Request calculation from exact documents, location, and provenance.

    Parameters
    ----------
    encoded_documents
        Exact input and retained-result byte documents.
    repository_root
        Caller-owned absolute base for repository-relative authenticated sources.
    provenance
        Explicit current execution provenance; it is not inferred from location.

    Raises
    ------
    TypeError
        If a field has an unsupported public type.
    ValueError
        If ``repository_root`` is relative.

    Notes
    -----
    Construction checks lexical absoluteness only and performs no filesystem access,
    decoding, source authentication, or numerical work.
    """

    encoded_documents: RouteReconciliationEncodedDocuments
    repository_root: Path
    provenance: RouteReconciliationProvenance

    def __post_init__(self) -> None:
        """Require exact documents, an absolute root, and typed provenance."""
        if type(self.encoded_documents) is not RouteReconciliationEncodedDocuments:
            raise TypeError(
                "encoded_documents must be RouteReconciliationEncodedDocuments"
            )
        self._check_repository_root()
        if type(self.provenance) is not RouteReconciliationProvenance:
            raise TypeError("provenance must be RouteReconciliationProvenance")

    def _check_repository_root(self) -> None:
        """Require a caller-owned absolute path without resolving it."""
        if not isinstance(self.repository_root, Path):
            raise TypeError("repository_root must be pathlib.Path")
        if not self.repository_root.is_absolute():
            raise ValueError("repository_root must be absolute")


@dataclass(frozen=True, slots=True)
class RouteReconciliationRetainedCorrelationRequest:
    """Request retained correlation from exact documents and location.

    Parameters
    ----------
    encoded_documents
        Exact input and retained-result byte documents.
    repository_root
        Caller-owned absolute base for repository-relative authenticated sources.

    Raises
    ------
    TypeError
        If a field has an unsupported public type.
    ValueError
        If ``repository_root`` is relative.

    Notes
    -----
    Construction checks lexical absoluteness only and performs no filesystem access,
    decoding, source authentication, retained reconstruction, or comparison.
    """

    encoded_documents: RouteReconciliationEncodedDocuments
    repository_root: Path

    def __post_init__(self) -> None:
        """Require exact documents and a caller-owned absolute path."""
        if type(self.encoded_documents) is not RouteReconciliationEncodedDocuments:
            raise TypeError(
                "encoded_documents must be RouteReconciliationEncodedDocuments"
            )
        if not isinstance(self.repository_root, Path):
            raise TypeError("repository_root must be pathlib.Path")
        if not self.repository_root.is_absolute():
            raise ValueError("repository_root must be absolute")


@dataclass(frozen=True, slots=True)
class RouteReconciliationResultCorrelation:
    """Report semantic-document and canonical-byte retained identity channels.

    Parameters
    ----------
    semantic_identity
        Whether independently reconstructed typed semantics equal the campaign
        result.
    canonical_byte_identity
        Whether canonical serialization reproduces the retained result bytes
        exactly.
    calculated_sha256
        Lowercase SHA-256 digest calculated from the exact retained bytes.
    retained_sha256
        Lowercase SHA-256 digest declared by the retained result document.

    Raises
    ------
    TypeError
        An argument does not have the required exact public type.
    ValueError
        An argument violates a schema, domain, identity, or correlation invariant.
    """

    semantic_identity: bool
    canonical_byte_identity: bool
    calculated_sha256: str
    retained_sha256: str

    def __post_init__(self) -> None:
        """Validate Booleans and lowercase SHA-256 identities."""
        if type(self.semantic_identity) is not bool:
            raise TypeError("semantic_identity must be Boolean")
        if type(self.canonical_byte_identity) is not bool:
            raise TypeError("canonical_byte_identity must be Boolean")
        for digest in (self.calculated_sha256, self.retained_sha256):
            if len(digest) != 64 or any(
                character not in "0123456789abcdef" for character in digest
            ):
                raise ValueError("correlation digests must be lowercase SHA-256")


@dataclass(frozen=True, slots=True)
class RouteReconciliationCampaign:
    """Encapsulate one route-reconciliation campaign behind a small façade.

    Parameters
    ----------
    encoded_documents
        Immutable exact input and retained-result byte documents.

    Raises
    ------
    TypeError
        An argument does not have the required exact public type.
    """

    encoded_documents: RouteReconciliationEncodedDocuments

    def __post_init__(self) -> None:
        """Require the exact encoded-document type."""
        if type(self.encoded_documents) is not RouteReconciliationEncodedDocuments:
            raise TypeError(
                "encoded_documents must be RouteReconciliationEncodedDocuments"
            )

    def calculate(
        self,
        *,
        repository_root: Path,
        input_path: str,
        input_sha256: str,
        script_path: str,
        script_sha256: str,
        python_version: str,
        numpy_version: str,
    ) -> RouteReconciliationCampaignResultDocument:
        """Calculate all route records under explicit adapter provenance.

        Parameters
        ----------
        repository_root
            Explicit absolute root confining authenticated repository-relative access.
        input_path
            Explicit path of the retained input within the operation-owned root.
        input_sha256
            Lowercase SHA-256 identity of the exact retained input bytes.
        script_path
            Explicit repository-relative path of the retained campaign script.
        script_sha256
            Lowercase SHA-256 identity of the exact retained script bytes.
        python_version
            Explicit nonempty Python version retained as software provenance.
        numpy_version
            Explicit nonempty NumPy version retained as software provenance.

        Returns
        -------
        RouteReconciliationCampaignResultDocument
            Immutable exact result document for nominal, adversarial, and reconciled
            routes.
        """
        return self._calculate(
            RouteReconciliationCalculationRequest(
                encoded_documents=self.encoded_documents,
                repository_root=repository_root,
                provenance=RouteReconciliationProvenance(
                    input_path=input_path,
                    input_sha256=input_sha256,
                    script_path=script_path,
                    script_sha256=script_sha256,
                    python_version=python_version,
                    numpy_version=numpy_version,
                ),
            )
        )

    def retained_result(self) -> RouteReconciliationCampaignResultDocument:
        """Return the retained result document without calculating or verifying it.

        Returns
        -------
        RouteReconciliationCampaignResultDocument
            Immutable document retaining the exact result bytes.
        """
        return RouteReconciliationCampaignResultDocument(
            self.encoded_documents.retained_result_document
        )

    def correlate_retained(
        self, repository_root: Path
    ) -> RouteReconciliationResultCorrelation:
        """Reconstruct using an explicit root and report identity correlation.

        Parameters
        ----------
        repository_root
            Explicit absolute root confining authenticated repository-relative access.

        Returns
        -------
        RouteReconciliationResultCorrelation
            Correlation report separating canonical-byte identity from typed semantic
            identity.
        """
        request = RouteReconciliationRetainedCorrelationRequest(
            self.encoded_documents, repository_root
        )
        retained = self.retained_result()
        calculated = self._calculate(
            RouteReconciliationCalculationRequest(
                request.encoded_documents,
                request.repository_root,
                self._retained_provenance(),
            )
        )
        retained_value = self._decode(retained.payload)
        calculated_value = self._decode(calculated.payload)
        return RouteReconciliationResultCorrelation(
            semantic_identity=calculated_value == retained_value,
            canonical_byte_identity=calculated.payload == retained.payload,
            calculated_sha256=calculated.sha256,
            retained_sha256=retained.sha256,
        )

    def verify_retained(
        self, repository_root: Path
    ) -> RouteReconciliationVerificationResult:
        """Independently authenticate and reconstruct the retained campaign.

        Parameters
        ----------
        repository_root
            Explicit absolute root confining authenticated repository-relative access.

        Returns
        -------
        RouteReconciliationVerificationResult
            Independent authentication and full route-reconstruction result.
        """
        return RouteReconciliationCampaignVerifier().execute(
            RouteReconciliationVerificationRequest(
                self.encoded_documents, repository_root
            )
        )

    def _calculate(
        self, request: RouteReconciliationCalculationRequest
    ) -> RouteReconciliationCampaignResultDocument:
        """Authenticate input, decode it, and execute the typed Workflow."""
        self._authenticate_input(request)
        specification = RouteReconciliationCampaignInputDeserializer().execute(
            request.encoded_documents.input_document
        )
        baseline = RouteReconciliationBaselineLoader().execute(
            specification, request.repository_root
        )
        return RouteReconciliationCampaignWorkflow().execute(
            specification, baseline, request.provenance
        )

    def _authenticate_input(
        self, request: RouteReconciliationCalculationRequest
    ) -> None:
        """Bind encapsulated and repository input bytes to declared provenance."""
        expected = request.provenance.input_sha256
        encapsulated = hashlib.sha256(
            request.encoded_documents.input_document
        ).hexdigest()
        if encapsulated != expected:
            raise ValueError("encapsulated input sha256 mismatch")
        retained = hashlib.sha256(
            (request.repository_root / request.provenance.input_path).read_bytes()
        ).hexdigest()
        if retained != expected:
            raise ValueError("repository input sha256 mismatch")

    def _retained_provenance(self) -> RouteReconciliationProvenance:
        """Decode only the fixed retained provenance needed for correlation."""
        root = self._decode(self.encoded_documents.retained_result_document)
        provenance_value = root.get("provenance")
        if not isinstance(provenance_value, dict):
            raise ValueError("retained provenance must be an object")
        provenance = provenance_value
        expected = {
            "input_path",
            "input_sha256",
            "script_path",
            "script_sha256",
            "python_version",
            "numpy_version",
        }
        if set(provenance) != expected:
            raise ValueError("retained provenance fields are unsupported")
        return RouteReconciliationProvenance(
            input_path=self._string(provenance["input_path"], "input_path"),
            input_sha256=self._string(provenance["input_sha256"], "input_sha256"),
            script_path=self._string(provenance["script_path"], "script_path"),
            script_sha256=self._string(provenance["script_sha256"], "script_sha256"),
            python_version=self._string(provenance["python_version"], "python_version"),
            numpy_version=self._string(provenance["numpy_version"], "numpy_version"),
        )

    @staticmethod
    def _decode(payload: bytes) -> dict[str, JsonValue]:
        """Decode strict JSON through the shared campaign boundary."""
        return Periodic1DCampaignJsonDecoder().document(payload)

    @staticmethod
    def _string(value: JsonValue, name: str) -> str:
        """Require one nonempty string field."""
        if not isinstance(value, str) or not value:
            raise ValueError(f"{name} must be a nonempty string")
        return value
