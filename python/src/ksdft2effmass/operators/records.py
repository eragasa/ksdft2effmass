r"""Immutable DataObjects for finite represented operator records.

This module defines metadata objects and ``OperatorRecord``, whose canonical
matrix represents :math:`\mathbf H\in\mathbb C^{N\times N}` in the exact index
order of ``Basis.ordering``. Matrix entries use the textual unit and energy-origin
convention stored by ``EnergyReference``. ``StateSpace``, ``Basis``, ``Geometry``,
and ``EnergyReference`` provide explicit interpreting metadata rather than
implicit global conventions.

These frozen, slotted DataObjects own represented state, intrinsic constructor
validation, owned-field canonicalization, defensive storage, and exact structural
equality only. ``OperatorRecord`` admits general finite non-Hermitian matrices;
Hermiticity tolerance/analysis, exact compatibility, represented differencing,
residual norms, aligned or approximate comparison, unit conversion, energy-zero
alignment, geometry transformation, physical-equivalence decisions, file I/O,
and JSON representation belong outside this module to named ActionObjects.

Construction and equality are software-verification surfaces. They do not prove
that metadata describe a physical system, validate a DFT or Wannier calculation,
establish an impurity Hamiltonian, perform scientific validation or uncertainty
quantification, or demonstrate Python/Rust conformance.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from types import MappingProxyType
from typing import TYPE_CHECKING, Any, ClassVar, cast

import numpy as np
from numpy.typing import NDArray

ComplexMatrix = NDArray[np.complex128]
"""Owned dense complex matrix type used by :class:`OperatorRecord`."""

if TYPE_CHECKING:
    # Constructor input typing mirrors the already accepted runtime integer
    # families. Boolean remains a runtime-rejected semantic refinement because
    # static integer typing cannot precisely exclude it.
    type _StateSpaceDimensionInput = int | np.integer[Any]
    type _BasisOrderingInput = Sequence[str]
    type _GeometryCellComponentInput = int | float | np.integer[Any] | np.floating[Any]
    type _GeometryCellInput = Sequence[Sequence[_GeometryCellComponentInput]]
    type _OperatorMatrixScalarInput = (
        int
        | float
        | complex
        | np.integer[Any]
        | np.floating[Any]
        | np.complexfloating[Any, Any]
    )
    type _OperatorMatrixRowInput = (
        tuple[_OperatorMatrixScalarInput, ...] | list[_OperatorMatrixScalarInput]
    )
    type _OperatorMatrixSequenceInput = (
        tuple[_OperatorMatrixRowInput, ...] | list[_OperatorMatrixRowInput]
    )
    type _OperatorMatrixInput = _OperatorMatrixSequenceInput | np.ndarray[Any, Any]


@dataclass(frozen=True, slots=True)
class StateSpace:
    r"""Finite represented state-space metadata.

    ``StateSpace`` represents the intrinsic metadata relation
    :math:`\dim\mathcal H=N` through ``state_space.dimension == N``. It stores
    no basis vectors or labels, matrix, operator, geometry, energy reference,
    numerical algorithm, serializer, or physical-validation result.

    Parameters
    ----------
    identifier
        Nonempty descriptive name for the represented finite state space within
        repository data. The string is stored exactly without normalization.
    kind
        Nonempty descriptive state-space metadata. It is stored exactly and is
        not restricted to a controlled vocabulary.
    dimension
        Positive finite number ``N`` of represented states. Python and NumPy
        integer scalars are accepted and canonicalized to built-in ``int``.
        Boolean values are rejected as a runtime semantic refinement. Positivity
        is the only magnitude policy; construction imposes no dimension cap and
        allocates no vector or matrix storage.

    Raises
    ------
    TypeError
        If ``identifier`` or ``kind`` is not a string, or if ``dimension`` is
        not a Python or NumPy integer scalar or is Boolean.
    ValueError
        If a metadata string is empty or ``dimension`` is not positive.

    Notes
    -----
    The DataObject validates only intrinsic metadata. Agreement among
    ``dimension``, a basis ordering, and a represented matrix belongs to
    :class:`OperatorRecord`. ``StateSpace`` has no standalone wire format; it is
    nested record state owned by :class:`OperatorRecordJsonSerializer`.
    Construction does not establish a physical Hilbert space, basis
    completeness, operator-domain correctness, or scientific validity.
    """

    identifier: str
    kind: str
    dimension: int

    if TYPE_CHECKING:

        def __init__(
            self,
            identifier: str,
            kind: str,
            dimension: _StateSpaceDimensionInput,
        ) -> None:
            """Declare admitted dimension inputs without changing runtime.

            Python and NumPy integer scalars are accepted at the constructor
            boundary and canonicalized to the stored built-in ``int`` attribute
            by ``__post_init__``. Boolean values remain rejected by runtime
            semantic validation even though static integer typing cannot express
            that exclusion precisely. The dataclass generates the actual runtime
            constructor because this declaration exists only during static type
            checking.
            """

    def __post_init__(self) -> None:
        """Validate intrinsic metadata and canonicalize the dimension.

        Raises
        ------
        TypeError
            If either descriptive field is not a string, or if ``dimension`` is
            not a Python or NumPy integer scalar or is Boolean.
        ValueError
            If either descriptive string is empty or ``dimension`` is not
            positive.

        Notes
        -----
        This runtime method enforces the semantic refinements that static typing
        cannot fully express, including Boolean rejection. The
        ``TYPE_CHECKING``-only constructor declaration broadens admitted input
        typing without replacing the generated dataclass runtime constructor.
        Canonicalization changes only the stored scalar type; it introduces no
        dimension cap, allocation, or cross-object validation.
        """

        self._require_string(self.identifier, "state-space identifier")
        self._require_string(self.kind, "state-space kind")
        if isinstance(self.dimension, bool) or not isinstance(
            self.dimension, int | np.integer
        ):
            msg = "state-space dimension must be a positive integer"
            raise TypeError(msg)
        # Canonical built-in integer storage provides a stable public data
        # boundary while preserving arbitrary-precision positive values.
        dimension = int(self.dimension)
        if dimension <= 0:
            msg = "state-space dimension must be positive"
            raise ValueError(msg)
        object.__setattr__(self, "dimension", dimension)

    @staticmethod
    def _require_string(value: object, name: str) -> None:
        """Validate a nonempty string field owned by ``StateSpace``.

        Parameters
        ----------
        value
            Candidate metadata value; only Python strings are accepted.
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
        This private method is owner-local intrinsic field validation and does
        not define cross-object compatibility policy.
        """

        if not isinstance(value, str):
            msg = f"{name} must be a string"
            raise TypeError(msg)
        if value == "":
            msg = f"{name} must not be empty"
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class Basis:
    r"""Ordered basis metadata for a finite matrix representation.

    For an ordered basis
    :math:`\mathcal B=(|b_0\rangle,\ldots,|b_{N-1}\rangle)`, ``ordering[i]``
    is the exact label for :math:`|b_i\rangle`. Order, spelling, and case are
    semantic coordinate metadata; labels are not sorted or normalized.

    Parameters
    ----------
    identifier
        Nonempty name of the basis metadata object, stored exactly.
    kind
        Nonempty description of the basis class or convention, stored exactly.
    ordering
        Ordered sequence of unique nonempty string labels associated with matrix
        rows and columns. Approved sequence inputs, including tuples and lists,
        are defensively copied and canonicalized to stored ``tuple[str, ...]``.
        Bare strings, bytes, unordered collections, mappings, generators, and
        arbitrary iterables are rejected.
    orthonormal
        Exact Python ``bool`` recording whether the represented basis convention
        is orthonormal. Both ``True`` and ``False`` are valid ``Basis`` metadata.
        No basis vectors or overlap matrix are stored, so this field is metadata
        rather than a numerical proof of orthogonality.

    Raises
    ------
    TypeError
        If ``identifier`` or ``kind`` is not a string; ``ordering`` is not an
        approved ordered sequence or contains a non-string label; or
        ``orthonormal`` is not an exact Python ``bool``.
    ValueError
        If a string field or label is empty, ``ordering`` is empty, or labels
        are duplicated by exact string equality.

    Notes
    -----
    ``Basis`` contains no vectors, overlap matrix, operator matrix, state space,
    geometry, energy metadata, numerical algorithm, or serialization behavior.
    Agreement between ordering length and matrix/state-space dimension, and the
    schema-version-1 requirement for an orthonormal record basis, belong to
    :class:`OperatorRecord`. Consequently, ``Basis(..., orthonormal=False)`` is
    valid even though an ``OperatorRecord`` containing it is rejected. Nested
    record serialization belongs to :class:`OperatorRecordJsonSerializer`; no
    independent ``Basis`` wire format is approved. Construction establishes no
    linear independence, completeness, physical equivalence, scientific
    validation, uncertainty quantification, or Rust conformance.
    """

    identifier: str
    kind: str
    ordering: tuple[str, ...]
    orthonormal: bool

    if TYPE_CHECKING:

        def __init__(
            self,
            identifier: str,
            kind: str,
            ordering: _BasisOrderingInput,
            orthonormal: bool,
        ) -> None:
            """Declare approved sequence inputs without changing storage.

            Tuple and list inputs are represented statically by ``Sequence`` and
            are canonicalized at runtime to the stored tuple field. Bare strings
            satisfy the broad static sequence protocol but remain a documented
            runtime semantic rejection. The dataclass generates the actual
            runtime constructor because this declaration exists only during
            static type checking.
            """

    def __post_init__(self) -> None:
        """Validate and canonicalize intrinsic ordered-basis metadata.

        Raises
        ------
        TypeError
            If metadata strings, the ordering container, labels, or the exact
            Python Boolean flag violate their semantic type boundaries.
        ValueError
            If a metadata string, ordering, or label is empty, or exact labels
            are duplicated.

        Notes
        -----
        The canonical tuple is a defensive copy preserving caller order and
        exact label spelling. This method performs no cross-object dimension
        check and no numerical orthogonality calculation.
        """

        self._require_string(self.identifier, "basis identifier")
        self._require_string(self.kind, "basis kind")
        if type(self.orthonormal) is not bool:
            msg = "basis orthonormal flag must be a Python bool"
            raise TypeError(msg)
        if isinstance(self.ordering, str | bytes):
            msg = "basis ordering must be an ordered sequence, not a string"
            raise TypeError(msg)
        if not isinstance(self.ordering, Sequence):
            msg = "basis ordering must be an ordered sequence of labels"
            raise TypeError(msg)
        # Canonical tuple storage preserves semantic order while preventing a
        # caller-owned mutable sequence from changing represented coordinates.
        ordering = tuple(self.ordering)
        if not ordering:
            msg = "basis ordering must not be empty"
            raise ValueError(msg)
        for label in ordering:
            self._require_string(label, "basis label")
        if len(set(ordering)) != len(ordering):
            msg = "basis ordering labels must be unique"
            raise ValueError(msg)
        object.__setattr__(self, "ordering", ordering)

    @staticmethod
    def _require_string(value: object, name: str) -> None:
        """Validate a nonempty string field owned by ``Basis``.

        Parameters
        ----------
        value
            Candidate basis metadata or label value.
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
        This owner-local private check prevents ambiguous module-level field
        validators and does not convert numeric values to labels.
        """

        if not isinstance(value, str):
            msg = f"{name} must be a string"
            raise TypeError(msg)
        if value == "":
            msg = f"{name} must not be empty"
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class Geometry:
    r"""Finite three-dimensional cell and boundary-condition metadata.

    The cell stores three row lattice vectors,

    .. math::

       \mathbf C=
       \begin{pmatrix}
       \mathbf a_1^{\mathsf T}\\
       \mathbf a_2^{\mathsf T}\\
       \mathbf a_3^{\mathsf T}
       \end{pmatrix}\in\mathbb R^{3\times3}.

    ``Geometry`` owns only this represented metadata, its intrinsic validation,
    canonicalization, defensive ownership, and exact structural equality. It
    performs no coordinate transformation, unit conversion, dimensional
    analysis, structure relaxation, or crystallographic validation.

    Parameters
    ----------
    system
        Nonempty physical-system label stored exactly. It is identity/provenance
        metadata and is ignored by compatibility analysis.
    cell
        Approved ordered sequence of three approved ordered row sequences, each
        containing three finite real components. Python ``int`` and ``float``
        values and NumPy integer and floating scalars are accepted. Boolean,
        complex, string, byte, and other scalar types are rejected. Components
        are expressed in ``length_unit`` and defensively canonicalized to nested
        built-in tuples containing built-in ``float`` values.
    boundary_conditions
        Nonempty boundary-condition convention string stored exactly. Exact
        equality is a compatibility rule.
    coordinate_convention
        Nonempty coordinate-convention string for interpreting cell rows, stored
        exactly. Exact equality is a compatibility rule.
    length_unit
        Nonempty dimensional-unit metadata for every cell component, stored
        exactly. No vocabulary lookup or unit conversion is performed.

    Attributes
    ----------
    LINEAR_INDEPENDENCE_RTOL
        Public dimensionless relative singular-value threshold
        :math:`r_{\mathrm{tol}}=10^{-12}` owned by ``Geometry``. For singular
        values of the cell, construction accepts exactly when
        :math:`\sigma_{\max}>0` and
        :math:`\sigma_{\min}>r_{\mathrm{tol}}\sigma_{\max}`. The calculation
        first scales all components by their largest absolute magnitude, so the
        decision is invariant under finite nonzero uniform scaling and row
        permutation up to supported binary64 arithmetic.

    Raises
    ------
    TypeError
        If a metadata field is not a string; the cell or a row is not an
        approved ordered sequence; or a component is not an accepted real
        scalar. Bare strings, bytes, mappings, sets, generators, unordered
        containers, Booleans, numeric strings, and complex values are not
        converted.
    ValueError
        If a metadata string is empty; an approved cell or row sequence has the
        wrong length; a component is nonfinite or cannot be represented as a
        finite binary64 value; or the row vectors fail the documented strict
        linear-independence criterion.

    Notes
    -----
    Row order, component signs, spelling, case, spaces, and punctuation are
    preserved exactly. Cells need not be orthogonal, normalized, cubic,
    right-handed, positive-determinant, physically realistic, or associated with
    a validated structure. ``Geometry`` has no standalone serialization API; it
    appears only as nested state owned by
    :class:`OperatorRecordJsonSerializer`. Construction is software and
    numerical verification scope and establishes no scientific validation or
    uncertainty quantification.
    """

    LINEAR_INDEPENDENCE_RTOL: ClassVar[float] = 1.0e-12

    system: str
    cell: tuple[tuple[float, float, float], ...]
    boundary_conditions: str
    coordinate_convention: str
    length_unit: str

    if TYPE_CHECKING:

        def __init__(
            self,
            system: str,
            cell: _GeometryCellInput,
            boundary_conditions: str,
            coordinate_convention: str,
            length_unit: str,
        ) -> None:
            """Declare approved cell inputs without changing runtime behavior.

            Approved ordered nested sequences and Python/NumPy real scalar
            families are exposed at the constructor boundary. Runtime semantic
            validation still rejects bare strings and Booleans that broad static
            sequence and integer protocols cannot exclude precisely. The
            dataclass generates the actual runtime constructor, and stored cell
            attributes retain their canonical nested-tuple-of-float type.
            """

    def __post_init__(self) -> None:
        """Validate intrinsic metadata and canonicalize owned cell storage.

        Raises
        ------
        TypeError
            If metadata strings, ordered-sequence containers, or component
            scalar types violate their documented semantic boundaries.
        ValueError
            If metadata is empty, cell shape or finiteness fails, conversion to
            binary64 overflows, or row vectors fail the public independence
            criterion.

        Notes
        -----
        Canonicalization defensively copies caller sequences. The numerical
        independence decision is intrinsic cell validation; this method performs
        no physical-unit interpretation or structure validation.
        """

        self._require_string(self.system, "geometry system")
        self._require_string(self.boundary_conditions, "geometry boundary conditions")
        self._require_string(
            self.coordinate_convention, "geometry coordinate convention"
        )
        self._require_string(self.length_unit, "geometry length unit")
        object.__setattr__(self, "cell", self._canonicalize_cell(self.cell))

    @staticmethod
    def _require_string(value: object, name: str) -> None:
        """Validate a nonempty string field owned by ``Geometry``.

        Parameters
        ----------
        value
            Candidate geometry metadata value.
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
        The method is private and owner-local; geometry dimensional units and
        conventions remain explicit string fields without numeric conversion.
        """

        if not isinstance(value, str):
            msg = f"{name} must be a string"
            raise TypeError(msg)
        if value == "":
            msg = f"{name} must not be empty"
            raise ValueError(msg)

    @classmethod
    def _canonicalize_cell(
        cls,
        cell: Sequence[Sequence[object]],
    ) -> tuple[tuple[float, float, float], ...]:
        """Return a validated immutable 3x3 row-vector cell.

        Parameters
        ----------
        cell
            Approved ordered sequence of three approved ordered row sequences.
            Components are passed individually to ``_finite_real`` without
            broad array coercion.

        Returns
        -------
        tuple[tuple[float, float, float], ...]
            Defensive nested-tuple copy containing built-in floats in the
            caller's exact row/component order and documented ``length_unit``.

        Raises
        ------
        TypeError
            If the cell or a row is not an approved ordered sequence, or a
            component is not an accepted Python/NumPy real scalar. Bare strings,
            bytes, mappings, sets, generators, Booleans, numeric strings, and
            complex values are rejected rather than iterated or converted.
        ValueError
            If an approved sequence has the wrong 3x3 shape, a component is
            nonfinite or overflows binary64 conversion, or the row vectors fail
            the documented strict relative singular-value criterion.

        Notes
        -----
        This private owner-local method mechanically implements public
        ``Geometry`` invariants. The largest-component scaling protects the
        scale-relative singular-value ratio from avoidable overflow or underflow
        for finite extreme-scale cells. It performs no coordinate or unit
        conversion and no scientific structure validation.
        """

        if isinstance(cell, str | bytes) or not isinstance(cell, Sequence):
            msg = "cell must be an ordered sequence of row lattice vectors"
            raise TypeError(msg)
        canonical_rows: list[tuple[float, ...]] = []
        for row in cell:
            if isinstance(row, str | bytes) or not isinstance(row, Sequence):
                msg = "cell rows must be ordered sequences of numeric components"
                raise TypeError(msg)
            canonical_rows.append(
                tuple(
                    cls._finite_real(component, "cell component") for component in row
                )
            )
        canonical = tuple(canonical_rows)
        if len(canonical) != 3 or any(len(vector) != 3 for vector in canonical):
            msg = "cell must contain three three-component row lattice vectors"
            raise ValueError(msg)
        # The maximum absolute component is a finite scale shared by every row;
        # normalization preserves the singular-value ratio while avoiding
        # avoidable LAPACK overflow or underflow at extreme binary64 scales.
        component_scale = max(abs(component) for row in canonical for component in row)
        if component_scale == 0.0:
            msg = "cell row lattice vectors must be sufficiently linearly independent"
            raise ValueError(msg)
        cell_array = np.array(canonical, dtype=float) / component_scale
        # Singular values of the normalized matrix determine the same
        # dimensionless ratio as the unscaled cell and are invariant under row
        # permutation up to supported binary64 arithmetic.
        singular_values = np.linalg.svd(cell_array, compute_uv=False)
        sigma_max = float(np.max(singular_values))
        sigma_min = float(np.min(singular_values))
        if sigma_max <= 0.0 or sigma_min <= cls.LINEAR_INDEPENDENCE_RTOL * sigma_max:
            msg = "cell row lattice vectors must be sufficiently linearly independent"
            raise ValueError(msg)
        return cast(tuple[tuple[float, float, float], ...], canonical)

    @staticmethod
    def _finite_real(value: object, name: str) -> float:
        """Return a canonical finite real cell component.

        Parameters
        ----------
        value
            Candidate component.  Python and NumPy integer or floating scalars
            are accepted; booleans, strings, bytes, complex values, and other
            objects are rejected.
        name
            Diagnostic field name.

        Returns
        -------
        float
            Built-in float used at the immutable Python/Rust data boundary.

        Raises
        ------
        TypeError
            If ``value`` is not an accepted real scalar.
        ValueError
            If ``value`` is nonfinite or conversion overflows.
        """

        if (
            isinstance(value, bool)
            or isinstance(value, np.bool_)
            or not isinstance(value, int | float | np.integer | np.floating)
        ):
            msg = f"{name} must be a finite real numeric value"
            raise TypeError(msg)
        # Canonicalize accepted Python/NumPy real scalars to built-in float for
        # stable immutable Python/Rust data boundaries.  Accepted integers
        # outside binary64 range raise the public finite-value ValueError rather
        # than leaking Python's conversion OverflowError.
        try:
            real = float(value)
        except OverflowError as exc:
            msg = f"{name} must be finite"
            raise ValueError(msg) from exc
        if not np.isfinite(real):
            msg = f"{name} must be finite"
            raise ValueError(msg)
        return real


@dataclass(frozen=True, slots=True)
class EnergyReference:
    """Exact textual energy-reference metadata for a finite matrix.

    ``EnergyReference`` is a frozen, slotted DataObject storing exactly two
    represented metadata fields. It interprets neither field and uses exact
    structural equality; metadata equality is not a determination of physical
    equivalence between energy references.

    Parameters
    ----------
    zero
        Nonempty Python string identifying the energy-origin convention, for
        example ``"explicit zero"`` or ``"valence-band maximum"``. This is a
        textual convention identifier, not a numerical energy offset. The
        string is stored exactly without trimming, case folding, vocabulary
        lookup, alias resolution, or interpretation.
    unit
        Nonempty Python string labeling the energy unit, for example ``"eV"``
        or ``"hartree"``. The string is stored exactly without normalization,
        registry lookup, dimensional analysis, alias resolution, or conversion.

    Raises
    ------
    TypeError
        If ``zero`` or ``unit`` is not a Python ``str`` instance. Booleans,
        numbers, bytes, ``None``, and arbitrary objects are not converted to
        strings.
    ValueError
        If ``zero`` or ``unit`` is the empty string. Because no trimming is
        performed, every nonempty string, including whitespace-only metadata,
        satisfies this intrinsic nonempty invariant.

    Notes
    -----
    Both accepted strings, including ``str`` subclasses, are retained unchanged;
    construction performs no canonicalization. No ``value``, ``offset``,
    ``energy_offset``, or ``reference_energy`` field is stored because this
    DataObject records metadata identity rather than an unapplied energy shift.
    Exact relational compatibility belongs to
    :class:`OperatorRecordCompatibilityAnalyzer`, and the nested record JSON
    representation belongs to :class:`OperatorRecordJsonSerializer`.

    Construction and exact value semantics are software-verification concerns.
    They establish neither physical suitability of a zero convention or unit nor
    scientific validation, uncertainty quantification, or Python/Rust
    conformance.
    """

    zero: str
    unit: str

    def __post_init__(self) -> None:
        """Validate the two owned textual metadata invariants.

        Raises
        ------
        TypeError
            If either field is not a Python ``str`` instance. Values are never
            passed through ``str()`` or another coercion before validation.
        ValueError
            If either correctly typed field is exactly the empty string.

        Notes
        -----
        Validation is field-local and preserves accepted values exactly: no
        trimming, case folding, normalization, vocabulary lookup, unit
        conversion, or offset interpretation occurs. The method stores no
        numerical offset and performs no compatibility analysis or
        serialization. Passing these intrinsic checks establishes a software
        metadata contract only, not physical equivalence or scientific validity.
        """

        self._require_string(self.zero, "energy-reference zero")
        self._require_string(self.unit, "energy-reference unit")

    @staticmethod
    def _require_string(value: object, name: str) -> None:
        """Validate a nonempty string field owned by ``EnergyReference``.

        Parameters
        ----------
        value
            Candidate energy-zero or energy-unit string.
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
        This private check is intrinsic field validation only; unit conversion
        and energy alignment are intentionally outside the DataObject.
        """

        if not isinstance(value, str):
            msg = f"{name} must be a string"
            raise TypeError(msg)
        if value == "":
            msg = f"{name} must not be empty"
            raise ValueError(msg)


@dataclass(frozen=True, slots=True, eq=False)
class OperatorRecord:
    r"""Finite matrix representation of an operator with interpreting metadata.

    The stored matrix represents
    :math:`\mathbf H\in\mathbb C^{N\times N}`. Matrix row and column index
    ``i`` follow ``basis.ordering[i]``; entries carry
    ``energy_reference.unit`` and use the origin identified by
    ``energy_reference.zero``. This DataObject stores a representation, not a
    basis-independent operator or a claim of physical validity.

    Parameters
    ----------
    identifier
        Nonempty record identifier stored exactly. It participates in exact
        DataObject equality but is ignored by representation compatibility.
    operator_kind
        Nonempty descriptive operator-kind string stored exactly. It is not
        normalized or restricted to a controlled vocabulary.
    matrix
        Exact NumPy array or nested tuple/list matrix containing Python integer,
        floating, or complex values or NumPy integer, floating, or complex
        scalars. Boolean values, numeric strings, bytes, ``None``, and arbitrary
        objects are rejected rather than coerced. The finite square input is
        defensively canonicalized to an exact two-dimensional C-contiguous
        ``numpy.ndarray`` with ``numpy.complex128`` dtype and operationally
        non-writeable storage.
    state_space
        Actual :class:`StateSpace` instance with
        ``state_space.dimension == matrix.shape[0]``.
    basis
        Actual :class:`Basis` instance with
        ``len(basis.ordering) == state_space.dimension``. The represented-record
        contract requires ``basis.orthonormal is True``; standalone ``Basis``
        metadata may validly store ``False``.
    geometry
        Actual :class:`Geometry` instance describing represented cell and
        coordinate metadata.
    energy_reference
        Actual :class:`EnergyReference` instance defining matrix-entry energy
        unit and energy-origin convention.
    provenance
        Any :class:`~collections.abc.Mapping` from nonempty Python strings to
        nonempty Python strings. An empty mapping is valid. Contents are
        defensively copied and exposed through a read-only ``Mapping``.

    Raises
    ------
    TypeError
        If textual fields, nested public objects, matrix container or scalar
        semantic types, provenance container, or provenance key/value types
        violate the documented boundary.
    ValueError
        If a textual or provenance string is empty; matrix rank, rectangularity,
        squareness, finiteness, conversion range, or cross-field dimensions
        violate an invariant; or the supplied basis is not orthonormal.

    Notes
    -----
    Exact structural equality includes all eight stored fields and uses
    ``numpy.array_equal`` for matrix entries and mapping-content equality for
    provenance. It is ordering- and complex-value-sensitive and uses no
    tolerance. The object is intentionally unhashable because it owns
    array-valued state and mutable-input mapping content has no approved exact
    hash protocol.

    ``OperatorRecord`` applies no Hermiticity requirement. Hermiticity policy
    belongs to :class:`HermiticityAnalyzer`; exact compatibility, represented
    subtraction, residual analysis, Workflow comparison, alignment, conversion,
    and physical-equivalence decisions belong to their respective ActionObjects.
    JSON representation belongs to :class:`OperatorRecordJsonSerializer`.
    Construction and equality are software verification of represented state;
    they establish no scientific validation, uncertainty quantification, or
    Python/Rust conformance.
    """

    identifier: str
    operator_kind: str
    matrix: ComplexMatrix
    state_space: StateSpace
    basis: Basis
    geometry: Geometry
    energy_reference: EnergyReference
    provenance: Mapping[str, str]

    if TYPE_CHECKING:

        def __init__(
            self,
            identifier: str,
            operator_kind: str,
            matrix: _OperatorMatrixInput,
            state_space: StateSpace,
            basis: Basis,
            geometry: Geometry,
            energy_reference: EnergyReference,
            provenance: Mapping[str, str],
        ) -> None:
            """Declare approved matrix inputs without changing runtime.

            Nested ordered sequences and exact NumPy arrays containing approved
            Python/NumPy real or complex scalar families are admitted at the
            constructor boundary. Runtime validation retains semantic refinements
            such as exact tuple/list/array containers and Boolean rejection that
            broad static protocols cannot express. The dataclass still generates
            the runtime constructor, while stored ``matrix`` remains the
            canonical ``ComplexMatrix`` field type.
            """

    def __post_init__(self) -> None:
        """Validate represented state and install immutable owned copies.

        Raises
        ------
        TypeError
            If record strings, nested public objects, matrix container/scalar
            types, provenance container, or provenance key/value types violate
            their semantic boundaries.
        ValueError
            If strings are empty; matrix shape, finiteness, conversion range, or
            cross-field dimension invariants fail; provenance entries are empty;
            or the basis is not orthonormal.

        Notes
        -----
        Matrix canonicalization and provenance copying preserve caller values
        while severing mutable ownership. No Hermiticity, norm, subtraction,
        compatibility, alignment, unit conversion, serialization, or scientific
        validation policy is executed here.
        """

        self._require_string(self.identifier, "operator-record identifier")
        self._require_string(self.operator_kind, "operator kind")
        if not isinstance(self.state_space, StateSpace):
            msg = "state_space must be a StateSpace"
            raise TypeError(msg)
        if not isinstance(self.basis, Basis):
            msg = "basis must be a Basis"
            raise TypeError(msg)
        if not isinstance(self.geometry, Geometry):
            msg = "geometry must be a Geometry"
            raise TypeError(msg)
        if not isinstance(self.energy_reference, EnergyReference):
            msg = "energy_reference must be an EnergyReference"
            raise TypeError(msg)
        # The canonical matrix is an owned C-order complex128 copy whose
        # dimensions and finite components have already passed intrinsic checks.
        canonical_matrix = self._canonicalize_matrix(self.matrix)
        self._validate_matrix(canonical_matrix)
        immutable_matrix = self._make_immutable_matrix(canonical_matrix)
        # Provenance is copied independently of truth value so an explicitly
        # supplied empty mapping remains valid empty represented metadata.
        canonical_provenance = self._copy_provenance(self.provenance)
        object.__setattr__(self, "matrix", immutable_matrix)
        object.__setattr__(self, "provenance", canonical_provenance)

    @property
    def shape(self) -> tuple[int, int]:
        """Two-dimensional shape of the canonical represented matrix.

        Returns
        -------
        tuple[int, int]
            Exact ``record.matrix.shape``. For a valid record this is ``(N, N)``,
            where ``N == state_space.dimension == len(basis.ordering)``.
        """

        return self.matrix.shape

    def __eq__(self, other: object) -> bool:
        """Return exact structural equality over every stored field.

        Parameters
        ----------
        other
            Candidate comparison object.

        Returns
        -------
        bool or NotImplemented
            Exact field equality for another ``OperatorRecord``; otherwise
            ``NotImplemented`` so Python can apply its ordinary reflected
            equality protocol.

        Notes
        -----
        Matrix comparison uses ``numpy.array_equal`` without tolerance and is
        sensitive to complex values and entry positions. Provenance compares as
        mapping content, independent of insertion order. Compatibility and
        physical equivalence are separate concepts.
        """

        if not isinstance(other, OperatorRecord):
            return NotImplemented
        return (
            self.identifier == other.identifier
            and self.operator_kind == other.operator_kind
            and np.array_equal(self.matrix, other.matrix)
            and self.state_space == other.state_space
            and self.basis == other.basis
            and self.geometry == other.geometry
            and self.energy_reference == other.energy_reference
            and dict(self.provenance) == dict(other.provenance)
        )

    __hash__ = None  # type: ignore[assignment]

    def _validate_matrix(self, matrix: ComplexMatrix) -> None:
        """Validate canonical matrix and cross-field representation invariants.

        Parameters
        ----------
        matrix
            Owned exact C-contiguous ``np.complex128`` matrix produced by
            ``_canonicalize_matrix``.

        Raises
        ------
        ValueError
            If the matrix is nonsquare or contains a nonfinite real or imaginary
            component; its dimension disagrees with ``state_space.dimension``;
            basis ordering length disagrees with the state-space dimension; or
            the basis is not orthonormal.

        Notes
        -----
        Rank and ragged-shape diagnostics are established before canonical
        conversion. This private owner-local method then validates the canonical
        represented matrix and dependency relations only. It does not require
        Hermiticity or perform a norm, eigensolve, alignment, comparison, or
        scientific validation.
        """

        if matrix.shape[0] != matrix.shape[1]:
            msg = "operator matrix must be square"
            raise ValueError(msg)
        # Real and imaginary components must both be finite; this is a storage
        # invariant and does not calculate any matrix norm.
        if not np.all(np.isfinite(matrix.real)) or not np.all(np.isfinite(matrix.imag)):
            msg = "operator matrix real and imaginary components must be finite"
            raise ValueError(msg)
        # The validated dimension identifies the common represented state count
        # shared by matrix axes, StateSpace, and ordered Basis labels.
        matrix_dimension = matrix.shape[0]
        if matrix_dimension != self.state_space.dimension:
            msg = "matrix dimension must match state-space dimension"
            raise ValueError(msg)
        if len(self.basis.ordering) != self.state_space.dimension:
            msg = "basis ordering length must match state-space dimension"
            raise ValueError(msg)
        if self.basis.orthonormal is not True:
            msg = "operator records require an orthonormal basis in schema version 1"
            raise ValueError(msg)

    @staticmethod
    def _require_string(value: object, name: str) -> None:
        """Validate a nonempty string field owned by ``OperatorRecord``.

        Parameters
        ----------
        value
            Candidate record identifier or operator-kind value.
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
        This private owner-local method protects record-owned string fields and
        does not implement metadata compatibility or serializer policy.
        """

        if not isinstance(value, str):
            msg = f"{name} must be a string"
            raise TypeError(msg)
        if value == "":
            msg = f"{name} must not be empty"
            raise ValueError(msg)

    @staticmethod
    def _make_immutable_matrix(matrix: ComplexMatrix) -> ComplexMatrix:
        """Return a matrix view backed by immutable owned bytes.

        Parameters
        ----------
        matrix
            Canonical finite C-contiguous ``np.complex128`` matrix.

        Returns
        -------
        ComplexMatrix
            Read-only matrix whose base chain owns an immutable ``bytes`` buffer;
            NumPy cannot mark the view writeable with ``setflags(write=True)``.

        Notes
        -----
        This private method owns the operational-immutability mechanism for the
        public ``OperatorRecord.matrix`` field.
        """

        immutable_buffer = matrix.tobytes(order="C")
        immutable_vector = np.frombuffer(immutable_buffer, dtype=np.complex128)
        immutable_matrix = immutable_vector.reshape(matrix.shape)
        return cast(ComplexMatrix, immutable_matrix)

    @classmethod
    def _canonicalize_matrix(cls, matrix: object) -> ComplexMatrix:
        """Return an owned C-order finite-shape ``complex128`` matrix candidate.

        Parameters
        ----------
        matrix
            Exact NumPy array or nested tuple/list matrix. Scalar entries must be
            approved Python/NumPy integer, floating, or complex scalars.

        Returns
        -------
        ComplexMatrix
            Exact built-in NumPy array with two dimensions, C-contiguous
            ``np.complex128`` storage, and a defensive copy. Squareness,
            finiteness, and cross-field relations are validated separately.

        Raises
        ------
        TypeError
            If the top-level matrix is not an exact NumPy array, tuple, or list;
            a nested row is not a tuple or list; or an entry has an unapproved
            semantic scalar type. Boolean, string, byte, ``None``, and arbitrary
            object entries are rejected before NumPy coercion.
        ValueError
            If the matrix rank is not two, nested rows are ragged, or an approved
            numeric scalar cannot be represented in ``complex128``. Conversion
            overflow is translated to the public finite-number taxonomy.

        Notes
        -----
        This private owner-local method mechanically implements the documented
        public constructor boundary. It performs no norm, Hermiticity analysis,
        alignment, unit conversion, or scientific calculation.
        """

        if type(matrix) is np.ndarray:
            if matrix.ndim != 2:
                msg = "operator matrix must be two-dimensional"
                raise ValueError(msg)
            entries = tuple(matrix.flat)
        elif type(matrix) in (tuple, list):
            sequence_matrix = cast(tuple[object, ...] | list[object], matrix)
            if not sequence_matrix or all(
                cls._is_approved_matrix_scalar(entry) for entry in sequence_matrix
            ):
                msg = "operator matrix must be two-dimensional"
                raise ValueError(msg)
            if not all(type(row) in (tuple, list) for row in sequence_matrix):
                msg = "operator matrix rows must be exact tuple or list sequences"
                raise TypeError(msg)
            rows = cast(Sequence[Sequence[object]], sequence_matrix)
            if any(
                type(entry) in (tuple, list, np.ndarray)
                for row in rows
                for entry in row
            ):
                msg = "operator matrix must be two-dimensional"
                raise ValueError(msg)
            row_lengths = tuple(len(row) for row in rows)
            if len(set(row_lengths)) != 1:
                msg = "operator matrix rows must form a non-ragged rectangular array"
                raise ValueError(msg)
            entries = tuple(entry for row in rows for entry in row)
        elif cls._is_approved_matrix_scalar(matrix):
            msg = "operator matrix must be two-dimensional"
            raise ValueError(msg)
        else:
            msg = "operator matrix must be an exact NumPy array or nested tuple/list"
            raise TypeError(msg)

        for entry in entries:
            if not cls._is_approved_matrix_scalar(entry):
                msg = (
                    "operator matrix entries must be real or complex numeric "
                    "scalars, not bool, string, bytes, None, or arbitrary objects"
                )
                raise TypeError(msg)

        try:
            canonical = np.array(matrix, dtype=np.complex128, copy=True, order="C")
        except OverflowError as exc:
            msg = "operator matrix entries must be finite complex128 values"
            raise ValueError(msg) from exc
        return canonical

    @staticmethod
    def _is_approved_matrix_scalar(value: object) -> bool:
        """Return whether one matrix entry has approved numeric semantics.

        Parameters
        ----------
        value
            Candidate scalar before NumPy conversion.

        Returns
        -------
        bool
            ``True`` only for Python integer, floating, or complex values and
            NumPy integer, floating, or complex scalar values, excluding Python
            and NumPy Booleans.

        Notes
        -----
        The predicate owns no coercion and no finiteness decision. It exists only
        as a private mechanical part of ``OperatorRecord`` constructor
        validation and is never called across objects.
        """

        return not isinstance(value, bool | np.bool_) and isinstance(
            value,
            int | float | complex | np.integer | np.floating | np.complexfloating,
        )

    @staticmethod
    def _copy_provenance(provenance: Mapping[str, str]) -> Mapping[str, str]:
        """Return an immutable string-to-string provenance mapping.

        Parameters
        ----------
        provenance
            Candidate mapping from provenance keys to provenance values.

        Returns
        -------
        Mapping[str, str]
            Defensive copy wrapped in ``MappingProxyType`` so later caller
            mutation cannot alter the record.

        Raises
        ------
        TypeError
            If ``provenance`` is not a mapping or any key/value is not a string.
        ValueError
            If any provenance key or value is empty.

        Notes
        -----
        This private method owns the ``OperatorRecord`` provenance invariant.
        Provenance is metadata and does not affect numerical matrix entries.
        """

        if not isinstance(provenance, Mapping):
            msg = "provenance must be a mapping from strings to strings"
            raise TypeError(msg)
        # Copy caller-owned mapping data before wrapping it in a read-only proxy
        # so later caller mutation cannot alter this immutable DataObject.
        copied = dict(provenance)
        if any(
            not isinstance(key, str) or not isinstance(value, str)
            for key, value in copied.items()
        ):
            msg = "provenance keys and values must be strings"
            raise TypeError(msg)
        if any(key == "" or value == "" for key, value in copied.items()):
            msg = "provenance keys and values must not be empty"
            raise ValueError(msg)
        return MappingProxyType(copied)
