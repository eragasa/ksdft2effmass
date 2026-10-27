"""Software verification for the smooth band-equivalent continuum."""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import replace
from importlib.resources import files
from importlib.resources.abc import Traversable

import pytest
from jsonschema import Draft202012Validator  # type: ignore[import-untyped]
from projectkoios.optimization.selection.harmonic import (
    PeriodicHarmonicMaximumStatus,
)
from workflow import (
    SmoothBlochContinuumConvergenceDefinition,
    SmoothBlochContinuumConvergenceDisposition,
    SmoothBlochContinuumConvergenceExperiment,
    SmoothBlochContinuumConvergenceResult,
    SmoothBlochContinuumConvergenceThresholds,
    SmoothBlochContinuumConvergenceVerifier,
    SmoothBlochContinuumDefinition,
    SmoothBlochContinuumExperiment,
    SmoothBlochContinuumInputSerializer,
    SmoothBlochContinuumResult,
    SmoothBlochContinuumResultSerializer,
    SmoothBlochContinuumVerificationSerializer,
    SmoothBlochContinuumVerifier,
    canonical_json_bytes,
)

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]

pytestmark = pytest.mark.software_verification


class TestSmoothBlochContinuumExperiment:
    """Establish the analytic, Fourier, owner-selection, and verifier contracts."""

    @staticmethod
    def mapping(value: JsonValue, context: str) -> dict[str, JsonValue]:
        """Narrow one decoded JSON mapping without an unspecified boundary type."""
        if type(value) is not dict:
            raise TypeError(f"{context} must be a built-in dict")
        return value

    @staticmethod
    def definition() -> SmoothBlochContinuumDefinition:
        """Return a compact complete continuum definition."""
        return SmoothBlochContinuumDefinition(
            reciprocal_mesh_size=64,
            amplitudes=(0.0, math.pi / 16.0, math.pi / 8.0, math.pi / 4.0),
            harmonic_absolute_degeneracy_tolerance=1.0e-14,
            harmonic_relative_degeneracy_tolerance=1.0e-13,
            verification_absolute_tolerance=1.0e-11,
        )

    @staticmethod
    def convergence_definition(
        *, maximum_correlation_change: float = 1.0e-10
    ) -> SmoothBlochContinuumConvergenceDefinition:
        """Return caller-selected controls for a compact nested-mesh study."""
        return SmoothBlochContinuumConvergenceDefinition(
            reciprocal_mesh_sizes=(8, 16, 32),
            amplitudes=(0.0, math.pi / 8.0, math.pi / 4.0),
            harmonic_absolute_degeneracy_tolerance=1.0e-14,
            harmonic_relative_degeneracy_tolerance=1.0e-13,
            verification_absolute_tolerance=1.0e-11,
            thresholds=SmoothBlochContinuumConvergenceThresholds(
                maximum_correlation_change=maximum_correlation_change,
                maximum_threshold_change=1.0e-9,
                maximum_hopping_weight_change=1.0e-9,
                maximum_hopping_block_power_change=1.0e-9,
                maximum_angle_change=1.0e-9,
                maximum_fine_quadrature_defect=1.0e-9,
                maximum_band_defect=1.0e-9,
                maximum_identity_defect=1.0e-9,
                maximum_parseval_defect=1.0e-9,
            ),
            required_stable_refinements=1,
        )

    @staticmethod
    def schema_documents() -> Traversable:
        """Return the calculation-owned workflow schema directory."""
        return files("workflow").joinpath("schema_documents")

    def test_definition_rejects_ambiguous_numeric_controls(self) -> None:
        """Reject booleans, numeric strings, incomplete meshes, and zero tolerance."""
        definition = self.definition()
        with pytest.raises(TypeError, match="built-in int"):
            replace(definition, reciprocal_mesh_size=True)
        with pytest.raises(TypeError, match="built-in float"):
            replace(definition, amplitudes=(0.0, "0.1"))  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="even"):
            replace(definition, reciprocal_mesh_size=63)
        with pytest.raises(ValueError, match="begin at zero"):
            replace(definition, amplitudes=(0.1, 0.2))
        with pytest.raises(ValueError, match="verification_absolute_tolerance"):
            replace(definition, verification_absolute_tolerance=0.0)

    def test_execute_separates_identical_bands_from_operator_and_hopping_channels(
        self,
    ) -> None:
        """Retain zero band defects and increasing operator/locality thresholds."""
        result = SmoothBlochContinuumExperiment().execute(self.definition())

        assert isinstance(result, SmoothBlochContinuumResult)
        assert len(result.points) == 4
        assert max(point.maximum_band_defect for point in result.points) < 5.0e-16
        assert (
            tuple(point.harmonic_maximum.status for point in result.points)
            == (PeriodicHarmonicMaximumStatus.UNIQUE,) * 4
        )
        assert (
            max(
                abs(point.harmonic_maximum.canonical_maximizing_argument or 0.0)
                for point in result.points
            )
            < 1.0e-14
        )

        analytic_correlations = (
            1.0,
            0.9618168560737431,
            0.8516319137048080,
            0.47200121576823473,
        )
        for point, expected in zip(result.points, analytic_correlations, strict=True):
            assert point.analytic_maximum_correlation == pytest.approx(
                expected, rel=0.0, abs=2.0e-15
            )
            assert point.discrete_maximum_correlation == pytest.approx(
                expected, rel=0.0, abs=2.0e-15
            )
            assert point.correlation_quadrature_defect < 2.0e-15
            assert point.three_way_identity_defect < 2.0e-15
            assert point.parseval_defect < 2.0e-15

        minimum_thresholds = tuple(
            point.minimum_operator_threshold for point in result.points
        )
        joint_thresholds = tuple(
            point.exact_spectrum_joint_operator_threshold for point in result.points
        )
        assert minimum_thresholds == tuple(sorted(minimum_thresholds))
        assert joint_thresholds == tuple(sorted(joint_thresholds))
        assert minimum_thresholds[0] == 0.0
        assert joint_thresholds[0] == 0.0
        assert result.points[-1].nonzero_hopping_weight == pytest.approx(
            result.points[-1].irreducible_operator_squared_loss,
            rel=0.0,
            abs=2.0e-15,
        )

    def test_finite_mesh_correlation_is_not_replaced_by_analytic_comparator(
        self,
    ) -> None:
        """Preserve quadrature evidence separately from the Bessel comparator."""
        defects: list[float] = []
        for sample_count in (8, 16, 32):
            definition = replace(
                self.definition(),
                reciprocal_mesh_size=sample_count,
                amplitudes=(0.0, math.pi / 4.0),
            )
            point = SmoothBlochContinuumExperiment().execute(definition).points[-1]
            defects.append(point.correlation_quadrature_defect)
            assert point.correlation_quadrature_defect == pytest.approx(
                abs(
                    point.discrete_maximum_correlation
                    - point.analytic_maximum_correlation
                ),
                rel=0.0,
                abs=1.0e-16,
            )
        assert defects[0] > 1.0e-6
        assert defects[1] < 3.0e-15
        assert defects[2] < defects[1]

    def test_nested_mesh_disposition_is_conservative_and_caller_controlled(
        self,
    ) -> None:
        """Classify only stable final refinements and otherwise remain unresolved."""
        action = SmoothBlochContinuumConvergenceExperiment()
        converged = action.execute(self.convergence_definition())
        assert converged.disposition is (
            SmoothBlochContinuumConvergenceDisposition.CONVERGED
        )
        assert len(converged.mesh_results) == 3
        assert len(converged.refinements) == 2
        assert not converged.refinements[0].within_tolerances
        assert converged.refinements[-1].within_tolerances

        strict = action.execute(
            self.convergence_definition(maximum_correlation_change=1.0e-18)
        )
        assert strict.disposition is (
            SmoothBlochContinuumConvergenceDisposition.UNRESOLVED
        )
        assert not strict.refinements[-1].within_tolerances

        base = self.convergence_definition()
        near_threshold = replace(
            base,
            thresholds=replace(
                base.thresholds,
                maximum_correlation_change=(
                    converged.refinements[-1].maximum_correlation_change
                    + 0.5 * base.verification_absolute_tolerance
                ),
            ),
        )
        near = action.execute(near_threshold)
        assert near.disposition is (
            SmoothBlochContinuumConvergenceDisposition.UNRESOLVED
        )

    def test_convergence_verifier_rejects_refinement_tampering(self) -> None:
        """Reconstruct each mesh and every disposition-driving refinement metric."""
        result = SmoothBlochContinuumConvergenceExperiment().execute(
            self.convergence_definition()
        )
        verifier = SmoothBlochContinuumConvergenceVerifier()
        verification = verifier.execute(result)
        assert verification.passes
        assert verification.maximum_refinement_absolute_defect < 2.0e-15

        refinement = result.refinements[-1]
        tampered_refinement = replace(
            refinement,
            maximum_correlation_change=(refinement.maximum_correlation_change + 1.0e-4),
        )
        tampered = SmoothBlochContinuumConvergenceResult(
            result.definition,
            result.mesh_results,
            (*result.refinements[:-1], tampered_refinement),
            result.disposition,
        )
        tampered_verification = verifier.execute(tampered)
        assert not tampered_verification.passes
        assert tampered_verification.maximum_refinement_absolute_defect == (
            pytest.approx(1.0e-4, rel=0.0, abs=1.0e-15)
        )

    def test_serialization_is_strict_canonical_and_contains_no_angle_inventory(
        self,
    ) -> None:
        """Validate strict schemas, digest bindings, and continuous-only alignment."""
        result = SmoothBlochContinuumConvergenceExperiment().execute(
            self.convergence_definition()
        )
        verification = SmoothBlochContinuumConvergenceVerifier().execute(result)
        input_wire = SmoothBlochContinuumInputSerializer().serialize(result.definition)
        result_wire = SmoothBlochContinuumResultSerializer().serialize(result)
        verification_wire = SmoothBlochContinuumVerificationSerializer().serialize(
            verification
        )
        schema_documents = self.schema_documents()
        records = (
            (
                input_wire,
                schema_documents.joinpath("smooth-continuum-input.schema.json"),
            ),
            (
                result_wire,
                schema_documents.joinpath("smooth-continuum-result.schema.json"),
            ),
            (
                verification_wire,
                schema_documents.joinpath("smooth-continuum-verification.schema.json"),
            ),
        )
        documents: list[dict[str, JsonValue]] = []
        for wire, schema_path in records:
            document_value: JsonValue = json.loads(wire)
            document = self.mapping(document_value, "serialized document")
            documents.append(document)
            assert canonical_json_bytes(document) == wire
            schema_value: JsonValue = json.loads(
                schema_path.read_text(encoding="utf-8")
            )
            schema = self.mapping(schema_value, "schema")
            Draft202012Validator.check_schema(schema)
            validator = Draft202012Validator(schema)
            assert validator.is_valid(document)
            changed_value: JsonValue = json.loads(json.dumps(document))
            changed = self.mapping(changed_value, "unknown-field document")
            changed["unknown"] = True
            assert not validator.is_valid(changed)
            identity_value: JsonValue = json.loads(json.dumps(document))
            identity_changed = self.mapping(identity_value, "identity document")
            identity = self.mapping(identity_changed["identity"], "identity")
            identity["method_id"] = f"{identity['method_id']}.tampered"
            assert not validator.is_valid(identity_changed)
        encoded_text = b"".join((input_wire, result_wire, verification_wire))
        assert b"alignment_angles" not in encoded_text
        assert b"finite_angle" not in encoded_text
        input_binding = self.mapping(documents[1]["input_binding"], "input binding")
        result_binding = self.mapping(documents[2]["result_binding"], "result binding")
        assert input_binding["sha256"] == hashlib.sha256(input_wire).hexdigest()
        assert result_binding["sha256"] == hashlib.sha256(result_wire).hexdigest()

    def test_verifier_reconstructs_and_rejects_tampering(self) -> None:
        """Independently reconstruct every channel and expose correlated tampering."""
        result = SmoothBlochContinuumExperiment().execute(self.definition())
        verifier = SmoothBlochContinuumVerifier()
        verification = verifier.execute(result)
        assert verification.passes
        assert verification.maximum_absolute_defect < 2.0e-15

        point = result.points[-1]
        tampered_analytic = point.analytic_maximum_correlation + 1.0e-4
        tampered_point = replace(
            point,
            analytic_maximum_correlation=tampered_analytic,
            correlation_quadrature_defect=abs(
                point.discrete_maximum_correlation - tampered_analytic
            ),
        )
        tampered = SmoothBlochContinuumResult(
            result.definition,
            (*result.points[:-1], tampered_point),
        )
        tampered_verification = verifier.execute(tampered)
        assert not tampered_verification.passes
        assert tampered_verification.maximum_absolute_defect == pytest.approx(
            1.0e-4, rel=0.0, abs=1.0e-15
        )
