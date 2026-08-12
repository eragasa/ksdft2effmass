r"""Software verification of ``UnavailableReason``.

Evidence profile: routine

Bounded artifact scope: typed unavailable semantic reasons in periodic records.

Facet and represented meaning

The enum distinguishes source absence, absent spin arrays, and absent retained subspace.

Intrinsic and cross-object scope

Only the closed public vocabulary and immutable string values are covered.

VVUQ and scientific exclusions

Unavailable reasons make no claim about physics outside the accepted source.
"""

import pytest

from ksdft2effmass.periodic import UnavailableReason

SUT = UnavailableReason
pytestmark = pytest.mark.software_verification


def test_field__closed_vocabulary__has_precise_nonmagic_reasons() -> None:
    """Evidence ID: SV-PERIODIC-014

    Requirement: Required absence uses a closed typed vocabulary with precise reasons.

    Acceptance: The exact three nonempty wire values are present and unknown text is
    rejected.
    """
    assert tuple(reason.value for reason in UnavailableReason) == (
        "not_represented_in_qexsd",
        "no_spin_resolved_arrays_in_qexsd",
        "no_retained_subspace_represented_in_qexsd",
    )
    with pytest.raises(ValueError):
        UnavailableReason("")
