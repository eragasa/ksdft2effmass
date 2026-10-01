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
   * - ``OperatorRecordDifferenceResult``
     - ResultObject
     - Immutable represented difference after compatibility succeeds
   * - ``OperatorRecordDifferencer``
     - ActionObject
     - Compatibility enforcement and signed matrix subtraction
   * - ``OperatorRecordComparisonResult``
     - ResultObject
     - Structural residual metrics for a represented difference
   * - ``OperatorRecordResidualAnalyzer``
     - ActionObject
     - Scale-safe residual norm analysis
   * - ``OperatorRecordComparator``
     - Workflow ActionObject
     - Concrete composition of differencer followed by residual analyzer
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

``OperatorRecord`` accepts exact NumPy arrays or nested tuple/list matrices.
Entries may be Python integers, floats, or complex values or NumPy integer,
floating, or complex scalars. Boolean values (including NumPy Booleans), numeric
strings, bytes, ``None``, and arbitrary objects are rejected with ``TypeError``
rather than silently converted. Invalid rank, nonsquare or ragged shape,
nonfinite real or imaginary components, and accepted numerical values outside
``complex128`` representable range raise ``ValueError``. This distinction is a
software input taxonomy, not a physical acceptance criterion.

The constructor defensively copies valid input into an exact built-in
``numpy.ndarray`` with two-dimensional, square, C-contiguous, row-major
``numpy.complex128`` storage. C-order, Fortran-order, and admitted noncontiguous
NumPy inputs therefore produce the same canonical represented values. The stored
array is operationally non-writeable: item assignment and
``matrix.setflags(write=True)`` are rejected. This public guarantee does not
specify a private backing-object type or claim protection against adversarial
memory manipulation.

A general finite matrix is valid represented state. ``OperatorRecord`` does not
require :math:`\mathbf H=\mathbf H^\dagger` and calculates no Hermiticity
residual; those policies belong to ``HermiticityAnalyzer``. Exact equality uses
``numpy.array_equal`` for matrix entries and exact equality for all metadata,
including identifiers and provenance that compatibility analysis may ignore. It
is complex-value and entry-position sensitive and uses no tolerance. Provenance
uses mapping-content equality independent of insertion order. This is not
approximate numerical, gauge-equivalent, compatibility, or physical equality.
``OperatorRecord`` is intentionally unhashable because its array-valued and
mapping-content state has no approved exact hash contract.

Metadata conventions
--------------------

``StateSpace(identifier, kind, dimension)``
   Stores exactly the intrinsic metadata ``identifier``, ``kind``, and
   ``dimension`` for a finite represented state space. ``identifier`` names the
   represented space within repository data, while ``kind`` is descriptive
   state-space metadata rather than a closed vocabulary. Both must be nonempty
   strings and are stored exactly: no stripping, case folding, slug conversion,
   Unicode normalization, or semantic-label validation is performed.

   The relationship :math:`\dim\mathcal H=N` is represented by
   ``state_space.dimension == N``. Python integer and NumPy integer scalar inputs
   are accepted and canonicalized to stored built-in ``int``; Boolean values are
   rejected as a runtime semantic refinement. ``dimension`` must be positive,
   but ``StateSpace`` imposes no maximum dimension and construction allocates no
   vector or matrix. The static constructor declaration exposes the admitted
   integer scalar families while the stored field annotation remains ``int``.

   This frozen, slotted DataObject validates only its intrinsic metadata and uses
   exact structural equality across all three fields. It stores no basis vectors
   or labels, matrix, operator, geometry, energy reference, numerical algorithm,
   serializer, or physical-validation state. Agreement among dimension, basis
   ordering, and matrix shape belongs to ``OperatorRecord``. ``StateSpace`` has
   no standalone wire format; schema-version-1 serialization includes it only as
   nested state owned by ``OperatorRecordJsonSerializer``. These software
   contracts do not establish a physical Hilbert space, basis completeness,
   operator-domain correctness, DFT or Wannier validity, scientific validation,
   uncertainty quantification, or Rust conformance.

