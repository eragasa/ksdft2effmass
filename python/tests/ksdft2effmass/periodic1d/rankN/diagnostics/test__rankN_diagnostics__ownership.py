"""Ownership checks for shared rank-N diagnostic records."""

import pytest

from ksdft2effmass.periodic1d.rankN import diagnostics
from ksdft2effmass.periodic1d.rankN.band_alignment import composite
from ksdft2effmass.periodic1d.rankN.diagnostics.frame import (
    Periodic1DRankNFrameErrorResult,
)
from ksdft2effmass.periodic1d.rankN.diagnostics.matrix import (
    Periodic1DRankNMatrixComparisonResult,
    Periodic1DRankNMatrixErrorResult,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestRankNDiagnosticsOwnership:
    """Keep shared diagnostics outside the composite study namespace."""

    def test__records__belong_to_the_shared_rankN_owner(self) -> None:
        expected_modules = {
            Periodic1DRankNFrameErrorResult: "diagnostics.frame",
            Periodic1DRankNMatrixComparisonResult: "diagnostics.matrix",
            Periodic1DRankNMatrixErrorResult: "diagnostics.matrix",
        }

        for record, module_suffix in expected_modules.items():
            assert record.__module__.endswith(module_suffix)

    def test__capability_packages__are_inert_namespaces(self) -> None:
        for package in (diagnostics, composite):
            assert not hasattr(package, "__all__")
            assert not any(name.startswith("Periodic1DRankN") for name in vars(package))
