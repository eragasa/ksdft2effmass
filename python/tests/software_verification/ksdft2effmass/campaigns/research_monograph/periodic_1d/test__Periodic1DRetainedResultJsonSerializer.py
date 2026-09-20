r"""Software verification of ``Periodic1DRetainedResultJsonSerializer``.

Evidence profile: claim_bearing

Bounded artifact scope: retained Appendix G result-document adaptation.

Facet and represented meaning

The serializer preserves every JSON value in six authenticated result formats while
retaining the source-byte SHA-256 identity separately from canonical output bytes.

Intrinsic and cross-object scope

Version, record identity, evidence status, immutable nesting, and round-trip canonical
representation are included.

VVUQ and scientific exclusions

This read-only compatibility evidence does not rerun or scientifically validate any
campaign or Wannier90 calculation.
"""

from pathlib import Path

import pytest

from ksdft2effmass.campaigns.research_monograph import (
    Periodic1DJsonArray,
    Periodic1DJsonObject,
    Periodic1DRetainedResultJsonSerializer,
    Periodic1DRetainedResultKind,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic1DRetainedResultJsonSerializer
type NestedKind = type[Periodic1DJsonArray] | type[Periodic1DJsonObject]
RESULT_CASES = (
    pytest.param(
        Periodic1DRetainedResultKind.ISOLATED_BAND,
        "result.json",
        "research-monograph.periodic-1d.isolated-band.v1",
        "isolated_band_reduction",
        Periodic1DJsonObject,
        id="isolated_band_campaign",
    ),
    pytest.param(
        Periodic1DRetainedResultKind.STRESS,
        "stress-result.json",
        "research-monograph.periodic-1d.stress.v1",
        "mesh_band_and_isolation_stress",
        Periodic1DJsonArray,
        id="adversarial_stress_campaign",
    ),
    pytest.param(
        Periodic1DRetainedResultKind.COMPOSITE,
        "composite-result.json",
        "research-monograph.periodic-1d.composite.v1",
        "groups",
        Periodic1DJsonArray,
        id="composite_band_campaign",
    ),
    pytest.param(
        Periodic1DRetainedResultKind.WANNIER90,
        "wannier90-result.json",
        "research-monograph.periodic-1d.wannier90.v1",
        "groups",
        Periodic1DJsonArray,
        id="native_localization_campaign",
    ),
    pytest.param(
        Periodic1DRetainedResultKind.WANNIER90_PRECONDITIONED,
        "wannier90-preconditioned-result.json",
        "research-monograph.periodic-1d.wannier90.v1",
        "groups",
        Periodic1DJsonArray,
        id="preconditioned_native_campaign",
    ),
    pytest.param(
        Periodic1DRetainedResultKind.WANNIER90_CONVERGENCE_ATTEMPT,
        "wannier90-convergence-attempt.json",
        "research-monograph.periodic-1d.wannier90.convergence-attempt-1",
        "stages",
        Periodic1DJsonArray,
        id="stopped_convergence_attempt",
    ),
)


class TestPeriodic1DRetainedResultJsonSerializer:
    """Own compatibility evidence for complete retained result documents."""

    @pytest.mark.parametrize(
        ("kind", "filename", "record_id", "nested_field", "nested_kind"),
        RESULT_CASES,
    )
    def test_method__decode_encode__preserves_complete_retained_document(
        self,
        kind: Periodic1DRetainedResultKind,
        filename: str,
        record_id: str,
        nested_field: str,
        nested_kind: NestedKind,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-007

        Requirement: Each demonstrated Appendix G result remains completely and
        immutably representable without changing its historical source-byte identity.

        Method: Decode retained bytes, assert independent identity and nested-shape
        literals, then decode the canonical representation and compare immutable roots.

        Oracle: The six retained Appendix G result and convergence-attempt artifacts.

        Acceptance: Version, identity, nested kind, source digest syntax, and canonical
        reconstruction agree for every explicitly identified result format.

        Interpretation: A pass establishes full JSON-level persistence compatibility.

        Limitations: Detailed scientific fields remain encoded values rather than
        acceptance claims; calculations, validation, and UQ are excluded.

        Provenance: Retained files under the Appendix G periodic-1D calculation
        directory.
        """
        repository_root = Path(__file__).resolve().parents[7]
        payload = repository_root.joinpath(
            "calculations/research-monograph/periodic-1d", filename
        ).read_bytes()
        serializer = SUT(kind)

        result = serializer.deserialize(payload)
        reconstructed = serializer.deserialize(serializer.serialize(result))

        assert result.schema_version == 1
        assert result.record_id == record_id
        assert type(result.root.field(nested_field)) is nested_kind
        assert len(result.source_sha256) == 64
        assert reconstructed.root == result.root
        assert reconstructed.record_id == result.record_id
