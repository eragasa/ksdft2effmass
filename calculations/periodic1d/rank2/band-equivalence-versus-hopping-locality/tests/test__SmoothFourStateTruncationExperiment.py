"""Software verification for finite-range non-flat band consequences."""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest
from jsonschema import Draft202012Validator  # type: ignore[import-untyped]
from workflow import canonical_json_bytes
from workflow.nonflat import SmoothFourStateDefinition
from workflow.serialization import JsonValue
from workflow.truncation import (
    SmoothFourStateTruncationDefinition,
    SmoothFourStateTruncationExperiment,
    SmoothFourStateTruncationInputSerializer,
    SmoothFourStateTruncationResultSerializer,
    SmoothFourStateTruncationVerificationSerializer,
    SmoothFourStateTruncationVerifier,
)

pytestmark = pytest.mark.software_verification


class TestSmoothFourStateTruncationExperiment:
    """Establish disjoint evaluation and separated approximation channels."""

    @staticmethod
    def _model() -> SmoothFourStateDefinition:
        return SmoothFourStateDefinition(
            reciprocal_mesh_size=32,
            amplitudes=(0.0, math.pi / 8.0, math.pi / 4.0),
            minimum_external_gap=1.0,
            minimum_transport_singular_value=0.99,
            frame_absolute_tolerance=1.0e-11,
            harmonic_absolute_degeneracy_tolerance=1.0e-14,
            harmonic_relative_degeneracy_tolerance=1.0e-13,
            verification_absolute_tolerance=1.0e-10,
            parent_hopping_scale=1.0,
        )

    @staticmethod
    def _mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        if type(value) is not dict:
            raise TypeError(f"{name} must be a mapping")
        return value

    @staticmethod
    def _experiment_root() -> Path:
        return Path(__file__).resolve().parents[1]

    @classmethod
    def _definition(cls) -> SmoothFourStateTruncationDefinition:
        return SmoothFourStateTruncationDefinition(
            model=cls._model(),
            maximum_ranges=(0, 1, 2, 15),
            evaluation_mesh_size=129,
        )

    def test_definition__rejects_cyclic_nyquist_and_invalid_scalar_types(self) -> None:
        model = self._model()
        with pytest.raises(ValueError, match="exclude the cyclic Nyquist"):
            SmoothFourStateTruncationDefinition(
                model=model,
                maximum_ranges=(0, 16),
                evaluation_mesh_size=129,
            )
        with pytest.raises(TypeError, match="built-in ints"):
            SmoothFourStateTruncationDefinition(
                model=model,
                maximum_ranges=(0, True),
                evaluation_mesh_size=129,
            )
        with pytest.raises(ValueError, match=r"at least 2\*N\+1"):
            SmoothFourStateTruncationDefinition(
                model=model,
                maximum_ranges=(0, 1),
                evaluation_mesh_size=64,
            )

    def test_definition__constructs_every_integer_cutoff_through_the_cap(self) -> None:
        definition = SmoothFourStateTruncationDefinition.every_integer_through(
            model=self._model(),
            maximum_range=15,
            evaluation_mesh_size=129,
        )

        assert definition.maximum_ranges == tuple(range(16))
        assert definition.has_dense_integer_inventory
        assert not self._definition().has_dense_integer_inventory
        with pytest.raises(TypeError, match="built-in int"):
            SmoothFourStateTruncationDefinition.every_integer_through(
                model=self._model(),
                maximum_range=True,
                evaluation_mesh_size=129,
            )

    def test_execute__separates_nyquist_interpolation_and_range_truncation(
        self,
    ) -> None:
        result = SmoothFourStateTruncationExperiment().execute(self._definition())

        assert result.minimum_construction_evaluation_separation > 0.0
        assert (
            tuple(point.amplitude for point in result.points)
            == self._model().amplitudes
        )
        assert result.points[
            0
        ].comparison_maximum_interpolation_band_error == pytest.approx(0.0, abs=2.0e-14)
        assert result.points[
            0
        ].comparison_maximum_interpolation_hamiltonian_error == pytest.approx(
            0.0, abs=2.0e-14
        )
        assert result.points[-1].maximum_direct_band_defect == pytest.approx(
            0.0, abs=2.0e-14
        )
        for point in result.points:
            assert point.reference_maximum_ordinary_hermiticity_defect <= 1.0e-11
            assert point.comparison_maximum_ordinary_hermiticity_defect <= 1.0e-11
            ordinary_reference = tuple(
                item.reference_ordinary_omitted_power for item in point.ranges
            )
            ordinary_comparison = tuple(
                item.comparison_ordinary_omitted_power for item in point.ranges
            )
            assert ordinary_reference == tuple(sorted(ordinary_reference, reverse=True))
            assert ordinary_comparison == tuple(
                sorted(ordinary_comparison, reverse=True)
            )
            full = point.ranges[-1]
            assert full.reference_ordinary_omitted_power == pytest.approx(0.0)
            assert full.comparison_ordinary_omitted_power == pytest.approx(0.0)
            assert full.reference_maximum_band_error == pytest.approx(0.0, abs=2.0e-14)
            assert full.reference_maximum_truncation_hamiltonian_error == pytest.approx(
                0.0, abs=2.0e-14
            )
            assert full.comparison_maximum_truncation_band_error == pytest.approx(
                0.0, abs=2.0e-14
            )
            assert (
                full.comparison_maximum_truncation_hamiltonian_error
                == pytest.approx(0.0, abs=2.0e-14)
            )
            assert full.reference_total_omitted_power == pytest.approx(
                point.reference_nyquist_power
            )
            assert full.comparison_total_omitted_power == pytest.approx(
                point.comparison_nyquist_power
            )
            assert full.comparison_maximum_total_band_error == pytest.approx(
                point.comparison_maximum_interpolation_band_error,
                abs=2.0e-14,
            )
            assert full.comparison_maximum_total_hamiltonian_error == pytest.approx(
                point.comparison_maximum_interpolation_hamiltonian_error,
                abs=2.0e-14,
            )

    def test_execute__relates_matrix_errors_to_power_and_band_bounds(self) -> None:
        result = SmoothFourStateTruncationExperiment().execute(self._definition())
        root_rank = math.sqrt(2.0)

        for point in result.points:
            assert point.comparison_maximum_interpolation_band_error <= (
                root_rank * point.comparison_maximum_interpolation_hamiltonian_error
                + 2.0e-14
            )
            for item in point.ranges:
                assert item.reference_rms_truncation_hamiltonian_error == pytest.approx(
                    math.sqrt(item.reference_ordinary_omitted_power),
                    abs=2.0e-14,
                )
                assert (
                    item.comparison_rms_truncation_hamiltonian_error
                    == pytest.approx(
                        math.sqrt(item.comparison_ordinary_omitted_power),
                        abs=2.0e-14,
                    )
                )
                assert item.reference_maximum_band_error <= (
                    root_rank * item.reference_maximum_truncation_hamiltonian_error
                    + 2.0e-14
                )
                assert item.comparison_maximum_truncation_band_error <= (
                    root_rank * item.comparison_maximum_truncation_hamiltonian_error
                    + 2.0e-14
                )
                assert item.comparison_maximum_total_band_error <= (
                    root_rank * item.comparison_maximum_total_hamiltonian_error
                    + 2.0e-14
                )

    def test_owner_eigenvalues__reject_nonhermitian_evaluated_matrices(self) -> None:
        matrices = np.asarray([[[0.0, 1.0], [0.0, 0.0]]], dtype=np.complex128)

        with pytest.raises(ValueError):
            SmoothFourStateTruncationExperiment._owner_eigenvalues(matrices, 1.0e-12)

    def test_verifier__independently_reconstructs_channels_and_range_decisions(
        self,
    ) -> None:
        result = SmoothFourStateTruncationExperiment().execute(self._definition())

        verification = SmoothFourStateTruncationVerifier().execute(
            result,
            (1.0e-6, 1.0e-8),
        )

        assert verification.passes
        assert verification.maximum_absolute_discrepancy <= 1.0e-10
        assert not verification.inventory_is_dense
        assert len(verification.decisions) == 2 * len(result.points)
        declared_ranges = set(self._definition().maximum_ranges)
        for decision in verification.decisions:
            for selected in (
                decision.reference_band_first_passing_range,
                decision.comparison_band_first_passing_range,
                decision.reference_hamiltonian_first_passing_range,
                decision.comparison_hamiltonian_first_passing_range,
            ):
                assert selected is None or selected in declared_ranges

    def test_verifier__fails_when_a_retained_channel_is_changed(self) -> None:
        result = SmoothFourStateTruncationExperiment().execute(self._definition())
        point = result.points[-1]
        changed_range = replace(
            point.ranges[0],
            comparison_maximum_total_band_error=(
                point.ranges[0].comparison_maximum_total_band_error + 1.0e-4
            ),
        )
        changed_point = replace(point, ranges=(changed_range, *point.ranges[1:]))
        changed = replace(result, points=(*result.points[:-1], changed_point))

        verification = SmoothFourStateTruncationVerifier().execute(
            changed,
            (1.0e-8,),
        )

        assert not verification.passes
        assert verification.maximum_absolute_discrepancy == pytest.approx(1.0e-4)

    def test_verifier__rejects_ambiguous_decision_tolerances(self) -> None:
        result = SmoothFourStateTruncationExperiment().execute(self._definition())
        verifier = SmoothFourStateTruncationVerifier()

        with pytest.raises(TypeError, match="built-in floats"):
            verifier.execute(result, (True,))
        with pytest.raises(ValueError, match="strictly decreasing"):
            verifier.execute(result, (1.0e-8, 1.0e-6))

    def test_serialization__is_strict_canonical_and_digest_bound(self) -> None:
        definition = SmoothFourStateTruncationDefinition.every_integer_through(
            model=self._model(),
            maximum_range=8,
            evaluation_mesh_size=129,
        )
        result = SmoothFourStateTruncationExperiment().execute(definition)
        verification = SmoothFourStateTruncationVerifier().execute(
            result,
            (1.0e-6, 1.0e-8),
        )
        input_wire = SmoothFourStateTruncationInputSerializer().serialize(definition)
        result_wire = SmoothFourStateTruncationResultSerializer().serialize(result)
        verification_wire = SmoothFourStateTruncationVerificationSerializer().serialize(
            verification
        )
        records = (
            (input_wire, "truncation-input.schema.json"),
            (result_wire, "truncation-result.schema.json"),
            (verification_wire, "truncation-verification.schema.json"),
        )
        documents: list[dict[str, JsonValue]] = []
        for wire, filename in records:
            document_value: JsonValue = json.loads(wire)
            document = self._mapping(document_value, "serialized document")
            documents.append(document)
            assert canonical_json_bytes(document) == wire
            schema_value: JsonValue = json.loads(
                (
                    self._experiment_root() / "workflow" / "schema_documents" / filename
                ).read_text(encoding="utf-8")
            )
            schema = self._mapping(schema_value, "schema")
            Draft202012Validator.check_schema(schema)
            validator = Draft202012Validator(schema)
            assert validator.is_valid(document)
            changed_value: JsonValue = json.loads(json.dumps(document))
            changed = self._mapping(changed_value, "changed document")
            changed["unknown"] = True
            assert not validator.is_valid(changed)

        input_binding = self._mapping(documents[1]["input_binding"], "input binding")
        result_binding = self._mapping(documents[2]["result_binding"], "result binding")
        assert input_binding["sha256"] == hashlib.sha256(input_wire).hexdigest()
        assert result_binding["sha256"] == hashlib.sha256(result_wire).hexdigest()
        assert documents[0]["dense_integer_inventory"] is True
        scope = self._mapping(documents[0]["scope"], "scope")
        assert scope["protocol_frozen"] is False
        assert scope["provenance_record"] is False
        assert scope["retained_run"] is False

    def test_result__rejects_total_power_that_excludes_ordinary_omissions(self) -> None:
        result = SmoothFourStateTruncationExperiment().execute(self._definition())
        first_range = result.points[-1].ranges[0]

        with pytest.raises(ValueError, match="must include Nyquist power"):
            replace(first_range, comparison_total_omitted_power=0.0)
