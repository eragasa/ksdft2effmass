"""Encapsulating façade for separated continuum refinement."""

from dataclasses import dataclass
from pathlib import Path

from ksdft2effmass.periodic1d.campaign.serialization import (
    Periodic1DCampaignJsonDecoder,
)
from ksdft2effmass.serialization.json import JsonValue

from .encoded_documents import ContinuumRefinementEncodedDocuments
from .result_documents import ContinuumRefinementCampaignResultDocument
from .verification import (
    ContinuumRefinementCampaignVerifier,
    ContinuumRefinementVerificationRequest,
    ContinuumRefinementVerificationResult,
)
from .workflow import (
    ContinuumParentLoader,
    ContinuumRefinementCampaignCalculator,
    ContinuumRefinementInputDeserializer,
    ContinuumRefinementProvenance,
    ContinuumResultSerializer,
)


@dataclass(frozen=True, slots=True)
class ContinuumRefinementResultCorrelation:
    """Report semantic and canonical retained identity channels.

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
    """

    semantic_identity: bool
    canonical_byte_identity: bool
    calculated_sha256: str
    retained_sha256: str


@dataclass(frozen=True, slots=True)
class ContinuumRefinementCampaign:
    """Encapsulate one separated continuum-refinement campaign.

    Parameters
    ----------
    encoded_documents
        Immutable exact input and retained-result byte documents.

    Raises
    ------
    TypeError
        An argument does not have the required exact public type.
    """

    encoded_documents: ContinuumRefinementEncodedDocuments

    def __post_init__(self) -> None:
        """Require the exact encoded-document type."""
        if type(self.encoded_documents) is not ContinuumRefinementEncodedDocuments:
            raise TypeError(
                "encoded_documents must be ContinuumRefinementEncodedDocuments"
            )

    def retained_result(self) -> ContinuumRefinementCampaignResultDocument:
        """Return retained bytes without calculating or verifying them.

        Returns
        -------
        ContinuumRefinementCampaignResultDocument
            Immutable document retaining the exact result bytes.
        """
        return ContinuumRefinementCampaignResultDocument(
            self.encoded_documents.retained_result_document
        )

    def correlate_retained(
        self, repository_root: Path
    ) -> ContinuumRefinementResultCorrelation:
        """Recalculate using an explicit root and report identity correlation.

        Parameters
        ----------
        repository_root
            Absolute filesystem base for repository-relative authenticated sources.

        Returns
        -------
        ContinuumRefinementResultCorrelation
            Separate semantic, canonical-byte, and digest identity channels.

        Raises
        ------
        TypeError
            If ``repository_root`` is not a :class:`pathlib.Path`.
        ValueError
            If ``repository_root`` is relative, encoded documents are invalid, source
            authentication fails, or reconstructed semantic data are incompatible.
        OSError
            If an authenticated source cannot be read from the explicit root.

        Notes
        -----
        The root is operation input rather than encoded-document state. This method
        performs authenticated source access and calculation; merely supplying a path
        establishes neither provenance nor scientific validity. Retained provenance is
        reused only for historical identity correlation, not as a claim of current
        execution under that provenance.
        """
        self._check_repository_root(repository_root)
        retained = self.retained_result()
        calculated = self._calculate(repository_root, self._retained_provenance())
        return ContinuumRefinementResultCorrelation(
            semantic_identity=self._decode(calculated.payload)
            == self._decode(retained.payload),
            canonical_byte_identity=calculated.payload == retained.payload,
            calculated_sha256=calculated.sha256,
            retained_sha256=retained.sha256,
        )

    def verify_retained(
        self, repository_root: Path
    ) -> ContinuumRefinementVerificationResult:
        """Independently authenticate and reconstruct every refinement axis.

        Parameters
        ----------
        repository_root
            Absolute filesystem base placed in the typed verification request.

        Returns
        -------
        ContinuumRefinementVerificationResult
            Separate source, structural, numerical, count, and digest channels.

        Raises
        ------
        TypeError
            If the root or composed request values use unsupported public types.
        ValueError
            If the root is relative or authentication, structure, or reconstruction
            disagrees with the retained documents.
        OSError
            If an authenticated source cannot be read from the explicit root.

        Notes
        -----
        Verification is bounded to the retained synthetic campaign and does not prove an
        asymptotic theorem, material validity, transferability, UQ, or acceptance.
        """
        return ContinuumRefinementCampaignVerifier().execute(
            ContinuumRefinementVerificationRequest(
                self.encoded_documents, repository_root
            )
        )

    @staticmethod
    def _check_repository_root(repository_root: Path) -> None:
        """Require an explicit absolute root before retained correlation accesses files.

        Raises
        ------
        TypeError
            If ``repository_root`` is not a :class:`pathlib.Path`.
        ValueError
            If ``repository_root`` is relative.
        """
        if not isinstance(repository_root, Path):
            raise TypeError("repository_root must be pathlib.Path")
        # Keep the caller-owned path unresolved: lexical absoluteness is required, but
        # source existence and authentication belong to the subsequent loader Action.
        if not repository_root.is_absolute():
            raise ValueError("repository_root must be absolute")

    def _calculate(
        self, repository_root: Path, provenance: ContinuumRefinementProvenance
    ) -> ContinuumRefinementCampaignResultDocument:
        """Decode, authenticate, calculate, and serialize one campaign."""
        specification = ContinuumRefinementInputDeserializer().execute(
            self.encoded_documents.input_document
        )
        parent = ContinuumParentLoader().execute(repository_root, specification)
        result = ContinuumRefinementCampaignCalculator(specification, parent).execute(
            provenance
        )
        return ContinuumRefinementCampaignResultDocument(
            ContinuumResultSerializer().execute(result)
        )

    def _retained_provenance(self) -> ContinuumRefinementProvenance:
        """Decode retained provenance used only for identity correlation."""
        root = self._decode(self.encoded_documents.retained_result_document)
        value = root.get("provenance")
        if not isinstance(value, dict):
            raise ValueError("retained provenance must be an object")
        implementations = value.get("implementation_identities")
        implementation_path: str | None = None
        implementation_sha256: str | None = None
        if implementations is not None:
            if not isinstance(implementations, list) or len(implementations) != 1:
                raise ValueError("one retained implementation identity is required")
            identity = implementations[0]
            if not isinstance(identity, dict):
                raise ValueError("implementation identity must be an object")
            implementation_path = self._string(identity.get("path"), "path")
            implementation_sha256 = self._string(identity.get("sha256"), "sha256")
        return ContinuumRefinementProvenance(
            input_sha256=self._string(value.get("input_sha256"), "input_sha256"),
            implementation_path=implementation_path,
            implementation_sha256=implementation_sha256,
            python_version=self._string(value.get("python"), "python"),
            numpy_version=self._string(value.get("numpy"), "numpy"),
        )

    @staticmethod
    def _decode(payload: bytes) -> dict[str, JsonValue]:
        """Decode strict UTF-8 JSON through the shared campaign boundary."""
        return Periodic1DCampaignJsonDecoder().document(payload)

    @staticmethod
    def _string(value: JsonValue, name: str) -> str:
        """Require one nonempty string."""
        if not isinstance(value, str) or not value:
            raise ValueError(f"{name} must be a nonempty string")
        return value
