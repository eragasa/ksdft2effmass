# Installation

This document describes the maintained development environment for
`ksdft2effmass`.

## Requirements

The Python workflow requires:

- Git;
- [uv](https://docs.astral.sh/uv/);
- a platform supported by the locked Python 3.14 project.

The authoritative Python project files are:

```text
python/pyproject.toml
python/uv.lock
```

Quantum ESPRESSO and Wannier90 are external scientific applications. They are
not installed as Python package dependencies.

## Clone the repository

```bash
git clone https://github.com/eragasa/ksdft2effmass.git
cd ksdft2effmass
```

All commands below run from the repository root unless a command explicitly
changes directory.

## Synchronize the canonical environment

The only maintained repository Python environment is:

```text
python/.venv
```

Do not activate or use a repository-root `.venv`. If another environment is
active, leave it before running uv so `VIRTUAL_ENV` cannot redirect or obscure
the project selection:

```bash
deactivate 2>/dev/null || unset VIRTUAL_ENV
```

Create or synchronize the complete locked development environment:

```bash
cd python
uv sync --locked --all-extras
cd ..
```

This installs the runtime package and the declared `workflow`, `dev`,
`notebooks`, and `docs` extras from `python/uv.lock`. It does not require shell
activation and does not modify dependency constraints or lock resolution.

Verify the interpreter from the repository root:

```bash
python/.venv/bin/python -c "import pathlib, sys; print(pathlib.Path(sys.executable).resolve())"
```

The result must resolve to the interpreter represented by
`python/.venv/bin/python`. If that file is absent or not executable, stop and
run the locked `uv sync` command above; do not fall back to system Python.

The equivalent uv check is:

```bash
cd python
uv run python -c "import pathlib, sys; print(pathlib.Path(sys.executable).resolve())"
cd ..
```

It must report the same resolved interpreter and emit no `VIRTUAL_ENV` mismatch
warning.

## Ordinary development commands

Use the canonical interpreter directly:

```bash
python/.venv/bin/python -c "import ksdft2effmass; print(ksdft2effmass.__file__)"
python/.venv/bin/python -m pytest python/tests
python/.venv/bin/python -m ruff format --check python
python/.venv/bin/python -m ruff check python
python/.venv/bin/python -m mypy --config-file python/pyproject.toml python/src python/tests
PYTHONPATH=python/src python/.venv/bin/python -m sphinx -W -b html docs /tmp/ksdft2effmass-docs
```

Build package artifacts through uv:

```bash
cd python
uv build
cd ..
```

Do not retain generated documentation or package-build output unless an
authorized task explicitly owns it.

## `pip` policy

The uv-managed project environment does not require persistent `pip`. Use
`uv sync` for project dependencies, `uv run` for commands, `uv build` for local
artifacts, and `uv pip` only for an explicitly authorized environment operation.

When a bounded validation specifically requires the `pip` Python module, inject
it for that invocation without adding it to project dependencies:

```bash
cd python
uv run --with pip python -m pip --version
cd ..
```

Do not add `pip` to `python/pyproject.toml` or `python/uv.lock` merely to support
that validation.

## Visual Studio Code

The maintained workspace interpreter is:

```text
${workspaceFolder}/python/.venv/bin/python
```

Repository settings select this path directly. Do not select the root `.venv`,
a system interpreter, or an unrelated activated environment.

## Updating the environment

After pulling changes to `python/pyproject.toml` or `python/uv.lock`, rerun:

```bash
cd python
uv sync --locked --all-extras
cd ..
```

`--locked` fails rather than rewriting the lockfile.

## Optional Rust and external software

Rust, Quantum ESPRESSO, and Wannier90 remain separate toolchains. Their presence
does not change the canonical Python environment. Production scientific
execution requires its own authorization, inputs, resources, and provenance.
