Backend-neutral DFT simulations
===============================

``ksdft2effmass.simulations.dft`` owns backend-neutral pseudopotential source
entries, independently identified native artifacts, deterministic
content-addressed external paths, schema-v1 SQLite catalog operations, and
current local-byte verification.

A source-entry identity records common library provenance; it does not assert
that PSP8, UPF2, or another representation has identical bytes, parser behavior,
or finite numerical operators. Library cutoff hints are represented in Hartree
and remain starting guidance rather than convergence results.

Catalog initialization creates only missing directories and schema objects.
Recording performs no acquisition or copying: it requires an artifact already at
its canonical path and verifies size and complete SHA-256 before insertion.
Resolution reconstructs metadata without asserting current-byte integrity; use
``PseudopotentialArtifactVerifier`` before staging a scientific run.

The explicit layout, accepted PseudoDojo branches, and scientific limitations are
specified by ``specification/dft-pseudopotential-library/v1/index.md``. No API on
this page downloads, converts, selects, or executes a pseudopotential.

Source entries, artifacts, layout, catalog, and verification
------------------------------------------------------------

.. automodule:: ksdft2effmass.simulations.dft
   :members:
   :imported-members:
