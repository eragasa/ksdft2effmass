"""Finite-rank oracle and dense-route comparison calculations."""

from __future__ import annotations

import hashlib

import numpy as np

from ksdft2effmass.serialization.json import JsonValue

from . import contracts, numerical_actions


class FiniteRankOracleComparisonCalculator:
    """Request finite-rank-oracle verification from explicit documents and location.

    Parameters
    ----------
    encoded_documents
        Exact finite-rank-oracle input and retained-result bytes. repository_root
        Absolute filesystem base for repository-relative authenticated sources.

    Raises
    ------
    TypeError
        If documents or repository root use unsupported public types.
    ValueError
        If ``repository_root`` is relative.

    Notes
    -----
    Construction checks intrinsic type and lexical location contracts only. It does
    not resolve the root, require it to exist, read files, decode JSON, authenticate
    identities, reconstruct resolvent roots or eigenspaces, or qualify an oracle.
    The verifier later authenticates the retained input identity, accepts only the
    frozen historical runner digest for a legacy result or checks explicit script
    and implementation identities for a newer result, and authenticates
    source-result identities declared by the input. It does not recursively follow
    provenance links in those source results. Neither the path nor successful
    authentication establishes material provenance, scientific validation, UQ, or
    acceptance.
    """

    __slots__ = ("_builder", "_oracle")

    def __init__(self) -> None:
        """Bind the concrete oracle and independent dense constructor."""
        self._builder = numerical_actions.FiniteRankSiteSpaceOperatorConstructor()
        self._oracle = numerical_actions.FiniteRankResolventOracle()

    def execute(
        self,
        specification: contracts.FiniteRankOracleCampaignInput,
        parent: contracts.FiniteRankOracleParentData,
    ) -> tuple[list[JsonValue], dict[str, JsonValue]]:
        """Calculate the rank-one sweep and special-control records.

        Parameters
        ----------
        specification
            Closed typed campaign specification owning all scientific controls.
        parent
            Explicit parent contract or authenticated parent data used by the operation.

        Returns
        -------
        tuple[list[JsonValue], dict[str, JsonValue]]
            Rank-one sweep records and separately retained special-control records.
        """
        sweep: list[JsonValue] = []
        for cell_count in specification.rank_one.cell_counts:
            for magnitude in specification.rank_one.attractive_magnitudes:
                sweep.append(
                    self._rank_one_record(specification, parent, cell_count, magnitude)
                )
        return sweep, self._special_records(specification, parent)

    def _rank_one_record(
        self,
        specification: contracts.FiniteRankOracleCampaignInput,
        parent: contracts.FiniteRankOracleParentData,
        cell_count: int,
        magnitude: float,
    ) -> dict[str, JsonValue]:
        """Implement the owner-local rank one record operation."""
        momentum = specification.parent.momentum
        orbital = specification.rank_one.orbital_vector
        edge = self._oracle.lower_edge(parent, cell_count, momentum)
        root = self._oracle.resolve_root(
            parent,
            cell_count,
            momentum,
            orbital,
            magnitude,
            edge,
            specification.tolerances.root_interval,
        )
        host = self._builder.execute(parent, cell_count, momentum)
        site_vector = self._site_vector(
            cell_count, specification.rank_one.defect_site, orbital
        )
        defect = -magnitude * np.outer(site_vector, site_vector.conj())
        physical = host + defect
        values, vectors = np.linalg.eigh(physical)
        oracle_vector = self._oracle.bound_vector(
            parent,
            cell_count,
            momentum,
            root.energy,
            orbital,
            specification.rank_one.defect_site,
        )
        numerical_vector = vectors[:, 0]
        fidelity = float(
            np.clip(abs(np.vdot(oracle_vector, numerical_vector)) ** 2, 0.0, 1.0)
        )
        oracle_projector = np.outer(oracle_vector, oracle_vector.conj())
        numerical_projector = np.outer(numerical_vector, numerical_vector.conj())
        numerical_host_edge = float(np.min(np.linalg.eigvalsh(host)))
        bound_count = int(np.sum(values < edge - specification.tolerances.edge_margin))
        energy_error = abs(root.energy - float(values[0]))
        eigen_residual = self._norm(
            physical @ oracle_vector - root.energy * oracle_vector
        )
        projector_defect = self._norm(oracle_projector - numerical_projector)
        if (
            energy_error > specification.tolerances.energy_agreement
            or root.secular_residual > specification.tolerances.secular_residual
            or eigen_residual > specification.tolerances.eigen_residual
            or projector_defect > specification.tolerances.projector_agreement
            or bound_count != 1
        ):
            raise ValueError("rank-one oracle comparison failed its frozen rule")
        return {
            "id": f"rank-one-N{cell_count}-g{magnitude:.3f}",
            "status": "oracle_agreement",
            "cell_count": cell_count,
            "attractive_magnitude": magnitude,
            "operator_rank": int(np.linalg.matrix_rank(defect, tol=1.0e-12)),
            "host_lower_edge": edge,
            "host_edge_route_discrepancy": abs(edge - numerical_host_edge),
            "oracle_energy": root.energy,
            "numerical_energy": float(values[0]),
            "binding_below_host_edge": edge - root.energy,
            "energy_absolute_discrepancy": energy_error,
            "oracle_secular_residual": root.secular_residual,
            "oracle_final_bracket_width": root.upper_bracket - root.lower_bracket,
            "oracle_iteration_count": root.iteration_count,
            "numerical_bound_state_count": bound_count,
            "oracle_eigen_residual": eigen_residual,
            "projector_frobenius_defect": projector_defect,
            "state_fidelity": fidelity,
            "defect_sha256": self._matrix_sha256(defect),
            "oracle_projector_sha256": self._matrix_sha256(oracle_projector),
        }

    def _special_records(
        self,
        specification: contracts.FiniteRankOracleCampaignInput,
        parent: contracts.FiniteRankOracleParentData,
    ) -> dict[str, JsonValue]:
        """Implement the owner-local special records operation."""
        control = specification.special
        momentum = specification.parent.momentum
        orbital = specification.rank_one.orbital_vector
        host = self._builder.execute(parent, control.cell_count, momentum)
        edge = self._oracle.lower_edge(parent, control.cell_count, momentum)
        site_vector = self._site_vector(
            control.cell_count, specification.rank_one.defect_site, orbital
        )
        threshold_values = np.linalg.eigvalsh(host)
        threshold_count = int(
            np.sum(threshold_values < edge - specification.tolerances.edge_margin)
        )
        probe = edge - max(specification.tolerances.edge_margin, 1.0e-4)
        green, green_imaginary, _derivative = self._oracle.local_green(
            parent, control.cell_count, momentum, probe, orbital
        )
        repulsive_defect = control.repulsive_magnitude * np.outer(
            site_vector, site_vector.conj()
        )
        repulsive_values = np.linalg.eigvalsh(host + repulsive_defect)
        repulsive_count = int(
            np.sum(repulsive_values < edge - specification.tolerances.edge_margin)
        )
        if threshold_count != 0 or repulsive_count != 0:
            raise ValueError(
                "threshold or repulsive control produced a lower bound state"
            )
        degenerate = self._degenerate_record(specification, parent)
        return {
            "threshold": {
                "id": "zero-coupling-threshold",
                "status": "threshold_no_isolated_state",
                "attractive_magnitude": control.threshold_magnitude,
                "oracle_root_energy": None,
                "numerical_bound_state_count": threshold_count,
                "edge_state_is_not_counted_as_bound": True,
            },
            "repulsive": {
                "id": "repulsive-no-lower-bound-state",
                "status": "no_bound_state_below_lower_edge",
                "repulsive_magnitude": control.repulsive_magnitude,
                "oracle_root_energy": None,
                "secular_value_near_lower_edge": 1.0
                + control.repulsive_magnitude * green,
                "secular_imaginary_part": green_imaginary,
                "numerical_bound_state_count": repulsive_count,
                "scope": "below the finite-host lower edge only",
            },
            "spin_degenerate": degenerate,
            "unequal_rank": {
                "id": "spin-degenerate-rank-one-comparison",
                "status": "stopped",
                "issue_codes": ["ANALYTICAL_ORACLE.EIGENSPACE_RANK_MISMATCH"],
                "numerical_eigenspace_rank": control.spin_degeneracy,
                "oracle_eigenspace_rank": 1,
                "projector_frobenius_defect": None,
                "state_fidelity": None,
            },
        }

    def _degenerate_record(
        self,
        specification: contracts.FiniteRankOracleCampaignInput,
        parent: contracts.FiniteRankOracleParentData,
    ) -> dict[str, JsonValue]:
        """Implement the owner-local degenerate record operation."""
        control = specification.special
        momentum = specification.parent.momentum
        orbital = specification.rank_one.orbital_vector
        edge = self._oracle.lower_edge(parent, control.cell_count, momentum)
        root = self._oracle.resolve_root(
            parent,
            control.cell_count,
            momentum,
            orbital,
            control.attractive_magnitude,
            edge,
            specification.tolerances.root_interval,
        )
        host = self._builder.execute(parent, control.cell_count, momentum)
        site_vector = self._site_vector(
            control.cell_count, specification.rank_one.defect_site, orbital
        )
        spin_identity = np.eye(control.spin_degeneracy)
        spin_host = np.asarray(np.kron(host, spin_identity), dtype=np.complex128)
        spin_defect = -control.attractive_magnitude * np.asarray(
            np.kron(np.outer(site_vector, site_vector.conj()), spin_identity),
            dtype=np.complex128,
        )
        values, vectors = np.linalg.eigh(spin_host + spin_defect)
        base_oracle = self._oracle.bound_vector(
            parent,
            control.cell_count,
            momentum,
            root.energy,
            orbital,
            specification.rank_one.defect_site,
        )
        oracle_columns = np.column_stack(
            [
                np.kron(base_oracle, spin_identity[:, index])
                for index in range(control.spin_degeneracy)
            ]
        )
        oracle_projector = oracle_columns @ oracle_columns.conj().T
        numerical_columns = vectors[:, : control.spin_degeneracy]
        numerical_projector = numerical_columns @ numerical_columns.conj().T
        bound_count = int(np.sum(values < edge - specification.tolerances.edge_margin))
        energy_error = float(
            np.max(np.abs(values[: control.spin_degeneracy] - root.energy))
        )
        projector_defect = self._norm(oracle_projector - numerical_projector)
        if (
            bound_count != control.spin_degeneracy
            or energy_error > specification.tolerances.energy_agreement
            or projector_defect > specification.tolerances.projector_agreement
        ):
            raise ValueError("degenerate oracle comparison failed its frozen rule")
        return {
            "id": "spin-degenerate-rank-two-oracle",
            "status": "oracle_agreement",
            "cell_count": control.cell_count,
            "attractive_magnitude": control.attractive_magnitude,
            "operator_rank": int(np.linalg.matrix_rank(spin_defect, tol=1.0e-12)),
            "oracle_eigenspace_rank": control.spin_degeneracy,
            "numerical_eigenspace_rank": control.spin_degeneracy,
            "numerical_bound_state_count": bound_count,
            "oracle_energy": root.energy,
            "maximum_energy_absolute_discrepancy": energy_error,
            "numerical_energy_splitting": float(
                np.ptp(values[: control.spin_degeneracy])
            ),
            "projector_frobenius_defect": projector_defect,
            "individual_state_fidelity": None,
            "comparison_rule": "equal-rank eigenspace projectors",
            "oracle_projector_sha256": self._matrix_sha256(oracle_projector),
        }

    def _site_vector(
        self, cell_count: int, defect_site: int, orbital: contracts.ComplexVector
    ) -> contracts.ComplexVector:
        """Construct this Workflow's localized orbital vector."""
        if defect_site >= cell_count:
            raise ValueError("defect site lies outside the supercell")
        result = np.zeros(2 * cell_count, dtype=np.complex128)
        result[2 * defect_site : 2 * defect_site + 2] = orbital
        return result

    def _matrix_sha256(self, matrix: contracts.ComplexMatrix) -> str:
        """Compute this Workflow's canonical matrix identity."""
        canonical = np.stack((matrix.real, matrix.imag), axis=-1).astype(
            "<f8", copy=True
        )
        canonical[canonical == 0.0] = 0.0
        return hashlib.sha256(canonical.tobytes(order="C")).hexdigest()

    def _norm(
        self,
        value: contracts.ComplexMatrix | contracts.ComplexVector | contracts.RealArray,
    ) -> float:
        """Compute one norm for this Workflow."""
        return float(np.linalg.norm(value))
