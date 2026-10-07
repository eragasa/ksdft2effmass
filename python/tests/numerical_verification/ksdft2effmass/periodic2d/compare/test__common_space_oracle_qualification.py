"""Independent qualification evidence for row-036 candidate analytic oracles.

The tests terminate at finite root-of-unity sums, direct action of the declared centered
stencil, and explicit exponential expansions of the cosine parent. They intentionally
do not import production constructors or the common-space comparator. All arrays are
synthetic complex128/binary64 values on the fixed period-``2*pi`` domains documented by
the three oracle dossiers.

Passing this module is one candidate-gate prerequisite. It does not create a technical
``QUALIFIED`` disposition, accept the consumer tests as numerical evidence, establish
convergence, validate a physical model, quantify uncertainty, or record human
acceptance.
"""

import numpy as np
import numpy.typing as npt
import pytest

pytestmark = [pytest.mark.unit, pytest.mark.numerical_verification]


class TestPeriodic2DCommonSpaceOracleQualification:
    """Qualify three candidate relations without invoking their production consumer."""

    @staticmethod
    def _direct_centered_action(
        momentum: float,
        mode_index: int,
        points: int,
    ) -> tuple[npt.NDArray[np.complex128], npt.NDArray[np.complex128]]:
        """Apply the declared one-dimensional stencil without a production constructor.

        Parameters
        ----------
        momentum
            Reduced Bloch momentum in the dimensionless period-``2*pi`` convention.
        mode_index
            Integer reciprocal label of the sampled Bloch mode.
        points
            Number of half-open uniform-grid points.

        Returns
        -------
        tuple[numpy.ndarray, numpy.ndarray]
            The complex128 sampled mode and its direct centered-stencil action in
            increasing coordinate order.
        """
        period = 2.0 * np.pi
        spacing = period / points
        coordinates = spacing * np.arange(points, dtype=np.float64)
        mode = np.asarray(
            np.exp(1j * (momentum + mode_index) * coordinates),
            dtype=np.complex128,
        )
        action = np.empty(points, dtype=np.complex128)
        coefficient = 1.0 / spacing**2
        for index in range(points):
            # At the two boundaries, the neighbor outside the stored half-open grid is
            # reconstructed by the declared directed Bloch seam rather than wrapping
            # the vector periodically without its fiber phase.
            left = (
                mode[index - 1]
                if index > 0
                else np.exp(-1j * momentum * period) * mode[-1]
            )
            right = (
                mode[index + 1]
                if index < points - 1
                else np.exp(1j * momentum * period) * mode[0]
            )
            action[index] = coefficient * (2.0 * mode[index] - left - right)
        return mode, action

    @staticmethod
    def _expected_cosine_coefficient(
        delta_p: int,
        delta_q: int,
        lambda_x: float,
        lambda_y: float,
        lambda_xy: float,
    ) -> complex:
        """Return the exact cosine-family coefficient for one transfer.

        Parameters
        ----------
        delta_p, delta_q
            Signed reciprocal transfers ``(p_prime-p, q_prime-q)``.
        lambda_x, lambda_y, lambda_xy
            Dimensionless coefficients of ``cos(x)``, ``cos(y)``, and
            ``cos(x)*cos(y)``.

        Returns
        -------
        complex
            The analytically expanded Fourier coefficient, including exact zero for
            transfers outside the three supported harmonic families.
        """
        if abs(delta_p) == 1 and delta_q == 0:
            return complex(lambda_x / 2.0)
        if delta_p == 0 and abs(delta_q) == 1:
            return complex(lambda_y / 2.0)
        if abs(delta_p) == 1 and abs(delta_q) == 1:
            return complex(lambda_xy / 4.0)
        return 0.0j

    @pytest.mark.parametrize(
        (
            "points",
            "cutoff",
            "momentum_x",
            "momentum_y",
            "entry_atol",
            "frobenius_atol",
            "two_sided",
        ),
        (
            (5, 2, 0.13, -0.21, 6.0e-15, 6.0e-15, True),
            (5, 1, 0.13, -0.21, 4.0e-15, 4.0e-15, False),
            (7, 1, -0.17, 0.09, 5.0e-15, 5.0e-15, False),
        ),
    )
    def test_dft_orthogonality__fixed_domains__matches_declared_gram_products(
        self,
        points: int,
        cutoff: int,
        momentum_x: float,
        momentum_y: float,
        entry_atol: float,
        frobenius_atol: float,
        two_sided: bool,
    ) -> None:
        """Explicit scalar geometric sums give the declared fixed-domain identities."""
        coordinates = 2.0 * np.pi * np.arange(points, dtype=np.float64) / points
        labels = tuple(range(-cutoff, cutoff + 1))
        modes = tuple((p, q) for p in labels for q in labels)
        column_gram = np.empty((len(modes), len(modes)), dtype=np.complex128)

        # Each Gram entry terminates at two scalar finite geometric sums. This route
        # neither builds the production sampling matrix nor uses outer/Kronecker matrix
        # construction, while retaining the fixed momentum's phase-rounding behavior.
        for left, (p, q) in enumerate(modes):
            for right, (p_prime, q_prime) in enumerate(modes):
                x_sum = 0.0j
                y_sum = 0.0j
                for coordinate in coordinates:
                    x_sum += np.conj(
                        np.exp(1j * (momentum_x + p) * coordinate)
                    ) * np.exp(1j * (momentum_x + p_prime) * coordinate)
                    y_sum += np.conj(
                        np.exp(1j * (momentum_y + q) * coordinate)
                    ) * np.exp(1j * (momentum_y + q_prime) * coordinate)
                column_gram[left, right] = (x_sum / points) * (y_sum / points)

        identity = np.eye(len(modes), dtype=np.complex128)
        np.testing.assert_allclose(
            column_gram,
            identity,
            rtol=0.0,
            atol=entry_atol,
        )
        assert np.linalg.norm(column_gram - identity) < frobenius_atol

        if two_sided:
            sites = tuple(
                (x_index, y_index)
                for x_index in range(points)
                for y_index in range(points)
            )
            row_gram = np.empty((len(sites), len(sites)), dtype=np.complex128)
            for left, (x_index, y_index) in enumerate(sites):
                for right, (x_prime, y_prime) in enumerate(sites):
                    x_sum = 0.0j
                    y_sum = 0.0j
                    for label in labels:
                        x_sum += np.conj(
                            np.exp(1j * (momentum_x + label) * coordinates[x_index])
                        ) * np.exp(1j * (momentum_x + label) * coordinates[x_prime])
                        y_sum += np.conj(
                            np.exp(1j * (momentum_y + label) * coordinates[y_index])
                        ) * np.exp(1j * (momentum_y + label) * coordinates[y_prime])
                    row_gram[left, right] = (x_sum / points) * (y_sum / points)
            np.testing.assert_allclose(
                row_gram,
                identity,
                rtol=0.0,
                atol=entry_atol,
            )

    @pytest.mark.parametrize(
        ("points", "momentum_x", "momentum_y", "consumer_atol"),
        (
            (5, 0.13, -0.21, 4.0e-15),
            (7, -0.17, 0.09, 6.0e-15),
        ),
    )
    def test_centered_difference_dispersion__fixed_domains__matches_direct_stencil_action(  # noqa: E501
        self,
        points: int,
        momentum_x: float,
        momentum_y: float,
        consumer_atol: float,
    ) -> None:
        """Direct seam-aware stencil action has the documented mode eigenvalues."""
        spacing = 2.0 * np.pi / points
        normalized_modes: list[npt.NDArray[np.complex128]] = []
        normalized_actions: list[npt.NDArray[np.complex128]] = []
        energies: list[float] = []
        for p in range(-1, 2):
            mode_x, action_x = self._direct_centered_action(momentum_x, p, points)
            energy_x = 4.0 / spacing**2 * np.sin(0.5 * (momentum_x + p) * spacing) ** 2
            np.testing.assert_allclose(
                action_x,
                energy_x * mode_x,
                rtol=0.0,
                atol=8.0e-15,
            )
            for q in range(-1, 2):
                mode_y, action_y = self._direct_centered_action(momentum_y, q, points)
                energy_y = (
                    4.0 / spacing**2 * np.sin(0.5 * (momentum_y + q) * spacing) ** 2
                )
                np.testing.assert_allclose(
                    action_y,
                    energy_y * mode_y,
                    rtol=0.0,
                    atol=8.0e-15,
                )
                # The two-dimensional stencil is a Kronecker sum, so its action on a
                # product mode is the sum of the independently checked eigenvalues.
                product_mode = np.asarray(
                    [x_value * y_value for x_value in mode_x for y_value in mode_y],
                    dtype=np.complex128,
                )
                product_action = np.asarray(
                    [
                        action_x[x_index] * mode_y[y_index]
                        + mode_x[x_index] * action_y[y_index]
                        for x_index in range(points)
                        for y_index in range(points)
                    ],
                    dtype=np.complex128,
                )
                energy = energy_x + energy_y
                np.testing.assert_allclose(
                    product_action,
                    energy * product_mode,
                    rtol=0.0,
                    atol=1.6e-14,
                )
                # Division by N gives each two-dimensional product mode Euclidean
                # norm one. Overlaps with the independently applied stencil then
                # reproduce the consumer's complete common-space kinetic matrix.
                normalized_modes.append(
                    np.asarray(product_mode / points, dtype=np.complex128)
                )
                normalized_actions.append(
                    np.asarray(product_action / points, dtype=np.complex128)
                )
                energies.append(float(energy))

        sampling = np.column_stack(normalized_modes)
        direct_action = np.column_stack(normalized_actions)
        np.testing.assert_allclose(
            sampling.conj().T @ direct_action,
            np.diag(energies),
            rtol=0.0,
            atol=consumer_atol,
        )

    def test_resolved_cosine_transfer__m1_n7__matches_every_fourier_block(
        self,
    ) -> None:
        """Every retained sampled cosine transfer equals its explicit coefficient."""
        points = 7
        lambda_x = 0.4
        lambda_y = 0.7
        lambda_xy = 0.2
        coordinates = 2.0 * np.pi * np.arange(points, dtype=np.float64) / points
        x_grid = coordinates[:, np.newaxis]
        y_grid = coordinates[np.newaxis, :]
        potential = (
            lambda_x * np.cos(x_grid)
            + lambda_y * np.cos(y_grid)
            + lambda_xy * np.cos(x_grid) * np.cos(y_grid)
        )

        for p in range(-1, 2):
            for q in range(-1, 2):
                for p_prime in range(-1, 2):
                    for q_prime in range(-1, 2):
                        delta_p = p_prime - p
                        delta_q = q_prime - q
                        phase = np.exp(1j * (delta_p * x_grid + delta_q * y_grid))
                        actual = complex(np.sum(potential * phase) / points**2)
                        expected = self._expected_cosine_coefficient(
                            delta_p,
                            delta_q,
                            lambda_x,
                            lambda_y,
                            lambda_xy,
                        )
                        assert abs(actual - expected) < 1.0e-15

    def test_resolved_cosine_transfer__m2_n5__demonstrates_alias_counterexample(
        self,
    ) -> None:
        """A retained transfer of four aliases to the minus-one cosine harmonic."""
        points = 5
        coordinates = 2.0 * np.pi * np.arange(points, dtype=np.float64) / points
        x_grid = coordinates[:, np.newaxis]
        potential = np.broadcast_to(np.cos(x_grid), (points, points))

        # The retained pair p=-2, p'=2 has delta p=4. Continuum cos(x) has no
        # coefficient at transfer four, but 4 is congruent to -1 modulo five.
        phase = np.exp(1j * 4 * x_grid)
        aliased = complex(np.sum(potential * phase) / points**2)
        assert abs(aliased - 0.5) < 1.0e-15
        assert self._expected_cosine_coefficient(4, 0, 1.0, 0.0, 0.0) == 0.0j
