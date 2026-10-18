# Bounded 3-D M1/M2 response development

This directory contains replaceable smoke records for the prospectively fixed M1 frozen
four-state bipartite parent and M2 radial-response control. Both use an `8 x 8 x 8`
construction mesh, separately shifted `17 x 17 x 17` evaluation mesh, nine strain
fractions, maximum imposed gauge angle `pi/4`, and complete physical-radius supports.

At the BCC Bain endpoint, M1's pointwise gauge-aligned strain perturbation remains at
`1.4e-15 E_ref`. Under M2 with fixed `beta=1`, the four selected parent bonds share an
endpoint response of approximately `0.97564`; the maximum aligned perturbation is
approximately `0.007289 E_ref` and is overwhelmingly traceless in this synthetic
retained representation. At tail tolerance `1e-5`, the endpoint perturbation
interpolation, deliberate-truncation, and total maximum matrix errors are approximately
`9.36e-5`, `1.61e-4`, and `1.89e-4`, respectively.

The M1 and M2 result documents are canonically encoded and validated against distinct
strict packaged v1 schemas. These values remain single-smoke development diagnostics:
they are not converged, independently reconstructed, retained, phase-stability,
material, or silicon results. Schema conformance establishes only the artifact shape.
