"""Exact geometric checks and synthetic ranks; not silicon numerical evidence."""

import io
from dataclasses import FrozenInstanceError, replace
from fractions import Fraction
from pathlib import Path

import pytest
from common_space.diagnostics.diagnosis import (
    DEFAULT_REQUEST,
    CommonSpaceRankDiagnosis,
    HumanReadableProgressReporter,
    KPointDiagnosis,
    read_request,
)
from common_space.diagnostics.point_inventory import (
    ADOPTED_GEOMETRY,
    DiamondConstructionPointInventory,
)
from common_space.diagnostics.source_association import AdoptedSiliconSourceAssociation


class TestDiamondConstructionPointInventory:
    """Exhaustive geometry does not authorize electronic symmetry conclusions."""

    @staticmethod
    def records() -> tuple[KPointDiagnosis, ...]:
        return tuple(
            KPointDiagnosis(
                ordered_index=i,
                fractional_coordinates=(
                    float(f"{(i // 36) / 6:.10f}"),
                    float(f"{(i // 6 % 6) / 6:.10f}"),
                    float(f"{(i % 6) / 6:.10f}"),
                ),
                resolved_rank=9 if i in (0, 12) else 10,
                maximum_singular_value=1.0,
                next_to_minimum_singular_value=0.5,
                minimum_singular_value=0.0 if i in (0, 12) else 0.1,
                condition_number=None if i in (0, 12) else 10.0,
                minimum_principal_cosine=0.1,
                maximum_principal_angle_radians=1.4706289056333368,
                full_rank_gate_passed=i not in (0, 12),
                minimum_direction_atomic_weights=(1.0, *([0.0] * 9))
                if i in (0, 12)
                else (),
            )
            for i in range(216)
        )

    def test__operations__form_the_48_element_diamond_affine_group(self) -> None:
        operations = DiamondConstructionPointInventory.operations()
        product = DiamondConstructionPointInventory._product
        group = {(m, (t, t, t)) for _r, m, _q, t in operations}
        assert len(group) == 48
        assert sum(t == 0 for _r, _m, _q, t in operations) == 24
        for _r, m, _q, t in operations:
            for _s, n, _p, u in operations:
                combined_translation = tuple((t + sum(row) * u) % 4 for row in m)
                assert (product(m, n), combined_translation) in group

    def test__inventory__partitions_every_index_and_reports_mixed_star_ranks(
        self,
    ) -> None:
        result = DiamondConstructionPointInventory(
            records=self.records(), geometry_identity=ADOPTED_GEOMETRY
        ).execute()
        assert result["operation_count"] == 48
        orbits = result["orbit_partition"]
        assert type(orbits) is list
        covered: list[int] = []
        for orbit in orbits:
            assert type(orbit) is list
            for index in orbit:
                assert type(index) is int
                covered.append(index)
        assert sorted(covered) == list(range(216))
        stars = result["deficient_point_stars"]
        assert type(stars) is list
        gamma, second = stars
        assert type(gamma) is dict and type(second) is dict
        assert gamma["related_indices"] == [0]
        # Independent Cartesian {(+/-1,+/-1,+/-1)} star in this primitive basis.
        assert second["related_indices"] == [2, 4, 12, 24, 72, 86, 144, 172]
        assert second["deficient_member_indices"] == [12]
        rows = second["point_diagnostics"]
        assert type(rows) is list and len(rows) == 8
        assert (
            sum(
                row["full_rank_gate_passed"] is True
                for row in rows
                if type(row) is dict
            )
            == 7
        )
        assert "physical symmetry breaking" in str(result["interpretation"])

    def test__presentation_residuals__are_exact_observations_not_zeroed(self) -> None:
        result = DiamondConstructionPointInventory(
            records=self.records(), geometry_identity=ADOPTED_GEOMETRY
        ).execute()
        operations = result["operations"]
        assert type(operations) is list
        residuals: list[Fraction] = []
        for row in operations:
            assert type(row) is dict
            encoded = row["maximum_printed_coordinate_component_residual"]
            assert type(encoded) is list
            top, bottom = encoded
            assert type(top) is str and type(bottom) is str
            residuals.append(Fraction(int(top, 16), int(bottom, 16)))
            permutation = row["point_permutation"]
            assert type(permutation) is list
            indices: list[int] = []
            for index in permutation:
                assert type(index) is int
                indices.append(index)
            assert sorted(indices) == list(range(216))
        assert min(residuals) == 0
        assert max(residuals) > 0

    def test__records__cannot_be_mutated_or_snapped(self) -> None:
        records = self.records()
        action = DiamondConstructionPointInventory(
            records=records, geometry_identity=ADOPTED_GEOMETRY
        )
        with pytest.raises(FrozenInstanceError):
            action.records = ()  # type: ignore[misc]
        changed = replace(records[1], fractional_coordinates=(0.0, 0.0, 1.0 / 6))
        with pytest.raises(ValueError, match="cannot snap"):
            DiamondConstructionPointInventory(
                records=(records[0], changed, *records[2:]),
                geometry_identity=ADOPTED_GEOMETRY,
            )
        with pytest.raises(ValueError, match="exact declared order"):
            DiamondConstructionPointInventory(
                records=(records[1], records[0], *records[2:]),
                geometry_identity=ADOPTED_GEOMETRY,
            )
        with pytest.raises(ValueError, match="all 216"):
            DiamondConstructionPointInventory(
                records=records[:-1], geometry_identity=ADOPTED_GEOMETRY
            )
        with pytest.raises(ValueError, match="adopted source geometry"):
            DiamondConstructionPointInventory(
                records=records, geometry_identity="unreviewed-nominal-cell"
            )

    def test__producer__requires_declaration_before_retained_reconstruction(
        self, tmp_path: Path
    ) -> None:
        with pytest.raises(ValueError, match="requires the adopted source declaration"):
            CommonSpaceRankDiagnosis().execute(
                request_path=DEFAULT_REQUEST,
                output_root=tmp_path / "absent",
                reporter=HumanReadableProgressReporter(stream=io.StringIO()),
            )
        assert not (tmp_path / "absent").exists()

    def test__declaration__rejects_changed_bytes_without_native_parsing(
        self, tmp_path: Path
    ) -> None:
        path = tmp_path / "unreviewed.json"
        path.write_text("{}")
        with pytest.raises(RuntimeError, match="byte size differs"):
            AdoptedSiliconSourceAssociation(declaration_path=path).execute(
                request=read_request(path=DEFAULT_REQUEST),
                request_path=DEFAULT_REQUEST,
                reporter=HumanReadableProgressReporter(stream=io.StringIO()),
            )

    def test__source_association__rejects_a_replaced_request(
        self, tmp_path: Path
    ) -> None:
        request = read_request(path=DEFAULT_REQUEST)
        with pytest.raises(ValueError, match="request differs"):
            AdoptedSiliconSourceAssociation(
                declaration_path=tmp_path / "never-read"
            ).execute(
                request=replace(request, status="synthetic-software-test-only"),
                request_path=DEFAULT_REQUEST,
                reporter=HumanReadableProgressReporter(stream=io.StringIO()),
            )
