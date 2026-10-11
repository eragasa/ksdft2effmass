Controlled periodic studies
===========================

The maintained controlled-study API separates physical models, finite
representations, calculations, result records, wire serializers, and independent
verifiers. M1--M3 are deterministic local synthetic studies; they do not execute
Quantum ESPRESSO or Wannier90 and do not establish material validation.

Use the package-level imports documented on the child pages. The ``isolated-band``
name is a historical calculation identity, not by itself evidence of physical band
isolation. Pointwise alignment and one-global-unitary alignment are different feasible
families. M3 dispositions apply only to the frozen two-parameter, nine-angle family.

.. toctree::
   :maxdepth: 1

   ksdft2effmass/periodic1d/model
   ksdft2effmass/periodic1d/isolated_band
   ksdft2effmass/periodic1d/multiband_alignment
   ksdft2effmass/periodic1d/admissible_sets
