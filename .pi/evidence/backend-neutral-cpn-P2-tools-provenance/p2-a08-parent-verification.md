# P2-A08 parent verification

Status: **PASS — P2-A08 audited_and_cleared; P2-A09 next and not started**

Reopened-correction starting revision:
`90eab67cb06ccceaeacc121b2cc3b40e70506a2d`, with `HEAD == origin/dev` and a
clean working tree after fetching `origin/dev`. P2-A08 alone was reopened for the
human-audited recursive wheel-content correction. P2-A09--P2-A11 retained their
identities and order and were not started.

The corrected module is artifact-owned software verification of the built wheel. One
module-scoped visible ID-free fixture builds the wheel once for two separated owners.
It preserves `SV-PROV-072` for exact archive content and assigns the next unused ID,
`SV-PROV-395`, to genuinely new isolated-import evidence. The historical combined node
maps one-to-one only to the content owner; the new import node has no predecessor.

The fixture preserves the environment and runs the current interpreter with:

```text
python -m pip wheel --no-deps --no-build-isolation --no-index \
  --wheel-dir <isolated-wheel-directory> <repository>/python
```

It sets `PIP_NO_INDEX=1` and `PIP_DISABLE_PIP_VERSION_CHECK=1`, uses a 120-second
timeout, inventories all `*.whl` outputs, requires exactly one, and then requires the
sole filename to identify `ksdft2effmass`. Validation used the selected offline
provisioned route:

```text
cd python && uv run --offline --with pip --with 'setuptools>=77' --with wheel pytest
```

The controlled environment already contained compatible pip, setuptools 83.0.0, and
wheel 0.47.0. The plain project test virtual environment lacks these build tools; this
is a documented setup limitation rather than permission for network access.

The visible ID-free helper `select_provenance_python_entries` uses
`PurePosixPath.is_relative_to` to select every `.py` entry recursively below
`ksdft2effmass/provenance/`. The controlled observation includes the expected direct
`actions.py`, unexpected direct `legacy.py`, nested `legacy/__init__.py`, and nested
`legacy/adapter.py`. Replacing the recursive predicate with the former direct-child
predicate caused `SV-PROV-072` to fail with both nested paths visible in the assertion
difference.

The observed recursive provenance Python inventory equaled exactly:

- `ksdft2effmass/provenance/__init__.py`
- `ksdft2effmass/provenance/actions.py`
- `ksdft2effmass/provenance/external_execution.py`
- `ksdft2effmass/provenance/external_tools.py`
- `ksdft2effmass/provenance/records.py`
- `ksdft2effmass/provenance/serialization.py`
- `ksdft2effmass/provenance/tool_observations.py`

No archive name had an exact `tests` path component. A `python -I -S` subprocess
prepended the exact wheel, imported provenance from the exact wheel plus
`ksdft2effmass/provenance/__init__.py`, and printed the exact sentinel
`ArtifactIdentity`.

The module contains two test functions/evidence owners, one visible ID-free selection
helper, one ID-free fixture, and two collected cases. The complete provenance
integration family contains 145 collected cases.
Structural validation, focused and family pytest, Ruff, mypy, evidence uniqueness,
node migration, P2 ownership/completion, checkpoints, protected nonmutation, and diff
checks pass.

The earlier targeted review remains historical evidence for the initial P2-A08
correction. The subsequent human audit identified the nested-subtree gap and authorized
this bounded correction. One bounded read-only confirmation (`2de2607b`) returned PASS for the exact recursive
predicate, shared controlled/real helper use, preserved exact equality, byte-identical
`SV-PROV-395`, protected boundaries, and inactive P2-A09. No new general review,
replay, or checkpoint loop was launched.

Production provenance source and exports, package metadata, lockfiles, schemas,
fixtures, other integration modules, harness resources, and protected inactive backlog
remain unchanged.

The queue retains `active_item: null`, marks P2-A08 `audited_and_cleared`, and names
P2-A09 as next without starting it. P2 remains open and unaccepted. P3, H5, protected
execution, publication, and release remain inactive.
