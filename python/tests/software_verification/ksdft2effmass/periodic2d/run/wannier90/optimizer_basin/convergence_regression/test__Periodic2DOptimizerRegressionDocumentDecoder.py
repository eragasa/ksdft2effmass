r"""Routine strict and historical-wire decoding evidence for row 054.

Evidence profile: routine

The tests establish fail-closed schema adaptation. They do not authenticate repository
artifacts or establish the retained statistical model's scientific validity.
"""

from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin import (
    convergence_regression as regression,
)
from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.convergence_regression.decode import (  # noqa: E501
    Periodic2DOptimizerRegressionDocumentDecoder,
)
from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.convergence_regression.records import (  # noqa: E501
    OptimizerRegressionDecodedDocuments,
)

Periodic2DOptimizerRegressionEncodedDocuments = (
    regression.Periodic2DOptimizerRegressionEncodedDocuments
)

pytestmark = pytest.mark.software_verification


class TestPeriodic2DOptimizerRegressionDocumentDecoder:
    """Own routine decoder evidence for row 054."""

    def retained_payloads(self) -> tuple[bytes, bytes, bytes]:
        """Return exact maintained source, analyzer, and regression bytes."""
        root = Path(__file__).resolve().parents[9]
        base = root / "calculations/research-monograph/periodic-2d-optimizer-basin"
        return (
            base.joinpath("standalone-result.json").read_bytes(),
            base.joinpath("analyze_standalone_convergence_regression.py").read_bytes(),
            base.joinpath("standalone-convergence-regression.json").read_bytes(),
        )

    def test_execute__adapts_retained_wires_to_closed_immutable_records(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-054-DECODE-001.

        Requirement: The historical source extension is bounded to unconsumed fields,
        while consumed finite source fields and strict regression JSON become closed
        immutable records.

        Acceptance: The retained documents decode to the exact aggregate type, endpoint
        and category sequences are tuples, and decoded state is frozen.
        """
        source, analyzer, regression = self.retained_payloads()
        decoded = Periodic2DOptimizerRegressionDocumentDecoder().execute(
            Periodic2DOptimizerRegressionEncodedDocuments(source, analyzer, regression)
        )
        assert type(decoded) is OptimizerRegressionDecodedDocuments
        assert type(decoded.source_result.endpoints) is tuple
        assert type(decoded.regression_result.category_estimates) is tuple
        with pytest.raises(FrozenInstanceError):
            decoded.source_result = decoded.source_result  # type: ignore[misc]

    def test_execute__rejects_ambiguous_or_nonfinite_consumed_source_fields(
        self,
    ) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-054-DECODE-002.

        Requirement: Historical unconsumed ``Infinity`` values do not permit duplicate
        keys or nonfinite values in any consumed endpoint field.

        Acceptance: A duplicate top-level schema key and a consumed ``Infinity`` each
        fail closed.
        """
        source, analyzer, regression = self.retained_payloads()
        duplicate = source.replace(
            b'  "schema_version": 1\n',
            b'  "schema_version": 1,\n  "schema_version": 1\n',
            1,
        )
        with pytest.raises(ValueError, match="duplicate JSON key"):
            Periodic2DOptimizerRegressionDocumentDecoder().execute(
                Periodic2DOptimizerRegressionEncodedDocuments(
                    duplicate, analyzer, regression
                )
            )
        nonfinite = source.replace(
            b'"effective_total_iterations": 2164',
            b'"effective_total_iterations": Infinity',
            1,
        )
        with pytest.raises(ValueError, match="must be finite"):
            Periodic2DOptimizerRegressionDocumentDecoder().execute(
                Periodic2DOptimizerRegressionEncodedDocuments(
                    nonfinite, analyzer, regression
                )
            )

    @pytest.mark.parametrize("constant", (b"Infinity", b"-Infinity", b"NaN"))
    def test_execute__rejects_regression_nonfinite_constants(
        self, constant: bytes
    ) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-054-DECODE-003.

        Requirement: Regression JSON rejects every Python-JSON nonfinite extension.

        Acceptance: Positive infinity, negative infinity, and NaN each raise
        ``ValueError`` before schema adaptation.
        """
        source, analyzer, regression = self.retained_payloads()
        nonfinite = regression.replace(
            b'"negative_log_likelihood": 361.4833736318742',
            b'"negative_log_likelihood": ' + constant,
            1,
        )
        with pytest.raises(ValueError, match="non-finite JSON constant"):
            Periodic2DOptimizerRegressionDocumentDecoder().execute(
                Periodic2DOptimizerRegressionEncodedDocuments(
                    source, analyzer, nonfinite
                )
            )

    def test_execute__rejects_regression_duplicate_and_selects_schema_first(
        self,
    ) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-054-DECODE-004.

        Requirement: Regression keys are unique and schema selection precedes access to
        version-one fields.

        Acceptance: Duplicate keys raise ``ValueError``; unsupported schema raises
        ``AssertionError`` without a missing-field error.
        """
        source, analyzer, regression = self.retained_payloads()
        duplicate = regression.replace(
            b'  "schema_version": 1,',
            b'  "schema_version": 1,\n  "schema_version": 1,',
            1,
        )
        with pytest.raises(ValueError, match="duplicate JSON key"):
            Periodic2DOptimizerRegressionDocumentDecoder().execute(
                Periodic2DOptimizerRegressionEncodedDocuments(
                    source, analyzer, duplicate
                )
            )
        with pytest.raises(AssertionError, match="regression schema changed"):
            Periodic2DOptimizerRegressionDocumentDecoder().execute(
                Periodic2DOptimizerRegressionEncodedDocuments(
                    source, analyzer, b'{"schema_version": 2}'
                )
            )
