PIAB1D eigenpair-sweep verification
===================================

Purpose and public contract
---------------------------

``Piab1dEigenpairSweepResultsVerifier`` authenticates one version-one retained result
for the full-spectrum and fixed-mode one-dimensional particle-in-a-box campaign. It
returns immutable typed reports that keep source authentication, numerical checks, and
their aggregate disposition separate. Content disagreement produces failed report
channels; malformed wire data, invalid scalar values, unsafe paths, and inconsistent
collection shapes raise exceptions.

The verifier does not import the producing
``Piab1dEigenpairSweepWorkflow``, grid evaluator, Hamiltonian constructor,
eigensolver, convergence estimator, or serializer. The represented subject is a
controlled dimensionless particle in a Dirichlet interval. The mathematical objects are
the continuum kinetic operator and its centered second-order finite-difference matrix.
The numerical representation is an ordered collection of binary64 scalar records, not
a retained operator or eigenvector array.

Mathematical representation
---------------------------

For interval length :math:`L`, particle mass :math:`m`, reduced Planck constant
:math:`\hbar`, and :math:`N` interior points, the grid spacing is

.. math::
   :label: piab-eigenpair-grid-spacing

   h = \frac{L}{N+1}.

The analytical Dirichlet energy of mode :math:`n` is

.. math::
   :label: piab-eigenpair-continuum-energy

   E_n = \frac{\hbar^2\pi^2 n^2}{2mL^2}.

For the centered second-order Dirichlet matrix, define the modal phase

.. math::
   :label: piab-eigenpair-modal-phase

   z_{n,N} = \frac{n\pi}{2(N+1)}.

Its exact discrete eigenvalue :math:`\varepsilon_{n,N}` satisfies

.. math::
   :label: piab-eigenpair-dispersion-ratio

   \frac{\varepsilon_{n,N}}{E_n}
   = \left(\frac{\sin z_{n,N}}{z_{n,N}}\right)^2,

so the nonnegative relative dispersion error reconstructed by the verifier is

.. math::
   :label: piab-eigenpair-relative-error

   \delta_{n,N}
   = 1 - \left(\frac{\sin z_{n,N}}{z_{n,N}}\right)^2.

The retained computed energy :math:`\widetilde E_{n,N}`, continuum energy, and reported
relative error must also satisfy the exact serialized relation

.. math::
   :label: piab-eigenpair-reported-relation

   \delta^{\mathrm{reported}}_{n,N}
   = \frac{|\widetilde E_{n,N}-E_n|}{E_n}.

This relation replaces an otherwise unsubstantiated direct-energy allowance. Together,
Equations :eq:`piab-eigenpair-continuum-energy`,
:eq:`piab-eigenpair-relative-error`, and
:eq:`piab-eigenpair-reported-relation` constrain the represented computed energy without
claiming a general eigensolver forward-error theorem.

For consecutive fixed-mode observations :math:`(h_a,\delta_a)` and
:math:`(h_b,\delta_b)`, the independently reconstructed observed order is

.. math::
   :label: piab-eigenpair-observed-order

   p = \frac{\log(\delta_a/\delta_b)}{\log(h_a/h_b)}.

The retained nodal-overlap and scaled-residual diagnostics represent

.. math::
   :label: piab-eigenpair-nodal-overlap

   d_{n,N} = 1 - |\mathbf v_{n,N}^{\mathsf T}\mathbf s_{n,N}|,

and

.. math::
   :label: piab-eigenpair-scaled-residual

   r_{n,N}
   = \frac{\|\mathbf H_N\mathbf v_{n,N}
     - \widetilde E_{n,N}\mathbf v_{n,N}\|_2}
     {\max_j |\widetilde E_{j,N}|}.

The result document does not retain :math:`\mathbf H_N`, :math:`\mathbf v_{n,N}`, or
:math:`\mathbf s_{n,N}`. Consequently, the verifier checks the represented diagnostics'
finite-value, threshold, and per-grid maximum relations but does not recompute them from
absent arrays.

Symbols, units, domains, and ordering
-------------------------------------

All physical-looking quantities in this campaign are dimensionless.

.. list-table::
   :header-rows: 1
   :widths: 16 38 16 30

   * - Symbol
     - Meaning
     - Unit
     - Domain and ordering
   * - :math:`L`
     - Dirichlet interval length
     - dimensionless
     - finite real, :math:`L>0`
   * - :math:`m`
     - particle mass parameter
     - dimensionless
     - finite real, :math:`m>0`
   * - :math:`\hbar`
     - reduced Planck parameter
     - dimensionless
     - finite real, :math:`\hbar>0`
   * - :math:`N`
     - number of interior grid points
     - dimensionless count
     - positive integer; grids are strictly increasing
   * - :math:`n`
     - one-based mode index
     - dimensionless count
     - :math:`1\leq n\leq N`; records are in ascending order
   * - :math:`h`
     - grid spacing
     - dimensionless
     - positive binary64 value
   * - :math:`E_n`
     - continuum Dirichlet energy
     - dimensionless energy
     - positive binary64 value
   * - :math:`\widetilde E_{n,N}`
     - represented computed discrete energy
     - dimensionless energy
     - positive binary64 value
   * - :math:`\delta_{n,N}`
     - relative dispersion error
     - dimensionless
     - finite and nonnegative
   * - :math:`d_{n,N}`
     - nodal-overlap defect
     - dimensionless
     - finite and nonnegative
   * - :math:`r_{n,N}`
     - scaled algebraic residual
     - dimensionless
     - finite and nonnegative
   * - :math:`p`
     - pairwise observed convergence order
     - dimensionless
     - finite real
   * - :math:`\epsilon_{64}`
     - binary64 machine epsilon
     - dimensionless
     - ``numpy.finfo(numpy.float64).eps``

