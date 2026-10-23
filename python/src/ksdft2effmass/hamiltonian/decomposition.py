"""Concrete reusable Hamiltonian-decomposition calculation."""

from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import TwoSlopeNorm

from ksdft2effmass.analysis.operators import (
    DecompositionIdentifiabilityAnalyzer,
    DecompositionIdentifiabilityResult,
)
from ksdft2effmass.linalg import RealMatrixQuantity, VerifiedMatrixUtils
from ksdft2effmass.operators import (
    ReducedHamiltonian,
)


@dataclass(frozen=True, slots=True)
class HamiltonianDecompositionVerification:
    """Record the independent verification disposition."""

    passed: bool
    issues: tuple[str, ...]

    def __post_init__(self) -> None:
        if type(self.passed) is not bool:
            raise TypeError("passed must be a built-in bool")
        if not isinstance(self.issues, tuple) or any(
            type(issue) is not str or not issue for issue in self.issues
        ):
            raise TypeError("issues must contain nonempty built-in strings")
        if self.passed == bool(self.issues):
            raise ValueError("passed must be true exactly when issues is empty")


@dataclass(frozen=True, slots=True)
class HamiltonianDecompositionVisualization:
    """Retain one immutable PNG visualization."""

    png: bytes
    media_type: str = "image/png"

    def __post_init__(self) -> None:
        if not isinstance(self.png, bytes):
            raise TypeError("png must be bytes")
        if not self.png.startswith(b"\x89PNG\r\n\x1a\n"):
            raise ValueError("png must contain a PNG image")
        if self.media_type != "image/png":
            raise ValueError("media_type must be image/png")


@dataclass(frozen=True, slots=True)
class HamiltonianDecompositionResult:
    """Correlate calculation, verification, and visualization results."""

    calculation: DecompositionIdentifiabilityResult
    verification: HamiltonianDecompositionVerification
    visualization: HamiltonianDecompositionVisualization

    def __post_init__(self) -> None:
        if type(self.calculation) is not DecompositionIdentifiabilityResult:
            raise TypeError("calculation must be DecompositionIdentifiabilityResult")
        if type(self.verification) is not HamiltonianDecompositionVerification:
            raise TypeError("verification must be HamiltonianDecompositionVerification")
        if type(self.visualization) is not HamiltonianDecompositionVisualization:
            raise TypeError(
                "visualization must be HamiltonianDecompositionVisualization"
            )
        if not self.verification.passed:
            raise ValueError("visualization requires passing verification")


class HamiltonianDecompositionRunner:
    """Calculate decomposition freedom and reduced model-class fits."""

    __slots__ = ("reduced_hamiltonian", "shift", "symmetry_absolute_tolerance")

    def __init__(
        self,
        reduced_hamiltonian: ReducedHamiltonian,
        shift: RealMatrixQuantity,
        symmetry_absolute_tolerance: float,
    ) -> None:
        self.reduced_hamiltonian = reduced_hamiltonian
        self.shift = shift
        self.symmetry_absolute_tolerance = symmetry_absolute_tolerance

    def run(self) -> DecompositionIdentifiabilityResult:
        """Return the generic finite Hamiltonian decomposition calculation."""
        matrix = self._require_compatible_real_symmetric_inputs()
        return DecompositionIdentifiabilityAnalyzer().execute(matrix, self.shift)

    def _require_compatible_real_symmetric_inputs(self) -> RealMatrixQuantity:
        dense_matrix = VerifiedMatrixUtils(
            self.reduced_hamiltonian.matrix
        ).to_dense_matrix()
        if not isinstance(dense_matrix, RealMatrixQuantity):
            raise TypeError("Hamiltonian decomposition requires a real matrix")
        matrix = dense_matrix
        hamiltonian = matrix.magnitude
        shift = self.shift.magnitude
        if shift.shape != hamiltonian.shape:
            raise ValueError("shift must have the reduced Hamiltonian shape")
        if matrix.unit != self.shift.unit:
            raise ValueError("reduced Hamiltonian and shift units must match")
        if not np.allclose(
            hamiltonian,
            hamiltonian.T,
            rtol=0.0,
            atol=self.symmetry_absolute_tolerance,
        ):
            raise ValueError("hamiltonian must be real symmetric")
        if not np.allclose(
            shift,
            shift.T,
            rtol=0.0,
            atol=self.symmetry_absolute_tolerance,
        ):
            raise ValueError("shift must be real symmetric")
        return matrix


