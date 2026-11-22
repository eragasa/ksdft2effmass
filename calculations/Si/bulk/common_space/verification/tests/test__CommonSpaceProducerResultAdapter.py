"""Actual producer JSON adaptation using synthetic native bytes, never retained analysis."""

from __future__ import annotations

import io
from dataclasses import replace
from fractions import Fraction
from itertools import product
from pathlib import Path

import common_space.diagnostics.diagnosis as producer
import common_space.verification.tests.test__CommonSpaceNativeOverlapReconstruction as native_fixture
import pytest
from common_space.verification import (
    CommonSpaceEvidenceRole,
    CommonSpaceIndependentGridResult,
    CommonSpaceNativeRoundingModel,
    CommonSpaceProducerCorrelation,
    CommonSpaceProducerCorrelationRun,
    CommonSpaceProducerResultAdapter,
    CommonSpaceReviewScope,
    CommonSpaceSourceAdmission,
    CommonSpaceSourceEvidence,
    CommonSpaceVerificationOutcome,
    CommonSpaceVerificationRun,
)
from common_space.verification.source_admission import (
    CommonSpaceVerificationJson,
    JsonValue,
)
from projectkoios.integrations.wannier90 import Wannier90NativeArtifact

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestCommonSpaceProducerResultAdapter:
    """Exercise original producer bytes and fail closed on missing/mismatched data."""

    @staticmethod
    def _object(value: JsonValue) -> dict[str, JsonValue]:
        assert type(value) is dict
        return value

    @staticmethod
    def _list(value: JsonValue) -> list[JsonValue]:
        assert type(value) is list
        return value

    @staticmethod
    def _seal(source: CommonSpaceSourceAdmission) -> CommonSpaceSourceAdmission:
        """Construct synthetic test declarations, not real scientific review/completion."""
        wire = CommonSpaceVerificationJson
        assertion = Wannier90NativeArtifact(
            "assertions.json", source.assertion_payload()
        )
        completion = Wannier90NativeArtifact(
            "completion.json",
            wire.encode(
                {
                    "record_type": "common-space-producer-prerequisites-v1",
                    "state_assertions_sha256": assertion.identity.sha256,
                    "full_grid_reconstruction_complete": True,
                    "symmetry_inventory_complete": True,
                    "completed_evidence": [
                        {
                            "role": role.to_wire(),
                            "identity": wire.identity(
                                next(
                                    item.expected
                                    for item in source.evidence
                                    if item.role is role
                                )
                            ),
                        }
                        for role in source.producer_prerequisite_roles
                    ],
                    "review_scope": CommonSpaceReviewScope.synthetic.to_wire(),
                }
            ),
        )
        replacements = {
            CommonSpaceEvidenceRole.state_assertions: assertion,
            CommonSpaceEvidenceRole.producer_completion: completion,
        }
        return replace(
            source,
            evidence=tuple(
                replace(
                    item,
                    expected=(value := replacements[item.role]).identity,
                    artifact=value,
                )
                if item.role in replacements
                else item
                for item in source.evidence
            ),
        )

    @pytest.fixture(scope="class")
    @classmethod
    def source(
        cls, tmp_path_factory: pytest.TempPathFactory
    ) -> CommonSpaceSourceAdmission:
        root = tmp_path_factory.mktemp("synthetic-original-producer")
        wire = CommonSpaceVerificationJson
        request = cls._object(wire.decode(producer.DEFAULT_REQUEST.read_bytes()))
        state = cls._object(request["state_space"])
        loader, _ = native_fixture.TestCommonSpaceNativeOverlapReconstruction._fixture(
            points=tuple(
                (x / 6, y / 6, z / 6) for x, y, z in product(range(6), repeat=3)
            ),
            bands=20,
            constant_target=True,
            deficient_indices=(0, 12),
            mixed_direction_indices=(12,),
            outside_frame_amplitude=complex(2.944603369441934),
        )
        geometry, energy = state["geometry"], state["energy_reference"]
        assert type(geometry) is str and type(energy) is str
        loader = replace(
            loader,
            contract=replace(
                loader.contract,
                geometry_identity=geometry,
                energy_reference_identity=energy,
            ),
        )
        artifacts: dict[CommonSpaceEvidenceRole, Wannier90NativeArtifact] = {}
        declarations: dict[str, JsonValue] = {}
        roles = (
            (
                "S30_untruncated_characterization",
                CommonSpaceEvidenceRole.full_source,
                "full-source.json",
            ),
            (
                "S105_full_support_disposition",
                CommonSpaceEvidenceRole.full_support,
                "full-support.json",
            ),
            (
                "S110_blocked_result",
                CommonSpaceEvidenceRole.blocked_alignment,
                "blocked-result.json",
            ),
            (
                "hopping_first_protocol",
                CommonSpaceEvidenceRole.protocol,
                "protocol.txt",
            ),
        )
        for label, role, name in roles:
            artifact = Wannier90NativeArtifact(
                name, b"Synthetic prerequisite placeholder; NOT scientific evidence.\n"
            )
            artifacts[role] = artifact
            path = root / artifact.name
            path.write_bytes(artifact.payload)
            declarations[label] = {
                "location": "absolute",
                "path": str(path),
                "byte_size": artifact.identity.byte_count,
                "sha256": artifact.identity.sha256,
            }
        for label, artifact in zip(
            ("AMN", "gauge", "disentanglement"), loader.artifacts, strict=True
        ):
            path = root / artifact.name
            path.write_bytes(artifact.payload)
            declarations[label] = {
                "location": "absolute",
                "path": str(path),
                "byte_size": artifact.identity.byte_count,
                "sha256": artifact.identity.sha256,
            }
        request["sources"] = declarations
        comparison = cls._object(request["retained_diagnosis_comparison"])
        comparison["deficient_kpoint_indices_zero_based"] = [0, 12]
        comparison["minimum_singular_values"] = [0.0, 0.0]
        comparison["gamma_atomic_orbital_weights"] = {
            label: float(i == 9)
            for i, label in enumerate(loader.contract.atomic_basis_order)
        }
        request_path = root / "request.json"
        request_path.write_bytes(wire.encode(request))
        artifacts[CommonSpaceEvidenceRole.request] = Wannier90NativeArtifact(
            request_path.name, request_path.read_bytes()
        )

        def synthetic_semantics(
            *,
            request: producer.CommonSpaceDiagnosisRequest,
            source_paths: dict[str, Path],
        ) -> None:
            # The real producer runs, but legacy physical source-review content is
            # deliberately outside this synthetic test. No live native path is read.
            assert all(path.parent == root for path in source_paths.values())

        with pytest.MonkeyPatch.context() as patch:
            patch.setattr(
                producer, "validate_retained_source_contract", synthetic_semantics
            )
            producer.CommonSpaceRankDiagnosis().execute(
                request_path=request_path,
                output_root=root / "producer",
                reporter=producer.HumanReadableProgressReporter(stream=io.StringIO()),
                source_scope=CommonSpaceReviewScope.synthetic,
            )
        assert not (root / "producer" / "producer-completion.json").exists()
        assert not (root / "producer" / "point-inventory.json").exists()
        path = root / "producer" / producer.RESULT_NAME
        artifacts[CommonSpaceEvidenceRole.producer_reconstruction] = (
            Wannier90NativeArtifact(path.name, path.read_bytes())
        )
        for role in CommonSpaceEvidenceRole:
            if role not in artifacts:
                artifacts[role] = Wannier90NativeArtifact(
                    f"{role.to_wire()}.json",
                    b"Synthetic review/prerequisite placeholder only.\n",
                )
        source = CommonSpaceSourceAdmission(
            parsed_inputs=loader.execute(),
            rounding_model=CommonSpaceNativeRoundingModel.from_nearest_decimal_places(
                amn=12, gauge=10, disentanglement=10
            ),
            frozen_rank_threshold=Fraction.from_float(5.890206739032098e-7),
            review_scope=CommonSpaceReviewScope.synthetic,
            review_reference="synthetic-fixture-not-scientific-review",
            parent_band_state_identity="synthetic-parent-band-space",
            gauge_state_identity="synthetic-gauge",
            evidence=tuple(
                CommonSpaceSourceEvidence(
                    role=role,
                    expected=artifacts[role].identity,
                    artifact=artifacts[role],
                )
                for role in CommonSpaceEvidenceRole
            ),
        )
        return cls._seal(source)

    @pytest.fixture(scope="class")
    @classmethod
    def run(
        cls,
        source: CommonSpaceSourceAdmission,
        tmp_path_factory: pytest.TempPathFactory,
    ) -> tuple[CommonSpaceIndependentGridResult, Path]:
        root = tmp_path_factory.mktemp("synthetic-original-comparison") / "independent"
        original = next(
            item.artifact.payload
            for item in source.evidence
            if item.role is CommonSpaceEvidenceRole.producer_reconstruction
        )
        decode = CommonSpaceVerificationJson.decode

        def independent_decode(payload: bytes) -> JsonValue:
            assert payload != original, (
                "producer numeric JSON must not be decoded during independent computation"
            )
            return decode(payload)

        with pytest.MonkeyPatch.context() as patch:
            patch.setattr(
                CommonSpaceVerificationJson, "decode", staticmethod(independent_decode)
            )
            result = CommonSpaceVerificationRun(
                admission=source, output_root=root
            ).execute()
        return result, root

    @classmethod
    def _document(
        cls, result: CommonSpaceIndependentGridResult
    ) -> dict[str, JsonValue]:
        artifact = next(
            item.artifact
            for item in result.admission.evidence
            if item.role is CommonSpaceEvidenceRole.producer_reconstruction
        )
        return cls._object(CommonSpaceVerificationJson.decode(artifact.payload))

    @classmethod
    def _rebind(
        cls, result: CommonSpaceIndependentGridResult, document: dict[str, JsonValue]
    ) -> CommonSpaceIndependentGridResult:
        evidence = tuple(
            replace(
                item,
                expected=(
                    artifact := Wannier90NativeArtifact(
                        item.artifact.name, CommonSpaceVerificationJson.encode(document)
                    )
                ).identity,
                artifact=artifact,
            )
            if item.role is CommonSpaceEvidenceRole.producer_reconstruction
            else item
            for item in result.admission.evidence
        )
        return replace(
            result, admission=cls._seal(replace(result.admission, evidence=evidence))
        )

    @classmethod
    def _explicit_source_link(
        cls, result: CommonSpaceIndependentGridResult
    ) -> CommonSpaceIndependentGridResult:
        """Model distinct description/identifier fields using ONLY synthetic evidence."""
        wire = CommonSpaceVerificationJson
        request_item = next(
            item
            for item in result.admission.evidence
            if item.role is CommonSpaceEvidenceRole.request
        )
        request = cls._object(wire.decode(request_item.artifact.payload))
        state = cls._object(request["state_space"])
        state["geometry"] = "synthetic legacy geometry description, not an identifier"
        state["energy_reference"] = (
            "synthetic legacy energy description, not an identifier"
        )
        request_artifact = Wannier90NativeArtifact(
            request_item.artifact.name, wire.encode(request)
        )
        source = cls._seal(
            replace(
                result.admission,
                evidence=tuple(
                    replace(
                        item,
                        expected=request_artifact.identity,
                        artifact=request_artifact,
                    )
                    if item.role is CommonSpaceEvidenceRole.request
                    else item
                    for item in result.admission.evidence
                ),
            )
        )
        result = replace(result, admission=source)
        declaration = next(
            item.expected
            for item in source.evidence
            if item.role is CommonSpaceEvidenceRole.state_assertions
        )
        data = cls._document(result)
        metadata = cls._object(data["CSD0"])
        metadata["request"] = {
            "label": "request",
            "path": request_artifact.name,
            "byte_size": request_artifact.identity.byte_count,
            "sha256": request_artifact.identity.sha256,
        }
        metadata["source_association"] = {
            "declaration": {
                "label": "source-state-assertions",
                "path": declaration.name,
                "byte_size": declaration.byte_count,
                "sha256": declaration.sha256,
            },
            "geometry_identity": source.parsed_inputs.contract.geometry_identity,
            "native_provider_binding": [
                {"module_name": item.module_name, "sha256": item.sha256}
                for item in source.parsed_inputs.provider_binding.modules
            ],
        }
        cls._object(data["CSD1"])["state_space"] = dict(state)
        return cls._rebind(result, data)

    def test_explicit_source_link__does_not_equate_descriptions_with_identifiers(
        self, run: tuple[CommonSpaceIndependentGridResult, Path]
    ) -> None:
        original, _ = run
        result = self._explicit_source_link(original)
        data = self._document(result)
        state = self._object(self._object(data["CSD1"])["state_space"])
        assert (
            state["geometry"]
            != result.admission.parsed_inputs.contract.geometry_identity
        )
        assert (
            state["energy_reference"]
            != result.admission.parsed_inputs.contract.energy_reference_identity
        )
        assert result.admission.review_scope is CommonSpaceReviewScope.synthetic
        reference = CommonSpaceProducerResultAdapter(independent=result).execute()
        assert (
            CommonSpaceProducerCorrelation(
                independent=result, producer=reference
            ).execute()
            == ()
        )

    @pytest.mark.parametrize(
        "case",
        (
            "declaration",
            "geometry",
            "provider",
            "scope",
            "wire_geometry",
            "wire_energy",
        ),
    )
    def test_explicit_source_link__rejects_a_missing_or_unequal_member(
        self, run: tuple[CommonSpaceIndependentGridResult, Path], case: str
    ) -> None:
        original, _ = run
        result = self._explicit_source_link(original)
        data = self._document(result)
        association = self._object(self._object(data["CSD0"])["source_association"])
        if case == "declaration":
            self._object(association["declaration"])["sha256"] = "0" * 64
        elif case == "geometry":
            association["geometry_identity"] = "unrelated geometry identity"
        elif case == "provider":
            self._object(self._list(association["native_provider_binding"])[0])[
                "sha256"
            ] = "0" * 64
        elif case == "scope":
            data["review_scope"] = CommonSpaceReviewScope.retained.to_wire()
        elif case == "wire_geometry":
            self._object(self._object(data["CSD1"])["state_space"])["geometry"] = (
                "different description"
            )
        else:
            self._object(self._object(data["CSD1"])["state_space"])[
                "energy_reference"
            ] = "different energy description"
        with pytest.raises(ValueError):
            CommonSpaceProducerResultAdapter(
                independent=self._rebind(result, data)
            ).execute()

    def test_unlinked_legacy_descriptions__are_not_accepted_as_aliases(
        self, run: tuple[CommonSpaceIndependentGridResult, Path]
    ) -> None:
        original, _ = run
        result = self._explicit_source_link(original)
        data = self._document(result)
        del self._object(data["CSD0"])["source_association"]
        with pytest.raises(ValueError, match="state space"):
            CommonSpaceProducerResultAdapter(
                independent=self._rebind(result, data)
            ).execute()

    def test_decisive_agreement__does_not_require_extra_precision_evidence(
        self, run: tuple[CommonSpaceIndependentGridResult, Path]
    ) -> None:
        result, _ = run
        assert all(
            "precision" not in item.role.to_wire() for item in result.admission.evidence
        )
        reference = CommonSpaceProducerResultAdapter(independent=result).execute()
        assert (
            CommonSpaceProducerCorrelation(
                independent=result, producer=reference
            ).execute()
            == ()
        )

    def test_actual_producer_output__correlates_without_manual_normalization(
        self, run: tuple[CommonSpaceIndependentGridResult, Path]
    ) -> None:
        result, root = run
        reference = CommonSpaceProducerResultAdapter(independent=result).execute()
        assert len(reference.points) == 216
        assert result.deficient_indices == (0, 12)
        assert reference.points[0].atomic_weights != reference.points[12].atomic_weights
        assert (
            CommonSpaceProducerCorrelation(
                independent=result, producer=reference
            ).execute()
            == ()
        )
        original = (root / "independent-verification.json").read_bytes()
        action = CommonSpaceProducerCorrelationRun(independent=result, output_root=root)
        assert (
            action.execute() is CommonSpaceVerificationOutcome.rank_diagnosis_correlated
        )
        assert (root / "independent-verification.json").read_bytes() == original
        record = self._object(
            CommonSpaceVerificationJson.decode(
                (root / "producer-correlation.json").read_bytes()
            )
        )
        assert record["mismatches"] == []
        assert record["producer_result"] == CommonSpaceVerificationJson.identity(
            reference.producer_result_identity
        )
        with pytest.raises(FileExistsError):
            action.execute()

    @pytest.mark.parametrize(
        "case",
        (
            "schema",
            "execution",
            "request_id",
            "request_hash",
            "source_hash",
            "source_missing",
            "source_duplicate",
            "source_filename",
            "source_byte_count",
            "provider",
            "module_fingerprint",
            "module_duplicate",
            "basis",
            "geometry",
            "threshold",
            "point_count",
            "point_order",
            "coordinates",
            "coordinate_bool",
            "atomic_weights",
            "group_weights",
            "group_scalar_bool",
            "full_rank_weights",
            "rank_bool",
            "spectrum_string",
            "gamma_duplicate",
            "counter_bool",
        ),
    )
    def test_malformed_or_mismatched_original__cannot_be_adapted(
        self, run: tuple[CommonSpaceIndependentGridResult, Path], case: str
    ) -> None:
        result, _ = run
        data = self._document(result)
        source = self._object(data["CSD0"])
        analysis = self._object(data["CSD1"])
        table = self._list(analysis["complete_kpoint_diagnostics"])
        point = self._object(table[12])
        if case == "schema":
            data["schema_version"] = 2
        elif case == "execution":
            data["execution_outcome"] = "failed"
        elif case == "request_id":
            data["request_id"] = "different"
        elif case == "request_hash":
            self._object(source["request"])["sha256"] = "0" * 64
        elif case == "source_hash":
            self._object(self._list(source["authenticated_files"])[0])["sha256"] = (
                "0" * 64
            )
        elif case == "source_missing":
            self._list(source["authenticated_files"]).pop()
        elif case == "source_duplicate":
            files = self._list(source["authenticated_files"])
            files[1] = files[0]
        elif case == "source_filename":
            self._object(self._list(source["authenticated_files"])[0])["path"] = (
                "/not-followed/different.json"
            )
        elif case == "source_byte_count":
            self._object(self._list(source["authenticated_files"])[0])["byte_size"] = (
                True
            )
        elif case == "provider":
            source["provider_version"] = "different"
        elif case == "module_fingerprint":
            self._object(self._list(source["provider_modules"])[0])["sha256"] = "0" * 64
        elif case == "module_duplicate":
            modules = self._list(source["provider_modules"])
            modules[1] = modules[0]
        elif case == "basis":
            self._list(self._object(analysis["state_space"])["basis_order"]).reverse()
        elif case == "geometry":
            self._object(analysis["state_space"])["geometry"] = "different"
        elif case == "threshold":
            analysis["singular_value_native_uncertainty_bound"] = 1e-4
        elif case == "point_count":
            table.pop()
        elif case == "point_order":
            table[0], table[1] = table[1], table[0]
        elif case == "coordinates":
            point["fractional_reciprocal_coordinates"] = [0.0, 0.0, 0.0]
        elif case == "coordinate_bool":
            self._list(point["fractional_reciprocal_coordinates"])[0] = False
        elif case == "atomic_weights":
            del point["minimum_direction_atomic_weights"]
        elif case == "group_weights":
            del point["minimum_direction_group_weights_s_p_s_star"]
        elif case == "group_scalar_bool":
            self._list(point["minimum_direction_group_weights_s_p_s_star"])[0] = True
        elif case == "full_rank_weights":
            self._object(table[1])["minimum_direction_group_weights_s_p_s_star"] = [
                0.0,
                0.0,
                0.0,
            ]
        elif case == "rank_bool":
            point["resolved_rank_at_native_bound"] = True
        elif case == "spectrum_string":
            point["minimum_singular_value"] = "0.0"
        elif case == "gamma_duplicate":
            self._object(analysis["gamma_null_direction_atomic_orbital_weights"])[
                result.admission.parsed_inputs.contract.atomic_basis_order[0]
            ] = 1.0
        elif case == "counter_bool":
            data["calculator_invocations"] = False
        with pytest.raises(ValueError):
            CommonSpaceProducerResultAdapter(
                independent=self._rebind(result, data)
            ).execute()

    def test_signed_zero_coordinate__matches_shared_parsed_numeric_contract(
        self, run: tuple[CommonSpaceIndependentGridResult, Path]
    ) -> None:
        result, _ = run
        data = self._document(result)
        analysis = self._object(data["CSD1"])
        point = self._object(self._list(analysis["complete_kpoint_diagnostics"])[12])
        self._list(point["fractional_reciprocal_coordinates"])[0] = -0.0
        self._list(analysis["deficient_kpoints"])[1] = point
        reference = CommonSpaceProducerResultAdapter(
            independent=self._rebind(result, data)
        ).execute()
        assert reference.points[12].resolved_rank == 9

    @pytest.mark.parametrize("places", (True, 11, 1000000000))
    def test_request_precision__must_match_the_explicit_admitted_model(
        self, run: tuple[CommonSpaceIndependentGridResult, Path], places: int | bool
    ) -> None:
        result, _ = run
        entry = next(
            item
            for item in result.admission.evidence
            if item.role is CommonSpaceEvidenceRole.request
        )
        request = self._object(
            CommonSpaceVerificationJson.decode(entry.artifact.payload)
        )
        self._object(request["native_precision"])["AMN_decimal_places"] = places
        artifact = Wannier90NativeArtifact(
            entry.artifact.name, CommonSpaceVerificationJson.encode(request)
        )
        document = self._document(result)
        request_identity = self._object(self._object(document["CSD0"])["request"])
        request_identity["byte_size"] = artifact.identity.byte_count
        request_identity["sha256"] = artifact.identity.sha256
        modified = self._rebind(result, document)
        evidence = tuple(
            replace(item, expected=artifact.identity, artifact=artifact)
            if item.role is CommonSpaceEvidenceRole.request
            else item
            for item in modified.admission.evidence
        )
        modified = replace(
            modified,
            admission=self._seal(replace(modified.admission, evidence=evidence)),
        )
        with pytest.raises(ValueError):
            CommonSpaceProducerResultAdapter(independent=modified).execute()

    def test_reported_group_weights__are_compared_not_recomputed_from_atomic_values(
        self, run: tuple[CommonSpaceIndependentGridResult, Path]
    ) -> None:
        result, _ = run
        data = self._document(result)
        analysis = self._object(data["CSD1"])
        table = self._list(analysis["complete_kpoint_diagnostics"])
        point = self._object(table[12])
        point["minimum_direction_group_weights_s_p_s_star"] = [1.0, 0.0, 0.0]
        self._list(analysis["deficient_kpoints"])[1] = point
        modified = self._rebind(result, data)
        reference = CommonSpaceProducerResultAdapter(independent=modified).execute()
        mismatch = CommonSpaceProducerCorrelation(
            independent=modified, producer=reference
        ).execute()
        assert any("aggregate orbital weights differ" in item for item in mismatch)

    def test_retired_manual_comparison_document__has_no_fallback(
        self, run: tuple[CommonSpaceIndependentGridResult, Path]
    ) -> None:
        result, _ = run
        legacy: dict[str, JsonValue] = {
            "record_type": "common-space-producer-comparison-v1",
            "points": [],
        }
        with pytest.raises(ValueError, match="schema_version"):
            CommonSpaceProducerResultAdapter(
                independent=self._rebind(result, legacy)
            ).execute()

    def test_unmatched_producer_bytes__fail_authentication_before_json_decoding(
        self, run: tuple[CommonSpaceIndependentGridResult, Path]
    ) -> None:
        result, _ = run
        evidence = tuple(
            replace(item, artifact=replace(item.artifact, payload=b"not JSON"))
            if item.role is CommonSpaceEvidenceRole.producer_reconstruction
            else item
            for item in result.admission.evidence
        )
        modified = replace(
            result, admission=replace(result.admission, evidence=evidence)
        )
        with pytest.raises(ValueError, match="identities do not agree"):
            CommonSpaceProducerResultAdapter(independent=modified).execute()

    def test_missing_completion__cannot_be_inferred_from_producer_success(
        self, run: tuple[CommonSpaceIndependentGridResult, Path]
    ) -> None:
        result, _ = run
        items: list[CommonSpaceSourceEvidence] = []
        for item in result.admission.evidence:
            if item.role is CommonSpaceEvidenceRole.producer_completion:
                data = self._object(
                    CommonSpaceVerificationJson.decode(item.artifact.payload)
                )
                data["full_grid_reconstruction_complete"] = False
                artifact = Wannier90NativeArtifact(
                    item.artifact.name, CommonSpaceVerificationJson.encode(data)
                )
                item = replace(item, expected=artifact.identity, artifact=artifact)
            items.append(item)
        with pytest.raises(ValueError, match="prerequisite"):
            CommonSpaceProducerResultAdapter(
                independent=replace(
                    result, admission=replace(result.admission, evidence=tuple(items))
                )
            ).execute()
