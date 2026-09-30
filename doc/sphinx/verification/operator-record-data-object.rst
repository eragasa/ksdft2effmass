OperatorRecord DataObject verification evidence
===============================================

Scope and represented state
---------------------------

``OperatorRecord`` is the frozen, slotted DataObject for one finite numerical
operator representation. It stores exactly:

.. code-block:: text

   identifier
   operator_kind
   matrix
   state_space
   basis
   geometry
   energy_reference
   provenance

The canonical matrix represents

.. math::

   \mathbf H\in\mathbb C^{N\times N},

with

.. math::

   N=\texttt{state_space.dimension}
    =\operatorname{len}(\texttt{basis.ordering}).

Matrix row and column index ``i`` follows ``basis.ordering[i]``. Every entry uses
the energy-unit label ``energy_reference.unit`` and energy-origin convention
``energy_reference.zero``. The record stores represented state and interpreting
metadata; it does not establish a basis-independent operator or physical
validity.

Construction and canonical matrix state
---------------------------------------

Approved matrix inputs are exact NumPy arrays and nested tuple/list matrices.
Entries may be Python integers, floats, or complex values or NumPy integer,
floating, or complex scalars. Construction does not pre-normalize caller data or
admit arbitrary array-like objects. Boolean values, NumPy Booleans, numeric
strings, bytes, ``None``, and arbitrary objects raise ``TypeError`` rather than
being treated as numbers.

A matrix must be rank two, non-ragged, square, and finite in both real and
imaginary components. Invalid rank, raggedness, nonsquareness, nonfiniteness, and
approved numeric values outside representable ``complex128`` range raise
``ValueError``. Huge Python integer conversion does not leak ``OverflowError``.
Largest finite representative binary64 entries remain admissible; construction
calculates no norm that could overflow later.

Valid input is defensively canonicalized to an exact built-in ``numpy.ndarray``
with ``numpy.complex128`` dtype, two square dimensions, and C-contiguous storage.
The source array, its view base, and non-C storage are not retained as mutable
represented state. Stored values are operationally immutable through ordinary
public NumPy APIs: item assignment and ``matrix.setflags(write=True)`` are both
rejected. This guarantee does not expose or require a particular private backing
object.

A general finite non-Hermitian matrix is admitted. ``OperatorRecord`` does not
calculate a Hermiticity residual or own a tolerance. ``HermiticityAnalyzer`` owns
that policy.

Metadata, dependency, and provenance invariants
-----------------------------------------------

``identifier`` and ``operator_kind`` are nonempty Python strings stored exactly
without trimming, case folding, normalization, or vocabulary lookup. Wrong
semantic types raise ``TypeError`` and empty strings raise ``ValueError``.

``state_space``, ``basis``, ``geometry``, and ``energy_reference`` must be actual
instances of their corresponding public DataObjects. Their intrinsic invariants
remain with those objects. ``OperatorRecord`` owns only these cross-field
relations:

.. math::

   \operatorname{shape}(\mathbf H)=(N,N),

.. math::

   N=\texttt{state_space.dimension},

.. math::

   N=\operatorname{len}(\texttt{basis.ordering}).

The supplied Basis must additionally satisfy ``basis.orthonormal is True`` for a
schema-version-1 represented record. This restriction belongs to
``OperatorRecord``. Independently valid ``Basis(..., orthonormal=False)`` metadata
remains supported.

Provenance accepts any ``collections.abc.Mapping`` with only nonempty string keys
and nonempty string values. An explicitly empty mapping is valid. Iterable pairs,
lists, tuples, strings, bytes, generators, and arbitrary non-Mapping objects are
not silently converted. Wrong key or value types raise ``TypeError``; empty keys
or values raise ``ValueError``.

Mapping content is defensively copied and exposed through a read-only ``Mapping``.
Caller replacement, addition, or deletion cannot affect the record. The public
contract does not require a concrete mapping implementation type.

Exact value semantics and ownership exclusions
----------------------------------------------

The outer record is frozen and slotted. Its fields cannot be reassigned, dynamic
attributes cannot be added, and no per-instance ``__dict__`` exists. Equality is
exact structural equality across all eight stored fields. Matrix equality is
complex-value and entry-position sensitive and uses no numerical tolerance.
Provenance compares as mapping content, independent of insertion order.
Identifiers, geometry-system metadata, and provenance participate in DataObject
equality even when exact compatibility policy deliberately ignores them.

``OperatorRecord.__eq__`` returns ``NotImplemented`` for unrelated objects. The
class is intentionally unhashable: ``OperatorRecord.__hash__ is None`` and no
content hash is defined for matrix and provenance state.

