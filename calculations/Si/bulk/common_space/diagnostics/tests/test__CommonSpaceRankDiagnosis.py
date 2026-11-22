"""Tests for the calculation-owned CSD0/CSD1 diagnostic implementation."""

from __future__ import annotations

import hashlib
import importlib.util
import io
import itertools
import json
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import common_space.diagnostics.diagnosis as producer
import common_space.verification.tests.test__CommonSpaceNativeOverlapReconstruction as native_fixture
import numpy as np
import pytest
from common_space.diagnostics import (
    DEFAULT_REQUEST,
    CommonSpaceRankDiagnosis,
    HumanReadableProgressReporter,
    NativePrecisionDefinition,
    atomic_to_projection_transform,
    gamma_grid,
    read_request,
    singular_value_uncertainty_bound,
)
from common_space.diagnostics.diagnosis import (
    FileSourceDeclaration,
    authenticate_file,
    authenticate_provider,
    reconstruct_rank_gate,
    validate_retained_source_contract,
)
from common_space.verification import (
    CommonSpaceDeficientDirectionAnalysis,
    CommonSpaceDirectionOutcome,
    CommonSpaceNativeOverlapReconstruction,
    CommonSpaceNativePrecisionAssessment,
    CommonSpaceNativeRoundingModel,
)


