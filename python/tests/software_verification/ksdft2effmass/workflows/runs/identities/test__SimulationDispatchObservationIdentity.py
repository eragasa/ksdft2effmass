r"""Software verification of ``SimulationDispatchObservationIdentity``.

Evidence profile: routine

Bounded artifact scope: the public runtime-observation identity DataObject.

Facet and represented meaning

This module verifies the exact nonempty identity-value contract.

Intrinsic and cross-object scope

Outcome and observation-record correlation remain with their owning evidence.

VVUQ and scientific exclusions

This is software verification only. It establishes no persistence, execution,
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

import pytest

from ksdft2effmass.workflows.runs import SimulationDispatchObservationIdentity

pytestmark = pytest.mark.software_verification
SUT = SimulationDispatchObservationIdentity


class TestSimulationDispatchObservationIdentity:
    """Own software evidence for ``SimulationDispatchObservationIdentity``."""

    def test_constructor__value__requires_nonempty_exact_text(self) -> None:
        """Accept only a nonempty built-in string.

        Evidence ID: SV-WFR-DISPATCH-OBSERVATION-IDENTITY-001
        """
        assert SUT("observation.one").value == "observation.one"
        with pytest.raises(ValueError):
            SUT("")
        with pytest.raises(TypeError):
            SUT(1)  # type: ignore[arg-type]
