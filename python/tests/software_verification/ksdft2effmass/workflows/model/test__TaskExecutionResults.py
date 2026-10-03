r"""Software verification of concrete nonempty ``TaskExecutionResults``."""

from dataclasses import dataclass, field

import pytest

from ksdft2effmass.workflows import (
    AbstractResultObject,
    ResultObjectIdentity,
    TaskExecutionResults,
)

pytestmark = pytest.mark.software_verification


class TestTaskExecutionResults:
    """Verify exact nominal membership, order, and identity uniqueness."""

    @dataclass(frozen=True, slots=True)
    class SyntheticResult(AbstractResultObject):
        identity: ResultObjectIdentity = field()

    def test_constructor_retains_nonempty_ordered_nominal_results(self) -> None:
        """Retain an ordered tuple of distinct nominal results.

        Evidence ID: SV-WFM-TASK-EXECUTION-RESULTS-001
        """
        first = self.SyntheticResult(ResultObjectIdentity("result.first"))
        second = self.SyntheticResult(ResultObjectIdentity("result.second"))
        value = TaskExecutionResults((first, second))
        assert value.results == (first, second)

    def test_constructor_rejects_wrong_container_and_identity_types(self) -> None:
        """Require an exact tuple and exact result identities."""
        result = self.SyntheticResult(ResultObjectIdentity("result.one"))

        @dataclass(frozen=True, slots=True)
        class WrongIdentityResult(AbstractResultObject):
            identity: str = field()

        with pytest.raises(TypeError, match="tuple"):
            TaskExecutionResults([result])  # type: ignore[arg-type]
        with pytest.raises(TypeError, match="ResultObjectIdentity"):
            TaskExecutionResults(  # type: ignore[arg-type]
                (WrongIdentityResult("result.wrong-identity"),)
            )

    def test_constructor_rejects_empty_or_duplicate_results(self) -> None:
        """Close the successful execution boundary against absent evidence.

        Evidence ID: SV-WFM-TASK-EXECUTION-RESULTS-002
        """
        result = self.SyntheticResult(ResultObjectIdentity("result.duplicate"))
        duplicate = self.SyntheticResult(ResultObjectIdentity("result.duplicate"))
        with pytest.raises(ValueError, match="must not be empty"):
            TaskExecutionResults(())
        with pytest.raises(ValueError, match="identities must be unique"):
            TaskExecutionResults((result, duplicate))

    def test_constructor_rejects_structural_lookalike(self) -> None:
        """Require explicit nominal result inheritance.

        Evidence ID: SV-WFM-TASK-EXECUTION-RESULTS-003
        """

        @dataclass(frozen=True, slots=True)
        class ResultLookalike:
            identity: ResultObjectIdentity

        with pytest.raises(TypeError, match="AbstractResultObject"):
            TaskExecutionResults(  # type: ignore[arg-type]
                (ResultLookalike(ResultObjectIdentity("result.lookalike")),)
            )
