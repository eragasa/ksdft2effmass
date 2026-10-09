r"""Software verification of ``Periodic1DWannier90ResultJsonSerializer``.

Evidence profile: claim_bearing

Bounded artifact scope: retained Appendix G Wannier90 Wilson-center adaptation.

Facet and represented meaning

Direct Wilson phases, phase-derived centers, reported centers, and circular defects are
included for original and preconditioned retained results.

Intrinsic and cross-object scope

The public Wilson comparator reconstructs the reported center-set defect.

VVUQ and scientific exclusions

The adapter does not execute Wannier90 or interpret a phase set as topology.
"""

import json
from pathlib import Path

import pytest

from ksdft2effmass.periodic1d.campaign import (
    Periodic1DEncodedResultKind,
)
from ksdft2effmass.periodic1d.campaign.wannier90 import (
    Periodic1DWannier90ResultJsonSerializer,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic1DWannier90ResultJsonSerializer


class TestPeriodic1DWannier90ResultJsonSerializer:
    """Own retained Wannier90 Wilson-center adaptation evidence."""

    @pytest.mark.parametrize(
        ("kind", "filename", "expected_defect"),
        (
            pytest.param(
                Periodic1DEncodedResultKind.WANNIER90,
                "wannier90-result.json",
                0.18118978430194888,
                id="native_localization_campaign",
            ),
            pytest.param(
                Periodic1DEncodedResultKind.WANNIER90_PRECONDITIONED,
                "wannier90-preconditioned-result.json",
                2.156980511980322e-07,
                id="preconditioned_native_campaign",
            ),
        ),
    )
    def test_method__deserialize__reconstructs_circular_center_comparison(
        self,
        kind: Periodic1DEncodedResultKind,
        filename: str,
        expected_defect: float,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-015

        Requirement: Both retained routes use one typed Wilson-center comparison.

        Method: Deserialize each retained format and inspect the low-pair comparison.

        Oracle: Reported defects and independently reconstructed circular matching.

        Acceptance: Spectrum rank is two and the reconstructed defect equals the wire.

        Interpretation: A pass establishes typed Wilson-center compatibility.

        Limitations: Convergence status is retained rather than inferred.

        Provenance: Original and preconditioned Appendix G result artifacts.
        """
        root = Path(__file__).resolve().parents[7]
        payload = (
            root / "calculations/research-monograph/periodic-1d" / filename
        ).read_bytes()

        result = SUT(kind).deserialize(payload)
        low_pair = result.groups[0]

        assert low_pair.direct_spectrum.rank == 2
        assert low_pair.recorded_center_set_circular_maximum_defect == expected_defect
        assert low_pair.center_phase_comparison.passes

    @pytest.mark.parametrize(
        ("kind", "filename"),
        (
            pytest.param(
                Periodic1DEncodedResultKind.WANNIER90_PRECONDITIONED,
                "wannier90-result.json",
                id="initial-as-preconditioned",
            ),
            pytest.param(
                Periodic1DEncodedResultKind.WANNIER90,
                "wannier90-preconditioned-result.json",
                id="preconditioned-as-initial",
            ),
        ),
    )
    def test_method__deserialize__rejects_variant_relabeling(
        self, kind: Periodic1DEncodedResultKind, filename: str
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-061-006.

        Requirement: An explicit schema selector cannot relabel the other valid
        Wannier90 result variant.

        Method: Pair each retained payload with the opposite supported result kind.

        Oracle: ``interface_conventions.preconditioned`` is the source variant
        declaration correlated only after the explicit kind selects the schema.

        Acceptance: Both crossed pairings raise ``ValueError`` before a typed campaign
        Result can be returned.

        Interpretation: A pass establishes fail-closed wire-variant correlation without
        inferring the selector from a path, filename, identifier, or matrix content.

        Limitations: Variant correlation does not authenticate execution provenance or
        validate the retained scientific observations.
        """
        root = Path(__file__).resolve().parents[7]
        payload = (
            root / "calculations/research-monograph/periodic-1d" / filename
        ).read_bytes()

        with pytest.raises(
            ValueError,
            match="interface preconditioning does not agree with the result kind",
        ):
            SUT(kind).deserialize(payload)

    @pytest.mark.parametrize(
        "location",
        (
            pytest.param("root", id="root-extension"),
            pytest.param("missing-root", id="root-omission"),
            pytest.param("provenance", id="provenance-extension"),
            pytest.param("group", id="group-extension"),
            pytest.param("artifact", id="artifact-extension"),
            pytest.param("range-study", id="range-study-extension"),
        ),
    )
    def test_method__deserialize__rejects_unknown_schema_fields(
        self, location: str
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-061-002.

        Requirement: Version-one Wannier90 result schemas are closed at campaign,
        group, and native-artifact identity boundaries.

        Method: Omit one required root field and add otherwise well-formed unknown
        fields at root, provenance, group, artifact, and range-study boundaries.

        Oracle: The documented exact field inventories of the version-one adapter.

        Acceptance: Deserialization rejects every omission or extension with a
        closed-schema diagnostic.

        Interpretation: A pass establishes that schema evolution cannot silently alter
        campaign meaning.

        Limitations: The test establishes field-set closure, not scientific validity of
        accepted field values.
        """
        root = Path(__file__).resolve().parents[7]
        source = root / (
            "calculations/research-monograph/periodic-1d/"
            "wannier90-preconditioned-result.json"
        )
        document = json.loads(source.read_bytes())
        if location == "root":
            document["extension"] = "unsupported"
        elif location == "missing-root":
            del document["claim_boundary"]
        elif location == "provenance":
            document["provenance"]["extension"] = "unsupported"
        elif location == "group":
            document["groups"][0]["extension"] = "unsupported"
        elif location == "artifact":
            document["groups"][0]["artifact_identities"][0]["extension"] = "unsupported"
        else:
            document["groups"][0]["range_study"][0]["extension"] = "unsupported"
        payload = json.dumps(document, sort_keys=True).encode("utf-8")

        with pytest.raises(ValueError, match="fields must match the closed schema"):
            SUT(Periodic1DEncodedResultKind.WANNIER90_PRECONDITIONED).deserialize(
                payload
            )

    def test_method__deserialize__rejects_invalid_unprojected_field_types(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-061-004.

        Requirement: Complete source retention does not permit unprojected schema
        fields to bypass exact primitive validation.

        Method: Replace the textual claim boundary by an integer while preserving the
        closed field set.

        Oracle: The version-one root schema declares claim-boundary text.

        Acceptance: Deserialization raises ``TypeError`` at the schema boundary.

        Interpretation: A pass establishes strict adaptation beyond fields projected
        into the compact typed Wilson Result.

        Limitations: Primitive validation does not establish the scientific truth of
        accepted text.
        """
        root = Path(__file__).resolve().parents[7]
        source = root / (
            "calculations/research-monograph/periodic-1d/"
            "wannier90-preconditioned-result.json"
        )
        document = json.loads(source.read_bytes())
        document["claim_boundary"] = 1

        with pytest.raises(TypeError, match="claim_boundary must be a JSON string"):
            SUT(Periodic1DEncodedResultKind.WANNIER90_PRECONDITIONED).deserialize(
                json.dumps(document, sort_keys=True).encode("utf-8")
            )

    def test_method__deserialize__rejects_binary64_overflow(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-061-005.

        Requirement: Public numeric adaptation fails closed when a JSON integer cannot
        be represented as finite binary64.

        Method: Replace one finite defect by an exact integer larger than binary64.

        Oracle: The serializer's documented finite-binary64 representation contract.

        Acceptance: Deserialization raises ``OverflowError`` rather than retaining an
        infinity.

        Interpretation: A pass establishes range failure separation from schema-type
        and nonfinite-value failures.

        Limitations: The test does not establish a scientifically appropriate defect
        tolerance.
        """
        root = Path(__file__).resolve().parents[7]
        source = root / (
            "calculations/research-monograph/periodic-1d/"
            "wannier90-preconditioned-result.json"
        )
        document = json.loads(source.read_bytes())
        document["groups"][0]["center_set_circular_maximum_defect"] = 10**400

        with pytest.raises(OverflowError):
            SUT(Periodic1DEncodedResultKind.WANNIER90_PRECONDITIONED).deserialize(
                json.dumps(document, sort_keys=True).encode("utf-8")
            )
