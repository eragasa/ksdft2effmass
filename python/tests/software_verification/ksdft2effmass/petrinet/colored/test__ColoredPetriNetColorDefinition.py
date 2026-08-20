r"""Software verification of ``ColoredPetriNetColorDefinition``.

Evidence profile: routine

Bounded artifact scope: the public ``ColoredPetriNetColorDefinition`` generic
colored-Petri-net contract.

Facet and represented meaning

The class represents its documented immutable data or deterministic action boundary.

Intrinsic and cross-object scope

The focused class contract is covered; enablement and firing remain excluded.

VVUQ and scientific exclusions

These synthetic checks establish software behavior only, not numerical verification,
scientific validation, UQ, authority, execution, or human acceptance.
"""

import pytest

from ksdft2effmass.petrinet.colored import (
    ColoredPetriNetColorDefinition,
    ColoredPetriNetColorIdentity,
    ColoredPetriNetValueKind,
)
from ksdft2effmass.workflows.cpn import ColorDefinition

pytestmark = pytest.mark.software_verification
SUT = ColoredPetriNetColorDefinition


def test_constructor__allowed_value_kinds__canonicalizes_unique_nonempty_set() -> None:
    """Evidence ID: SV-PETRINET-059

    Requirement: A color admits a canonical nonempty unique set of value kinds.

    Acceptance: Reversed kinds sort; empty and duplicate tuples reject exactly.
    """
    identity = ColoredPetriNetColorIdentity("color")
    color = SUT(
        identity, (ColoredPetriNetValueKind.STRING, ColoredPetriNetValueKind.INTEGER)
    )
    assert color.allowed_value_kinds == (
        ColoredPetriNetValueKind.INTEGER,
        ColoredPetriNetValueKind.STRING,
    )
    with pytest.raises(ValueError):
        SUT(identity, ())
    with pytest.raises(ValueError):
        SUT(identity, (ColoredPetriNetValueKind.NONE,) * 2)


def test_artifact__v1_no_payload_mapping__maps_to_none_value_kind() -> None:
    """Evidence ID: SV-PETRINET-065

    Requirement: A valid v1 no-payload color maps explicitly to singleton ``NONE``.

    Acceptance: The fixed v1/v2 mapping retains absence without inventing payload.
    """
    v1 = ColorDefinition("control", "Control token", ())
    v2 = SUT(
        ColoredPetriNetColorIdentity(v1.color_id), (ColoredPetriNetValueKind.NONE,)
    )
    assert v1.allowed_payload_type_ids == ()
    assert v2.allowed_value_kinds == (ColoredPetriNetValueKind.NONE,)