``Basis(identifier, kind, ordering, orthonormal)``
   Stores exactly the basis-metadata-object name ``identifier``, descriptive
   basis class or convention ``kind``, exact ordered coordinate labels
   ``ordering``, and Boolean convention metadata ``orthonormal``. For

   .. math::

      \mathcal B=(|b_0\rangle,|b_1\rangle,\ldots,|b_{N-1}\rangle),

   the software representation is the tuple ``("b0", "b1", ..., f"b{N - 1}")``.
   Order is semantic: swapping labels changes the represented coordinate
   convention. Labels are unique nonempty strings compared exactly; construction
   performs no sorting, trimming, case folding, orbital-name interpretation, or
   Unicode normalization.

   Approved ordered sequences, including tuples and lists, are defensively copied
   and canonicalized to an exact built-in tuple, so later mutation of a caller's
   list cannot alter stored state. Bare strings, bytes, unordered collections,
   mappings, generators, and arbitrary iterables are rejected. The static
   constructor declaration exposes the approved sequence input while the stored
   field remains ``ordering: tuple[str, ...]``; bare strings remain a documented
   runtime semantic rejection despite satisfying the broad sequence protocol.

   ``orthonormal`` requires an exact built-in Python ``bool`` without truth-value
   coercion. Both ``True`` and ``False`` are valid ``Basis`` metadata. This does
   not numerically establish

   .. math::

      \langle b_i|b_j\rangle=\delta_{ij},

   because ``Basis`` stores no vectors or overlap matrix. ``OperatorRecord``
   separately requires ``basis.orthonormal is True`` under schema version 1 and
   owns agreement among matrix dimension, state-space dimension, and ordering
   length. Thus a nonorthonormal ``Basis`` is independently valid even though an
   ``OperatorRecord`` containing it is rejected.

   ``Basis`` contains no operator matrix, state-space object, geometry, energy
   metadata, orthogonality algorithm, or serialization behavior. It is serialized
   only as nested state by ``OperatorRecordJsonSerializer``; no independent Basis
   schema is approved. Frozen slotted state and equality are exact across all four
   fields, including label order; hash behavior is unspecified. These software
   contracts establish no basis-vector existence, linear independence,
   completeness, matrix compatibility, gauge alignment, physical equivalence,
   scientific validation, uncertainty quantification, or Rust conformance.

``Geometry(system, cell, boundary_conditions, coordinate_convention, length_unit)``
   Stores finite geometry metadata with exactly these five represented fields.
   The cell contains three row lattice vectors,

   .. math::

      \mathbf C=
      \begin{pmatrix}
      \mathbf a_1^{\mathsf T}\\
      \mathbf a_2^{\mathsf T}\\
      \mathbf a_3^{\mathsf T}
      \end{pmatrix}\in\mathbb R^{3\times3}.

   Thus ``cell[i][j]`` is component ``j`` of row lattice vector ``i``. Every
   component is expressed in the explicit ``length_unit`` metadata under the
   explicit ``coordinate_convention`` metadata. These strings are not registries:
   construction performs no unit conversion, dimensional analysis, coordinate
   transformation, vocabulary lookup, trimming, or normalization.

   The constructor accepts approved nested ordered sequences, including tuple and
   list outer containers and tuple and list rows. Python integers, Python floats,
   NumPy integer scalars, and NumPy floating scalars are accepted as components.
   They are canonicalized to built-in ``float`` values in defensively owned exact
   built-in tuple rows and an exact built-in outer tuple. Bare strings, bytes,
   mappings, sets, frozensets, generators, arbitrary unordered iterables,
   Booleans (including NumPy Booleans), numeric strings, complex values, and
   arbitrary objects are rejected rather than converted. An unapproved container
   or wrong scalar semantic type raises ``TypeError``. An approved sequence with
   the wrong length, a nonfinite value, or an integer that overflows finite
   binary64 conversion raises ``ValueError``.

   ``Geometry.LINEAR_INDEPENDENCE_RTOL`` is the public dimensionless tolerance
   :math:`r_{\mathrm{tol}}=10^{-12}` owned by this intrinsic DataObject invariant.
   For singular values of :math:`\mathbf C`, define

   .. math::

      \rho(\mathbf C)
      =\frac{\sigma_{\min}(\mathbf C)}{\sigma_{\max}(\mathbf C)}.

   Construction accepts exactly when

   .. math::

      \sigma_{\max}>0
      \quad\text{and}\quad
      \sigma_{\min}>r_{\mathrm{tol}}\sigma_{\max},

   equivalently :math:`\rho(\mathbf C)>r_{\mathrm{tol}}` when
   :math:`\sigma_{\max}>0`. Equality at the tolerance is not admitted under this
   strict criterion. The implementation first divides by the largest absolute
   finite component before singular-value calculation. This preserves the ratio
   while avoiding avoidable overflow or underflow, so the validity decision is
   invariant under tested finite nonzero uniform scales and row permutations.

   ``system``, ``boundary_conditions``, ``coordinate_convention``, and
   ``length_unit`` must be nonempty Python strings and are preserved exactly,
   including spelling, case, spaces, and punctuation. Equality is exact
   structural equality over all five fields and is row-order, component-value,
   and sign sensitive; it is not approximate or physical equivalence. The cell
   need not be orthogonal, normalized, cubic, right-handed, positive-determinant,
   physically realistic, relaxed, or associated with a validated crystal
   structure. ``Geometry`` has no standalone serialization API; only
   ``OperatorRecordJsonSerializer`` owns its nested record wire representation.
   These software and numerical contracts establish no scientific validation,
   uncertainty quantification, or Rust conformance. Detailed evidence is in
   :doc:`../verification/operator-record-geometry`.

