# `ksdft2effmass.periodic2d.run.wannier90.balanced`

## Purpose and migration status

This package owns the retained balanced periodic-2D Wannier90 campaign record, its exact
encoded result, and an independent verification surface. Those responsibilities remain
separate from native execution and scientific acceptance.

Crosswalk row 050 reconciles the encoded result container. The historical contract
contains no separately retained encoded input field, and this migration does not invent
one. Row 071 completes the bounded campaign operation: a fresh verifier reconstructs
from authenticated portable evidence confined to the supplied repository root. The
former campaign-native external-run-tree branch is removed; native formats and artifact
parsing remain integration-owned.

## Child map

- [Encoded documents](encoded_documents/index.md)
  - [`Periodic2DWannier90BalancedEncodedDocuments`](encoded_documents/Periodic2DWannier90BalancedEncodedDocuments/index.md)

## Supported imports and evidence

The reviewed facade exposes only `Periodic2DWannier90BalancedCampaign` and
`Periodic2DWannier90BalancedEncodedDocuments`; verifier contracts remain in `verify`.
The exact campaign node is
`python/tests/ksdft2effmass/periodic2d/run/wannier90/balanced/test__Periodic2DWannier90BalancedCampaign.py`,
with retained-artifact nodes in the mirrored software-verification manifest. Sphinx maps
the defining family in
`doc/sphinx/api/ksdft2effmass/periodic2d/run/wannier90-balanced.rst`.

## Claim boundary

Passing establishes portable reconstruction only. The word “balanced” is a retained
campaign identity; it is not evidence of localization convergence, optimizer
correctness, model adequacy, native-file presence, historical execution, scientific
validation, UQ, or acceptance. No native artifact is accessed and Wannier90 is not
rerun.
