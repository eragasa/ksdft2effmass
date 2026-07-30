Finite operator records
=======================

A dense array does not, by itself, identify a represented scientific operator.
The same numbers can represent different objects when the state space, ordered
basis, cell convention, energy zero, units, or provenance differ.  The
``ksdft2effmass.operators`` package therefore records a finite matrix together
with the comparison-critical metadata needed to interpret that matrix.

This page documents the implemented operator-record model.  It distinguishes
among the physical model being studied, the mathematical operator, the numerical
matrix representation, and the Python objects used to store and analyze that
representation.  Passing the software checks described here is not scientific
validation of a first-principles calculation or of an effective-mass model.

DataObject/ActionObject architecture
------------------------------------

Operator records follow the repository DataObject/ActionObject programming
model.  DataObjects are frozen, slotted dataclasses that own represented data,
intrinsic validation, canonicalization of their own fields, and exact structural
equality.  ActionObjects own policies for analyses or external representations.
The usual flow is

.. code-block:: text

   DataObject --ActionObject--> DataObject or ResultObject

There is intentionally no ``OperatorRecordWorkflow`` for construction,
Hermiticity analysis, encoding, and decoding.  Construction belongs to the data
objects, Hermiticity policy belongs to ``HermiticityAnalyzer``, and the wire
format belongs to ``OperatorRecordJsonSerializer``.

.. list-table:: Responsibilities
   :header-rows: 1

   * - Object
     - Category
     - Responsibility
   * - ``StateSpace``
     - DataObject
     - Finite represented state-space metadata
   * - ``Basis``
     - DataObject
     - Ordered basis metadata
   * - ``Geometry``
     - DataObject
     - Three-dimensional cell and boundary metadata
   * - ``EnergyReference``
     - DataObject
     - Energy-zero and energy-unit metadata
   * - ``OperatorRecord``
     - DataObject
     - Finite matrix representation and comparison-critical metadata
   * - ``HermiticityResult``
     - ResultObject
     - Immutable Hermiticity-analysis result
   * - ``HermiticityAnalyzer``
     - ActionObject
     - Hermiticity analysis and enforcement
   * - ``OperatorRecordCompatibilityIssue``
     - ResultObject
     - One deterministic representation-compatibility mismatch
   * - ``OperatorRecordCompatibilityResult``
     - ResultObject
     - Ordered compatibility issues and applied rules
   * - ``OperatorRecordCompatibilityAnalyzer``
     - ActionObject
     - Exact representation-compatibility analysis
   * - ``OperatorRecordComparisonResult``
     - ResultObject
     - Absolute residual metrics for compatible records
   * - ``OperatorRecordComparator``
     - ActionObject
     - Residual comparison of already-compatible records
   * - ``OperatorRecordJsonSerializer``
     - ActionObject
     - Strict versioned JSON-compatible serialization

Mathematical and numerical convention
-------------------------------------

An ``OperatorRecord`` represents a finite square matrix realization

.. math::

   \mathbf H \in \mathbb C^{N \times N}

of an operator acting on one identified finite state space.  The software stores
the represented matrix, not a basis-independent operator.  Direct physical or aligned comparison between two records requires a separate
future comparison action that establishes compatible state spaces, bases,
geometries, units, energy zeros, and alignment conventions.  The exact
compatible-record residual comparison documented below is implemented only after
those representation fields already match.

Construction enforces

.. math::

   \operatorname{shape}(\mathbf H)=(N,N),

.. math::

   N=\texttt{state\_space.dimension},

and

.. math::

   N=\operatorname{len}(\texttt{basis.ordering}).

The entry ``basis.ordering[i]`` identifies the basis state associated with row
and column index ``i``.  Schema version 1 requires ``basis.orthonormal is
True``; nonorthogonal representations, overlap matrices, and generalized
eigenproblems are outside this refactor.

``OperatorRecord`` copies the supplied matrix into owned, C-contiguous,
row-major ``numpy.complex128`` storage, rejects nonfinite entries, and marks the
stored array non-writeable through the public API.  This is API-level
immutability for the represented data; it is not a statement about all possible
NumPy internals.  Exact equality uses ``numpy.array_equal`` for the matrix and
exact equality for metadata.  It is not approximate numerical equivalence,
gauge-equivalent equality, or physical equality.  ``OperatorRecord`` is
unhashable because it owns array-valued data.

Metadata conventions
--------------------

``StateSpace(identifier, kind, dimension)``
   Identifies a finite represented vector space.  ``dimension`` is the positive
   integer ``N``.  The object does not store separate domain or codomain fields.

