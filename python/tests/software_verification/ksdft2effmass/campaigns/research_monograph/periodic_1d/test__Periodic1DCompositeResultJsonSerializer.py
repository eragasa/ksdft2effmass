r"""Software verification of ``Periodic1DCompositeResultJsonSerializer``.

Evidence profile: claim_bearing

Bounded artifact scope: retained Appendix G composite result adaptation.

Facet and represented meaning

Both retained composite-band groups and their separated matrix, hopping, gap, gauge,
range, route, Wilson, and identity channels are included.

Intrinsic and cross-object scope

Group band counts are correlated with Wilson-spectrum and represented-matrix ranks;
complete smooth and rough hopping inventories remain separately represented.

VVUQ and scientific exclusions

Deserialization does not reproduce the calculation or establish topology, material
validation, or uncertainty quantification.
"""

from pathlib import Path

import numpy as np
import pytest

from ksdft2effmass.campaigns.research_monograph import (
    Periodic1DCompositeResultJsonSerializer,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic1DCompositeResultJsonSerializer


class TestPeriodic1DCompositeResultJsonSerializer:
    """Own retained composite Wilson-result adaptation evidence."""

    def test_method__deserialize__extracts_both_wilson_spectra(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-013

        Requirement: Retained composite Wilson phases use the public spectrum contract.

        Method: Deserialize the authenticated retained composite result bytes.

        Oracle: Exact phase values and group identities in the retained document.

        Acceptance: Both rank-two groups expose their canonical Wilson phase pairs.

        Interpretation: A pass establishes typed retained-wire compatibility.

        Limitations: The historical controlled-gauge spectrum was not retained.

        Provenance: Appendix G ``composite-result.json``.
        """
        root = Path(__file__).resolve().parents[7]
        payload = (
            root / "calculations/research-monograph/periodic-1d/composite-result.json"
        ).read_bytes()

        result = SUT().deserialize(payload)

        assert tuple(group.group_id for group in result.groups) == (
            "low_pair",
            "higher_pair",
        )
        assert result.groups[0].spectrum.eigenphases == (
            -1.9856198592310257,
            1.985619859231026,
        )
        assert result.groups[1].spectrum.rank == 2

    def test_method__deserialize__extracts_non_wilson_composite_channels(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-020

        Requirement: The composite adapter exposes every demonstrated non-Wilson
        matrix, hopping, gap, gauge, range, route, and identity channel.

        Method: Deserialize the authenticated retained composite result and inspect
        the first group through public typed records.

        Oracle: Exact field inventories, dimensions, representatives, and selected
        values in the retained version-one result document.

        Acceptance: All channels are present with 128 rank-two matrices and hopping
        blocks, the complete range inventory, exact diagnostics, and exact identities.

        Interpretation: A pass establishes typed retained-wire compatibility for the
        non-Wilson composite result channels.

        Limitations: The test neither recomputes the arrays nor accepts their physical
        or scientific adequacy.

        Provenance: Appendix G ``composite-result.json`` with source SHA-256
        ``9231057d96be5e7277e5d76d7272a9bad0a00b02996b7e989164ab619e19c02f``.
        """
        root = Path(__file__).resolve().parents[7]
        payload = (
            root / "calculations/research-monograph/periodic-1d/composite-result.json"
        ).read_bytes()

        result = SUT().deserialize(payload)
        group = result.groups[0]
        hopping = group.hopping_representation

        assert result.source_document.source_sha256 == (
            "9231057d96be5e7277e5d76d7272a9bad0a00b02996b7e989164ab619e19c02f"
        )
        assert group.isolation.internal_minimum_gap == 0.4923392223766146
        assert group.isolation.external_minimum_gap == 0.11356905243415372
        assert group.isolation.external_status.value == "pass"
        assert group.gauge_comparison.neighbor_overlap_minimum_singular_value == (
            0.9916955643071454
        )
        assert (
            group.gauge_comparison.rough_vs_smooth_unaligned_hopping_l2_defect
            == 0.9436644561504324
        )
        assert len(hopping.smooth_reciprocal_hamiltonians.matrices) == 128
        assert hopping.smooth_reciprocal_hamiltonians.matrix_dimension == 2
        assert np.array_equal(
            hopping.smooth_reciprocal_hamiltonians.matrices[0].magnitude,
            np.asarray(
                [
                    [
                        complex(-0.027562204248023768, -2.7807682655029573e-33),
                        complex(1.141808610376433e-16, 2.4270297653870398e-17),
                    ],
                    [
                        complex(6.408699334035203e-17, -2.4270297653870398e-17),
                        complex(0.46477701812859074, -1.8720062925997535e-33),
                    ],
                ],
                dtype=np.complex128,
            ),
        )
        assert hopping.smooth_hopping_model.representatives == tuple(range(-64, 64))
        assert hopping.rough_hopping_model.representatives == tuple(range(-64, 64))
        assert len(hopping.smooth_block_frobenius_norms) == 128
        assert len(hopping.rough_block_frobenius_norms) == 128
        assert hopping.smooth_full_reconstruction_maximum_frobenius_error == (
            3.704064955824442e-15
        )
        assert hopping.rough_full_reconstruction_maximum_frobenius_error == (
            9.36974336950289e-15
        )
        assert tuple(item.hopping_range_cells for item in group.range_study) == (
            0,
            1,
            2,
            3,
            4,
            6,
            8,
            12,
        )
        assert group.range_study[0].smooth_omitted_block_l2_norm == (0.5284695426526016)
        assert group.range_study[0].rough_withheld_eigenvalue_maximum_error == (
            0.5910991186755913
        )
        assert group.direct_route.hopping_range_cells == 4
        assert group.direct_route.coefficient_frobenius_defect == (
            6.103589373315561e-16
        )
        assert group.identities.smooth_frame_sha256 == (
            "3b843b5660bb0f4faf01a616847512ff93b3be628b84eaabc22ef9fc2ff3396c"
        )
        assert group.identities.rough_hopping_sha256 == (
            "7dfdf696d67e5b764232151dbe14c38cf683d4e0ace19c1edbd488a49b2e5f7f"
        )
