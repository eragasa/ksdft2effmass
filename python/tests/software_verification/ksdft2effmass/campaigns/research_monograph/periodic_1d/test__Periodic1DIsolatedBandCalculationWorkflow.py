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

from dataclasses import fields, is_dataclass
from pathlib import Path
from typing import Any

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

        Acceptance: Discrete structure agrees exactly; ordinary binary64 channels
        agree within ``1e-10 E_G`` and curvature-bearing parent observables agree
        within their separately accepted ``1e-7 E_G`` tolerance.

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

        assert self.numerically_compatible(
            calculated.parent_verification,
            retained.parent_verification,
            absolute_tolerance=1.0e-10,
        )
        assert np.array_equal(
            calculated.reciprocal_samples.coordinates.magnitude,
            retained.reduction.reciprocal_samples.coordinates.magnitude,
        )
        assert all(
            np.allclose(
                calculated_matrix.magnitude,
                retained_matrix.magnitude,
                rtol=0.0,
                atol=1.0e-10,
            )
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
            np.allclose(
                calculated_block.magnitude,
                retained_block.magnitude,
                rtol=0.0,
                atol=1.0e-10,
            )
            for calculated_block, retained_block in zip(
                calculated.hopping_model.hopping_blocks,
                retained.reduction.hopping_model.hopping_blocks,
                strict=True,
            )
        )
        assert self.numerically_compatible(
            calculated.hopping_range_study,
            retained.reduction.hopping_range_study,
            absolute_tolerance=1.0e-10,
        )
        assert self.numerically_compatible(
            calculated.parent_observables,
            retained.reduction.parent_observables,
            absolute_tolerance=1.0e-7,
        )
        assert calculated.full_mesh_reconstruction_maximum_absolute_error == (
            pytest.approx(
                retained.reduction.full_mesh_reconstruction_maximum_absolute_error,
                rel=0.0,
                abs=1.0e-10,
            )
        )
        assert calculated.full_mesh_reconstruction_maximum_imaginary == pytest.approx(
            retained.reduction.full_mesh_reconstruction_maximum_imaginary,
            rel=0.0,
            abs=1.0e-10,
        )
        assert calculated.hopping_maximum_imaginary == pytest.approx(
            retained.reduction.hopping_maximum_imaginary,
            rel=0.0,
            abs=1.0e-10,
        )

    @classmethod
    def numerically_compatible(
        cls, calculated: Any, retained: Any, *, absolute_tolerance: float
    ) -> bool:
        """Compare discrete structure exactly and binary64 fields by tolerance."""
        if type(calculated) is not type(retained):
            return False
        if type(retained) is float:
            return calculated == pytest.approx(
                retained, rel=0.0, abs=absolute_tolerance
            )
        if isinstance(retained, np.ndarray):
            return bool(
                np.allclose(calculated, retained, rtol=0.0, atol=absolute_tolerance)
            )
        if is_dataclass(retained) and not isinstance(retained, type):
            return all(
                cls.numerically_compatible(
                    getattr(calculated, field.name),
                    getattr(retained, field.name),
                    absolute_tolerance=absolute_tolerance,
                )
                for field in fields(retained)
            )
        if isinstance(retained, tuple):
            return len(calculated) == len(retained) and all(
                cls.numerically_compatible(
                    calculated_value,
                    retained_value,
                    absolute_tolerance=absolute_tolerance,
                )
                for calculated_value, retained_value in zip(
                    calculated, retained, strict=True
                )
            )
        return calculated == retained
