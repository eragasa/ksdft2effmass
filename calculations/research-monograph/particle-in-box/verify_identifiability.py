#!/usr/bin/env python3
"""Verify the retained-space Appendix D identifiability demonstration."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import numpy.typing as npt

RealMatrix = npt.NDArray[np.float64]


def _matrix(value: object) -> RealMatrix:
    return np.asarray(value, dtype=np.float64)


def verify(payload: dict[str, Any]) -> None:
    """Raise ``AssertionError`` unless the identifiability result meets its protocol."""
    assert payload["schema_version"] == 1
    assert payload["evidence_status"] == "illustrative numerical experiment"
    assert payload["calculation_status"] == "calculated illustrative result"

    hamiltonian = _matrix(payload["retained_space"]["reduced_hamiltonian"])
    assert hamiltonian.shape == (3, 3)
    assert payload["retained_space"]["dimension"] == 3
    shift = _matrix(payload["illustrative_shift"])
    np.testing.assert_array_equal(shift, shift.T)

    physical = payload["decompositions"]["consistently_reduced_dirichlet"]
    shifted = payload["decompositions"]["illustratively_shifted"]
    physical_kinetic = _matrix(physical["kinetic"])
    physical_potential = _matrix(physical["potential"])
    shifted_kinetic = _matrix(shifted["kinetic"])
    shifted_potential = _matrix(shifted["potential"])
    np.testing.assert_allclose(
        physical_kinetic + physical_potential,
        hamiltonian,
        rtol=0.0,
        atol=2.0e-14,
    )
    np.testing.assert_allclose(
        shifted_kinetic + shifted_potential,
        hamiltonian,
        rtol=0.0,
        atol=2.0e-14,
    )
    np.testing.assert_array_equal(physical_potential, np.zeros((3, 3)))
    np.testing.assert_array_equal(shifted_potential, shift)
    assert not np.array_equal(physical_potential, shifted_potential)

    dimension = shift.shape[0]
    rows, columns = np.indices(shift.shape)
    independent_candidates = {
        "scalar_identity": np.eye(dimension) * np.trace(shift) / dimension,
        "diagonal_in_retained_basis": np.diag(np.diag(shift)),
        "real_symmetric_tridiagonal": np.where(np.abs(rows - columns) <= 1, shift, 0.0),
        "arbitrary_real_symmetric": shift,
    }
    recorded_fits = payload["model_class_fits"]
    norms = []
    for name in payload["input"]["admissible_model_classes"]:
        candidate = independent_candidates[name]
        unexplained = shift - candidate
        record = recorded_fits[name]
        np.testing.assert_array_equal(record["best_fit"], candidate)
        np.testing.assert_array_equal(record["unexplained_residual"], unexplained)
        np.testing.assert_allclose(
            record["unexplained_frobenius_norm"],
            np.linalg.norm(unexplained, ord="fro"),
            rtol=0.0,
            atol=2.0e-15,
        )
        norms.append(record["unexplained_frobenius_norm"])
    assert norms[0] > norms[1] > norms[2] > norms[3]
    assert norms[-1] == 0.0

    assert payload["limitations"] == [
        "The alternative shift is illustrative and has no physical assignment.",
        "Model-class fits depend on the declared retained basis and Frobenius metric.",
        "Algebraic reconstructability does not establish physical identifiability.",
        "The result is not semiconductor evidence or scientific validation.",
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    args = parser.parse_args()
    verify(json.loads(args.result.read_text(encoding="utf-8")))
    print("particle-in-box identifiability demonstration: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
