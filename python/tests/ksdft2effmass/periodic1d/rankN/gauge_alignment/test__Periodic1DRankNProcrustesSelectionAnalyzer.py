"""Tests for typed rank-N Procrustes selection outcomes."""

from dataclasses import replace

import numpy as np
import pytest
from projectkoios.numerics.numpy.validation import NumpyImmutableArrayConstructor
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesDefinition,
    NumpyBatchedComplexUnitaryProcrustesSolver,
)
from projectkoios.optimization.alignment.procrustes import (
    ComplexUnitaryProcrustesRankCutoffRule,
    ComplexUnitaryProcrustesTolerance,
)

from ksdft2effmass.periodic1d.rankN.gauge_alignment.definition import (
    Periodic1DRankNGaugeAlignment,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.procrustes.selection import (
    Periodic1DRankNProcrustesSelectionAnalyzer,
    Periodic1DRankNProcrustesSelectionRequest,
    Periodic1DRankNResolvedProcrustesSelection,
    Periodic1DRankNUnresolvedProcrustesSelection,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.status import (
    Periodic1DRankNAlignmentBackendExceptionCode,
    Periodic1DRankNAlignmentStatus,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


def _request() -> Periodic1DRankNProcrustesSelectionRequest:
    source = np.zeros((513, 6, 3), dtype=np.complex128)
    source[:, :3, :] = np.eye(3, dtype=np.complex128)
    target = source.copy()
    source = NumpyImmutableArrayConstructor(
        source,
        "source",
        np.dtype(np.complex128),
    ).execute()
    target = NumpyImmutableArrayConstructor(
        target,
        "target",
        np.dtype(np.complex128),
    ).execute()
    return Periodic1DRankNProcrustesSelectionRequest(
        case_identity="r03-L01",
        retained_rank=3,
        circuit_depth=1,
        gauge_alignment=Periodic1DRankNGaugeAlignment.POINTWISE_UNITARY,
        selection_mesh_size=513,
        source=source,
        target=target,
        tolerance=ComplexUnitaryProcrustesTolerance(
            rank_absolute=1.0e-12,
            rank_relative=1.0e-10,
            validation_absolute=1.0e-12,
            validation_relative=1.0e-10,
            rank_cutoff_rule=ComplexUnitaryProcrustesRankCutoffRule.MAXIMUM,
        ),
        alignment_integrity_tolerance=1.0e-10,
    )


class TestPeriodic1DRankNProcrustesSelectionAnalyzer:
    """Establish immutable requests and disjoint completed/failure outcomes."""

    def test__execute__returns_resolved_right_actions(self) -> None:
        request = _request()

        selection = Periodic1DRankNProcrustesSelectionAnalyzer(
            request,
            NumpyBatchedComplexUnitaryProcrustesSolver(),
        ).execute()

        assert type(selection) is Periodic1DRankNResolvedProcrustesSelection
        assert selection.diagnostics.status.status is (
            Periodic1DRankNAlignmentStatus.QUALIFIED
        )
        assert selection.right_unitaries.shape == (513, 3, 3)
        assert not request.source.flags.writeable
        assert not request.target.flags.writeable
        assert not selection.right_unitaries.flags.writeable

    def test__execute__returns_unresolved_without_right_actions(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        def fail_svd(
            solver: NumpyBatchedComplexUnitaryProcrustesSolver,
            definition: NumpyBatchedComplexUnitaryProcrustesDefinition,
        ) -> None:
            del solver, definition
            raise np.linalg.LinAlgError("synthetic backend failure")

        monkeypatch.setattr(
            NumpyBatchedComplexUnitaryProcrustesSolver,
            "solve",
            fail_svd,
        )

        selection = Periodic1DRankNProcrustesSelectionAnalyzer(
            _request(),
            NumpyBatchedComplexUnitaryProcrustesSolver(),
        ).execute()

        assert type(selection) is Periodic1DRankNUnresolvedProcrustesSelection
        assert selection.diagnostics.status.status is (
            Periodic1DRankNAlignmentStatus.NUMERICALLY_UNRESOLVED
        )
        assert selection.diagnostics.status.backend_exception_code is (
            Periodic1DRankNAlignmentBackendExceptionCode.NONCONVERGENCE
        )
        assert not hasattr(selection, "right_unitaries")

    def test__request__preserves_immutable_array_identity_and_rejects_mutable_arrays(
        self,
    ) -> None:
        request = _request()
        source = request.source
        target = request.target

        reconstructed = replace(request, source=source, target=target)

        assert reconstructed.source is source
        assert reconstructed.target is target
        mutable = np.array(source, copy=True)
        with pytest.raises(ValueError, match="read-only"):
            replace(request, source=mutable)

    @pytest.mark.parametrize(
        ("field", "value"),
        (
            ("retained_rank", True),
            ("circuit_depth", True),
            ("selection_mesh_size", True),
        ),
    )
    def test__request__rejects_boolean_integer_fields(
        self,
        field: str,
        value: bool,
    ) -> None:
        with pytest.raises(TypeError, match="built-in integer"):
            replace(_request(), **{field: value})  # type: ignore[arg-type]

    def test__request__rejects_nonprocrustes_alignment(self) -> None:
        with pytest.raises(ValueError, match="global or pointwise"):
            replace(
                _request(),
                gauge_alignment=Periodic1DRankNGaugeAlignment.IDENTITY,
            )
