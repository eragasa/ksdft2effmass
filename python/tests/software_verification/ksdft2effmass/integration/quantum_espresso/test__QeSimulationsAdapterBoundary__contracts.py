r"""Software verification of the QE Project Koios Simulations adapter design.

Evidence profile: routine

Bounded artifact scope: the source-adjacent architecture document and its
machine-readable transition contract.

Facet and represented meaning

The artifact verifies that the seven qualified duplicate-owner groups remain fully
accounted for, adapter actions remain non-authorizing and effect-free, and legacy wire
removal remains gated by replacement result families rather than compatibility
fallbacks.

VVUQ and scientific exclusions

This is structural software verification only. It performs no calculator execution and
establishes no numerical verification, scientific validation, uncertainty
quantification, scientific acceptance, or publication qualification.
"""

import json
import tomllib
from pathlib import Path

import pytest

pytestmark = pytest.mark.software_verification


class TestQeSimulationsAdapterBoundary:
    """Own structural evidence for the cross-repository QE adapter design."""

    @staticmethod
    def _paths() -> tuple[Path, Path]:
        repository_root = Path(__file__).resolve().parents[6]
        architecture_root = (
            repository_root
            / "docs"
            / "architecture"
            / "v2"
            / "ksdft2effmass"
            / "integration"
            / "quantum_espresso"
        )
        return (
            architecture_root / "simulations-adapter-boundary.json",
            architecture_root / "simulations_adapter_boundary" / "index.md",
        )

    def test__QeSimulationsAdapterBoundary__accounts_for_qualified_owners(
        self,
    ) -> None:
        """Require the seven qualification groups to account for exactly 101 owners."""
        contract_path, _ = self._paths()
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
        capabilities = contract["capability_reconciliation"]
        expected_counts = {
            "native-input-and-rendering": 10,
            "executable-binding-and-preparation": 26,
            "process-capture": 14,
            "diagnostic-classification": 14,
            "workspace-and-native-output-evidence": 20,
            "terminal-and-calculator-outcome": 14,
            "provider-data-and-consumer-result-correlation": 3,
        }

        assert contract["provider_baseline"]["audit_owner_count"] == 101
        assert {item["id"]: item["qualified_owner_count"] for item in capabilities} == (
            expected_counts
        )
        assert sum(expected_counts.values()) == 101
        assert all(item["deletion_gate"] for item in capabilities)

    def test__QeSimulationsAdapterBoundary__keeps_boundary_actions_non_authorizing(
        self,
    ) -> None:
        """Require every designed adapter to be pure and non-authorizing."""
        contract_path, _ = self._paths()
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
        actions = contract["boundary_actions"]
        actions_by_id = {item["id"]: item for item in actions}

        assert len(actions_by_id) == len(actions)
        assert len({item["action_object"] for item in actions}) == len(actions)
        assert all(item["effect_free"] is True for item in actions)
        assert all(item["authority"] == "none" for item in actions)
        assert actions_by_id["prepared-calculator-input"]["action_object"] == (
            "QeCalculatorInputAdmission"
        )
        assert actions_by_id["prepared-calculator-input"]["output"] == (
            "QeCalculatorInputBinding"
        )
        assert actions_by_id["prepared-calculator-input"]["status"] == (
            "implemented_and_provider_input_resource_staging_reachable"
        )
        assert actions_by_id["prepared-calculator-input"]["implementation_path"] == (
            "ksdft2effmass.integration.quantum_espresso.calculator_input."
            "QeCalculatorInputAdmission"
        )
        assert actions_by_id["executable-binding"]["status"] == (
            "implemented_and_reachable"
        )
        assert actions_by_id["executable-binding"]["implementation_path"] == (
            "ksdft2effmass.integration.quantum_espresso.executable_binding."
            "QeExecutableBindingAdapter"
        )
        execution_evidence = actions_by_id["mechanical-execution-evidence"]
        assert execution_evidence["implementation_path"] == (
            "ksdft2effmass.integration.quantum_espresso.execution_evidence."
            "QePwEvidenceAdapter"
        )
        assert execution_evidence["intermediate_output"] == ("QePwObservation")
        assert execution_evidence["publication_action_object"] == (
            "QePwEvidencePublisher"
        )
        assert execution_evidence["publication_output"] == ("QePwPublishedEvidence")
        assert execution_evidence["result_assembly_action_object"] == (
            "QePwResultAssembler"
        )
        assert execution_evidence["result_assembly_implementation_path"] == (
            "ksdft2effmass.integration.quantum_espresso.results.assembly."
            "QePwResultAssembler"
        )
        assert execution_evidence["output"] == ["QePwResult"]
        assert execution_evidence["status"] == (
            "pw_terminal_evidence_and_result_assembly_reachable"
        )
        assert contract["provider_baseline"]["ksd_dependency_pin"] == (
            "841f5e34afd0a83c9a63da10c41a9d513c1caa80"
        )
        assert contract["claim_boundary"] == [
            "This design authorizes no Quantum ESPRESSO or Wannier90 execution.",
            (
                "This design establishes no numerical convergence, material "
                "validation, scientific acceptance or publication qualification."
            ),
            (
                "A passing software test establishes only the represented software "
                "contract."
            ),
        ]

    def test__QeSimulationsAdapterBoundary__pins_provider_baseline(self) -> None:
        """Require project metadata and the lock to select the qualified provider."""
        repository_root = Path(__file__).resolve().parents[6]
        project = tomllib.loads(
            (repository_root / "python" / "pyproject.toml").read_text(encoding="utf-8")
        )
        lock = (repository_root / "python" / "uv.lock").read_text(encoding="utf-8")
        expected_commit = "841f5e34afd0a83c9a63da10c41a9d513c1caa80"

        assert (
            project["tool"]["uv"]["sources"]["projectkoios-simulations"]["rev"]
            == expected_commit
        )
        assert lock.count(expected_commit) == 3
        assert "bbb9f1d8110ed9fe3ea1873c2366073c98f48c71" not in lock

    def test__QeSimulationsAdapterBoundary__rejects_class_substitution(
        self,
    ) -> None:
        """Require provider data and KSD execution evidence to remain distinct."""
        contract_path, _ = self._paths()
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
        rules = contract["non_substitutability"]

        assert "QeScfData is not QePwResult." in rules
        assert "QeNscfData is not QePwResult." in rules
        assert "QeBandsData is pw.x band-path data and is not QeBandsResult." in rules
        assert (
            "CalculatorPreparedExecutable is a read-only observation and grants no "
            "execution authority." in rules
        )

    def test__QeSimulationsAdapterBoundary__defines_atomic_wire_replacement(
        self,
    ) -> None:
        """Require exact PW replacement while retaining separately gated branches."""
        contract_path, document_path = self._paths()
        raw_contract = contract_path.read_text(encoding="utf-8")
        contract = json.loads(raw_contract)
        wire = contract["wire_migration"]
        document = document_path.read_text(encoding="utf-8")

        assert raw_contract == json.dumps(contract, indent=2, sort_keys=True) + "\n"
        assert wire["legacy_schema"] == "qe-result-value:1"
        assert wire["replacement_schema"] == ("quantum-espresso-simulations-result:1")
        assert wire["retained_non_synthetic_legacy_records"] == 0
        assert wire["permanent_dual_read"] is False
        assert set(wire["legacy_owner_types"]) == {
            "QeBandsResult",
            "QeExtractedObservationResult",
        }
        assert set(wire["legacy_wire_type_tags"]) == {
            "QuantumEspressoBandsResult",
            "QuantumEspressoExtractedObservationResult",
        }
        assert "QePwResult" in wire["replacement_concrete_types"]
        assert "without fallback or dual write" in wire["strategy"]
        assert "quantum-espresso-simulations-result:1" in document
        assert "No fallback read or dual write remains" in document
