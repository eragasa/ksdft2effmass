# Balanced Wannier90 encoded documents

This module owns one immutable exact-byte result container, not a native Wannier90
artifact group, input document, physical model, localization result, optimizer result,
numerical oracle, provenance record, or serializer.

## Classes

- [`Periodic2DWannier90BalancedEncodedDocuments`](Periodic2DWannier90BalancedEncodedDocuments/index.md)
  — exact bytes for the retained balanced-comparison result.

## Boundary

Decoding belongs to explicit serialization owners; native-file authentication,
correlation, independent numerical reconstruction, localization assessment, and
scientific acceptance belong to dedicated owners. No missing input or native artifact
is inferred from paths, filenames, hashes, schema fields, dimensions, labels, or the
balanced campaign name.