``Basis(identifier, kind, ordering, orthonormal)``
   Identifies the ordered matrix representation.  ``ordering`` is a nonempty
   tuple of unique nonempty string labels.  The Boolean ``orthonormal`` records
   an assertion about the basis; basis vectors themselves are not stored.

``Geometry(system, cell, boundary_conditions, coordinate_convention, length_unit)``
   Records geometric metadata for the representation.  Lattice vectors are rows:
   ``cell[i][j]`` is Cartesian component ``j`` of lattice vector ``i``.  Every
   cell component is expressed in ``length_unit``.  The cell must contain three
   sufficiently linearly independent row vectors.  With singular values
   ``sigma_min`` and ``sigma_max``, construction accepts only when

   .. math::

      \sigma_{\max} > 0
      \quad\text{and}\quad
      \sigma_{\min} > r_{\mathrm{cell}}\sigma_{\max},

   where ``r_cell`` is ``Geometry.LINEAR_INDEPENDENCE_RTOL = 1.0e-12``.

``EnergyReference(zero, unit)``
   Records the energy-zero convention already applied to the matrix and the
   energy unit.  The named reference ``zero`` has numerical value zero in the
   stored matrix coordinate system.  No unapplied offset or ``value`` field is
   stored; energy alignment and unit conversion are future actions.

``provenance``
   A copied, read-only string-to-string mapping for compact computational
   context.  It records context supplied by the caller but does not validate the
   underlying first-principles calculation.

Hermiticity analysis
--------------------

``HermiticityAnalyzer`` computes the absolute entrywise maximum residual

.. math::

   \varepsilon_{\mathrm H}
   =
   \max_{i,j}\left|H_{ij}-H_{ji}^{*}\right|.

The analyzer owns the tolerance ``tau`` and the expected ``energy_unit`` because
tolerance is a unit-bearing analysis policy, not represented data.
``HermiticityAnalyzer(tolerance, energy_unit)`` has no unitless compatibility
path.  The analyzer requires exact equality between its ``energy_unit`` and
``record.energy_reference.unit`` and performs no automatic unit conversion.
Both ``epsilon_H`` and ``tau`` are expressed in that common energy unit.
``HermiticityResult.is_hermitian`` is derived from

.. math::

   \varepsilon_{\mathrm H}\leq\tau.

This criterion is not a relative norm, spectral norm, Frobenius norm, or
scientific validation metric.  Unit mismatch raises the structured public
``HermiticityUnitMismatchError`` with analyzer and record units available for
inspection.  ``HermiticityAnalyzer.require(record)`` returns the
``HermiticityResult`` when accepted and otherwise raises
``HermiticityRequirementError`` retaining the failed result.  If finite public
record inputs overflow during residual subtraction, the analyzer raises
``HermiticityNumericalError`` rather than requiring callers to parse a generic
message.

Compatible-record comparison
----------------------------

``OperatorRecordComparator`` compares finite records only after
``OperatorRecordCompatibilityAnalyzer`` establishes exact representation
compatibility.  Compatibility is a software precondition for subtracting the two
stored matrices.  It is not basis alignment, unit conversion, energy alignment,
normalization, serialization, or a scientific acceptance rule.

For this first comparison operation, two records are compatible when the
following representation fields match exactly and in deterministic rule order:

.. list-table:: Compatibility rules and mismatch codes
   :header-rows: 1

   * - Rule
     - Stable mismatch code value
   * - Matrix dimension
     - ``matrix_dimension_mismatch``
   * - State-space kind
     - ``state_space_kind_mismatch``
   * - ``operator_kind``
     - ``operator_kind_mismatch``
   * - Ordered basis labels
     - ``ordered_basis_labels_mismatch``
   * - Basis kind
     - ``basis_kind_mismatch``
   * - Lattice vectors
     - ``lattice_vectors_mismatch``
   * - Boundary conditions
     - ``boundary_conditions_mismatch``
   * - Coordinate convention
     - ``coordinate_convention_mismatch``
   * - Geometry length unit
     - ``geometry_length_unit_mismatch``
   * - Energy unit
     - ``energy_unit_mismatch``
   * - Energy-zero convention
     - ``energy_zero_convention_mismatch``

The compatibility-critical representation fields are exactly the fields in the
rule table above.  Compatibility deliberately excludes fields that identify a
record instance, represented physical object, or provenance context:

.. list-table:: Deliberately ignored identity and provenance fields
   :header-rows: 1

   * - Ignored field
     - Reason
   * - ``OperatorRecord.identifier``
     - Record-instance identity is provenance for the result, not a matrix
       representation rule.
   * - ``StateSpace.identifier``
     - State-space label may differ while the state-space kind and dimension are
       representation-compatible.
   * - ``Basis.identifier``
     - Basis label may differ while ordered basis states and basis kind match.
   * - ``Geometry.system``
     - Physical-system name is provenance and may distinguish pristine and doped
       records.
   * - ``OperatorRecord.provenance``
     - Computational provenance is retained on records but does not decide
       subtractability.

