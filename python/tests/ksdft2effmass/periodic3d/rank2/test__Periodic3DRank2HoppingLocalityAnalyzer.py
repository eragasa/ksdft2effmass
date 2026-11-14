"""Periodic-3D rank-two hopping-locality action contracts."""

from __future__ import annotations

import numpy as np
import pytest
from projectkoios.numerics.finite_periodic.numpy.matrix_series import (
    NumpyFiniteFourierMatrixSeries,
)
from projectkoios.physkit.periodic.lattice import DirectLattice2D, DirectLattice3D
from projectkoios.physkit.periodic.lattice.finite_domain import LatticeDimension
from projectkoios.physkit.solidstate.tb.diagnostics import BlockHoppingPowerAnalyzer
from projectkoios.physkit.units import PhysicalUnit

from ksdft2effmass.band_equivalence_hopping_locality.block_hopping import (
    FourierSeriesBlockHoppingRepresentation,
    FourierSeriesBlockHoppingRepresentationRequest,
)
from ksdft2effmass.periodic.models import PeriodicModelRole
from ksdft2effmass.periodic.operators import LabeledComponentBasisCoordinate
from ksdft2effmass.periodic.periodic2d.operators import Periodic2DBasisIdentity
from ksdft2effmass.periodic.periodic2d.rank2.models import (
    Periodic2DRank2BlockHoppingModel,
)
from ksdft2effmass.periodic.periodic3d.operators import Periodic3DBasisIdentity
from ksdft2effmass.periodic.periodic3d.rank2.models import (
    Periodic3DRank2BlockHoppingModel,
)
from ksdft2effmass.periodic2d.geometry import Periodic2DLatticeGeometry
from ksdft2effmass.periodic3d.geometry import Periodic3DLatticeGeometry
from ksdft2effmass.periodic3d.rank2.hopping_locality.analysis import (
    Periodic3DRank2HoppingLocalityAnalyzer,
)
from ksdft2effmass.periodic3d.rank2.hopping_locality.request import (
    Periodic3DRank2HoppingLocalityAnalysisRequest,
)
from ksdft2effmass.periodic3d.rank2.hopping_locality.result import (
    Periodic3DRank2HoppingLocalityAnalysis,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic3DRank2HoppingLocalityAnalyzer:
    """Bind one model and preserve its three-dimensional metric-shell identity."""

    _BASIS_COORDINATES = (
        LabeledComponentBasisCoordinate(label="retained-component-0"),
        LabeledComponentBasisCoordinate(label="retained-component-1"),
    )

    @staticmethod
    def _series(dimension: int) -> NumpyFiniteFourierMatrixSeries:
        """Construct a three-term rank-two Fourier series in a selected dimension.

        Parameters
        ----------
        dimension
            Number of integer components in each ordinary-lattice mode.

        Returns
        -------
        NumpyFiniteFourierMatrixSeries
            Symmetric nearest-cell series with an onsite coefficient of twice the
            identity and unit-identity coefficients at opposite displacements.

        """
        modes = np.zeros((3, dimension), dtype=np.int64)
        modes[0, 0] = -1
        modes[2, 0] = 1
        blocks = np.zeros((3, 2, 2), dtype=np.complex128)
        blocks[0] = np.eye(2, dtype=np.complex128)
        blocks[1] = 2.0 * np.eye(2, dtype=np.complex128)
        blocks[2] = np.eye(2, dtype=np.complex128)
        return NumpyFiniteFourierMatrixSeries.from_arrays(dimension, modes, blocks)

    @classmethod
    def _model(
        cls,
        dimension: int,
    ) -> Periodic2DRank2BlockHoppingModel | Periodic3DRank2BlockHoppingModel:
        """Promote the controlled series into one exact dimensional model.

        Parameters
        ----------
        dimension
            Spatial dimension, restricted by this fixture to two or three.

        Returns
        -------
        Periodic2DRank2BlockHoppingModel | Periodic3DRank2BlockHoppingModel
            Model whose ordered primitive basis and physical length unit are explicit.

        Notes
        -----
        The Fourier conversion creates provider coefficient storage. Model construction
        separately correlates that storage with the direct-lattice coordinate map.

        """
        representation = FourierSeriesBlockHoppingRepresentation(
            request=FourierSeriesBlockHoppingRepresentationRequest(
                identifier="ordinary-hopping",
                energy_reference="synthetic-zero",
                basis_identifier="retained-rank-two",
                series=cls._series(dimension),
            )
        ).result()
        if dimension == 2:
            # Build a dimensionally valid counterexample for the ownership rejection
            # test; it is a complete 2D model, not a malformed 3D value.
            geometry_2d = Periodic2DLatticeGeometry.from_direct_lattice(
                DirectLattice2D(
                    np.array([1.0, 0.0], dtype=np.float64),
                    np.array([0.0, 1.0], dtype=np.float64),
                ),
                PhysicalUnit("bohr"),
            )
            return Periodic2DRank2BlockHoppingModel(
                identifier="ordinary-hopping",
                role=PeriodicModelRole.CONTROL_MODEL,
                geometry=geometry_2d,
                basis=Periodic2DBasisIdentity(
                    display_identifier="retained-rank-two",
                    coordinates=cls._BASIS_COORDINATES,
                ),
                representation=representation,
            )
        # The columns of this direct-lattice matrix are the ordered primitive vectors.
        # The unit declaration supplies the physical dimensions omitted by a bare
        # numerical matrix or Gram metric.
        geometry_3d = Periodic3DLatticeGeometry.from_direct_lattice(
            DirectLattice3D(
                np.array([1.0, 0.0, 0.0], dtype=np.float64),
                np.array([0.0, 1.0, 0.0], dtype=np.float64),
                np.array([0.0, 0.0, 1.0], dtype=np.float64),
            ),
            PhysicalUnit("bohr"),
        )
        return Periodic3DRank2BlockHoppingModel(
            identifier="ordinary-hopping",
            role=PeriodicModelRole.CONTROL_MODEL,
            geometry=geometry_3d,
            basis=Periodic3DBasisIdentity(
                display_identifier="retained-rank-two",
                coordinates=cls._BASIS_COORDINATES,
            ),
            representation=representation,
        )

    def test_executes_one_typed_three_dimensional_model(self) -> None:
        """Resolve shell power while preserving the model's 3D geometry identity."""
        model = self._model(3)
        assert type(model) is Periodic3DRank2BlockHoppingModel
        request = Periodic3DRank2HoppingLocalityAnalysisRequest(
            model=model,
            shell_indices=(1, 0, 1),
        )

        analyzer = Periodic3DRank2HoppingLocalityAnalyzer(
            request=request,
            power_analyzer=BlockHoppingPowerAnalyzer(),
        )
        result = analyzer.execute()

        assert request.band_subspace_rank == 2
        assert result.band_subspace_rank == 2
        assert analyzer.band_subspace_rank == 2
        assert type(result) is Periodic3DRank2HoppingLocalityAnalysis
        assert result.request is request
        assert result.retained_rank == 2
        # Frobenius power is normalized by retained rank two. The onsite block ``2 I``
        # contributes 4 after normalization, while the two unit-identity neighbors
        # together contribute 2 to shell one.
        assert result.normalized_power_at_shell(0) == pytest.approx(4.0)
        assert result.normalized_power_at_shell(1) == pytest.approx(2.0)
        assert all(
            power.displacement.dimension is LatticeDimension.THREE
            for power in result.powers
        )

    def test_rejects_a_two_dimensional_model(self) -> None:
        """Reject cross-dimensional model substitution at the request boundary."""
        with pytest.raises(TypeError, match="Periodic3DRank2BlockHoppingModel"):
            Periodic3DRank2HoppingLocalityAnalysisRequest(
                model=self._model(2),  # type: ignore[arg-type]
                shell_indices=(1, 0, 1),
            )
