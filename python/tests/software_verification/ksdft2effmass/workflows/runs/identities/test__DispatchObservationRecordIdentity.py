r"""Software verification of ``DispatchObservationRecordIdentity``.

Evidence profile: routine

Bounded artifact scope: the public observation-record identity DataObject.

Facet and represented meaning

This module verifies the exact nonempty identity-value contract.

Intrinsic and cross-object scope

Observation lifecycle correlation remains with aggregate and replay evidence.

VVUQ and scientific exclusions

This is software verification only. It establishes no persistence, execution,
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

import pytest

from ksdft2effmass.workflows.runs import DispatchObservationRecordIdentity

pytestmark = pytest.mark.software_verification
SUT = DispatchObservationRecordIdentity


class TestDispatchObservationRecordIdentity:
    """Own software evidence for ``DispatchObservationRecordIdentity``."""

    def test_constructor__value__requires_nonempty_exact_text(self) -> None:
        """Accept only a nonempty built-in string.

        Evidence ID: SV-WFR-DISPATCH-OBSERVATION-RECORD-IDENTITY-001
        """
        assert SUT("observation-record.one").value == "observation-record.one"
        with pytest.raises(ValueError):
            SUT("")
        with pytest.raises(TypeError):
            SUT(1)  # type: ignore[arg-type]
