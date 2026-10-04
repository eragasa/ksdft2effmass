"""Software verification of ``Periodic1DBandFrameRetainedSubspace``.

Evidence profile: routine

Facet and represented meaning
-----------------------------
The class binds gauge-dependent reciprocal-path frames to an identified scientific
retained space without equating the frame with that space.

Intrinsic and cross-object scope
--------------------------------
Exact types, one-dimensional parentage, rank, and ambient dimension are covered.

VVUQ and scientific exclusions
------------------------------
Synthetic frames establish software compatibility only, not smoothness, convergence,
topology, scientific validation, or uncertainty quantification.
"""

import numpy as np
import pytest

from ksdft2effmass.operators import ComplexMatrixQuantity, ScalarQuantity, Unitless
from ksdft2effmass.periodic import (
    PeriodicOperatorReference,
    PeriodicRetainedSubspace,
    PeriodicRetentionDefinition,
    PeriodicRetentionKind,
)
from ksdft2effmass.periodic1d import Periodic1DBandFrameRetainedSubspace
from ksdft2effmass.solid_state import (
    CenteredUniformReciprocalMesh1D,
    ReciprocalBandFramePath1D,
)

pytestmark = pytest.mark.software_verification


class TestPeriodic1DBandFrameRetainedSubspace:
    """Own compatibility evidence for reciprocal-frame retained spaces."""

    @staticmethod
    def make_retained_subspace(ambient_dimension: int = 3) -> PeriodicRetainedSubspace:
        """Return one synthetic rank-two scientific retained space."""
        definition = PeriodicRetentionDefinition(
            "retention",
            PeriodicOperatorReference("parent", "operator", "ambient", 1),
            "retained",
            PeriodicRetentionKind.SELECTED_BANDS,
            2,
            ("band-0", "band-1"),
            "mesh",
            "selection",
            (),
            "provenance",
        )
        return PeriodicRetainedSubspace(
            definition,
            "ambient",
            ambient_dimension,
            "spinless",
            "scalar",
            "periodic-sewing",
            "frame-provenance",
        )

    @staticmethod
    def make_frame_path() -> ReciprocalBandFramePath1D:
        """Return two identical synthetic three-by-two orthonormal frames."""
        mesh = CenteredUniformReciprocalMesh1D(ScalarQuantity(1.0, Unitless()), 2)
        matrix = ComplexMatrixQuantity(
            np.asarray(((1.0, 0.0), (0.0, 1.0), (0.0, 0.0))), Unitless()
        )
        sewing = ComplexMatrixQuantity(np.eye(3, dtype=np.complex128), Unitless())
        return ReciprocalBandFramePath1D(mesh, (matrix, matrix), sewing, 1.0e-14)

    def test_construction__frame_path__binds_matching_dimensions(self) -> None:
        """Evidence ID: SV-PERIODIC1D-BAND-FRAME-SUBSPACE-001

        Requirement: A frame path represents the declared retained rank and ambient
        dimension while the scientific retained-space identity remains separate.

        Acceptance: Construction preserves both exact input objects.
        """
        retained = self.make_retained_subspace()
        frame_path = self.make_frame_path()
        result = Periodic1DBandFrameRetainedSubspace(
            retained,
            frame_path,
            "d5a15821a040358ecad5d1794a9eb3f8cd464f09cc81ad37e470d3ec4e7679a2",
        )
        assert result.retained_subspace is retained
        assert result.frame_path is frame_path
        assert result.frame_content_sha256 == (
            "d5a15821a040358ecad5d1794a9eb3f8cd464f09cc81ad37e470d3ec4e7679a2"
        )

    def test_construction__ambient_dimension__rejects_mismatch(self) -> None:
        """Evidence ID: SV-PERIODIC1D-BAND-FRAME-SUBSPACE-002

        Requirement: Frame coordinates use the retained space's declared ambient
        representation dimension.

        Acceptance: Dimension disagreement raises ``ValueError``.
        """
        with pytest.raises(ValueError, match="ambient dimension must equal"):
            Periodic1DBandFrameRetainedSubspace(
                self.make_retained_subspace(4),
                self.make_frame_path(),
                "d5a15821a040358ecad5d1794a9eb3f8cd464f09cc81ad37e470d3ec4e7679a2",
            )

    def test_construction__frame_content_sha256__rejects_wrong_content(self) -> None:
        """Evidence ID: SV-PERIODIC1D-BAND-FRAME-SUBSPACE-003

        Requirement: The typed frame binding authenticates canonical frame-matrix
        bytes rather than treating a digest as mathematical retained-space identity.

        Acceptance: A valid but nonmatching lowercase SHA-256 digest raises
        ``ValueError``.
        """
        with pytest.raises(ValueError, match="must authenticate frame matrices"):
            Periodic1DBandFrameRetainedSubspace(
                self.make_retained_subspace(), self.make_frame_path(), "0" * 64
            )

    def test_construction__frame_content_sha256__rejects_malformed_digest(
        self,
    ) -> None:
        """Evidence ID: SV-PERIODIC1D-BAND-FRAME-SUBSPACE-004

        Requirement: Frame content identity uses exact lowercase SHA-256 syntax.

        Acceptance: A malformed digest raises ``ValueError`` before content
        authentication.
        """
        with pytest.raises(ValueError, match="lowercase SHA-256 hexadecimal"):
            Periodic1DBandFrameRetainedSubspace(
                self.make_retained_subspace(), self.make_frame_path(), "not-a-digest"
            )
