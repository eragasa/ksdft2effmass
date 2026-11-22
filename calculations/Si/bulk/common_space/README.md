# Bulk-silicon common-space calculations

This directory is the calculation-owned incubation root for bulk-silicon state-space
identification, overlap diagnostics, and future independently verified common-space
studies. It does not define a second reusable Python library and is not part of the
supported `ksdft2effmass` import surface.

## Ownership

The bulk-silicon calculation owns the exact source identities, basis order, geometry,
energy reference, native precision policy, stop conditions, retained-result comparison,
and scientific disposition. Project Koios Simulations owns parsing of native Wannier90
artifacts. Reusable mathematical behavior may move to `python/src/ksdft2effmass/` only
through a separately reviewed migration; this incubation package must not become a
competing permanent source tree.

## Current package

- [`diagnostics/`](diagnostics/) contains the CSD0/CSD1 producer used to authenticate
  the adopted C6-B20-W21 source meaning and reconstruct the blocked S110 rank gate.
  Its [retained checkpoint](../analysis/common-space-producer/) includes the complete
  216-point field and an exhaustive geometric construction-index inventory.

- [`verification/`](verification/) contains declared native-byte correlation through
  shared provider parsers, independently reconstructed exact overlaps, rational
  Gram-rank enclosures, conditional native/parse error propagation, direction and
  unitary controls, complete-grid composition, separate numerical artifacts, and later
  producer comparison. Reviewed source assertions and producer prerequisites must be
  supplied externally; matching declarations alone do not substantiate them. Only
  synthetic tests and the separately authorized [retained CSD1-V run](../analysis/common-space-verification/)
  have exercised its verification/correlation. An authenticated adapter consumes
  the producer's original reconstruction result after independent computation. It does
  not manufacture completed point-inventory evidence or source review. Higher arithmetic
  precision is a conditional follow-up to unresolved arithmetic or route disagreement,
  not a routine prerequisite when existing bounds and agreement are decisive.

The source review/adoption and actual producer/inventory/completion evidence are now
retained. The complete verifier bundle and independent numerical reconstruction now
pass all-point producer correlation under the declared contract. The geometric index
inventory still does not supply electronic symmetry actions; CSD2 remains unrun.
No symmetry attribution, scientific disposition, fit, or calculator execution is supplied
by these numerical software checks.
