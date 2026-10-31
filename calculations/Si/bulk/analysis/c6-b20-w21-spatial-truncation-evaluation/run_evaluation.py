from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import sys
from pathlib import Path
from types import ModuleType
from typing import Protocol, cast

import numpy as np
import projectkoios
from projectkoios.numerics.numpy.typing import (
    Complex128Array,
    Float64Array,
    Int64Array,
)
from scipy import constants  # type: ignore[import-untyped]

from ksdft2effmass.serialization import TypedJsonMappingSerializer

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]

ROOT = Path(__file__).resolve().parent
BULK = ROOT.parents[1]
PROTOCOL = BULK / "research-protocol/controlled-reduction-protocol.tex"
S30_ROOT = BULK / "analysis/c6-b20-w21-untruncated-characterization"
S30_IMPLEMENTATION = S30_ROOT / "run_analysis.py"
S30_RESULT = S30_ROOT / "characterization-result.json"
S90_ROOT = BULK / "analysis/c6-b20-w21-spatial-truncation-design"
S90_IMPLEMENTATION = S90_ROOT / "prepare_design.py"
S90_DESIGN = S90_ROOT / "truncation-design.json"
PROJECTKOIOS_PACKAGE = Path(
    "/Users/eugene/worktrees/"
    "projectkoios-simulations-pw-dft-wannierization-tranche-1/"
    "src/python/projectkoios"
)
PROJECTKOIOS_WANNIER90 = PROJECTKOIOS_PACKAGE / "integrations/wannier90"
PROJECTKOIOS_PARSER_SOURCES = {
    PROJECTKOIOS_WANNIER90 / "__init__.py": (
        "26f568e7446d2721983ec0e0a3e7131ba8c2e6442c88b91d92d81c4b296a36ad"
    ),
    PROJECTKOIOS_WANNIER90 / "_parsing.py": (
        "07de9ab225fbc7cfd5317f1592b5dcd0105d5eaec982d814980272cdd578439a"
    ),
    PROJECTKOIOS_WANNIER90 / "hamiltonian_blocks.py": (
        "ba1496692abd7b8edf627c6836535daeced5d80f95489b639af22637a545388d"
    ),
    PROJECTKOIOS_WANNIER90 / "interface_data.py": (
        "5b4033f5b99373eca5bd7ce1b492f52f3d16cad43945e0e2ddf845121193b078"
    ),
    PROJECTKOIOS_WANNIER90 / "unitary_matrices.py": (
        "33ebad1a82f887f0dd59787c066bded1989b6dd9b7220c3e551b0c5cb798e75f"
    ),
    PROJECTKOIOS_WANNIER90 / "disentanglement_matrices.py": (
        "64ede7d0e45b9d1b200026322f48d832fe7587b5b99c7eb292bfae2d7390fdd7"
    ),
}
OUTPUT = ROOT / "truncation-evaluation.json"
EXPECTED = {
    PROTOCOL: "80cf67acf00d6b906a64471ed06379a321bca71ed5b6636174c634a30d8b2380",
    S30_IMPLEMENTATION: (
        "985dcc7e000fdd0aea76e046f8cfbf8cf12b73990decdc2808be517fd50a538e"
    ),
    S30_RESULT: ("37f654ae31bc21e43b768bf2b9da5edabd88c195e3f6e1c87708eaa1c4773c18"),
    S90_IMPLEMENTATION: (
        "687ed568e392ea1c3ac333c543313cc57206d5a92903b7e3e015b5103224cc1d"
    ),
    S90_DESIGN: ("6b9863271ba8241881d62435a7c8307d3431ffe59bfdcce5d96525fe86fcb531"),
    **PROJECTKOIOS_PARSER_SOURCES,
}
ELECTRON_MASS_CURVATURE_EV_ANGSTROM2 = (
    constants.hbar**2 / constants.m_e / constants.electron_volt * 1.0e20
)


