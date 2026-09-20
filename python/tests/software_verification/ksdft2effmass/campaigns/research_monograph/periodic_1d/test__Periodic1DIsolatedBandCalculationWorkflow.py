r"""Software verification of ``Periodic1DIsolatedBandCalculationWorkflow``.

Evidence profile: claim_bearing

Bounded artifact scope: execution-local Appendix G isolated-band diagnostic channels.

Facet and represented meaning

The Workflow calculates parent convergence/reference channels, a complete scalar
Fourier pair, finite-range metrics, and parent observables from the public campaign
definition without reading a retained result.

Intrinsic and cross-object scope

This evidence checks the extracted Workflow contract and compatibility with the frozen
historical result.  Independent numerical reconstruction remains owned by
``Periodic1DIsolatedResultVerifier``.

VVUQ and scientific exclusions

Compatibility does not establish material validation, uncertainty quantification, or
human acceptance.
"""

from pathlib import Path

import numpy as np
import pytest

from ksdft2effmass.campaigns.research_monograph import (
    Periodic1DIsolatedBandCalculationRequest,
    Periodic1DIsolatedBandCalculationWorkflow,
    Periodic1DIsolatedBandCampaignJsonSerializer,
    Periodic1DIsolatedBandResultJsonSerializer,
)
from ksdft2effmass.operators import ScalarQuantity, Unitless

pytestmark = pytest.mark.software_verification
SUT = Periodic1DIsolatedBandCalculationWorkflow


class TestPeriodic1DIsolatedBandCalculationWorkflow:
    """Own extracted isolated-band calculation compatibility evidence."""

    def test_method__execute__calculates_all_requested_diagnostic_channels(
        self,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-023

        Requirement: The public calculation Workflow produces every requested parent,
        reciprocal, Fourier, finite-range, route, and observable channel without
        consuming retained result bytes.

        Method: Deserialize only the versioned input, execute with the historical
        ``1e-3`` curvature step, and separately decode the immutable historical result
        for compatibility comparison.

        Oracle: The frozen retained typed channels and exact complete-mesh samples;
        independent mathematical verification belongs to
        ``NV-CAMPAIGN-PERIODIC-ONE-D-ISOLATED-001``.

        Acceptance: Parent records, scalar samples, hopping blocks, all range records,
        and parent observables agree exactly with the historical result.

        Interpretation: A pass establishes behavior-preserving extraction of the
        listed calculation channels into the public Workflow.

        Limitations: Gauge transport and localization are intentionally outside this
        result, and compatibility is not an independent physical oracle.

        Provenance: Appendix G ``input.json`` and ``result.json``.
        """
        root = Path(__file__).resolve().parents[7]
        directory = root / "calculations/research-monograph/periodic-1d"
        definition = Periodic1DIsolatedBandCampaignJsonSerializer().deserialize(
            (directory / "input.json").read_bytes()
        )
        retained = Periodic1DIsolatedBandResultJsonSerializer().deserialize(
            (directory / "result.json").read_bytes()
        )

        calculated = SUT().execute(
            Periodic1DIsolatedBandCalculationRequest(
                definition,
                ScalarQuantity(1.0e-3, Unitless()),
            )
        )

        assert calculated.parent_verification == retained.parent_verification
        assert np.array_equal(
            calculated.reciprocal_samples.coordinates.magnitude,
            retained.reduction.reciprocal_samples.coordinates.magnitude,
        )
        assert all(
            np.array_equal(calculated_matrix.magnitude, retained_matrix.magnitude)
            for calculated_matrix, retained_matrix in zip(
                calculated.reciprocal_samples.matrices,
                retained.reduction.reciprocal_samples.matrices,
                strict=True,
            )
        )
        assert calculated.hopping_model.representatives == (
            retained.reduction.hopping_model.representatives
        )
        assert all(
            np.array_equal(calculated_block.magnitude, retained_block.magnitude)
            for calculated_block, retained_block in zip(
                calculated.hopping_model.hopping_blocks,
                retained.reduction.hopping_model.hopping_blocks,
                strict=True,
            )
        )
        assert calculated.hopping_range_study == retained.reduction.hopping_range_study
        assert calculated.parent_observables == retained.reduction.parent_observables
        assert calculated.full_mesh_reconstruction_maximum_absolute_error == (
            retained.reduction.full_mesh_reconstruction_maximum_absolute_error
        )
        assert calculated.full_mesh_reconstruction_maximum_imaginary == (
            retained.reduction.full_mesh_reconstruction_maximum_imaginary
        )
        assert calculated.hopping_maximum_imaginary == (
            retained.reduction.hopping_maximum_imaginary
        )
