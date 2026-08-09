r"""Software verification of ``ArtifactIdentityVerificationStatus``.

Facet and represented meaning

-----------------------------
This module verifies the closed exact artifact-identity outcome vocabulary.

Intrinsic and cross-object scope

--------------------------------
``ArtifactIdentityVerificationStatus`` is the sole SUT; enum names, values, and order
are fixed by the public P2 contract.

VVUQ and scientific exclusions

------------------------------
Passing establishes only the software vocabulary. It excludes content observation,
format truth, numerical verification, scientific validation, UQ, and portability.
"""

import pytest

from ksdft2effmass.provenance import ArtifactIdentityVerificationStatus

SUT = ArtifactIdentityVerificationStatus
pytestmark = pytest.mark.software_verification


def test_field__verification_status_vocabulary__is_exact() -> None:
    """Evidence ID: SV-PROV-048

    Requirement: Exact identity outcomes are named VERIFIED and MISMATCH with stable
    wire values.

    Method: Enumerate the public string enum without executing the verifier.

    Oracle: The accepted P2 vocabulary independently fixes names, values, and
    declaration order.

    Acceptance: Name and value tuples equal the two literal expected tuples exactly.

    Interpretation: Failure indicates public or serialized vocabulary drift.

    Limitations: Enumeration does not establish that represented bytes were observed or
    compared.
    """
    assert tuple(item.name for item in SUT) == ("VERIFIED", "MISMATCH")
    assert tuple(item.value for item in SUT) == ("verified", "mismatch")
