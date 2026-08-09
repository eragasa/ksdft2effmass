r"""Software verification of ``SkillInventoryAdapter``.

Facet and represented meaning

The module verifies explicit skill-inventory adaptation.

Intrinsic and cross-object scope

``SkillInventoryAdapter`` is the sole system under test.

VVUQ and scientific exclusions

Passing establishes software behavior only, not scientific validation or UQ.
"""

from typing import Any, cast

import pytest

from ksdft2effmass.harness.pi.local import SkillInventoryAdapter

from .conftest import repository_root

pytestmark = pytest.mark.software_verification
SUT = SkillInventoryAdapter


def test_method__execute__returns_only_explicitly_selected_skill() -> None:
    """Evidence ID: SV-HL-043

    Requirement: Skill adaptation returns only descriptors supplied by the caller.

    Method: Supply the current capability inventory and one selected descriptor.

    Oracle: The explicit selection contains only ``document-python-research-software``.

    Acceptance: Adaptation passes and returns exactly that one skill identity.

    Interpretation: Failure indicates fallback discovery or inventory drift.

    Limitations: The test does not assess skill prose quality, scientific validity, or
    UQ.
    """
    root = repository_root()
    descriptor = "harness/pi/skills/document-python-research-software/descriptor.json"
    result = SkillInventoryAdapter().execute(
        (root / ".pi/skills/skill-capability-inventory.json").read_bytes(),
        ((descriptor, (root / descriptor).read_bytes()),),
    )
    assert result.validation.status == "PASS"
    assert tuple(item.skill_id for item in cast(Any, result.value)) == (
        "document-python-research-software",
    )
