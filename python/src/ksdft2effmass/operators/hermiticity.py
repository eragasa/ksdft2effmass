r"""Unit-bearing Hermiticity analysis for finite operator records.

Hermiticity is measured for a fixed matrix representation ``H`` by

.. math::

   \varepsilon_{\mathrm H} = \max_{i,j} |H_{ij} - H_{ji}^*|.

The residual has the same dimensional energy unit as the represented matrix.
Exact Hermiticity is invariant under unitary basis transformations. For a
numerically non-Hermitian matrix, however, this entrywise maximum residual is
generally basis-dependent. The analyzer is therefore a fixed-representation
software-verification policy; it performs no unit conversion and does not
scientifically validate an electronic-structure calculation or reduced model.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from typing import Any

    # Constructor inputs intentionally include the runtime-admitted Python and
    # NumPy real-scalar families. Boolean remains a runtime-rejected semantic
    # refinement because static integer typing cannot precisely exclude it.
    type _HermiticityRealScalarInput = int | float | np.integer[Any] | np.floating[Any]

from .records import OperatorRecord


class HermiticityUnitMismatchError(ValueError):
    """Raised when analyzer and record energy-unit strings differ exactly.

    Parameters
    ----------
    analyzer_energy_unit
        Nonempty unit string configured on the :class:`HermiticityAnalyzer`.
        The Analyzer tolerance is interpreted in this unit.
    record_energy_unit
        Nonempty unit string stored on ``record.energy_reference.unit``. The
        represented matrix and Hermiticity residual use this unit.

    Attributes
    ----------
    analyzer_energy_unit
        Public retained Analyzer-policy unit for structured inspection.
    record_energy_unit
        Public retained record-metadata unit for structured inspection.

    Raises
    ------
    TypeError
        If either unit is not a string under the public string-type policy.
    ValueError
        If either string is empty or the two strings are equal.

    Notes
    -----
    Comparison is exact and case-sensitive. The exception performs no trimming,
    normalization, unit conversion, registry lookup, dimensional analysis, or
    physical-unit validation. It represents only the structured disagreement
    ``analyzer_energy_unit != record_energy_unit``.
    """

    analyzer_energy_unit: str
    record_energy_unit: str

    def __init__(self, analyzer_energy_unit: str, record_energy_unit: str) -> None:
        """Validate and retain both ordered unit roles.

        Parameters
        ----------
        analyzer_energy_unit
            Candidate nonempty Analyzer-policy unit string.
        record_energy_unit
            Candidate nonempty record-metadata unit string.

        Raises
        ------
        TypeError
            If either value is not a string.
        ValueError
            If either string is empty or both strings are exactly equal.
        """

        if not isinstance(analyzer_energy_unit, str):
            msg = "analyzer energy unit must be a string"
            raise TypeError(msg)
        if not isinstance(record_energy_unit, str):
            msg = "record energy unit must be a string"
            raise TypeError(msg)
        if analyzer_energy_unit == "":
            msg = "analyzer energy unit must not be empty"
            raise ValueError(msg)
        if record_energy_unit == "":
            msg = "record energy unit must not be empty"
            raise ValueError(msg)
        if analyzer_energy_unit == record_energy_unit:
            msg = "analyzer and record energy units must differ"
            raise ValueError(msg)

        self.analyzer_energy_unit = analyzer_energy_unit
        self.record_energy_unit = record_energy_unit
        super().__init__(
            "Hermiticity analyzer energy unit "
            f"{analyzer_energy_unit!r} does not match record energy unit "
            f"{record_energy_unit!r}"
        )


class HermiticityNumericalErrorCode(StrEnum):
    """Stable structured Hermiticity numerical-error categories.

    Attributes
    ----------
    NONFINITE_RESIDUAL
        Matrix subtraction or residual reduction produced a nonfinite residual.
    """

    NONFINITE_RESIDUAL = "nonfinite_residual"


class HermiticityNumericalError(ValueError):
    """Raised when Hermiticity residual computation fails numerically.

    Parameters
    ----------
    reason
        Stable public enum category describing the numerical failure.  Arbitrary
        strings and string values of enum members are rejected rather than
        coerced so callers can rely on a closed structured error set.

    Attributes
    ----------
    reason
        Public structured enum reason for inspection without parsing message
        text.
    """

    reason: HermiticityNumericalErrorCode

    def __init__(self, reason: HermiticityNumericalErrorCode) -> None:
        """Store the structured enum reason and build a concise diagnostic."""

        if not isinstance(reason, HermiticityNumericalErrorCode):
            msg = (
                "Hermiticity numerical-error reason must be a "
                "HermiticityNumericalErrorCode"
            )
            raise TypeError(msg)
        self.reason = reason
        super().__init__(f"Hermiticity numerical failure: {reason.value}")


class HermiticityRequirementError(ValueError):
    """Raised when :meth:`HermiticityAnalyzer.require` rejects a record.

    Parameters
    ----------
    result
        Structured Hermiticity result whose ``is_hermitian`` property is false.

    Attributes
    ----------
    result
        Public retained failed :class:`HermiticityResult`; callers inspect this
        object instead of parsing exception-message text.

    Raises
    ------
    TypeError
        If ``result`` is not a :class:`HermiticityResult`.
    ValueError
        If ``result.is_hermitian`` is true. This exception represents only a
        failed requirement, so retaining a successful result would create
        contradictory public state.
    """

    result: HermiticityResult

    def __init__(self, result: HermiticityResult) -> None:
        """Retain the structured result and build a concise message."""

        if not isinstance(result, HermiticityResult):
            msg = "result must be a HermiticityResult"
            raise TypeError(msg)
        if result.is_hermitian:
            msg = "result must be a failed HermiticityResult"
            raise ValueError(msg)
        self.result = result
        super().__init__("operator matrix is not Hermitian within tolerance")


@dataclass(frozen=True, slots=True)
class HermiticityResult:
    """Immutable result of unit-bearing Hermiticity analysis.

    Parameters
    ----------
    residual
        Non-negative residual :math:`\\varepsilon_{\\mathrm H}` in ``energy_unit``.
        Python and NumPy integer or floating scalars are accepted and
        canonicalized to built-in ``float``; booleans, strings, bytes, complex
        values, nonfinite values, and negative values are rejected.
    tolerance
        Non-negative acceptance tolerance in ``energy_unit``. Accepted scalar
        types and canonicalization match ``residual``.
    energy_unit
        Nonempty string naming the dimensional energy unit shared by ``residual``
        and ``tolerance``.
    """

    residual: float
    tolerance: float
    energy_unit: str

    if TYPE_CHECKING:

        def __init__(
            self,
            residual: _HermiticityRealScalarInput,
            tolerance: _HermiticityRealScalarInput,
            energy_unit: str,
        ) -> None:
            """Declare admitted constructor inputs without changing runtime.

            Python and NumPy integer and floating scalars are accepted at the
            constructor boundary and canonicalized to the stored ``float``
            attributes by ``__post_init__``. Boolean values remain rejected by
            runtime semantic validation even though static integer typing cannot
            express that exclusion precisely. The dataclass generates the actual
            runtime constructor because this declaration exists only during
            static type checking.
            """

    def __post_init__(self) -> None:
        """Canonicalize scalar and unit fields and enforce non-negativity."""

        residual = self._finite_real(self.residual, "Hermiticity residual")
        tolerance = self._finite_real(self.tolerance, "Hermiticity tolerance")
        self._require_string(self.energy_unit, "Hermiticity energy unit")
        if residual < 0.0:
            msg = "Hermiticity residual must be non-negative"
            raise ValueError(msg)
        if tolerance < 0.0:
            msg = "Hermiticity tolerance must be non-negative"
            raise ValueError(msg)
        object.__setattr__(self, "residual", residual)
        object.__setattr__(self, "tolerance", tolerance)

    @property
    def is_hermitian(self) -> bool:
        """Whether ``residual <= tolerance`` for this unit-bearing result."""

        return self.residual <= self.tolerance

    @staticmethod
    def _finite_real(value: object, name: str) -> float:
        """Return a canonical finite real scalar owned by this result.

        Parameters
        ----------
        value
            Candidate public scalar. Python and NumPy integer and floating
            scalars are accepted; booleans, strings, bytes, complex values, and
            arbitrary coercible objects are rejected.
        name
            Diagnostic field name used in structured exception messages.

        Returns
        -------
        float
            Built-in finite float for the immutable Python/Rust boundary.

        Raises
        ------
        TypeError
            If ``value`` is not an accepted real scalar type.
        ValueError
            If conversion overflows or produces a nonfinite value.
        """

        if isinstance(
            value, bool | np.bool_ | str | bytes | complex | np.complexfloating
        ):
            msg = f"{name} must be a real number"
            raise TypeError(msg)
        if not isinstance(value, int | float | np.integer | np.floating):
            msg = f"{name} must be a real number"
            raise TypeError(msg)
        try:
            real = float(value)
        except OverflowError as exc:
            msg = f"{name} must be finite"
            raise ValueError(msg) from exc
        if not np.isfinite(real):
            msg = f"{name} must be finite"
            raise ValueError(msg)
        return real

    @staticmethod
    def _require_string(value: object, name: str) -> None:
        """Validate a nonempty string field owned by this result.

        Parameters
        ----------
        value
            Candidate unit string. Only Python strings are accepted.
        name
            Diagnostic field name.

        Raises
        ------
        TypeError
            If ``value`` is not a string.
        ValueError
            If ``value`` is empty.

        Notes
        -----
        This private method is owner-local ResultObject validation and does not
        perform unit conversion or parse unit syntax. It is private because only
        ``HermiticityResult`` owns the invariant for its stored unit string.
        """

        if not isinstance(value, str):
            msg = f"{name} must be a string"
            raise TypeError(msg)
        if value == "":
            msg = f"{name} must not be empty"
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class HermiticityAnalyzer:
    """ActionObject for fixed-representation Hermiticity analysis.

    Parameters
    ----------
    tolerance
        Non-negative finite tolerance :math:`\\tau` in ``energy_unit``. Python
        and NumPy integer or floating scalars are accepted and canonicalized to
        built-in ``float``. Booleans remain a runtime-rejected semantic
        refinement because static integer typing cannot express their exclusion
        precisely.
    energy_unit
        Required nonempty energy-unit string. It must exactly equal
        ``record.energy_reference.unit`` when a record is analyzed. No automatic
        unit conversion is authorized.
    """

    tolerance: float
    energy_unit: str

    if TYPE_CHECKING:

        def __init__(
            self,
            tolerance: _HermiticityRealScalarInput,
            energy_unit: str,
        ) -> None:
            """Declare admitted tolerance inputs without changing runtime.

            Python and NumPy integer and floating scalars are accepted at the
            constructor boundary and canonicalized to the stored ``float``
            attribute by ``__post_init__``. Boolean values remain rejected by
            runtime semantic validation even though static integer typing cannot
            express that exclusion precisely. The dataclass generates the actual
            runtime constructor because this declaration exists only during
            static type checking.
            """

    def __post_init__(self) -> None:
        """Canonicalize analyzer-owned tolerance and validate its unit."""

        tolerance = self._finite_real(self.tolerance, "Hermiticity tolerance")
        self._require_string(self.energy_unit, "Hermiticity energy unit")
        if tolerance < 0.0:
            msg = "Hermiticity tolerance must be non-negative"
            raise ValueError(msg)
        object.__setattr__(self, "tolerance", tolerance)

    @staticmethod
    def _finite_real(value: object, name: str) -> float:
        """Return a canonical finite real tolerance owned by this analyzer.

        Parameters
        ----------
        value
            Candidate tolerance scalar. Python and NumPy integer and floating
            scalars are accepted; booleans, numeric strings, complex values, and
            arbitrary coercible objects are rejected at the public boundary.
        name
            Diagnostic field name used in exceptions.

        Returns
        -------
        float
            Built-in finite tolerance in ``energy_unit``.

        Raises
        ------
        TypeError
            If ``value`` is not an accepted real scalar type.
        ValueError
            If conversion overflows or produces a nonfinite value.
        """

        if isinstance(
            value, bool | np.bool_ | str | bytes | complex | np.complexfloating
        ):
            msg = f"{name} must be a real number"
            raise TypeError(msg)
        if not isinstance(value, int | float | np.integer | np.floating):
            msg = f"{name} must be a real number"
            raise TypeError(msg)
        try:
            real = float(value)
        except OverflowError as exc:
            msg = f"{name} must be finite"
            raise ValueError(msg) from exc
        if not np.isfinite(real):
            msg = f"{name} must be finite"
            raise ValueError(msg)
        return real

    @staticmethod
    def _require_string(value: object, name: str) -> None:
        """Validate a nonempty string field owned by this analyzer.

        Parameters
        ----------
        value
            Candidate analyzer energy-unit string. Only Python strings are
            accepted.
        name
            Diagnostic field name.

        Raises
        ------
        TypeError
            If ``value`` is not a string.
        ValueError
            If ``value`` is empty.

        Notes
        -----
        This private method is owner-local ActionObject policy validation. It
        does not perform unit conversion or parse unit syntax. It is private
        because only ``HermiticityAnalyzer`` owns the configured policy unit.
        """

        if not isinstance(value, str):
            msg = f"{name} must be a string"
            raise TypeError(msg)
        if value == "":
            msg = f"{name} must not be empty"
            raise ValueError(msg)

    def execute(self, record: OperatorRecord) -> HermiticityResult:
        """Analyze one ``OperatorRecord`` and return a unit-bearing result.

        Parameters
        ----------
        record
            Operator record whose matrix is tested in its fixed representation.
            Its energy unit must exactly match ``self.energy_unit``.

        Returns
        -------
        HermiticityResult
            Residual, tolerance, and energy unit for this fixed-representation
            software-verification policy.

        Raises
        ------
        TypeError
            If ``record`` is not an :class:`OperatorRecord`.
        HermiticityUnitMismatchError
            If ``self.energy_unit`` differs exactly from
            ``record.energy_reference.unit``.
        HermiticityNumericalError
            If finite public record inputs produce a nonfinite residual
            intermediate, for example through floating-point subtraction
            overflow.
        """

        if not isinstance(record, OperatorRecord):
            msg = "Hermiticity analysis requires an OperatorRecord"
            raise TypeError(msg)
        if self.energy_unit != record.energy_reference.unit:
            raise HermiticityUnitMismatchError(
                analyzer_energy_unit=self.energy_unit,
                record_energy_unit=record.energy_reference.unit,
            )
        with np.errstate(over="ignore", invalid="ignore"):
            # The residual matrix is an internal fixed-representation software
            # check; it is not exposed as an operator-difference object.
            residual_matrix = record.matrix - record.matrix.conj().T
        if not np.all(np.isfinite(residual_matrix)):
            raise HermiticityNumericalError(
                HermiticityNumericalErrorCode.NONFINITE_RESIDUAL
            )
        # The entrywise maximum absolute residual is epsilon_H in the record's
        # energy unit and is basis-dependent for non-Hermitian matrices.
        residual = float(np.max(np.abs(residual_matrix)))
        if not np.isfinite(residual):
            raise HermiticityNumericalError(
                HermiticityNumericalErrorCode.NONFINITE_RESIDUAL
            )
        return HermiticityResult(
            residual=residual,
            tolerance=self.tolerance,
            energy_unit=self.energy_unit,
        )

    def require(self, record: OperatorRecord) -> HermiticityResult:
        """Return an accepted result or raise a structured requirement error.

        Parameters
        ----------
        record
            Operator record analyzed by :meth:`execute`.

        Returns
        -------
        HermiticityResult
            The accepted result when ``result.is_hermitian`` is true.

        Raises
        ------
        TypeError
            If ``record`` is not an :class:`OperatorRecord`.
        HermiticityUnitMismatchError
            If analyzer and record energy units differ.
        HermiticityNumericalError
            If residual computation produces a nonfinite intermediate.
        HermiticityRequirementError
            If the result is not accepted; the exception retains the structured
            ``HermiticityResult``.
        """

        result = self.execute(record)
        if not result.is_hermitian:
            raise HermiticityRequirementError(result)
        return result
