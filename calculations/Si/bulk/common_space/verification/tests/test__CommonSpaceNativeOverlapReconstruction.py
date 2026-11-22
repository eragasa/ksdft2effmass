"""Synthetic native-byte composition checks; no retained silicon data are opened."""

from __future__ import annotations

import hashlib
import importlib
from dataclasses import FrozenInstanceError, replace
from fractions import Fraction
from importlib.metadata import version
from math import nextafter
from pathlib import Path

import numpy as np
import pytest
from common_space.verification.gram_rank import GramRankDisposition
from common_space.verification.native_inputs import (
    CommonSpaceNativeInputContract,
    CommonSpaceNativeInputLoader,
    CommonSpaceProviderBinding,
    CommonSpaceProviderModuleIdentity,
    CommonSpaceTrialConvention,
)
from common_space.verification.native_overlap import (
    CommonSpaceNativeOverlapReconstruction,
)
from common_space.verification.native_precision import (
    CommonSpaceNativePrecisionAssessment,
    CommonSpaceNativeRoundingModel,
)
from projectkoios.integrations.wannier90 import (
    Wannier90NativeArtifact,
    Wannier90TrialOrbitalOverlapParser,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestCommonSpaceNativeOverlapReconstruction:
    """Keep byte correlation, parsed state labels, and exact products explicit."""

    @staticmethod
    def _provider_binding() -> CommonSpaceProviderBinding:
        # Synthetic test declarations only, not a production source-admission policy.
        modules: list[CommonSpaceProviderModuleIdentity] = []
        for name in CommonSpaceProviderBinding.REQUIRED_MODULES:
            module = importlib.import_module(name)
            assert module.__file__ is not None
            modules.append(
                CommonSpaceProviderModuleIdentity(
                    module_name=name,
                    sha256=hashlib.sha256(
                        Path(module.__file__).read_bytes()
                    ).hexdigest(),
                )
            )
        return CommonSpaceProviderBinding(
            distribution_version=version("projectkoios-simulations"),
            modules=tuple(modules),
        )

    @classmethod
    def _fixture(
        cls,
        *,
        trial_count: int = 10,
        native_frame_scale: float = 1.0,
        points: tuple[tuple[float, float, float], ...] | None = None,
        bands: int = 12,
        constant_target: bool = False,
        mix_atomic_direction: bool = False,
        mixed_direction_indices: tuple[int, ...] = (),
        outside_frame_amplitude: complex = 7 - 2j,
        deficient_indices: tuple[int, ...] | None = None,
        gauge_points: tuple[tuple[float, float, float], ...] | None = None,
        disentanglement_points: tuple[tuple[float, float, float], ...] | None = None,
    ) -> tuple[
        CommonSpaceNativeInputLoader,
        tuple[tuple[tuple[complex, ...], ...], ...],
    ]:
        points = ((0.0, 0.0, 0.0), (0.25, 0.0, 0.0)) if points is None else points
        gauge_points = points if gauge_points is None else gauge_points
        disentanglement_points = (
            points if disentanglement_points is None else disentanglement_points
        )
        # Independent test oracle: the declared native hybrid coefficient table.
        hybrids = (
            np.asarray(
                ((1, 1, 1, 1), (1, 1, -1, -1), (1, -1, 1, -1), (1, -1, -1, 1)),
                dtype=np.complex128,
            )
            / 2
        )
        transform = np.zeros((10, 10), dtype=np.complex128)
        transform[:4, :4] = hybrids
        transform[5:9, 4:8] = hybrids
        transform[4, 8] = transform[9, 9] = 1
        gauge = np.zeros((10, 10), dtype=np.complex128)
        disentanglement = np.zeros((bands, 10), dtype=np.complex128)
        for column in range(10):
            gauge[9 - column, column] = (1j, -1, 1, -1j)[column % 4]
            disentanglement[bands - 1 - column, column] = (1, -1j, -1, 1j)[column % 4]
        targets: list[tuple[tuple[complex, ...], ...]] = []
        amn_lines = [
            "Synthetic AMN; not silicon evidence.",
            f"{bands} {len(points)} {trial_count}",
        ]
        gauge_lines = ["Synthetic gauge; not silicon evidence.", f"{len(points)} 10 10"]
        dis_lines = [
            "Synthetic disentanglement; not silicon evidence.",
            f"{len(points)} 10 {bands}",
        ]
        for index in range(len(points)):
            target = np.eye(10, dtype=np.complex128) * (
                1 if constant_target else index + 1
            )
            if deficient_indices is None or index in deficient_indices:
                target[9, 9] = 0
            target[0, 1] = 0.25 + 0.5j
            target[3, 6] = -0.125j
            target[8, 2] = 0.375j
            if mix_atomic_direction or index in mixed_direction_indices:
                right_rotation = np.eye(10, dtype=np.complex128)
                indices = (0, 4, 5, 9)
                right_rotation[np.ix_(indices, indices)] = hybrids
                target = target @ right_rotation
            targets.append(
                tuple(tuple(complex(value) for value in row) for row in target)
            )
            amn = disentanglement @ gauge @ target @ transform
            # Parent-band directions outside the retained isometry must disappear.
            amn[: bands - 10, :] = outside_frame_amplitude
            amn_lines.extend(
                f"{band + 1} {trial + 1} {index + 1} {amn[band, trial].real:.17g} {amn[band, trial].imag:.17g}"
                for trial in range(trial_count)
                for band in range(bands)
            )
            for lines, matrix, coordinates in (
                (gauge_lines, gauge * native_frame_scale, gauge_points),
                (
                    dis_lines,
                    disentanglement * native_frame_scale,
                    disentanglement_points,
                ),
            ):
                lines.append(
                    " ".join(f"{coordinate:.17g}" for coordinate in coordinates[index])
                )
                lines.extend(
                    f"{matrix[row, column].real:.17g} {matrix[row, column].imag:.17g}"
                    for column in range(matrix.shape[1])
                    for row in range(matrix.shape[0])
                )
        artifacts = tuple(
            Wannier90NativeArtifact(name, ("\n".join(lines) + "\n").encode("utf-8"))
            for name, lines in (
                ("synthetic.amn", amn_lines),
                ("synthetic_u.mat", gauge_lines),
                ("synthetic_u_dis.mat", dis_lines),
            )
        )
        contract = CommonSpaceNativeInputContract(
            trial_overlap_identity=artifacts[0].identity,
            gauge_identity=artifacts[1].identity,
            disentanglement_identity=artifacts[2].identity,
            ordered_fractional_kpoints=points,
            parent_band_count=bands,
            atomic_basis_order=CommonSpaceNativeInputContract.ATOMIC_BASIS_ORDER,
            trial_convention=CommonSpaceTrialConvention.two_center_sp3s_star,
            geometry_identity="Synthetic two-center geometry, not retained silicon",
            energy_reference_identity="Synthetic energy reference, not a parent alignment",
        )
        return CommonSpaceNativeInputLoader(
            contract=contract,
            provider_binding=cls._provider_binding(),
            artifacts=artifacts,
        ), tuple(targets)

    def test_native_parsing__retains_exact_identity_and_state_receipts(self) -> None:
        loader, _ = self._fixture()

        parsed = loader.execute()

        assert (
            parsed.source_correlation.expected_identities == loader.contract.identities
        )
        assert (
            parsed.source_correlation.observed_identities == loader.contract.identities
        )
        assert parsed.provider_binding == loader.provider_binding
        assert parsed.contract is loader.contract
        assert parsed.trial_overlaps.band_count == 12
        assert parsed.disentanglement.wannier_count == 10

    @pytest.mark.numerical_verification
    @pytest.mark.parametrize("index", (0, 1))
    def test_reconstruction__matches_known_complex_overlap_in_atomic_order(
        self, index: int
    ) -> None:
        loader, targets = self._fixture()
        parsed = loader.execute()

        overlap = CommonSpaceNativeOverlapReconstruction(
            parsed_inputs=parsed, ordered_index=index
        ).execute()

        assert (
            overlap.fractional_kpoint
            == loader.contract.ordered_fractional_kpoints[index]
        )
        assert overlap.atomic_basis_order == loader.contract.atomic_basis_order
        for row in range(10):
            for column in range(10):
                expected = targets[index][row][column]
                assert overlap.entry(row=row, column=column) == (
                    Fraction.from_float(expected.real),
                    Fraction.from_float(expected.imag),
                )
        result = overlap.enclose_rank(rank_threshold=Fraction(1, 100))
        assert result.disposition is GramRankDisposition.rank_resolved
        assert result.resolved_rank == 9

    @pytest.mark.numerical_verification
    def test_reconstruction__does_not_round_an_unrepresentable_binary64_product(
        self,
    ) -> None:
        # Deliberately non-isometric synthetic frames test arithmetic, not a physical source.
        scale = 1.0 + 2.0**-52
        loader, _ = self._fixture(native_frame_scale=scale)
        overlap = CommonSpaceNativeOverlapReconstruction(
            parsed_inputs=loader.execute(), ordered_index=0
        ).execute()
        expected = Fraction.from_float(scale) ** 2

        assert overlap.entry(row=0, column=0) == (expected, Fraction(0))
        assert expected != Fraction.from_float(float(expected))
        assert overlap.enclose_rank(rank_threshold=Fraction(1, 100)).resolved_rank == 9

    def test_native_precision__keeps_error_channels_and_frozen_gate_separate(
        self,
    ) -> None:
        loader, _ = self._fixture()
        overlap = CommonSpaceNativeOverlapReconstruction(
            parsed_inputs=loader.execute(), ordered_index=0
        ).execute()
        threshold = Fraction.from_float(5.890206739032098e-7)
        model = CommonSpaceNativeRoundingModel.from_nearest_decimal_places(
            amn=12, gauge=10, disentanglement=10
        )
        result = CommonSpaceNativePrecisionAssessment(
            overlap=overlap, rounding_model=model, frozen_rank_threshold=threshold
        ).execute()

        assert result.uncertainty_bound_covered
        assert result.coverage_margin >= 0
        assert result.resolved_rank == 9
        assert result.frozen_rank_threshold == threshold
        assert result.arithmetic == overlap.enclose_rank(rank_threshold=threshold)
        assert (
            0
            < result.uncertainty.parsing_error_bound
            < result.uncertainty.native_error_bound
        )
        assert result.uncertainty.combined_error_bound == (
            result.uncertainty.parsing_error_bound
            + result.uncertainty.native_error_bound
        )

    def test_uncovered_uncertainty_bound__cannot_promote_resolved_arithmetic(
        self,
    ) -> None:
        loader, _ = self._fixture()
        overlap = CommonSpaceNativeOverlapReconstruction(
            parsed_inputs=loader.execute(), ordered_index=0
        ).execute()
        model = CommonSpaceNativeRoundingModel.from_nearest_decimal_places(
            amn=0, gauge=0, disentanglement=0
        )
        result = CommonSpaceNativePrecisionAssessment(
            overlap=overlap, rounding_model=model, frozen_rank_threshold=Fraction(1, 10)
        ).execute()

        assert result.arithmetic.resolved_rank == 9
        assert result.frozen_rank_threshold == Fraction(1, 10)
        assert not result.uncertainty_bound_covered
        assert result.coverage_margin < 0
        assert result.resolved_rank is None
        assert result.disposition is GramRankDisposition.numerically_inconclusive
        # Synthetic boundary exercise only; not production threshold selection.
        boundary = replace(
            result,
            arithmetic=replace(
                result.arithmetic,
                rank_threshold=result.uncertainty.combined_error_bound,
            ),
        )
        assert boundary.uncertainty_bound_covered
        assert boundary.coverage_margin == 0

    def test_covered_uncertainty_bound__does_not_override_arithmetic_ambiguity(
        self,
    ) -> None:
        loader, _ = self._fixture()
        overlap = CommonSpaceNativeOverlapReconstruction(
            parsed_inputs=loader.execute(), ordered_index=0
        ).execute()
        # Synthetic zero native-quantization model; parsing error remains nonzero.
        model = CommonSpaceNativeRoundingModel(
            amn_component_error=Fraction(0),
            gauge_component_error=Fraction(0),
            disentanglement_component_error=Fraction(0),
        )
        result = CommonSpaceNativePrecisionAssessment(
            overlap=overlap,
            rounding_model=model,
            frozen_rank_threshold=Fraction(1, 10**10),
        ).execute()

        assert result.uncertainty_bound_covered
        assert result.arithmetic.resolved_rank is None
        assert result.resolved_rank is None
        assert result.disposition is GramRankDisposition.numerically_inconclusive

    @pytest.mark.parametrize("threshold", (True, "0", 0.0, Fraction(-1)))
    def test_precision_assessment_threshold__requires_nonnegative_exact_fraction(
        self, threshold: Fraction | str | float
    ) -> None:
        loader, _ = self._fixture()
        overlap = CommonSpaceNativeOverlapReconstruction(
            parsed_inputs=loader.execute(), ordered_index=0
        ).execute()
        model = CommonSpaceNativeRoundingModel.from_nearest_decimal_places(
            amn=12, gauge=10, disentanglement=10
        )
        with pytest.raises(ValueError, match="nonnegative built-in Fraction"):
            CommonSpaceNativePrecisionAssessment(
                overlap=overlap,
                rounding_model=model,
                frozen_rank_threshold=threshold,  # type: ignore[arg-type]
            )

    def test_all_byte_identities__are_checked_before_first_parser(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        loader, _ = self._fixture()
        tampered = replace(
            loader.artifacts[2], payload=loader.artifacts[2].payload + b"tamper"
        )
        loader = replace(loader, artifacts=(*loader.artifacts[:2], tampered))

        def forbidden_parse(_self: Wannier90TrialOrbitalOverlapParser) -> None:
            raise AssertionError("parser must not run before all byte identities pass")

        monkeypatch.setattr(
            Wannier90TrialOrbitalOverlapParser, "parse", forbidden_parse
        )
        with pytest.raises(ValueError, match="identities do not agree"):
            loader.execute()

    def test_provider_identity__is_checked_before_first_parser(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        loader, _ = self._fixture()
        modules = loader.provider_binding.modules
        binding = replace(
            loader.provider_binding,
            modules=(replace(modules[0], sha256="0" * 64), *modules[1:]),
        )

        def forbidden_parse(_self: Wannier90TrialOrbitalOverlapParser) -> None:
            raise AssertionError("parser must not run before provider sources pass")

        monkeypatch.setattr(
            Wannier90TrialOrbitalOverlapParser, "parse", forbidden_parse
        )
        with pytest.raises(RuntimeError, match="provider module SHA-256 differs"):
            replace(loader, provider_binding=binding).execute()

    def test_provider_version__has_no_source_only_fallback(self) -> None:
        loader, _ = self._fixture()
        with pytest.raises(RuntimeError, match="distribution version differs"):
            replace(
                loader,
                provider_binding=replace(
                    loader.provider_binding, distribution_version="wrong"
                ),
            ).execute()

    def test_provider_closure__requires_correlator_and_all_parser_sources(self) -> None:
        binding = self._provider_binding()
        with pytest.raises(ValueError, match="module closure"):
            replace(
                binding,
                modules=tuple(
                    module
                    for module in binding.modules
                    if not module.module_name.endswith(".artifacts")
                ),
            )
        with pytest.raises(ValueError, match="module closure"):
            replace(binding, modules=tuple(reversed(binding.modules)))
        with pytest.raises(ValueError, match="module closure"):
            replace(
                binding,
                modules=(
                    replace(binding.modules[0], module_name="common_space.diagnostics"),
                    *binding.modules[1:],
                ),
            )

    @pytest.mark.parametrize("inventory", ("missing", "duplicate", "extra"))
    def test_native_inventory__does_not_admit_an_alternative_source(
        self, inventory: str
    ) -> None:
        loader, _ = self._fixture()
        if inventory == "missing":
            artifacts = loader.artifacts[:-1]
        elif inventory == "duplicate":
            artifacts = (loader.artifacts[0], loader.artifacts[0], loader.artifacts[2])
        else:
            artifacts = (
                *loader.artifacts,
                Wannier90NativeArtifact("extra.amn", b"extra"),
            )
        with pytest.raises(ValueError, match="artifact name"):
            replace(loader, artifacts=artifacts).execute()

    def test_native_byte_count__is_required_in_addition_to_digest(self) -> None:
        loader, _ = self._fixture()
        identity = replace(
            loader.contract.trial_overlap_identity,
            byte_count=loader.contract.trial_overlap_identity.byte_count + 1,
        )
        with pytest.raises(ValueError, match="identities do not agree"):
            replace(
                loader,
                contract=replace(loader.contract, trial_overlap_identity=identity),
            ).execute()

    def test_authenticated_malformed_payload__has_no_alternate_parser(self) -> None:
        loader, _ = self._fixture()
        malformed = Wannier90NativeArtifact(loader.artifacts[0].name, b"malformed")
        with pytest.raises(ValueError):
            replace(
                loader,
                artifacts=(malformed, *loader.artifacts[1:]),
                contract=replace(
                    loader.contract, trial_overlap_identity=malformed.identity
                ),
            ).execute()

    def test_explicit_roles__are_not_repaired_from_native_dimensions(self) -> None:
        loader, _ = self._fixture()
        swapped = replace(
            loader.contract,
            gauge_identity=loader.contract.disentanglement_identity,
            disentanglement_identity=loader.contract.gauge_identity,
        )
        with pytest.raises(ValueError, match="square"):
            replace(loader, contract=swapped).execute()

    def test_trial_count__cannot_define_the_trial_convention(self) -> None:
        loader, _ = self._fixture(trial_count=9)
        with pytest.raises(ValueError, match="native dimensions differ"):
            loader.execute()

    def test_parent_band_count__must_match_declaration(self) -> None:
        loader, _ = self._fixture()
        with pytest.raises(ValueError, match="native dimensions differ"):
            replace(
                loader, contract=replace(loader.contract, parent_band_count=13)
            ).execute()

    @pytest.mark.parametrize(
        "kind", ("gauge-order", "disentanglement-order", "one-ulp", "periodic-image")
    )
    def test_point_identity__has_no_order_normalization_or_tolerance(
        self, kind: str
    ) -> None:
        points = ((0.0, 0.0, 0.0), (0.25, 0.0, 0.0))
        if kind == "gauge-order":
            loader, _ = self._fixture(gauge_points=tuple(reversed(points)))
        elif kind == "disentanglement-order":
            loader, _ = self._fixture(disentanglement_points=tuple(reversed(points)))
        elif kind == "one-ulp":
            loader, _ = self._fixture(
                gauge_points=(points[0], (nextafter(0.25, 1), 0.0, 0.0))
            )
        else:
            loader, _ = self._fixture(gauge_points=(points[0], (1.25, 0.0, 0.0)))
        with pytest.raises(ValueError, match="ordered k points differ"):
            loader.execute()

    def test_basis_order__must_be_explicit_even_when_dimensions_match(self) -> None:
        loader, _ = self._fixture()
        with pytest.raises(ValueError, match="atomic_basis_order differs"):
            replace(
                loader.contract,
                atomic_basis_order=tuple(reversed(loader.contract.atomic_basis_order)),
            )
        with pytest.raises(TypeError, match="CommonSpaceTrialConvention"):
            replace(
                loader.contract,
                trial_convention="sp3s-star",  # type: ignore[arg-type]
            )

    def test_convention__uses_closed_wire_vocabulary(self) -> None:
        convention = CommonSpaceTrialConvention.two_center_sp3s_star
        assert CommonSpaceTrialConvention.from_wire(convention.to_wire()) is convention
        with pytest.raises(ValueError, match="unsupported"):
            CommonSpaceTrialConvention.from_wire("guessed-from-rank-ten")

    def test_state_labels__cannot_be_empty(self) -> None:
        loader, _ = self._fixture()
        with pytest.raises(ValueError, match="geometry and energy-reference"):
            replace(loader.contract, geometry_identity="")
        with pytest.raises(ValueError, match="geometry and energy-reference"):
            replace(loader.contract, energy_reference_identity="")

    @pytest.mark.parametrize("index", (True, "0", -1, 2))
    def test_point_index__rejects_coercion_and_out_of_range_values(
        self, index: bool | str | int
    ) -> None:
        loader, _ = self._fixture()
        with pytest.raises(ValueError, match="ordered_index"):
            CommonSpaceNativeOverlapReconstruction(
                parsed_inputs=loader.execute(),
                ordered_index=index,  # type: ignore[arg-type]
            )

    def test_contract_storage__does_not_admit_mutable_coordinates(self) -> None:
        loader, _ = self._fixture()
        with pytest.raises(ValueError, match="nonempty tuple"):
            replace(
                loader.contract,
                ordered_fractional_kpoints=list(  # type: ignore[arg-type]
                    loader.contract.ordered_fractional_kpoints
                ),
            )
        with pytest.raises(ValueError, match="finite built-in floats"):
            replace(loader.contract, ordered_fractional_kpoints=((0, 0.0, 0.0),))
        with pytest.raises(ValueError, match="unique"):
            replace(loader.contract, ordered_fractional_kpoints=((0.0, 0.0, 0.0),) * 2)
        with pytest.raises(ValueError, match="at least ten"):
            replace(loader.contract, parent_band_count=True)

    def test_declared_roles__cannot_share_one_artifact_identity(self) -> None:
        loader, _ = self._fixture()
        with pytest.raises(ValueError, match="three distinct names"):
            replace(
                loader.contract, gauge_identity=loader.contract.trial_overlap_identity
            )

    def test_parsed_receipt__cannot_be_rebound_to_another_input(self) -> None:
        loader, _ = self._fixture()
        parsed = loader.execute()
        changed = replace(loader.contract.trial_overlap_identity, sha256="0" * 64)
        with pytest.raises(ValueError, match="receipt differs"):
            replace(
                parsed,
                contract=replace(loader.contract, trial_overlap_identity=changed),
            )

    def test_input_order__is_correlated_by_explicit_role_not_tuple_position(
        self,
    ) -> None:
        loader, _ = self._fixture()
        parsed = replace(loader, artifacts=tuple(reversed(loader.artifacts))).execute()
        overlap = CommonSpaceNativeOverlapReconstruction(
            parsed_inputs=parsed, ordered_index=0
        ).execute()
        assert overlap.entry(row=0, column=1) == (Fraction(1, 4), Fraction(1, 2))

    def test_records__retain_immutable_data_without_floating_B_conversion(self) -> None:
        loader, _ = self._fixture()
        overlap = CommonSpaceNativeOverlapReconstruction(
            parsed_inputs=loader.execute(), ordered_index=0
        ).execute()
        with pytest.raises(FrozenInstanceError):
            overlap.ordered_index = 1  # type: ignore[misc]
        with pytest.raises(FrozenInstanceError):
            loader.contract = replace(loader.contract, parent_band_count=13)  # type: ignore[misc]
        with pytest.raises(TypeError):
            overlap._matrix.rows[0][0] = overlap._matrix.rows[1][0]  # type: ignore[index]
        with pytest.raises(ValueError, match="entry indices"):
            overlap.entry(row=True, column=0)
        with pytest.raises(ValueError, match="entry indices"):
            overlap.entry(row=0, column=10)
        with pytest.raises(ValueError, match="nonnegative built-in Fraction"):
            overlap.enclose_rank(rank_threshold=True)  # type: ignore[arg-type]
