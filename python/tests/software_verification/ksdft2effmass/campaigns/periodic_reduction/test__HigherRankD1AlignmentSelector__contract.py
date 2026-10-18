"""Software verification for higher-rank D1 alignment selection dispositions."""

from __future__ import annotations

import numpy as np
import pytest
from projectkoios.numerics.numpy.validation import immutable_complex128_array

from ksdft2effmass.campaigns.periodic_reduction.higher_rank_d1 import (
    HigherRankD1A1QualifiedSelection,
    HigherRankD1A1RankDeficientSelection,
    HigherRankD1A2RankDeficientSelection,
    HigherRankD1A2Selection,
    HigherRankD1AlignmentBackendError,
    HigherRankD1AlignmentSelector,
    HigherRankD1ModelConstructor,
)

pytestmark = pytest.mark.software_verification


class TestHigherRankD1AlignmentSelector:
    """Establish qualified, deficient, and thrown backend outcomes."""

    def test_select__recovers_right_action_and_retains_global_family(self) -> None:
        """A2 reconstructs the inverse while A1 selects one final-mesh unitary."""
        constructor = HigherRankD1ModelConstructor()
        selector = HigherRankD1AlignmentSelector()
        final = constructor.execute(
            3,
            2,
            constructor.construction_coordinates(2049),
        )

        a1 = selector.select_a1(final.candidate_frames, final.reference_frames)
        assert isinstance(a1, HigherRankD1A1QualifiedSelection)
        assert a1.status == "qualified"
        assert a1.rank_margin > 0.9
        assert a1.unitarity_defect < 2.0e-15

        coarse = constructor.execute(
            3,
            2,
            constructor.construction_coordinates(513),
        )
        a2 = selector.select_a2(coarse.candidate_frames, coarse.reference_frames)
        assert isinstance(a2, HigherRankD1A2Selection)
        expected = np.swapaxes(coarse.gauges.conjugate(), -1, -2)
        assert a2.status == "qualified"
        assert a2.deficient_indices == ()
        assert np.max(np.abs(a2.transformations - expected)) < 2.0e-15
        recovered = (
            np.swapaxes(a2.transformations.conjugate(), -1, -2)
            @ coarse.attacked_operators
            @ a2.transformations
        )
        assert (
            np.max(
                np.linalg.norm(recovered - coarse.reference_operators, axis=(-2, -1))
            )
            < 3.0e-15
        )

    def test_select__rejects_noncanonical_mutable_frame_arrays(self) -> None:
        """The Optimization immutable-array boundary rejects mutable inputs."""
        mutable = np.zeros((3, 6, 3), dtype=np.complex128)

        with pytest.raises(ValueError, match="must be read-only"):
            HigherRankD1AlignmentSelector().select_a2(mutable, mutable)

    def test_select__returns_rank_deficiency_without_null_space_completion(
        self,
    ) -> None:
        """Deficient A1/A2 inputs retain evidence and omit transformations."""
        selector = HigherRankD1AlignmentSelector()
        reference = immutable_complex128_array(
            np.broadcast_to(np.eye(6, 3, dtype=np.complex128), (2049, 6, 3)).copy(),
            "reference",
        )
        zero = immutable_complex128_array(
            np.zeros((2049, 6, 3), dtype=np.complex128), "zero"
        )

        a1 = selector.select_a1(zero, reference)
        a2 = selector.select_a2(zero[:3], reference[:3])

        assert isinstance(a1, HigherRankD1A1RankDeficientSelection)
        assert a1.status == "aggregate-rank-deficient"
        assert isinstance(a2, HigherRankD1A2RankDeficientSelection)
        assert a2.status == "pointwise-rank-deficient"
        assert a2.deficient_indices == (0, 1, 2)
        assert a2.numerical_ranks == (0, 0, 0)
        assert not hasattr(a1, "transformation")
        assert not hasattr(a2, "transformations")

    def test_select__throws_documented_backend_failure(self) -> None:
        """Nonfinite backend arithmetic leaves selection through one typed exception."""
        selector = HigherRankD1AlignmentSelector()
        huge = immutable_complex128_array(
            np.full((2049, 6, 3), 1.0e308 + 0.0j, dtype=np.complex128),
            "huge",
        )

        with pytest.raises(HigherRankD1AlignmentBackendError) as a1_error:
            selector.select_a1(huge, huge)
        with pytest.raises(HigherRankD1AlignmentBackendError) as a2_error:
            selector.select_a2(huge[:3], huge[:3])

        assert isinstance(a1_error.value.backend_exception, FloatingPointError)
        assert isinstance(a2_error.value.backend_exception, FloatingPointError)
