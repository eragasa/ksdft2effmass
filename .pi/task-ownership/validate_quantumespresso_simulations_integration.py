#!/usr/bin/env python3
"""Completion command for the QE integration implementation operation.

This exact command is owned by the operation-scoped task-ownership manifest. It
runs deterministic software checks only and does not invoke Quantum ESPRESSO or
another scientific executable.
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from ksdft2effmass.harness.pi.conformance.python.parser import PythonTestModuleParser
from ksdft2effmass.harness.pi.conformance.python.validation import (
    PythonConformanceRequest,
    PythonConformanceValidator,
    PythonModuleSource,
)


@dataclass(frozen=True, slots=True)
class QuantumEspressoIntegrationCompletionValidator:
    """Run the bounded deterministic completion commands in declared order."""

    repository_root: Path

    def execute(self) -> int:
        """Return the first nonzero command status, otherwise zero."""
        python_root = self.repository_root / "python"
        interpreter = python_root / ".venv/bin/python"
        test_paths = (
            "tests/software_verification/ksdft2effmass/calculators/"
            "test__PlaneWaveCalculator.py",
            "tests/software_verification/ksdft2effmass/harness/pi/"
            "test__PythonTestModuleParser.py",
            "tests/software_verification/ksdft2effmass/integration/quantum_espresso",
        )
        source_paths = (
            "src/ksdft2effmass/calculators/dft/pw",
            "src/ksdft2effmass/harness/pi/conformance/python/parser.py",
            "src/ksdft2effmass/integration/quantum_espresso",
            "../examples/tutorials/silicon-scf/qe/reconstruct_silicon_scf.py",
        )
        conformance_test_paths = (
            "python/tests/software_verification/ksdft2effmass/calculators/"
            "test__PlaneWaveCalculator.py",
            "python/tests/software_verification/ksdft2effmass/harness/pi/"
            "test__PythonTestModuleParser.py",
            "python/tests/software_verification/ksdft2effmass/integration/"
            "quantum_espresso/qexsd/test__ConstructQexsdKohnShamPlaneWaveRecord.py",
            "python/tests/software_verification/ksdft2effmass/integration/"
            "quantum_espresso/qexsd/test__QexsdDocument.py",
            "python/tests/software_verification/ksdft2effmass/integration/"
            "quantum_espresso/qexsd/test__QexsdSource.py",
            "python/tests/software_verification/ksdft2effmass/integration/"
            "quantum_espresso/qexsd/test__QuantumEspressoXsdDocumentParser.py",
            "python/tests/software_verification/ksdft2effmass/integration/"
            "quantum_espresso/qexsd/test__actual_qexsd_extraction.py",
            "python/tests/software_verification/ksdft2effmass/integration/"
            "quantum_espresso/qexsd/test__plane_wave_record_rejection.py",
            "python/tests/software_verification/ksdft2effmass/integration/"
            "quantum_espresso/qexsd/test__qexsd_ownership.py",
            "python/tests/software_verification/ksdft2effmass/integration/"
            "quantum_espresso/test__LocalQuantumEspressoExecutor.py",
            "python/tests/software_verification/ksdft2effmass/integration/"
            "quantum_espresso/test__QePwInputFile.py",
            "python/tests/software_verification/ksdft2effmass/integration/"
            "quantum_espresso/test__QePwInputFileWriter.py",
            "python/tests/software_verification/ksdft2effmass/integration/"
            "quantum_espresso/test__QuantumEspressoCalculatorOutcomeResolver.py",
            "python/tests/software_verification/ksdft2effmass/integration/"
            "quantum_espresso/test__QuantumEspressoDiagnosticClassifier.py",
            "python/tests/software_verification/ksdft2effmass/integration/"
            "quantum_espresso/test__quantum_espresso_execution_contract.py",
            "python/tests/software_verification/ksdft2effmass/integration/"
            "quantum_espresso/test__quantum_espresso_local_execution.py",
        )
        conformance_status = self._class_owned_conformance(conformance_test_paths)
        if conformance_status != 0:
            return conformance_status
        example = subprocess.run(
            (
                interpreter,
                "examples/tutorials/silicon-scf/qe/reconstruct_silicon_scf.py",
            ),
            cwd=self.repository_root,
            check=False,
            capture_output=True,
        )
        expected_example = self.repository_root / (
            "examples/tutorials/silicon-scf/qe/input/si.scf.david.in"
        )
        if (
            example.returncode != 0
            or example.stderr
            or example.stdout != expected_example.read_bytes()
        ):
            return 1
        commands = (
            (interpreter, "-m", "pytest", *test_paths),
            (interpreter, "-m", "ruff", "check", *source_paths, *test_paths),
            (interpreter, "-m", "mypy", *source_paths, *test_paths),
            (
                interpreter,
                "-m",
                "ksdft2effmass.harness.cli",
                "harness-projection",
                "--repository-root",
                str(self.repository_root),
                "check",
            ),
            (
                interpreter,
                "-m",
                "ksdft2effmass.harness.cli",
                "validate-harness",
                "--repository-root",
                str(self.repository_root),
            ),
        )
        for command in commands:
            completed = subprocess.run(command, cwd=python_root, check=False)
            if completed.returncode != 0:
                return completed.returncode
        return 0

    def _class_owned_conformance(self, paths: tuple[str, ...]) -> int:
        """Run existing conformance rules over explicit class-owned method facts."""
        sources = tuple(
            PythonModuleSource(
                path=path,
                payload=(self.repository_root / path).read_bytes(),
            )
            for path in paths
        )
        models = tuple(
            PythonTestModuleParser.execute_class_owned(source.path, source.payload)
            for source in sources
            if source.payload is not None
        )
        ownership_path = self.repository_root / (
            ".pi/evidence/quantumespresso-simulations-integration/"
            "test-ownership.json"
        )
        profile_path = self.repository_root / (
            "harness/pi/evidence/python-test-evidence-profile-matrix-v1.json"
        )
        result = PythonConformanceValidator().execute(
            PythonConformanceRequest(
                sources=sources,
                ownership_path=ownership_path.relative_to(
                    self.repository_root
                ).as_posix(),
                ownership_payload=ownership_path.read_bytes(),
                profile_path=profile_path.relative_to(self.repository_root).as_posix(),
                profile_payload=profile_path.read_bytes(),
                _parsed_models=models,
            )
        )
        print(
            "class-owned conformance: "
            f"{result.status}; {result.modules} modules, "
            f"{result.test_functions} tests, "
            f"{result.unique_evidence_owners} evidence owners"
        )
        for finding in result.findings:
            print(f"{finding.code}: {finding.path}:{finding.line}: {finding.message}")
        return 0 if result.status == "PASS" else 1


def main() -> int:
    """Adapt the external command entry point to the validator ActionObject."""
    repository_root = Path(__file__).resolve().parents[2]
    return QuantumEspressoIntegrationCompletionValidator(repository_root).execute()


if __name__ == "__main__":
    sys.exit(main())
