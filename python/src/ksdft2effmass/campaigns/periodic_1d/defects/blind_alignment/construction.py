"""Synthetic observation construction for periodic-1D blind alignment."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..matched_extraction import RepresentedOperator, SupercellBasis
from .baseline import BlindAlignmentBaselineData
from .records import BlindAlignmentObservation, ComplexMatrix


@dataclass(frozen=True, slots=True)
class BlindAlignmentHiddenTruth:
    """Store construction-only values withheld from inference.

    Parameters
    ----------
    candidate_to_reference
        Authored map from candidate coordinates to reference coordinates.
    planted_defect
        Authored perturbation in reference coordinates and energy unit ``E_G``.
    energy_shift
        Authored candidate-minus-reference scalar energy shift in ``E_G``.

    Notes
    -----
    This record exists only for synthetic construction and post hoc evaluation. It is
    not a member of :class:`BlindAlignmentObservation` or
    :class:`BlindAlignmentInferenceRequest`.
    """

    candidate_to_reference: ComplexMatrix
    planted_defect: ComplexMatrix
    energy_shift: float

    def __post_init__(self) -> None:
        """Validate scalar truth and copy hidden matrices into read-only storage."""
        if isinstance(self.energy_shift, bool) or not isinstance(
            self.energy_shift, int | float
        ):
            raise TypeError("energy_shift must be a real number")
        if not np.isfinite(self.energy_shift):
            raise ValueError("energy_shift must be finite")
        for name in ("candidate_to_reference", "planted_defect"):
            source = getattr(self, name)
            if not isinstance(source, np.ndarray):
                raise TypeError(f"{name} must be a NumPy array")
            if not np.issubdtype(source.dtype, np.number) or np.issubdtype(
                source.dtype, np.bool_
            ):
                raise TypeError(f"{name} must contain numeric non-Boolean values")
            value = np.asarray(source, dtype=np.complex128)
            if value.ndim != 2 or value.shape[0] == 0:
                raise ValueError(f"{name} must be a nonempty matrix")
            if not np.all(np.isfinite(value)):
                raise ValueError(f"{name} must be finite")
            immutable = np.frombuffer(
                value.tobytes(order="C"), dtype=np.complex128
            ).reshape(value.shape)
            object.__setattr__(self, name, immutable)


@dataclass(frozen=True, slots=True)
class BlindAlignmentObservationConstructionRequest:
    """Request one full-dimensional synthetic blind observation.

    Parameters
    ----------
    baseline
        Authenticated matched-extraction baseline.
    identifier
        Nonempty observation identifier.
    defect_id
        Exact planted-defect identifier.
    spin_count
        Represented spin factor, one or two.
    minimum_anchor_singular_value
        Positive smallest authored anchor singular value in ``(0, 1]``.
    unitary_noise_radians
        Nonnegative finite rotation amplitude applied to the anchor covariance.
    generator_seed
        Python integer deterministic noise seed.
    core_radius_cells
        Nonnegative integer radius excluded from the exterior energy anchor.
    allow_partial_alignment
        Explicit permission for an identified-sector result.
    """

    baseline: BlindAlignmentBaselineData
    identifier: str
    defect_id: str
    spin_count: int
    minimum_anchor_singular_value: float
    unitary_noise_radians: float
    generator_seed: int
    core_radius_cells: int
    allow_partial_alignment: bool = False

    def __post_init__(self) -> None:
        """Validate exact baseline, case, numeric, and partial-alignment controls."""
        if not isinstance(self.baseline, BlindAlignmentBaselineData):
            raise TypeError("baseline must be BlindAlignmentBaselineData")
        if type(self.identifier) is not str or not self.identifier:
            raise ValueError("identifier must be nonempty")
        if type(self.defect_id) is not str or not self.defect_id:
            raise ValueError("defect_id must be nonempty")
        if type(self.spin_count) is not int:
            raise TypeError("spin_count must be an integer")
        if self.spin_count not in (1, 2):
            raise ValueError("spin_count must be one or two")
        reals = (
            self.minimum_anchor_singular_value,
            self.unitary_noise_radians,
        )
        if any(
            isinstance(value, bool) or not isinstance(value, int | float)
            for value in reals
        ):
            raise TypeError("anchor singular value and noise must be real numbers")
        if (
            not np.isfinite(self.minimum_anchor_singular_value)
            or not 0.0 < self.minimum_anchor_singular_value <= 1.0
        ):
            raise ValueError("minimum anchor singular value must lie in (0, 1]")
        if (
            not np.isfinite(self.unitary_noise_radians)
            or self.unitary_noise_radians < 0.0
        ):
            raise ValueError("unitary noise must be nonnegative and finite")
        if type(self.generator_seed) is not int:
            raise TypeError("generator_seed must be an integer")
        if type(self.core_radius_cells) is not int:
            raise TypeError("core_radius_cells must be an integer")
        if self.core_radius_cells < 0:
            raise ValueError("core_radius_cells must be nonnegative")
        if type(self.allow_partial_alignment) is not bool:
            raise TypeError("allow_partial_alignment must be Boolean")


@dataclass(frozen=True, slots=True)
class BlindAlignmentObservationConstructionResult:
    """Return inference-visible observation separately from hidden truth.

    Parameters
    ----------
    observation
        Record permitted as input to blind inference.
    hidden_truth
        Construction-only record permitted only for post hoc evaluation.
    """

    observation: BlindAlignmentObservation
    hidden_truth: BlindAlignmentHiddenTruth

    def __post_init__(self) -> None:
        """Require distinct exact observation and hidden-truth record types."""
        if not isinstance(self.observation, BlindAlignmentObservation):
            raise TypeError("observation must be BlindAlignmentObservation")
        if not isinstance(self.hidden_truth, BlindAlignmentHiddenTruth):
            raise TypeError("hidden_truth must be BlindAlignmentHiddenTruth")


class BlindAlignmentObservationConstructor:
    """Construct a synthetic observation while preserving the inference boundary."""

    __slots__ = ()

    def execute(
        self, request: BlindAlignmentObservationConstructionRequest
    ) -> BlindAlignmentObservationConstructionResult:
        """Construct one full-dimensional synthetic observation.

        Parameters
        ----------
        request
            Authenticated baseline and authored synthetic case controls.

        Returns
        -------
        BlindAlignmentObservationConstructionResult
            Inference-visible observation and a separately typed hidden oracle.

        Raises
        ------
        TypeError
            If ``request`` has the wrong public type.
        ValueError
            If the selected defect and spin space are inconsistent or the exterior
            anchor has no represented direction.
        """
        if not isinstance(request, BlindAlignmentObservationConstructionRequest):
            raise TypeError(
                "request must be BlindAlignmentObservationConstructionRequest"
            )
        baseline = request.baseline
        defect = baseline.defect(request.defect_id)
        if defect.spin_count != request.spin_count:
            raise ValueError("selected defect spin count is inconsistent")
        if request.spin_count == 1:
            reference = baseline.pristine_spinless
            transform = baseline.candidate_to_reference_spinless
        else:
            reference = np.asarray(
                np.kron(baseline.pristine_spinless, np.eye(2)),
                dtype=np.complex128,
            )
            transform = baseline.candidate_to_reference_spinor
        dimension = reference.shape[0]
        noise = self._unitary_noise(
            dimension, request.unitary_noise_radians, request.generator_seed
        )
        singular_values = np.linspace(
            1.0, request.minimum_anchor_singular_value, dimension
        )
        anchor = np.diag(singular_values) @ noise @ transform
        candidate = transform.conj().T @ (
            reference + defect.matrix
        ) @ transform + baseline.energy_shift * np.eye(dimension)
        exterior = self._exterior_projector(
            baseline.cell_count,
            2 * request.spin_count,
            request.core_radius_cells,
        )
        if not np.any(np.diag(exterior).real > 0.5):
            raise ValueError("core radius leaves no exterior energy-anchor direction")
        reference_basis = self._basis(
            baseline.cell_count,
            request.spin_count,
            baseline.reduced_momentum,
            "reference-canonical",
            "reference-zero",
        )
        candidate_basis = self._basis(
            baseline.cell_count,
            request.spin_count,
            baseline.reduced_momentum,
            "candidate-hidden-frame",
            "candidate-shifted-zero",
        )
        observation = BlindAlignmentObservation(
            identifier=request.identifier,
            reference_operator=RepresentedOperator(
                f"{request.identifier}-reference", reference_basis, reference
            ),
            candidate_operator=RepresentedOperator(
                f"{request.identifier}-candidate", candidate_basis, candidate
            ),
            anchor_cross_covariance=anchor,
            retained_subspace_overlap=np.eye(dimension, dtype=np.complex128),
            exterior_energy_anchor=exterior,
            allow_partial_alignment=request.allow_partial_alignment,
        )
        truth = BlindAlignmentHiddenTruth(
            candidate_to_reference=transform,
            planted_defect=defect.matrix,
            energy_shift=baseline.energy_shift,
        )
        return BlindAlignmentObservationConstructionResult(observation, truth)

    @staticmethod
    def _unitary_noise(dimension: int, radians: float, seed: int) -> ComplexMatrix:
        """Construct the deterministic nearest-neighbor Hermitian rotation."""
        if radians == 0.0:
            return np.eye(dimension, dtype=np.complex128)
        generator = np.zeros((dimension, dimension), dtype=np.complex128)
        rng = np.random.default_rng(seed)
        for index in range(dimension - 1):
            value = rng.normal() + 1j * rng.normal()
            generator[index, index + 1] = value
            generator[index + 1, index] = value.conjugate()
        norm = float(np.linalg.norm(generator, 2))
        if norm == 0.0:
            raise ValueError("noise generator must be nonzero")
        values, vectors = np.linalg.eigh(generator / norm)
        return np.asarray(
            vectors @ np.diag(np.exp(1j * radians * values)) @ vectors.conj().T,
            dtype=np.complex128,
        )

    @staticmethod
    def _exterior_projector(
        cell_count: int, block_size: int, core_radius: int
    ) -> ComplexMatrix:
        """Construct the minimum-image exterior-site orthogonal projector."""
        coordinates = np.arange(cell_count, dtype=np.int64)
        coordinates = np.where(
            coordinates <= cell_count // 2,
            coordinates,
            coordinates - cell_count,
        )
        result = np.zeros(
            (cell_count * block_size, cell_count * block_size),
            dtype=np.complex128,
        )
        for site, coordinate in enumerate(coordinates):
            if abs(coordinate) > core_radius:
                begin = block_size * site
                result[begin : begin + block_size, begin : begin + block_size] = np.eye(
                    block_size
                )
        return result

    @staticmethod
    def _basis(
        cell_count: int,
        spin_count: int,
        momentum: float,
        coordinate_frame: str,
        energy_reference: str,
    ) -> SupercellBasis:
        """Describe one comparison-critical synthetic supercell representation."""
        return SupercellBasis(
            state_space_id=(
                "low-pair-orbital-supercell"
                if spin_count == 1
                else "low-pair-orbital-supercell-x-spin-half"
            ),
            cell_count=cell_count,
            orbital_count=2,
            spin_count=spin_count,
            reduced_momentum=momentum,
            site_ordering="canonical-cyclic-sites",
            orbital_ordering="low-pair-smooth-frame",
            spin_ordering=("not-applicable" if spin_count == 1 else "up-down-fast"),
            coordinate_frame=coordinate_frame,
            energy_unit="E_G",
            energy_reference=energy_reference,
            geometry_id=f"one-dimensional-supercell-{cell_count}",
            subspace_id="accepted-low-pair-composite",
        )
