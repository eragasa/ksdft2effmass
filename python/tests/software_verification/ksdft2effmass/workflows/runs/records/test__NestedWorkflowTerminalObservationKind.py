r"""Software verification of ``NestedWorkflowTerminalObservationKind``.

Evidence profile: claim_bearing

Bounded artifact scope: the exact terminal-only enum vocabulary.

Facet and represented meaning

Confirmed, rejected and indeterminate are observations; pending is not terminal.

Intrinsic and cross-object scope

This checks enum construction, not variant fields or retained history closure.

VVUQ and scientific exclusions

Represented labels establish no child execution, replay, authority or science.
"""

import pytest
from ksdft2effmass.workflows import NestedWorkflowTerminalObservationKind

pytestmark = pytest.mark.software_verification
SUT = NestedWorkflowTerminalObservationKind


class TestNestedWorkflowTerminalObservationKind:
    """Own the terminal observation vocabulary."""

    def test_field__members__matches_exact_inventory(self) -> None:
        """Expose exactly the three terminal observation variants.

        Evidence ID: SV-WFR-NESTED-TERMINAL-KIND-001

        Requirement: The enum contains confirmed, rejected and indeterminate only.

        Method: Inspect public enum names and values, including possible aliases.

        Oracle: The independently stated terminal-only vocabulary.

        Acceptance: Exact name/value inventory equality.

        Interpretation: Pending is not represented as terminal evidence.

        Limitations: Enum members alone do not establish valid observation fields.
        """
        assert tuple(
            (name, member.value) for name, member in SUT.__members__.items()
        ) == (
            ("CONFIRMED", "confirmed"),
            ("REJECTED", "rejected"),
            ("INDETERMINATE", "indeterminate"),
        )

    @pytest.mark.parametrize(
        "value",
        (
            pytest.param("pending", id="pending_intent"),
            pytest.param("cancelled", id="unsupported_cancellation"),
            pytest.param("CONFIRMED", id="noncanonical_capitalization"),
        ),
    )
    def test_constructor__terminal_only__rejects_other_labels(self, value: str) -> None:
        """Reject states outside the closed enum.

        Evidence ID: SV-WFR-NESTED-TERMINAL-KIND-002

        Requirement: No pending, cancellation or normalized alternative is added.

        Method: Construct from explicit nonterminal or misspelled strings.

        Oracle: Closed exact enum membership.

        Acceptance: ValueError for each label.

        Interpretation: Unsupported states are not silently reinterpreted.

        Limitations: This does not validate an invocation lifecycle.
        """
        with pytest.raises(ValueError):
            SUT(value)
