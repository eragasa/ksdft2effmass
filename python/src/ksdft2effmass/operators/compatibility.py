r"""Exact representation compatibility analysis for operator records.

This module owns only metadata compatibility checks required before direct
subtraction of two finite represented operator matrices.  It depends on
``records.py`` for :class:`OperatorRecord` and must not import
``difference.py``, ``residuals.py``, or ``comparison.py``.  The
comparison-related dependency direction is ``records.py -> compatibility.py ->
difference.py -> residuals.py -> comparison.py``.  This module does not
subtract matrices, calculate residual norms, own floating-point roundoff policy,
align bases, convert units, or determine physical equivalence.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import ClassVar

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
        """Return deterministic explanatory text for this mismatch code.

        Returns
        -------
        str
            Canonical human-readable description of the compatibility rule
            represented by this enum member.

        Notes
        -----
        The enum value remains the authoritative machine-readable code.
        Descriptions are deterministic explanatory text for diagnostics and
        documentation only. Callers must not parse descriptions as stable
        machine-readable codes or compatibility-rule identifiers.
        """

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

    Raises
    ------
    TypeError
        If ``code`` is not an
        :class:`OperatorRecordCompatibilityMismatchCode`. Strings are not
        coerced to enum members.
    """

    code: OperatorRecordCompatibilityMismatchCode

    def __post_init__(self) -> None:
        """Validate the issue-owned mismatch-code invariant.

        Raises
        ------
        TypeError
            If ``code`` is not an
            :class:`OperatorRecordCompatibilityMismatchCode`.

        Notes
        -----
        This private dataclass hook owns only the structural invariant that one
        issue stores one public enum code. It performs no string-to-enum
        coercion and no compatibility analysis.
        """

        if not isinstance(self.code, OperatorRecordCompatibilityMismatchCode):
            msg = (
                "compatibility issue code must be an "
                "OperatorRecordCompatibilityMismatchCode"
            )
            raise TypeError(msg)

    @property
    def description(self) -> str:
        """Return canonical human-readable description derived from ``code``.

        Returns
        -------
        str
            Deterministic explanatory text associated with the authoritative
            mismatch code.
        """

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
        """Validate identifiers and structural compatibility-result state.

        Raises
        ------
        TypeError
            If either identifier is not a string, ``issues`` is not an exact
            built-in tuple, or any issue is not an
            :class:`OperatorRecordCompatibilityIssue`.
        ValueError
            If either identifier is empty, issue codes are duplicated, issue
            codes are not members of ``rules_applied``, or issue ordering is not
            canonical declaration order.

        Notes
        -----
        This private dataclass hook owns structural ResultObject validation
        only: identifier validation; exact tuple enforcement; and issue type,
        uniqueness, membership, and ordering validation. It performs no
        compatibility analysis, matrix operation, tolerance policy, alignment,
        conversion, or scientific acceptance check.
        """

        self._require_string(self.reference_identifier, "reference identifier")
        self._require_string(self.candidate_identifier, "candidate identifier")
        issues = self._require_issue_tuple(self.issues)
        self._validate_issues(issues, self.rules_applied)
        object.__setattr__(self, "issues", issues)

    @property
    def rules_applied(self) -> tuple[OperatorRecordCompatibilityMismatchCode, ...]:
        """Return the complete canonical version-1 rule sequence.

        Returns
        -------
        tuple[OperatorRecordCompatibilityMismatchCode, ...]
            Immutable tuple of every public mismatch code in declaration order.

        Notes
        -----
        The value is derived from the public enum declaration and is not
        constructor state. It documents which rules were available for the audit
        even when ``issues`` is empty.
        """

        return self._RULES_APPLIED

    @property
    def is_compatible(self) -> bool:
        """Return compatibility status derived from the issue collection.

        Returns
        -------
        bool
            ``True`` exactly when ``issues`` is empty; otherwise ``False``.

        Notes
        -----
        Compatibility status is derived state, not an independently supplied
        flag, preventing contradictory public objects.
        """

        return len(self.issues) == 0

    @staticmethod
    def _require_issue_tuple(
        issues: tuple[OperatorRecordCompatibilityIssue, ...],
    ) -> tuple[OperatorRecordCompatibilityIssue, ...]:
        """Require the exact public tuple container for issues.

        Parameters
        ----------
        issues
            Public constructor value for the issue collection.  It must already
            be a tuple; general iterables, lists, strings, bytes, and
            non-iterable values are rejected rather than canonicalized.

        Returns
        -------
        tuple[OperatorRecordCompatibilityIssue, ...]
            The same tuple, preserving caller order for later canonical-order
            validation.

        Raises
        ------
        TypeError
            If ``issues`` is not exactly a tuple container.

        Notes
        -----
        This private method enforces the public tuple-only ResultObject
        boundary.  It intentionally does not sort, copy from a general iterable,
        or otherwise canonicalize issues because noncanonical ordering is an
        auditable construction error.
        """

        if type(issues) is not tuple:
            msg = "compatibility issues must be an exact tuple of issues"
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


