"""Repository-confined authentication for standalone optimizer documents."""

import hashlib
from pathlib import Path

from .encoded_documents import Periodic2DOptimizerStandaloneEncodedDocuments
from .records import OptimizerStandaloneGaugeDesign, OptimizerStandaloneResult

_CAMPAIGN_DIRECTORY = Path(
    "calculations/research-monograph/periodic-2d-optimizer-basin"
)
_PROPOSAL_PATH = _CAMPAIGN_DIRECTORY / "standalone-study-proposal.json"
_GAUGES_PATH = _CAMPAIGN_DIRECTORY / "standalone-initial-gauges.json"
_RESULT_PATH = _CAMPAIGN_DIRECTORY / "standalone-result.json"
_EXTRACTOR_PATH = _CAMPAIGN_DIRECTORY / "extract_standalone_results.py"
_PROPOSAL_SHA256 = "d260475252b420d151ebfd7e276e170c1d069e4bbc7ad974d21e911dd6db3485"
_GAUGES_SHA256 = "34ebdb57dbcdb3cb72bb3fbc602a12b3c05b58534d1c028047578afceb1a8f4b"
_RESULT_SHA256 = "add349df1cccd95fc35c1984a21f58d4d5b49b62ba528377ea0f4245e5d5ce9a"
_EXTRACTOR_SHA256 = "c30612ccd886f140fe429f04233b6312601859d8a09328c71312e1fc204fe5c3"


class Periodic2DOptimizerStandaloneSourceAuthenticator:
    """Authenticate exact compact wires and their directly declared extractor."""

    __slots__ = ()

    def execute(
        self,
        documents: Periodic2DOptimizerStandaloneEncodedDocuments,
        gauge_design: OptimizerStandaloneGaugeDesign,
        result: OptimizerStandaloneResult,
        repository_root: Path,
    ) -> None:
        """Authenticate maintained bytes without opening external native run paths.

        Parameters
        ----------
        documents
            Exact encapsulated proposal, initial-gauge, and result bytes.
        gauge_design
            Typed gauge record declaring its proposal identity.
        result
            Typed result record declaring proposal and extractor identities.
        repository_root
            Absolute :class:`pathlib.Path` that confines maintained-file reads.

        Raises
        ------
        TypeError
            If an argument has an incompatible exact software representation.
        ValueError
            If ``repository_root`` is relative or a maintained path escapes it.
        OSError
            If a confined maintained file cannot be read.
        AssertionError
            If any encapsulated, maintained, or declared identity disagrees.
        """
        if type(documents) is not Periodic2DOptimizerStandaloneEncodedDocuments:
            raise TypeError(
                "documents must be Periodic2DOptimizerStandaloneEncodedDocuments"
            )
        if type(gauge_design) is not OptimizerStandaloneGaugeDesign:
            raise TypeError("gauge_design must be OptimizerStandaloneGaugeDesign")
        if type(result) is not OptimizerStandaloneResult:
            raise TypeError("result must be OptimizerStandaloneResult")
        if not isinstance(repository_root, Path):
            raise TypeError("repository_root must be pathlib.Path")
        if not repository_root.is_absolute():
            raise ValueError("repository_root must be absolute")
        resolved_root = repository_root.resolve()
        maintained = (
            (_PROPOSAL_PATH, documents.proposal_payload, "proposal"),
            (_GAUGES_PATH, documents.initial_gauges_payload, "initial gauges"),
            (_RESULT_PATH, documents.result_payload, "standalone result"),
        )
        for relative_path, payload, label in maintained:
            resolved_path = (resolved_root / relative_path).resolve()
            if not resolved_path.is_relative_to(resolved_root):
                raise ValueError(f"{label} must resolve within repository_root")
            if resolved_path.read_bytes() != payload:
                raise AssertionError(f"{label} repository bytes changed")
        self._require_digest(documents.proposal_payload, _PROPOSAL_SHA256, "proposal")
        self._require_digest(
            documents.initial_gauges_payload, _GAUGES_SHA256, "initial gauges"
        )
        self._require_digest(documents.result_payload, _RESULT_SHA256, "result")
        if gauge_design.proposal_sha256 != _PROPOSAL_SHA256:
            raise AssertionError("gauge proposal identity mismatch")
        if result.provenance.proposal_sha256 != _PROPOSAL_SHA256:
            raise AssertionError("result proposal identity mismatch")
        if result.provenance.extractor_sha256 != _EXTRACTOR_SHA256:
            raise AssertionError("declared extractor identity mismatch")
        extractor = (resolved_root / _EXTRACTOR_PATH).resolve()
        if not extractor.is_relative_to(resolved_root):
            raise ValueError("extractor must resolve within repository_root")
        self._require_digest(extractor.read_bytes(), _EXTRACTOR_SHA256, "extractor")

    def _require_digest(self, payload: bytes, expected: str, label: str) -> None:
        """Require one exact SHA-256 identity without assigning provenance meaning."""
        if hashlib.sha256(payload).hexdigest() != expected:
            raise AssertionError(f"{label} identity mismatch")
