# Aggregated artifact workflow

This calculation-owned package contains the shared artifact boundary for the four dimensional band-equivalence/locality families, the two synthetic-strain calculations, and their cross-family decision-landscape aggregation.

It owns:

- immutable JSON Schema documents;
- canonical JSON encoding and SHA-256 bindings;
- typed result, verification, refinement, strain, scan, and decision-landscape artifact composition; and
- environment and read-back verification records.

Reusable scientific calculators, diagnostics, and plot renderers remain under `ksdft2effmass.analysis`. This package is not included in the installed `ksdft2effmass` library API. Calculation entrypoints add this aggregation root explicitly before importing it.

Schema validation and read-back agreement qualify artifact mechanics only. They do not establish convergence, retained-evidence status, material applicability, or scientific acceptance.
