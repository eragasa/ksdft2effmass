"""Saved numerical-certificate contracts, not another rank reconstruction."""

import hashlib
import json
from fractions import Fraction
from pathlib import Path

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
ROOT = Path(__file__).resolve().parents[1]


class TestRetainedCommonSpaceVerification:
    """Preserve the first attempt and bind the successful post-computation result."""

    @staticmethod
    def record(path: Path) -> dict[str, JsonValue]:
        value: JsonValue = json.loads(path.read_bytes())
        assert type(value) is dict
        return value

    @staticmethod
    def rows(value: JsonValue) -> list[dict[str, JsonValue]]:
        assert type(value) is list
        result: list[dict[str, JsonValue]] = []
        for row in value:
            assert type(row) is dict
            result.append(row)
        return result

    @staticmethod
    def rational(value: JsonValue) -> Fraction:
        assert type(value) is list and len(value) == 2
        top, bottom = value
        assert type(top) is str and type(bottom) is str
        return Fraction(int(top, 16), int(bottom, 16))

    def test__saved_certificate__covers_all_points_with_decisive_controls(self) -> None:
        data = self.record(ROOT / "run-002/independent-verification.json")
        assert data["outcome"] == "independent-result-complete-pending-comparison"
        assert data["deficient_indices"] == [0, 12]
        state = data["source_assertions"]
        assert type(state) is dict
        assert self.rational(state["frozen_rank_threshold"]) == Fraction.from_float(
            5.890206739032098e-7
        )
        rows = self.rows(data["points"])
        assert len(rows) == 216
        assert [row["ordered_index"] for row in rows] == list(range(216))
        assert [row["resolved_rank"] for row in rows] == [
            9 if i in (0, 12) else 10 for i in range(216)
        ]
        assert [row["fractional_kpoint"] for row in rows] == state[
            "ordered_fractional_kpoints"
        ]
        for row in rows:
            assert row["arithmetic_failure"] is None
            assert row["uncertainty_bound_covered"] is True
            assert row["unitary_invariance_passed"] is True
            assert self.rational(row["hermiticity_defect_bound"]) == 0
            assert (
                row["arithmetic_rank_lower_bound"]
                == row["arithmetic_rank_upper_bound"]
                == row["resolved_rank"]
            )
        for index in (0, 12):
            assert rows[index]["direction_outcome"] == "isolated-direction-enclosed"
            assert len(self.rows(data["source_ledger"])) == 9

    def test__post_comparison__binds_saved_result_manifest_and_actual_producer(
        self,
    ) -> None:
        root = ROOT / "run-002"
        data = self.record(root / "producer-correlation.json")
        assert data["outcome"] == "rank-diagnosis-correlated-under-declared-contract"
        assert data["mismatches"] == []
        for key, name in (
            ("independent_result", "independent-verification.json"),
            ("independent_manifest", "manifest.json"),
        ):
            identity = data[key]
            assert type(identity) is dict
            payload = (root / name).read_bytes()
            assert len(payload) == identity["byte_count"]
            assert hashlib.sha256(payload).hexdigest() == identity["sha256"]
        producer = data["producer_result"]
        assert type(producer) is dict
        assert (
            producer["sha256"]
            == "761d58b83a43a9544ad2aae1872ef91cd4ef5387dbae9a6db169a32ee5498dd8"
        )
        assert (
            hashlib.sha256(
                (root / "producer-correlation.json").read_bytes()
            ).hexdigest()
            == "c1979a548d41ddb3de81e398d5317972029d47fab1c6d30dae1d2405295b5d72"
        )

    def test__initial_attempt__is_preserved_not_silently_promoted(self) -> None:
        first = ROOT / "run-001"
        assert not (first / "producer-correlation.json").exists()
        assert (
            hashlib.sha256((first / "manifest.json").read_bytes()).hexdigest()
            == "c1e3900a531e53c275938448bd4c5db29e864f8a00060edd38056f9c882e1f93"
        )
        assert "request state space differs" in (first / "execution.log").read_text()
        manifest = self.record(first / "manifest.json")
        old = next(
            row
            for row in self.rows(manifest["implementation"])
            if row["name"] == "producer_result.py"
        )
        assert (
            hashlib.sha256(
                (first / "comparison-adapter-before.py.txt").read_bytes()
            ).hexdigest()
            == old["sha256"]
        )
        assert (first / "independent-verification.json").read_bytes() == (
            ROOT / "run-002/independent-verification.json"
        ).read_bytes()
        assert (
            hashlib.sha256(
                (first / "independent-verification.json").read_bytes()
            ).hexdigest()
            == "3ed6f7bb54086ac8005acea8c34a9a47c475b14878618da4b5c6eaa01ac532ee"
        )

    def test__as_run_implementation__matches_successful_manifest(self) -> None:
        source = ROOT.parents[1] / "common_space/verification"
        manifest = self.record(ROOT / "run-002/manifest.json")
        for row in self.rows(manifest["implementation"]):
            name = row["name"]
            assert type(name) is str
            payload = (source / name).read_bytes()
            assert len(payload) == row["byte_count"]
            assert hashlib.sha256(payload).hexdigest() == row["sha256"]
        assert (
            hashlib.sha256((ROOT / "run_verification.py").read_bytes()).hexdigest()
            == "af0e7d9d44ce4360b0f33ea84ea567cd52b76a48e31a4aefc704b9f41118b05e"
        )
