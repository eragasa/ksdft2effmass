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
   * - ``OperatorRecordJsonSerializer``
     - ActionObject
     - Strict versioned JSON-compatible serialization

Mathematical and numerical convention
-------------------------------------

An ``OperatorRecord`` represents a finite square matrix realization

.. math::

   \mathbf H \in \mathbb C^{N \times N}

of an operator acting on one identified finite state space.  The software stores
the represented matrix, not a basis-independent operator.  Direct physical
comparison between two records requires a separate future comparison action that
establishes compatible state spaces, bases, geometries, units, energy zeros, and
alignment conventions.

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

The analyzer owns the tolerance ``tau`` because tolerance is an analysis policy,
not represented data.  ``HermiticityResult.is_hermitian`` is derived from

.. math::

   \varepsilon_{\mathrm H}\leq\tau.

This criterion is not a relative norm, spectral norm, Frobenius norm, or
scientific validation metric.

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
finiteness, cell linear independence, and operator-level orthonormality are
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

   analyzer = HermiticityAnalyzer(tolerance=1.0e-12)
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
