r"""Software verification of ``NativeOutputAdmission``.

Evidence profile: routine

Bounded artifact scope: dispatch-specific native-output admission correlation.

Facet and represented meaning

The record correlates one confirmed dispatch production to an exact native manifest and
admitted entry identities.

Intrinsic and cross-object scope

This module verifies immutable record construction only; replay owns aggregate closure.

VVUQ and scientific exclusions

This is software verification only and establishes no file access, scientific
validation, uncertainty quantification, or human acceptance.
"""

import pytest

from ksdft2effmass.workflows import (
    ArtifactManifestEntryIdentity,
    ArtifactManifestIdentity,
    DispatchOutcomeRecordIdentity,
    NativeOutputAdmission,
    NativeOutputAdmissionIdentity,
    ResultObjectReferenceIdentity,
    ResultProductionRecordIdentity,
    SimulationDispatchObservationIdentity,
    WorkflowRunIdentity,
)

pytestmark = pytest.mark.software_verification
SUT = NativeOutputAdmission


class TestNativeOutputAdmission:
    """Own construction evidence for dispatch-specific output admission."""

    def test_constructor__exact_correlations__retains_native_manifest_entries(
        self,
    ) -> None:
        """Correlate one dispatch and production to exact admitted native entries.

        Evidence ID: SV-WFR-NATIVE-OUTPUT-ADMISSION-001
        """
        admission = SUT(
            identity=NativeOutputAdmissionIdentity("native-admission.one"),
            workflow_run_identity=WorkflowRunIdentity("run.one"),
            dispatch_outcome_record_identity=DispatchOutcomeRecordIdentity(
                "dispatch.one"
            ),
            dispatch_envelope_identity=SimulationDispatchObservationIdentity(
                "envelope.one"
            ),
            production_record_identity=ResultProductionRecordIdentity("production.one"),
            result_reference_identity=ResultObjectReferenceIdentity("result.one"),
            manifest_identity=ArtifactManifestIdentity("manifest.one"),
            manifest_entry_identities=(
                ArtifactManifestEntryIdentity("manifest-entry.one"),
            ),
        )
        assert admission.manifest_entry_identities == (
            ArtifactManifestEntryIdentity("manifest-entry.one"),
        )
