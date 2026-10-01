"""Independent verification of PIAB1D retained-space identifiability."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from .decoder import ParticleInBoxCampaignResultDecoder


class ParticleInBoxIdentifiabilityVerifier(ParticleInBoxCampaignResultDecoder):
    """Independently verify the retained identifiability campaign."""

    def execute(self, path: Path) -> None:
        """Raise unless one result satisfies decomposition and fit identities."""
        payload = self.decode(path)
        assert self.integer(payload["schema_version"], "schema_version") == 1
        retained = self.mapping(payload["retained_space"], "retained_space")
        hamiltonian = self.matrix(retained["reduced_hamiltonian"], "Hamiltonian")
        assert hamiltonian.shape == (3, 3)
        assert self.integer(retained["dimension"], "dimension") == 3
        shift = self.matrix(payload["illustrative_shift"], "shift")
        np.testing.assert_array_equal(shift, shift.T)
        decompositions = self.mapping(payload["decompositions"], "decompositions")
        physical = self.mapping(
            decompositions["consistently_reduced_dirichlet"], "physical"
        )
        shifted = self.mapping(decompositions["illustratively_shifted"], "shifted")
        physical_kinetic = self.matrix(physical["kinetic"], "physical kinetic")
        physical_potential = self.matrix(physical["potential"], "physical potential")
        shifted_kinetic = self.matrix(shifted["kinetic"], "shifted kinetic")
        shifted_potential = self.matrix(shifted["potential"], "shifted potential")
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
        dimension = shift.shape[0]
        rows, columns = np.indices(shift.shape)
        independent = {
            "scalar_identity": np.eye(dimension) * np.trace(shift) / dimension,
            "diagonal_in_retained_basis": np.diag(np.diag(shift)),
            "real_symmetric_tridiagonal": np.where(
                np.abs(rows - columns) <= 1, shift, 0.0
            ),
            "arbitrary_real_symmetric": shift,
        }
        fits = self.mapping(payload["model_class_fits"], "model_class_fits")
        input_payload = self.mapping(payload["input"], "input")
        classes = self.sequence(
            input_payload["admissible_model_classes"], "admissible_model_classes"
        )
        norms: list[float] = []
        for value in classes:
            if not isinstance(value, str):
                raise TypeError("model class names must be strings")
            candidate = independent[value]
            unexplained = shift - candidate
            record = self.mapping(fits[value], "fit")
            np.testing.assert_array_equal(
                self.matrix(record["best_fit"], "best_fit"), candidate
            )
            np.testing.assert_array_equal(
                self.matrix(record["unexplained_residual"], "unexplained residual"),
                unexplained,
            )
            observed = self.real(
                record["unexplained_frobenius_norm"], "unexplained norm"
            )
            np.testing.assert_allclose(
                observed,
                np.linalg.norm(unexplained, ord="fro"),
                rtol=0.0,
                atol=2.0e-15,
            )
            norms.append(observed)
        assert norms[0] > norms[1] > norms[2] > norms[3]
        assert norms[-1] == 0.0
        assert payload["limitations"] == [
            "The alternative shift is illustrative and has no physical assignment.",
            (
                "Model-class fits depend on the declared retained basis and "
                "Frobenius metric."
            ),
            "Algebraic reconstructability does not establish physical identifiability.",
            "The result is not semiconductor evidence or scientific validation.",
        ]
