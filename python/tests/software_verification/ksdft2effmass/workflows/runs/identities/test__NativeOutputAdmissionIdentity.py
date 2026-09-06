r"""Software verification of ``NativeOutputAdmissionIdentity``.

Evidence profile: routine

Bounded artifact scope: the nominal native-output admission identity.

Facet and represented meaning

The identity names one exact dispatch-specific native-output admission record.

Intrinsic and cross-object scope

This module verifies only nominal identity construction.

VVUQ and scientific exclusions

This is software verification only and establishes no file access, scientific
validation, uncertainty quantification, or human acceptance.
"""

import pytest

from ksdft2effmass.workflows import NativeOutputAdmissionIdentity

pytestmark = pytest.mark.software_verification
SUT = NativeOutputAdmissionIdentity


class TestNativeOutputAdmissionIdentity:
    """Own nominal identity evidence for native-output admission."""

    def test_constructor__nonempty_value__preserves_nominal_identity(self) -> None:
        """Construct a nonempty exact admission identity.

        Evidence ID: SV-WFR-NATIVE-OUTPUT-ADMISSION-IDENTITY-001
        """
        identity = SUT("native-admission.one")
        assert identity.value == "native-admission.one"
