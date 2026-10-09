"""Encapsulating façade for the finite-rank analytical oracle."""

import hashlib
from dataclasses import dataclass
from pathlib import Path

from ksdft2effmass.periodic1d.campaign.serialization import (
    Periodic1DCampaignJsonDecoder,
)

from .contracts import FiniteRankOracleProvenance
from .encoded_documents import FiniteRankOracleEncodedDocuments
from .input_decoding import FiniteRankOracleCampaignInputDeserializer
from .parent_data import FiniteRankOracleParentDataLoader
from .result_documents import FiniteRankOracleCampaignResultDocument
from .verification import (
    FiniteRankOracleCampaignVerifier,
    FiniteRankOracleVerificationRequest,
    FiniteRankOracleVerificationResult,
)
from .workflow import FiniteRankOracleCampaignWorkflow


@dataclass(frozen=True, slots=True)
class FiniteRankOracleResultCorrelation:
    """Report semantic and canonical retained-result identity channels.

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
class FiniteRankOracleCampaign:
    """Encapsulate one finite-rank-oracle campaign behind a narrow façade.

    Parameters
    ----------
    encoded_documents
        Immutable exact input and retained-result byte documents.

    Raises
    ------
    TypeError
        An argument does not have the required exact public type.

    Notes
    -----
    Encoded documents and repository location remain separate. Calculation and
    retained correlation receive an explicit root at their executing operation
    boundaries. Independent verification places the same kind of location in
    :class:`FiniteRankOracleVerificationRequest`. No location is inferred from
    encoded bytes, filenames, or digests. Root validation and retained-correlation
    parsing are instance-owned behavior rather than static namespace utilities.
    """

    encoded_documents: FiniteRankOracleEncodedDocuments

    def __post_init__(self) -> None:
        """Require the exact encoded-document type."""
        if type(self.encoded_documents) is not FiniteRankOracleEncodedDocuments:
            raise TypeError(
                "encoded_documents must be FiniteRankOracleEncodedDocuments"
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
    ) -> FiniteRankOracleCampaignResultDocument:
        """Calculate the finite campaign under explicit adapter provenance.

        Parameters
        ----------
        repository_root
            Absolute filesystem base for repository-relative authenticated sources.
        input_path, script_path
            Explicit retained provenance paths; the operation does not derive them.
        input_sha256, script_sha256
            Explicit lowercase content identities retained by campaign provenance.
        python_version, numpy_version
            Explicit nonempty software-version strings retained by provenance.

        Returns
        -------
        FiniteRankOracleCampaignResultDocument
            Canonically encoded finite synthetic campaign result.

        Raises
        ------
        TypeError
            If ``repository_root`` is not :class:`pathlib.Path`.
        ValueError
            If ``repository_root`` is relative or downstream contracts fail.

        Notes
        -----
        Root validation is lexical and performs no ambient path resolution. Execution
        then decodes input, authenticates explicitly declared sources, and runs the
        finite represented comparison. Success does not establish an infinite-system
        limit, material validation, transferability, UQ, or acceptance.
        """
        self._check_repository_root(repository_root)
        return self._calculate(
            repository_root,
            FiniteRankOracleProvenance(
                input_path,
                input_sha256,
                script_path,
                script_sha256,
                python_version,
                numpy_version,
            ),
        )

    def retained_result(self) -> FiniteRankOracleCampaignResultDocument:
        """Return retained bytes without calculating or verifying them.

        Returns
        -------
        FiniteRankOracleCampaignResultDocument
            Immutable document retaining the exact result bytes.
        """
        return FiniteRankOracleCampaignResultDocument(
            self.encoded_documents.retained_result_document
        )

    def correlate_retained(
        self, repository_root: Path
    ) -> FiniteRankOracleResultCorrelation:
        """Recalculate with an explicit root and report retained identity channels.

        Parameters
        ----------
        repository_root
            Absolute filesystem base for authenticated repository-relative sources.

        Returns
        -------
        FiniteRankOracleResultCorrelation
            Semantic-document and canonical-byte correlation diagnostics.

        Raises
        ------
        TypeError
            If ``repository_root`` is not :class:`pathlib.Path`.
        ValueError
            If ``repository_root`` is relative, retained provenance is unsupported, or
            downstream authentication or calculation fails.

        Notes
        -----
        The root is validated before retained-result decoding or source access.
        Correlation establishes result identity under the executed finite campaign; it
        is not independent verification, provenance by itself, oracle qualification,
        scientific validation, uncertainty quantification, or acceptance.
        """
        self._check_repository_root(repository_root)
        retained = self.retained_result()
        calculated = self._calculate(repository_root, self._retained_provenance())
        decoder = Periodic1DCampaignJsonDecoder()
        return FiniteRankOracleResultCorrelation(
            semantic_identity=(
                decoder.document(calculated.payload)
                == decoder.document(retained.payload)
            ),
            canonical_byte_identity=calculated.payload == retained.payload,
            calculated_sha256=calculated.sha256,
            retained_sha256=retained.sha256,
        )

    def verify_retained(
        self, repository_root: Path
    ) -> FiniteRankOracleVerificationResult:
        """Independently authenticate and reconstruct the retained finite result.

        ``FiniteRankOracleVerificationRequest`` owns and validates the explicit root
        before the verifier reads authenticated sources. Verification remains bounded to
        the represented synthetic campaign and is not a production-oracle qualification
        or material-validation decision.

        Parameters
        ----------
        repository_root
            Explicit absolute root confining authenticated repository-relative access.

        Returns
        -------
        FiniteRankOracleVerificationResult
            Independent authentication and finite reconstruction result.
        """
        return FiniteRankOracleCampaignVerifier().execute(
            FiniteRankOracleVerificationRequest(self.encoded_documents, repository_root)
        )

    def _check_repository_root(self, repository_root: Path) -> None:
        """Require this campaign's explicit absolute base without accessing it."""
        if not isinstance(repository_root, Path):
            raise TypeError("repository_root must be pathlib.Path")
        if not repository_root.is_absolute():
            raise ValueError("repository_root must be absolute")

    def _calculate(
        self, repository_root: Path, provenance: FiniteRankOracleProvenance
    ) -> FiniteRankOracleCampaignResultDocument:
        """Authenticate input, decode it, and execute the campaign Workflow."""
        self._authenticate_input(repository_root, provenance)
        specification = FiniteRankOracleCampaignInputDeserializer().execute(
            self.encoded_documents.input_document
        )
        parent = FiniteRankOracleParentDataLoader().execute(
            specification, repository_root
        )
        return FiniteRankOracleCampaignWorkflow().execute(
            specification, parent, provenance
        )

    def _authenticate_input(
        self, repository_root: Path, provenance: FiniteRankOracleProvenance
    ) -> None:
        """Bind encapsulated and repository input bytes to declared provenance."""
        expected = provenance.input_sha256
        encapsulated = hashlib.sha256(self.encoded_documents.input_document).hexdigest()
        if encapsulated != expected:
            raise ValueError("encapsulated input sha256 mismatch")
        retained = hashlib.sha256(
            (repository_root / provenance.input_path).read_bytes()
        ).hexdigest()
        if retained != expected:
            raise ValueError("repository input sha256 mismatch")

    def _retained_provenance(self) -> FiniteRankOracleProvenance:
        """Decode the fixed retained provenance used only for correlation."""
        decoder = Periodic1DCampaignJsonDecoder()
        root = decoder.document(self.encoded_documents.retained_result_document)
        value = decoder.mapping(root.get("provenance"), "retained provenance")
        expected = {
            "input_path",
            "input_sha256",
            "script_path",
            "script_sha256",
            "python_version",
            "numpy_version",
        }
        if set(value) != expected:
            raise ValueError("retained provenance fields are unsupported")
        return FiniteRankOracleProvenance(
            decoder.nonempty_string(value["input_path"], "input_path"),
            decoder.sha256(value["input_sha256"], "input_sha256"),
            decoder.nonempty_string(value["script_path"], "script_path"),
            decoder.sha256(value["script_sha256"], "script_sha256"),
            decoder.nonempty_string(value["python_version"], "python_version"),
            decoder.nonempty_string(value["numpy_version"], "numpy_version"),
        )
