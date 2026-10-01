"""Reconstruct the retained-space identities in the PIAB1D identifiability study."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path

import numpy as np

from .decoder import Piab1dResultDecoder
from .records import (
    Piab1dNumericalVerificationResult,
    Piab1dVerificationCheck,
    Piab1dVerificationCount,
    Piab1dVerificationResult,
)
from .source import (
    Piab1dSourceAuthenticator,
    Piab1dSourceIdentity,
    Piab1dSourceIdentityRole,
)


class Piab1dIdentifiabilityVerificationChannel(StrEnum):
    """Identify the retained-space identities reconstructed by the verifier."""

    RETAINED_SPACE = "retained_space"
    SHIFT_SYMMETRY = "shift_symmetry"
    DECOMPOSITION_SUMS = "decomposition_sums"
    POTENTIAL_ASSIGNMENTS = "potential_assignments"
    MODEL_CLASS_BEST_FITS = "model_class_best_fits"
    MODEL_CLASS_RESIDUALS = "model_class_residuals"
    MODEL_CLASS_RESIDUAL_NORMS = "model_class_residual_norms"


class Piab1dIdentifiabilityResultsVerifier(Piab1dResultDecoder):
    """Check algebraic decompositions and least-residual model-class fits.

    The verifier checks only the finite retained-space arithmetic. It does not rank the
    model classes or interpret a smaller residual as physical identifiability.
    """

    __slots__ = ()

    historical_runner_sha256 = (
        "f1080fe6d1de047302cb15483c1cddfea653fba0f4e32c85db7e751c063a017c"
    )
    expected_implementation_paths = (
        "python/src/ksdft2effmass/campaigns/piab1d/identifiability.py",
    )

    def execute(self, path: Path, repository_root: Path) -> Piab1dVerificationResult:
        """Return source and numerical reports for one identifiability result."""
        payload = self.decode(path)
        if self.integer(payload["schema_version"], "schema_version") != 1:
            raise ValueError("identifiability schema_version must equal one")
        input_payload = self.mapping(payload["input"], "input")
        if self.integer(input_payload["schema_version"], "input.schema_version") != 1:
            raise ValueError("identifiability input schema_version must equal one")
        if input_payload["experiment_id"] != payload["experiment_id"]:
            raise ValueError("input and result experiment_id values must agree")
        if input_payload["evidence_status"] != payload["evidence_status"]:
            raise ValueError("input and result evidence_status values must agree")
        expected_limitations = [
            "The alternative shift is illustrative and has no physical assignment.",
            (
                "Model-class fits depend on the declared retained basis and "
                "Frobenius metric."
            ),
            "Algebraic reconstructability does not establish physical identifiability.",
            "The result is not semiconductor evidence or scientific validation.",
        ]
        if payload["limitations"] != expected_limitations:
            raise ValueError("identifiability limitations must match version one")

        provenance = self.mapping(payload["provenance"], "provenance")
        retained_identity = Piab1dSourceIdentity(
            Piab1dSourceIdentityRole.RETAINED_RESULT,
            self.string(provenance["retained_result_path"], "retained_result_path"),
            self.sha256_string(
                provenance["retained_result_sha256"], "retained_result_sha256"
            ),
        )
        source = Piab1dSourceAuthenticator().execute(
            provenance,
            repository_root,
            self.expected_implementation_paths,
            self.historical_runner_sha256,
            (retained_identity,),
        )

        retained = self.mapping(payload["retained_space"], "retained_space")
        dimension = self.integer(retained["dimension"], "dimension")
        if dimension <= 0:
            raise ValueError("retained dimension must be positive")
        hamiltonian = self.matrix(retained["reduced_hamiltonian"], "Hamiltonian")
        shift = self.matrix(payload["illustrative_shift"], "shift")
        expected_shape = (dimension, dimension)
        if hamiltonian.shape != expected_shape or shift.shape != expected_shape:
            raise ValueError("retained matrices must match the declared dimension")

        # A real Hamiltonian represented on one retained basis must be symmetric.
        # Record its largest antisymmetric matrix entry; the shape was checked above.
        retained_defect = np.max(
            np.abs(hamiltonian - hamiltonian.T), initial=0.0
        ).item()
        shift_symmetry_defect = np.max(np.abs(shift - shift.T), initial=0.0).item()
        decompositions = self.mapping(payload["decompositions"], "decompositions")
        physical = self.mapping(
            decompositions["consistently_reduced_dirichlet"], "physical"
        )
        shifted = self.mapping(decompositions["illustratively_shifted"], "shifted")
        physical_kinetic = self.matrix(physical["kinetic"], "physical.kinetic")
        physical_potential = self.matrix(physical["potential"], "physical.potential")
        shifted_kinetic = self.matrix(shifted["kinetic"], "shifted.kinetic")
        shifted_potential = self.matrix(shifted["potential"], "shifted.potential")
        for name, matrix in (
            ("physical.kinetic", physical_kinetic),
            ("physical.potential", physical_potential),
            ("shifted.kinetic", shifted_kinetic),
            ("shifted.potential", shifted_potential),
        ):
            if matrix.shape != expected_shape:
                raise ValueError(f"{name} must match the retained-space shape")

        # Both kinetic-plus-potential decompositions must reconstruct the same H_r.
        decomposition_defect = max(
            np.max(
                np.abs(physical_kinetic + physical_potential - hamiltonian),
                initial=0.0,
            ).item(),
            np.max(
                np.abs(shifted_kinetic + shifted_potential - hamiltonian),
                initial=0.0,
            ).item(),
        )
        potential_defect = max(
            np.max(np.abs(physical_potential), initial=0.0).item(),
            np.max(np.abs(shifted_potential - shift), initial=0.0).item(),
        )

        # These are orthogonal Frobenius projections onto the four declared linear
        # matrix classes. Their differences from S are the unexplained residuals.
        rows, columns = np.indices(expected_shape)
        independent = {
            "scalar_identity": np.eye(dimension) * np.trace(shift) / dimension,
            "diagonal_in_retained_basis": np.diag(np.diag(shift)),
            "real_symmetric_tridiagonal": np.where(
                np.abs(rows - columns) <= 1, shift, 0.0
            ),
            "arbitrary_real_symmetric": shift,
        }
        classes = tuple(
            self.string(value, "model class")
            for value in self.sequence(
                input_payload["admissible_model_classes"], "admissible_model_classes"
            )
        )
        if classes != tuple(independent):
            raise ValueError(
                "admissible_model_classes must match the version-one inventory"
            )
        fits = self.mapping(payload["model_class_fits"], "model_class_fits")
        if set(fits) != set(classes):
            raise ValueError("model_class_fits must match the input inventory")
        best_fit_defects: list[float] = []
        residual_defects: list[float] = []
        norm_defects: list[float] = []
        for model_class in classes:
            candidate = independent[model_class]
            unexplained = shift - candidate
            record = self.mapping(fits[model_class], "fit")
            best_fit = self.matrix(record["best_fit"], "best_fit")
            residual = self.matrix(
                record["unexplained_residual"], "unexplained_residual"
            )
            if best_fit.shape != expected_shape or residual.shape != expected_shape:
                raise ValueError("fit matrices must match the retained-space shape")
            best_fit_defects.append(
                np.max(np.abs(best_fit - candidate), initial=0.0).item()
            )
            residual_defects.append(
                np.max(np.abs(residual - unexplained), initial=0.0).item()
            )
            observed_norm = self.nonnegative_real(
                record["unexplained_frobenius_norm"],
                "unexplained_frobenius_norm",
            )
            expected_norm = np.linalg.norm(unexplained, ord="fro").item()
            norm_defects.append(abs(observed_norm - expected_norm))

        check = Piab1dVerificationCheck
        checks = (
            check(
                Piab1dIdentifiabilityVerificationChannel.RETAINED_SPACE,
                retained_defect,
                5.0e-15,
            ),
            check(
                Piab1dIdentifiabilityVerificationChannel.SHIFT_SYMMETRY,
                shift_symmetry_defect,
                0.0,
            ),
            check(
                Piab1dIdentifiabilityVerificationChannel.DECOMPOSITION_SUMS,
                decomposition_defect,
                2.0e-14,
            ),
            check(
                Piab1dIdentifiabilityVerificationChannel.POTENTIAL_ASSIGNMENTS,
                potential_defect,
                0.0,
            ),
            check(
                Piab1dIdentifiabilityVerificationChannel.MODEL_CLASS_BEST_FITS,
                max(best_fit_defects),
                0.0,
            ),
            check(
                Piab1dIdentifiabilityVerificationChannel.MODEL_CLASS_RESIDUALS,
                max(residual_defects),
                0.0,
            ),
            check(
                Piab1dIdentifiabilityVerificationChannel.MODEL_CLASS_RESIDUAL_NORMS,
                max(norm_defects),
                2.0e-15,
            ),
        )
        numerical = Piab1dNumericalVerificationResult(
            checks,
            tuple(Piab1dIdentifiabilityVerificationChannel),
            (Piab1dVerificationCount("model_classes", len(classes)),),
        )
        return Piab1dVerificationResult(source, numerical)
