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

- [`diagnostics/`](diagnostics/) contains the unretained CSD0/CSD1 producer used to
  authenticate the frozen C6-B20-W21 inputs and reconstruct the blocked S110 rank gate.

No independent CSD1 verifier, higher-precision sensitivity extension,
symmetry-related deficient-point inventory, CSD2 symmetry attribution, CSD3 human
disposition, fit, or calculator execution is implemented or authorized here.