``EnergyReference(zero, unit)``
   Stores exactly two textual metadata fields. ``zero`` is a nonempty identifier
   for the energy-origin convention already associated with the represented
   matrix, such as ``"explicit zero"`` or ``"valence-band maximum"``. It is not
   a numerical energy offset. ``unit`` is a nonempty energy-unit label, such as
   ``"eV"`` or ``"hartree"``. There is no ``value``, ``offset``,
   ``energy_offset``, or ``reference_energy`` field or constructor role.

   Both inputs must be Python ``str`` instances. ``None``, Booleans, numbers,
   bytes, and arbitrary objects raise ``TypeError`` rather than being converted.
   The empty string has the correct semantic type but violates the nonempty
   invariant and raises ``ValueError``. No trimming occurs, so whitespace-only
   strings remain nonempty metadata. Accepted strings, including case, spacing,
   punctuation, hyphenation, and ``str`` subclass identity, are retained exactly.
   Construction performs no case folding, normalization, vocabulary lookup,
   alias resolution, dimensional analysis, unit conversion, or physical
   interpretation.

   The DataObject is frozen and slotted and uses exact structural equality across
   ``zero`` and ``unit``. Consequently, differently represented labels such as
   ``"valence-band maximum"`` and ``"Valence-Band Maximum"``, or ``"eV"`` and
   ``"EV"``, need not compare equal. This is metadata identity, not a conclusion
   about physical equivalence. Exact relational compatibility belongs to
   ``OperatorRecordCompatibilityAnalyzer``. Nested schema-version-1 JSON state
   belongs to ``OperatorRecordJsonSerializer``; ``EnergyReference`` exposes no
   standalone serialization API.

   These construction, invariant, immutability, and equality checks are software
   verification only. ``EnergyReference`` owns no numerical algorithm, so
   numerical verification is not applicable. Scientific validation, uncertainty
   quantification, and Rust conformance have not been performed. Detailed
   evidence is in
   :doc:`../verification/operator-record-energy-reference`.

``provenance``
   Accepts any ``collections.abc.Mapping`` whose keys and values are nonempty
   Python strings. An empty mapping is valid. Iterable key/value pairs, lists,
   tuples, strings, bytes, generators, and arbitrary non-Mapping objects are not
   silently converted and raise ``TypeError``. Non-string keys or values also
   raise ``TypeError``; empty string keys or values raise ``ValueError``.

   Construction defensively copies mapping content, so caller replacement,
   addition, or deletion cannot change stored state. Public exposure remains a
   read-only ``Mapping`` without committing the API to a concrete mapping type.
   Provenance records context supplied by the caller but does not validate the
   underlying first-principles calculation. It has no independent serialization
   behavior; record JSON representation remains owned by
   ``OperatorRecordJsonSerializer``.

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
``HermiticityResult`` stores exactly ``residual``, ``tolerance``, and
``energy_unit``. The two scalars share that energy unit. The declared constructor
input types include Python and NumPy integer and floating scalars, which are
canonicalized to built-in stored ``float``. Static integer typing cannot precisely
exclude Boolean, so Boolean rejection remains an explicit runtime semantic
refinement. Booleans, numeric strings, bytes, complex values, and arbitrary
objects raise ``TypeError``; nonfinite values, binary64 conversion overflow, and
finite negative values raise ``ValueError``. The unit must be a nonempty Python
string. No trimming, normalization, unit registry, or conversion is performed.

``HermiticityResult.is_hermitian`` is derived rather than stored:

.. math::

   \varepsilon_{\mathrm H}\leq\tau.

The comparison is exact over the stored binary64 scalars and inclusive at
equality, including ``0.0 <= 0.0``. ``is_hermitian`` cannot be supplied as
constructor state. The frozen, slotted ResultObject has exact structural equality
across its three stored fields and no instance ``__dict__``; hash behavior is not
part of this contract.

The ResultObject stores no matrix, ``OperatorRecord``, Analyzer policy beyond the
recorded tolerance, unit conversion, scientific acceptance criterion, physical
provenance, or independent serialization behavior.
``OperatorRecordJsonSerializer`` serializes only ``OperatorRecord`` and no
``HermiticityResult`` schema is approved. The predicate is a software result; it
does not establish physical Hermiticity of a DFT or Wannier operator. Direct
construction, invariant, and value-semantics evidence is documented in
:doc:`../verification/operator-record-hermiticity`.

The Analyzer's declared tolerance-constructor inputs match its runtime admission:
Python and NumPy integer/floating scalars are accepted and canonicalized to the
stored built-in ``float``. Boolean rejection is a runtime semantic refinement;
no runtime admission or numerical behavior is implied by the typing declaration.
Configuration and execution evidence are separated into ``SV-HA-001`` through
``SV-HA-019``. Numerical residual accuracy is separately owned by ``NV-HA-001``
through ``NV-HA-005``. Every numerical execution promotes ``RuntimeWarning`` to
an error. Exact analytical zero requires exact ``0.0``; small normal nonzero
cases use the explicit bound
:math:`64\epsilon_{\mathrm{mach}}|x_{\mathrm{expected}}|`, with zero excluded.
This is a local test criterion rather than Analyzer tolerance policy or a
scientific acceptance threshold.

Hermiticity status is invariant under unitary basis transformation. For exact
stored arithmetic, an exactly Hermitian matrix remains at zero under the tested
diagonal-phase similarity :math:`U^\dagger H U`. In contrast, the nonzero
entrywise maximum residual is generally basis dependent: the documented
three-dimensional Fourier case changes from ``1`` to
:math:`1/\sqrt{3}`. This does not contradict invariance of zero-versus-nonzero
Hermiticity status.

This criterion is not a relative norm, spectral norm, Frobenius norm, or
scientific validation metric. Before residual calculation, the Analyzer compares
its policy unit :math:`u_{\mathrm{analyzer}}` exactly with the record metadata
unit :math:`u_{\mathrm{record}}`. The structured public
``HermiticityUnitMismatchError`` represents only
:math:`u_{\mathrm{analyzer}}\ne u_{\mathrm{record}}`. It retains the ordered
strings as ``analyzer_energy_unit`` and ``record_energy_unit``; a wrong unit type
raises ``TypeError``, while an empty string or equal-unit state raises
``ValueError`` at direct construction.

Comparison is exact and case-sensitive. No trimming, normalization, registry
lookup, dimensional-equivalence inference, or unit conversion is performed, so
differently cased strings remain a software mismatch without implying physical
inequivalence. The message labels both roles and values for humans, while the
structured fields are authoritative. The exception accepts no free-form reason
and has no independent serialization API. ``OperatorRecordJsonSerializer``
serializes only ``OperatorRecord``. Direct software-verification evidence and
VVUQ limitations are documented in
:doc:`../verification/operator-record-hermiticity`.

``HermiticityAnalyzer.require(record)`` returns the
``HermiticityResult`` when accepted and otherwise raises
``HermiticityRequirementError``. This structured ``ValueError`` retains the
exact failed Result by identity through ``error.result``. The strict exception
state is :math:`\varepsilon_{\mathrm H}>\tau`; equality is successful, so direct
exception construction rejects a Result satisfying
:math:`\varepsilon_{\mathrm H}\leq\tau` with ``ValueError``. A value that is not
``HermiticityResult`` raises ``TypeError``. Residual, tolerance, and energy unit
remain authoritative fields of the Result rather than duplicated exception
fields. The concise message is human-readable secondary evidence and need not be
parsed.

The exception accepts no free-form reason, exposes no ``reason`` attribute, and
has no independent JSON, dictionary, serializer, or deserializer API.
``OperatorRecordJsonSerializer`` serializes only ``OperatorRecord``; no wire
format for the exception or retained Result is approved. Direct exception
software-verification evidence is documented in
:doc:`../verification/operator-record-hermiticity`.

If finite public record inputs overflow while forming :math:`H-H^\dagger`, or if
reduction cannot produce a finite binary64
:math:`\varepsilon_{\mathrm H}`, the Analyzer raises
``HermiticityNumericalError``. Its structured category is the closed Python 3.14
``StrEnum`` ``HermiticityNumericalErrorCode``. The exact sole member is
``NONFINITE_RESIDUAL = "nonfinite_residual"``; the public registry has no aliases.
The enum performs no matrix operation or numerical detection. Value and name
lookups follow standard ``StrEnum`` behavior, and the ASCII lowercase snake-case
value is stable machine-readable Python state, not an approved serialization
format.

``HermiticityNumericalError`` is a public ``ValueError`` with one structured
field, ``reason``. Positional and ``reason=`` keyword construction retain the
exact supplied ``HermiticityNumericalErrorCode`` object. Raw strings and members
of unrelated enums are rejected with ``TypeError`` rather than coerced. The
approved structured field is deliberately named ``reason`` and is an enum-backed
category, not free-form prose. No additional free-form ``detail`` is accepted.
The message is a secondary human-readable summary containing the stable reason value,
while ``error.reason`` remains authoritative.

The exception has no independent JSON, dictionary, serializer, or deserializer
API. ``OperatorRecordJsonSerializer`` serializes only ``OperatorRecord``.
``StrEnum`` behavior does not approve an exception wire format. A future Rust
mapping would use a closed error enum, but no Rust implementation, serialization,
or conformance evidence exists.

