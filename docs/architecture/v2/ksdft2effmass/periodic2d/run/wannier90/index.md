# `ksdft2effmass.periodic2d.run.wannier90`

## Purpose and migration status

This package owns retained periodic-2D Wannier90 campaign families and their exact
encoded documents. Encoded-wire ownership remains distinct from native-file ownership,
execution provenance, localization diagnostics, numerical verification, and scientific
acceptance.

Crosswalk row 050 reconciles the single encoded result for the balanced campaign. Rows
051–055 separately cover the study and optimizer-family documents. No row may infer
native artifact presence, successful Wannier90 execution, localization convergence, or
optimizer validity from compact encoded results.

## Child map

- [Balanced campaign](balanced/index.md)
  - [Encoded documents](balanced/encoded_documents/index.md)
  - [`Periodic2DWannier90BalancedEncodedDocuments`](balanced/encoded_documents/Periodic2DWannier90BalancedEncodedDocuments/index.md)
- [Bounded sensitivity study](study/index.md)
  - [Encoded documents](study/encoded_documents/index.md)
  - [`Periodic2DWannier90StudyEncodedDocuments`](study/encoded_documents/Periodic2DWannier90StudyEncodedDocuments/index.md)
- [Optimizer-basin campaign family](optimizer_basin/index.md)
  - [Base encoded documents](optimizer_basin/encoded_documents/index.md)
  - [`Periodic2DOptimizerBasinEncodedDocuments`](optimizer_basin/encoded_documents/Periodic2DOptimizerBasinEncodedDocuments/index.md)

## Claim boundary

Encoded content and digest identity establish bounded wire identity only. They do not
establish that a native `.win`, `.wout`, `.chk`, `_hr.dat`, or other Wannier90 file is
available; authenticate execution provenance; prove localization convergence; validate
an optimizer; quantify uncertainty; or record scientific acceptance.
