Spectral dispersion contrast
============================

Purpose
-------

:class:`~ksdft2effmass.analysis.SpectralDispersionContrast` is a small, transparent
analysis record for comparing relative errors at two caller-identified positions in an
ordered spectrum. It preserves the historical qualitative question “is a declared low
mode accurate while a declared high mode is strongly dispersed?” without making that
question part of numerical verification.

The tool does not calculate eigenvalues, choose modes, infer ordering, or supply hidden
default thresholds. The caller must provide all four dimensionless values explicitly.

Mathematical definition
-----------------------

Let:

``e_low``
   Dimensionless relative error for a caller-identified low mode.

``e_high``
   Dimensionless relative error for a caller-identified high mode.

``tau_low``
   Dimensionless upper reference bound for ``e_low``.

``tau_high``
   Dimensionless lower reference bound for ``e_high``.

The contrast is observed exactly when

.. math::

   e_{\mathrm{low}} \leq \tau_{\mathrm{low}}
   \quad\text{and}\quad
   e_{\mathrm{high}} \geq \tau_{\mathrm{high}}.

The signed diagnostic difference is

.. math::

   \Delta e = e_{\mathrm{high}} - e_{\mathrm{low}}.

All inputs must be finite, nonnegative built-in ``float`` values. The tool requires
:math:`\tau_{\mathrm{high}} > \tau_{\mathrm{low}}` so that the declared regimes do not
overlap. Booleans, integers, strings, NumPy scalar types, and non-finite values are
rejected rather than coerced.

Usage
-----

The former PIAB1D illustrative diagnostic used 2% and 50% as explicit bounds:

.. code-block:: python

   from ksdft2effmass.analysis import SpectralDispersionContrast

   contrast = SpectralDispersionContrast(
       low_mode_relative_error=0.01,
       high_mode_relative_error=0.60,
       low_mode_maximum_relative_error=0.02,
       high_mode_minimum_relative_error=0.50,
   )

   assert contrast.is_observed
   assert contrast.error_difference == 0.59

Those values are an illustrative caller policy, not package defaults. A different study
must choose and document bounds appropriate to its question. The caller must also state
which modes supplied ``e_low`` and ``e_high``; this DataObject intentionally stores no
implicit mode-selection rule.

Algorithm and tolerance ownership
---------------------------------

Construction validates exact runtime types, finiteness, nonnegativity, and ordered
bounds. The three properties then apply direct binary64 subtraction and inclusive
comparisons. There is no optimizer, fit, asymptotic estimator, hidden tolerance, or
statistical model.

The caller owns both bounds and the identities of the compared modes. The class owns
only their deterministic comparison. In particular, ``is_observed`` is not a test of
whether retained eigenpairs were calculated correctly; that belongs to the applicable
independent verifier.

Provenance and evidence
-----------------------

The implementation is
``python/src/ksdft2effmass/analysis/spectral_dispersion.py``. Software-verification
evidence is maintained in
``python/tests/software_verification/ksdft2effmass/analysis/test__SpectralDispersionContrast.py``.
The historical 2%/50% example originated as an explicitly bounded PIAB1D exploratory
diagnostic. This page introduces no external literature value.

Limitations
-----------

An observed contrast:

* does not establish convergence of either mode;
* does not characterize unexamined modes or the complete spectrum;
* is sensitive to caller-selected modes and reference bounds;
* is not an uncertainty estimate or hypothesis test;
* does not validate a physical material model; and
* does not provide scientific acceptance.

For the centered second-difference particle-in-a-box spectrum, the complete dispersion
relation contains substantially more information than this two-point summary. The
contrast is useful for communication and filtering, not as a substitute for the error
curve.

API
---

.. currentmodule:: ksdft2effmass.analysis

.. autoclass:: SpectralDispersionContrast
   :members:
