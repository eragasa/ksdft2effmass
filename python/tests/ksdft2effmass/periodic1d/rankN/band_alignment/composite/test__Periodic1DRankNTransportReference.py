"""Tests for the bounded producer-independent transport reference slice."""

import ast
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest
from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    ScalarQuantity,
    Unitless,
)

from ksdft2effmass.periodic1d.rankN.band_alignment.calculation_result import (
    Periodic1DRankNAlignmentCalculationResult,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.composite import (
    transport_reference as reference_module,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.composite.transport_reference import (  # noqa: E501
    Periodic1DRankNQualifiedTransportLinkArrays,
    Periodic1DRankNTransportReferenceAnalyzer,
    Periodic1DRankNTransportReferenceComparisonConstructor,
    Periodic1DRankNTransportReferenceRequest,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.frame_transport.result import (
    Periodic1DRankNAlignmentTransportOwnerResult,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DRankNTransportReference:
    """Establish bounded constant-frame transport coverage and independence."""

    def test__execute__reconstructs_all_constant_frame_routes(
        self,
        higher_rank_calculation_result: (Periodic1DRankNAlignmentCalculationResult),
    ) -> None:
        request = Periodic1DRankNTransportReferenceRequest(
            calculation_result=higher_rank_calculation_result
        )
        analyzer = Periodic1DRankNTransportReferenceAnalyzer(request)

        reference = analyzer.execute()

        assert analyzer.request is request
        assert len(reference.comparisons) == 45
        assert all(
            comparison.result().passed for comparison in reference.comparisons.values()
        )
        assert (
            sum(
                name.endswith(".link_singular_values") for name in reference.comparisons
            )
            == 3
        )
        assert (
            sum(
                name.endswith(".distributed_correction_step")
                for name in reference.comparisons
            )
            == 3
        )
        assert (
            sum(
                name.endswith(".endpoint_closure_defect")
                for name in reference.comparisons
            )
            == 3
        )

    def test__execute__detects_tampered_closure_actions(
        self,
        higher_rank_calculation_result: (Periodic1DRankNAlignmentCalculationResult),
    ) -> None:
        first_mesh = higher_rank_calculation_result.meshes[0]
        transport = first_mesh.transport
        assert transport is not None
        negative_identity = ComplexMatrixQuantity(
            -np.eye(transport.retained_rank, dtype=np.complex128),
            Unitless(),
        )
        tampered_transport = replace(
            transport,
            primitive_last_to_sewn_first_right_unitary=negative_identity,
            sewn_first_to_primitive_last_right_unitary=negative_identity,
            distributed_closure_correction_right_unitary_step=negative_identity,
        )
        tampered_mesh = replace(first_mesh, transport=tampered_transport)
        tampered_result = replace(
            higher_rank_calculation_result,
            meshes=(tampered_mesh, *higher_rank_calculation_result.meshes[1:]),
        )

        reference = Periodic1DRankNTransportReferenceAnalyzer(
            Periodic1DRankNTransportReferenceRequest(calculation_result=tampered_result)
        ).execute()

        comparison = reference.comparisons[
            "mesh[513].transport.distributed_correction_step"
        ]
        assert not comparison.result().passed

    def test__qualified_link_arrays__own_immutable_transport_evidence(
        self,
        higher_rank_calculation_result: Periodic1DRankNAlignmentCalculationResult,
    ) -> None:
        transport = higher_rank_calculation_result.meshes[0].transport
        assert type(transport) is Periodic1DRankNAlignmentTransportOwnerResult

        arrays = Periodic1DRankNQualifiedTransportLinkArrays(transport)

        assert arrays.singular_values.shape == (513, transport.retained_rank)
        assert arrays.cutoffs.shape == (513,)
        assert arrays.margins.shape == (513,)
        assert arrays.numerical_ranks.shape == (513,)
        assert arrays.unitarity_defects.shape == (513,)
        assert not arrays.singular_values.flags.writeable
        assert not arrays.cutoffs.flags.writeable
        assert not arrays.margins.flags.writeable
        assert not arrays.numerical_ranks.flags.writeable
        assert not arrays.unitarity_defects.flags.writeable

    def test__comparison_constructor__binds_unit_aware_tolerance(self) -> None:
        constructor = Periodic1DRankNTransportReferenceComparisonConstructor(
            observed=ScalarQuantity(1.0, Unitless()),
            reference=ScalarQuantity(1.0, Unitless()),
            absolute_tolerance=1.0e-12,
        )

        comparison = constructor.execute()

        assert comparison.result().passed
        assert comparison.tolerance == ScalarQuantity(1.0e-12, Unitless())

    def test__comparison_constructor__rejects_boolean_tolerance(self) -> None:
        with pytest.raises(TypeError, match="built-in float"):
            Periodic1DRankNTransportReferenceComparisonConstructor(
                observed=ScalarQuantity(1.0, Unitless()),
                reference=ScalarQuantity(1.0, Unitless()),
                absolute_tolerance=True,
            )

    def test__request__rejects_non_result_subject(self) -> None:
        with pytest.raises(TypeError, match="exact calculation result"):
            Periodic1DRankNTransportReferenceRequest(
                calculation_result="not-a-result"  # type: ignore[arg-type]
            )

    def test__module__does_not_import_transport_backend_or_producer_actions(
        self,
    ) -> None:
        module_path = Path(reference_module.__file__).resolve()
        tree = ast.parse(module_path.read_text(encoding="utf-8"), filename=module_path)
        imported_modules = {
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module is not None
        }

        assert "calculation" not in imported_modules
        assert "model" not in imported_modules
        assert "analysis" not in imported_modules
        assert "analysis.calculation" not in imported_modules
        assert all(
            not module.startswith(
                "projectkoios.physkit.solidstate.electronic.frame_transport"
            )
            for module in imported_modules
        )
        assert all(
            not module.endswith("frame_transport.analysis")
            for module in imported_modules
        )
