OperatorRecord residual-analysis numerical verification
=======================================================

This page records numerical-verification evidence for
``OperatorRecordResidualAnalyzer``. It concerns the implemented finite-matrix
norm kernel only. It does not establish physical equivalence between represented
Hamiltonians, validate a reduced model, or perform uncertainty quantification.

Metric definitions
------------------

For a represented difference

.. math::

   \Delta H = H_{\mathrm{candidate}} - H_{\mathrm{reference}},

stored as a finite ``numpy.complex128`` matrix, the analyzer computes

.. math::

   \varepsilon_{\max}=\max_{i,j}|\Delta H_{ij}|,

.. math::

   \varepsilon_{\mathrm F}=\sqrt{\sum_{i,j}|\Delta H_{ij}|^2},

and

.. math::

   \varepsilon_2=\sigma_{\max}(\Delta H).

Stored metrics satisfy

.. math::

   0 \leq \varepsilon_{\max} \leq \varepsilon_2
   \leq \varepsilon_{\mathrm F}.

Small binary64 ordering discrepancies may be canonicalized upward by the
analyzer. A material violation raises ``METRIC_ORDER_VIOLATION``.

Analytical evidence
-------------------

The analytical suite uses six stable evidence identifiers. Expected values are
derived below; they are not generated with ``numpy.linalg.svd``,
``numpy.linalg.norm``, or the production analyzer.

``NV-ORA-001`` — exact zero ``2 x 2`` matrix
   For

   .. math::

      \Delta H=\begin{pmatrix}0&0\\0&0\end{pmatrix},

   every entry and singular value is zero. Therefore all three metrics are
   exactly zero.

``NV-ORA-002`` — diagonal 3-4 matrix
   For

   .. math::

      \Delta H=\begin{pmatrix}3&0\\0&4\end{pmatrix},

   the largest entry magnitude is 4,
   :math:`\varepsilon_{\mathrm F}=\sqrt{3^2+4^2}=5`, and the singular values
   are 3 and 4. Thus
   :math:`(\varepsilon_{\max},\varepsilon_{\mathrm F},\varepsilon_2)=(4,5,4)`.

``NV-ORA-003`` — complex scalar 3+4i
   For :math:`\Delta H=(3+4i)`, the only singular value is
   :math:`|3+4i|=5`; all three metrics equal 5.

``NV-ORA-004`` — nonsymmetric rank-one matrix
   For

   .. math::

      \Delta H=\begin{pmatrix}0&3\\0&4\end{pmatrix},

   the only nonzero column has Euclidean norm 5. The rank-one matrix therefore
   has one nonzero singular value equal to 5, while its largest entry magnitude
   is 4. Hence
   :math:`(\varepsilon_{\max},\varepsilon_{\mathrm F},\varepsilon_2)=(4,5,5)`.

``NV-ORA-005`` — large normal-scale rank-one matrix
   For :math:`\Delta H=\operatorname{diag}(10^{200},0)`, one entry and one
   singular value are nonzero, so every metric is :math:`10^{200}`.

``NV-ORA-006`` — small normal-scale rank-one matrix
   For :math:`\Delta H=\operatorname{diag}(10^{-200},0)`, one entry and one
   singular value are nonzero, so every metric is :math:`10^{-200}`.

All matrices are at most ``2 x 2`` and use ``numpy.complex128``. The common
``eV`` unit is synthetic deterministic metadata, not evidence of physical or
scientific validity.

Binary64 analytical acceptance
------------------------------

Expected zero requires exact equality. For a nonzero normal-scale expected value
:math:`x`, the analytical suite accepts a metric only when

.. math::

   |x_{\mathrm{actual}}-x|
   \leq 64\epsilon_{\mathrm{mach}}|x|.

The stored metrics are binary64 floats. For every nonzero analytical case, the
allowed error is representable, positive, and strictly smaller than :math:`|x|`.
Consequently, an actual value of zero cannot pass a nonzero case.

The factor :math:`64\epsilon_{\mathrm{mach}}` is a conservative regression
criterion for these small matrices and their absolute-value, scaled-summation,
and SVD calculations. It is not a formal global forward-error bound for
arbitrary matrix dimensions or conditioning, a production comparison policy, or
a scientific acceptance tolerance. Every analytical execution also treats
``RuntimeWarning`` as an error.

Floating-point regression evidence
----------------------------------

The floating-point module verifies representable behavior separately from the
six analytical cases. Its stable evidence and scale regimes are:

