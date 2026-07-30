Finite operator records
=======================

A matrix alone is not enough to identify a represented physical operator.  The
same array of numbers may describe different scientific objects if it is written
in a different state space, ordered basis, geometry, unit system, or energy-zero
convention.  ``ksdft2effmass.operators`` therefore represents operator data with
explicit metadata and keeps external actions separate from the data object.

DataObject/ActionObject architecture
------------------------------------

The operator-record implementation follows a concrete DataObject/ActionObject
style that maps directly to Rust structs and ``impl`` blocks.  Data objects are
frozen, slotted dataclasses that enforce only their intrinsic invariants.
Action objects transform or analyze data objects and return explicit result data
objects.  There are no abstract base classes, inheritance hooks, monkey patches,
or module-global workflow state.

.. list-table:: Responsibilities
   :header-rows: 1

   * - Object
     - Category
     - Responsibility
   * - ``StateSpace``
     - DataObject
     - Finite state-space metadata
   * - ``Basis``
     - DataObject
     - Ordered basis metadata
   * - ``Geometry``
     - DataObject
     - Cell and boundary metadata
   * - ``EnergyReference``
     - DataObject
     - Energy-zero metadata
   * - ``OperatorRecord``
     - DataObject
     - Matrix and comparison-critical metadata
   * - ``HermiticityResult``
     - DataObject
     - Immutable analysis result
   * - ``HermiticityAnalyzer``
     - ActionObject
     - Hermiticity analysis and enforcement
   * - ``OperatorRecordJsonCodec``
     - ActionObject
     - Versioned JSON-compatible serialization

Hermiticity tolerance belongs to ``HermiticityAnalyzer`` because tolerance is an
analysis policy, not intrinsic represented data.  Hermiticity results are not
stored in ``OperatorRecord`` because analyses may be repeated with different
policies.  Serialization belongs to ``OperatorRecordJsonCodec`` because the wire
format is an external representation.  This separation maps naturally to Rust as
field-based structs, associated methods, and explicit ``Result``-like failures.

Mathematical object
-------------------

An ``OperatorRecord`` represents a finite matrix realization

.. math::

   \mathbf H : \mathbb C^N \rightarrow \mathbb C^N.

Successful construction enforces

.. math::

   \operatorname{shape}(\mathbf H)=(N,N),

.. math::

   N=\texttt{state\_space.dimension},

and

.. math::

   N=\operatorname{len}(\texttt{basis.ordering}).

The entry ``basis.ordering[i]`` identifies the basis state associated with row
and column index ``i``.  The stored matrix is a representation in that ordered
basis, not a basis-independent operator by itself.

Metadata roles
--------------

``StateSpace`` identifies the finite represented vector space and its stated
domain and codomain.  ``Basis`` identifies the ordered representation and records
an orthonormality assertion without storing basis vectors.  ``Geometry`` records
the system, boundary conditions, and three linearly independent row lattice
vectors: ``cell[i][j]`` is Cartesian component ``j`` of lattice vector ``i``.
``EnergyReference`` records the energy zero and unit already applied to the
matrix.  The ``value`` field is metadata associated with the declared zero; it is
not an unapplied shift.  ``provenance`` is a read-only string-to-string mapping
for tracing computational context; it does not itself validate a calculation.

Hermiticity analysis
--------------------

``HermiticityAnalyzer`` computes

.. math::

   \varepsilon_{\mathrm H}
   =
   \max_{i,j}\left|H_{ij}-H_{ji}^{*}\right|.

The result is a ``HermiticityResult`` with ``residual``, ``tolerance``, and
``is_hermitian``.  The acceptance condition is

.. math::

   \varepsilon_{\mathrm H}\leq\texttt{tolerance}.

This is an absolute entrywise maximum norm criterion.  It is not a relative
norm, spectral norm, or Frobenius-norm criterion.

Immutability and equality
-------------------------

Construction copies the supplied matrix, converts it to ``complex128``, and
marks the stored array as non-writeable.  The provenance mapping is copied and
exposed as read-only.  Exact equality is structural: ``OperatorRecord`` uses
``numpy.array_equal`` for the matrix and exact equality for metadata.  Equality
is not numerical or physical equivalence.  Records are unhashable because they
contain array-valued scientific data.

Serialization schema
--------------------

``OperatorRecordJsonCodec.encode()`` returns a JSON-compatible dictionary with
``schema_version`` set to integer ``1``.  The version-1 payload fields are:

* ``schema_version``;
* ``identifier``;
* ``operator_kind``;
* ``matrix``;
* ``state_space``;
* ``basis``;
* ``geometry``;
* ``energy_reference``;
* ``provenance``.

There is no Hermiticity tolerance in the serialized ``OperatorRecord`` payload.
Each complex entry is encoded as ``[real, imaginary]``.  An ``N`` by ``N``
complex matrix is represented by a nested ``N x N x 2`` JSON array.  Decoding
rejects missing schema versions, unsupported schema versions, missing required
fields, malformed complex entries, and data inconsistent with DataObject
constructors.

Compact serialized example::

   {
     "schema_version": 1,
     "identifier": "toy",
     "operator_kind": "finite_test_hamiltonian",
     "matrix": [[[1.0, 0.0], [0.0, 0.2]], [[0.0, -0.2], [2.0, 0.0]]],
     "state_space": {
       "identifier": "toy-space", "kind": "finite synthetic",
       "dimension": 2, "domain": "C^2", "codomain": "C^2"
     },
     "basis": {
       "identifier": "canonical", "kind": "orthonormal test basis",
       "ordering": ["a", "b"], "orthonormal": true
     },
     "geometry": {
       "system": "synthetic",
       "cell": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
       "boundary_conditions": "finite synthetic",
       "coordinate_convention": "Cartesian dimensionless, row lattice vectors"
     },
     "energy_reference": {
       "zero": "explicit synthetic zero", "unit": "eV", "value": 0.0
     },
     "provenance": {"source": "documentation example"}
   }

Construction and action examples
--------------------------------

.. code-block:: python

   import json
   import numpy as np
   from ksdft2effmass.operators import (
       Basis,
       EnergyReference,
       Geometry,
       HermiticityAnalyzer,
       OperatorRecord,
       OperatorRecordJsonCodec,
       StateSpace,
   )

   record = OperatorRecord(
       identifier="toy",
       operator_kind="finite_test_hamiltonian",
       matrix=np.array([[1.0, 0.2j], [-0.2j, 2.0]]),
       state_space=StateSpace("toy-space", "finite synthetic", 2, "C^2", "C^2"),
       basis=Basis("canonical", "orthonormal test basis", ("a", "b"), True),
       geometry=Geometry(
           "synthetic",
           ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
           "finite synthetic",
           "Cartesian dimensionless, row lattice vectors",
       ),
       energy_reference=EnergyReference("explicit synthetic zero", "eV"),
       provenance={"source": "documentation example"},
   )

   analyzer = HermiticityAnalyzer(tolerance=1.0e-12)
   result = analyzer.execute(record)
   assert result.is_hermitian

   codec = OperatorRecordJsonCodec()
   payload = codec.encode(record)
   restored = codec.decode(json.loads(json.dumps(payload)))
   assert restored == record

Comparison requirements and limitations
---------------------------------------

Before two records can be compared physically, a workflow must establish any
needed alignment of state spaces, ordered bases, geometries, energy units, energy
zeros, and basis transformations.  The current implementation intentionally does
not provide that comparison framework, unit conversion, sparse storage,
symmetry-aware equivalence, schema migration, or validation of the underlying
first-principles calculation.