These fields may differ while the finite matrix representations remain
subtractable.

``OperatorRecordCompatibilityMismatchCode`` is the public enum of stable,
machine-readable mismatch codes.  ``OperatorRecordCompatibilityIssue`` stores a
``code`` and explanatory ``description`` for one failed rule.
``OperatorRecordCompatibilityResult`` stores reference and candidate
identifiers, an immutable ordered collection of issues, and the complete applied
rule sequence.  For the fixed version-1 policy, the applied rule sequence is the
public read-only property
``tuple(OperatorRecordCompatibilityMismatchCode)`` and is not an arbitrary
constructor parameter.  The result rejects duplicated issue codes,
noncanonically ordered issues, and issue codes outside the evaluated rule set.
Its ``is_compatible`` property is derived solely from whether the issue
collection is empty; there is no independent compatibility flag.  Issues are
reported in enum declaration order.

If comparison is requested for incompatible records,
``OperatorRecordComparator.execute()`` raises
``IncompatibleOperatorRecordsError``.  The exception has a public
``compatibility_result`` attribute carrying the complete
``OperatorRecordCompatibilityResult`` so callers can inspect all mismatches
without parsing the exception string.  A future Rust implementation should model
the same public boundary as a ``Result`` whose error variant carries the
compatibility result, rather than as an uninspectable panic or message-only
failure.  This is a conceptual cross-language contract; no Rust implementation
is provided by the current Python package.

For compatible records, the comparator may form an intermediate represented
matrix residual, but the public operation is a symmetric operator comparison.
Swapping reference and candidate preserves all three norm values and swaps only
the reported identifiers.  The sign of an intermediate difference is not a
public observable because this task does not return the residual matrix.
Reference and candidate roles are retained for provenance and future asymmetric
operations.  A signed operator-difference ResultObject and ActionObject belong
to a later impurity-extraction task.

Let ``Delta H`` denote either intermediate difference
``candidate.matrix - reference.matrix`` or its negative; the following norms are
unchanged by that sign choice.  The comparator reports three absolute metrics in
``OperatorRecordComparisonResult``:

.. math::

   \varepsilon_{\max}
   =
   \max_{i,j}\left|\Delta H_{ij}\right|,

.. math::

   \varepsilon_{\mathrm F}
   =
   \left(\sum_{i,j}\left|\Delta H_{ij}\right|^{2}\right)^{1/2},

and

.. math::

   \varepsilon_{2}
   =
   \sigma_{\max}(\Delta\mathbf H).

The public result fields map to mathematical notation as follows:

.. list-table:: Public metric fields
   :header-rows: 1

   * - Public field
     - Mathematical symbol
     - Meaning
   * - ``maximum_absolute_residual``
     - :math:`\varepsilon_{\max}`
     - Entrywise maximum residual
   * - ``frobenius_residual``
     - :math:`\varepsilon_{\mathrm F}`
     - Frobenius residual
   * - ``spectral_residual``
     - :math:`\varepsilon_2`
     - Induced matrix 2-norm residual

These metrics are symmetric absolute norms, are not normalized, do not return
``Delta H``, and are reported only after exact compatibility succeeds.  They
satisfy

.. math::

   0 \leq \varepsilon_{\max}\leq\varepsilon_2\leq\varepsilon_{\mathrm F}.

``OperatorRecordComparisonResult`` rejects direct construction that violates
this norm ordering.  The comparator uses scale-safe Frobenius and spectral norm
algorithms for extreme finite magnitudes such as ``1e200`` and ``1e-200``.  If
subtraction produces nonfinite intermediates, if a scaled metric becomes
nonfinite, or if singular-value computation fails, comparison raises
``OperatorRecordComparisonNumericalError`` with a structured ``reason`` such as
``nonfinite_residual``, ``nonfinite_metric``, or ``linear_algebra_failure``.
They verify implemented numerical behavior on already-compatible
representations.  They do not validate a DFT calculation, prove that an
effective-mass model is scientifically acceptable, or combine parent-model,
numerical/discretization, and model-reduction errors.

Serialization schema version 1
------------------------------

``OperatorRecordJsonSerializer`` owns the first supported operator-record wire
format.  ``serialize()`` returns actual deterministic JSON text with
``schema_version`` set to integer ``1``.  ``deserialize()`` is strict: it requires
a top-level JSON object, rejects malformed JSON, duplicate object keys,
nonstandard constants such as ``NaN`` and ``Infinity``, missing fields, unknown
fields at every object level, booleans where integers or real numbers are
required, numeric strings, nonfinite values, malformed or ragged matrices,
duplicate basis labels through ``Basis``, ``basis.orthonormal = false`` through
``OperatorRecord``, and ``energy_reference.value`` as an unknown field.  The
serializer uses deterministic key ordering and compact separators equivalent to
``json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)``.