``NONFINITE_RESIDUAL`` belongs to ``HermiticityAnalyzer`` production emission and
is distinct from unit mismatch, finite-residual requirement failure,
``OperatorRecordDifferenceNumericalErrorCode.NONFINITE_DIFFERENCE``, and
``OperatorRecordComparisonNumericalErrorCode`` residual-analysis failures. A
nonfinite residual is a software/numerical failure and does not establish that a
physical Hamiltonian is non-Hermitian. Future Rust mapping is conceptual only;
no Rust implementation or conformance is established. Detailed enum evidence and
VVUQ boundaries are documented in
:doc:`../verification/operator-record-hermiticity`.

Compatibility and comparison subsystems
---------------------------------------

The operator package separates exact representation-metadata compatibility,
represented signed differences, residual analysis, and Workflow composition. The
public pipeline is

.. math::

   (\mathbf H_{\mathrm{reference}},
   \mathbf H_{\mathrm{candidate}})
   \longrightarrow
   \text{compatibility audit}
   \longrightarrow
   \Delta\mathbf H
   \longrightarrow
   (\varepsilon_{\max},\varepsilon_{\mathrm F},\varepsilon_2).

The dependency direction is ``records.py -> compatibility.py -> difference.py ->
residuals.py -> comparison.py``. Earlier layers must not import later layers.

``OperatorRecordCompatibilityAnalyzer`` owns only exact compatibility of already
represented metadata.  It does not subtract matrices, calculate residual norms,
own roundoff policy, align bases, convert units, or determine physical
equivalence. Detailed software-verification evidence for rule reachability,
dimension/label coupling, ignored metadata, deterministic ordering, and
``execute()`` versus ``require()`` is documented in
:doc:`../verification/operator-record-compatibility-analysis`.

``OperatorRecordComparator`` is a genuine concrete production Workflow, not a
technical-integration owner or generic Workflow base class. It sequences
``OperatorRecordDifferencer.execute(reference, candidate)`` followed by
``OperatorRecordResidualAnalyzer.execute(difference)`` and returns the resulting
``OperatorRecordComparisonResult``. It compares finite records only after the
differencer's compatibility dependency establishes exact representation
compatibility. The Workflow does not own compatibility rules, signed
subtraction, matrix storage, finite-difference checks, norm calculation,
floating-point scaling, roundoff allowance, metric canonicalization, or physical
acceptance thresholds. Compatibility is a software precondition for subtracting
the two stored matrices. It is not basis alignment, unit conversion, energy
alignment, normalization, serialization, scientific validation, or uncertainty
quantification.

For this first comparison operation, two records are compatible when the
following representation fields match exactly and in deterministic rule order:

.. list-table:: Public compatibility mismatch-code enumeration contract
   :header-rows: 1

   * - Canonical order
     - Enum name
     - Stable machine value
     - Human-readable description
   * - 1
     - ``MATRIX_DIMENSION_MISMATCH``
     - ``matrix_dimension_mismatch``
     - matrix dimensions must match exactly
   * - 2
     - ``STATE_SPACE_KIND_MISMATCH``
     - ``state_space_kind_mismatch``
     - state-space kind must match exactly
   * - 3
     - ``OPERATOR_KIND_MISMATCH``
     - ``operator_kind_mismatch``
     - operator_kind must match exactly
   * - 4
     - ``ORDERED_BASIS_LABELS_MISMATCH``
     - ``ordered_basis_labels_mismatch``
     - ordered basis labels must match exactly
   * - 5
     - ``BASIS_KIND_MISMATCH``
     - ``basis_kind_mismatch``
     - basis kind must match exactly
   * - 6
     - ``LATTICE_VECTORS_MISMATCH``
     - ``lattice_vectors_mismatch``
     - lattice vectors must match exactly
   * - 7
     - ``BOUNDARY_CONDITIONS_MISMATCH``
     - ``boundary_conditions_mismatch``
     - boundary conditions must match exactly
   * - 8
     - ``COORDINATE_CONVENTION_MISMATCH``
     - ``coordinate_convention_mismatch``
     - coordinate convention must match exactly
   * - 9
     - ``GEOMETRY_LENGTH_UNIT_MISMATCH``
     - ``geometry_length_unit_mismatch``
     - geometry length unit must match exactly
   * - 10
     - ``ENERGY_UNIT_MISMATCH``
     - ``energy_unit_mismatch``
     - energy unit must match exactly
   * - 11
     - ``ENERGY_ZERO_CONVENTION_MISMATCH``
     - ``energy_zero_convention_mismatch``
     - energy-zero convention must match exactly

The declaration and iteration order is deterministic:
``tuple(OperatorRecordCompatibilityMismatchCode)`` defines the canonical rule
order used by compatibility results and analyzers. Stable enum values are ASCII
snake-case strings for machine-readable and cross-language mapping. Descriptions
are canonical human-facing findings and do not replace enum values in serialized
or cross-language logic. Reachability of every mismatch from independently valid
records belongs to ``OperatorRecordCompatibilityAnalyzer`` software-verification
tests, not to the enum-contract tests.