class HamiltonianDecompositionVerifier:
    """Independently verify decomposition and model-fit identities."""

    __slots__ = ("absolute_tolerance", "reduced_hamiltonian", "shift")

    def __init__(
        self,
        reduced_hamiltonian: ReducedHamiltonian,
        shift: RealMatrixQuantity,
        absolute_tolerance: float,
    ) -> None:
        self.reduced_hamiltonian = reduced_hamiltonian
        self.shift = shift
        self.absolute_tolerance = absolute_tolerance

    def verify(
        self,
        calculation: DecompositionIdentifiabilityResult,
    ) -> HamiltonianDecompositionVerification:
        """Return all failed independently reconstructed identities."""
        if type(calculation) is not DecompositionIdentifiabilityResult:
            raise TypeError("calculation must be DecompositionIdentifiabilityResult")
        dense_matrix = VerifiedMatrixUtils(
            self.reduced_hamiltonian.matrix
        ).to_dense_matrix()
        if not isinstance(dense_matrix, RealMatrixQuantity):
            raise TypeError("Hamiltonian decomposition requires a real matrix")
        matrix = dense_matrix
        hamiltonian = matrix.magnitude
        shift = self.shift.magnitude
        unit = matrix.unit
        issues: list[str] = []
        matrices = (
            calculation.physical_kinetic,
            calculation.physical_potential,
            calculation.alternative_kinetic,
            calculation.alternative_potential,
        )
        if any(value.unit != unit for value in matrices):
            issues.append("decomposition units differ from the Hamiltonian unit")
        if any(value.magnitude.shape != hamiltonian.shape for value in matrices):
            issues.append("decomposition matrix shapes differ from the Hamiltonian")
        else:
            self._check_close(
                calculation.physical_kinetic.magnitude
                + calculation.physical_potential.magnitude,
                hamiltonian,
                "reference decomposition does not reconstruct the Hamiltonian",
                issues,
            )
            self._check_close(
                calculation.alternative_kinetic.magnitude
                + calculation.alternative_potential.magnitude,
                hamiltonian,
                "alternative decomposition does not reconstruct the Hamiltonian",
                issues,
            )
            self._check_close(
                calculation.physical_kinetic.magnitude,
                hamiltonian,
                "reference kinetic matrix differs from the Hamiltonian",
                issues,
            )
            self._check_close(
                calculation.physical_potential.magnitude,
                np.zeros_like(hamiltonian),
                "reference potential is not zero",
                issues,
            )
            self._check_close(
                calculation.alternative_kinetic.magnitude,
                hamiltonian - shift,
                "alternative kinetic matrix differs from Hamiltonian minus shift",
                issues,
            )
            self._check_close(
                calculation.alternative_potential.magnitude,
                shift,
                "alternative potential differs from the declared shift",
                issues,
            )
        self._verify_model_class_fits(calculation, issues)
        return HamiltonianDecompositionVerification(
            passed=not issues,
            issues=tuple(issues),
        )

    def _verify_model_class_fits(
        self,
        calculation: DecompositionIdentifiabilityResult,
        issues: list[str],
    ) -> None:
        shift = self.shift.magnitude
        dimension = shift.shape[0]
        rows, columns = np.indices(shift.shape)
        expected = (
            (
                "scalar_identity",
                np.eye(dimension) * float(np.trace(shift) / dimension),
            ),
            ("diagonal_in_retained_basis", np.diag(np.diag(shift))),
            (
                "real_symmetric_tridiagonal",
                np.where(np.abs(rows - columns) <= 1, shift, 0.0),
            ),
            ("arbitrary_real_symmetric", shift),
        )
        if len(calculation.model_class_fits) != len(expected):
            issues.append("model-class fit inventory is incomplete")
            return
        for fit, (name, candidate) in zip(
            calculation.model_class_fits,
            expected,
            strict=True,
        ):
            if fit.name != name:
                issues.append(f"unexpected model-class fit {fit.name}")
                continue
            residual = shift - candidate
            self._check_close(
                fit.best_fit.magnitude,
                candidate,
                f"{name} best fit is incorrect",
                issues,
            )
            self._check_close(
                fit.unexplained_residual.magnitude,
                residual,
                f"{name} unexplained residual is incorrect",
                issues,
            )
            expected_norm = float(np.linalg.norm(residual, ord="fro"))
            if (
                fit.unexplained_frobenius_norm.unit != self.shift.unit
                or abs(fit.unexplained_frobenius_norm.magnitude - expected_norm)
                > self.absolute_tolerance
            ):
                issues.append(f"{name} unexplained Frobenius norm is incorrect")

    def _check_close(
        self,
        observed: np.ndarray[tuple[int, int], np.dtype[np.float64]],
        expected: np.ndarray[tuple[int, int], np.dtype[np.float64]],
        issue: str,
        issues: list[str],
    ) -> None:
        if observed.shape != expected.shape or not np.allclose(
            observed,
            expected,
            rtol=0.0,
            atol=self.absolute_tolerance,
        ):
            issues.append(issue)


