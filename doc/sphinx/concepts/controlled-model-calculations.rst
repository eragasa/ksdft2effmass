Controlled QHO1D and particle-in-a-box calculations
====================================================

The QHO1D and particle-in-a-box calculations are controlled model systems for
studying representation, discretization, compression, and comparison.
They are not silicon calculations and do not validate a semiconductor model.  Their
calculated outputs provide software and numerical evidence only for the finite
mathematical constructions declared by each calculation protocol.

Ownership layers
----------------

The implementation separates four concrete layers.

``ksdft2effmass.operators``
   Owns reusable represented operators, immutable unit-aware quantities, sparse
   matrices, eigensolvers, spectral-subspace selection, and operator compression.

``ksdft2effmass.model_systems``
   Owns mathematical model definitions and reusable evaluations. The concrete
   ``qho1d`` owner owns typed direct analysis, adjacent-grid diagnostics, independent
   verification, and authenticated visualization. It does not imply a
   dimension-neutral QHO implementation. The former JSON-authored QHO1D ``study``
   contract was removed after migration.

``calculations/qho1d``
   Owns the Python-authored QHO1D configuration, direct calculate--verify--render
   scripts, unsealed execution, provenance records, and calculation-owned technical
   report.

``docs/publications/research-monograph``
   Consumes the direct QHO1D result, verification identities, and exact presentation
   copies of authenticated figures. It does not own the numerical algorithms or create
   an independent evidence package.

The API references are :doc:`../api/model-systems` and
:doc:`../api/research-monograph-campaigns`.

QHO1D
-----

.. currentmodule:: ksdft2effmass.model_systems.qho1d

:class:`Qho1dParameters` stores either a fully physical parameter set
or a fully nondimensional one.  The two modes cannot be mixed.  The oscillator
length is

.. math::

   \ell = \sqrt{\frac{\hbar}{m\omega}}.

:class:`Qho1dAnalytical` represents the real-line oscillator.  It
provides the exact number-state energies

.. math::

   E_n = \hbar\omega\left(n + \frac{1}{2}\right)

and normalized Hermite wavefunctions sampled at explicit dimensionless coordinates
:math:`x/\ell`.

:class:`Qho1dFiniteDifference` represents the same oscillator on a
symmetric finite interval with homogeneous Dirichlet data.  It composes a centered
second-order Laplacian, Schrödinger kinetic-energy operator, and sampled quadratic
potential.  The resulting CSR matrix is a finite numerical representation; it is not
the real-line differential operator.

:class:`Qho1dLadderOperators` applies the oscillator energy scale to a
finite occupation-number basis.  Truncation leaves the expected highest-state defect
in the ladder commutator, so the finite commutator must not be identified with the
infinite-dimensional canonical relation.

Common-coordinate comparison
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:class:`Qho1dComparator` compares the spatial and ladder
representations only after constructing an explicit map.  For retained analytical
states sampled on the interior grid, let :math:`S` be the matrix whose columns include
the square-root quadrature weight.  The sampled Gram matrix and symmetric
orthonormalizing map are

.. math::

   G = S^{\mathsf T}S,
   \qquad
   J = S G^{-1/2}.

The comparator rejects a non-positive-definite :math:`G`; it does not silently
regularize the map.  It then forms

.. math::

   H_{\mathrm{grid}\rightarrow K} = J^{\mathsf T} H_h J,
   \qquad
   \Delta H = H_{\mathrm{grid}\rightarrow K} - H_{\mathrm{ladder}}.

The result retains :math:`J`, :math:`G`, :math:`G^{-1/2}`, both common-coordinate
Hamiltonians, the signed difference, map diagnostics, and Frobenius discrepancy
components.  The comparison combines finite-interval and finite-difference effects;
the reported decomposition does not constitute uncertainty quantification.

The direct :class:`Qho1dAnalyzer` processes box half-width, requested grid spacing,
and retained dimension in a deterministic Cartesian product, with retained dimension
varying fastest. :class:`Qho1dCrossGridAnalyzer` compares adjacent coarse/fine
pullbacks at fixed box and retained dimension after state-space alignment. The
calculation is under ``calculations/qho1d`` and uses the explicit nondimensional
convention :math:`\hbar=m=\omega=\ell=1`.

The current discrepancy combines finite-domain closure, centered-difference,
Gram-correction, and floating-point effects. It is not yet an error bound. For an
exactly isometric injection, the computable residual identity

.. math::

   J^{\mathsf T}H_hJ-H_K = J^{\mathsf T}(H_hJ-JH_K)