No orthonormality mismatch code exists. Valid schema-version-1
``OperatorRecord`` objects already require orthonormal bases, so such a mismatch
cannot arise between independently valid records; no obsolete member or alias is
retained.

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

Under the current software contract, differences in these fields alone do not
prevent direct subtraction when every compatibility-critical field matches.
This ignored-field policy does not establish that the records describe the same
physical system or that subtraction is scientifically acceptable.

``OperatorRecordCompatibilityMismatchCode`` is the authoritative public enum of
stable machine-readable mismatch codes. ``OperatorRecordCompatibilityIssue``
stores exactly one authoritative field, ``code``, containing one such enum
member. Its human-readable ``description`` is derived canonically from
``issue.code.description``; description text is neither constructor state nor
independently editable. Free-form Issue text is intentionally unsupported, which
prevents a machine code and contradictory human description from coexisting.
This Python structure is conceptually portable to a Rust value object containing
one enum field and a derived description method, but no Rust implementation or
conformance is established. The Issue has no independent wire-format contract;
future compatibility-result serialization requires an approved serializer and
versioned schema.

``OperatorRecordCompatibilityResult`` stores exactly three fields:
``reference_identifier``, ``candidate_identifier``, and ``issues``. The Issue
collection must be an exact built-in tuple containing only
``OperatorRecordCompatibilityIssue`` values, with no duplicated mismatch codes
and with codes in canonical enum order. General iterables, mutable collections,
and tuple subclasses are rejected rather than canonicalized.

The complete applied rule sequence and compatibility status are derived public
properties, not constructor state. ``rules_applied`` is always the exact built-in
tuple ``tuple(OperatorRecordCompatibilityMismatchCode)``, including for an empty
Issue collection. ``is_compatible`` is true exactly when ``issues == ()``;
callers cannot supply an independent compatibility flag. The ResultObject has no
independent serialization API or approved wire format. Any future wire format
requires an explicitly approved serializer and versioned schema.

These invariants protect immutable audit-state structure only.
``OperatorRecordCompatibilityAnalyzer`` owns rule execution and evidence that a
mismatch can be reached from independently valid record pairs. Direct
ResultObject construction does not execute compatibility rules or establish
reachability. The stored/derived representation is conceptually portable to a
validated Rust struct, but no Rust implementation or conformance is established.

If compatibility is required for an operation,
``OperatorRecordCompatibilityAnalyzer.require()`` returns the compatible result
or raises ``IncompatibleOperatorRecordsError``. The exception is a public
``ValueError`` subtype with a public ``compatibility_result`` attribute carrying
the exact complete ``OperatorRecordCompatibilityResult`` by identity. Callers can
therefore inspect reference and candidate roles and the canonical ordered Issue
tuple without reconstructing state or parsing the exception string. The message
is a human-readable mismatch-code summary only; the retained Result is the
authoritative machine-readable interface.

Direct exception construction rejects a non-Result input with ``TypeError`` and
a correctly typed compatible Result with ``ValueError`` because the latter
violates the exception-state invariant. Analyzer propagation is verified
separately from the exception's direct constructor contract. The exception has
no independent JSON or dictionary serialization API; exception and compatibility-
result wire formats are outside schema version 1.

Incompatibility means failure of the current exact direct-representation
contract. It does not prove that basis alignment, gauge alignment, energy-zero
alignment, unit conversion, geometry transformation, or another scientifically
justified identification map could not make the records comparable. These are
software semantics, not physical incompatibility, scientific validation, or
uncertainty quantification. A future Rust implementation should model the same
structured boundary as a ``Result`` whose error variant carries the compatibility
result, rather than as an uninspectable panic or message-only failure. This is a
conceptual cross-language contract; no Rust implementation or conformance is
provided by the current Python package. See
:doc:`../verification/operator-record-compatibility-analysis` for executable
evidence ownership.

``OperatorRecordDifferencer`` forms the public represented operator difference

.. math::

   \Delta\mathbf H
   =
   \mathbf H_{\mathrm{candidate}}
   -
   \mathbf H_{\mathrm{reference}}

only after compatibility succeeds. ``OperatorRecordDifferenceResult`` stores a
compatible audit result, immutable bytes-backed C-contiguous ``np.complex128``
difference matrix, and common energy unit. Its identifiers are exposed through
the compatibility result. The ResultObject constructor validates only intrinsic
stored state; direct construction cannot reconstruct or independently prove that
the matrix came from the audited records. The ResultObject is intentionally
unhashable under the Python data model because it owns array-valued exact state
and no safe exact hash is implemented. ``OperatorRecordDifferencer.execute()``
establishes operational provenance and the sign convention when it constructs
the result. The object is not a complete independently serializable
``OperatorRecord`` and has no JSON serialization contract in this version. The
represented difference is not automatically an impurity operator; identifying an
impurity operator requires additional physical assumptions and alignment
procedures outside this task. Future block- or shell-resolved analyzers may
consume this represented difference, but those analyses are not implemented by
this subsystem.

