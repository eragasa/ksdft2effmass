# Wannier90 integration boundary

Reusable native Wannier90 integration belongs to the `projectkoios-simulations`
distribution under `projectkoios.integrations.wannier90`. That owner provides native
artifact records, authentication, bounded parsers, parsed-artifact aggregation, and
calculator-facing preprocessing or execution contracts available in the selected
revision. KSD neither duplicates nor re-exports those contracts.

KSD consumes the integration-owned immutable values in project-specific campaign
composition. The Appendix G native-artifact Workflow obtains its exact expected
inventory from the retained result document, requires caller-supplied bytes, delegates
authentication and parsing to Project Koios Simulations, and then applies KSD-owned
correlation and independent Wilson-loop verification.

The KSD composition does not:

- execute Wannier90;
- implement localization, disentanglement, or spread optimization;
- discover native files, run roots, or authoritative manifests;
- construct eigenvalues, projections, or overlap matrices;
- silently select an `_hr.dat` interpolation or degeneracy convention; or
- treat byte authentication as numerical or scientific validation.

Exact dependency revision and resolved transitive dependencies are recorded in
`python/pyproject.toml` and `python/uv.lock`.
