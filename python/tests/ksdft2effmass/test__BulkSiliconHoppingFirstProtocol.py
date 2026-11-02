"""Ownership and ordering checks for the bulk-silicon hopping-first protocol."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import cast

import pytest

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestBulkSiliconHoppingFirstProtocol:
    """Preserve bound protocols and keep Pareto characterization hopping-first."""

    def test_preserves_bound_protocol_bytes_and_selects_new_authority(
        self,
        repository_root: Path,
    ) -> None:
        protocol_root = (
            repository_root / "calculations" / "Si" / "bulk" / "research-protocol"
        )
        expected_hashes = {
            "research-protocol.tex": (
                "230aa0cebb37cf28a2e2e7cdcf1186d5ded98971217be3bbb8beadc2879d9dad"
            ),
            "controlled-reduction-protocol.tex": (
                "80cf67acf00d6b906a64471ed06379a321bca71ed5b6636174c634a30d8b2380"
            ),
            "controlled-reduction-protocol-post-s110.tex": (
                "3ec2902a94ebe78eba1e223a0ee4ef99075f4bd86238398b67d370fa88224653"
            ),
            "controlled-reduction-protocol-hopping-first.tex": (
                "d28146dc2c481d4793b7e8294c4bc43196eba387bce3052b24d8bde269859f79"
            ),
        }

        for filename, expected_hash in expected_hashes.items():
            assert (
                hashlib.sha256((protocol_root / filename).read_bytes()).hexdigest()
                == expected_hash
            )

        owner = (protocol_root / "README.md").read_text(encoding="utf-8")
        assert "controlled-reduction-protocol-hopping-first.tex" in owner
        assert "controlled-reduction-protocol-post-s110.tex" in owner
        assert "retained byte-for-byte" in owner
        assert "HF0--HF4" in owner

    def test_orders_complete_hopping_analysis_before_slater_koster(
        self,
        repository_root: Path,
    ) -> None:
        protocol = (
            repository_root
            / "calculations"
            / "Si"
            / "bulk"
            / "research-protocol"
            / "controlled-reduction-protocol-hopping-first.tex"
        ).read_text(encoding="utf-8")

        ordered_markers = (
            r"\section{Hopping-before-Slater--Koster dependency}",
            r"\subsection{HF0: representation and authority gate}",
            r"\subsection{HF1: complete hopping representation before support removal}",
            r"\subsection{HF2: development evaluation and descriptive locality}",
            r"\subsection{HF3: support consequence and current disposition}",
            r"\subsection{HF4: handoff to constrained parameterization}",
            r"\section{Post-S110 Slater--Koster continuation after hopping analysis}",
        )
        positions = tuple(protocol.index(marker) for marker in ordered_markers)
        assert positions == tuple(sorted(positions))

        assert (
            "Analyze the complete set of 383 element-resolved WS representatives"
            in protocol
        )
        assert (
            "Individual entries and an\nentry-wise ``orbital hopping'' interpretation "
            "are gauge dependent" in protocol
        )
        assert r"H_{\mathrm{T}}=H_{\mathrm{W}}" in protocol
        assert (
            "216-point C6 construction mesh establishes\nsource reconstruction"
            in protocol
        )
        assert "408-point geometry is the development evaluation\ninventory" in protocol
        assert "402-point geometry is confirmation-only" in protocol
        assert "108/108 construction-grid split remains reserved" in protocol
        assert "Do not scalarize channels" in protocol
        assert "selected numerical policy uses exact integer support cost" in protocol
        assert (
            "positive interval overlaps remain unresolved and incomparable" in protocol
        )
        assert "fixed-gauge finite enumeration" in protocol
        assert "reimplement Wannier90" in protocol
        assert "authorizes no calculator invocation, analysis execution" in protocol

        for superseded_claim in (
            "operational diagnostics predict those labels",
            "diagnostic-to-hidden-error prediction",
            "predicted the hidden parent discrepancies",
            "development-oracle calibration",
            "predicted hidden errors",
        ):
            assert superseded_claim not in protocol

    def test_pareto_contract_binds_evidence_and_versioned_executions(
        self,
        repository_root: Path,
    ) -> None:
        bulk = repository_root / "calculations" / "Si" / "bulk"
        contract_root = bulk / "analysis" / "c6-b20-w21-hopping-pareto-synthesis"
        contract = (contract_root / "README.md").read_text(encoding="utf-8")
        bound_inputs = (
            (
                "analysis/c6-b20-w21-untruncated-characterization/"
                "characterization-result.json",
                "37f654ae31bc21e43b768bf2b9da5edabd88c195e3f6e1c87708eaa1c4773c18",
            ),
            (
                "analysis/c6-b20-w21-spatial-truncation-design/truncation-design.json",
                "6b9863271ba8241881d62435a7c8307d3431ffe59bfdcce5d96525fe86fcb531",
            ),
            (
                "analysis/c6-b20-w21-spatial-truncation-evaluation/"
                "truncation-evaluation.json",
                "1ac8bb59137e8dc7217df52f89c18a84e8599bcf82ec59f40a361929d4322a52",
            ),
            (
                "analysis/c6-b20-w21-spatial-truncation-disposition/"
                "spatial-truncation-disposition.json",
                "519adfcf1101f7caa7916e04f3bf37879f4ad82b0f30e4ef38adc39770224f68",
            ),
            (
                "analysis/construction-mesh-adequacy-recommendation/"
                "construction-mesh-candidates.json",
                "1e5ebb9dffa6a97a2f2445cfd6290aff4cd3d6c06c15e4e0e7d6bbde7826c803",
            ),
            (
                "analysis/withheld-parent-validation-preflight/"
                "withheld-kpoint-manifest.json",
                "754bce5030ef0e34eb092406b27d9094287b4f749e358ef36404040f44b8d2b4",
            ),
            (
                "analysis/c6-b20-w21-revealed-408-development/development-result.json",
                "bb1a6d0fab5d08fecaa0d86cbfe00e8670e7f089e289c6fabc59c32c6f76991d",
            ),
            (
                "analysis/construction-mesh-adequacy-recommendation/"
                "successor-confirmation-holdout.json",
                "51427c7389ae293566d865d42a3a8a8217b0fed4607ac65c5a97199ce6a383c8",
            ),
        )

        assert {path.name for path in contract_root.iterdir()} == {
            "README.md",
            "executions",
            "replaceable",
            "run_analysis.py",
        }
        action = contract_root / "run_analysis.py"
        assert hashlib.sha256(action.read_bytes()).hexdigest() == (
            "76321e9fa38b789dadd4d6b771ac57283deadf95e0c3249569af05287ad76a86"
        )
        assert "V2 LATEST EXECUTION; FORMATTING-ONLY V3 LIVE AND UNEXECUTED" in contract
        for relative_path, expected_hash in bound_inputs:
            assert (
                hashlib.sha256((bulk / relative_path).read_bytes()).hexdigest()
                == expected_hash
            )
            assert expected_hash in contract

        assert "18 nested complete physical-radius shells" in contract
        assert "383 effective\nWS representatives" in contract
        assert "C6 construction mesh has 216 points" in contract
        assert "408-point geometry is the development evaluation inventory" in contract
        assert "402-point geometry is confirmation-only" in contract
        assert "108/108 construction-grid split remains reserved" in contract
        assert "Do not scalarize\nchannels" in contract
        assert "Tail Frobenius norms" in contract
        assert (
            "selected policy is **conservative interval Pareto dominance**" in contract
        )
        assert "UNRESOLVED_INTERVAL_OVERLAP" in contract
        assert "does not invent intervals from point estimates" in contract
        assert "UNRESOLVED_DEVELOPMENT_EVALUATION" in contract
        assert "INAPPLICABLE_OBSERVABLE_IDENTITY" in contract
        assert "`H_T = H_W`" in contract
        assert "no newly accepted support" in contract
        assert "do **not** contain the required per-shell\ninterval metrics" in contract
        assert "runs invoked no Quantum ESPRESSO or Wannier90" in contract
        assert "402-point parent calculation" in contract

        result_path = (
            contract_root / "replaceable" / "hopping-pareto-synthesis-result.json"
        )
        assert hashlib.sha256(result_path.read_bytes()).hexdigest() == (
            "4dd7ae9842a2b33784f6c9ec19b0353e8959c8d25fa3682603f509852146ad3c"
        )
        result = cast(JsonValue, json.loads(result_path.read_text(encoding="utf-8")))
        assert isinstance(result, dict)
        assert result["disposition"] == "UNRESOLVED_DEVELOPMENT_EVALUATION"
        assert result["calculator_invocations"] == 0
        implementation = result["implementation"]
        assert isinstance(implementation, dict)
        retained_v1_producer = (
            contract_root / "executions" / "identity-gap-v1" / "producer-source.py.txt"
        )
        assert (
            implementation["sha256"]
            == hashlib.sha256(retained_v1_producer.read_bytes()).hexdigest()
        )
        assert implementation["sha256"] == (
            "d745b753d9d608cbcbf9dacb12b5a9159727d66ba97fc9c13840eb07d00962cf"
        )
        retained_v1_result = (
            contract_root
            / "executions"
            / "identity-gap-v1"
            / "hopping-pareto-synthesis-result.json"
        )
        assert retained_v1_result.read_bytes() == result_path.read_bytes()
        candidate_records = result["candidate_records"]
        assert isinstance(candidate_records, list)
        assert len(candidate_records) == 18
        assert result["confirmation_402_boundary"] == {
            "identity": "confirmation_402_geometry",
            "parent_values_consumed": False,
            "point_count": 402,
            "sha256": (
                "51427c7389ae293566d865d42a3a8a8217b0fed4607ac65c5a97199ce6a383c8"
            ),
        }

        v2_root = contract_root / "executions" / "identity-gap-v2"
        retained_v2_producer = v2_root / "producer-source.py.txt"
        retained_v2_result = v2_root / "hopping-pareto-synthesis-result.json"
        assert hashlib.sha256(retained_v2_producer.read_bytes()).hexdigest() == (
            "c156d413ef11cc37aae5b93f2f239b9d23344d8f6ad194f2bef781188065aeb1"
        )
        assert retained_v2_producer.read_bytes() != action.read_bytes()
        assert not (contract_root / "executions" / "identity-gap-v3").exists()
        assert "No v3 result, manifest, execution identity" in contract
        assert hashlib.sha256(retained_v2_result.read_bytes()).hexdigest() == (
            "1af973546b6e1a9687a51433b0ba61227b9f2d13b711d89e789a3ba7c29e6b50"
        )
        v2_result = cast(
            JsonValue,
            json.loads(retained_v2_result.read_text(encoding="utf-8")),
        )
        assert isinstance(v2_result, dict)
        assert v2_result["disposition"] == "UNRESOLVED_DEVELOPMENT_EVALUATION"
        v2_implementation = v2_result["implementation"]
        assert isinstance(v2_implementation, dict)
        assert v2_implementation == {
            "path": (
                "calculations/Si/bulk/analysis/"
                "c6-b20-w21-hopping-pareto-synthesis/run_analysis.py"
            ),
            "sha256": (
                "c156d413ef11cc37aae5b93f2f239b9d23344d8f6ad194f2bef781188065aeb1"
            ),
        }
        normalized_v1 = dict(result)
        normalized_v2 = dict(v2_result)
        normalized_v1["implementation"] = None
        normalized_v2["implementation"] = None
        assert normalized_v1 == normalized_v2

        for execution_id, expected_disposition, expected_manifest_hash in (
            (
                "identity-gap-v1",
                "UNRESOLVED_DEVELOPMENT_EVALUATION",
                "49d723bbcbe45ecbdf1d3a9bc39fbfcc04884e271dea074acaf894e0b0791076",
            ),
            (
                "identity-gap-v2",
                "UNRESOLVED_DEVELOPMENT_EVALUATION",
                "84b3170a59f24d730f8f5a41d37042c820917b711471f1b92c19be831b243284",
            ),
        ):
            manifest_path = (
                contract_root / "executions" / execution_id / "manifest.json"
            )
            assert hashlib.sha256(manifest_path.read_bytes()).hexdigest() == (
                expected_manifest_hash
            )
            manifest = cast(
                JsonValue,
                json.loads(manifest_path.read_text(encoding="utf-8")),
            )
            assert isinstance(manifest, dict)
            assert manifest["execution_identity"] == execution_id
            assert manifest["disposition"] == expected_disposition

    @staticmethod
    def _artificial_bundle(
        tmp_path: Path,
    ) -> tuple[Path, Path, Path, dict[str, JsonValue]]:
        objective_ids = (
            "operator.maximum_spectral_ev",
            "operator.weighted_rms_frobenius_ev",
            "ordered_spectrum.maximum_absolute_ev",
            "ordered_spectrum.weighted_rms_ev",
            "gap.absolute_change_ev",
            "valley.maximum_displacement_inverse_angstrom",
            "valley.maximum_energy_change_ev",
            "curvature.maximum_primary_absolute_relative_change",
            "mass.maximum_primary_absolute_relative_change",
            "mass.maximum_stencil_relative_spread",
        )
        support_costs = (
            1,
            13,
            19,
            43,
            55,
            79,
            87,
            135,
            141,
            177,
            201,
            225,
            249,
            313,
            353,
            365,
            371,
            383,
        )
        operator_intervals = (
            (4.0, 5.0),
            (5.0, 6.0),
            (4.5, 6.5),
            (1.0, 2.0),
        )
        candidates: list[JsonValue] = []
        for index, cost in enumerate(support_costs):
            lower, upper = (
                operator_intervals[index]
                if index < len(operator_intervals)
                else (8.0 + index, 9.0 + index)
            )
            objectives: dict[str, JsonValue] = {
                objective_id: {
                    "disposition": "INTERVAL",
                    "lower": lower,
                    "upper": upper,
                }
                for objective_id in objective_ids
            }
            if index == 0:
                objectives["gap.absolute_change_ev"] = {
                    "disposition": "UNRESOLVED_CHANNEL_METRIC",
                    "reason": "artificial missing metric",
                }
                objectives["valley.maximum_displacement_inverse_angstrom"] = {
                    "disposition": "INAPPLICABLE_OBSERVABLE_IDENTITY",
                    "reason": "artificial identity failure",
                }
            candidates.append(
                {
                    "shell_id": f"H-shell-{index:02d}",
                    "support_cost": cost,
                    "objectives": objectives,
                }
            )

        producer = tmp_path / "artificial-producer.py"
        producer.write_text("# artificial software-test producer\n", encoding="utf-8")
        policy = tmp_path / "artificial-interval-policy.md"
        policy.write_text(
            "artificial closed intervals for software tests\n", encoding="utf-8"
        )
        bundle: dict[str, JsonValue] = {
            "evaluation_inventory_sha256": "synthetic-inventory",
            "producer": {
                "identity": "artificial-software-test-producer",
                "sha256": hashlib.sha256(producer.read_bytes()).hexdigest(),
            },
            "interval_policy": {
                "identity": "artificial-software-test-policy",
                "sha256": hashlib.sha256(policy.read_bytes()).hexdigest(),
            },
            "source_bindings": [],
            "candidates": candidates,
        }
        bundle_path = tmp_path / "artificial-metrics.json"
        bundle_path.write_text(json.dumps(bundle), encoding="utf-8")
        return bundle_path, producer, policy, bundle

    @staticmethod
    def _run_artificial_action(
        action: Path,
        bundle: Path,
        producer: Path,
        policy: Path,
        output: Path,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(action),
                "--software-test-input",
                str(bundle),
                "--metrics-producer",
                str(producer),
                "--interval-policy",
                str(policy),
                "--output",
                str(output),
            ],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_action_classifies_artificial_intervals_without_silicon_inputs(
        self,
        repository_root: Path,
        tmp_path: Path,
    ) -> None:
        action = (
            repository_root
            / "calculations"
            / "Si"
            / "bulk"
            / "analysis"
            / "c6-b20-w21-hopping-pareto-synthesis"
            / "run_analysis.py"
        )
        bundle, producer, policy, _ = self._artificial_bundle(tmp_path)
        output = tmp_path / "artificial-result.json"

        completed = self._run_artificial_action(
            action, bundle, producer, policy, output
        )
        assert completed.returncode == 0, completed.stderr
        result = cast(JsonValue, json.loads(output.read_text(encoding="utf-8")))
        assert isinstance(result, dict)
        assert result["disposition"] == "SYNTHETIC_SOFTWARE_TEST_ONLY"
        assert result["calculator_invocations"] == 0
        assert result["confirmation_402_parent_values_consumed"] is False
        assert result["slater_koster_108_108_split_consumed"] is False
        implementation = result["implementation"]
        assert isinstance(implementation, dict)
        assert (
            implementation["sha256"] == hashlib.sha256(action.read_bytes()).hexdigest()
        )
        assert implementation["path"] == (
            "calculations/Si/bulk/analysis/"
            "c6-b20-w21-hopping-pareto-synthesis/run_analysis.py"
        )
        frontiers = result["frontiers"]
        assert isinstance(frontiers, dict)
        operator_frontier = frontiers["operator.maximum_spectral_ev"]
        assert isinstance(operator_frontier, list)
        dispositions: dict[str, str] = {}
        for raw_membership in operator_frontier[:4]:
            assert isinstance(raw_membership, dict)
            membership_shell_id = raw_membership["shell_id"]
            membership_disposition = raw_membership["disposition"]
            assert isinstance(membership_shell_id, str)
            assert isinstance(membership_disposition, str)
            dispositions[membership_shell_id] = membership_disposition
        assert dispositions == {
            "H-shell-00": "NONDOMINATED",
            "H-shell-01": "DOMINATED",
            "H-shell-02": "UNRESOLVED_INTERVAL_OVERLAP",
            "H-shell-03": "NONDOMINATED",
        }
        gap_frontier = frontiers["gap.absolute_change_ev"]
        valley_frontier = frontiers["valley.maximum_displacement_inverse_angstrom"]
        assert isinstance(gap_frontier, list)
        assert isinstance(valley_frontier, list)
        assert isinstance(gap_frontier[0], dict)
        assert isinstance(valley_frontier[0], dict)
        assert gap_frontier[0]["disposition"] == "UNRESOLVED_CHANNEL_METRIC"
        assert valley_frontier[0]["disposition"] == "INAPPLICABLE_OBSERVABLE_IDENTITY"

        repeated = self._run_artificial_action(action, bundle, producer, policy, output)
        assert repeated.returncode != 0
        assert "refusing to overwrite existing output" in repeated.stderr

    def test_action_rejects_invalid_artificial_bundle_contracts(
        self,
        repository_root: Path,
        tmp_path: Path,
    ) -> None:
        action = (
            repository_root
            / "calculations"
            / "Si"
            / "bulk"
            / "analysis"
            / "c6-b20-w21-hopping-pareto-synthesis"
            / "run_analysis.py"
        )
        bundle_path, producer, policy, original = self._artificial_bundle(tmp_path)
        candidates = original["candidates"]
        assert isinstance(candidates, list)

        invalid_cases: list[tuple[str, dict[str, JsonValue], str]] = []
        reversed_bundle = dict(original)
        reversed_bundle["candidates"] = list(reversed(candidates))
        invalid_cases.append(
            (
                "reversed",
                reversed_bundle,
                "candidate order must be exactly H-shell-00 through H-shell-17",
            )
        )

        noninteger_bundle = cast(dict[str, JsonValue], json.loads(json.dumps(original)))
        noninteger_candidates = noninteger_bundle["candidates"]
        assert isinstance(noninteger_candidates, list)
        first_candidate = noninteger_candidates[0]
        assert isinstance(first_candidate, dict)
        first_candidate["support_cost"] = 1.0
        invalid_cases.append(
            (
                "noninteger",
                noninteger_bundle,
                "support_cost must have exact type int",
            )
        )

        missing_policy_bundle = dict(original)
        del missing_policy_bundle["interval_policy"]
        invalid_cases.append(
            (
                "missing-policy",
                missing_policy_bundle,
                "metrics.interval_policy must be a JSON object",
            )
        )

        for name, bundle_value, expected_error in invalid_cases:
            case_path = tmp_path / f"{name}.json"
            case_path.write_text(json.dumps(bundle_value), encoding="utf-8")
            output = tmp_path / f"{name}-result.json"
            completed = self._run_artificial_action(
                action, case_path, producer, policy, output
            )
            assert completed.returncode != 0
            assert expected_error in completed.stderr
            assert not output.exists()

        assert bundle_path.exists()

    def test_calculation_documents_point_to_hopping_first_authority(
        self,
        repository_root: Path,
    ) -> None:
        bulk = repository_root / "calculations" / "Si" / "bulk"
        documents = (
            bulk / "development-plan.md",
            bulk / "evidence-crosswalk.md",
            bulk / "analysis" / "README.md",
            bulk / "simulations" / "README.md",
            bulk / "analysis" / "c6-b20-w21-slater-koster-definition-fit" / "README.md",
        )

        for document in documents:
            assert (
                "controlled-reduction-protocol-hopping-first.tex"
                in document.read_text(encoding="utf-8")
            )

        for document in (
            bulk / "development-plan.md",
            bulk / "evidence-crosswalk.md",
            bulk / "analysis" / "README.md",
            bulk / "research-protocol" / "README.md",
        ):
            assert "c6-b20-w21-hopping-pareto-synthesis" in document.read_text(
                encoding="utf-8"
            )

        retained_series = (
            bulk / "simulations" / "preflight" / "c6-b20-w21-gated-series" / "README.md"
        ).read_text(encoding="utf-8")
        assert "series-plan.json` retain the historical stage graph" in retained_series
        assert "controlled-reduction-protocol-post-s110.tex" in retained_series
        assert "controlled-reduction-protocol-hopping-first.tex" in retained_series
        assert "do not relabel a completed S stage or activate S50" in retained_series
