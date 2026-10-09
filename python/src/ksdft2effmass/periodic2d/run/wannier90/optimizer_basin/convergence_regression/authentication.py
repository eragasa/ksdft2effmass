"""Repository-confined authentication for optimizer regression documents."""

import hashlib
from pathlib import Path

from .encoded_documents import Periodic2DOptimizerRegressionEncodedDocuments
from .records import OptimizerRegressionResult

_CAMPAIGN_DIRECTORY = Path(
    "calculations/research-monograph/periodic-2d-optimizer-basin"
)
_SOURCE_RESULT_PATH = _CAMPAIGN_DIRECTORY / "standalone-result.json"
_ANALYZER_PATH = _CAMPAIGN_DIRECTORY / "analyze_standalone_convergence_regression.py"
_REGRESSION_PATH = _CAMPAIGN_DIRECTORY / "standalone-convergence-regression.json"
_ANALYZER_SHA256 = "e80c16ab7fd11d86e6c51a344e01790306982f1a628b962611dfd0291d16fe46"


class Periodic2DOptimizerRegressionSourceAuthenticator:
    """Authenticate encapsulated bytes against declarations and repository files."""

    __slots__ = ()

    def execute(
        self,
        documents: Periodic2DOptimizerRegressionEncodedDocuments,
        regression: OptimizerRegressionResult,
        repository_root: Path,
    ) -> None:
        """Authenticate every exact wire owned by the portable campaign.

        Parameters
        ----------
        documents
            Exact encapsulated source, analyzer, and regression bytes.
        regression
            Typed regression record declaring the source-result digest.
        repository_root
            Absolute root that confines all maintained-file reads.

        Raises
        ------
        TypeError
            If an argument has an incompatible exact type.
        ValueError
            If ``repository_root`` is relative or a maintained path escapes it.
        OSError
            If a confined maintained file cannot be read.
        AssertionError
            If an encapsulated or maintained byte identity disagrees.
        """
        if type(documents) is not Periodic2DOptimizerRegressionEncodedDocuments:
            raise TypeError(
                "documents must be Periodic2DOptimizerRegressionEncodedDocuments"
            )
        if type(regression) is not OptimizerRegressionResult:
            raise TypeError("regression must be OptimizerRegressionResult")
        if not isinstance(repository_root, Path):
            raise TypeError("repository_root must be pathlib.Path")
        if not repository_root.is_absolute():
            raise ValueError("repository_root must be absolute")
        resolved_root = repository_root.resolve()
        maintained = (
            (_SOURCE_RESULT_PATH, documents.standalone_result_payload, "source result"),
            (_ANALYZER_PATH, documents.analyzer_payload, "regression analyzer"),
            (_REGRESSION_PATH, documents.regression_payload, "regression result"),
        )
        for relative_path, payload, label in maintained:
            resolved_path = (resolved_root / relative_path).resolve()
            if not resolved_path.is_relative_to(resolved_root):
                raise ValueError(f"{label} must resolve within repository_root")
            if resolved_path.read_bytes() != payload:
                raise AssertionError(f"{label} repository bytes changed")
        if (
            hashlib.sha256(documents.standalone_result_payload).hexdigest()
            != regression.source_result_sha256
        ):
            raise AssertionError("source result identity mismatch")
        if hashlib.sha256(documents.analyzer_payload).hexdigest() != _ANALYZER_SHA256:
            raise AssertionError("regression analyzer identity mismatch")