class TestCommonSpaceRankDiagnosis:
    """Keep the diagnostic explicit, fail-closed, and operator-readable."""

    def test__package__owns_the_diagnostic_without_a_flat_compatibility_module(
        self,
    ) -> None:
        package = importlib.util.find_spec("common_space.diagnostics")

        assert package is not None
        assert package.origin is not None
        assert Path(package.origin).parent.name == "diagnostics"
        assert importlib.util.find_spec("common_space_diagnosis") is None

    def test__request__binds_rank_ten_without_authorizing_fit_or_calculators(
        self,
    ) -> None:
        request = read_request(path=DEFAULT_REQUEST)

        assert request.state_space.retained_rank == 10
        assert request.state_space.basis_order == (
            "diamond_origin_center:s",
            "diamond_origin_center:px",
            "diamond_origin_center:py",
            "diamond_origin_center:pz",
            "diamond_origin_center:s-star",
            "diamond_body_diagonal_quarter_center:s",
            "diamond_body_diagonal_quarter_center:px",
            "diamond_body_diagonal_quarter_center:py",
            "diamond_body_diagonal_quarter_center:pz",
            "diamond_body_diagonal_quarter_center:s-star",
        )
        assert request.retained_comparison.deficient_indices == (0, 12)
        assert "no-retained-execution-authority" in request.status
        assert tuple(module.module_name for module in request.provider_modules) == (
            "projectkoios.integrations.wannier90",
            "projectkoios.integrations.wannier90._matrix_conventions",
            "projectkoios.integrations.wannier90._parsing",
            "projectkoios.integrations.wannier90.interface_data",
            "projectkoios.integrations.wannier90.unitary_matrices",
            "projectkoios.integrations.wannier90.disentanglement_matrices",
        )

    def test__request__rejects_a_changed_stage_inventory(self, tmp_path: Path) -> None:
        payload = json.loads(DEFAULT_REQUEST.read_text(encoding="utf-8"))
        payload["stages"] = ["CSD1"]
        request_path = tmp_path / "request.json"
        request_path.write_text(json.dumps(payload), encoding="utf-8")

        with pytest.raises(ValueError, match="stages must be exactly"):
            read_request(path=request_path)

    def test__repository_source__rejects_parent_path_escape(self) -> None:
        source = FileSourceDeclaration(
            label="escape",
            location="repository",
            declared_path="../outside.json",
            byte_size=0,
            sha256="0" * 64,
        )

        with pytest.raises(ValueError, match="escapes its owner"):
            source.resolve()

    def test__repository_sources__retain_the_declared_byte_identities(self) -> None:
        request = read_request(path=DEFAULT_REQUEST)
        reporter = HumanReadableProgressReporter(stream=io.StringIO())

        identities = tuple(
            authenticate_file(source, reporter)
            for source in request.file_sources
            if source.location == "repository"
        )

        assert tuple(identity.label for identity in identities) == (
            "S30_untruncated_characterization",
            "S105_full_support_disposition",
            "S110_blocked_result",
            "hopping_first_protocol",
        )

    def test__provider_sources__retain_the_declared_byte_identities(self) -> None:
        request = read_request(path=DEFAULT_REQUEST)
        reporter = HumanReadableProgressReporter(stream=io.StringIO())

        identities = authenticate_provider(request, reporter)

        assert len(identities) == 6

    def test__provider_sources__rejects_a_changed_digest(self) -> None:
        request = read_request(path=DEFAULT_REQUEST)
        request = replace(
            request,
            provider_modules=(
                replace(request.provider_modules[0], sha256="0" * 64),
                *request.provider_modules[1:],
            ),
        )
        reporter = HumanReadableProgressReporter(stream=io.StringIO())

        with pytest.raises(RuntimeError, match="provider module SHA-256 differs"):
            authenticate_provider(request, reporter)

    def test__retained_contract__matches_authenticated_repository_results(self) -> None:
        request = read_request(path=DEFAULT_REQUEST)
        retained_labels = {
            "S30_untruncated_characterization",
            "S105_full_support_disposition",
            "S110_blocked_result",
        }
        source_paths = {
            source.label: source.resolve()
            for source in request.file_sources
            if source.label in retained_labels
        }

        validate_retained_source_contract(
            request=request,
            source_paths=source_paths,
        )

    def test__native_parser_boundary__rejects_a_different_trial_count(
        self, tmp_path: Path
    ) -> None:
        """Parse synthetic native bytes, then stop before rank reconstruction."""
        request = read_request(path=DEFAULT_REQUEST)
        points = tuple(itertools.product(range(6), repeat=3))
        payloads = {
            "AMN": (
                "Synthetic parser-boundary fixture; not silicon evidence.\n"
                "20 216 1\n"
                + "".join(
                    f"{band} 1 {index} {int(band == 1)}.0 0.0\n"
                    for index in range(1, 217)
                    for band in range(1, 21)
                )
            ).encode("utf-8")
        }
        for label, rows in (("gauge", 10), ("disentanglement", 20)):
            matrix = "".join(
                f"{int(row == column)}.0 0.0\n"
                for column in range(10)
                for row in range(rows)
            )
            payloads[label] = (
                "Synthetic parser-boundary fixture; not silicon evidence.\n"
                f"216 10 {rows}\n"
                + "".join(
                    f"\n{x / 6:.16f} {y / 6:.16f} {z / 6:.16f}\n{matrix}"
                    for x, y, z in points
                )
            ).encode("utf-8")
        native_sources: dict[str, FileSourceDeclaration] = {}
        reporter = HumanReadableProgressReporter(stream=io.StringIO())
        for label, payload in payloads.items():
            path = tmp_path / label
            path.write_bytes(payload)
            source = FileSourceDeclaration(
                label=label,
                location="absolute",
                declared_path=str(path),
                byte_size=len(payload),
                sha256=hashlib.sha256(payload).hexdigest(),
            )
            authenticate_file(source, reporter)
            native_sources[label] = source
        request = replace(
            request,
            file_sources=tuple(
                native_sources.get(source.label, source)
                for source in request.file_sources
            ),
        )

        with pytest.raises(RuntimeError, match="parsed artifact dimensions differ"):
            reconstruct_rank_gate(request, reporter)

        assert "Computing raw overlap singular values" not in reporter.transcript()

    def test__reconstruction__retains_distinct_non_gamma_direction_weights(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Run producer arithmetic on synthetic bytes; upstream review is tested separately."""
        points = tuple(
            (x / 6, y / 6, z / 6) for x, y, z in itertools.product(range(6), repeat=3)
        )
        loader, _ = native_fixture.TestCommonSpaceNativeOverlapReconstruction._fixture(
            points=points,
            bands=20,
            constant_target=True,
            deficient_indices=(0, 12),
            mixed_direction_indices=(12,),
            # Synthetic amplitude chosen to exercise the unchanged frozen gate.
            outside_frame_amplitude=complex(2.944603369441934),
        )
        request = read_request(path=DEFAULT_REQUEST)
        sources: dict[str, FileSourceDeclaration] = {}
        for label, artifact in zip(
            ("AMN", "gauge", "disentanglement"), loader.artifacts, strict=True
        ):
            path = tmp_path / artifact.name
            path.write_bytes(artifact.payload)
            sources[label] = FileSourceDeclaration(
                label=label,
                location="absolute",
                declared_path=str(path),
                byte_size=artifact.identity.byte_count,
                sha256=artifact.identity.sha256,
            )
        request = replace(
            request,
            status="synthetic-software-test-only",
            file_sources=tuple(
                sources.get(item.label, item) for item in request.file_sources
            ),
            retained_comparison=replace(
                request.retained_comparison,
                deficient_indices=(0, 12),
                minimum_singular_values=(0.0, 0.0),
                gamma_atomic_orbital_weights=tuple(
                    (label, float(index == 9))
                    for index, label in enumerate(request.state_space.basis_order)
                ),
            ),
        )

        def reviewed_elsewhere(
            *,
            request: producer.CommonSpaceDiagnosisRequest,
            source_paths: dict[str, Path],
        ) -> None:
            assert request.status == "synthetic-software-test-only"
            assert all(source_paths[label].parent == tmp_path for label in sources)

        monkeypatch.setattr(
            producer, "validate_retained_source_contract", reviewed_elsewhere
        )
        result = reconstruct_rank_gate(
            request, HumanReadableProgressReporter(stream=io.StringIO())
        )
        table = result["complete_kpoint_diagnostics"]
        assert type(table) is list and len(table) == 216
        gamma, second, full = table[0], table[12], table[1]
        assert type(gamma) is dict and type(second) is dict and type(full) is dict
        expected_gamma = [0.0] * 9 + [1.0]
        expected_second = [0.25 if i in (0, 4, 5, 9) else 0.0 for i in range(10)]

        def numeric_weights(value: producer.JsonValue) -> tuple[float, ...]:
            assert type(value) is list
            numbers: list[float] = []
            for item in value:
                assert type(item) is float
                numbers.append(item)
            return tuple(numbers)

        np.testing.assert_allclose(
            np.asarray(
                numeric_weights(gamma["minimum_direction_atomic_weights"]),
                dtype=np.float64,
            ),
            np.asarray(expected_gamma, dtype=np.float64),
            atol=2e-14,
            rtol=0,
        )
        np.testing.assert_allclose(
            np.asarray(
                numeric_weights(second["minimum_direction_atomic_weights"]),
                dtype=np.float64,
            ),
            np.asarray(expected_second, dtype=np.float64),
            atol=2e-14,
            rtol=0,
        )
        np.testing.assert_allclose(
            np.asarray(
                numeric_weights(second["minimum_direction_group_weights_s_p_s_star"]),
                dtype=np.float64,
            ),
            np.asarray([0.5, 0.0, 0.5], dtype=np.float64),
            atol=2e-14,
            rtol=0,
        )
        assert full["minimum_direction_atomic_weights"] == []
        assert full["minimum_direction_group_weights_s_p_s_star"] == []
        assert (
            result["singular_value_native_uncertainty_bound"]
            == request.retained_comparison.native_uncertainty_bound
        )
        old_gamma = result["gamma_null_direction_atomic_orbital_weights"]
        assert type(old_gamma) is dict
        assert [old_gamma[label] for label in request.state_space.basis_order] == gamma[
            "minimum_direction_atomic_weights"
        ]
        deficient = result["deficient_kpoints"]
        assert type(deficient) is list
        assert deficient == [gamma, second]
        assert result["producer_scope"] == "projector-rank-reconstruction-subset"
        assert result["unimplemented_CSD1_extensions"] == [
            "integration with independent verification of this producer result",
            "symmetry-related deficient-point inventory",
        ]
        # Cross-route software check on the SAME synthetic native bytes. No source
        # review or completion declaration is manufactured by this selected-point test.
        parsed = loader.execute()
        for index in (0, 12, 1):
            row = table[index]
            assert type(row) is dict
            overlap = CommonSpaceNativeOverlapReconstruction(
                parsed_inputs=parsed, ordered_index=index
            ).execute()
            assessment = CommonSpaceNativePrecisionAssessment(
                overlap=overlap,
                rounding_model=CommonSpaceNativeRoundingModel.from_nearest_decimal_places(
                    amn=request.native_precision.amn_decimal_places,
                    gauge=request.native_precision.gauge_decimal_places,
                    disentanglement=request.native_precision.disentanglement_decimal_places,
                ),
                frozen_rank_threshold=Fraction.from_float(
                    request.retained_comparison.native_uncertainty_bound
                ),
            ).execute()
            assert assessment.resolved_rank == row["resolved_rank_at_native_bound"]
            direction = CommonSpaceDeficientDirectionAnalysis(
                assessment=assessment
            ).execute()
            weights = numeric_weights(row["minimum_direction_atomic_weights"])
            if index == 1:
                assert direction.outcome is CommonSpaceDirectionOutcome.full_rank
                assert weights == ()
            else:
                assert direction.outcome is CommonSpaceDirectionOutcome.enclosed
                for interval, value in zip(
                    direction.orbital_intervals, weights, strict=True
                ):
                    assert (
                        interval.lower <= Fraction.from_float(value) <= interval.upper
                    )
                grouped = numeric_weights(
                    row["minimum_direction_group_weights_s_p_s_star"]
                )
                for interval, value in zip(
                    direction.group_intervals, grouped, strict=True
                ):
                    assert (
                        interval.lower <= Fraction.from_float(value) <= interval.upper
                    )

    def test__continuation__requires_independent_verification_before_symmetry(
        self,
    ) -> None:
        assert CommonSpaceRankDiagnosis.NEXT_CONTROLLED_STEPS == (
            "CSD1-V: independently verify the complete producer result; higher precision remains conditional on arithmetic ambiguity or independent-route disagreement.",
            "CSD2 remains blocked until complete CSD1 and independent CSD1-V pass.",
        )

    def test__execute__requires_a_fresh_output_root(self, tmp_path: Path) -> None:
        output_root = tmp_path / "existing"
        output_root.mkdir()
        reporter = HumanReadableProgressReporter(stream=io.StringIO())

        with pytest.raises(FileExistsError, match="fresh output root already exists"):
            CommonSpaceRankDiagnosis().execute(
                request_path=DEFAULT_REQUEST,
                output_root=output_root,
                reporter=reporter,
            )

    def test__atomic_transform__is_exactly_unitary_in_the_declared_basis(self) -> None:
        transform = atomic_to_projection_transform()

        np.testing.assert_array_equal(
            transform.conj().T @ transform,
            np.eye(10, dtype=np.complex128),
        )
        with pytest.raises(ValueError):
            transform[0, 0] = 0.0

    def test__native_bound__reproduces_the_frozen_uncertainty_value(self) -> None:
        observed = singular_value_uncertainty_bound(
            maximum_amn=2.944603369441934,
            parent_band_count=20,
            retained_rank=10,
            precision=NativePrecisionDefinition(
                amn_decimal_places=12,
                gauge_decimal_places=10,
                disentanglement_decimal_places=10,
            ),
        )

        assert observed == pytest.approx(5.890206739032098e-7, abs=1.0e-22)
        with pytest.raises(ValueError, match="maximum_amn"):
            singular_value_uncertainty_bound(
                maximum_amn=True,
                parent_band_count=20,
                retained_rank=10,
                precision=NativePrecisionDefinition(
                    amn_decimal_places=12,
                    gauge_decimal_places=10,
                    disentanglement_decimal_places=10,
                ),
            )

    def test__gamma_grid__preserves_the_declared_lexicographic_order(self) -> None:
        grid = gamma_grid(6)

        assert grid.shape == (216, 3)
        np.testing.assert_array_equal(grid[0], (0.0, 0.0, 0.0))
        np.testing.assert_allclose(grid[12], (0.0, 1.0 / 3.0, 0.0))
        np.testing.assert_allclose(grid[-1], (5.0 / 6.0, 5.0 / 6.0, 5.0 / 6.0))

    def test__reporter__emits_immediate_human_readable_stage_status(self) -> None:
        stream = io.StringIO()
        reporter = HumanReadableProgressReporter(stream=stream)

        reporter.heading("Common-space diagnosis")
        reporter.stage("CSD1", "Reconstruct the rank gate")
        reporter.line("  Execution outcome: COMPLETED")
        reporter.line("  Scientific disposition: BLOCKED")

        expected = (
            "Common-space diagnosis\n"
            "======================\n"
            "\n"
            "[CSD1] Reconstruct the rank gate\n"
            "  Execution outcome: COMPLETED\n"
            "  Scientific disposition: BLOCKED\n"
        )
        assert stream.getvalue() == expected
        assert reporter.transcript() == expected
