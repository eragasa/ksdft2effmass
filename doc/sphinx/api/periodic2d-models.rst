Periodic-2D models and representations
======================================

The periodic-2D owner contains scientific models, exact model roles, finite
plane-wave and finite-difference representation construction, reciprocal meshes, and
finite-cutoff sewing mechanics. A model's controlled/reference/reduced role is data in
``PeriodicModelRole`` rather than a package namespace or class-name category.

The reusable plane-wave owner uses PhysKit direct and reciprocal lattices, an explicit
finite Fourier inventory, reduced primitive-basis momentum coordinates, and a
caller-toleranced two-pi duality check. The reciprocal-mesh surface adds centered
half-open sampling, explicit positive-neighbor translations, and truncating finite-basis
sewing maps.

.. toctree::
   :hidden:

   ksdft2effmass/periodic/periodic2d/models/plane_waves
   ksdft2effmass/periodic/periodic2d/models/reciprocal_mesh
