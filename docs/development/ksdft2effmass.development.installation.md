# Installation

This document describes how to install the development version of
`ksdft2effmass` from source.

## Requirements

### Python

The Python implementation requires:

- Git;
- a supported Python version, as declared in `python/pyproject.toml`;
- `pip`;
- a platform capable of creating Python virtual environments.

### Rust

The optional Rust implementation requires:

- the Rust toolchain;
- Cargo.

Quantum ESPRESSO and Wannier90 are external scientific applications. They are
not installed as Python package dependencies.

## Clone the repository

```bash
git clone https://github.com/eragasa/ksdft2effmass.git
cd ksdft2effmass
```

All commands below are executed from the repository root unless stated
otherwise.

## Create the Python environment

Create a virtual environment at the repository root:

### Linux/macOS

```bash
python3 -m venv --prompt ksdft2effmass .venv
source .venv/bin/activate
```

After activation the prompt should show `(ksdft2effmass)`
Confirm that the virtual environment is active:

```bash
python --version
python -m pip --version
```

The displayed Python and `pip` paths should refer to `.venv`.

### PowerShell

```powershell
python3 -m venv .venv
.venv\Scripts\Activate.ps1
```

Confirm that the virtual environment is active:

```bash
python --version
python -m pip --version
```

The displayed Python and `pip` paths should refer to `.venv`.

## Install the Python implementation

Upgrade the packaging tools:

```bash
python -m pip install --upgrade pip
```

Install the Python package in editable mode:

```bash
python -m pip install -e ./python
```

Editable installation makes the package importable while allowing changes under

```text
python/src/ksdft2effmass/
```

to take effect without reinstalling the package.

For development, install the optional development dependencies:

```bash
python -m pip install -e "./python[dev]"
```

The `dev` dependency group must be defined in `python/pyproject.toml`.

## Verify the Python installation

Run:

```bash
python -c "import ksdft2effmass; print(ksdft2effmass.__file__)"
```

The reported path should resolve to the source tree under:

```text
python/src/ksdft2effmass/
```

Run the Python test suite:

```bash
python -m pytest python/tests
```

A successful import confirms that the package is installed. Passing tests
provide the stronger verification that the installed environment satisfies the
current software requirements.

## Configure Visual Studio Code

Select the repository virtual environment as the Python interpreter:

```text
ksdft2effmass/.venv/bin/python
```

On Windows, select:

```text
ksdft2effmass\.venv\Scripts\python.exe
```

The repository-local virtual environment should not be committed to Git.

## Install the Rust implementation

Rust is optional unless the selected workflow depends on a Rust executable,
library, or Python extension.

Confirm that the Rust toolchain is available:

```bash
rustc --version
cargo --version
```

Build the Rust workspace:

```bash
cargo build --manifest-path rust/Cargo.toml
```

Run its tests:

```bash
cargo test --manifest-path rust/Cargo.toml
```

For an optimized build, run:

```bash
cargo build --release --manifest-path rust/Cargo.toml
```

Compiled artifacts are written under `rust/target/` and should not be committed
to Git.

## External electronic-structure software

The computational workflows may require Quantum ESPRESSO and Wannier90.
Installation procedures depend on the workstation or computing facility and
are therefore maintained separately from the Python package installation.

Verify that the required executables are available:

```bash
pw.x --version
wannier90.x --version
```

On systems using environment modules, the corresponding software modules may
need to be loaded first:

```bash
module load quantum-espresso
module load wannier90
```

Module names vary between computing facilities. Record the software versions,
compiler toolchains, mathematical libraries, and module names used for every
production calculation.

## Update the development installation

Retrieve the latest development changes:

```bash
git switch dev
git pull
```

Update the installed dependencies if `python/pyproject.toml` has changed:

```bash
python -m pip install -e "./python[dev]"
```

Rebuild the Rust implementation if `rust/Cargo.toml`, `rust/Cargo.lock`, or the
Rust source has changed:

```bash
cargo build --manifest-path rust/Cargo.toml
```

## Deactivate the environment

When finished, deactivate the Python virtual environment:

```bash
deactivate
```

The environment can be reactivated later with:

```bash
source .venv/bin/activate
```