"""Authenticated matched-extraction baseline adaptation for blind alignment."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import numpy as np

from ...model.toy_defects import (
    Periodic1DBasisScramblingConstructor,
    Periodic1DBasisScramblingModel,
    Periodic1DBasisScramblingRequest,
    Periodic1DFiniteHoppingToyModel,
    Periodic1DHoppingBlock,
    Periodic1DSupercellHamiltonianConstructor,
    Periodic1DSupercellHamiltonianRequest,
)
from ..matched_extraction import (
    MatchedDefectExtractionInputDeserializer,
    MatchedDefectParentDataLoader,
)
from .input_records import BlindAlignmentCampaignInput, BlindAlignmentSourceIdentity
from .records import ComplexMatrix

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


@dataclass(frozen=True, slots=True)
class BlindAlignmentNamedDefect:
    """Store one immutable planted operator used to construct observations.

    Parameters
    ----------
    identifier
        Nonempty retained defect identifier.
    spin_count
        Represented spin factor, one or two.
    matrix
        Finite square ``complex128`` represented perturbation in the reference basis.
    """

    identifier: str
    spin_count: int
    matrix: ComplexMatrix

    def __post_init__(self) -> None:
        """Validate identity and spin factor and retain a read-only finite matrix."""
        if type(self.identifier) is not str or not self.identifier:
            raise ValueError("defect identifier must be nonempty")
        if type(self.spin_count) is not int:
            raise TypeError("spin_count must be an integer")
        if self.spin_count not in (1, 2):
            raise ValueError("spin_count must be one or two")
        if not isinstance(self.matrix, np.ndarray):
            raise TypeError("matrix must be a NumPy array")
        if not np.issubdtype(self.matrix.dtype, np.number) or np.issubdtype(
            self.matrix.dtype, np.bool_
        ):
            raise TypeError("matrix must contain numeric non-Boolean values")
        value = np.asarray(self.matrix, dtype=np.complex128)
        if value.ndim != 2 or value.shape[0] == 0 or value.shape[0] != value.shape[1]:
            raise ValueError("matrix must be nonempty and square")
        if not np.all(np.isfinite(value)):
            raise ValueError("matrix must be finite")
        immutable = np.frombuffer(
            value.tobytes(order="C"), dtype=np.complex128
        ).reshape(value.shape)
        object.__setattr__(self, "matrix", immutable)


@dataclass(frozen=True, slots=True)
class BlindAlignmentBaselineData:
    """Store authenticated matched-extraction data needed by blind alignment.

    Parameters
    ----------
    cell_count
        Number of primitive cells in the finite periodic reference.
    reduced_momentum
        Primitive reciprocal-coordinate momentum represented by the supercell.
    pristine_spinless
        Two-orbital reference Hamiltonian.
    candidate_to_reference_spinless
        Hidden spinless map retained only for post hoc campaign construction and
        evaluation; it is never included in an inference request.
    candidate_to_reference_spinor
        Spin-lifted hidden map with the same restriction.
    energy_shift
        Authored candidate-minus-reference scalar energy shift in ``E_G``.
    defects
        Planted represented perturbations reconstructed from retained compact blocks.
    source_identities
        Authenticated baseline input, result, and transitive composite-parent
        identities in deterministic order.
    """

    cell_count: int
    reduced_momentum: float
    pristine_spinless: ComplexMatrix
    candidate_to_reference_spinless: ComplexMatrix
    candidate_to_reference_spinor: ComplexMatrix
    energy_shift: float
    defects: tuple[BlindAlignmentNamedDefect, ...]
    source_identities: tuple[BlindAlignmentSourceIdentity, ...]

    def __post_init__(self) -> None:
        """Validate baseline metadata, inventories, and immutable matrix storage."""
        if type(self.cell_count) is not int or self.cell_count < 1:
            raise ValueError("cell_count must be a positive integer")
        if not np.isfinite(self.reduced_momentum):
            raise ValueError("reduced_momentum must be finite")
        if not np.isfinite(self.energy_shift):
            raise ValueError("energy_shift must be finite")
        if not self.defects or not self.source_identities:
            raise ValueError("baseline defects and source identities must be nonempty")
        identifiers = tuple(value.identifier for value in self.defects)
        if identifiers != tuple(sorted(set(identifiers))):
            raise ValueError("baseline defects must be sorted and unique")
        for name in (
            "pristine_spinless",
            "candidate_to_reference_spinless",
            "candidate_to_reference_spinor",
        ):
            source = getattr(self, name)
            if not isinstance(source, np.ndarray):
                raise TypeError(f"{name} must be a NumPy array")
            value = np.asarray(source, dtype=np.complex128)
            if value.ndim != 2 or not np.all(np.isfinite(value)):
                raise ValueError(f"{name} must be a finite matrix")
            immutable = np.frombuffer(
                value.tobytes(order="C"), dtype=np.complex128
            ).reshape(value.shape)
            object.__setattr__(self, name, immutable)

    def defect(self, identifier: str) -> BlindAlignmentNamedDefect:
        """Return the uniquely identified planted defect.

        Parameters
        ----------
        identifier
            Exact retained defect identifier.

        Returns
        -------
        BlindAlignmentNamedDefect
            Matching immutable perturbation.

        Raises
        ------
        ValueError
            If the identifier does not occur exactly once.
        """
        matches = tuple(
            value for value in self.defects if value.identifier == identifier
        )
        if len(matches) != 1:
            raise ValueError(f"baseline defect must occur exactly once: {identifier}")
        return matches[0]


class BlindAlignmentBaselineLoader:
    """Authenticate and adapt the matched-extraction baseline.

    The loader verifies the two direct source identities declared by the
    blind-alignment input. It then uses the matched-extraction version-one adapter and
    parent loader, which authenticate the transitive periodic parents, before
    constructing the pristine supercell. Planted perturbations are decoded only from
    authenticated retained compact blocks. No historical runner module is imported.
    """

    __slots__ = ()

    def execute(
        self, specification: BlindAlignmentCampaignInput, repository_root: Path
    ) -> BlindAlignmentBaselineData:
        """Load one authenticated baseline.

        Parameters
        ----------
        specification
            Typed blind-alignment campaign input.
        repository_root
            Explicit repository root containing the declared relative paths.

        Returns
        -------
        BlindAlignmentBaselineData
            Immutable pristine operator, hidden construction oracles, planted
            perturbations, and source identities.

        Raises
        ------
        TypeError
            If arguments or retained representations have incorrect semantic types.
        ValueError
            If an identity, retained field, or represented matrix is invalid.
        """
        if not isinstance(specification, BlindAlignmentCampaignInput):
            raise TypeError("specification must be a BlindAlignmentCampaignInput")
        if not isinstance(repository_root, Path):
            raise TypeError("repository_root must be a Path")
        input_path = repository_root / specification.baseline_input.path
        result_path = repository_root / specification.baseline_result.path
        self._verify_identity(input_path, specification.baseline_input.sha256)
        self._verify_identity(result_path, specification.baseline_result.sha256)
        matched_input = MatchedDefectExtractionInputDeserializer().execute(
            input_path.read_bytes()
        )
        parent = MatchedDefectParentDataLoader().execute(
            matched_input.parent, repository_root
        )
        size = matched_input.extraction.supercell_size
        momentum = matched_input.extraction.reduced_momentum_times_supercell / size
        model = Periodic1DFiniteHoppingToyModel(
            tuple(
                Periodic1DHoppingBlock(
                    displacement,
                    np.asarray(matrix, dtype=np.complex128),
                )
                for displacement, matrix in parent.composite_hoppings
            ),
            "E_G",
            1.0e-12,
        )
        pristine = (
            Periodic1DSupercellHamiltonianConstructor()
            .execute(Periodic1DSupercellHamiltonianRequest(model, size, momentum))
            .matrix
        )
        alignment = matched_input.alignment
        scrambling = Periodic1DBasisScramblingModel(
            translation_cells=alignment.translation_cells,
            orbital_permutation=alignment.orbital_permutation,
            orbital_rotation_radians=alignment.orbital_rotation_angle,
            orbital_phases_radians=alignment.orbital_phases,
            site_phase_step_radians=alignment.site_phase_step,
            spin_rotation_axis=alignment.spin_axis,
            spin_rotation_radians=alignment.spin_rotation_angle,
        )
        constructor = Periodic1DBasisScramblingConstructor()
        spinless_maps = constructor.execute(
            Periodic1DBasisScramblingRequest(scrambling, size, momentum, 1)
        )
        spinor_maps = constructor.execute(
            Periodic1DBasisScramblingRequest(scrambling, size, momentum, 2)
        )
        retained = self._load(result_path)
        controls = self._records(retained["extraction_controls"], "extraction_controls")
        defects = tuple(
            sorted(
                (
                    BlindAlignmentNamedDefect(
                        self._string(record["id"], "defect id"),
                        self._integer(record["spin_count"], "spin count"),
                        self._compact_matrix(
                            record["compact_planted_blocks"],
                            size,
                            2 * self._integer(record["spin_count"], "spin count"),
                        ),
                    )
                    for record in controls
                ),
                key=lambda value: value.identifier,
            )
        )
        composite_identity = BlindAlignmentSourceIdentity(
            matched_input.parent.composite_path,
            matched_input.parent.composite_sha256,
        )
        return BlindAlignmentBaselineData(
            cell_count=size,
            reduced_momentum=momentum,
            pristine_spinless=pristine,
            candidate_to_reference_spinless=spinless_maps.candidate_to_reference,
            candidate_to_reference_spinor=spinor_maps.candidate_to_reference,
            energy_shift=matched_input.alignment.energy_shift,
            defects=defects,
            source_identities=(
                specification.baseline_input,
                specification.baseline_result,
                composite_identity,
            ),
        )

    def _compact_matrix(
        self, value: JsonValue, size: int, block_size: int
    ) -> ComplexMatrix:
        """Expand retained site-block records into one represented perturbation."""
        result = np.zeros((size * block_size, size * block_size), dtype=np.complex128)
        for record in self._records(value, "compact blocks"):
            row = self._integer(record["row_site"], "row site")
            column = self._integer(record["column_site"], "column site")
            block = self._complex_matrix(record["matrix"], "compact block")
            if block.shape != (block_size, block_size):
                raise ValueError("compact block shape is inconsistent")
            result[
                block_size * row : block_size * (row + 1),
                block_size * column : block_size * (column + 1),
            ] = block
        return result

    @staticmethod
    def _load(path: Path) -> dict[str, JsonValue]:
        """Decode one retained JSON object after identity verification."""
        decoded = cast(JsonValue, json.loads(path.read_text(encoding="utf-8")))
        if not isinstance(decoded, dict):
            raise TypeError("retained result root must be a JSON object")
        return decoded

    @staticmethod
    def _records(value: JsonValue, name: str) -> tuple[dict[str, JsonValue], ...]:
        """Require and return a JSON array containing only object records."""
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        records: list[dict[str, JsonValue]] = []
        for item in value:
            if not isinstance(item, dict):
                raise TypeError(f"{name} entries must be JSON objects")
            records.append(item)
        return tuple(records)

    @staticmethod
    def _string(value: JsonValue, name: str) -> str:
        """Require one nonempty built-in string field."""
        if type(value) is not str or not value:
            raise TypeError(f"{name} must be a nonempty string")
        return value

    @staticmethod
    def _integer(value: JsonValue, name: str) -> int:
        """Require one built-in integer while rejecting booleans."""
        if type(value) is not int:
            raise TypeError(f"{name} must be an integer")
        return value

    def _complex_matrix(self, value: JsonValue, name: str) -> ComplexMatrix:
        """Decode a finite rectangular matrix of real-imaginary pairs."""
        if not isinstance(value, list) or not value:
            raise TypeError(f"{name} must be a nonempty matrix")
        rows: list[list[complex]] = []
        for row in value:
            if not isinstance(row, list):
                raise TypeError(f"{name} rows must be arrays")
            parsed: list[complex] = []
            for pair in row:
                if not isinstance(pair, list) or len(pair) != 2:
                    raise TypeError(f"{name} values must be complex pairs")
                parsed.append(
                    complex(self._real(pair[0], name), self._real(pair[1], name))
                )
            rows.append(parsed)
        matrix = np.asarray(rows, dtype=np.complex128)
        if matrix.ndim != 2 or not np.all(np.isfinite(matrix)):
            raise ValueError(f"{name} must be finite and rectangular")
        return matrix

    @staticmethod
    def _real(value: JsonValue, name: str) -> float:
        """Convert one finite JSON number to binary64 while rejecting booleans."""
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(f"{name} must be a real number")
        converted = float(value)
        if not np.isfinite(converted):
            raise ValueError(f"{name} must be finite")
        return converted

    @staticmethod
    def _verify_identity(path: Path, expected: str) -> None:
        """Require one file to match its expected SHA-256 identity exactly."""
        if (
            not path.is_file()
            or hashlib.sha256(path.read_bytes()).hexdigest() != expected
        ):
            raise ValueError(f"source identity mismatch: {path}")
