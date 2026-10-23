# Bounded 2-D M1/M2 response development

This directory contains replaceable smoke records for the prospectively fixed M1 frozen
four-state bipartite parent and M2 radial-response control. Both use a `16 x 16`
construction mesh, separately shifted `33 x 33` evaluation mesh, nine strain fractions,
maximum imposed gauge angle `pi/4`, and complete physical-radius supports.

At the square-metric endpoint, M1's pointwise gauge-aligned strain perturbation remains
at `1.4e-15 E_ref`. Under M2 with fixed `beta=1`, bond responses span approximately
`0.81758` to `1.27146`, while the maximum aligned perturbation is approximately
`0.063575 E_ref` and is overwhelmingly traceless in this synthetic retained
representation. At tail tolerance `1e-5`, the endpoint perturbation interpolation,
deliberate-truncation, and total maximum matrix errors are approximately `6.0e-8`,
`7.801e-4`, and `7.802e-4`, respectively.

The M1 and M2 result documents are canonically encoded and validated against distinct
strict packaged v1 schemas. These values remain single-smoke development diagnostics:
they are not converged, independently reconstructed, retained, material, elastic, or
graphene results. Schema conformance establishes only the artifact shape.
