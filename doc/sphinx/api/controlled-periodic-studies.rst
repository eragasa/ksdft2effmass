Controlled periodic studies
===========================

The maintained controlled-study API separates physical models, finite
representations, calculations, result records, wire serializers, and independent
verifiers. The direct rank-one Fourier-locality, rank-two composite-alignment, and
constrained-admissible-set controls are deterministic local synthetic studies. The
higher-rank alignment package currently exposes its fixed study parameters,
alignment outcomes, and periodic-frame transport results. None of these APIs
executes Quantum ESPRESSO or Wannier90 or establishes material validation.

Use the package-level imports documented on the child pages. The former M1
``isolated-band`` and M2 ``multiband-alignment`` APIs have been completely replaced
rather than retained as compatibility surfaces. Pointwise alignment and
one-global-unitary alignment are different feasible families. M3 dispositions apply
only to the frozen two-parameter, nine-angle family.

.. toctree::
   :maxdepth: 1

   ksdft2effmass/periodic1d/fourier_locality
   ksdft2effmass/periodic1d/composite_band_alignment
   ksdft2effmass/periodic1d/admissible_sets
   ksdft2effmass/periodic1d/higher_rank_alignment