``OperatorRecordDifferenceNumericalErrorCode`` is the closed public Python 3.14
``StrEnum`` for failures owned by represented differencing. Its exact sole member
is ``NONFINITE_DIFFERENCE`` with stable ASCII snake-case value
``nonfinite_difference``. It means that subtraction of two individually finite,
compatible represented matrices produced at least one nonfinite entry in
:math:`\Delta\mathbf H`. The enum supplies machine-readable classification only:
``OperatorRecordDifferencer`` owns error production, while
``OperatorRecordDifferenceNumericalError`` owns exception construction. The enum
does not perform subtraction, detect nonfinite values, expose aliases or a
free-form reason, or define a serialization format.

``OperatorRecordDifferenceNumericalError`` is the corresponding structured
public ``ValueError``. Its one-argument constructor accepts only an
``OperatorRecordDifferenceNumericalErrorCode`` and retains the exact enum member
by identity in ``error.code``. The human-readable message identifies an operator-
record difference numerical failure and includes the stable code value, but the
enum attribute—not parsed message text—is authoritative machine-readable state.
Raw strings, unrelated enum members, ``None``, Booleans, and arbitrary objects
are rejected with ``TypeError`` rather than coerced.

No positional or keyword free-form ``reason`` is accepted, and valid exceptions
have no public ``reason`` attribute. The exception has no independent JSON,
dictionary, serializer, or deserializer API; schema version 1 applies only to
``OperatorRecord``. ``OperatorRecordDifferencer`` owns actual error production,
while direct exception tests own construction and invariant evidence.

This difference code is distinct from residual-analysis codes for nonfinite
metrics, singular-value-decomposition failure, and metric-order violation. Its
stable name/value pair supports future conceptual mapping to a Rust error enum,
but no Rust implementation or conformance is established. Enum-contract tests
are software verification of classification vocabulary, not numerical
verification of subtraction or evidence that a matrix operation is
scientifically acceptable. The exception's direct-construction tests likewise
verify only in-memory software structure and taxonomy. Scientific validation and
uncertainty quantification have not been performed. See
:doc:`../verification/operator-record-difference` for executable evidence and
scope.

``OperatorRecordResidualAnalyzer`` consumes an
``OperatorRecordDifferenceResult``. It reports three absolute metrics in
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

These metrics are absolute fixed-representation norms, are not normalized, and
are reported only after exact compatibility succeeds and a represented
difference has been constructed.  They satisfy

.. math::

   0 \leq \varepsilon_{\max}\leq\varepsilon_2\leq\varepsilon_{\mathrm F}.

``OperatorRecordComparisonResult`` is a structural ResultObject: direct
construction rejects any violation of this exact stored norm ordering and does
not estimate floating-point roundoff, repair metric order, or impose a maximum
matrix-dimension policy. Direct callers are responsible for supplying already
canonical metric values. Python and NumPy integer dimensions and real metric
scalars are canonicalized to built-in Python ``int`` and ``float`` values;
metrics must be finite and non-negative. Equality is exact structural equality
over all stored fields, not approximate numerical agreement or physical
operator equivalence. The ResultObject has no approved JSON serialization
contract; any wire format requires a separately approved serializer ActionObject
and specification. Hash behavior is not specified as part of this public
contract.

Because the residual analyzer computes the maximum-entry, Frobenius, and
spectral norms independently, valid outputs can differ by binary64 roundoff.
``OperatorRecordResidualAnalyzer`` owns the numerical policy for this case. Its
metric-order allowance is the larger of a relative component and a lower-ULP
component. For common metric scale ``s > 0`` and dimension ``N``, it uses
``dimension_factor = 4 * max(1, N)``,
``relative_allowance = dimension_factor * eps * s``, and
``ulp_allowance = dimension_factor * (s - nextafter(s, 0.0))``. Exact zero has
zero allowance. This prevents the allowance from underflowing to zero for
positive subnormal metrics while avoiding ``np.spacing`` overflow near the
largest finite binary64 value. Ordering violations within the allowance are
canonicalized upward before ResultObject construction so the stored immutable
values satisfy ``epsilon_max <= epsilon_2 <= epsilon_F`` exactly. Larger ordering
violations raise ``OperatorRecordComparisonNumericalErrorCode.METRIC_ORDER_VIOLATION``;
no absolute tolerance with an implicit energy unit or scientific acceptance
threshold is introduced.

The residual analyzer uses scale-safe Frobenius and spectral norm algorithms for
extreme finite magnitudes such as ``1e200`` and ``1e-200``. Spectral-norm scaling
uses an exact power of two instead of direct complex division by a possibly
subnormal scale, because such division can overflow internally even when the
mathematically normalized matrix is finite. If ``e`` is the binary exponent from
``np.frexp(scale)``, the analyzer forms