separates the next a-posteriori bound from later a-priori continuum estimates. The
boundary-adjacent rows and interior stencil residual must be retained separately
before either is interpreted.

One-dimensional particle in a box
---------------------------------

PhysKit owns the ``Piab1D`` model, its unit system, the analytical solution, and the
homogeneous-Dirichlet finite-difference eigensolution. The unit system supplies
:math:`\hbar`; KSD callers provide the box length :math:`L`, particle mass :math:`m`,
and the selected PhysKit unit system. The analytical spectrum is

.. math::

   E_n = \frac{\hbar^2\pi^2n^2}{2mL^2},
   \qquad n=1,2,\ldots.

The PhysKit finite-difference solution uses :math:`N` interior points and spacing
:math:`h=L/(N+1)`. Its exact centered-difference eigenvalues are

.. math::

   E_{n,h}
   = \frac{2\hbar^2}{m h^2}
     \sin^2\left(\frac{n\pi}{2(N+1)}\right),
   \qquad n=1,\ldots,N.

``projectkoios.physkit.qm.piab1d.tise_fd.Piab1dTiseFdSolver`` constructs the
interval, sparse Hamiltonian, and complete real-symmetric eigensystem for one declared
grid. KSD converts that result only at the explicit boundary required by its retained
operator-analysis types. Agreement with PhysKit's discrete closed form checks matrix
construction and eigensolver behavior; comparison with :math:`E_n` measures
finite-difference error for the declared modes and grids.

The optional version-two quadrature record is enabled by default. Project Koios
Numerics supplies the unit-free endpoint-inclusive trapezoidal rule, its explicit
homogeneous-Dirichlet interior restriction, and the diagonal mass matrix. PhysKit
applies the resulting unit-bearing weights to sampled quantum states. This produces
quadrature-normalized nodal amplitudes while retaining the Euclidean-normalized solver
vectors separately; it does not introduce a generalized eigenproblem.

Residual experiment
~~~~~~~~~~~~~~~~~~~

.. currentmodule:: ksdft2effmass.model_systems.piab1d

:class:`Piab1dAnalyzer` selects the lowest spectral subspace with orthonormal basis
:math:`U`, projector :math:`P=UU^{\mathsf T}`, and complement :math:`Q=I-P`. It stores
three differences separately in the typed direct result:

.. math::

   \Delta_{\mathrm{consistent}}
   &= U(U^{\mathsf T}HU)U^{\mathsf T} - PHP, \\
   \Delta_{\mathrm{unmatched}}
   &= U(U^{\mathsf T}HU)U^{\mathsf T} - H, \\
   \Delta_{\mathrm{boundary}}
   &= H_{\mathrm{Dirichlet}} - H_{\mathrm{cyclic}}.

The first is an algebraic consistency check and should vanish up to floating-point
error.  For this spectral subspace the second is checked against the discarded sector
:math:`-QHQ`.  The third compares two declared boundary closures on the same finite
coordinate space; it is not interpreted as a representation-independent continuum
potential.

Auxiliary campaigns
~~~~~~~~~~~~~~~~~~~

The typed :class:`Piab1dCalculationResult` also stores four bounded monograph analyses:
fixed-mode refinement, complete-spectrum and higher-mode diagnostics, raw and
same-grid-normalized residual norms, and two exact decompositions with nested
least-Frobenius model-class fits. :class:`Piab1dVerifier` reconstructs these values
independently of :class:`Piab1dAnalyzer`; :class:`Piab1dVisualizer` renders only an
authenticated passing projection.

The unrestricted identifiability fit is algebraically exact by construction. It does
not identify a physical potential. The restricted residuals depend on the declared
basis, metric, and admissible model class. The former calculation-local campaign
modules, flat version-one wires, and installed ``study`` package were removed after the
direct replacement. Exact Git recovery identities are recorded in the Architecture v3
PIAB1D legacy disposition.

Serialization, provenance, and verification
--------------------------------------------

The direct controlled-model calculations write typed canonical JSON results,
byte-owning independent verification aggregates, authenticated visualization
projections, and development-provenance records. Outputs include repository-relative
paths, SHA-256 identities, implementation-source identities, runtime versions, the
binary64 representation, and the declared eigensolver where applicable.

The independent result verifiers admit exact immutable bytes and reconstruct analytic
or algebraic checks without treating the production analyzer or serializer as the
oracle. A passing verifier establishes only its declared finite software or numerical
requirements. It does not establish physical model adequacy, semiconductor validation,
transferability, or uncertainty quantification. Development-provenance inventories and
semantic verification remain separate contracts.