class IncompatibleOperatorRecordsError(ValueError):
    """Raised when an operation requires compatible operator records.

    Parameters
    ----------
    compatibility_result
        Structured incompatible compatibility audit result.  The exception
        retains this public result so callers can inspect mismatch codes without
        parsing message text.

    Raises
    ------
    TypeError
        If ``compatibility_result`` is not an
        :class:`OperatorRecordCompatibilityResult`.
    ValueError
        If ``compatibility_result`` is compatible, because this exception can
        represent only failed compatibility preconditions.
    """

    compatibility_result: OperatorRecordCompatibilityResult

    def __init__(self, compatibility_result: OperatorRecordCompatibilityResult) -> None:
        """Store an incompatible structured result and build a message.

        Parameters
        ----------
        compatibility_result
            Public incompatible compatibility audit result to retain as
            authoritative structured exception state.

        Raises
        ------
        TypeError
            If ``compatibility_result`` is not an
            :class:`OperatorRecordCompatibilityResult`.
        ValueError
            If ``compatibility_result`` is compatible.

        Notes
        -----
        The exception message summarizes mismatch codes for readability only.
        The retained ``compatibility_result`` is the authoritative machine-
        inspectable state and should be used instead of parsing message text.
        """

        if not isinstance(compatibility_result, OperatorRecordCompatibilityResult):
            msg = "compatibility_result must be an OperatorRecordCompatibilityResult"
            raise TypeError(msg)
        if compatibility_result.is_compatible:
            msg = "compatibility_result must be incompatible"
            raise ValueError(msg)
        self.compatibility_result = compatibility_result
        issue_code_summary = ", ".join(
            issue.code.value for issue in compatibility_result.issues
        )
        message = "operator records are not compatible"
        if issue_code_summary:
            message = f"{message}: {issue_code_summary}"
        super().__init__(message)


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

    def require(
        self, reference: OperatorRecord, candidate: OperatorRecord
    ) -> OperatorRecordCompatibilityResult:
        """Return a compatible audit result or raise a structured error.

        Parameters
        ----------
        reference
            Reference represented operator record to audit.
        candidate
            Candidate represented operator record to audit.

        Returns
        -------
        OperatorRecordCompatibilityResult
            Compatible audit result with an empty issue tuple and complete
            ``rules_applied`` sequence.

        Raises
        ------
        TypeError
            If either ``reference`` or ``candidate`` is not an
            :class:`OperatorRecord`.
        IncompatibleOperatorRecordsError
            If the complete audit finds one or more incompatibilities. The
            exception retains the complete audit result.

        Notes
        -----
        This method runs the same complete audit as :meth:`execute` before
        deciding whether to raise. It does not fail on the first mismatch. It
        performs no matrix subtraction, residual norm calculation, tolerance
        policy, basis or gauge alignment, unit conversion, energy-zero
        alignment, physical-equivalence determination, or scientific acceptance
        check.
        """

        result = self.execute(reference, candidate)
        if not result.is_compatible:
            raise IncompatibleOperatorRecordsError(result)
        return result

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
