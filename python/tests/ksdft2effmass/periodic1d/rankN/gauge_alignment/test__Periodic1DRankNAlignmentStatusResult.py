"""Tests for typed rank-N gauge-alignment status records."""

from dataclasses import replace

import pytest

from ksdft2effmass.periodic1d.rankN.gauge_alignment.definition import (
    Periodic1DRankNGaugeAlignment,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.status import (
    Periodic1DRankNAlignmentBackendExceptionCode,
    Periodic1DRankNAlignmentStatus,
    Periodic1DRankNAlignmentStatusResult,
    Periodic1DRankNGlobalUnitaryDownstreamApplicability,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DRankNAlignmentStatusResult:
    """Establish gauge-specific dispositions and canonical record boundaries."""

    def test__round_trip__preserves_qualified_global_unitary(self) -> None:
        result = Periodic1DRankNAlignmentStatusResult(
            case_identity="r03-L01",
            retained_rank=3,
            circuit_depth=1,
            construction_mesh_size=513,
            gauge_alignment=Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY,
            status=Periodic1DRankNAlignmentStatus.QUALIFIED,
            global_unitary_downstream_applicability=(
                Periodic1DRankNGlobalUnitaryDownstreamApplicability.APPLICABLE
            ),
            backend_exception_code=None,
        )

        reconstructed = Periodic1DRankNAlignmentStatusResult.from_json(result.to_json())

        assert reconstructed == result
        assert reconstructed.to_json() == result.to_json()

        old_key = dict(result.to_dict())
        old_key["channel"] = old_key.pop("gauge_alignment")
        with pytest.raises(ValueError, match="status fields do not match"):
            Periodic1DRankNAlignmentStatusResult.from_dict(old_key)

    def test__round_trip__retains_failure_code_without_exception_text(self) -> None:
        result = Periodic1DRankNAlignmentStatusResult(
            case_identity="r04-L02",
            retained_rank=4,
            circuit_depth=2,
            construction_mesh_size=1025,
            gauge_alignment=Periodic1DRankNGaugeAlignment.POINTWISE_UNITARY,
            status=Periodic1DRankNAlignmentStatus.NUMERICALLY_UNRESOLVED,
            global_unitary_downstream_applicability=None,
            backend_exception_code=(
                Periodic1DRankNAlignmentBackendExceptionCode.NONCONVERGENCE
            ),
        )

        wire = result.to_json()

        assert Periodic1DRankNAlignmentStatusResult.from_json(wire) == result
        assert result.to_dict()["backend_exception_code"] == "backend-nonconvergence"
        assert b"exception_text" not in wire

    def test__admission__rejects_alignment_and_applicability_mismatch(self) -> None:
        valid = Periodic1DRankNAlignmentStatusResult(
            case_identity="r03-L01",
            retained_rank=3,
            circuit_depth=1,
            construction_mesh_size=513,
            gauge_alignment=Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY,
            status=Periodic1DRankNAlignmentStatus.AGGREGATE_RANK_DEFICIENT,
            global_unitary_downstream_applicability=(
                Periodic1DRankNGlobalUnitaryDownstreamApplicability.INAPPLICABLE_AGGREGATE_RANK_DEFICIENT
            ),
            backend_exception_code=None,
        )

        with pytest.raises(ValueError, match="disagree"):
            replace(
                valid,
                global_unitary_downstream_applicability=(
                    Periodic1DRankNGlobalUnitaryDownstreamApplicability.APPLICABLE
                ),
            )
        with pytest.raises(ValueError, match="not admissible"):
            replace(
                valid,
                gauge_alignment=Periodic1DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE,
            )
        with pytest.raises(ValueError, match="not in the frozen inventory"):
            replace(valid, construction_mesh_size=512)