class FiniteOperator(Protocol):
    """Expose only finite-operator behavior used by S100."""

    @property
    def representatives(self) -> Int64Array: ...

    @property
    def blocks_ev(self) -> Complex128Array: ...

    @property
    def dimension(self) -> int: ...

    def matrices(self, kpoints: Float64Array) -> Complex128Array: ...

    def eigenvalues(
        self, kpoints: Float64Array, chunk_size: int = 2048
    ) -> Float64Array: ...

    def eigenvalue(self, kpoint: Float64Array, band_index: int) -> float: ...


class ValleyMinimum(Protocol):
    """Expose the retained minimum fields returned by the S30 analyzer."""

    @property
    def label(self) -> str: ...

    @property
    def fractional(self) -> Float64Array: ...

    @property
    def energy_ev(self) -> float: ...

    @property
    def optimizer_success(self) -> bool: ...

    @property
    def identity_matches(self) -> bool: ...


class LatticeProtocol(Protocol):
    """Expose reciprocal geometry used by the curvature calculation."""

    @property
    def reciprocal(self) -> ReciprocalProtocol: ...


class ReciprocalProtocol(Protocol):
    """Expose the primitive reciprocal-basis matrix."""

    @property
    def primitive_basis_matrix(self) -> Float64Array: ...


class GridProtocol(Protocol):
    """Expose a deterministic fractional reciprocal grid."""

    @property
    def points(self) -> Float64Array: ...


class SourceOperatorLoader:
    """Authenticate and reconstruct the exact S30 full operator."""

    __slots__ = ()

    def execute(self) -> tuple[ModuleType, FiniteOperator, LatticeProtocol]:
        source_package = str(PROJECTKOIOS_PACKAGE)
        if source_package not in projectkoios.__path__:
            projectkoios.__path__.append(source_package)
        specification = importlib.util.spec_from_file_location(
            "c6_b20_w21_s30_for_s100", S30_IMPLEMENTATION
        )
        if specification is None or specification.loader is None:
            raise RuntimeError("cannot load S30 implementation")
        module = importlib.util.module_from_spec(specification)
        sys.modules[specification.name] = module
        specification.loader.exec_module(module)
        authenticator = module.ArtifactAuthenticator()
        eig = authenticator.execute(module.ARTIFACTS["eig"])
        candidate = module.CandidateOperatorLoader(authenticator, eig).execute(
            module.ELIGIBLE_DECLARATION
        )
        structure = authenticator.execute(module.ARTIFACTS["structure"])
        lattice = module.SiliconLattice.from_structure(structure.path)
        return (
            module,
            cast(FiniteOperator, candidate.finite_operator),
            cast(LatticeProtocol, lattice),
        )


class Statistics:
    """Calculate scalar summaries for one finite array."""

    __slots__ = ()

    @staticmethod
    def absolute(values: Float64Array) -> JsonObject:
        absolute = np.abs(values)
        return {
            "maximum_absolute_ev": float(np.max(absolute)),
            "rms_ev": float(np.sqrt(np.mean(np.square(values)))),
            "percentile_95_absolute_ev": float(np.percentile(absolute, 95.0)),
        }

    @staticmethod
    def nonnegative(values: Float64Array) -> JsonObject:
        return {
            "maximum_ev": float(np.max(values)),
            "rms_ev": float(np.sqrt(np.mean(np.square(values)))),
            "percentile_95_ev": float(np.percentile(values, 95.0)),
        }


