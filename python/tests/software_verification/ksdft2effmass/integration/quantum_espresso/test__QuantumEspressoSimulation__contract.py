r"""Software verification of ``QuantumEspressoSimulation``.

Evidence profile: routine

Bounded artifact scope: the public import and inward dependency surfaces of
``QuantumEspressoSimulation``.

Facet and represented meaning

The artifact represents integration ownership of the concrete QE Simulation
composition and the one-way dependencies on generic calculator and Workflow ports.

Intrinsic and cross-object scope

Tests cover canonical package export and source-level dependency direction. Constructor,
correlation, immutability, and result-role behavior belong to the class-owned module.

VVUQ and scientific exclusions

This structural software verification invokes no calculator or executor and establishes
no execution authority, numerical verification, scientific validation, uncertainty
quantification, physical correctness, production readiness, or human acceptance.
"""

import ast
from pathlib import Path

import pytest

import ksdft2effmass.calculators as calculators
import ksdft2effmass.integration.quantum_espresso as qe
import ksdft2effmass.workflows as workflows
from ksdft2effmass.integration.quantum_espresso import QuantumEspressoSimulation

pytestmark = pytest.mark.software_verification
SUT = QuantumEspressoSimulation


class TestQuantumEspressoSimulationContract:
    """Own public-surface and dependency evidence for the QE Simulation contract."""

    def test_public_api__package__exports_simulation_from_qe_only(self) -> None:
        """Evidence ID: SV-QE-SIM-001

        Requirement: The concrete Simulation composition is QE-integration-owned,
        while generic calculator and Workflow packages expose no QE class.

        Acceptance: The public QE name resolves to its canonical defining module and
        the generic package roots do not expose it.
        """
        assert SUT.__module__ == (
            "ksdft2effmass.integration.quantum_espresso.simulation"
        )
        assert "QuantumEspressoSimulation" in qe.__all__
        assert not hasattr(calculators, "QuantumEspressoSimulation")
        assert not hasattr(workflows, "QuantumEspressoSimulation")

    def test_artifact__dependency__generic_ports_import_no_qe_owner(self) -> None:
        """Evidence ID: SV-QE-SIM-005

        Requirement: The defining generic calculator and Workflow effect-port modules
        remain inward dependencies and do not import the QE composition owner.

        Acceptance: Parsed syntax trees for both port-defining modules contain no
        ``ksdft2effmass.integration.quantum_espresso`` import target.
        """
        source_root = Path(__file__).resolve().parents[5] / "src" / "ksdft2effmass"
        calculator_tree = ast.parse(
            (source_root / "calculators/dft/pw/_calculator.py").read_text(
                encoding="utf-8"
            )
        )
        workflow_tree = ast.parse(
            (source_root / "workflows/control/dispatch.py").read_text(encoding="utf-8")
        )

        assert "ksdft2effmass.integration.quantum_espresso" not in ast.dump(
            calculator_tree
        )
        assert "ksdft2effmass.integration.quantum_espresso" not in ast.dump(
            workflow_tree
        )
