Geometry verification evidence
==============================

Scope and represented object
----------------------------

``Geometry`` is the finite geometry-metadata DataObject used by
``OperatorRecord``. It stores exactly ``system``, ``cell``,
``boundary_conditions``, ``coordinate_convention``, and ``length_unit``. The
cell contains three row lattice vectors,

.. math::

   \mathbf C=
   \begin{pmatrix}
   \mathbf a_1^{\mathsf T}\\
   \mathbf a_2^{\mathsf T}\\
   \mathbf a_3^{\mathsf T}
   \end{pmatrix}\in\mathbb R^{3\times3}.

``cell[i][j]`` is component ``j`` of row vector ``i`` in the explicit
``length_unit`` and under the explicit ``coordinate_convention``. Those strings,
``system``, and ``boundary_conditions`` are nonempty descriptive metadata, not
controlled vocabularies. They are preserved exactly without trimming, case
folding, registry lookup, normalization, conversion, or semantic interpretation.

Software-verification ownership
-------------------------------

The target software-verification facets are:

* ``test__Geometry__construction.py``: ``SV-G-001`` through ``SV-G-006``;
* ``test__Geometry__invariants.py``: ``SV-G-007`` through ``SV-G-019``;
* ``test__Geometry__value_semantics.py``: ``SV-G-020`` through ``SV-G-022``.

Construction admits tuple and list outer containers and tuple and list rows under
the approved ordered-sequence contract. Component inputs may be Python integers,
Python floats, NumPy integer scalars, or NumPy floating scalars. The constructor,
not test preprocessing, defensively canonicalizes them to
``tuple[tuple[float, float, float], ...]``: both container levels are exact
built-in tuples and every component has exact built-in ``float`` type. Row order,
component signs, and metadata spelling/case/spacing/punctuation are retained.
Mutation of caller-owned inner or outer lists cannot alter stored state.

Bare strings, bytes, mappings, sets, frozensets, generators, unordered
containers, and arbitrary objects are not approved cell/row containers. Boolean
and NumPy Boolean values, numeric strings, bytes, complex values, ``None``, and
arbitrary objects are not real cell components. Wrong semantic container or
scalar types raise ``TypeError``. Approved ordered sequences with too few or too
many rows/components raise ``ValueError``. NaN, positive/negative infinity, and
accepted integers whose binary64 conversion overflows raise the documented
finite-component ``ValueError``; raw ``OverflowError`` does not leak.

All four metadata fields independently require a Python string. Wrong semantic
types raise field-specific ``TypeError`` and empty strings raise field-specific
``ValueError``. Whitespace-only or unusual strings remain nonempty exact metadata
and are not normalized.

The DataObject is frozen and slotted with tuple-backed nested state and no
per-instance ``__dict__``. Equality is exact structural equality over every
stored field. It distinguishes row permutations, component changes, and sign
changes; it is not approximate comparison or physical equivalence. No hash
contract is assigned by this evidence. Geometry has no standalone ``serialize``,
``deserialize``, ``to_json``, ``from_json``, ``to_dict``, or ``from_dict`` API.
Only ``OperatorRecordJsonSerializer`` owns Geometry's nested record wire
representation.

Numerical-verification ownership
--------------------------------

The target numerical-verification module
``test__Geometry__linear_independence.py`` owns ``NV-G-001`` through
``NV-G-009``. ``Geometry.LINEAR_INDEPENDENCE_RTOL`` is an explicitly documented
public, dimensionless policy attribute with value
:math:`r_{\mathrm{tol}}=10^{-12}`. Define

.. math::

   \rho(\mathbf C)=
   \frac{\sigma_{\min}(\mathbf C)}{\sigma_{\max}(\mathbf C)}.

The implemented strict criterion is

.. math::

   \sigma_{\max}>0
   \quad\text{and}\quad
   \sigma_{\min}>r_{\mathrm{tol}}\sigma_{\max},

or equivalently :math:`\rho(\mathbf C)>r_{\mathrm{tol}}` when
:math:`\sigma_{\max}>0`. Equality is rejected by the documented strict
inequality. The evidence independently fixes the public tolerance at ``1e-12``
and uses diagonal cells for clearly below, exact-equality, and clearly above
ratios; diagonal singular values make the equality oracle explicit and stable for
the stored public binary64 tolerance.

Before singular-value calculation, production divides every finite component by
the largest absolute component. This scale is positive for any candidate capable
of being independent. Normalization preserves the singular-value ratio while
avoiding avoidable overflow/underflow for extreme finite component magnitudes.
Consequently,

.. math::

   \rho(s\mathbf C)=\rho(\mathbf C),\qquad s\ne0,

over the supported binary64 calculation, and row permutation preserves the
validity decision. Stored exact value remains row-order sensitive even though the
independence decision is row-permutation invariant.

The analytical evidence cases are:

* ``NV-G-001``: ``diag(1, 2, 4)`` has singular values ``1``, ``2``, and ``4``;
* ``NV-G-002``: duplicated rows have the exact nontrivial relation
  :math:`\mathbf a_2-\mathbf a_1=0`;
* ``NV-G-003``: a skew triangular cell has nonzero diagonal product ``24``;
* ``NV-G-004``: a left-handed triangular cell has diagonal product ``-24`` and
  remains valid because handedness is not an invariant;
* ``NV-G-005`` and ``NV-G-006``: diagonal cells attest the exact public
  ``1e-12`` tolerance and have analytical ratios
  :math:`r_{\mathrm{tol}}/2`, :math:`r_{\mathrm{tol}}`, and
  :math:`2r_{\mathrm{tol}}`, confirming the strict equality boundary;
* ``NV-G-007``: scaled identities at both signs of ``1e-200``, ``1``, and
  ``1e200`` retain ratio one;
* ``NV-G-008``: scaled below-threshold diagonal cells at the same signed scales
  retain ratio :math:`r_{\mathrm{tol}}/2`;
* ``NV-G-009``: every row permutation preserves the full-rank triangular argument
  or the exact duplicated-row dependence.

Expected decisions use these analytical arguments. Tests do not call
``numpy.linalg.matrix_rank``, ``numpy.linalg.svd``, or ``numpy.linalg.det`` to
construct an oracle and do not reference private Geometry methods. Every
numerical construction runs with ``RuntimeWarning`` promoted to an error, so a
pass establishes both the documented decision and absence of leaked NumPy
runtime warnings for these cases.

Scientific and implementation boundaries
-----------------------------------------

A valid Geometry cell need not be orthogonal, normalized, cubic, right-handed,
positive-determinant, physically realistic, relaxed, or associated with a
validated crystal structure. Geometry performs no coordinate transformation,
unit conversion, dimensional analysis, crystallographic lookup, DFT or Wannier
calculation, impurity calculation, or structure relaxation.

Software-verification passing means the Python object satisfies its documented
construction, invariant, ownership, error-taxonomy, and exact-value contract.
Numerical-verification passing means the implemented binary64 independence
criterion agrees with the listed analytical fixtures and tested scales and
permutations. Neither class establishes physical structure validity or a
scientifically appropriate threshold for an intended use. Scientific validation
has not been performed. Uncertainty quantification has not been performed. A
conceptual Rust struct can represent the five fields and validated constructor,
but no Rust implementation or Python/Rust conformance evidence is provided.