class ShellEvaluator:
    """Evaluate every frozen shell against the exact full operator."""

    __slots__ = (
        "_module",
        "_full",
        "_lattice",
        "_design",
        "_s30",
        "_grid21",
        "_grid41",
        "_full_matrices21",
        "_full_eigenvalues21",
        "_edge_mask21",
        "_full_reference",
    )

    def __init__(
        self,
        module: ModuleType,
        full: FiniteOperator,
        lattice: LatticeProtocol,
        design: JsonObject,
        s30: JsonObject,
    ) -> None:
        self._module = module
        self._full = full
        self._lattice = lattice
        self._design = design
        self._s30 = s30
        self._grid21 = cast(GridProtocol, module.ReciprocalGrid.gamma_origin(21))
        self._grid41 = cast(GridProtocol, module.ReciprocalGrid.gamma_origin(41))
        self._full_matrices21 = self._matrices_chunked(full, self._grid21.points)
        self._full_eigenvalues21 = np.linalg.eigvalsh(self._full_matrices21)
        edge = float(np.min(self._full_eigenvalues21[:, 4]))
        self._edge_mask21 = self._full_eigenvalues21[:, 4] <= edge + 0.5
        self._full_reference = self._full_observable_reference()

    def execute(self) -> list[JsonValue]:
        family = mapping(self._design["truncation_family"], "S90 family")
        shells = mapping_list(family["shells"], "S90 shells")
        direct_basis = np.asarray(
            mapping(self._design["fixed_reduction_source"], "S90 source")[
                "direct_basis_columns_angstrom"
            ],
            dtype=np.float64,
        )
        radii = np.linalg.norm(self._full.representatives @ direct_basis.T, axis=1)
        rounded_radii = np.round(radii, decimals=9)
        unique_radii = np.unique(rounded_radii)
        if len(unique_radii) != len(shells):
            raise RuntimeError("S90 shell count disagrees with reconstructed operator")
        records: list[JsonValue] = []
        for shell, radius in zip(shells, unique_radii, strict=True):
            display_radius = number(shell["display_radius_angstrom"], "S90 radius")
            if display_radius != float(radius):
                raise RuntimeError("S90 radius disagrees with reconstructed operator")
            mask = rounded_radii <= radius
            included = int(np.count_nonzero(mask))
            if included != integer(
                shell["included_representative_count"], "S90 included count"
            ):
                raise RuntimeError(
                    "S90 mask count disagrees with reconstructed operator"
                )
            operator = cast(
                FiniteOperator,
                self._module.FiniteWannierOperator(
                    self._full.representatives[mask], self._full.blocks_ev[mask]
                ),
            )
            records.append(self._evaluate_shell(shell, mask, operator))
        self._append_monotone_envelopes(records)
        return records

    def _evaluate_shell(
        self,
        shell: JsonObject,
        mask: np.ndarray[tuple[int], np.dtype[np.bool_]],
        operator: FiniteOperator,
    ) -> JsonObject:
        excluded = ~mask
        block_frobenius = np.linalg.norm(self._full.blocks_ev, axis=(1, 2))
        block_spectral = np.linalg.svd(self._full.blocks_ev, compute_uv=False)[:, 0]
        truncated_matrices = self._matrices_chunked(operator, self._grid21.points)
        matrix_difference = truncated_matrices - self._full_matrices21
        point_spectral = np.max(np.abs(np.linalg.eigvalsh(matrix_difference)), axis=1)
        point_frobenius = np.linalg.norm(matrix_difference, axis=(1, 2))
        truncated_eigenvalues = np.linalg.eigvalsh(truncated_matrices)
        spectrum_difference = truncated_eigenvalues - self._full_eigenvalues21
        structural = self._structural(operator)
        observable = self._observables(operator)
        return {
            "shell_index_zero_based": shell["shell_index_zero_based"],
            "shell_id": shell["shell_id"],
            "radius_angstrom": shell["display_radius_angstrom"],
            "included_representative_count": int(np.count_nonzero(mask)),
            "excluded_representative_count": int(np.count_nonzero(excluded)),
            "structural": structural,
            "tail": {
                "spectral_triangle_bound_ev": float(np.sum(block_spectral[excluded])),
                "frobenius_norm_ev": float(
                    np.sqrt(np.sum(np.square(block_frobenius[excluded])))
                ),
                "maximum_excluded_block_spectral_norm_ev": (
                    float(np.max(block_spectral[excluded])) if np.any(excluded) else 0.0
                ),
            },
            "direct_operator": {
                "spectral_norm": Statistics.nonnegative(point_spectral),
                "frobenius_norm": Statistics.nonnegative(point_frobenius),
            },
            "ordered_spectrum": {
                "all_bands": Statistics.absolute(spectrum_difference),
                "lowest_conduction": Statistics.absolute(spectrum_difference[:, 4]),
                "edge_lowest_conduction": Statistics.absolute(
                    spectrum_difference[self._edge_mask21, 4]
                ),
            },
            "full_source_observable_changes": observable,
        }

    def _structural(self, operator: FiniteOperator) -> JsonObject:
        indices = {
            tuple(int(value) for value in representative): index
            for index, representative in enumerate(operator.representatives)
        }
        missing = 0
        residual = 0.0
        for representative, index in indices.items():
            opposite = tuple(-value for value in representative)
            if opposite not in indices:
                missing += 1
                continue
            residual = max(
                residual,
                float(
                    np.max(
                        np.abs(
                            operator.blocks_ev[index]
                            - operator.blocks_ev[indices[opposite]].conj().T
                        )
                    )
                ),
            )
        full_support = len(operator.representatives) == len(self._full.representatives)
        full_matrix_residual = (
            float(
                np.max(
                    np.abs(
                        self._matrices_chunked(operator, self._grid21.points)
                        - self._full_matrices21
                    )
                )
            )
            if full_support
            else None
        )
        return {
            "missing_negative_representative_count": missing,
            "maximum_pair_hermiticity_residual_ev": residual,
            "pair_closure_passed": missing == 0,
            "full_support_control": full_support,
            "full_support_matrix_maximum_absolute_residual_ev": full_matrix_residual,
        }

    def _observables(self, operator: FiniteOperator) -> JsonObject:
        dense_eigenvalues = operator.eigenvalues(self._grid41.points)
        conduction_spread = float(np.ptp(dense_eigenvalues[:, 4]))
        if conduction_spread == 0.0:
            return {
                "status": "undefined-flat-conduction-band",
                "dense_conduction_spread_ev": conduction_spread,
                "gap_change_ev": None,
                "valley_energy_spread_change_ev": None,
                "opposite_pair_splitting_changes_ev": None,
                "maximum_valley_displacement_inverse_angstrom": None,
                "maximum_valley_energy_change_ev": None,
                "maximum_primary_mass_absolute_relative_change": None,
                "maximum_mass_stencil_relative_spread": None,
                "valleys": [],
            }
        policy = self._module.QualificationPolicy()
        analyzer = self._module.ValleyFamilyAnalyzer(self._lattice, policy)
        valley_result, raw_valleys = analyzer.execute(
            operator, self._grid41, dense_eigenvalues
        )
        valleys = cast(tuple[ValleyMinimum, ...], raw_valleys)
        gamma_values = operator.eigenvalues(np.zeros((1, 3), dtype=np.float64))[0]
        candidate_gap = min(item.energy_ev for item in valleys) - float(gamma_values[3])
        full_gap = number(self._full_reference["indirect_gap_ev"], "full gap")
        full_valleys = mapping(self._full_reference["valleys"], "full valleys")
        candidate_energies = {item.label: item.energy_ev for item in valleys}
        full_energies = {
            label: number(mapping(value, "full valley")["energy_ev"], "full energy")
            for label, value in full_valleys.items()
        }
        candidate_splits = opposite_pair_splits(candidate_energies)
        full_splits = opposite_pair_splits(full_energies)
        valley_records: list[JsonValue] = []
        displacements: list[float] = []
        energy_changes: list[float] = []
        mass_changes: list[float] = []
        stencil_spreads: list[float] = []
        for valley in valleys:
            reference = mapping(full_valleys[valley.label], "full valley")
            displacement = minimum_periodic_cartesian_displacement(
                valley.fractional,
                np.asarray(reference["fractional"], dtype=np.float64),
                self._lattice.reciprocal.primitive_basis_matrix,
            )
            displacement_norm = float(np.linalg.norm(displacement))
            energy_change = valley.energy_ev - number(
                reference["energy_ev"], "full valley energy"
            )
            curvature = self._curvature_records(operator, valley, reference)
            primary_change = curvature["primary_maximum_mass_absolute_relative_change"]
            if isinstance(primary_change, float):
                mass_changes.append(primary_change)
            stencil_spread = curvature["maximum_mass_stencil_relative_spread"]
            if isinstance(stencil_spread, float):
                stencil_spreads.append(stencil_spread)
            displacements.append(displacement_norm)
            energy_changes.append(abs(energy_change))
            valley_records.append(
                {
                    "label": valley.label,
                    "optimizer_success": valley.optimizer_success,
                    "declared_identity_preserved": valley.identity_matches,
                    "fractional_reciprocal_coordinates": valley.fractional.tolist(),
                    "energy_ev_native_reference": valley.energy_ev,
                    "full_source_displacement_cartesian_inverse_angstrom": (
                        displacement.tolist()
                    ),
                    "full_source_displacement_inverse_angstrom": displacement_norm,
                    "full_source_energy_change_ev": energy_change,
                    "curvature_and_mass": curvature,
                }
            )
        candidate_spread = max(candidate_energies.values()) - min(
            candidate_energies.values()
        )
        full_spread = max(full_energies.values()) - min(full_energies.values())
        return {
            "status": (
                "defined"
                if all(item.optimizer_success for item in valleys)
                else "optimizer-failure-recorded"
            ),
            "dense_conduction_spread_ev": conduction_spread,
            "candidate_indirect_gap_ev": candidate_gap,
            "full_source_indirect_gap_ev": full_gap,
            "gap_change_ev": candidate_gap - full_gap,
            "candidate_valley_energy_spread_ev": candidate_spread,
            "full_source_valley_energy_spread_ev": full_spread,
            "valley_energy_spread_change_ev": candidate_spread - full_spread,
            "candidate_opposite_pair_splittings_ev": candidate_splits,
            "full_source_opposite_pair_splittings_ev": full_splits,
            "opposite_pair_splitting_changes_ev": {
                axis: candidate_splits[axis] - full_splits[axis]
                for axis in ("x", "y", "z")
            },
            "all_optimizers_succeeded": valley_result["all_optimizers_succeeded"],
            "all_declared_identities_preserved": valley_result[
                "all_declared_identities_preserved"
            ],
            "maximum_valley_displacement_inverse_angstrom": max(displacements),
            "maximum_valley_energy_change_ev": max(energy_changes),
            "maximum_primary_mass_absolute_relative_change": (
                max(mass_changes) if mass_changes else None
            ),
            "maximum_mass_stencil_relative_spread": (
                max(stencil_spreads) if stencil_spreads else None
            ),
            "valleys": valley_records,
        }

    def _curvature_records(
        self,
        operator: FiniteOperator,
        valley: ValleyMinimum,
        reference: JsonObject,
    ) -> JsonObject:
        step_records: list[JsonValue] = []
        aligned_masses_by_step: list[Float64Array] = []
        primary_change: float | None = None
        all_curvatures_positive = True
        reference_stencils = mapping(
            reference["stencils_by_step"], "full reference stencils"
        )
        for step in (0.001, 0.002, 0.005, 0.01):
            hessian = self._hessian(operator, valley.fractional, step)
            curvatures, axes = np.linalg.eigh(hessian)
            all_curvatures_positive = all_curvatures_positive and bool(
                np.all(curvatures > 0.0)
            )
            reference_step = mapping(
                reference_stencils[f"{step:.3f}"], "full reference stencil"
            )
            reference_axes = np.asarray(
                reference_step["principal_axes_cartesian_columns"], dtype=np.float64
            )
            reference_masses = np.asarray(
                reference_step["principal_mass_ratios_to_electron_mass"],
                dtype=np.float64,
            )
            if np.any(curvatures == 0.0):
                masses: Float64Array | None = None
                comparisons: list[JsonValue] = []
                maximum_change: float | None = None
                status = "undefined-zero-principal-curvature"
            else:
                masses = ELECTRON_MASS_CURVATURE_EV_ANGSTROM2 / curvatures
                permutation = max(
                    itertools.permutations(range(3)),
                    key=lambda indices: sum(
                        abs(axes[:, row] @ reference_axes[:, column])
                        for row, column in enumerate(indices)
                    ),
                )
                aligned_masses = np.empty(3, dtype=np.float64)
                comparisons = []
                changes: list[float] = []
                for candidate_index, reference_index in enumerate(permutation):
                    aligned_masses[reference_index] = masses[candidate_index]
                    relative = abs(
                        masses[candidate_index] - reference_masses[reference_index]
                    ) / abs(reference_masses[reference_index])
                    changes.append(float(relative))
                    comparisons.append(
                        {
                            "candidate_principal_index": candidate_index,
                            "full_source_principal_index": reference_index,
                            "axis_absolute_overlap": float(
                                abs(
                                    axes[:, candidate_index]
                                    @ reference_axes[:, reference_index]
                                )
                            ),
                            "candidate_mass_ratio_to_electron_mass": float(
                                masses[candidate_index]
                            ),
                            "full_source_mass_ratio_to_electron_mass": float(
                                reference_masses[reference_index]
                            ),
                            "absolute_relative_change": float(relative),
                        }
                    )
                aligned_masses_by_step.append(aligned_masses)
                maximum_change = max(changes)
                status = "defined"
            if step == 0.002:
                primary_change = maximum_change
            step_records.append(
                {
                    "step_inverse_angstrom": step,
                    "status": status,
                    "principal_curvatures_ev_angstrom_squared": curvatures.tolist(),
                    "principal_axes_cartesian_columns": axes.tolist(),
                    "principal_mass_ratios_to_electron_mass": (
                        masses.tolist() if masses is not None else None
                    ),
                    "direction_matched_mass_comparisons": comparisons,
                    "maximum_mass_absolute_relative_change": maximum_change,
                }
            )
        if len(aligned_masses_by_step) == 4:
            mass_array = np.asarray(aligned_masses_by_step)
            relative_spread = np.ptp(mass_array, axis=0) / np.abs(mass_array[1])
            maximum_stencil_spread: float | None = float(np.max(relative_spread))
        else:
            maximum_stencil_spread = None
        return {
            "stencils": step_records,
            "all_principal_curvatures_positive": all_curvatures_positive,
            "primary_maximum_mass_absolute_relative_change": primary_change,
            "maximum_mass_stencil_relative_spread": maximum_stencil_spread,
        }

    def _hessian(
        self, operator: FiniteOperator, minimum: Float64Array, step: float
    ) -> Float64Array:
        inverse_reciprocal = np.linalg.inv(
            self._lattice.reciprocal.primitive_basis_matrix
        )
        origin = operator.eigenvalue(minimum, 4)
        hessian = np.empty((3, 3), dtype=np.float64)
        for row in range(3):
            row_delta = inverse_reciprocal[:, row] * step
            hessian[row, row] = (
                operator.eigenvalue(minimum + row_delta, 4)
                - 2.0 * origin
                + operator.eigenvalue(minimum - row_delta, 4)
            ) / step**2
            for column in range(row):
                column_delta = inverse_reciprocal[:, column] * step
                value = (
                    operator.eigenvalue(minimum + row_delta + column_delta, 4)
                    - operator.eigenvalue(minimum + row_delta - column_delta, 4)
                    - operator.eigenvalue(minimum - row_delta + column_delta, 4)
                    + operator.eigenvalue(minimum - row_delta - column_delta, 4)
                ) / (4.0 * step**2)
                hessian[row, column] = value
                hessian[column, row] = value
        return hessian

    def _full_observable_reference(self) -> JsonObject:
        results = mapping(self._s30["results"], "S30 results")
        valley_records = mapping_list(
            mapping(results["valley_family"], "S30 valley family")["valleys"],
            "S30 valleys",
        )
        mass_records = mapping_list(
            mapping(results["effective_mass_diagnostic"], "S30 mass diagnostic")[
                "valleys"
            ],
            "S30 mass valleys",
        )
        masses = {
            string(item["valley_label"], "S30 mass label"): item
            for item in mass_records
        }
        valleys: JsonObject = {}
        for valley in valley_records:
            label = string(valley["label"], "S30 valley label")
            mass = masses[label]
            stencil_records = mapping_list(mass["stencils"], "S30 stencils")
            by_step: JsonObject = {}
            for stencil in stencil_records:
                step = number(stencil["step_inverse_angstrom"], "S30 step")
                by_step[f"{step:.3f}"] = {
                    "principal_axes_cartesian_columns": stencil[
                        "principal_axes_cartesian_columns"
                    ],
                    "principal_mass_ratios_to_electron_mass": stencil[
                        "principal_mass_ratios_to_electron_mass"
                    ],
                }
            valleys[label] = {
                "fractional": valley["fractional_reciprocal_coordinates"],
                "energy_ev": valley["energy_ev_native_reference"],
                "stencils_by_step": by_step,
            }
        gamma = self._full.eigenvalues(np.zeros((1, 3), dtype=np.float64))[0]
        minimum = min(
            number(mapping(value, "full valley")["energy_ev"], "full valley energy")
            for value in valleys.values()
        )
        return {
            "indirect_gap_ev": minimum - float(gamma[3]),
            "valleys": valleys,
        }

    def _matrices_chunked(
        self, operator: FiniteOperator, points: Float64Array
    ) -> Complex128Array:
        chunks: list[Complex128Array] = []
        for start in range(0, len(points), 1024):
            chunks.append(operator.matrices(points[start : start + 1024]))
        return np.concatenate(chunks, axis=0)

    def _append_monotone_envelopes(self, records: list[JsonValue]) -> None:
        typed_records = [mapping(item, "shell record") for item in records]
        metric_paths = {
            "direct_operator_maximum_spectral_norm_ev": (
                "direct_operator",
                "spectral_norm",
                "maximum_ev",
            ),
            "direct_operator_percentile_95_spectral_norm_ev": (
                "direct_operator",
                "spectral_norm",
                "percentile_95_ev",
            ),
            "direct_operator_rms_frobenius_norm_ev": (
                "direct_operator",
                "frobenius_norm",
                "rms_ev",
            ),
        }
        for population in (
            "all_bands",
            "lowest_conduction",
            "edge_lowest_conduction",
        ):
            for statistic in (
                "maximum_absolute_ev",
                "rms_ev",
                "percentile_95_absolute_ev",
            ):
                metric_paths[f"ordered_spectrum_{population}_{statistic}"] = (
                    "ordered_spectrum",
                    population,
                    statistic,
                )
        for index, record in enumerate(typed_records):
            envelope: JsonObject = {}
            for name, path in metric_paths.items():
                values = [nested_number(item, path) for item in typed_records[index:]]
                envelope[name] = max(values)
            record["monotone_larger_shell_envelope"] = envelope


class SpatialTruncationEvaluator:
    """Orchestrate S100 without parent-oracle or calculator access."""

    __slots__ = ()

    def execute(self) -> JsonObject:
        for path, expected in EXPECTED.items():
            if not path.is_file() or path.is_symlink() or sha256(path) != expected:
                raise RuntimeError(f"source identity mismatch: {path}")
        design = load_json(S90_DESIGN)
        s30 = load_json(S30_RESULT)
        module, full, lattice = SourceOperatorLoader().execute()
        records = ShellEvaluator(module, full, lattice, design, s30).execute()
        return {
            "schema_version": 1,
            "stage_id": "S100-spatial-truncation-evaluation",
            "status": "complete-family-evaluated-no-radius-selected",
            "calculator_invocations": 0,
            "bound_inputs": {
                "current_protocol": identity(PROTOCOL),
                "S30_implementation": identity(S30_IMPLEMENTATION),
                "S30_full_operator_characterization": identity(S30_RESULT),
                "S90_design_implementation": identity(S90_IMPLEMENTATION),
                "S90_frozen_truncation_design": identity(S90_DESIGN),
                "ProjectKoios_parser_sources": [
                    identity(path) for path in PROJECTKOIOS_PARSER_SOURCES
                ],
            },
            "source_operator": {
                "route": "C6-B20-W21-aiida-precise",
                "wannier_rank": full.dimension,
                "effective_representative_count": len(full.representatives),
                "role": "fixed full untruncated controlled-reduction source",
            },
            "evaluation": {
                "shell_count": len(records),
                "all_declared_shells_reported": len(records) == 18,
                "radius_selected": False,
                "Slater_Koster_fit_performed": False,
                "shells": records,
            },
            "oracle_boundary": {
                "revealed_408_parent_values_consumed": False,
                "confirmation_402_parent_values_observed": False,
                "confirmation_402_parent_values_consumed": False,
                "interpretation": (
                    "every reported error is internal to H_W-to-H_truncated; no "
                    "direct-parent value enters S100"
                ),
            },
            "disposition": (
                "the complete frozen shell family is evaluated; no shell is accepted "
                "or rejected and no model is fit; a separate decision is required "
                "before any truncation selection or Slater-Koster definition"
            ),
            "nonclaims": [
                "No truncation radius is selected or accepted.",
                "No Slater-Koster model is defined, fit, or validated.",
                "No internal reduction diagnostic is relabeled as hidden-parent error.",
                "No physical validation or uncertainty bound is established.",
                "No later-stage authorization is implied.",
            ],
        }


