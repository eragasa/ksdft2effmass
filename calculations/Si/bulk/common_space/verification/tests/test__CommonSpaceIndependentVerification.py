"""Complete synthetic C6 verifier checks; no retained source admission or execution."""

from __future__ import annotations

import hashlib
from dataclasses import replace
from fractions import Fraction
from itertools import product
from pathlib import Path

import common_space.verification.tests.test__CommonSpaceNativeOverlapReconstruction as native_fixture
import numpy as np
import pytest
from common_space.verification.controls import (
    CommonSpaceDeficientDirectionAnalysis,
    CommonSpaceDirectionOutcome,
    CommonSpaceUnitaryInvariance,
    CommonSpaceWeightInterval,
)
from common_space.verification.gram_rank import GramRankDisposition, GramRankFailure
from common_space.verification.grid_verification import (
    CommonSpaceIndependentGridResult,
    CommonSpaceIndependentVerification,
    CommonSpaceProducerCorrelation,
    CommonSpaceProducerPoint,
    CommonSpaceProducerReference,
    CommonSpaceVerificationOutcome,
)
from common_space.verification.native_inputs import CommonSpaceTrialConvention
from common_space.verification.native_overlap import (
    CommonSpaceNativeOverlapReconstruction,
)
from common_space.verification.native_precision import (
    CommonSpaceNativePrecisionAssessment,
    CommonSpaceNativeRoundingModel,
)
from common_space.verification.producer_result import CommonSpaceProducerResultAdapter
from common_space.verification.source_admission import (
    CommonSpaceEvidenceRole,
    CommonSpaceReviewScope,
    CommonSpaceSourceAdmission,
    CommonSpaceSourceEvidence,
    CommonSpaceVerificationJson,
)
from common_space.verification.verification_io import (
    CommonSpaceProducerCorrelationRun,
    CommonSpaceVerificationRun,
)
from ksdft2effmass.serialization.enums import StrWireEnum
from numpy.typing import NDArray
from projectkoios.integrations.wannier90 import Wannier90NativeArtifact

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestCommonSpaceIndependentVerification:
    """Exercise full-grid independence and fail-closed prerequisite handling."""

    @pytest.fixture(scope="class")
    @classmethod
    def source(cls) -> CommonSpaceSourceAdmission:
        points = tuple((x / 6, y / 6, z / 6) for x, y, z in product(range(6), repeat=3))
        loader, _ = native_fixture.TestCommonSpaceNativeOverlapReconstruction._fixture(
            points=points, bands=20, constant_target=True, deficient_indices=(0,)
        )
        # These are synthetic software-test declarations, NOT completed scientific work.
        evidence = tuple(
            CommonSpaceSourceEvidence(
                role=role,
                expected=(
                    artifact := Wannier90NativeArtifact(
                        f"{role.to_wire()}.json",
                        b"Synthetic fixture only; no retained scientific evidence.\n",
                    )
                ).identity,
                artifact=artifact,
            )
            for role in CommonSpaceEvidenceRole
        )
        admission = CommonSpaceSourceAdmission(
            parsed_inputs=loader.execute(),
            rounding_model=CommonSpaceNativeRoundingModel.from_nearest_decimal_places(
                amn=12, gauge=10, disentanglement=10
            ),
            frozen_rank_threshold=Fraction.from_float(5.890206739032098e-7),
            review_scope=CommonSpaceReviewScope.synthetic,
            review_reference="synthetic-fixture-not-scientific-review",
            parent_band_state_identity="synthetic-shared-parent-band-space",
            gauge_state_identity="synthetic-native-wannier-gauge",
            evidence=evidence,
        )
        assertion = Wannier90NativeArtifact(
            "reviewed-state-assertions.json", admission.assertion_payload()
        )
        completion = Wannier90NativeArtifact(
            "producer-completion-evidence.json",
            CommonSpaceVerificationJson.encode(
                {
                    "record_type": "common-space-producer-prerequisites-v1",
                    "state_assertions_sha256": assertion.identity.sha256,
                    "full_grid_reconstruction_complete": True,
                    "symmetry_inventory_complete": True,
                    "completed_evidence": [
                        {
                            "role": role.to_wire(),
                            "identity": CommonSpaceVerificationJson.identity(
                                next(
                                    item.expected
                                    for item in admission.evidence
                                    if item.role is role
                                )
                            ),
                        }
                        for role in admission.producer_prerequisite_roles
                    ],
                    "review_scope": CommonSpaceReviewScope.synthetic.to_wire(),
                }
            ),
        )
        completed_evidence: list[CommonSpaceSourceEvidence] = []
        replacements = {
            CommonSpaceEvidenceRole.state_assertions: assertion,
            CommonSpaceEvidenceRole.producer_completion: completion,
        }
        for item in admission.evidence:
            replacement = replacements.get(item.role)
            if replacement is not None:
                item = CommonSpaceSourceEvidence(
                    role=item.role,
                    expected=replacement.identity,
                    artifact=replacement,
                )
            completed_evidence.append(item)
        return replace(admission, evidence=tuple(completed_evidence))

    @pytest.fixture(scope="class")
    @classmethod
    def published(
        cls,
        source: CommonSpaceSourceAdmission,
        tmp_path_factory: pytest.TempPathFactory,
    ) -> tuple[CommonSpaceIndependentGridResult, Path]:
        root = tmp_path_factory.mktemp("synthetic-rank-verifier") / "independent"
        return CommonSpaceVerificationRun(
            admission=source, output_root=root
        ).execute(), root

    @pytest.fixture(scope="class")
    @classmethod
    def producer(
        cls, published: tuple[CommonSpaceIndependentGridResult, Path]
    ) -> CommonSpaceProducerReference:
        result, _ = published
        # An independent synthetic oracle, NOT values copied from verifier intervals.
        points: list[CommonSpaceProducerPoint] = []
        for index in range(216):
            matrix = np.eye(10, dtype=np.complex128)
            if index == 0:
                matrix[9, 9] = 0
            matrix[0, 1] = 0.25 + 0.5j
            matrix[3, 6] = -0.125j
            matrix[8, 2] = 0.375j
            values = np.linalg.svd(matrix, compute_uv=False)
            points.append(
                CommonSpaceProducerPoint(
                    ordered_index=index,
                    resolved_rank=9 if index == 0 else 10,
                    singular_values=(
                        Fraction.from_float(float(values[0])),
                        Fraction.from_float(float(values[-2])),
                        Fraction.from_float(float(values[-1])),
                    ),
                    atomic_weights=(Fraction(0),) * 9 + (Fraction(1),)
                    if index == 0
                    else (),
                    group_weights=(Fraction(0), Fraction(0), Fraction(1))
                    if index == 0
                    else (),
                )
            )
        assertion = next(
            value.expected
            for value in result.admission.evidence
            if value.role is CommonSpaceEvidenceRole.state_assertions
        )
        return CommonSpaceProducerReference(
            state_assertions_sha256=assertion.sha256,
            producer_result_identity=next(
                item.expected
                for item in result.admission.evidence
                if item.role is CommonSpaceEvidenceRole.producer_reconstruction
            ),
            native_identities=result.admission.parsed_inputs.contract.identities,
            frozen_rank_threshold=result.admission.frozen_rank_threshold,
            points=tuple(points),
        )

    def test_decisive_arithmetic__needs_no_higher_precision_artifact(
        self, source: CommonSpaceSourceAdmission
    ) -> None:
        source.authenticate()
        assert all("precision" not in item.role.to_wire() for item in source.evidence)
        completion = next(
            item.artifact
            for item in source.evidence
            if item.role is CommonSpaceEvidenceRole.producer_completion
        )
        payload = CommonSpaceVerificationJson.decode(completion.payload)
        assert type(payload) is dict
        assert "higher_precision_sensitivity_complete" not in payload

    def test_complete_grid__retains_every_point_without_consuming_producer(
        self, published: tuple[CommonSpaceIndependentGridResult, Path]
    ) -> None:
        result, root = published
        assert len(result.points) == 216
        assert result.deficient_indices == (0,)
        assert (
            result.outcome is CommonSpaceVerificationOutcome.independent_result_complete
        )
        assert all(point.unitary_invariance_passed for point in result.points)
        gamma = result.points[0].direction
        assert gamma.outcome is CommonSpaceDirectionOutcome.enclosed
        assert gamma.nominal_weights == (Fraction(0),) * 9 + (Fraction(1),)
        assert gamma.group_intervals[2].lower <= 1 <= gamma.group_intervals[2].upper
        assert all(
            point.direction.outcome is CommonSpaceDirectionOutcome.full_rank
            for point in result.points[1:]
        )
        payload = (root / "independent-verification.json").read_bytes()
        data = CommonSpaceVerificationJson.decode(payload)
        assert type(data) is dict
        assert data["review_scope"] == "synthetic-development-only"
        assert set(data) == {
            "record_type",
            "review_scope",
            "review_reference",
            "outcome",
            "source_assertions",
            "provider_version",
            "provider_modules",
            "source_ledger",
            "points",
            "deficient_indices",
        }
        assert str(root) not in payload.decode()
        manifest = CommonSpaceVerificationJson.decode(
            (root / "manifest.json").read_bytes()
        )
        assert type(manifest) is dict
        identity = manifest["result"]
        assert type(identity) is dict
        assert identity["sha256"] == hashlib.sha256(payload).hexdigest()
        assert identity["byte_count"] == len(payload)

    def test_correlation__runs_only_on_finished_independent_result(
        self,
        published: tuple[CommonSpaceIndependentGridResult, Path],
        producer: CommonSpaceProducerReference,
    ) -> None:
        result, root = published
        before = (root / "independent-verification.json").read_bytes()
        assert (
            CommonSpaceProducerCorrelation(
                independent=result, producer=producer
            ).execute()
            == ()
        )
        assert (root / "independent-verification.json").read_bytes() == before

    def test_producer_mismatch__cannot_change_independent_rank_or_weights(
        self,
        published: tuple[CommonSpaceIndependentGridResult, Path],
        producer: CommonSpaceProducerReference,
    ) -> None:
        result, _ = published
        incorrect = replace(
            producer.points[0], atomic_weights=(Fraction(1),) + (Fraction(0),) * 9
        )
        changed = replace(producer, points=(incorrect, *producer.points[1:]))
        mismatch = CommonSpaceProducerCorrelation(
            independent=result, producer=changed
        ).execute()
        assert any("weights differ" in value for value in mismatch)
        assert result.points[0].assessment.resolved_rank == 9
        assert result.points[0].direction.nominal_weights[-1] == 1

    @pytest.mark.parametrize("change", ("rank", "spectrum"))
    def test_producer_rank_or_spectrum_mismatch__is_reported(
        self,
        published: tuple[CommonSpaceIndependentGridResult, Path],
        producer: CommonSpaceProducerReference,
        change: str,
    ) -> None:
        point = producer.points[0]
        if change == "rank":
            point = replace(
                point, resolved_rank=10, atomic_weights=(), group_weights=()
            )
            expected = "resolved rank differs"
        else:
            point = replace(
                point, singular_values=(Fraction(99), *point.singular_values[1:])
            )
            expected = "singular value differs"
        mismatches = CommonSpaceProducerCorrelation(
            independent=published[0],
            producer=replace(producer, points=(point, *producer.points[1:])),
        ).execute()
        assert any(expected in value for value in mismatches)

    def test_original_producer_identity__must_match_reviewed_reconstruction(
        self,
        published: tuple[CommonSpaceIndependentGridResult, Path],
        producer: CommonSpaceProducerReference,
    ) -> None:
        with pytest.raises(ValueError, match="identities differ"):
            CommonSpaceProducerCorrelation(
                independent=published[0],
                producer=replace(
                    producer,
                    producer_result_identity=replace(
                        producer.producer_result_identity, sha256="0" * 64
                    ),
                ),
            ).execute()

    def test_source_mismatch__is_not_numerical_comparison_failure(
        self,
        published: tuple[CommonSpaceIndependentGridResult, Path],
        producer: CommonSpaceProducerReference,
    ) -> None:
        with pytest.raises(ValueError, match="identities differ"):
            CommonSpaceProducerCorrelation(
                independent=published[0],
                producer=replace(producer, state_assertions_sha256="0" * 64),
            ).execute()

    def test_missing_producer_prerequisite__stops_before_reconstruction(
        self, source: CommonSpaceSourceAdmission, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        items: list[CommonSpaceSourceEvidence] = []
        for item in source.evidence:
            if item.role is CommonSpaceEvidenceRole.producer_completion:
                payload = CommonSpaceVerificationJson.decode(item.artifact.payload)
                assert type(payload) is dict
                payload["full_grid_reconstruction_complete"] = False
                artifact = Wannier90NativeArtifact(
                    item.artifact.name, CommonSpaceVerificationJson.encode(payload)
                )
                item = replace(item, expected=artifact.identity, artifact=artifact)
            items.append(item)

        def forbidden(_self: CommonSpaceNativeOverlapReconstruction) -> None:
            raise AssertionError("no reconstruction before source prerequisites")

        monkeypatch.setattr(
            CommonSpaceNativeOverlapReconstruction, "execute", forbidden
        )
        with pytest.raises(ValueError, match="producer prerequisite"):
            CommonSpaceIndependentVerification(
                admission=replace(source, evidence=tuple(items))
            ).execute()

    def test_tampered_prerequisite_bytes__stop_before_reconstruction(
        self, source: CommonSpaceSourceAdmission, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        def forbidden(_self: CommonSpaceNativeOverlapReconstruction) -> None:
            raise AssertionError("source byte failure must precede reconstruction")

        monkeypatch.setattr(
            CommonSpaceNativeOverlapReconstruction, "execute", forbidden
        )
        evidence = tuple(
            replace(item, artifact=replace(item.artifact, payload=b"tampered"))
            if item.role is CommonSpaceEvidenceRole.symmetry_inventory
            else item
            for item in source.evidence
        )
        with pytest.raises(ValueError, match="identities do not agree"):
            CommonSpaceIndependentVerification(
                admission=replace(source, evidence=evidence)
            ).execute()

    def test_non_cartesian_point_inventory__cannot_be_admitted(
        self, source: CommonSpaceSourceAdmission
    ) -> None:
        loader, _ = native_fixture.TestCommonSpaceNativeOverlapReconstruction._fixture(
            points=tuple((index / 216, 0.0, 0.0) for index in range(216)), bands=20
        )
        with pytest.raises(ValueError, match="six-by-six-by-six"):
            replace(source, parsed_inputs=loader.execute())

    def test_tampered_semantics__does_not_pass_on_matching_byte_counts(
        self, source: CommonSpaceSourceAdmission
    ) -> None:
        with pytest.raises(ValueError, match="assertions do not match"):
            replace(source, gauge_state_identity="different-gauge").authenticate()
        with pytest.raises(ValueError, match="inventory"):
            replace(source, evidence=source.evidence[:-1])

    def test_existing_output__is_rejected_before_admission(
        self,
        source: CommonSpaceSourceAdmission,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        def forbidden(_self: CommonSpaceSourceAdmission) -> None:
            raise AssertionError("admission must not run for an existing output")

        monkeypatch.setattr(CommonSpaceSourceAdmission, "authenticate", forbidden)
        with pytest.raises(FileExistsError, match="must not exist"):
            CommonSpaceVerificationRun(admission=source, output_root=tmp_path).execute()
        dangling = tmp_path / "dangling"
        dangling.symlink_to(tmp_path / "absent")
        with pytest.raises(FileExistsError, match="must not exist"):
            CommonSpaceVerificationRun(admission=source, output_root=dangling).execute()

    @pytest.mark.parametrize(
        "enum_type",
        (
            GramRankDisposition,
            GramRankFailure,
            CommonSpaceTrialConvention,
            CommonSpaceDirectionOutcome,
            CommonSpaceVerificationOutcome,
            CommonSpaceReviewScope,
            CommonSpaceEvidenceRole,
        ),
    )
    def test_enumeration_members__use_lowercase_names_without_aliases(
        self, enum_type: type[StrWireEnum]
    ) -> None:
        assert len(enum_type.__members__) == len(tuple(enum_type))
        for member in enum_type:
            assert member.name == member.name.lower()
            assert enum_type.from_wire(member.to_wire()) is member

    def test_exact_wire__avoids_float_and_decimal_digit_limits(self) -> None:
        value = Fraction(1, 2**30000)
        encoded = CommonSpaceVerificationJson.rational(value)
        assert CommonSpaceVerificationJson.read_rational(encoded) == value
        assert CommonSpaceVerificationJson.encode(encoded)
        with pytest.raises(ValueError, match="canonical"):
            CommonSpaceVerificationJson.read_rational(["0x2", "0x4"])
        with pytest.raises(ValueError, match="duplicate"):
            CommonSpaceVerificationJson.decode(b'{"value":1,"value":2}')

    @pytest.mark.parametrize(
        "payload", (b'{"value":1e999}', b'{"value":NaN}', b'{"value":Infinity}')
    )
    def test_nonfinite_json__cannot_enter_reviewed_assertions(
        self, payload: bytes
    ) -> None:
        with pytest.raises(ValueError, match="nonfinite"):
            CommonSpaceVerificationJson.decode(payload)

    @pytest.mark.parametrize(
        "case", ("missing_manifest", "tampered_manifest", "tampered_result")
    )
    def test_incomplete_or_tampered_output__stops_before_reference_decoding(
        self,
        published: tuple[CommonSpaceIndependentGridResult, Path],
        producer: CommonSpaceProducerReference,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        case: str,
    ) -> None:
        result, root = published
        content = (root / "independent-verification.json").read_bytes()
        (tmp_path / "independent-verification.json").write_bytes(
            b"tampered" if case == "tampered_result" else content
        )
        if case != "missing_manifest":
            manifest = CommonSpaceVerificationJson.decode(
                (root / "manifest.json").read_bytes()
            )
            assert type(manifest) is dict
            if case == "tampered_manifest":
                manifest["result"] = None
            (tmp_path / "manifest.json").write_bytes(
                CommonSpaceVerificationJson.encode(manifest)
            )

        def forbidden(
            _self: CommonSpaceProducerResultAdapter,
        ) -> CommonSpaceProducerReference:
            raise AssertionError("output failure must precede reference decoding")

        monkeypatch.setattr(CommonSpaceProducerResultAdapter, "execute", forbidden)
        error: type[Exception] = (
            FileNotFoundError if case == "missing_manifest" else ValueError
        )
        with pytest.raises(error):
            CommonSpaceProducerCorrelationRun(
                independent=result,
                output_root=tmp_path,
            ).execute()
        assert not (tmp_path / "producer-correlation.json").exists()

    def test_eigensolver_failure__retains_complete_inconclusive_grid(
        self,
        source: CommonSpaceSourceAdmission,
        producer: CommonSpaceProducerReference,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
    ) -> None:
        def unavailable(
            matrix: NDArray[np.complex128],
        ) -> tuple[NDArray[np.float64], NDArray[np.complex128]]:
            raise np.linalg.LinAlgError("synthetic eigensolver unavailability")

        monkeypatch.setattr(np.linalg, "eigh", unavailable)
        result = CommonSpaceVerificationRun(
            admission=source, output_root=tmp_path / "unavailable"
        ).execute()
        assert len(result.points) == 216
        assert result.outcome is CommonSpaceVerificationOutcome.numerically_inconclusive
        assert all(point.assessment.resolved_rank is None for point in result.points)
        mismatches = CommonSpaceProducerCorrelation(
            independent=result, producer=producer
        ).execute()
        assert len(mismatches) == 216
        assert all("inconclusive" in value for value in mismatches)

    def test_nonunique_direction__does_not_create_resolved_orbital_weights(
        self,
    ) -> None:
        loader, _ = native_fixture.TestCommonSpaceNativeOverlapReconstruction._fixture()
        overlap = CommonSpaceNativeOverlapReconstruction(
            parsed_inputs=loader.execute(), ordered_index=0
        ).execute()
        assessment = CommonSpaceNativePrecisionAssessment(
            overlap=overlap,
            rounding_model=CommonSpaceNativeRoundingModel.from_nearest_decimal_places(
                amn=12, gauge=10, disentanglement=10
            ),
            frozen_rank_threshold=Fraction(1, 100),
        ).execute()
        uncertain = replace(
            assessment,
            arithmetic=replace(assessment.arithmetic, rank_threshold=Fraction(1000)),
        )
        direction = CommonSpaceDeficientDirectionAnalysis(
            assessment=uncertain
        ).execute()
        assert direction.outcome is CommonSpaceDirectionOutcome.multiple_directions
        assert direction.orbital_intervals == ()
        assert CommonSpaceUnitaryInvariance(assessment=assessment).execute()
        with pytest.raises(ValueError, match="lie in"):
            CommonSpaceWeightInterval(lower=Fraction(-1), upper=Fraction(1))
