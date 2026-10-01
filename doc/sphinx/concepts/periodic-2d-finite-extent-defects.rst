Periodic two-dimensional finite-extent defects
==============================================

Purpose
-------

The controlled periodic-2D defect campaign asks whether a modification of a periodic
bulk representation can be isolated as a perturbation of finite spatial extent.  The
software contract distinguishes three mathematical operators:

.. math::

   H_0,
   \qquad
   \Delta H,
   \qquad
   H_{\mathrm{def}} = H_0 + \Delta H.

``H_0`` is the translation-invariant bulk Hamiltonian, ``Delta H`` is the defect
perturbation, and ``H_def`` is the modified Hamiltonian.  Their finite sparse matrices
are numerical representations on an explicitly declared periodic lattice shape and
boundary-twist fiber.  The calculation does not identify a finite matrix with an
infinite-system operator or a material potential.

An onsite-only ``Delta H`` is a scalar perturbation potential in the represented
lattice basis.  A perturbation containing bond terms changes off-diagonal hopping and
is therefore a more general finite-extent operator perturbation.  The implementation
preserves this distinction through
:attr:`~ksdft2effmass.campaigns.research_monograph.Periodic2DDefectModel.represents_onsite_potential`.

Encapsulated model and representation
--------------------------------------

.. currentmodule:: ksdft2effmass.campaigns.research_monograph

:class:`Periodic2DDefectModel` encapsulates one
:class:`~ksdft2effmass.solid_state.ScalarHoppingModel` and one
:class:`~ksdft2effmass.solid_state.LocalizedPerturbation`.  The perturbation is a
finite, canonically ordered tuple of onsite and directed-bond terms relative to a
declared defect origin.  The model owns only immutable state and intrinsic
two-dimensional invariants.

:class:`Periodic2DDefectRepresenter` receives the model together with an explicit
finite shape and boundary-twist lift.  It separately constructs the sparse bulk and
perturbation matrices, checks their represented compatibility, and then composes the
defect matrix.  Its result retains all four objects:

* the represented bulk operator;
* the represented perturbation operator;
* compatibility evidence; and
* the represented defect operator.

Direct composition is permitted only when shape, twist fiber, scalar basis, energy
unit, and energy-reference identity agree.  No conversion between unmatched state
spaces is inferred from equal matrix dimensions.

Perturbation extraction
-----------------------

Given already aligned bulk and defect representations, the extraction operation is

.. math::

   \Delta H_{\mathrm{ext}} = H_{\mathrm{def}} - H_0.

:class:`Periodic2DDefectPerturbationExtractor` performs this subtraction only after
checking the same geometry, twist, basis, unit, and energy-reference metadata required
for composition.  It does not infer a site map, perform a gauge transformation, align
subspaces, or estimate an energy-zero shift.  Those are logically prior operations.
If any prerequisite differs, extraction stops instead of returning an unidentified
matrix difference.

The synthetic software-verification case constructs a known one-site perturbation,
forms ``H_def``, and recovers the planted represented perturbation exactly.  This is a
round-trip verification of the represented software contract, not evidence that an
unknown material defect has been inferred.

Finite-extent assessment
------------------------

Finite extent is measured rather than assumed from the model name.  For a declared
defect origin and nonnegative integer core radius, sites are assigned minimum-image
Chebyshev shells.  Let ``P_r`` project onto sites in the core and
``Q_r = I - P_r`` project onto its exterior.  The locality Actionizer reports

.. math::

   \varepsilon_{\mathrm{core}}
   &= \lVert P_r \Delta H P_r \rVert_{\mathrm F}, \\
   \varepsilon_{\mathrm{ext}}
   &= \lVert Q_r \Delta H Q_r \rVert_{\mathrm F}, \\
   \varepsilon_{\mathrm{cross}}
   &= \left(
      \lVert P_r \Delta H Q_r \rVert_{\mathrm F}^2
      + \lVert Q_r \Delta H P_r \rVert_{\mathrm F}^2
      \right)^{1/2}.

:class:`Periodic2DDefectLocalityAnalyzer` additionally retains the global maximum and
Frobenius residuals and one row-resolved Frobenius norm for every represented shell.
A finite-extent pass requires both ``epsilon_ext`` and ``epsilon_cross`` to satisfy
explicit nonnegative tolerances carrying the represented energy unit.  The core radius
and tolerances are declared controls; a passing value is not a proof of continuum
compact support.

A one-site onsite perturbation passes a zero-radius core with zero exterior tolerances.
A nearest-neighbor bond crossing the same core has nonzero cross-coupling norm and
fails.  These controls verify that the assessment responds to represented support
rather than a descriptive label.

Methodological boundary
-----------------------

The current implementation establishes software and bounded represented-numerical
behavior only.  It does not:

* derive a defect perturbation from DFT or Wannier90;
* align pristine and defect bases, gauges, geometries, or energy references;
* establish convergence with supercell area, shape, or boundary twist;
* validate a silicon impurity model or any other material system; or
* perform uncertainty quantification.

Those questions require separately identified parent calculations, alignment evidence,
refinement studies, and independent scientific references.  Historical calculation
records may retain execution labels for provenance, but the public methodology and API
use capability names: representation, compatibility, extraction, and locality.

See :doc:`../api/research-monograph-campaigns` for the complete public API.