Algorithm and data flow
-----------------------

The verifier performs the following bounded operations:

#. decode the UTF-8 JSON document into the closed ``JsonValue`` representation;
#. enforce the version-one schema, evidence status, calculation status, experiment
   identity, and exact limitation inventory;
#. authenticate the decoded provenance with ``Piab1dSourceAuthenticator``;
#. reconstruct grid spacing, mode inventories, fractional indices, analytical energies,
   dispersion errors, reported-energy relations, grid diagnostic maxima, fixed-mode
   series, and observed orders;
#. evaluate all 16 declared channels exactly once; and
#. derive grid, eigenpair, fixed-mode-series, and channel counts from decoded
   collections rather than fixed campaign constants.

For the retained campaign, the reconstructed collection sizes are six grids, 504
full-spectrum eigenpair records, and three fixed-mode series. Those values describe the
retained artifact; the AbstractResultObject still derives them at runtime.

Tolerance and failure policy
----------------------------

Exact structural and algebraic relations use zero tolerance. The strict
:math:`d_{n,N}<10^{-13}` and :math:`r_{n,N}<10^{-13}` version-one requirements are
represented by the greatest binary64 value below :math:`10^{-13}`, allowing the
AbstractResultObject to retain an inclusive comparison.

The represented relative dispersion error is compared with Equation
:eq:`piab-eigenpair-relative-error` using

.. math::
   :label: piab-eigenpair-roundoff-envelope

   \alpha_{n,N}
   = \frac{2^7\epsilon_{64}}{h^2E_n}.

The factor :math:`2^7` is inherited version-one compatibility policy from the
independent verifier. It is documented and named in source, but is not asserted to be a
derived forward-error bound for SciPy, LAPACK, or all symmetric eigensolvers. Removing
or replacing it requires a separate numerical-contract decision and corresponding
evidence.

Represented observed orders use an absolute-plus-relative reconstruction allowance
:math:`2\times10^{-10}+2\times10^{-10}|p|`. Near-second-order fixed-mode behavior and
stronger error near the spectral edge are expected patterns recorded by the input, not
verification conditions. A caller can summarize a chosen pair of modes with
:class:`ksdft2effmass.analysis.SpectralDispersionContrast`; the complete error curve
contains more information than that two-point diagnostic.

Source and compatibility behavior
---------------------------------

Current result documents carry input, runner, and exact implementation-source SHA-256
identities. Historical documents without implementation identities may recognize only
the explicitly recorded historical runner digest. Historical recognition does not
assert equality with current bytes. Every declared source path is resolved beneath the
explicit repository root; absolute paths and escaping paths are rejected.

The supported campaign-root import remains
``ksdft2effmass.campaigns.piab1d.Piab1dEigenpairSweepResultsVerifier``. Typed report
classes are documented from their defining module and do not expand the curated
campaign-root export list.

Mappings and retained artifacts
-------------------------------

.. list-table::
   :header-rows: 1
   :widths: 38 62

   * - Surface
     - Repository path
   * - Verifier and ResultObjects
     - ``python/src/ksdft2effmass/campaigns/piab1d/verification/eigenpair_sweep.py``
   * - Shared source authentication
     - ``python/src/ksdft2effmass/campaigns/piab1d/verification/source.py``
   * - Producing Workflow, excluded from verifier imports
     - ``python/src/ksdft2effmass/campaigns/piab1d/eigenpair_sweep.py``
   * - Maintained software-verification evidence
     - ``python/tests/software_verification/ksdft2effmass/campaigns/piab1d/test__Piab1dAuxiliaryCampaigns.py``
   * - Version-one protocol
     - ``calculations/research-monograph/particle-in-box/protocol.md``
   * - Retained input and result
     - ``calculations/research-monograph/particle-in-box/eigenpair-sweep-input.json`` and ``eigenpair-sweep-result.json``
   * - Retained content catalog
     - ``calculations/research-monograph/particle-in-box/SHA256SUMS``
   * - Scientific-methodology authority
     - ``docs/publications/research-monograph/appendices/D-particle-in-a-box-residuals.tex``

References and provenance
-------------------------

The software contract is repository-derived from the version-one protocol, retained
input/result pair, and Appendix D listed above. Appendix D cites the following verified
finite-difference reference for the centered Dirichlet discretization:

* John C. Strikwerda, *Finite Difference Schemes and Partial Differential Equations*,
  second edition, SIAM, 2004, DOI `10.1137/1.9780898717938
  <https://doi.org/10.1137/1.9780898717938>`_.

No external reference is used to justify the :math:`2^7` compatibility multiplier. It
is retained version-one reconstruction policy.

Evidence status and limitations
-------------------------------

The retained analytical identities, dispersion reconstruction, and represented-order
reconstruction are numerical-verification evidence for the declared finite
discretization. Wire validation, typed results, source-path containment, import
identity, and separate source and numerical outcomes are software-verification
evidence.

The nodal-overlap defect does not measure continuum interpolation error. Fixed-mode
second-order behavior does not imply uniform spectral or operator convergence. Source
correlation does not establish numerical correctness. Passing reports do not validate a
semiconductor model, material physics, transferability, or uncertainty propagation.
Human acceptance is not inferred from verifier output.

API
---

.. currentmodule:: ksdft2effmass.campaigns.piab1d.verification.eigenpair_sweep

.. autoclass:: Piab1dEigenpairSweepVerificationChannel
   :members:

.. autoclass:: Piab1dEigenpairSweepResultsVerifier
   :members:
