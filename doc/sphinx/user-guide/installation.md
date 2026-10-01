# Installation

## Canonical Python environment

The current Python project root is `python/` and requires Python 3.14 or later.
The authoritative dependency inputs are `python/pyproject.toml` and
`python/uv.lock`. The only maintained repository environment is
`python/.venv`; do not use a root `.venv`, system Python, shell activation, or an
unrelated `VIRTUAL_ENV`.

From the repository root, synchronize the complete locked environment:

```bash
deactivate 2>/dev/null || unset VIRTUAL_ENV
cd python
uv sync --locked --all-extras
cd ..
```

Use `python/.venv/bin/python` for ordinary Python execution. If it is missing,
stop and synchronize with uv rather than falling back to another interpreter.

Runtime dependencies remain NumPy and SciPy. `jsonschema`, mypy, pytest, Ruff,
and coverage are development dependencies. SNAKES, notebook tooling, and the
Sphinx/MyST documentation toolchain are declared extras included by
`--all-extras`.

## Optional focused synchronization

When a complete development environment is not required, synchronize an
explicit locked extra from the Python project root:

```bash
cd python
uv sync --locked --extra workflow
# or: uv sync --locked --extra docs
cd ..
```

The workflow extra installs the separate SNAKES distribution in the accepted
range. Installing it does not implement the project-owned CPN contract or
activate scientific execution. The docs extra installs MyST Parser and Sphinx.

## Running and building

Examples from the repository root are:

```bash
python/.venv/bin/python -c "import ksdft2effmass; print(ksdft2effmass.__file__)"
python/.venv/bin/python -m pytest python/tests
cd python
uv build
cd ..
```

A uv-managed environment does not need persistent `pip`. Use `uv sync`,
`uv run`, `uv build`, or a bounded `uv pip` operation. If one validation
explicitly requires the `pip` module, inject it only for that command with
`uv run --with pip python -m pip ...`; do not add `pip` to project dependencies.

## External executables

Quantum ESPRESSO, Wannier90, Graphviz, MPI, scheduler clients, and container
runtimes are not Python wheel dependencies. Do not install or run them solely
because they appear in the catalog. Production execution requires separate
human authorization and retained settings, resource, artifact, and data-transfer
provenance.
