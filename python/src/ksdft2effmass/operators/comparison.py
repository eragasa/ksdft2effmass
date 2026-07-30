r"""Compatibility analysis and residual comparison for operator records.

The objects in this module compare two already represented finite operator
matrices only after checking that their representation metadata make direct
matrix subtraction meaningful.  Compatibility is a software precondition for
forming a represented residual matrix; it is not equality of complete records,
basis alignment, energy alignment, gauge alignment, geometry alignment,
normalization, serialization compatibility, or a scientific acceptance rule.

Version-1 compatibility compares matrix dimension, state-space kind, operator
kind, ordered basis labels, basis kind, lattice
vectors, boundary conditions, coordinate convention, geometry length unit,
energy unit, and energy-zero convention.  It deliberately ignores identity and
provenance fields such as record identifiers, state-space identifiers, basis
identifiers, geometry system names, and provenance mappings because those fields
identify where represented data came from rather than whether the two finite
matrix representations can be subtracted.

For compatible records an implementation may form

.. math::

   \Delta\mathbf H
   =
   \mathbf H_{\mathrm{candidate}}
   -
   \mathbf H_{\mathrm{reference}}.

The public result does not expose this signed matrix.  It exposes only three
symmetric residual norms in the common energy unit:

.. math::

   \varepsilon_{\max}
   =
   \max_{i,j}|\Delta H_{ij}|,

.. math::

   \varepsilon_{\mathrm F}
   =
   \left(\sum_{i,j}|\Delta H_{ij}|^2\right)^{1/2},

and

.. math::

   \varepsilon_2
   =
   \sigma_{\max}(\Delta\mathbf H).

Because these are norms, exchanging reference and candidate swaps identifiers
while preserving metric values.  The entrywise maximum residual is basis
dependent.  The Frobenius norm and induced matrix 2-norm are invariant under a
common unitary transformation of both represented matrices, but that invariance
does not align different bases.  The Frobenius norm generally scales with matrix
dimension.  None of the metrics establishes scientific acceptability of a DFT
calculation, a reduced model, or an effective-mass approximation; they are
software-verification quantities for already-compatible finite representations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import ClassVar

import numpy as np

from .records import OperatorRecord


class OperatorRecordCompatibilityMismatchCode(StrEnum):
    """Stable mismatch codes in canonical version-1 audit order.

    Each member represents one exact compatibility rule.  Declaration order is
    the canonical rule order used by
    :class:`OperatorRecordCompatibilityAnalyzer` and exposed by
    :attr:`OperatorRecordCompatibilityResult.rules_applied` for deterministic
    audits.

    Attributes
    ----------
    MATRIX_DIMENSION_MISMATCH
        Matrix shapes, and therefore represented dimensions, differ.
    STATE_SPACE_KIND_MISMATCH
        State-space kind metadata differs.
    OPERATOR_KIND_MISMATCH
        Operator-kind metadata differs.
    ORDERED_BASIS_LABELS_MISMATCH
        Ordered basis labels differ, so matrix indices do not identify the same
        represented basis states.
    BASIS_KIND_MISMATCH
        Basis-kind metadata differs.
    LATTICE_VECTORS_MISMATCH
        Row lattice vectors differ exactly.
    BOUNDARY_CONDITIONS_MISMATCH
        Boundary-condition metadata differs.
    COORDINATE_CONVENTION_MISMATCH
        Coordinate-convention metadata differs.
    GEOMETRY_LENGTH_UNIT_MISMATCH
        Geometry length units differ.
    ENERGY_UNIT_MISMATCH
        Matrix energy units differ.
    ENERGY_ZERO_CONVENTION_MISMATCH
        Energy-zero conventions differ.
    """

    MATRIX_DIMENSION_MISMATCH = "matrix_dimension_mismatch"
    STATE_SPACE_KIND_MISMATCH = "state_space_kind_mismatch"
    OPERATOR_KIND_MISMATCH = "operator_kind_mismatch"
    ORDERED_BASIS_LABELS_MISMATCH = "ordered_basis_labels_mismatch"
    BASIS_KIND_MISMATCH = "basis_kind_mismatch"
    LATTICE_VECTORS_MISMATCH = "lattice_vectors_mismatch"
    BOUNDARY_CONDITIONS_MISMATCH = "boundary_conditions_mismatch"
    COORDINATE_CONVENTION_MISMATCH = "coordinate_convention_mismatch"
    GEOMETRY_LENGTH_UNIT_MISMATCH = "geometry_length_unit_mismatch"
    ENERGY_UNIT_MISMATCH = "energy_unit_mismatch"
    ENERGY_ZERO_CONVENTION_MISMATCH = "energy_zero_convention_mismatch"

    @property
    def description(self) -> str:
        """Canonical human-readable description for this mismatch code."""

        code = OperatorRecordCompatibilityMismatchCode
        descriptions = {
            code.MATRIX_DIMENSION_MISMATCH: "matrix dimensions must match exactly",
            code.STATE_SPACE_KIND_MISMATCH: "state-space kind must match exactly",
            code.OPERATOR_KIND_MISMATCH: "operator_kind must match exactly",
            code.ORDERED_BASIS_LABELS_MISMATCH: (
                "ordered basis labels must match exactly"
            ),
            code.BASIS_KIND_MISMATCH: "basis kind must match exactly",
            code.LATTICE_VECTORS_MISMATCH: "lattice vectors must match exactly",
            code.BOUNDARY_CONDITIONS_MISMATCH: (
                "boundary conditions must match exactly"
            ),
            code.COORDINATE_CONVENTION_MISMATCH: (
                "coordinate convention must match exactly"
            ),
            code.GEOMETRY_LENGTH_UNIT_MISMATCH: (
                "geometry length unit must match exactly"
            ),
            code.ENERGY_UNIT_MISMATCH: "energy unit must match exactly",
            code.ENERGY_ZERO_CONVENTION_MISMATCH: (
                "energy-zero convention must match exactly"
            ),
        }
        return descriptions[self]


@dataclass(frozen=True, slots=True)
class OperatorRecordCompatibilityIssue:
    """One immutable compatibility-rule failure.

    Parameters
    ----------
    code
        Stable machine-readable mismatch code for the failed version-1 rule.
        The code is the authoritative state.  The human-readable
        :attr:`description` is derived canonically from the code and is not a
        constructor argument.
    """

    code: OperatorRecordCompatibilityMismatchCode

    def __post_init__(self) -> None:
        """Validate that the public state is exactly one mismatch code."""

        if not isinstance(self.code, OperatorRecordCompatibilityMismatchCode):
            msg = (
                "compatibility issue code must be an "
                "OperatorRecordCompatibilityMismatchCode"
            )
            raise TypeError(msg)

    @property
    def description(self) -> str:
        """Canonical human-readable description derived from ``code``."""

        return self.code.description


@dataclass(frozen=True, slots=True)
class OperatorRecordCompatibilityResult:
    """Immutable audit result for exact representation compatibility.

    Parameters
    ----------
    reference_identifier
        Identifier of the reference record supplied to the analyzer or direct
        constructor.  It is provenance for the audit, not a compatibility rule.
    candidate_identifier
        Identifier of the candidate record supplied to the analyzer or direct
        constructor.  It is provenance for the audit, not a compatibility rule.
    issues
        Complete immutable collection of compatibility issues.  It must contain
        only :class:`OperatorRecordCompatibilityIssue` objects, no duplicated
        codes, codes only from the version-1 rule set, and canonical enum
        declaration order.

    Attributes
    ----------
    rules_applied
        Public read-only canonical version-1 rule sequence, always
        ``tuple(OperatorRecordCompatibilityMismatchCode)``.  It is derived from
        the public mismatch-code declaration rather than accepted as an
        arbitrary constructor argument.
    _RULES_APPLIED
        Private class-owned canonical tuple backing ``rules_applied``.  It is
        private so callers cannot confuse the storage detail with constructor
        state; it is immutable, deterministic, dimensionless, derived from the
        public enum declaration, and affects only compatibility-audit ordering.
    is_compatible
        Derived compatibility status.  It is ``True`` exactly when ``issues`` is
        empty, preventing contradictory compatibility state.

    Raises
    ------
    TypeError
        If identifiers are not strings, ``issues`` is not a tuple, or any issue
        is not an :class:`OperatorRecordCompatibilityIssue`.
    ValueError
        If an identifier is empty, issue codes are duplicated, issue ordering is
        noncanonical, or an issue code is outside the version-1 rule set.

    Notes
    -----
    The result has no JSON serialization contract in this version.  Determinism
    is provided by canonical rule and issue ordering.
    """

    reference_identifier: str
    candidate_identifier: str
    issues: tuple[OperatorRecordCompatibilityIssue, ...]

    _RULES_APPLIED: ClassVar[tuple[OperatorRecordCompatibilityMismatchCode, ...]] = (
        tuple(OperatorRecordCompatibilityMismatchCode)
    )

    def __post_init__(self) -> None:
        """Canonicalize issues and enforce compatibility-result invariants."""

        self._require_string(self.reference_identifier, "reference identifier")
        self._require_string(self.candidate_identifier, "candidate identifier")
        issues = self._canonicalize_issues(self.issues)
        self._validate_issues(issues, self.rules_applied)
        object.__setattr__(self, "issues", issues)

    @property
    def rules_applied(self) -> tuple[OperatorRecordCompatibilityMismatchCode, ...]:
        """Complete canonical version-1 compatibility-rule sequence."""

        return self._RULES_APPLIED

    @property
    def is_compatible(self) -> bool:
        """Whether the canonical issue collection is empty."""

        return len(self.issues) == 0

    @staticmethod
    def _canonicalize_issues(
        issues: tuple[OperatorRecordCompatibilityIssue, ...],
    ) -> tuple[OperatorRecordCompatibilityIssue, ...]:
        """Return an immutable issue tuple without reordering it.

        Parameters
        ----------
        issues
            Iterable supplied to the public constructor.  Strings, bytes, and
            non-iterable values are rejected because they cannot represent an
            issue collection.

        Returns
        -------
        tuple[OperatorRecordCompatibilityIssue, ...]
            Tuple preserving caller order for later canonical-order validation.

        Raises
        ------
        TypeError
            If ``issues`` is not an iterable collection of issue objects.

        Notes
        -----
        This private method is mechanical canonicalization owned by the result
        object.  It intentionally does not sort issues because noncanonical
        ordering is an auditable construction error.
        """

        if not isinstance(issues, tuple):
            msg = "compatibility issues must be a tuple of issues"
            raise TypeError(msg)
        # Preserve supplied ordering so invalid ordering remains detectable.
        return issues

    @staticmethod
    def _validate_issues(
        issues: tuple[OperatorRecordCompatibilityIssue, ...],
        rules_applied: tuple[OperatorRecordCompatibilityMismatchCode, ...],
    ) -> None:
        """Validate version-1 issue type, uniqueness, membership, and order.

        Parameters
        ----------
        issues
            Canonical tuple preserving direct-construction order.
        rules_applied
            Complete version-1 rule sequence used as the membership and order
            reference.

        Raises
        ------
        TypeError
            If an issue is not an :class:`OperatorRecordCompatibilityIssue`.
        ValueError
            If a code is duplicated, not part of the rule set, or out of
            canonical declaration order.

        Notes
        -----
        The method is private because it protects only the structural invariant
        of the containing ResultObject.  Compatibility science and public rule
        definitions are declared by the public enum and analyzer.
        """

        issue_codes: list[OperatorRecordCompatibilityMismatchCode] = []
        for issue in issues:
            if not isinstance(issue, OperatorRecordCompatibilityIssue):
                msg = (
                    "compatibility issues must be "
                    "OperatorRecordCompatibilityIssue values"
                )
                raise TypeError(msg)
            if issue.code not in rules_applied:
                msg = "compatibility issue code must be in rules_applied"
                raise ValueError(msg)
            if issue.code in issue_codes:
                msg = "compatibility issue codes must not be duplicated"
                raise ValueError(msg)
            # Keep the submitted code sequence for duplicate and ordering checks.
            issue_codes.append(issue.code)
        issue_code_set = set(issue_codes)
        canonical_issue_order = tuple(
            code for code in rules_applied if code in issue_code_set
        )
        if tuple(issue_codes) != canonical_issue_order:
            msg = "compatibility issues must follow canonical mismatch-code order"
            raise ValueError(msg)

    @staticmethod
    def _require_string(value: object, name: str) -> None:
        """Validate a nonempty string identifier owned by this result.

        Parameters
        ----------
        value
            Candidate identifier value.  Numeric strings are still strings and
            are not interpreted as numbers; non-string values are rejected.
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
        This private method is mechanical constructor validation for provenance
        identifiers, not compatibility or scientific policy.
        """

        if not isinstance(value, str):
            msg = f"{name} must be a string"
            raise TypeError(msg)
        if value == "":
            msg = f"{name} must not be empty"
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class OperatorRecordCompatibilityAnalyzer:
    """ActionObject for exact version-1 representation compatibility analysis.

    Attributes
    ----------
    RULES_APPLIED
        Class-owned canonical rule sequence equal to
        ``tuple(OperatorRecordCompatibilityMismatchCode)``.

    Notes
    -----
    The algorithm validates both inputs, evaluates every compatibility rule in
    canonical order, does not fail at the first mismatch, collects every failed
    rule, and constructs one immutable audit result.  It compares only fields
    required for direct subtraction of represented matrices.  It ignores record
    identifiers, state-space identifiers, basis identifiers, geometry system
    names, and provenance because those are identity/provenance fields rather
    than representation-compatibility fields.
    """

    RULES_APPLIED: ClassVar[tuple[OperatorRecordCompatibilityMismatchCode, ...]] = (
        tuple(OperatorRecordCompatibilityMismatchCode)
    )

    def execute(
        self, reference: OperatorRecord, candidate: OperatorRecord
    ) -> OperatorRecordCompatibilityResult:
        """Return complete exact compatibility audit for two records.

        Parameters
        ----------
        reference
            Reference represented operator record.
        candidate
            Candidate represented operator record.

        Returns
        -------
        OperatorRecordCompatibilityResult
            Immutable audit result with all failed compatibility rules in
            canonical order.

        Raises
        ------
        TypeError
            If either argument is not an :class:`OperatorRecord`.
        """

        self._require_operator_record(reference, "reference")
        self._require_operator_record(candidate, "candidate")
        # Collect every failed rule instead of failing immediately so callers
        # receive one complete, deterministic audit of representation
        # incompatibility.
        compatibility_issues: list[OperatorRecordCompatibilityIssue] = []
        for code, reference_value, candidate_value in (
            (
                OperatorRecordCompatibilityMismatchCode.MATRIX_DIMENSION_MISMATCH,
                reference.matrix.shape,
                candidate.matrix.shape,
            ),
            (
                OperatorRecordCompatibilityMismatchCode.STATE_SPACE_KIND_MISMATCH,
                reference.state_space.kind,
                candidate.state_space.kind,
            ),
            (
                OperatorRecordCompatibilityMismatchCode.OPERATOR_KIND_MISMATCH,
                reference.operator_kind,
                candidate.operator_kind,
            ),
            (
                OperatorRecordCompatibilityMismatchCode.ORDERED_BASIS_LABELS_MISMATCH,
                reference.basis.ordering,
                candidate.basis.ordering,
            ),
            (
                OperatorRecordCompatibilityMismatchCode.BASIS_KIND_MISMATCH,
                reference.basis.kind,
                candidate.basis.kind,
            ),
            (
                OperatorRecordCompatibilityMismatchCode.LATTICE_VECTORS_MISMATCH,
                reference.geometry.cell,
                candidate.geometry.cell,
            ),
            (
                OperatorRecordCompatibilityMismatchCode.BOUNDARY_CONDITIONS_MISMATCH,
                reference.geometry.boundary_conditions,
                candidate.geometry.boundary_conditions,
            ),
            (
                OperatorRecordCompatibilityMismatchCode.COORDINATE_CONVENTION_MISMATCH,
                reference.geometry.coordinate_convention,
                candidate.geometry.coordinate_convention,
            ),
            (
                OperatorRecordCompatibilityMismatchCode.GEOMETRY_LENGTH_UNIT_MISMATCH,
                reference.geometry.length_unit,
                candidate.geometry.length_unit,
            ),
            (
                OperatorRecordCompatibilityMismatchCode.ENERGY_UNIT_MISMATCH,
                reference.energy_reference.unit,
                candidate.energy_reference.unit,
            ),
            (
                OperatorRecordCompatibilityMismatchCode.ENERGY_ZERO_CONVENTION_MISMATCH,
                reference.energy_reference.zero,
                candidate.energy_reference.zero,
            ),
        ):
            # Exact equality is intentional: this analyzer does not own any
            # tolerance, alignment, unit-conversion, or approximate comparison
            # policy for representation metadata.
            if reference_value != candidate_value:
                compatibility_issues.append(OperatorRecordCompatibilityIssue(code=code))
        return OperatorRecordCompatibilityResult(
            reference_identifier=reference.identifier,
            candidate_identifier=candidate.identifier,
            issues=tuple(compatibility_issues),
        )

    @staticmethod
    def _require_operator_record(value: object, name: str) -> None:
        """Validate an analyzer input as an OperatorRecord.

        Parameters
        ----------
        value
            Candidate object supplied to the analyzer.
        name
            Diagnostic role name, either reference or candidate.

        Raises
        ------
        TypeError
            If ``value`` is not an :class:`OperatorRecord`.

        Notes
        -----
        This private method is a mechanical input-boundary check owned by the
        analyzer.  It is not a cross-object private call and does not implement
        compatibility policy.
        """

        if not isinstance(value, OperatorRecord):
            msg = f"{name} must be an OperatorRecord"
            raise TypeError(msg)


@dataclass(frozen=True, slots=True)
class OperatorRecordComparisonResult:
    """Immutable residual metrics for compatible operator records.

    Parameters
    ----------
    reference_identifier
        Identifier of the reference record.  It records comparison provenance
        and is not used in metric computation.
    candidate_identifier
        Identifier of the candidate record.  It records comparison provenance
        and is not used in metric computation.
    matrix_dimension
        Positive represented dimension ``N`` of the square matrices.  NumPy
        integer scalars are accepted and canonicalized to Python ``int``;
        booleans, strings, floats, complex values, and nonpositive integers are
        rejected.
    energy_unit
        Common energy unit of all three residual metrics.
    maximum_absolute_residual
        Entrywise maximum absolute residual, :math:`\\varepsilon_{\\max}`.  It is
        finite, non-negative, basis dependent, and expressed in ``energy_unit``.
    frobenius_residual
        Frobenius residual, :math:`\\varepsilon_{\\mathrm F}`.  It is finite,
        non-negative, invariant under a common unitary transformation, generally
        dimension-scaling, and expressed in ``energy_unit``.
    spectral_residual
        Induced matrix 2-norm residual, :math:`\\varepsilon_2`.  It is finite,
        non-negative, invariant under a common unitary transformation, and
        expressed in ``energy_unit``.

    Raises
    ------
    TypeError
        If identifiers or ``energy_unit`` are not strings, ``matrix_dimension``
        is not an integer, or a metric is not a real scalar.  Boolean values and
        numeric strings are rejected rather than converted.
    ValueError
        If a string field is empty, dimension is not positive, a metric is
        nonfinite or negative, or the norm ordering
        ``maximum_absolute_residual <= spectral_residual <= frobenius_residual``
        is violated.

    Notes
    -----
    The metrics are symmetric norms: exchanging reference and candidate changes
    only the identifier roles.  They are software-verification measurements for
    compatible representations and carry no scientific pass/fail meaning.
    """

    reference_identifier: str
    candidate_identifier: str
    matrix_dimension: int
    energy_unit: str
    maximum_absolute_residual: float
    frobenius_residual: float
    spectral_residual: float

    def __post_init__(self) -> None:
        """Canonicalize scalar fields and validate residual metric invariants."""

        self._require_string(self.reference_identifier, "reference identifier")
        self._require_string(self.candidate_identifier, "candidate identifier")
        self._require_string(self.energy_unit, "energy unit")
        if isinstance(self.matrix_dimension, bool) or not isinstance(
            self.matrix_dimension, int | np.integer
        ):
            msg = "matrix_dimension must be a positive integer"
            raise TypeError(msg)
        # Convert an accepted NumPy integer scalar to a built-in integer for a
        # stable immutable Python/Rust data boundary.
        matrix_dimension = int(self.matrix_dimension)
        if matrix_dimension <= 0:
            msg = "matrix_dimension must be positive"
            raise ValueError(msg)
        object.__setattr__(self, "matrix_dimension", matrix_dimension)
        for field_name in (
            "maximum_absolute_residual",
            "frobenius_residual",
            "spectral_residual",
        ):
            # Canonicalize accepted NumPy floating scalars to built-in floats so
            # result fields map directly to Rust floating-point scalars.
            canonical_metric = self._finite_nonnegative_real(
                getattr(self, field_name), field_name
            )
            object.__setattr__(self, field_name, canonical_metric)
        if self.maximum_absolute_residual > self.spectral_residual:
            msg = "maximum_absolute_residual must not exceed spectral_residual"
            raise ValueError(msg)
        if self.spectral_residual > self.frobenius_residual:
            msg = "spectral_residual must not exceed frobenius_residual"
            raise ValueError(msg)

    @staticmethod
    def _require_string(value: object, name: str) -> None:
        """Validate a nonempty public string field.

        Parameters
        ----------
        value
            Candidate string value.  Numeric strings remain strings and are not
            converted to numbers.
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
        This private method is mechanical validation of fields owned by the
        result object; it is not numerical or scientific policy.
        """

        if not isinstance(value, str):
            msg = f"{name} must be a string"
            raise TypeError(msg)
        if value == "":
            msg = f"{name} must not be empty"
            raise ValueError(msg)

    @staticmethod
    def _finite_nonnegative_real(value: object, name: str) -> float:
        """Return a canonical non-negative finite Python float.

        Parameters
        ----------
        value
            Metric value to validate.  Python and NumPy integer or floating
            scalars are accepted.  Booleans, strings, bytes, complex values,
            nonnumeric objects, nonfinite values, and negative values are
            rejected.
        name
            Metric field name used in diagnostics.

        Returns
        -------
        float
            Canonical built-in float for the immutable ResultObject boundary.

        Raises
        ------
        TypeError
            If ``value`` is not an accepted real scalar type.
        ValueError
            If ``value`` is nonfinite or negative.

        Notes
        -----
        This private method is mechanical public-boundary canonicalization for
        residual metrics.  It does not compare metrics against each other or
        apply an undocumented floating-point tolerance.
        """

        if isinstance(
            value, bool | np.bool_ | str | bytes | complex | np.complexfloating
        ):
            msg = f"{name} must be a real number"
            raise TypeError(msg)
        if not isinstance(value, int | float | np.integer | np.floating):
            msg = f"{name} must be a real number"
            raise TypeError(msg)
        # Canonicalize accepted Python/NumPy real scalars to a built-in float at
        # the public Python/Rust interoperability boundary.
        real = float(value)
        if not np.isfinite(real):
            msg = f"{name} must be finite"
            raise ValueError(msg)
        if real < 0.0:
            msg = f"{name} must be non-negative"
            raise ValueError(msg)
        return real


class OperatorRecordComparisonNumericalError(ValueError):
    """Raised when residual metric computation fails numerically.

    Parameters
    ----------
    reason
        Stable reason string describing the numerical failure category.

    Attributes
    ----------
    reason
        Public structured reason, such as ``"nonfinite_residual"`` or
        ``"linear_algebra_failure"``.
    """

    reason: str

    def __init__(self, reason: str) -> None:
        """Store the structured reason and build a concise message."""

        if not isinstance(reason, str):
            msg = "comparison numerical-error reason must be a string"
            raise TypeError(msg)
        if reason == "":
            msg = "comparison numerical-error reason must not be empty"
            raise ValueError(msg)
        self.reason = reason
        super().__init__(f"operator-record comparison numerical failure: {reason}")


class IncompatibleOperatorRecordsError(ValueError):
    """Raised when comparison is requested for incompatible records.

    Parameters
    ----------
    compatibility_result
        Structured compatibility audit result explaining every failed rule.

    Attributes
    ----------
    compatibility_result
        Public retained :class:`OperatorRecordCompatibilityResult`.  Keeping the
        structured result lets callers inspect mismatch codes without parsing a
        message string and corresponds to an error-valued result boundary in a
        future Rust implementation.

    Raises
    ------
    TypeError
        If ``compatibility_result`` is not an
        :class:`OperatorRecordCompatibilityResult`.
    """

    compatibility_result: OperatorRecordCompatibilityResult

    def __init__(self, compatibility_result: OperatorRecordCompatibilityResult) -> None:
        """Build an exception message while retaining the structured result."""

        if not isinstance(compatibility_result, OperatorRecordCompatibilityResult):
            msg = "compatibility_result must be an OperatorRecordCompatibilityResult"
            raise TypeError(msg)
        self.compatibility_result = compatibility_result
        # Summarize stable issue codes in canonical order for the exception text;
        # the structured compatibility_result remains the authoritative payload.
        issue_code_summary = ", ".join(
            issue.code.value for issue in compatibility_result.issues
        )
        # Keep the human-readable message concise while preserving structured
        # inspection through compatibility_result.
        message = "operator records are not compatible"
        if issue_code_summary:
            message = f"{message}: {issue_code_summary}"
        super().__init__(message)


@dataclass(frozen=True, slots=True)
class OperatorRecordComparator:
    """ActionObject for residual comparison of compatible records.

    Parameters
    ----------
    compatibility_analyzer
        Analyzer dependency used to audit exact representation compatibility
        before numerical metrics are computed.

    Raises
    ------
    TypeError
        If ``compatibility_analyzer`` is not an
        :class:`OperatorRecordCompatibilityAnalyzer`.

    Notes
    -----
    The algorithm obtains a compatibility result, rejects incompatible
    representations with a structured exception, constructs the intermediate
    residual matrix for compatible inputs, computes residual magnitudes,
    computes the Frobenius norm, computes singular values, extracts the largest
    singular value as the spectral norm, and constructs an immutable
    :class:`OperatorRecordComparisonResult`.
    """

    compatibility_analyzer: OperatorRecordCompatibilityAnalyzer = field(
        default_factory=OperatorRecordCompatibilityAnalyzer
    )

    def __post_init__(self) -> None:
        """Validate that the comparator owns a compatibility analyzer."""

        if not isinstance(
            self.compatibility_analyzer, OperatorRecordCompatibilityAnalyzer
        ):
            msg = (
                "compatibility_analyzer must be an OperatorRecordCompatibilityAnalyzer"
            )
            raise TypeError(msg)

    def execute(
        self, reference: OperatorRecord, candidate: OperatorRecord
    ) -> OperatorRecordComparisonResult:
        """Compare compatible records using symmetric residual norms.

        Parameters
        ----------
        reference
            Reference operator record used for provenance and the intermediate
            signed residual convention.
        candidate
            Candidate operator record used for provenance and the intermediate
            signed residual convention.

        Returns
        -------
        OperatorRecordComparisonResult
            Immutable metric result with descriptive public field names mapped
            to :math:`\\varepsilon_{\\max}`,
            :math:`\\varepsilon_{\\mathrm F}`, and :math:`\\varepsilon_2`.

        Raises
        ------
        TypeError
            If either input is not an :class:`OperatorRecord` through the
            compatibility analyzer.
        IncompatibleOperatorRecordsError
            If exact representation compatibility fails.
        OperatorRecordComparisonNumericalError
            If matrix subtraction produces nonfinite intermediates, if a scaled
            norm is nonfinite, or if singular-value computation fails.
        """

        compatibility_result = self.compatibility_analyzer.execute(reference, candidate)
        if not compatibility_result.is_compatible:
            raise IncompatibleOperatorRecordsError(compatibility_result)
        # The signed residual is an internal computational object only; the
        # public ResultObject exposes symmetric norms and not this matrix.
        with np.errstate(over="ignore", invalid="ignore"):
            matrix_residual = candidate.matrix - reference.matrix
        if not np.all(np.isfinite(matrix_residual)):
            raise OperatorRecordComparisonNumericalError("nonfinite_residual")
        maximum_absolute_residual = self._maximum_absolute_residual(matrix_residual)
        frobenius_residual = self._scale_safe_frobenius_norm(matrix_residual)
        spectral_residual = self._scale_safe_spectral_norm(matrix_residual)
        return OperatorRecordComparisonResult(
            reference_identifier=reference.identifier,
            candidate_identifier=candidate.identifier,
            matrix_dimension=reference.matrix.shape[0],
            energy_unit=reference.energy_reference.unit,
            maximum_absolute_residual=maximum_absolute_residual,
            frobenius_residual=frobenius_residual,
            spectral_residual=spectral_residual,
        )

    @staticmethod
    def _maximum_absolute_residual(matrix_residual: np.ndarray) -> float:
        """Return the finite entrywise maximum absolute residual.

        Parameters
        ----------
        matrix_residual
            Finite complex residual matrix already formed by subtracting two
            compatible represented matrices.

        Returns
        -------
        float
            Built-in finite non-negative entrywise maximum magnitude in the
            common matrix energy unit.

        Raises
        ------
        OperatorRecordComparisonNumericalError
            If absolute-value reduction yields a nonfinite metric.

        Notes
        -----
        This private owner-local helper implements one documented metric for
        ``OperatorRecordComparator``; it is private because callers receive the
        complete ``OperatorRecordComparisonResult`` rather than individual
        helper outputs.
        """

        # Entrywise magnitudes convert the signed residual matrix into the
        # absolute residual values used by the public maximum norm definition.
        residual_magnitudes = np.abs(matrix_residual)
        # The maximum magnitude is the unit-bearing epsilon_max metric before
        # ResultObject construction canonicalizes the Python float boundary.
        maximum = float(np.max(residual_magnitudes))
        if not np.isfinite(maximum):
            raise OperatorRecordComparisonNumericalError("nonfinite_metric")
        return maximum

    @staticmethod
    def _scale_safe_frobenius_norm(matrix_residual: np.ndarray) -> float:
        """Return a scaled Frobenius norm avoiding avoidable over/underflow.

        Parameters
        ----------
        matrix_residual
            Finite complex residual matrix in the common energy unit.

        Returns
        -------
        float
            Frobenius norm computed as ``scale * sqrt(sum(abs(delta/scale)^2))``
            so finite representable results for very large or very small inputs
            are not lost to avoidable overflow or underflow.

        Raises
        ------
        OperatorRecordComparisonNumericalError
            If scaling or reduction yields a nonfinite metric.

        Notes
        -----
        This private owner-local helper implements comparator policy for one
        documented metric. It stays private because direct callers should not
        bypass compatibility checks or structured result construction.
        """

        # Magnitudes are scaled before squaring so very large residuals do not
        # overflow and very small residuals do not underflow unnecessarily.
        residual_magnitudes = np.abs(matrix_residual)
        # The largest entry magnitude is the numerical scale factored out of the
        # Frobenius norm; zero scale means the residual matrix is exactly zero.
        scale = float(np.max(residual_magnitudes))
        if scale == 0.0:
            return 0.0
        if not np.isfinite(scale):
            raise OperatorRecordComparisonNumericalError("nonfinite_metric")
        # The scaled magnitudes are dimensionless; multiplying by scale restores
        # the matrix energy unit after the stable sum-of-squares reduction.
        scaled_magnitudes = residual_magnitudes / scale
        norm = scale * float(np.sqrt(np.sum(scaled_magnitudes * scaled_magnitudes)))
        if not np.isfinite(norm):
            raise OperatorRecordComparisonNumericalError("nonfinite_metric")
        return norm

    @staticmethod
    def _scale_safe_spectral_norm(matrix_residual: np.ndarray) -> float:
        """Return a scaled induced 2-norm for a finite residual matrix.

        Parameters
        ----------
        matrix_residual
            Finite complex residual matrix in the common energy unit.

        Returns
        -------
        float
            Largest singular value of a scaled residual matrix multiplied by
            the scale, preserving the matrix energy unit while avoiding
            avoidable overflow in singular-value computation.

        Raises
        ------
        OperatorRecordComparisonNumericalError
            If scaling is nonfinite, singular-value computation fails, singular
            values are nonfinite, or the rescaled norm is nonfinite.

        Notes
        -----
        This private owner-local helper implements comparator policy for the
        spectral norm. It is private so callers cannot skip compatibility,
        nonfinite-intermediate checks, or structured error handling.
        """

        # The spectral norm is computed on a dimensionless scaled residual to
        # avoid avoidable overflow inside the SVD implementation.
        residual_magnitudes = np.abs(matrix_residual)
        # The largest absolute entry provides a stable scale; zero scale means
        # every residual entry is exactly zero.
        scale = float(np.max(residual_magnitudes))
        if scale == 0.0:
            return 0.0
        if not np.isfinite(scale):
            raise OperatorRecordComparisonNumericalError("nonfinite_metric")
        try:
            # Singular values of the scaled residual are dimensionless; the
            # largest one becomes epsilon_2 after multiplication by scale.
            singular_values = np.linalg.svd(matrix_residual / scale, compute_uv=False)
        except np.linalg.LinAlgError as exc:
            raise OperatorRecordComparisonNumericalError(
                "linear_algebra_failure"
            ) from exc
        if not np.all(np.isfinite(singular_values)):
            raise OperatorRecordComparisonNumericalError("linear_algebra_failure")
        # Rescale the largest singular value to restore the common energy unit.
        norm = scale * float(singular_values[0])
        if not np.isfinite(norm):
            raise OperatorRecordComparisonNumericalError("nonfinite_metric")
        return norm