The DataObject owns no Hermiticity analysis, compatibility audit, represented
subtraction, residual norm, approximate comparison, comparison Workflow,
basis/gauge/energy-zero alignment, unit conversion, geometry transformation,
file I/O, physical-equivalence decision, scientific-validation policy, or JSON
serialization. Those operations remain with named ActionObjects. In particular,
this evidence does not duplicate serializer schemas, malformed-payload fixtures,
or round-trip integration.

Software-verification traceability
----------------------------------

The five target facets assign exactly one executable owner to every stable
identifier:

* ``test__OperatorRecord__construction.py``:

  * ``SV-OR-001`` — public construction and exact stored-field mapping;
  * ``SV-OR-002`` — approved matrix-container and scalar canonicalization;
  * ``SV-OR-003`` — C-contiguous complex128 canonical representation;
  * ``SV-OR-004`` — general non-Hermitian finite matrix admission;
  * ``SV-OR-005`` — exact identifier and operator-kind preservation;
  * ``SV-OR-006`` — derived shape contract;
  * ``SV-OR-007`` — DataObject action and serialization API exclusions.

* ``test__OperatorRecord__matrix_invariants.py``:

  * ``SV-OR-008`` — matrix rank rejection;
  * ``SV-OR-009`` — nonsquare matrix rejection;
  * ``SV-OR-010`` — ragged matrix rejection;
  * ``SV-OR-011`` — invalid matrix-scalar semantic-type rejection;
  * ``SV-OR-012`` — nonfinite real-component rejection;
  * ``SV-OR-013`` — nonfinite imaginary-component rejection;
  * ``SV-OR-014`` — scalar conversion-overflow taxonomy;
  * ``SV-OR-015`` — matrix/state-space dimension agreement;
  * ``SV-OR-016`` — basis-ordering/state-space dimension agreement;
  * ``SV-OR-017`` — orthonormal-basis requirement.

* ``test__OperatorRecord__metadata_invariants.py``:

  * ``SV-OR-018`` and ``SV-OR-019`` — identifier type and nonempty invariants;
  * ``SV-OR-020`` and ``SV-OR-021`` — operator-kind type and nonempty invariants;
  * ``SV-OR-022`` through ``SV-OR-025`` — exact dependency type boundaries;
  * ``SV-OR-026`` — provenance Mapping boundary;
  * ``SV-OR-027`` through ``SV-OR-030`` — provenance key/value type and
    nonempty invariants;
  * ``SV-OR-031`` — empty provenance mapping admission.

* ``test__OperatorRecord__ownership.py``:

  * ``SV-OR-032`` — defensive matrix ownership;
  * ``SV-OR-033`` — operational matrix immutability;
  * ``SV-OR-034`` — canonical storage from non-C-contiguous input;
  * ``SV-OR-035`` — defensive provenance ownership;
  * ``SV-OR-036`` — read-only provenance exposure;
  * ``SV-OR-037`` — frozen and slotted record state.

* ``test__OperatorRecord__value_semantics.py``:

  * ``SV-OR-038`` — exact structural equality across every field;
  * ``SV-OR-039`` — exact and ordering-sensitive matrix equality;
  * ``SV-OR-040`` — exact provenance mapping equality;
  * ``SV-OR-041`` — unrelated-object equality protocol;
  * ``SV-OR-042`` — public unhashability.

All facets use only the ``software_verification`` marker. Typed helpers construct
synthetic public dependencies, pass matrix inputs through without ``np.asarray``
or dtype coercion, and distinguish ``None`` from explicit empty provenance.
Passing means the Python DataObject satisfies the documented representation,
validation, ownership, immutability, equality, and error-taxonomy contract.
Failure may indicate an implementation regression, documentation mismatch, or
evidence defect requiring investigation; it does not by itself establish a
physical-model error or scientific invalidity.

VVUQ and cross-language status
------------------------------

Matrix shape, dtype, finiteness, canonical storage, defensive ownership, and
exact equality are software representation contracts. ``OperatorRecord``
performs no norm, residual, eigensolver, decomposition, convergence calculation,
or scientific numerical algorithm. Numerical verification is therefore not
applicable to this DataObject migration, and no ``NV-OR`` identifier is assigned.

The synthetic fixtures do not establish that a matrix is a valid Hamiltonian,
that metadata identify the correct state space or basis, that a first-principles
calculation is accurate, or that a represented model is adequate for an intended
use. Scientific validation has not been performed. Uncertainty quantification
has not been performed. The data model is conceptually portable to Rust structs
and validated constructors, but no Rust implementation or Python/Rust conformance
evidence has been demonstrated.
