Controlled harmonic-oscillator and particle-in-a-box calculations
=================================================================

The harmonic-oscillator and particle-in-a-box calculations are controlled model
systems for studying representation, discretization, compression, and comparison.
They are not silicon calculations and do not validate a semiconductor model.  Their
calculated outputs provide software and numerical evidence only for the finite
mathematical constructions declared by each calculation protocol.

Ownership layers
----------------

The implementation separates four layers.

``ksdft2effmass.operators``
   Owns reusable represented operators, immutable unit-aware quantities, sparse
   matrices, eigensolvers, spectral-subspace selection, and operator compression.

``ksdft2effmass.analysis.model_systems``
   Owns the mathematical model definitions and reusable evaluations.  These objects
   distinguish a continuum operator from a finite matrix representation and do not
   know about monograph files or retained JSON formats.

``ksdft2effmass.campaigns.research_monograph``
   Owns the fixed parameter studies, version-one JSON decoding and serialization,
   deterministic ordering, provenance identities, and independent retained-result
   verification.

``calculations/research-monograph``
   Owns inputs, thin command-line adapters, retained calculated outputs, figures,
   protocols, reports, and checksum catalogs.  The command-line files adapt paths to
   the package-owned classes; they do not own the numerical algorithms.

The API references are :doc:`../api/model-systems` and
:doc:`../api/research-monograph-campaigns`.

Finite harmonic oscillator
--------------------------

.. currentmodule:: ksdft2effmass.analysis.model_systems.harmonic_oscillator

:class:`HarmonicOscillatorParameters` stores either a fully physical parameter set
or a fully nondimensional one.  The two modes cannot be mixed.  The oscillator
length is

.. math::

   \ell = \sqrt{\frac{\hbar}{m\omega}}.

:class:`HarmonicOscillatorAnalytical` represents the real-line oscillator.  It
provides the exact number-state energies

.. math::

   E_n = \hbar\omega\left(n + \frac{1}{2}\right)

and normalized Hermite wavefunctions sampled at explicit dimensionless coordinates
:math:`x/\ell`.

:class:`HarmonicOscillatorFiniteDifference` represents the same oscillator on a
symmetric finite interval with homogeneous Dirichlet data.  It composes a centered
second-order Laplacian, Schrödinger kinetic-energy operator, and sampled quadratic
potential.  The resulting CSR matrix is a finite numerical representation; it is not
the real-line differential operator.

:class:`HarmonicOscillatorLadderOperators` applies the oscillator energy scale to a
finite occupation-number basis.  Truncation leaves the expected highest-state defect
in the ladder commutator, so the finite commutator must not be identified with the
infinite-dimensional canonical relation.

Common-coordinate comparison
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:class:`HarmonicOscillatorComparator` compares the spatial and ladder
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

The monograph campaign evaluates box half-width, requested grid spacing, and retained
dimension in a deterministic Cartesian product, with retained dimension varying
fastest.  The retained calculation uses the explicit nondimensional convention
:math:`\hbar=m=\omega=\ell=1`.

One-dimensional particle in a box
---------------------------------

.. currentmodule:: ksdft2effmass.analysis.model_systems

:class:`ParticleInBoxParameters` stores the box length :math:`L`, particle mass
:math:`m`, and reduced Planck constant :math:`\hbar` in either one fully physical unit
mode or one fully nondimensional mode.  :class:`ParticleInBoxAnalytical` represents
the continuum homogeneous-Dirichlet spectrum

.. math::

   E_n = \frac{\hbar^2\pi^2n^2}{2mL^2},
   \qquad n=1,2,\ldots.

:class:`ParticleInBoxFiniteDifference` uses :math:`N` interior points and spacing
:math:`h=L/(N+1)`.  Its exact centered-difference eigenvalues are

.. math::

   E_{n,h}
   = \frac{2\hbar^2}{m h^2}
     \sin^2\left(\frac{n\pi}{2(N+1)}\right),
   \qquad n=1,\ldots,N.

:class:`ParticleInBoxGridEvaluator` constructs the interval, sparse Hamiltonian, and
complete real-symmetric eigensystem for one declared grid.  It supports either one
fully physical unit mode or the explicitly nondimensional mode used by the retained
monograph campaigns.  In physical mode the coordinate grid has length units, the
homogeneous wavefunction boundary value has inverse-square-root-length units, and the
Hamiltonian and eigenvalues have energy units.  Agreement with the discrete closed
form checks matrix construction and eigensolver behavior; comparison with
:math:`E_n` measures finite-difference error for the declared modes and grids.

Residual experiment
~~~~~~~~~~~~~~~~~~~

.. currentmodule:: ksdft2effmass.campaigns.research_monograph

:class:`ParticleInBoxResidualStudyEvaluator` selects the lowest spectral subspace
with orthonormal basis :math:`U`, projector :math:`P=UU^{\mathsf T}`, and complement
:math:`Q=I-P`.  It keeps three differences separate:

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

The particle-in-a-box directory contains four additional package-owned campaigns.

.. list-table::
   :header-rows: 1
   :widths: 28 72

   * - Owner
     - Represented calculation
   * - :class:`ParticleInBoxConvergenceWorkflow`
     - Fixed-mode continuum energy errors and observed refinement orders over an
       increasing grid sequence.  Raw residual norms from different finite spaces are
       retained only as within-grid diagnostics.
   * - :class:`ParticleInBoxEigenpairSweepWorkflow`
     - Complete finite spectra, higher fixed modes, modes whose indices grow with grid
       dimension, nodal eigenvector overlap, and scaled algebraic residuals.
   * - :class:`ParticleInBoxNormSweepWorkflow`
     - Raw and same-grid-normalized Frobenius, spectral, and maximum-entry residual
       norms.  Maximum-entry results remain basis dependent.
   * - :class:`ParticleInBoxIdentifiabilityWorkflow`
     - Two exact decompositions of one retained Hamiltonian and least-Frobenius fits
       of nested scalar, diagonal, real-symmetric tridiagonal, and unrestricted
       real-symmetric model classes.

The unrestricted identifiability fit is algebraically exact by construction.  It does
not identify a physical potential.  The restricted residuals depend on the declared
basis, metric, and admissible model class.

Serialization, provenance, and verification
--------------------------------------------

The retained calculations use closed version-one JSON inputs and canonical JSON
outputs.  New outputs include repository-relative input and runner paths, SHA-256
identities, implementation-source identities, Python and NumPy versions, the binary64
representation, and the declared eigensolver where applicable.  Paths supplied to
campaign workflows must resolve beneath the explicit repository root.

The independent result verifiers decode the retained representation and reconstruct
analytic or algebraic checks without treating the serializer as the oracle.  A
passing verifier establishes only the verifier's declared finite software or
numerical requirements.  It does not establish physical model adequacy, semiconductor
validation, transferability, or uncertainty quantification.

The checksum catalogs bind the maintained calculation artifacts as a set.  They do
not replace the semantic verifiers, and a successful semantic verifier does not
replace checksum agreement.