class HamiltonianDecompositionVisualizer:
    """Render the declared shift and model-class residual norms."""

    __slots__ = ("dpi",)

    def __init__(self, dpi: int) -> None:
        self.dpi = dpi

    def visualize(
        self,
        calculation: DecompositionIdentifiabilityResult,
        verification: HamiltonianDecompositionVerification,
    ) -> HamiltonianDecompositionVisualization:
        """Return an immutable PNG only for a verified calculation."""
        if type(calculation) is not DecompositionIdentifiabilityResult:
            raise TypeError("calculation must be DecompositionIdentifiabilityResult")
        if type(verification) is not HamiltonianDecompositionVerification:
            raise TypeError("verification must be HamiltonianDecompositionVerification")
        if not verification.passed:
            raise ValueError("cannot visualize a failed decomposition verification")
        shift = calculation.alternative_potential.magnitude
        names = tuple(fit.name for fit in calculation.model_class_fits)
        labels = tuple(name.replace("_", "\n") for name in names)
        values = tuple(
            fit.unexplained_frobenius_norm.magnitude
            for fit in calculation.model_class_fits
        )
        figure, axes = plt.subplots(
            1,
            2,
            figsize=(10.8, 4.4),
            constrained_layout=True,
        )
        matrix_axis, fit_axis = axes
        maximum = float(np.max(np.abs(shift)))
        if maximum == 0.0:
            maximum = 1.0
        image = matrix_axis.imshow(
            shift,
            cmap="RdBu_r",
            norm=TwoSlopeNorm(vmin=-maximum, vcenter=0.0, vmax=maximum),
            interpolation="nearest",
        )
        matrix_axis.set(
            title="Illustrative decomposition shift",
            xlabel="coordinate column",
            ylabel="coordinate row",
            xticks=np.arange(shift.shape[1]),
            yticks=np.arange(shift.shape[0]),
        )
        figure.colorbar(image, ax=matrix_axis, shrink=0.82)
        bars = fit_axis.bar(labels, values)
        fit_axis.set(
            title="Unexplained model-class residual",
            xlabel="admissible model class",
            ylabel="Frobenius norm",
        )
        fit_axis.grid(True, axis="y", alpha=0.25)
        offset = 0.025 * max(values, default=0.0)
        for bar, value in zip(bars, values, strict=True):
            fit_axis.text(
                bar.get_x() + bar.get_width() / 2.0,
                value + offset,
                f"{value:.3f}",
                ha="center",
                va="bottom",
            )
        figure.suptitle(
            "Hamiltonian decomposition depends on the declared model class",
            fontsize=13,
            fontweight="bold",
        )
        buffer = BytesIO()
        figure.savefig(buffer, format="png", dpi=self.dpi)
        plt.close(figure)
        return HamiltonianDecompositionVisualization(png=buffer.getvalue())


class HamiltonianDecomposition:
    """Run, independently verify, and visualize one finite decomposition."""

    __slots__ = ("o_runner", "o_verifier", "o_visualizer")

    def __init__(
        self,
        reduced_hamiltonian: ReducedHamiltonian,
        shift: RealMatrixQuantity,
        *,
        absolute_tolerance: float = 2.0e-14,
        visualization_dpi: int = 180,
    ) -> None:
        """Compose the reusable concrete actions for one declared input pair."""
        if not isinstance(reduced_hamiltonian, ReducedHamiltonian):
            raise TypeError("reduced_hamiltonian must be ReducedHamiltonian")
        if not isinstance(shift, RealMatrixQuantity):
            raise TypeError("shift must be RealMatrixQuantity")
        if type(absolute_tolerance) is not float:
            raise TypeError("absolute_tolerance must be a built-in float")
        if not np.isfinite(absolute_tolerance) or absolute_tolerance < 0.0:
            raise ValueError("absolute_tolerance must be finite and nonnegative")
        if type(visualization_dpi) is not int:
            raise TypeError("visualization_dpi must be a built-in int")
        if visualization_dpi <= 0:
            raise ValueError("visualization_dpi must be positive")
        self.o_runner = HamiltonianDecompositionRunner(
            reduced_hamiltonian,
            shift,
            absolute_tolerance,
        )
        self.o_verifier = HamiltonianDecompositionVerifier(
            reduced_hamiltonian,
            shift,
            absolute_tolerance,
        )
        self.o_visualizer = HamiltonianDecompositionVisualizer(visualization_dpi)

    def run(self) -> DecompositionIdentifiabilityResult:
        """Return the decomposition calculation without later stages."""
        return self.o_runner.run()

    def verify(
        self,
        calculation: DecompositionIdentifiabilityResult,
    ) -> HamiltonianDecompositionVerification:
        """Independently verify one calculation from this declared input pair."""
        return self.o_verifier.verify(calculation)

    def visualize(
        self,
        calculation: DecompositionIdentifiabilityResult,
        verification: HamiltonianDecompositionVerification,
    ) -> HamiltonianDecompositionVisualization:
        """Visualize one successfully verified calculation."""
        return self.o_visualizer.visualize(calculation, verification)

    def execute(self) -> HamiltonianDecompositionResult:
        """Run, verify, and visualize in order, failing closed before rendering."""
        calculation = self.run()
        verification = self.verify(calculation)
        if not verification.passed:
            joined = "; ".join(verification.issues)
            raise ValueError(f"Hamiltonian decomposition verification failed: {joined}")
        visualization = self.visualize(calculation, verification)
        return HamiltonianDecompositionResult(
            calculation=calculation,
            verification=verification,
            visualization=visualization,
        )
