"""Ownership checks for shared rank-N diagnostic records."""

import pytest

from ksdft2effmass.periodic1d.rankN import diagnostics
from ksdft2effmass.periodic1d.rankN.band_alignment import composite

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestRankNDiagnosticsOwnership:
    """Keep shared diagnostics outside the composite study namespace."""

    def test__records__belong_to_the_shared_rankN_owner(self) -> None:
        expected_modules = {
            "Periodic1DRankNFrameErrorResult": "diagnostics.frame",
            "Periodic1DRankNMatrixComparisonResult": "diagnostics.matrix",
            "Periodic1DRankNMatrixErrorResult": "diagnostics.matrix",
        }

        for name, module_suffix in expected_modules.items():
            record = getattr(diagnostics, name)
            assert record.__module__.endswith(module_suffix)

    def test__composite_package__does_not_reexport_shared_diagnostics(self) -> None:
        for name in diagnostics.__all__:
            assert name not in composite.__all__
            assert not hasattr(composite, name)
