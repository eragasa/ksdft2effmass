r"""Software verification of ``Periodic1DWannier90WilsonVerifier``.

Evidence profile: claim_bearing

Bounded artifact scope: independent one-dimensional native Wilson-loop reconstruction.

Facet and represented meaning

Active-neighbor selection, polar factors, ordered loop multiplication, native gauge
transformation, phase spectra, circular defects, and dispositions are included.

Intrinsic and cross-object scope

Authenticated parsed ``nnkp``, ``mmn``, and ``u.mat`` records are compared with a
typed retained Wilson spectrum without production Wilson analysis Actions.

VVUQ and scientific exclusions

The maintained data are synthetic software fixtures and establish neither topology,
material validation, nor uncertainty quantification.
"""

import json
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from ksdft2effmass.integration.wannier90 import (
    Wannier90EigenvalueData,
    Wannier90NativeArtifact,
    Wannier90NeighborListData,
    Wannier90NeighborOverlapData,
    Wannier90ProjectionData,
    Wannier90UnitaryMatrixData,
)
from ksdft2effmass.operators import ComplexMatrixQuantity, MatrixQuantity, Unitless
from ksdft2effmass.periodic1d.campaign import (
    Periodic1DCampaignJsonDecoder,
    Periodic1DEncodedResultKind,
)
from ksdft2effmass.periodic1d.campaign.wannier90 import (
    Periodic1DWannier90NativeArtifactGroup,
    Periodic1DWannier90NativeArtifactGroupResult,
    Periodic1DWannier90NativeArtifactWorkflow,
    Periodic1DWannier90NativeArtifactWorkflowRequest,
    Periodic1DWannier90NativeArtifactWorkflowResult,
    Periodic1DWannier90WilsonVerificationRequest,
    Periodic1DWannier90WilsonVerifier,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic1DWannier90WilsonVerifier


class TestPeriodic1DWannier90WilsonVerifier:
    """Own independent native Wilson-loop reconstruction evidence."""

    def test_method__execute__reconstructs_known_loop_in_two_gauges(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-018

        Requirement: The verifier reconstructs an unordered Wilson spectrum from the
        active native overlap loop and obtains the same spectrum after native gauge
        transformation.

        Method: Verify a maintained one-point rank-two loop with diagonal eigenvalues
        ``-i`` and ``+i`` and an identity native gauge.

        Oracle: The exact loop eigenphases are analytically ``-pi/2`` and ``+pi/2``.

        Acceptance: Both spectra equal the retained pair within ``1e-12`` radians,
        both loops are unitary within ``1e-12``, and the aggregate disposition passes.

        Interpretation: A pass establishes independent loop assembly and gauge-route
        comparison for the represented native contracts.

        Limitations: One synthetic loop does not establish retained-run correctness.

        Provenance: Maintained ``native-artifact-correlation-fixture.json``.
        """
        native_result = self.native_result()

        result = SUT().execute(
            Periodic1DWannier90WilsonVerificationRequest(
                native_result,
                1.0e-12,
                1.0e-12,
                0.5,
            )
        )

        group = result.groups[0]
        assert group.active_overlap_count == 1
        assert group.direct_spectrum.eigenphases == (
            -1.5707963267948966,
            1.5707963267948966,
        )
        assert group.native_gauge_spectrum == group.direct_spectrum
        assert group.minimum_active_overlap_singular_value == 1.0
        assert group.passes
        assert result.passes

    def test_method__execute__uses_ordered_multiedge_native_gauge_route(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-061-009.

        Requirement: Raw and native-gauge routes independently assemble the same
        periodic Wilson spectrum over an ordered multi-edge loop with a Bloch seam.

        Method: Replace only the parsed loop records in the authenticated synthetic
        Result by three noncommuting unitary overlaps, three varying nonidentity gauge
        matrices, one wrapped final edge, and one inactive transverse neighbor per
        reciprocal point.

        Oracle: The active overlap product is exactly ``diag(-i, +i)`` by construction,
        while gauge factors telescope to a similarity transform of that product.

        Acceptance: Exactly three active edges are selected; both reconstructed phase
        multisets equal ``(-pi/2, +pi/2)`` within ``1e-12`` radians; conditioning and
        unitarity controls pass.

        Interpretation: A pass distinguishes native-gauge transformation, ordered
        multiplication, seam handling, and inactive-neighbor exclusion from the raw
        overlap route.

        Limitations: The typed parsed records are synthetic verifier fixtures; this test
        does not qualify the parsers, authenticate an external run, or validate material
        topology.
        """
        native_result = self.native_result()
        first_group = native_result.groups[0]
        parsed = first_group.parsed_artifacts
        identity = np.eye(2, dtype=np.complex128)
        hadamard = np.asarray(((1.0, 1.0), (1.0, -1.0)), dtype=np.complex128) / np.sqrt(
            2.0
        )
        phase = np.diag(
            np.asarray((np.exp(0.31j), np.exp(-0.31j)), dtype=np.complex128)
        )
        target_loop = np.diag(np.asarray((-1.0j, 1.0j), dtype=np.complex128))
        final_overlap = (hadamard @ phase).conj().T @ target_loop
        active_overlaps = (hadamard, phase, final_overlap)
        assert not np.allclose(hadamard @ phase, phase @ hadamard)
        overlap_matrices = tuple(
            ComplexMatrixQuantity(matrix, Unitless())
            for active in active_overlaps
            for matrix in (active, identity)
        )
        neighbor_overlaps = Wannier90NeighborOverlapData(
            3,
            2,
            (0, 0, 1, 1, 2, 2),
            (1, 0, 2, 1, 0, 2),
            (
                (0, 0, 0),
                (0, 1, 0),
                (0, 0, 0),
                (0, 1, 0),
                (1, 0, 0),
                (0, 1, 0),
            ),
            overlap_matrices,
        )
        neighbor_list = Wannier90NeighborListData(
            2,
            (
                (1, 2, 0, 0, 0),
                (1, 1, 0, 1, 0),
                (2, 3, 0, 0, 0),
                (2, 2, 0, 1, 0),
                (3, 1, 1, 0, 0),
                (3, 3, 0, 1, 0),
            ),
        )
        angle = 0.43
        gauge_zero = np.asarray(
            (
                (np.cos(angle), -np.sin(angle)),
                (np.sin(angle), np.cos(angle)),
            ),
            dtype=np.complex128,
        )
        gauge_one = np.diag(
            np.asarray((np.exp(0.17j), np.exp(-0.17j)), dtype=np.complex128)
        )
        gauge_two = hadamard @ np.diag(np.asarray((1.0, 1.0j), dtype=np.complex128))
        gauge_matrices = (gauge_zero, gauge_one, gauge_two)
        assert all(not np.allclose(gauge, identity) for gauge in gauge_matrices)
        unitary_matrices = Wannier90UnitaryMatrixData(
            MatrixQuantity(
                np.asarray(
                    ((0.0, 0.0, 0.0), (1.0 / 3.0, 0.0, 0.0), (2.0 / 3.0, 0.0, 0.0)),
                    dtype=np.float64,
                ),
                Unitless(),
            ),
            tuple(ComplexMatrixQuantity(gauge, Unitless()) for gauge in gauge_matrices),
        )
        eigenvalues = Wannier90EigenvalueData(
            MatrixQuantity(
                np.repeat(parsed.eigenvalues.eigenvalues.magnitude, 3, axis=0),
                parsed.eigenvalues.eigenvalues.unit,
            )
        )
        projections = Wannier90ProjectionData((parsed.projections.matrices[0],) * 3)
        analytic_parsed = replace(
            parsed,
            eigenvalues=eigenvalues,
            projections=projections,
            neighbor_overlaps=neighbor_overlaps,
            neighbor_list=neighbor_list,
            unitary_matrices=unitary_matrices,
        )
        analytic_group = Periodic1DWannier90NativeArtifactGroupResult(
            first_group.group_id,
            first_group.correlation,
            analytic_parsed,
        )
        analytic_result = Periodic1DWannier90NativeArtifactWorkflowResult(
            native_result.campaign_result,
            (analytic_group,),
        )

        result = SUT().execute(
            Periodic1DWannier90WilsonVerificationRequest(
                analytic_result,
                1.0e-12,
                1.0e-12,
                0.5,
            )
        )

        group = result.groups[0]
        expected_phases = (-np.pi / 2.0, np.pi / 2.0)
        assert group.active_overlap_count == 3
        assert group.direct_spectrum.eigenphases == pytest.approx(
            expected_phases, abs=1.0e-12
        )
        assert group.native_gauge_spectrum.eigenphases == pytest.approx(
            expected_phases, abs=1.0e-12
        )
        assert group.minimum_active_overlap_singular_value == pytest.approx(1.0)
        assert group.passes
        assert result.passes

    def native_result(self) -> Periodic1DWannier90NativeArtifactWorkflowResult:
        """Build the correlated native Workflow result from maintained resources."""
        path = Path(__file__).with_name("resources") / (
            "native-artifact-correlation-fixture.json"
        )
        decoder = Periodic1DCampaignJsonDecoder()
        fixture = decoder.document(path.read_bytes())
        result_document = decoder.mapping(
            fixture.get("result_document"), "result_document"
        )
        artifact_text = decoder.mapping(
            fixture.get("artifact_text_by_name"), "artifact_text_by_name"
        )
        result_payload = (
            json.dumps(result_document, sort_keys=True, separators=(",", ":")) + "\n"
        ).encode("utf-8")
        artifacts = tuple(
            Wannier90NativeArtifact(name, decoder.string(value, name).encode("utf-8"))
            for name, value in artifact_text.items()
        )
        return Periodic1DWannier90NativeArtifactWorkflow().execute(
            Periodic1DWannier90NativeArtifactWorkflowRequest(
                result_payload,
                Periodic1DEncodedResultKind.WANNIER90,
                (Periodic1DWannier90NativeArtifactGroup("fixture", artifacts),),
            )
        )
