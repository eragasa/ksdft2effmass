"""Typed synthetic fixtures for public ``OperatorRecord`` software evidence.

The helpers in this module construct only public operator-record DataObjects.
They pass caller inputs through without hidden matrix coercion, preserve an
explicitly empty provenance mapping, and provide deterministic defaults only for
arguments equal to ``None``. All values are synthetic software fixtures: no DFT,
Wannier, experimental, or impurity calculation supplies them, and successful
construction establishes no physical validity, scientific validation,
uncertainty quantification, or Rust conformance.
"""

from collections.abc import Mapping, Sequence
from typing import Any

import numpy as np

from ksdft2effmass.operators import (
    Basis,
    EnergyReference,
    Geometry,
    OperatorRecord,
    StateSpace,
)

type MatrixScalar = (
    int
    | float
    | complex
    | np.integer[Any]
    | np.floating[Any]
    | np.complexfloating[Any, Any]
)
type MatrixRowInput = tuple[MatrixScalar, ...] | list[MatrixScalar]
type MatrixSequenceInput = tuple[MatrixRowInput, ...] | list[MatrixRowInput]
type MatrixInput = MatrixSequenceInput | np.ndarray[Any, Any]

VALID_CELL = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))


def make_state_space(
    *,
    dimension: int = 2,
    identifier: str = "H_test",
) -> StateSpace:
    """Construct synthetic finite state-space metadata.

    Requirement
        OperatorRecord fixtures use an independently valid public StateSpace.
    Method
        Supply the explicit identifier and dimension unchanged with kind
        ``"finite synthetic"``.
    Oracle
        The approved StateSpace constructor owns its intrinsic invariants.
    Interpretation
        The result provides typed dependency metadata for OperatorRecord tests.
    Limitations
        The helper performs no matrix inference, DFT, Wannier, experimental, or
        impurity calculation and establishes no physical/scientific validity,
        scientific validation, UQ, or Rust conformance.
    """

    return StateSpace(identifier, "finite synthetic", dimension)


def make_basis(
    *,
    ordering: Sequence[str] = ("a", "b"),
    orthonormal: bool = True,
    identifier: str = "canonical",
) -> Basis:
    """Construct synthetic ordered-basis metadata.

    Requirement
        OperatorRecord fixtures use an independently valid Basis with explicit
        ordering and orthonormality metadata.
    Method
        Pass identifier, ordering, and orthonormality unchanged with deterministic
        kind ``"test basis"``.
    Oracle
        The approved Basis constructor owns sequence canonicalization and its
        intrinsic metadata invariants.
    Interpretation
        The result provides typed dependency metadata without modifying frozen
        state or numerically checking orthogonality.
    Limitations
        No basis vectors, DFT, Wannier, experimental, or impurity calculation are
        supplied; no physical/scientific validity, scientific validation, UQ, or
        Rust conformance is established.
    """

    return Basis(identifier, "test basis", ordering, orthonormal)


def make_geometry(*, system: str = "synthetic") -> Geometry:
    """Construct synthetic finite-cell metadata.

    Requirement
        OperatorRecord fixtures use an independently valid public Geometry.
    Method
        Pass the system unchanged and supply the exact identity cell,
        ``"finite synthetic"`` boundary conditions, Cartesian row-vector
        convention, and ``"angstrom"`` label.
    Oracle
        The approved Geometry constructor owns cell and metadata invariants.
    Interpretation
        The result supplies deterministic represented geometry metadata.
    Limitations
        It performs no normalization, conversion, DFT, Wannier, experimental, or
        impurity calculation and establishes no physical/scientific validity,
        scientific validation, UQ, or Rust conformance.
    """

    return Geometry(
        system,
        VALID_CELL,
        "finite synthetic",
        "cartesian row lattice vectors",
        "angstrom",
    )


def make_energy_reference(
    *,
    zero: str = "explicit zero",
    unit: str = "eV",
) -> EnergyReference:
    """Construct synthetic textual energy-reference metadata.

    Requirement
        OperatorRecord fixtures use an independently valid EnergyReference.
    Method
        Pass the explicit zero-convention and unit strings unchanged.
    Oracle
        The approved EnergyReference constructor owns its intrinsic string
        invariants and performs no conversion.
    Interpretation
        The result supplies deterministic represented energy metadata.
    Limitations
        No normalization, conversion, DFT, Wannier, experimental, or impurity
        calculation occurs; no physical/scientific validity, scientific
        validation, UQ, or Rust conformance is established.
    """

    return EnergyReference(zero, unit)


def make_record(
    matrix: MatrixInput | None = None,
    *,
    identifier: str = "synthetic-two-level",
    operator_kind: str = "finite_test_hamiltonian",
    state_space: StateSpace | None = None,
    basis: Basis | None = None,
    geometry: Geometry | None = None,
    energy_reference: EnergyReference | None = None,
    provenance: Mapping[str, str] | None = None,
) -> OperatorRecord:
    """Construct a public synthetic ``OperatorRecord`` without hidden coercion.

    Requirement
        Valid fixtures expose every record dependency and preserve caller matrix
        and provenance choices, including an explicitly empty mapping.
    Method
        Use a nested-list 2x2 matrix and typed public dependencies only when the
        corresponding argument is ``None``. Pass every non-``None`` input
        unchanged to ``OperatorRecord``. Provenance uses an explicit ``is None``
        branch rather than truth-value fallback.
    Oracle
        The approved eight-field OperatorRecord contract owns matrix
        canonicalization, dependency relations, and defensive copying.
    Interpretation
        The helper creates independently reproducible synthetic software state
        while leaving the behavior under test visible at the public constructor.
    Limitations
        It does not call ``np.asarray`` or pre-coerce matrix values, infer
        dependency dimensions from malformed matrices, mutate frozen objects,
        normalize values, or perform DFT, Wannier, experimental, or impurity
        calculations. Construction establishes no physical/scientific validity,
        scientific validation, UQ, or Rust conformance.
    """

    if matrix is None:
        matrix = [[1.0, 0.25j], [-0.25j, 2.0]]
    if state_space is None:
        state_space = make_state_space()
    if basis is None:
        basis = make_basis()
    if geometry is None:
        geometry = make_geometry()
    if energy_reference is None:
        energy_reference = make_energy_reference()
    if provenance is None:
        provenance = {"source": "unit test"}
    return OperatorRecord(
        identifier=identifier,
        operator_kind=operator_kind,
        matrix=matrix,
        state_space=state_space,
        basis=basis,
        geometry=geometry,
        energy_reference=energy_reference,
        provenance=provenance,
    )
