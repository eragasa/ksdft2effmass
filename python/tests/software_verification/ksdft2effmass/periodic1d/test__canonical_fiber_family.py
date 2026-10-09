"""Artifact-owned evidence for the canonical periodic-1D fiber family."""

import importlib.util
from pathlib import Path

import pytest

from ksdft2effmass import periodic1d
from ksdft2effmass.periodic1d.fibers import Periodic1DFiberHamiltonianRequest
from ksdft2effmass.periodic1d.finite_differences import (
    PeriodicFiniteDifferenceFiberHamiltonian1DConstructor,
)
from ksdft2effmass.periodic1d.plane_waves import (
    PlaneWaveFiberHamiltonian1DConstructor,
)

pytestmark = pytest.mark.software_verification


class TestCanonicalPeriodic1DFiberFamily:
    """Verify reviewed imports and removal of former ownership routes."""

    def test_artifact__canonical_facade__exports_defining_class_objects(self) -> None:
        """Evidence ID: SV-PERIODIC-ONE-D-FIBER-ROUTE-001."""
        assert (
            periodic1d.Periodic1DFiberHamiltonianRequest
            is Periodic1DFiberHamiltonianRequest
        )
        assert (
            periodic1d.PlaneWaveFiberHamiltonian1DConstructor
            is PlaneWaveFiberHamiltonian1DConstructor
        )
        assert (
            periodic1d.PeriodicFiniteDifferenceFiberHamiltonian1DConstructor
            is PeriodicFiniteDifferenceFiberHamiltonian1DConstructor
        )

    def test_artifact__former_routes__are_absent_without_forwarders(self) -> None:
        """Evidence ID: SV-PERIODIC-ONE-D-FIBER-ROUTE-002."""
        former_modules = (
            "ksdft2effmass.analysis.model_systems.periodic_1d.plane_waves",
            "ksdft2effmass.analysis.model_systems.periodic_1d.finite_differences",
            "ksdft2effmass.campaigns.periodic_1d.model.plane_wave",
            "ksdft2effmass.campaigns.periodic_1d.model.finite_difference",
        )
        assert all(importlib.util.find_spec(name) is None for name in former_modules)

    def test_artifact__mirrored_layout__contains_source_and_evidence(self) -> None:
        """Evidence ID: SV-PERIODIC-ONE-D-FIBER-ROUTE-003."""
        python_root = Path(__file__).resolve().parents[4]
        source = python_root / "src" / "ksdft2effmass" / "periodic1d"
        tests = (
            python_root
            / "tests"
            / "software_verification"
            / "ksdft2effmass"
            / "periodic1d"
        )
        assert (source / "fibers.py").is_file()
        assert (source / "plane_waves.py").is_file()
        assert (source / "finite_differences.py").is_file()
        assert (tests / "test__Periodic1DFiberHamiltonianRequest.py").is_file()
