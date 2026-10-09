# `solidstate.representedoperators`

## Purpose and status

This canonical architecture page maps the implemented specialized sparse scalar
finite-periodic represented-operator owner. Current source remains
`ksdft2effmass.solid_state.represented_operators`; the architecture path uses the
canonical unseparated `solidstate` segment.

[`ScalarFiniteLatticeOperator`](ScalarFiniteLatticeOperator/index.md) composes a
canonical complex CSR quantity with finite lattice shape/order, twist fiber and gauge,
scalar basis identity, energy reference, and provenance.

Source: `python/src/ksdft2effmass/solid_state/represented_operators.py`.
Tests: `python/tests/software_verification/ksdft2effmass/solid_state/test__ScalarFiniteLatticeOperator.py` and separate compatibility/composition suites.
Sphinx: `doc/sphinx/api/solid-state.rst`.