.. list-table:: Floating-point residual evidence
   :header-rows: 1
   :widths: 18 36 46

   * - Evidence
     - Input regime
     - Independent oracle
   * - ``NV-ORA-007``
     - :math:`(1+i)10^{100}` scalar
     - ``math.hypot`` of stored binary64 components
   * - ``NV-ORA-008``
     - :math:`(1+2i)10^{100}` scalar
     - ``math.hypot`` of stored binary64 components
   * - ``NV-ORA-009``
     - real scalar :math:`10^{-200}`
     - exact stored real magnitude
   * - ``NV-ORA-010``
     - :math:`(1+i)10^{-310}` subnormal
     - ``math.hypot`` of stored binary64 components
   * - ``NV-ORA-011``
     - :math:`(1+2i)10^{-310}` subnormal
     - ``math.hypot`` of stored binary64 components
   * - ``NV-ORA-012``
     - real scalar :math:`10^{-320}`
     - ``math.hypot`` of stored binary64 components
   * - ``NV-ORA-013``
     - :math:`(1+i)10^{-320}` subnormal
     - ``math.hypot`` of stored binary64 components
   * - ``NV-ORA-014``
     - smallest positive binary64 subnormal
     - exact value from ``numpy.nextafter(0, 1)``
   * - ``NV-ORA-015``
     - two-dimensional subnormal matrix
     - analytical coefficient-matrix norms
   * - ``NV-ORA-016``
     - largest finite binary64 scalar
     - exact stored real magnitude
   * - ``NV-ORA-017``
     - exact scalar zero
     - exact mathematical zero

For complex scalar cases, ``math.hypot(real, imag)`` is an independent scalar
binary64 oracle for the actual stored components. It is not the production
analyzer, NumPy SVD, or NumPy norm. Normal nonzero values use the same explicit
:math:`64\epsilon_{\mathrm{mach}}` criterion as the analytical module; the
allowed error is positive and smaller than the expected magnitude, so zero
cannot pass.

Subnormal values use at most eight ULPs, where one ULP is one adjacent
representable binary64 step in the relevant subnormal region. Relative error is
unsuitable because its allowed error can underflow. Expected and actual values
must both be strictly positive, so zero cannot pass. Eight ULPs is a conservative
regression limit for the scalar magnitude, scaled Frobenius, and scaled spectral
paths exercised here. It is not a formal arbitrary-matrix or backend-independent
error bound and is not a physical tolerance. On the supported Python 3.14/NumPy
environment, the maximum observed distance across ``NV-ORA-010`` through
``NV-ORA-015`` was **zero ULPs**, leaving eight ULPs of regression headroom.

``NV-ORA-014`` requires IEEE-754 binary64 gradual underflow. A runtime that
flushes the smallest positive subnormal to zero does not satisfy this verified
contract.

For ``NV-ORA-015``, let

.. math::

   \Delta H=10^{-310}
   \begin{pmatrix}2+2i&2-2i\\1&-i\end{pmatrix}.

The largest entry magnitude is :math:`2\sqrt{2}\,10^{-310}` and the Frobenius
norm is :math:`\sqrt{8+8+1+1}\,10^{-310}=3\sqrt{2}\,10^{-310}`. For the
coefficient matrix :math:`A`,

.. math::

   A^\dagger A=\begin{pmatrix}9&-9i\\9i&9\end{pmatrix},

whose eigenvalues are 18 and 0. The spectral norm is therefore also
:math:`3\sqrt{2}\,10^{-310}`. Public roundoff canonicalization stores the
spectral and Frobenius metrics exactly equal for this regression while
preserving exact metric ordering.

``NV-ORA-016`` confirms that scale restoration remains finite for a ``1 x 1``
matrix containing ``numpy.finfo(numpy.float64).max``; all three norms equal that
representable scalar. This differs from software-verification evidence
``SV-ORA-006``, where multiple finite entries have a true Frobenius norm beyond
binary64 range and must produce ``NONFINITE_METRIC``. The nonrepresentable case
is not duplicated under a numerical-verification identifier.

``NV-ORA-017`` requires exact zero for every metric and exercises the public
zero-scale path without calling private allowance logic. Every floating-point
case promotes ``RuntimeWarning`` to an exception. Passing therefore establishes
both the stated representable output criterion and absence of leaked NumPy
runtime warnings.

Platform assumptions are finite ``numpy.complex128`` inputs, binary64 real
metrics, IEEE-754 gradual underflow for subnormal cases, and the repository-
supported Python 3.14/NumPy environment. These tests do not provide arbitrary-
dimension forward-error bounds, BLAS-independent formal guarantees, scientific
model validation, uncertainty quantification, or a physical residual-acceptance
criterion.

Closed residual numerical-error enum
------------------------------------

``OperatorRecordComparisonNumericalErrorCode`` is the closed Python 3.14
``StrEnum`` for residual-analysis numerical failures. Despite its retained
historical ``Comparison`` name, ``OperatorRecordResidualAnalyzer`` owns
production emission of these codes. ``OperatorRecordComparator`` may propagate
the resulting lower-layer exception as a Workflow, but it neither calculates
residual metrics nor owns this taxonomy.

