Mathieu1D direct finite reduction
=================================

The direct Mathieu1D surface asks how one selected band of the represented periodic
Hamiltonian

.. math::

   H = -\frac{d^2}{dx^2} + 0.5\cos(x)

behaves under fixed finite parent representations, a complete finite reciprocal-mesh
Fourier transform, and declared symmetric hopping-range truncations.  It owns typed
model-specific configuration and result semantics while consuming the existing
plane-wave, periodic finite-difference, Fourier-transform, truncation, fitting,
interpolation, and diagnostic owners directly.

The calculation result is a finite binary64 record.  Adjacent representations and
sampled gaps are diagnostics, not continuum errors or isolation certificates.  The
independent verifier owns the SHA-256 digest of the exact admitted result bytes,
reconstructs the finite formulas without calling the producer, and authenticates the
closed visualization projection.  Passing checks do not establish scientific
validation, uncertainty quantification, publication acceptance, or evidence sealing.
The implementation, numerical conventions, scientific limits, and data-flow diagrams
are documented in the Architecture v3 source mirror at
``docs/architecture/v3/ksdft2effmass/model_systems/mathieu1d/``.

Configuration
-------------

.. automodule:: ksdft2effmass.model_systems.mathieu1d.configuration
   :members:

Calculation and result sections
-------------------------------

.. automodule:: ksdft2effmass.model_systems.mathieu1d.analysis
   :members:

.. automodule:: ksdft2effmass.model_systems.mathieu1d.result
   :members:

Independent verification
------------------------

.. automodule:: ksdft2effmass.model_systems.mathieu1d.verification_values
   :members:

.. automodule:: ksdft2effmass.model_systems.mathieu1d.verification
   :members:

Authenticated visualization
----------------------------

.. automodule:: ksdft2effmass.model_systems.mathieu1d.visualizations
   :members:
