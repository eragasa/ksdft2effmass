r"""Software verification of ``EvidenceModuleSelector``.

Facet and represented meaning

The module verifies explicit profile-confined evidence-module selection.

Intrinsic and cross-object scope

``EvidenceModuleSelector`` is the sole system under test.

VVUQ and scientific exclusions

Passing establishes software behavior only, not scientific validation or UQ.
"""

import pytest

from ksdft2effmass.harness.pi import ProjectProfile
from ksdft2effmass.harness.pi.local import EvidenceModuleSelector

from .conftest import local_context

pytestmark = pytest.mark.software_verification
SUT = EvidenceModuleSelector


def test_method__execute__preserves_in_scope_bytes_and_rejects_outside_scope() -> None:
    """Evidence ID: SV-HL-005

    Requirement: Evidence selection accepts only caller-supplied modules inside the
    explicit profile.

    Method: Select one in-scope Python path and one documentation path with the current
    profile.

    Oracle: The profile admits maintained Python evidence roots and excludes ``docs/``.

    Acceptance: In-scope bytes are unchanged; outside scope reports
    ``PIHL.EVIDENCE.OUTSIDE_SCOPE``.

    Interpretation: Failure indicates scope leakage or profile drift.

    Limitations: The test samples one path on each side and makes no scientific or UQ
    claim.
    """
    context = local_context()
    assert isinstance(context.profile, ProjectProfile)
    selected = EvidenceModuleSelector().execute(
        (("python/tests/software_verification/x.py", b"x"),), context.profile
    )
    assert selected.value == (("python/tests/software_verification/x.py", b"x"),)
    outside = EvidenceModuleSelector().execute((("docs/x.py", b"x"),), context.profile)
    assert outside.validation.issues[0].code == "PIHL.EVIDENCE.OUTSIDE_SCOPE"
