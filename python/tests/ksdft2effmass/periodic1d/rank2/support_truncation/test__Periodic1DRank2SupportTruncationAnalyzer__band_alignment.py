"""Tests for rank-two band-alignment support truncation."""

import numpy as np
import pytest
from projectkoios.numerics.numpy.typing import Float64Array
from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.analysis.periodic_bands import BandSpectrumSamples1D
from ksdft2effmass.periodic1d.rank2 import support_truncation as namespace
from ksdft2effmass.periodic1d.rank2.band_alignment.configuration import (
    Periodic1DCompositeBandAlignmentConfiguration,
)
from ksdft2effmass.periodic1d.rank2.hopping_locality.analysis import (
    Periodic1DRank2HoppingLocalityAnalyzer,
)
from ksdft2effmass.periodic1d.rank2.hopping_locality.request import (
    Periodic1DRank2HoppingLocalityAnalysisRequest,
)
from ksdft2effmass.periodic1d.rank2.support_truncation import (
    band_alignment as band_alignment_namespace,
)
from ksdft2effmass.periodic1d.rank2.support_truncation.band_alignment import (
    analysis as analysis_module,
)
from ksdft2effmass.periodic1d.rank2.support_truncation.band_alignment import (
    request as request_module,
)
from ksdft2effmass.periodic1d.rank2.support_truncation.band_alignment import (
    result as result_module,
)
from ksdft2effmass.periodic1d.rank2.support_truncation.band_alignment.analysis import (
    Periodic1DRank2SupportTruncationAnalyzer,
)
from ksdft2effmass.periodic1d.rank2.support_truncation.band_alignment.request import (
    Periodic1DRank2SupportTruncationAnalysisRequest,
)
from ksdft2effmass.periodic1d.rank2.support_truncation.band_alignment.result import (
    Periodic1DRank2SupportTruncationAnalysis,
)
from ksdft2effmass.solidstate.hopping_transforms import (
    BlockHoppingInterpolationRequest1D,
    BlockHoppingInterpolator1D,
    BlockHoppingModel1D,
    ReciprocalOperatorSamples1D,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DRank2SupportTruncationAnalyzer:
    """Establish irreversible support removal as a separate action."""

    def test__namespace__is_inert_and_action_modules_are_authoritative(self) -> None:
        action_name = "Periodic1DRank2SupportTruncationAnalyzer"
        assert not hasattr(namespace, action_name)
        assert not hasattr(band_alignment_namespace, action_name)
        assert analysis_module.__all__ == [action_name]
        assert request_module.__all__ == [
            "Periodic1DRank2SupportTruncationAnalysisRequest"
        ]
        assert result_module.__all__ == [
            "Periodic1DRank2SupportResult",
            "Periodic1DRank2SupportTruncationAnalysis",
        ]

    def test__execute__retains_support_errors_but_not_locality_diagnostics(
        self,
        composite_configuration: Periodic1DCompositeBandAlignmentConfiguration,
    ) -> None:
        model = self._model()
        locality = Periodic1DRank2HoppingLocalityAnalyzer(
            request=Periodic1DRank2HoppingLocalityAnalysisRequest(
                configuration=composite_configuration,
                channel="reference",
                ordinary_model=model,
            )
        ).execute()
        construction_coordinates = VectorQuantity(
            np.asarray(
                composite_configuration.construction_reduced_momenta(),
                dtype=np.float64,
            ),
            Unitless(),
        )
        evaluation_coordinates = VectorQuantity(
            np.asarray(
                composite_configuration.evaluation_reduced_momenta(),
                dtype=np.float64,
            ),
            Unitless(),
        )
        construction = self._interpolate(model, construction_coordinates)
        complete = self._interpolate(model, evaluation_coordinates)
        request = Periodic1DRank2SupportTruncationAnalysisRequest(
            configuration=composite_configuration,
            hopping_locality_analysis=locality,
            construction_target=BandSpectrumSamples1D(
                coordinates=construction_coordinates,
                reciprocal_period=ScalarQuantity(1.0, Unitless()),
                eigenvalues=MatrixQuantity(
                    self._eigenvalues(construction),
                    Unitless(),
                ),
            ),
            complete_evaluation=complete,
            direct_evaluation=complete,
        )

        analysis = Periodic1DRank2SupportTruncationAnalyzer(request=request).execute()

        assert type(analysis) is Periodic1DRank2SupportTruncationAnalysis
        assert analysis.request is request
        assert request.channel == "reference"
        assert tuple(item.maximum_range for item in analysis.supports) == (
            composite_configuration.hopping_ranges
        )
        for support in analysis.supports:
            assert support.support_policy.translations == tuple(
                range(-support.maximum_range, support.maximum_range + 1)
            )
            assert not hasattr(support, "ordinary_omitted_block_l2_norm")
            assert (
                support.evaluation_truncation_hamiltonian_maximum_error
                == support.evaluation_total_hamiltonian_maximum_error
            )
            assert (
                support.evaluation_truncation_spectral_maximum_error
                == support.evaluation_total_spectral_maximum_error
            )

    @staticmethod
    def _model() -> BlockHoppingModel1D:
        unit = Unitless()
        representatives = tuple(range(-31, 32))
        return BlockHoppingModel1D(
            reciprocal_period=ScalarQuantity(1.0, unit),
            representatives=representatives,
            hopping_blocks=tuple(
                ComplexMatrixQuantity(
                    np.eye(2, dtype=np.complex128) / float((abs(value) + 1) ** 2),
                    unit,
                )
                for value in representatives
            ),
        )

    @staticmethod
    def _interpolate(
        model: BlockHoppingModel1D,
        coordinates: VectorQuantity,
    ) -> ReciprocalOperatorSamples1D:
        return BlockHoppingInterpolator1D(
            BlockHoppingInterpolationRequest1D(model, coordinates)
        ).execute()

    @staticmethod
    def _eigenvalues(samples: ReciprocalOperatorSamples1D) -> Float64Array:
        return np.asarray(
            [np.linalg.eigvalsh(matrix.magnitude) for matrix in samples.matrices],
            dtype=np.float64,
        )