The exact declaration order is:

.. list-table:: Residual-analysis numerical-error enum contract
   :header-rows: 1

   * - Order
     - Public name
     - Stable machine-readable value
   * - 1
     - ``NONFINITE_METRIC``
     - ``nonfinite_metric``
   * - 2
     - ``LINEAR_ALGEBRA_FAILURE``
     - ``linear_algebra_failure``
   * - 3
     - ``METRIC_ORDER_VIOLATION``
     - ``metric_order_violation``

The enum has no aliases, integer discriminants, description properties,
free-form reasons, or serialization methods. Every value behaves as an ASCII
lowercase snake-case string. Name and value lookups use standard Enum semantics.
The stable vocabulary supports future conceptual mapping to a Rust enum, but no
Rust implementation, conformance, JSON schema, or serialized numerical-exception
format is approved.

Structured failure conditions
-----------------------------

``NONFINITE_METRIC``
   A finite represented-difference matrix leads to a residual metric that cannot
   be represented as a finite binary64 scalar. This includes a mathematically
   finite norm exceeding finite ``float64`` range. It is distinct from
   ``OperatorRecordDifferenceNumericalErrorCode.NONFINITE_DIFFERENCE``, which
   belongs to represented subtraction before residual analysis.

``LINEAR_ALGEBRA_FAILURE``
   The spectral-norm calculation fails because the SVD backend raises a linear-
   algebra failure or returns nonfinite singular values while computing

   .. math::

      \varepsilon_2=\sigma_{\max}(\Delta H).

``METRIC_ORDER_VIOLATION``
   Independently computed raw metrics violate

   .. math::

      0\leq\varepsilon_{\max}\leq\varepsilon_2\leq\varepsilon_{\mathrm F}

   by more than the analyzer-owned floating-point allowance. Roundoff-scale
   differences within the allowance are canonicalized by the analyzer and do
   not produce this error.

Direct structured-exception evidence
------------------------------------

``OperatorRecordComparisonNumericalError`` is a public ``ValueError`` with one
structured category field, ``code``. Positional and ``code=`` keyword
construction accept every ``OperatorRecordComparisonNumericalErrorCode`` member
and retain the exact supplied enum object by identity. The former ``reason``
alias is intentionally absent. Raw strings, including all three stable enum
values, members of unrelated enums, ``None``, Booleans, integers, and arbitrary
objects are rejected with ``TypeError`` rather than coerced.

The exception accepts no additional positional or keyword free-form detail. Its
message is a secondary human-readable summary that identifies an operator-record
residual numerical failure and includes the stable code value; callers inspect
``error.code`` and must not parse message formatting. The exception exposes no
independent JSON, dictionary, serializer, or deserializer API. In particular,
``OperatorRecordJsonSerializer`` serializes only ``OperatorRecord`` and the
``StrEnum`` value does not independently approve a numerical-exception schema.

``SV-ORCNE-001`` through ``SV-ORCNE-008`` verify direct construction and
``ValueError`` hierarchy, complete code admission and exact identity retention,
positional/keyword equivalence, semantic diagnostics, invalid-type rejection,
continued removal of ``reason``, arbitrary-detail exclusion, and serialization
exclusion. These direct tests do not execute ``OperatorRecordResidualAnalyzer``
or ``OperatorRecordComparator`` and do not produce the numerical conditions.
Analyzer production emission belongs to ``SV-ORA``; Workflow propagation belongs
to ``SV-ORC``; metric accuracy and representable floating-point behavior belong
to ``NV-ORA``.

``SV-ORCNEC-001`` through ``SV-ORCNEC-006`` separately verify the exact
three-member sequence, stable names/values/order, alias absence, Python 3.14
``StrEnum`` behavior, name/value lookup round trips, and exact invalid-lookup
taxonomy. Those are software-verification tests of vocabulary only. Enum tests
perform no metric calculation, SVD, differencing, roundoff canonicalization, or
Workflow execution.

Evidence boundaries and status
------------------------------

For the seventeen cases documented on this page:

* ``software_verification``: metadata propagation, public input typing, and
  structured error translation, including nonrepresentable output under
  ``SV-ORA-006``, are covered separately and are not duplicated as numerical
  oracles;
* ``numerical_verification``: six analytical cases and eleven representable
  floating-point cases pass under their explicit binary64 criteria and warning
  boundaries;
* ``scientific_validation``: not performed;
* ``uncertainty_quantification``: not performed.

Passing these cases or the direct exception evidence does not establish basis
or gauge alignment, physical Hamiltonian equivalence, DFT or Wannier accuracy,
scientific acceptability of a residual, model validity, or uncertainty bounds.
No convergence claim is made because this kernel has no discretization or
refinement parameter. The exception taxonomy has only conceptual future Rust
mapping; no Rust implementation, serialization, or conformance evidence exists.
