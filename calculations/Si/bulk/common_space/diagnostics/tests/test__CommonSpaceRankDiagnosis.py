"""Tests for the calculation-owned CSD0/CSD1 diagnostic implementation."""

from __future__ import annotations

import importlib.util
import io
import json
from pathlib import Path

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
    validate_retained_source_contract,
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