Version 1 top-level fields are:

.. list-table:: Version-1 field table
   :header-rows: 1

   * - Field
     - Meaning
   * - ``schema_version``
     - Integer ``1``
   * - ``identifier``
     - Operator-record identifier string
   * - ``operator_kind``
     - Descriptive operator category string
   * - ``matrix``
     - Nested ``N x N x 2`` array of complex entries encoded as ``[real, imaginary]``
   * - ``state_space``
     - Object with ``identifier``, ``kind``, and ``dimension``
   * - ``basis``
     - Object with ``identifier``, ``kind``, ``ordering``, and ``orthonormal``
   * - ``geometry``
     - Object with ``system``, ``cell``, ``boundary_conditions``, ``coordinate_convention``, and ``length_unit``
   * - ``energy_reference``
     - Object with ``zero`` and ``unit``
   * - ``provenance``
     - Object whose keys and values are strings

The public language-neutral schema and fixtures live under
``specification/operator-record/v1/``:

- ``operator-record.schema.json`` defines schema-version-1 structural rules;
- ``valid/minimal.json``, ``valid/complex-hermitian.json``, and
  ``valid/complex-nonhermitian.json`` must deserialize successfully;
- ``invalid/`` contains golden rejection fixtures for missing fields, unknown
  fields, unsupported versions, numeric strings, booleans-as-numbers, duplicate
  basis labels, nonorthogonal bases, ragged and nonsquare matrices, dimension
  mismatch, empty strings, singular cells, and forbidden
  ``energy_reference.value``.

Cross-field constraints such as
``N = state_space.dimension = len(basis.ordering)``, matrix squareness, matrix
finiteness, cell linear independence, and the schema-version-1 operator-level orthonormal-basis requirement are
public rules enforced through DataObjects or the serializer even when JSON Schema
cannot express them completely.

Compact serialized example::

   {
     "schema_version": 1,
     "identifier": "toy",
     "operator_kind": "finite_test_hamiltonian",
     "matrix": [[[1.0, 0.0], [0.0, 0.2]], [[0.0, -0.2], [2.0, 0.0]]],
     "state_space": {
       "identifier": "toy-space", "kind": "finite synthetic", "dimension": 2
     },
     "basis": {
       "identifier": "canonical", "kind": "orthonormal test basis",
       "ordering": ["a", "b"], "orthonormal": true
     },
     "geometry": {
       "system": "synthetic",
       "cell": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
       "boundary_conditions": "finite synthetic",
       "coordinate_convention": "Cartesian row lattice vectors",
       "length_unit": "dimensionless"
     },
     "energy_reference": {"zero": "explicit synthetic zero", "unit": "eV"},
     "provenance": {"source": "documentation example"}
   }

Python example
--------------

The supported public import path is ``ksdft2effmass.operators``.

.. code-block:: python

   import numpy as np
   from ksdft2effmass.operators import (
       Basis,
       EnergyReference,
       Geometry,
       HermiticityAnalyzer,
       OperatorRecord,
       OperatorRecordJsonSerializer,
       StateSpace,
   )

   record = OperatorRecord(
       identifier="toy",
       operator_kind="finite_test_hamiltonian",
       matrix=np.array([[1.0, 0.2j], [-0.2j, 2.0]]),
       state_space=StateSpace("toy-space", "finite synthetic", 2),
       basis=Basis("canonical", "orthonormal test basis", ("a", "b"), True),
       geometry=Geometry(
           "synthetic",
           ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
           "finite synthetic",
           "Cartesian row lattice vectors",
           "dimensionless",
       ),
       energy_reference=EnergyReference("explicit synthetic zero", "eV"),
       provenance={"source": "documentation example"},
   )

   analyzer = HermiticityAnalyzer(tolerance=1.0e-12, energy_unit="eV")
   result = analyzer.execute(record)
   assert result.is_hermitian

   serializer = OperatorRecordJsonSerializer()
   text = serializer.serialize(record)
   restored = serializer.deserialize(text)
   assert restored == record

Limits and future work
----------------------

The current implementation does not provide basis alignment, unit conversion,
energy alignment, sparse storage, nonorthogonal metrics, approximate record
comparison, schema migration from earlier ad hoc payloads, or validation of a
DFT/Wannier calculation.  Those operations require explicit future ActionObjects
or scientific specifications before they can be used as validation evidence.