.. math::

   \widetilde{\mathbf H}=2^{-e}\Delta\mathbf H

with ``np.ldexp`` applied separately to real and imaginary parts, computes
singular values of ``\widetilde{\mathbf H}``, and restores

.. math::

   \|\Delta\mathbf H\|_2=2^e\|\widetilde{\mathbf H}\|_2.

If a scaled metric becomes nonfinite, if a power-of-two scaled matrix is
nonfinite, if singular-value computation fails, or if the restored norm is truly
nonrepresentable, residual analysis raises ``OperatorRecordComparisonNumericalError``.
Its closed ``OperatorRecordComparisonNumericalErrorCode`` taxonomy has exact
Python 3.14 ``StrEnum`` declaration order:

.. list-table:: Residual-analysis numerical-error codes
   :header-rows: 1

   * - Order
     - Public name
     - Stable value
   * - 1
     - ``NONFINITE_METRIC``
     - ``nonfinite_metric``
   * - 2
     - ``LINEAR_ALGEBRA_FAILURE``
     - ``linear_algebra_failure``
   * - 3
     - ``METRIC_ORDER_VIOLATION``
     - ``metric_order_violation``

``NONFINITE_METRIC`` means a residual metric from a finite represented difference
cannot be represented as finite binary64, including a mathematically finite norm
beyond ``float64`` range. ``LINEAR_ALGEBRA_FAILURE`` means the SVD backend raised
a linear-algebra failure or returned nonfinite singular values while computing
:math:`\varepsilon_2=\sigma_{\max}(\Delta H)`. ``METRIC_ORDER_VIOLATION`` means
raw metrics violate
:math:`0\leq\varepsilon_{\max}\leq\varepsilon_2\leq\varepsilon_{\mathrm F}` by
more than the analyzer-owned allowance; within-allowance differences are
canonicalized instead.

Despite its historical ``Comparison`` name, this taxonomy and its production
emission belong to ``OperatorRecordResidualAnalyzer``.
``OperatorRecordComparator`` may propagate the lower-layer exception but does
not calculate metrics or own the taxonomy.

``OperatorRecordComparisonNumericalError`` is the corresponding public
``ValueError``. Its sole structured category field is ``code``. Positional and
``code=`` keyword construction accept every member of the closed residual enum
and retain the exact supplied object by identity. Raw strings, including all
three stable enum values, and members of unrelated enums are rejected with
``TypeError`` rather than coerced. The former ``reason`` alias is intentionally
absent: valid instances expose no ``reason`` attribute and ``reason=`` is not a
supported constructor form. No additional positional or keyword free-form detail
is accepted or exposed.

The message is a secondary human-readable residual-failure summary containing the
stable code value. Machine logic inspects ``error.code`` and does not parse
punctuation, capitalization, quoting, or separators. The exception has no
independent JSON, dictionary, serializer, or deserializer API.
``OperatorRecordJsonSerializer`` serializes only ``OperatorRecord``; the residual
``StrEnum`` values do not create an exception schema.

Signed subtraction that produces a nonfinite represented difference belongs to
``OperatorRecordDifferenceNumericalError`` and
``OperatorRecordDifferenceNumericalErrorCode.NONFINITE_DIFFERENCE``. Failure to
produce a finite Hermiticity residual belongs to
``HermiticityNumericalError``. Exact representation-metadata incompatibility
belongs to ``IncompatibleOperatorRecordsError`` and is not a residual numerical
failure.

The residual enum has no aliases, descriptions, free-form reasons, integer
discriminants, or serialization methods. Its values are stable ASCII snake-case
strings supporting future conceptual Rust-enum mapping, but no Rust
implementation, conformance, or serialized numerical-exception format is
approved. Direct exception and enum-contract tests are software verification;
actual Analyzer emission remains separate software-verification evidence, while
residual metric accuracy and floating-point behavior remain
numerical-verification evidence. None decides whether a residual is
scientifically acceptable, and no scientific validation or uncertainty
quantification is established. See
:doc:`../verification/operator-record-residual-analyzer` for detailed evidence
ownership. Users may execute ``OperatorRecordCompatibilityAnalyzer``,
``OperatorRecordDifferencer``, and ``OperatorRecordResidualAnalyzer``
independently, or use ``OperatorRecordComparator`` as the composed convenience
Workflow. These checks verify implemented numerical behavior on
already-compatible representations. They do not validate a DFT calculation,
prove that an effective-mass model is scientifically acceptable, or combine
parent-model, numerical/discretization, and model-reduction errors.

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
finiteness, cell linear independence, and the schema-version-1 operator-level
orthonormal-basis requirement are public rules enforced through DataObjects or
the serializer even when JSON Schema cannot express them completely. Runtime,
public-schema, and golden-fixture software evidence have distinct owners and are
traced in :doc:`../verification/operator-record-json-serialization`. No Rust
implementation or cross-language conformance evidence is supplied.

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
