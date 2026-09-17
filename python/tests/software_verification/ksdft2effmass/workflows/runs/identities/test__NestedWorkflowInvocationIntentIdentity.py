r"""Software verification of ``NestedWorkflowInvocationIntentIdentity``.

Evidence profile: claim_bearing

Bounded artifact scope: immutable nominal child-intent identity construction.

Facet and represented meaning

Exact nonempty strings are preserved without normalization or nominal aliasing.

Intrinsic and cross-object scope

The identity owns string validity. Resolution into retained history is excluded.

VVUQ and scientific exclusions

Synthetic labels establish no child creation, replay, persistence or science.
"""

from dataclasses import FrozenInstanceError

import pytest
from ksdft2effmass.workflows import (
    NestedWorkflowInvocationIdentity,
    NestedWorkflowInvocationIntentIdentity,
)

pytestmark = pytest.mark.software_verification
SUT = NestedWorkflowInvocationIntentIdentity


class TestNestedWorkflowInvocationIntentIdentity:
    """Own the exact nominal identity contract."""

    @pytest.mark.parametrize(
        "value",
        (
            pytest.param("intent.one", id="ordinary_label"),
            pytest.param("  Δ\n", id="unicode_without_normalization"),
        ),
    )
    def test_constructor__value__preserves_exact_string(self, value: str) -> None:
        """Preserve the input label exactly.

        Evidence ID: SV-WFR-NESTED-INTENT-ID-001

        Requirement: Nonempty built-in strings are not normalized.

        Method: Construct from each explicit string partition.

        Oracle: The independently supplied string.

        Acceptance: The stored value equals the input exactly.

        Interpretation: Construction retains the represented label.

        Limitations: No identity resolution or retained intent is established.
        """
        assert SUT(value).value == value

    @pytest.mark.parametrize(
        "value",
        (
            pytest.param(True, id="boolean"),
            pytest.param(1, id="integer"),
            pytest.param(b"intent", id="encoded_bytes"),
        ),
    )
    def test_constructor__value__rejects_non_string(
        self, value: bool | int | bytes
    ) -> None:
        """Reject wrong semantic types without conversion.

        Evidence ID: SV-WFR-NESTED-INTENT-ID-002

        Requirement: The nominal identity accepts only exact strings.

        Method: Call the public constructor with a closed invalid-type union.

        Oracle: The documented TypeError taxonomy.

        Acceptance: Each input raises TypeError.

        Interpretation: No implicit string coercion occurs.

        Limitations: The partitions are bounded software inputs.
        """
        with pytest.raises(TypeError, match="must be a string"):
            SUT(value)  # type: ignore[arg-type]

    def test_constructor__value__rejects_empty_string(self) -> None:
        """Reject an empty label rather than inventing an identity.

        Evidence ID: SV-WFR-NESTED-INTENT-ID-003

        Requirement: An identity value must be nonempty.

        Method: Construct from an empty built-in string.

        Oracle: The nonempty-string invariant.

        Acceptance: ValueError reports the empty value.

        Interpretation: Empty labels cannot identify intent.

        Limitations: No uniqueness across stored records is checked.
        """
        with pytest.raises(ValueError, match="must not be empty"):
            SUT("")

    def test_method__eq__preserves_nominal_distinction(self) -> None:
        """Keep new and combined intent identities distinct dictionary keys.

        Evidence ID: SV-WFR-NESTED-INTENT-ID-004

        Requirement: String equality does not alias the two nominal intent types.

        Method: Compare equal new labels and a same-string combined identity.

        Oracle: Frozen nominal value semantics.

        Acceptance: Equal new identities compare/hash equally and remain distinct
        from the combined identity in a set.

        Interpretation: Typed references can retain which intent source they name.

        Limitations: This does not resolve an observation reference.
        """
        first = SUT("same")
        second = SUT("same")
        combined = NestedWorkflowInvocationIdentity("same")
        assert first == second
        assert hash(first) == hash(second)
        assert len({first, second, combined}) == 2

    def test_field__value__is_frozen(self) -> None:
        """Reject ordinary public mutation.

        Evidence ID: SV-WFR-NESTED-INTENT-ID-005

        Requirement: The nominal record is frozen.

        Method: Assign a new value through the public field.

        Oracle: Frozen dataclass assignment semantics.

        Acceptance: FrozenInstanceError is raised and the original value remains.

        Interpretation: Ordinary callers cannot rewrite this identity.

        Limitations: Deliberate Python runtime bypasses are excluded.
        """
        identity = SUT("original")
        with pytest.raises(FrozenInstanceError):
            identity.value = "changed"  # type: ignore[misc]
        assert identity.value == "original"
