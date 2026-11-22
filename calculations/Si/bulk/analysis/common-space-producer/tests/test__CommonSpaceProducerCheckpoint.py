"""Retained producer-byte contracts, not independent numerical verification."""

import hashlib
import json
from pathlib import Path

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
ROOT = Path(__file__).resolve().parents[1] / "run-001"


class TestCommonSpaceProducerCheckpoint:
    """Keep complete producer delivery distinct from independent verification."""

    @staticmethod
    def record(name: str) -> dict[str, JsonValue]:
        value: JsonValue = json.loads((ROOT / name).read_bytes())
        assert type(value) is dict
        return value

    @staticmethod
    def rows(value: JsonValue) -> list[dict[str, JsonValue]]:
        assert type(value) is list
        result: list[dict[str, JsonValue]] = []
        for item in value:
            assert type(item) is dict
            result.append(item)
        return result

    def test__saved_bytes__match_frozen_result_and_actual_completion(self) -> None:
        assert (
            hashlib.sha256((ROOT / "result.json").read_bytes()).hexdigest()
            == "761d58b83a43a9544ad2aae1872ef91cd4ef5387dbae9a6db169a32ee5498dd8"
        )
        assert (
            hashlib.sha256((ROOT / "point-inventory.json").read_bytes()).hexdigest()
            == "fd23080496ee077e967631a1cf4258301f4efc41d045557a03365d8bcaed19c7"
        )
        assert (
            hashlib.sha256((ROOT / "producer-completion.json").read_bytes()).hexdigest()
            == "0d03312dea85e6881fa432ee15f402ab9d0011e9312bfff749dcf2dc9d28c452"
        )
        receipt = self.record("producer-completion.json")
        assert receipt["full_grid_reconstruction_complete"] is True
        assert receipt["symmetry_inventory_complete"] is True
        assert (
            receipt["state_assertions_sha256"]
            == "c01997f800728dfb7ac1925e8719af22033d4437949c72a3294850dd87a3add3"
        )
        for row in self.rows(receipt["completed_evidence"]):
            identity = row["identity"]
            assert type(identity) is dict
            name = identity["name"]
            assert type(name) is str
            payload = (ROOT / name).read_bytes()
            assert len(payload) == identity["byte_count"]
            assert hashlib.sha256(payload).hexdigest() == identity["sha256"]

    def test__field__retains_every_point_at_the_unchanged_raw_threshold(self) -> None:
        result = self.record("result.json")
        csd1 = result["CSD1"]
        assert type(csd1) is dict
        rows = self.rows(csd1["complete_kpoint_diagnostics"])
        assert len(rows) == 216
        assert [row["ordered_kpoint_index_zero_based"] for row in rows] == list(
            range(216)
        )
        assert [row["resolved_rank_at_native_bound"] for row in rows] == [
            9 if i in (0, 12) else 10 for i in range(216)
        ]
        assert csd1["singular_value_native_uncertainty_bound"] == 5.890206739032098e-7
        assert csd1["unimplemented_CSD1_extensions"] == []
        assert (
            result["scientific_disposition"]
            == "blocked-orbital-alignment-rank-deficient-no-fit"
        )

    def test__stars__retain_actual_member_rows_without_rank_invariance(self) -> None:
        inventory = self.record("point-inventory.json")
        result = self.record("result.json")
        csd1 = result["CSD1"]
        assert type(csd1) is dict
        rows = self.rows(csd1["complete_kpoint_diagnostics"])
        assert inventory["operation_count"] == 48
        stars = self.rows(inventory["deficient_point_stars"])
        assert [row["deficient_seed_index"] for row in stars] == [0, 12]
        assert stars[1]["related_indices"] == [2, 4, 12, 24, 72, 86, 144, 172]
        assert stars[1]["deficient_member_indices"] == [12]
        assert stars[1]["point_diagnostics"] == [
            rows[i] for i in (2, 4, 12, 24, 72, 86, 144, 172)
        ]
        assert "not electronic symmetry representations" in str(inventory["scope"])
        assert "Nonzero coordinate residuals are not waived" in str(
            inventory["interpretation"]
        )

    def test__continuation__does_not_claim_independent_verification_or_a_fit(
        self,
    ) -> None:
        result = self.record("result.json")
        independent = result["independent_verification"]
        csd2 = result["CSD2"]
        csd3 = result["CSD3"]
        assert type(independent) is dict and independent["outcome"] == "not-run"
        assert type(csd2) is dict and csd2["outcome"] == "not-run"
        assert type(csd3) is dict and csd3["authorization_inferred"] is False
        assert result["calculator_invocations"] == result["fit_invocations"] == 0
