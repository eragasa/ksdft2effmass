# Installation

## Implemented Python package

The current Python project root is `python/` and requires Python 3.14 or later. Install only through the repository's declared packaging workflow. Runtime dependencies currently remain NumPy and SciPy; `jsonschema` is a development/test dependency.

SNAKES and MyST are optional extras. Quantum ESPRESSO, Wannier90, Graphviz, MPI, scheduler clients, and container runtimes are not Python wheel dependencies.

## Optional workflow installation

Install the bounded workflow dependency with `pip install ".[workflow]"` from the Python project root, or use the equivalent locked `uv sync --extra workflow` workflow. This installs the separate `SNAKES` distribution in the accepted range `>=0.9.33,<0.10`; it does not bundle SNAKES into the project wheel. SNAKES retains its own license, recorded in [`THIRD_PARTY_NOTICES.md`](https://github.com/eragasa/ksdft2effmass/blob/dev/THIRD_PARTY_NOTICES.md).

The optional dependency does not implement the project-owned CPN contract. P1 is closed as human-accepted `PASS` through `P1-HC03`. P2 is active and its provenance/external-tool implementation remains provisional pending the required correction review, replacement replay, parent verification, and human acceptance. H5 and P3–P11 remain inactive; production and scientific execution remain unauthorized. The executable backend-neutral contract provides project-owned tokens, markings, validation, enablement, and firing. Installing SNAKES does not add the deferred adapter, authoritative persistence, a concrete scientific workflow, or external execution.

## Markdown documentation tooling

Install the documentation environment with `pip install ".[docs]"` or the equivalent locked `uv sync --extra docs` workflow. The docs extra declares MyST Parser `>=5.1,<6` and Sphinx `>=8,<10`.

Sphinx collects every maintained RST source but only Markdown under `docs/user-guide/`. The 14 user-guide pages enter one explicit toctree. Architecture, computational, research, conference, paper, and meeting Markdown remain repository/Obsidian sources and are not implicitly parsed as Sphinx documents. The maintained mixed RST/MyST build passes with warnings treated as errors.

## External executables

Do not install or run external executables solely because they appear in the catalog. A production checkpoint must identify the exact environment, executable versions, pseudopotential, resources, artifact roots, expected runtime, retained outputs, and data-transfer policy before a real QE or Wannier90 operation.
