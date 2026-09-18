#!/usr/bin/env python3
"""Independently reconstruct the synthetic 1D continuum-refinement result."""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type ComplexMatrix = npt.NDArray[np.complex128]
type ComplexVector = npt.NDArray[np.complex128]
type IntegerVector = npt.NDArray[np.int64]


@dataclass(frozen=True, slots=True)
class ParentReference:
    """Retain the independently decoded scalar parent."""

    displacements: IntegerVector
    hoppings: ComplexVector
    edge: float
    coefficient: float


@dataclass(frozen=True, slots=True)
class ReconstructedSpectrum:
    """Record independently reconstructed finite spectral information."""

    energy: float
    binding: float
    count: int
    state: ComplexVector
    boundary_probability: float


class WireReader:
    """Own strict scalar access to retained JSON values."""

    __slots__ = ()

    @staticmethod
    def mapping(value: JsonValue, field: str) -> dict[str, JsonValue]:
        if type(value) is not dict:
            raise TypeError(f"{field} must be an object")
        return value

    @staticmethod
    def sequence(value: JsonValue, field: str) -> list[JsonValue]:
        if type(value) is not list:
            raise TypeError(f"{field} must be an array")
        return value

    @staticmethod
    def string(value: JsonValue, field: str) -> str:
        if type(value) is not str:
            raise TypeError(f"{field} must be a string")
        return value

    @staticmethod
    def integer(value: JsonValue, field: str) -> int:
        if type(value) is not int:
            raise TypeError(f"{field} must be an int excluding bool")
        return value

    @staticmethod
    def real(value: JsonValue, field: str) -> float:
        if type(value) is int:
            return float(value)
        if type(value) is float and np.isfinite(value):
            return value
        raise TypeError(f"{field} must be finite real excluding bool")

    @staticmethod
    def boolean(value: JsonValue, field: str) -> bool:
        if type(value) is not bool:
            raise TypeError(f"{field} must be bool")
        return value


