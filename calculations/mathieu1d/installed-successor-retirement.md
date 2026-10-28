# Installed Mathieu1D predecessor retirement

## Scope

The direct typed Mathieu1D lifecycle replaced the installed `study/` predecessor after
calculation parity, exact-byte verification, authenticated rendering, caller inventory,
and explicit operator authorization. This retirement changes installed Python source
only. The four version-one runs were outside this source-retirement scope and were later
removed under the separate authorization recorded in
[`legacy-run-retirement.md`](legacy-run-retirement.md).

The supported imports now come from
`ksdft2effmass.model_systems.mathieu1d` and identify the direct configuration, analyzer,
result sections, byte-owning verifier, verification values, visualization projection,
closed plot enumeration, and visualizer. No compatibility facade or live historical
wire decoder remains.

## Recovery authority

- recovery revision: `2ea109d5165366bc507d8900cf85a67de1a2bf73`;
- Mathieu1D package tree at that revision:
  `452f2187f45e2c8f97e408993aa992b700f5e0ab`;
- retired `study/` tree:
  `7e9c91b7b95255b3f7c647c57b7b37562dc0d59e`;
- SHA-256 of the newline-delimited, bytewise-sorted six-path retirement inventory:
  `0a5b20746e041cbfd2ee520892c9c07fbc40ab06e508a87f6f3cf0e6263b575f`.

The two modified export modules remain recoverable from the same revision:

| Path | Predecessor Git blob | Predecessor SHA-256 |
|---|---|---|
| `python/src/ksdft2effmass/model_systems/__init__.py` | `494936932531c8754b9b9290beef09638b3af0c5` | `0a941d9c2d0b10e12f93cc629d55e6361db1372c6526440f4511872af36b85c5` |
| `python/src/ksdft2effmass/model_systems/mathieu1d/__init__.py` | `45ee95490d464b320b58799635beb34e0f6036f7` | `3238b7e7db9cacf862da7e5f382707d8bfa8c7deb4af5b04e80a32262a84297c` |

The retired inventory is:

| Path | Git blob | SHA-256 |
|---|---|---|
| `python/src/ksdft2effmass/model_systems/mathieu1d/study/__init__.py` | `ce3558c9864004d2b900638bc7670bd52b3c1e0b` | `edf0842e385087a95e02b4c274dce21aba3f0348d605a98fe5d8ca6eacf34352` |
| `python/src/ksdft2effmass/model_systems/mathieu1d/study/evaluation.py` | `61dcf7d43825d7ee2559e373b03558e2d2622dc0` | `d239169e55128f6e3078caa5d45f43bc84dd8044f3f2193e1e1cdddbaaaf41a5` |
| `python/src/ksdft2effmass/model_systems/mathieu1d/study/input.py` | `4a1e3961a5abd2e5ea788eabd97703954a179a85` | `1a35188526b283cbf05aa75b906db3debf81a0cfd30028b1a7815c3a9e9e3b50` |
| `python/src/ksdft2effmass/model_systems/mathieu1d/study/records.py` | `cd73f84fae9c370de24a20f8cc20c0053f45e7ef` | `3e6b5b1c1da00eb985f59593468f54becdd196e78203e8e5259941771e29dd3f` |
| `python/src/ksdft2effmass/model_systems/mathieu1d/study/serialization.py` | `64f8e495d33996f5896f2898815c7d129ca748ef` | `5c9dc62746966413ac080ef5f85594d80194a86b3b03ee1eaed6d809e7b15a85` |
| `python/src/ksdft2effmass/model_systems/mathieu1d/study/verification.py` | `0f3d69727930bad982b5f7d2bd9366f3cc10af98` | `d2fc6e67e921997b49f0da3c485358cb8ef929502f5bc378c83e6573eb5f1544` |

Each predecessor can be recovered without restoring the retired package, for example:

```console
git show 2ea109d5165366bc507d8900cf85a67de1a2bf73:python/src/ksdft2effmass/model_systems/mathieu1d/study/records.py
```

Recovery establishes byte availability only. It does not reactivate the predecessor as
a supported API or compatibility contract.
