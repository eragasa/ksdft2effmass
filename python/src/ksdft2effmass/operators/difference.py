r"""Represented operator differences for compatible operator records.

This module owns the public represented-difference validation surface in the
comparison decomposition
``compatibility -> represented difference -> residual analysis -> comparison
Workflow``.  It depends only on ``records.py`` and ``compatibility.py``.  A
represented difference is the finite matrix

.. math::

   \Delta\mathbf H = \mathbf H_{\mathrm{candidate}} - \mathbf H_{\mathrm{reference}}

formed after exact compatibility succeeds.  It is not automatically an impurity
operator; impurity interpretation would require additional physical assumptions,
alignment procedures, and validation outside this task.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import cast

import numpy as np
import numpy.typing as npt

from .compatibility import (
    OperatorRecordCompatibilityAnalyzer,
    OperatorRecordCompatibilityResult,
)
from .records import OperatorRecord

ComplexMatrix = npt.NDArray[np.complex128]


@dataclass(frozen=True, slots=True, eq=False)
class OperatorRecordDifferenceResult:
    """Immutable represented difference in an already-compatible basis.

    Parameters
    ----------
    compatibility_result
        Compatible structured audit result for the reference and candidate
        records.  The result records a compatible audit state and supplies
        public identifiers; it does not store the matrix dimension or prove how
        a directly constructed difference matrix was computed.
    matrix
        Exact ``np.ndarray`` finite square ``np.complex128`` represented matrix
        for ``candidate - reference``.  Constructor storage is copied in C order
        into an owned immutable bytes-backed ``np.ndarray``, so callers cannot
        restore writeability by ``setflags(write=True)``.
    energy_unit
        Nonempty unit string for every matrix entry.  No unit conversion is
        performed.

    Notes
    -----
    The matrix is expressed in the already-compatible common representation, but
    this ResultObject is not a complete independently serializable
    ``OperatorRecord`` and has no JSON contract in this version.  It is a public
    Python/Rust boundary for residual analysis. Future block- or shell-resolved
    analyzers may consume this object, but those analyses are not implemented by
    this subsystem. The object is intentionally unhashable because it owns
    array-valued exact state and no safe exact hash is implemented.
    ``OperatorRecordDifferencer.execute()`` establishes
    operational provenance and the sign convention for produced results. Direct
    ResultObject construction validates only intrinsic stored state and cannot
    reconstruct or independently prove the source subtraction.
    """

    compatibility_result: OperatorRecordCompatibilityResult
    matrix: ComplexMatrix
    energy_unit: str

    def __post_init__(self) -> None:
        """Validate compatibility, matrix, and unit fields.

        Raises
        ------
        TypeError
            If ``compatibility_result`` is not an
            :class:`OperatorRecordCompatibilityResult`, ``energy_unit`` is not a
            string, or ``matrix`` is not an exact ``np.ndarray`` with dtype
            ``np.complex128``.
        ValueError
            If the compatibility result is incompatible, ``energy_unit`` is
            empty, or ``matrix`` is nonsquare, empty, or nonfinite.

        Notes
        -----
        This private dataclass hook implements intrinsic constructor validation
        owned by ``OperatorRecordDifferenceResult``. It does not call private
        ``OperatorRecord`` validators and does not apply numerical comparison
        policy. The final array copy uses immutable bytes-backed storage so the
        public matrix cannot be made writeable with ``setflags(write=True)``.
        """

        if not isinstance(self.compatibility_result, OperatorRecordCompatibilityResult):
            msg = "compatibility_result must be an OperatorRecordCompatibilityResult"
            raise TypeError(msg)
        if not self.compatibility_result.is_compatible:
            msg = "compatibility_result must be compatible"
            raise ValueError(msg)
        if not isinstance(self.energy_unit, str):
            msg = "energy_unit must be a string"
            raise TypeError(msg)
        if self.energy_unit == "":
            msg = "energy_unit must not be empty"
            raise ValueError(msg)
        if type(self.matrix) is not np.ndarray:
            msg = "matrix must be an exact NumPy ndarray"
            raise TypeError(msg)
        if self.matrix.dtype != np.dtype(np.complex128):
            msg = "matrix must have dtype np.complex128"
            raise TypeError(msg)
        if self.matrix.ndim != 2 or self.matrix.shape[0] != self.matrix.shape[1]:
            msg = "matrix must be a finite square complex128 matrix"
            raise ValueError(msg)
        if not np.all(np.isfinite(self.matrix)):
            msg = "matrix must be finite"
            raise ValueError(msg)
        if self.matrix.shape[0] <= 0:
            msg = "matrix dimension must be positive"
            raise ValueError(msg)
        # Copy through immutable bytes so public callers cannot make storage
        # writeable later with ndarray.setflags(write=True).
        immutable_matrix = cast(
            ComplexMatrix,
            np.frombuffer(self.matrix.tobytes(order="C"), dtype=np.complex128).reshape(
                self.matrix.shape,
                order="C",
            ),
        )
        object.__setattr__(self, "matrix", immutable_matrix)

    @property
    def reference_identifier(self) -> str:
        """Identifier of the reference record from the compatibility audit."""

        return self.compatibility_result.reference_identifier

    @property
    def candidate_identifier(self) -> str:
        """Identifier of the candidate record from the compatibility audit."""

        return self.compatibility_result.candidate_identifier

    @property
    def shape(self) -> tuple[int, int]:
        """Square matrix shape of the represented difference."""

        return self.matrix.shape

    @property
    def matrix_dimension(self) -> int:
        """Positive represented matrix dimension."""

        return self.matrix.shape[0]

    def __eq__(self, other: object) -> bool:
        """Return exact equality for public metadata and matrix entries."""

        if not isinstance(other, OperatorRecordDifferenceResult):
            return NotImplemented
        return (
            self.compatibility_result == other.compatibility_result
            and self.energy_unit == other.energy_unit
            and np.array_equal(self.matrix, other.matrix)
        )

    __hash__ = None  # type: ignore[assignment]


class OperatorRecordDifferenceNumericalErrorCode(StrEnum):
    """Stable represented-difference numerical-error categories.

    Attributes
    ----------
    NONFINITE_DIFFERENCE
        Subtracting two finite compatible matrices produced at least one
        nonfinite entry in the represented difference. This belongs to
        differencing, not residual-metric analysis.
    """

    NONFINITE_DIFFERENCE = "nonfinite_difference"


class OperatorRecordDifferenceNumericalError(ValueError):
    """Raised when represented matrix subtraction fails numerically.

    Parameters
    ----------
    code
        Closed structured enum code for the difference failure. Only
        :class:`OperatorRecordDifferenceNumericalErrorCode` values are accepted;
        arbitrary strings are rejected so the public Python exception maps to a
        future Rust error enum without string parsing.

    Attributes
    ----------
    code
        Public structured represented-difference numerical error code.

    Raises
    ------
    TypeError
        If ``code`` is not an
        :class:`OperatorRecordDifferenceNumericalErrorCode`.
    """

    code: OperatorRecordDifferenceNumericalErrorCode

    def __init__(self, code: OperatorRecordDifferenceNumericalErrorCode) -> None:
        """Retain the structured enum code without string coercion."""

        if not isinstance(code, OperatorRecordDifferenceNumericalErrorCode):
            msg = (
                "difference numerical-error code must be an "
                "OperatorRecordDifferenceNumericalErrorCode"
            )
            raise TypeError(msg)
        self.code = code
        super().__init__(f"operator-record difference numerical failure: {code.value}")


@dataclass(frozen=True, slots=True)
class OperatorRecordDifferencer:
    r"""ActionObject that forms ``candidate - reference`` for compatible records.

    Parameters
    ----------
    compatibility_analyzer
        Public compatibility analyzer dependency. Its ``require()`` method owns
        complete compatibility auditing and structured incompatible-record
        errors. The differencer uses it before any matrix subtraction.

    Attributes
    ----------
    compatibility_analyzer
        Frozen dependency used for exact representation compatibility. It is an
        explicit field to make the operation boundary portable to a Rust struct
        with an analyzer member and an ``execute`` method returning ``Result``.

    Raises
    ------
    TypeError
        If ``compatibility_analyzer`` is not an
        :class:`OperatorRecordCompatibilityAnalyzer`.

    Notes
    -----
    This ActionObject owns the sign convention
    :math:`\Delta\mathbf H = \mathbf H_{\mathrm{candidate}} -
    \mathbf H_{\mathrm{reference}}`, subtraction-overflow handling, nonfinite
    difference detection, and construction of
    :class:`OperatorRecordDifferenceResult`. It performs no residual norm
    calculation and makes no impurity-operator interpretation.
    """

    compatibility_analyzer: OperatorRecordCompatibilityAnalyzer = field(
        default_factory=OperatorRecordCompatibilityAnalyzer
    )

    def __post_init__(self) -> None:
        """Validate the compatibility analyzer dependency.

        Raises
        ------
        TypeError
            If ``compatibility_analyzer`` is not an
            :class:`OperatorRecordCompatibilityAnalyzer`.

        Notes
        -----
        This private dataclass hook enforces only the explicit ActionObject
        dependency boundary. Compatibility policy remains on the analyzer and
        represented subtraction remains on :meth:`execute`.
        """

        if not isinstance(
            self.compatibility_analyzer, OperatorRecordCompatibilityAnalyzer
        ):
            msg = (
                "compatibility_analyzer must be an OperatorRecordCompatibilityAnalyzer"
            )
            raise TypeError(msg)

    def execute(
        self, reference: OperatorRecord, candidate: OperatorRecord
    ) -> OperatorRecordDifferenceResult:
        r"""Return the represented difference ``candidate.matrix - reference.matrix``.

        Parameters
        ----------
        reference
            Reference :class:`OperatorRecord`. Its matrix is subtracted from the
            candidate matrix and its energy unit is the common unit after
            compatibility succeeds.
        candidate
            Candidate :class:`OperatorRecord`. Its matrix provides the positive
            term in the represented difference.

        Returns
        -------
        OperatorRecordDifferenceResult
            Immutable represented operator difference with compatible audit
            result, bytes-backed ``np.complex128`` matrix, and common energy
            unit.

        Raises
        ------
        TypeError
            If either input is not an :class:`OperatorRecord`, as enforced by
            the compatibility analyzer.
        IncompatibleOperatorRecordsError
            If the complete compatibility audit finds any mismatch.
        OperatorRecordDifferenceNumericalError
            If subtraction overflow or invalid arithmetic produces a nonfinite
            represented difference entry.
        """

        compatibility_result = self.compatibility_analyzer.require(reference, candidate)
        # NumPy overflow and invalid-operation warnings are converted into a
        # structured public finite-difference check below rather than leaking
        # warning policy to callers.
        with np.errstate(over="ignore", invalid="ignore"):
            difference_matrix = candidate.matrix - reference.matrix
        # The represented-difference subsystem owns only finite subtraction;
        # residual metric nonfiniteness is checked later by residual analysis.
        if not np.all(np.isfinite(difference_matrix)):
            raise OperatorRecordDifferenceNumericalError(
                OperatorRecordDifferenceNumericalErrorCode.NONFINITE_DIFFERENCE
            )
        # Result construction owns storage immutability and shape/dtype checks.
        return OperatorRecordDifferenceResult(
            compatibility_result=compatibility_result,
            matrix=np.asarray(difference_matrix, dtype=np.complex128),
            energy_unit=reference.energy_reference.unit,
        )