class IndependentOperatorAssembler:
    """Build continuum matrices by loops and lattice matrices through site space."""

    __slots__ = ("_parent", "_integrated", "_peak")

    def __init__(self, parent: ParentReference, integrated: float, peak: float) -> None:
        self._parent = parent
        self._integrated = integrated
        self._peak = peak

    @staticmethod
    def modes(count: int) -> IntegerVector:
        """Return centered Fourier labels."""
        return np.arange(-count // 2, count // 2, dtype=np.int64)

    def continuum(
        self, count: int, length: float, width: float, family: str
    ) -> ComplexMatrix:
        """Build the spectral continuum matrix entry by entry."""
        modes = self.modes(count)
        matrix = np.zeros((count, count), dtype=np.complex128)
        for row, left in enumerate(modes):
            wave_number = float(left) / length
            matrix[row, row] = self._parent.edge + self._parent.coefficient * (
                wave_number**2
            )
            for column, right in enumerate(modes):
                delta = float(left - right) / length
                gaussian = np.exp(-2.0 * np.pi**2 * width**2 * delta**2)
                if family == "fixed-integrated":
                    matrix[row, column] -= self._integrated * gaussian / length
                elif family == "fixed-peak":
                    matrix[row, column] -= (
                        self._peak * np.sqrt(2.0 * np.pi) * width * gaussian / length
                    )
                else:
                    raise ValueError(f"unsupported profile family {family}")
        return matrix

    def lattice_site_route(
        self, count: int, spacing: float, width: float, family: str
    ) -> ComplexMatrix:
        """Assemble the scaled parent in site space before Fourier transformation."""
        site = np.zeros((count, count), dtype=np.complex128)
        for row in range(count):
            for displacement, hopping in zip(
                self._parent.displacements, self._parent.hoppings, strict=True
            ):
                column = (row + int(displacement)) % count
                site[row, column] += hopping
        identity = np.eye(count, dtype=np.complex128)
        site = (
            self._parent.edge * identity
            + (site - self._parent.edge * identity) / spacing**2
        )
        site += np.diag(self._sample_profile(count, spacing, width, family))
        modes = self.modes(count)
        positions = np.arange(count, dtype=np.float64)
        transform = np.exp(2j * np.pi * np.outer(positions, modes) / count) / np.sqrt(
            count
        )
        matrix = transform.conj().T @ site @ transform
        residual = float(np.max(np.abs(matrix - matrix.conj().T)))
        if residual > 2e-11:
            raise ValueError(f"independent lattice matrix is not Hermitian: {residual}")
        return matrix

    def _sample_profile(
        self, count: int, spacing: float, width: float, family: str
    ) -> npt.NDArray[np.float64]:
        length = count * spacing
        values = np.zeros(count, dtype=np.float64)
        for point in range(count):
            x_value = point * spacing
            periodic = 0.0
            for image in range(-4, 5):
                periodic += float(
                    np.exp(-0.5 * ((x_value + image * length) / width) ** 2)
                )
            if family == "fixed-integrated":
                scale = -self._integrated / (np.sqrt(2.0 * np.pi) * width)
            elif family == "fixed-peak":
                scale = -self._peak
            else:
                raise ValueError(f"unsupported profile family {family}")
            values[point] = scale * periodic
        return values


class IndependentSpectrumReconstructor:
    """Diagonalize reconstructed matrices and derive retained diagnostics."""

    __slots__ = ("_edge", "_margin")

    def __init__(self, edge: float, margin: float) -> None:
        self._edge = edge
        self._margin = margin

    def execute(self, matrix: ComplexMatrix, length: float) -> ReconstructedSpectrum:
        eigenvalues, eigenvectors = np.linalg.eigh(matrix)
        state = np.asarray(eigenvectors[:, 0], dtype=np.complex128)
        energy = float(eigenvalues[0])
        count = int(np.count_nonzero(eigenvalues < self._edge - self._margin))
        modes = IndependentOperatorAssembler.modes(state.size)
        positions = np.arange(state.size, dtype=np.float64)
        transform = np.exp(
            2j * np.pi * np.outer(positions, modes) / state.size
        ) / np.sqrt(state.size)
        real_state = transform @ state
        distances = np.minimum(
            positions * length / state.size,
            length - positions * length / state.size,
        )
        boundary = float(np.sum(np.abs(real_state[distances >= length / 4.0]) ** 2))
        return ReconstructedSpectrum(
            energy,
            max(0.0, self._edge - energy),
            count,
            state,
            boundary,
        )


class IndependentResultVerifier:
    """Reconstruct every axis and compare with the retained result."""

    __slots__ = (
        "_root",
        "_input",
        "_assembler",
        "_spectrum",
        "_comparison",
    )

    def __init__(
        self,
        root: dict[str, JsonValue],
        input_root: dict[str, JsonValue],
        assembler: IndependentOperatorAssembler,
        spectrum: IndependentSpectrumReconstructor,
    ) -> None:
        self._root = root
        self._input = input_root
        self._assembler = assembler
        self._spectrum = spectrum
        self._comparison = WireReader.mapping(
            input_root["comparison_contract"], "comparison"
        )

    def execute(self) -> None:
        mesh_pass = self._verify_mesh()
        domain_pass = self._verify_domain()
        supercell_pass = self._verify_supercell()
        scale_boundary = self._verify_scale()
        profile_boundaries = self._verify_profiles()
        assessment = WireReader.mapping(
            self._root["crossover_assessment"], "assessment"
        )
        support = mesh_pass and domain_pass and supercell_pass
        self._equal(assessment["supporting_axes_pass"], support, "supporting axes")
        self._optional_real(
            assessment["lattice_scale_persistent_pass_spacing"],
            scale_boundary,
            "scale boundary",
        )
        self._optional_real(
            assessment["fixed_integrated_crossover_width"],
            profile_boundaries["fixed-integrated"],
            "fixed-integrated crossover",
        )
        self._optional_real(
            assessment["fixed_peak_crossover_width"],
            profile_boundaries["fixed-peak"],
            "fixed-peak crossover",
        )
        stable = support and scale_boundary is not None
        self._equal(
            assessment["stable_lattice_scale_comparison"],
            stable,
            "stable lattice-scale comparison",
        )
        self._equal(
            assessment["profile_defined_crossover_established"],
            profile_boundaries["fixed-integrated"] is not None,
            "profile crossover state",
        )

    def _verify_mesh(self) -> bool:
        config = WireReader.mapping(self._input["continuum_mesh_axis"], "mesh")
        section = WireReader.mapping(self._root["continuum_mesh_axis"], "mesh result")
        records = self._record_list(section["records"], "mesh records")
        counts = tuple(
            WireReader.integer(value, "mode count")
            for value in WireReader.sequence(config["mode_counts"], "mode counts")
        )
        length = WireReader.real(config["domain_length"], "mesh length")
        width = WireReader.real(config["profile_width"], "mesh width")
        family = WireReader.string(config["profile_family"], "mesh family")
        spectra: list[ReconstructedSpectrum] = []
        matrices: list[ComplexMatrix] = []
        for count in counts:
            matrix = self._assembler.continuum(count, length, width, family)
            matrices.append(matrix)
            spectra.append(self._spectrum.execute(matrix, length))
        reference = spectra[-1]
        for record, count, matrix, spectrum in zip(
            records, counts, matrices, spectra, strict=True
        ):
            self._equal(record["mode_count"], count, "mesh mode count")
            self._close(record["binding_energy"], spectrum.binding, "mesh binding")
            self._equal(record["bound_state_count"], spectrum.count, "mesh count")
            self._close(
                record["boundary_probability"],
                spectrum.boundary_probability,
                "mesh boundary",
            )
            self._close(
                record["binding_defect_from_finest"],
                abs(spectrum.binding - reference.binding),
                "mesh reference binding",
            )
            projector = self._projector(
                spectrum.state,
                self._assembler.modes(count),
                reference.state,
                self._assembler.modes(counts[-1]),
            )
            self._close(
                record["projector_defect_from_finest"], projector, "mesh projector"
            )
            self._equal(record["operator_sha256"], self._digest(matrix), "mesh digest")
        latest_binding = abs(spectra[-2].binding - spectra[-1].binding)
        latest_projector = self._projector(
            spectra[-2].state,
            self._assembler.modes(counts[-2]),
            spectra[-1].state,
            self._assembler.modes(counts[-1]),
        )
        passed = latest_binding <= self._tolerance(
            "continuum_mesh_binding_tolerance"
        ) and latest_projector <= self._tolerance("continuum_mesh_projector_tolerance")
        self._equal(section["latest_step_pass"], passed, "mesh pass")
        return passed

    def _verify_domain(self) -> bool:
        config = WireReader.mapping(self._input["continuum_domain_axis"], "domain")
        section = WireReader.mapping(
            self._root["continuum_domain_axis"], "domain result"
        )
        records = self._record_list(section["records"], "domain records")
        lengths = tuple(
            WireReader.real(value, "domain length")
            for value in WireReader.sequence(config["domain_lengths"], "domain lengths")
        )
        spacing = WireReader.real(config["spectral_spacing"], "spectral spacing")
        width = WireReader.real(config["profile_width"], "domain width")
        family = WireReader.string(config["profile_family"], "domain family")
        spectra: list[ReconstructedSpectrum] = []
        matrices: list[ComplexMatrix] = []
        for length in lengths:
            matrix = self._assembler.continuum(
                int(round(length / spacing)), length, width, family
            )
            matrices.append(matrix)
            spectra.append(self._spectrum.execute(matrix, length))
        for record, length, matrix, spectrum in zip(
            records, lengths, matrices, spectra, strict=True
        ):
            self._close(record["domain_length"], length, "domain length")
            self._close(record["binding_energy"], spectrum.binding, "domain binding")
            self._equal(record["bound_state_count"], spectrum.count, "domain count")
            self._close(
                record["boundary_probability"],
                spectrum.boundary_probability,
                "domain boundary probability",
            )
            self._close(
                record["binding_defect_from_largest_domain"],
                abs(spectrum.binding - spectra[-1].binding),
                "domain reference binding",
            )
            self._equal(
                record["operator_sha256"], self._digest(matrix), "domain digest"
            )
        passed = abs(spectra[-2].binding - spectra[-1].binding) <= self._tolerance(
            "finite_domain_binding_tolerance"
        ) and spectra[-1].boundary_probability <= self._tolerance(
            "finite_domain_boundary_probability_tolerance"
        )
        self._equal(section["latest_step_pass"], passed, "domain pass")
        return passed

    def _verify_supercell(self) -> bool:
        config = WireReader.mapping(self._input["lattice_supercell_axis"], "supercell")
        section = WireReader.mapping(
            self._root["lattice_supercell_axis"], "supercell result"
        )
        records = self._record_list(section["records"], "supercell records")
        counts = tuple(
            WireReader.integer(value, "cell count")
            for value in WireReader.sequence(config["cell_counts"], "cell counts")
        )
        spacing = WireReader.real(config["lattice_spacing"], "lattice spacing")
        width = WireReader.real(config["profile_width"], "supercell width")
        family = WireReader.string(config["profile_family"], "supercell family")
        spectra: list[ReconstructedSpectrum] = []
        matrices: list[ComplexMatrix] = []
        for count in counts:
            matrix = self._assembler.lattice_site_route(count, spacing, width, family)
            matrices.append(matrix)
            spectra.append(self._spectrum.execute(matrix, count * spacing))
        for record, count, matrix, spectrum in zip(
            records, counts, matrices, spectra, strict=True
        ):
            self._equal(record["cell_count"], count, "cell count")
            self._close(record["binding_energy"], spectrum.binding, "supercell binding")
            self._equal(record["bound_state_count"], spectrum.count, "supercell count")
            self._close(
                record["boundary_probability"],
                spectrum.boundary_probability,
                "supercell boundary probability",
            )
            self._close(
                record["binding_defect_from_largest_supercell"],
                abs(spectrum.binding - spectra[-1].binding),
                "supercell reference binding",
            )
            self._equal(
                record["operator_sha256"], self._digest(matrix), "supercell digest"
            )
        passed = abs(spectra[-2].binding - spectra[-1].binding) <= self._tolerance(
            "lattice_supercell_binding_tolerance"
        ) and spectra[-1].boundary_probability <= self._tolerance(
            "lattice_supercell_boundary_probability_tolerance"
        )
        self._equal(section["latest_step_pass"], passed, "supercell pass")
        return passed

    def _verify_scale(self) -> float | None:
        config = WireReader.mapping(self._input["lattice_scale_axis"], "scale")
        section = WireReader.mapping(self._root["lattice_scale_axis"], "scale result")
        records = self._record_list(section["records"], "scale records")
        length = WireReader.real(config["domain_length"], "scale length")
        width = WireReader.real(config["profile_width"], "scale width")
        family = WireReader.string(config["profile_family"], "scale family")
        spacings = tuple(
            WireReader.real(value, "scale spacing")
            for value in WireReader.sequence(
                config["lattice_spacings"], "scale spacings"
            )
        )
        passes: list[bool] = []
        for record, spacing in zip(records, spacings, strict=True):
            count = int(round(length / spacing))
            lattice = self._assembler.lattice_site_route(count, spacing, width, family)
            continuum = self._assembler.continuum(count, length, width, family)
            passed = self._verify_comparison(
                record, lattice, continuum, length, spacing
            )
            passes.append(passed)
        boundary = next(
            (spacing for index, spacing in enumerate(spacings) if all(passes[index:])),
            None,
        )
        self._optional_real(
            section["largest_spacing_with_persistent_pass"], boundary, "scale result"
        )
        return boundary

    def _verify_profiles(self) -> dict[str, float | None]:
        config = WireReader.mapping(self._input["profile_width_axis"], "profile")
        section = WireReader.mapping(self._root["profile_width_axis"], "profiles")
        families = self._record_list(section["families"], "profile families")
        length = WireReader.real(config["domain_length"], "profile length")
        spacing = WireReader.real(config["lattice_spacing"], "profile spacing")
        count = int(round(length / spacing))
        widths = tuple(
            WireReader.real(value, "profile width")
            for value in WireReader.sequence(config["widths"], "profile widths")
        )
        boundaries: dict[str, float | None] = {}
        for family_record in families:
            family = WireReader.string(family_record["family"], "family")
            records = self._record_list(family_record["records"], "family records")
            passes: list[bool] = []
            for record, width in zip(records, widths, strict=True):
                lattice = self._assembler.lattice_site_route(
                    count, spacing, width, family
                )
                continuum = self._assembler.continuum(count, length, width, family)
                passes.append(
                    self._verify_comparison(record, lattice, continuum, length, spacing)
                )
            boundary = next(
                (width for index, width in enumerate(widths) if all(passes[index:])),
                None,
            )
            self._optional_real(
                family_record["crossover_width"], boundary, f"{family} crossover"
            )
            boundaries[family] = boundary
        return boundaries

    def _verify_comparison(
        self,
        record: dict[str, JsonValue],
        lattice: ComplexMatrix,
        continuum: ComplexMatrix,
        length: float,
        spacing: float,
    ) -> bool:
        lattice_spectrum = self._spectrum.execute(lattice, length)
        continuum_spectrum = self._spectrum.execute(continuum, length)
        binding_error = abs(lattice_spectrum.binding - continuum_spectrum.binding)
        relative = binding_error / max(continuum_spectrum.binding, np.finfo(float).tiny)
        modes = self._assembler.modes(lattice.shape[0])
        projector = self._projector(
            lattice_spectrum.state, modes, continuum_spectrum.state, modes
        )
        wave_numbers = modes.astype(np.float64) / length
        low = np.abs(wave_numbers) <= self._tolerance("physical_low_momentum_cutoff")
        difference = lattice - continuum
        compressed = difference[np.ix_(low, low)]
        compressed_norm = float(np.max(np.abs(np.linalg.eigvalsh(compressed))))
        cross = difference[np.ix_(low, ~low)]
        cross_norm = (
            float(np.linalg.svd(cross, compute_uv=False)[0]) if cross.size else 0.0
        )
        edge = np.abs(spacing * wave_numbers) >= self._tolerance(
            "brillouin_edge_fraction"
        )
        edge_weight = float(np.sum(np.abs(lattice_spectrum.state[edge]) ** 2))
        count_equal = lattice_spectrum.count == continuum_spectrum.count
        criteria = {
            "relative_binding": relative
            <= self._tolerance("relative_binding_tolerance"),
            "projector": projector <= self._tolerance("projector_frobenius_tolerance"),
            "compressed_operator": compressed_norm
            <= self._tolerance("compressed_operator_tolerance"),
            "cross_coupling": cross_norm <= self._tolerance("cross_coupling_tolerance"),
            "brillouin_edge_weight": edge_weight
            <= self._tolerance("brillouin_edge_weight_tolerance"),
            "bound_state_count": count_equal
            or not WireReader.boolean(
                self._comparison["require_equal_bound_state_count"], "count rule"
            ),
        }
        numeric = {
            "lattice_binding_energy": lattice_spectrum.binding,
            "continuum_binding_energy": continuum_spectrum.binding,
            "absolute_binding_error": binding_error,
            "relative_binding_error": relative,
            "projector_frobenius_defect": projector,
            "compressed_operator_spectral_norm": compressed_norm,
            "cross_coupling_spectral_norm": cross_norm,
            "brillouin_edge_weight": edge_weight,
        }
        for key, value in numeric.items():
            self._close(record[key], value, key)
        self._equal(
            record["lattice_bound_state_count"],
            lattice_spectrum.count,
            "lattice bound count",
        )
        self._equal(
            record["continuum_bound_state_count"],
            continuum_spectrum.count,
            "continuum bound count",
        )
        retained_criteria = WireReader.mapping(record["criteria"], "criteria")
        for key, value in criteria.items():
            self._equal(retained_criteria[key], value, f"criterion {key}")
        passed = all(criteria.values())
        self._equal(record["all_criteria_pass"], passed, "all criteria")
        self._equal(
            record["lattice_operator_sha256"],
            self._digest(lattice),
            "lattice digest",
        )
        self._equal(
            record["continuum_operator_sha256"],
            self._digest(continuum),
            "continuum digest",
        )
        return passed

    def _tolerance(self, field: str) -> float:
        return WireReader.real(self._comparison[field], field)

    @staticmethod
    def _record_list(value: JsonValue, field: str) -> list[dict[str, JsonValue]]:
        return [
            WireReader.mapping(item, field)
            for item in WireReader.sequence(value, field)
        ]

    @staticmethod
    def _projector(
        left: ComplexVector,
        left_modes: IntegerVector,
        right: ComplexVector,
        right_modes: IntegerVector,
    ) -> float:
        right_by_mode = {
            int(mode): right[index] for index, mode in enumerate(right_modes)
        }
        overlap = sum(
            np.conj(left[index]) * right_by_mode.get(int(mode), 0.0j)
            for index, mode in enumerate(left_modes)
        )
        norms = float(np.vdot(left, left).real * np.vdot(right, right).real)
        fidelity = min(1.0, max(0.0, float(abs(overlap) ** 2 / norms)))
        return float(np.sqrt(2.0 * (1.0 - fidelity)))

    @staticmethod
    def _digest(matrix: ComplexMatrix) -> str:
        canonical = np.asarray(matrix, dtype=np.complex128).copy()
        canonical.real = np.round(canonical.real, decimals=9)
        canonical.imag = np.round(canonical.imag, decimals=9)
        canonical.real[canonical.real == 0.0] = 0.0
        canonical.imag[canonical.imag == 0.0] = 0.0
        return hashlib.sha256(canonical.tobytes(order="C")).hexdigest()

    @staticmethod
    def _close(retained: JsonValue, reconstructed: float, field: str) -> None:
        value = WireReader.real(retained, field)
        tolerance = 2e-10 * max(1.0, abs(value), abs(reconstructed))
        if abs(value - reconstructed) > tolerance:
            raise ValueError(
                f"{field} mismatch: retained={value}, reconstructed={reconstructed}"
            )

    @staticmethod
    def _equal(retained: JsonValue, reconstructed: JsonValue, field: str) -> None:
        if retained != reconstructed:
            raise ValueError(
                f"{field} mismatch: retained={retained}, reconstructed={reconstructed}"
            )

    @staticmethod
    def _optional_real(
        retained: JsonValue, reconstructed: float | None, field: str
    ) -> None:
        if retained is None and reconstructed is None:
            return
        if retained is None or reconstructed is None:
            raise ValueError(f"{field} optional-value mismatch")
        IndependentResultVerifier._close(retained, reconstructed, field)


class VerificationApplication:
    """Own source loading and command-line verification."""

    __slots__ = ()

    def execute(self) -> None:
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("--result", type=Path, required=True)
        arguments = parser.parse_args()
        result_path = cast(Path, arguments.result).resolve()
        package = result_path.parent
        input_path = package / "input.json"
        result_root = WireReader.mapping(
            cast(JsonValue, json.loads(result_path.read_bytes())), "result"
        )
        input_payload = input_path.read_bytes()
        input_root = WireReader.mapping(
            cast(JsonValue, json.loads(input_payload)), "input"
        )
        provenance = WireReader.mapping(result_root["provenance"], "provenance")
        expected_input_hash = WireReader.string(
            provenance["input_sha256"], "input hash"
        )
        if hashlib.sha256(input_payload).hexdigest() != expected_input_hash:
            raise ValueError("input identity mismatch")
        repository_root = input_path.parents[3]
        self._verify_sources(repository_root, input_root)
        parent = self._load_parent(repository_root, input_root)
        represented = WireReader.mapping(
            input_root["represented_contract"], "represented"
        )
        assembler = IndependentOperatorAssembler(
            parent,
            WireReader.real(
                represented["fixed_integrated_magnitude"], "integrated magnitude"
            ),
            WireReader.real(represented["fixed_peak_magnitude"], "peak magnitude"),
        )
        comparison = WireReader.mapping(input_root["comparison_contract"], "comparison")
        spectrum = IndependentSpectrumReconstructor(
            parent.edge,
            WireReader.real(comparison["bound_state_edge_margin"], "edge margin"),
        )
        IndependentResultVerifier(
            result_root, input_root, assembler, spectrum
        ).execute()
        print("independent verification: PASS")

    @staticmethod
    def _verify_sources(
        repository_root: Path, input_root: dict[str, JsonValue]
    ) -> None:
        for item in WireReader.sequence(input_root["source_identities"], "sources"):
            source = WireReader.mapping(item, "source")
            path = WireReader.string(source["path"], "source path")
            expected = WireReader.string(source["sha256"], "source sha256")
            if (
                hashlib.sha256((repository_root / path).read_bytes()).hexdigest()
                != expected
            ):
                raise ValueError(f"source identity mismatch: {path}")

    @staticmethod
    def _load_parent(
        repository_root: Path, input_root: dict[str, JsonValue]
    ) -> ParentReference:
        parent_path = ""
        for item in WireReader.sequence(input_root["source_identities"], "sources"):
            source = WireReader.mapping(item, "source")
            candidate = WireReader.string(source["path"], "source path")
            if candidate.endswith("periodic-1d/result.json"):
                parent_path = candidate
        if not parent_path:
            raise ValueError("parent source is missing")
        parent_root = WireReader.mapping(
            cast(
                JsonValue,
                json.loads((repository_root / parent_path).read_bytes()),
            ),
            "parent result",
        )
        reduction = WireReader.mapping(
            parent_root["isolated_band_reduction"], "reduction"
        )
        displacements = np.asarray(
            [
                WireReader.integer(value, "displacement")
                for value in WireReader.sequence(
                    reduction["hopping_representatives_cells"], "displacements"
                )
            ],
            dtype=np.int64,
        )
        coefficients: list[complex] = []
        for value in WireReader.sequence(reduction["hopping_coefficients"], "hoppings"):
            pair = WireReader.sequence(value, "hopping pair")
            coefficients.append(
                complex(
                    WireReader.real(pair[0], "hopping real"),
                    WireReader.real(pair[1], "hopping imaginary"),
                )
            )
        hoppings = np.asarray(coefficients, dtype=np.complex128)
        edge = float(np.real(np.sum(hoppings)))
        coefficient = float(
            np.real(-0.5 * np.sum((2.0 * np.pi * displacements) ** 2 * hoppings))
        )
        return ParentReference(displacements, hoppings, edge, coefficient)


def main() -> None:
    """Adapt the Python script entry point to the owned verifier."""
    VerificationApplication().execute()


if __name__ == "__main__":
    main()
