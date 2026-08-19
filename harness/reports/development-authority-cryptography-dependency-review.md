# Development-authority cryptography dependency review

## Status

**Planning evidence only.** This report records the bounded compatibility and license
review authorized by the resolved
`migration.v2.harness.decisions-authority.signature-mechanism` checkpoint. It does not
add or install a project dependency, accept a lockfile change, authorize credentials,
perform signing, or establish a security audit.

## Inputs

- Retrieval date: 2026-08-18 UTC.
- Python: CPython 3.14.6.
- Resolver: `uv 0.11.25`.
- Temporary requirement: `cryptography==50.0.0` under `requires-python = ">=3.14"`.
- Public metadata: `https://pypi.org/project/cryptography/50.0.0/`.
- Ed25519 API: `https://cryptography.io/en/50.0.0/hazmat/primitives/asymmetric/ed25519/`.
- License entry point: `https://github.com/pyca/cryptography/blob/50.0.0/LICENSE`.
- Transitive metadata: `https://pypi.org/project/cffi/2.1.1/` and
  `https://pypi.org/project/pycparser/3.0/`.

## Resolution command and result

The temporary directory contained only this probe project:

```toml
[project]
name = "cryptography-resolution-probe"
version = "0.0.0"
requires-python = ">=3.14"
dependencies = ["cryptography==50.0.0"]
```

Command:

```text
uv lock --python 3.14
```

Result:

```text
Resolved 4 packages
cryptography==50.0.0
cffi==2.1.1 ; platform_python_implementation != "PyPy"
pycparser==3.0 ; implementation_name != "PyPy"
```

The generated temporary lock had SHA-256
`0b5bcfb041487aa48061cc31907c1b30bda778720e89571a49234b78126d28bd`.
The retained package identities reported by that lock included:

| Package artifact | SHA-256 |
|---|---|
| `cryptography-50.0.0.tar.gz` | `eeac2acb5a20ed25e0ad6d1df9891a520b78b404266b6d11778f25d5d691a6c9` |
| `cffi-2.1.1.tar.gz` | `dd31f52ea1086513bb9df30f8fcee9b8918323ae067a3d5b78bc826a000712be` |
| `pycparser-3.0.tar.gz` | `600f49d217304a5902ac3c37e1281c9fe94e4d0489de643a9504c5cdfdfc6b29` |

The PyPI metadata lists Python 3.14 support and CPython 3.14 wheels for
`cryptography` 50.0.0. The selected Ed25519 API accepts raw 32-byte public keys,
produces 64-byte signatures, and raises `InvalidSignature` for verification failure.

## License observations

- `cryptography` 50.0.0 is offered under either Apache-2.0 or BSD-3-Clause terms.
- CFFI 2.1.1 states MIT No Attribution terms.
- pycparser states BSD-3-Clause terms.

These are verified source observations for human dependency disposition, not legal
advice. The actual project `python/uv.lock` remains the resolved-version authority
only after a separately authorized project dependency mutation and complete lock
review.

## Proposed optional capability dependency

Following the exact human correction recorded in
`migration.v2.harness.decisions-authority.signed-ledger-contract`, use
`cryptography==50.0.0` only in an optional `authority-signatures` dependency group.
The default unsigned path neither imports nor requires it. An explicitly signature-
required Task fails closed when the optional capability is unavailable; it never
installs dynamically or downgrades to unsigned behavior. A later version change
requires its own compatibility, package identity, license, lock, and verification
review. No dependency file was mutated by this planning review.