def opposite_pair_splits(energies_ev: dict[str, float]) -> dict[str, float]:
    """Return absolute signed-pair energy splittings by Cartesian family."""
    return {
        axis: abs(energies_ev[f"+{axis}"] - energies_ev[f"-{axis}"])
        for axis in ("x", "y", "z")
    }


def minimum_periodic_cartesian_displacement(
    candidate: Float64Array, reference: Float64Array, reciprocal: Float64Array
) -> Float64Array:
    shifts = np.asarray(
        tuple(itertools.product((-1, 0, 1), repeat=3)), dtype=np.float64
    )
    values = (candidate[np.newaxis, :] - reference[np.newaxis, :] + shifts) @ (
        reciprocal.T
    )
    return values[int(np.argmin(np.linalg.norm(values, axis=1)))]


def nested_number(record: JsonObject, path: tuple[str, ...]) -> float:
    value: JsonValue = record
    for key in path:
        value = mapping(value, "nested metric")[key]
    return number(value, "nested metric")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def identity(path: Path) -> JsonObject:
    return {
        "path": str(path),
        "byte_size": path.stat().st_size,
        "sha256": sha256(path),
    }


def load_json(path: Path) -> JsonObject:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"JSON root must be a mapping: {path}")
    return cast(JsonObject, value)


def mapping(value: JsonValue, label: str) -> JsonObject:
    if not isinstance(value, dict):
        raise TypeError(f"{label} must be a mapping")
    return value


def mapping_list(value: JsonValue, label: str) -> list[JsonObject]:
    if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
        raise TypeError(f"{label} must be a list of mappings")
    return cast(list[JsonObject], value)


def integer(value: JsonValue, label: str) -> int:
    if type(value) is not int:
        raise TypeError(f"{label} must be an integer")
    return value


def number(value: JsonValue, label: str) -> float:
    if type(value) not in {int, float}:
        raise TypeError(f"{label} must be numeric")
    return float(cast(int | float, value))


def string(value: JsonValue, label: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{label} must be a string")
    return value


def main() -> None:
    if OUTPUT.exists():
        raise RuntimeError("S100 truncation evaluation already exists")
    result = SpatialTruncationEvaluator().execute()
    OUTPUT.write_bytes(TypedJsonMappingSerializer().serialize(result))


if __name__ == "__main__":
    main()
