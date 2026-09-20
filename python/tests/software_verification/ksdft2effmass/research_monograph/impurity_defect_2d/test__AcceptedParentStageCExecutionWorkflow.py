r"""Software verification of ``AcceptedParentStageCExecutionWorkflow``.

Evidence profile: routine

Bounded artifact scope: fail-closed authorization ordering before accepted-parent reads.

Facet and represented meaning

The Workflow composes exact authorization validation, accepted-parent adaptation,
evaluation, and retained-package finalization. This module exercises only its pre-read
authority refusal with an authored nonexecuting fixture.

Intrinsic and cross-object scope

The Workflow owns the protected execution sequence. Its accepted execution remains
historical and is not repeated by this test.

VVUQ and scientific exclusions

This is software verification of refusal behavior. It performs no accepted-parent read
or protected execution and establishes no scientific validation, uncertainty
quantification, publication, or release status.
"""

from pathlib import Path

import pytest
from stage_c_parent.workflows import AcceptedParentStageCExecutionWorkflow

pytestmark = pytest.mark.software_verification
SUT = AcceptedParentStageCExecutionWorkflow


class TestAcceptedParentStageCExecutionWorkflow:
    """Own fail-closed authorization evidence for the protected Workflow."""

    @staticmethod
    def repository_root() -> Path:
        """Return the repository containing the Stage C artifacts.

        Evidence ID: Helper owns no identifier.
        """

        return Path(__file__).resolve().parents[6]

    @classmethod
    def stage_directory(cls) -> Path:
        """Return the maintained defect-2D calculation directory.

        Evidence ID: Helper owns no identifier.
        """

        return (
            cls.repository_root() / "calculations/research-monograph/impurity-defect-2d"
        )

    @classmethod
    def authorization_fixture(cls) -> Path:
        """Return the nonexecuting future-authorization wire fixture.

        Evidence ID: Helper owns no identifier.
        """

        return (
            Path(__file__).resolve().parent
            / "resources/stage-c-execution-authorization-authored-fixture.json"
        )

    def test_artifact__authorization__rejects_nonexecuting_fixture_before_parent_read(
        self,
    ) -> None:
        """Fail before accepted inputs when execution authority is not exact.

        Evidence ID: SV-RM-DEFECT2D-C-024

        Requirement: Post-HC17 execution mode still requires the exact canonical
        authorization path and must preserve the immutable retained result when a
        different schema-valid authorization is supplied.

        Method: Capture the canonical retained result bytes, then invoke the Workflow
        with the authored authorization at its maintained fixture path rather than the
        consumed HC17 authorization path.

        Oracle: HC17 binds one exact consumed authorization and immutable result;
        the authored fixture is not accepted execution authority.

        Acceptance: The Workflow fails with the authorization-path mismatch, and the
        canonical retained result bytes remain exactly unchanged.

        Interpretation: Passing verifies fail-closed pre-read authority ordering and
        byte-preserving refusal without rerun or overwrite.

        Limitations: Rejection proves authority-path enforcement and result
        immutability, not another accepted-parent execution.
        """

        stage = self.stage_directory()
        output = stage / "stage-c-accepted-parent-result.json"
        retained_result = output.read_bytes()
        with pytest.raises(ValueError, match="execution authorization path differs"):
            SUT().execute(
                stage / "stage-c-accepted-parent-design.json",
                self.authorization_fixture(),
                self.repository_root(),
                output,
            )
        assert output.read_bytes() == retained_result
