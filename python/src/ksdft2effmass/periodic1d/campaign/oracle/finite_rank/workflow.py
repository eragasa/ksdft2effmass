"""Orchestrate the finite-rank-oracle campaign result."""

from __future__ import annotations

import json
from typing import cast

from ksdft2effmass.serialization.json import JsonValue

from . import contracts
from .comparison import FiniteRankOracleComparisonCalculator
from .result_documents import FiniteRankOracleCampaignResultDocument


class FiniteRankOracleCampaignWorkflow:
    """Identify one immutable source artifact.

    Parameters
    ----------
    path
        Nonempty repository-relative path of an authenticated compact source. sha256
        Lowercase 64-character SHA-256 content identity.

    Raises
    ------
    ValueError
        An argument violates a schema, domain, identity, or correlation invariant.
    """

    __slots__ = ("_comparison",)

    def __init__(self) -> None:
        """Bind the concrete finite-rank comparison calculator."""
        self._comparison = FiniteRankOracleComparisonCalculator()

    def execute(
        self,
        specification: contracts.FiniteRankOracleCampaignInput,
        parent: contracts.FiniteRankOracleParentData,
        provenance: contracts.FiniteRankOracleProvenance,
    ) -> FiniteRankOracleCampaignResultDocument:
        """Calculate the rank-one sweep and all special controls.

        Parameters
        ----------
        specification
            Closed typed campaign specification owning all scientific controls.
        parent
            Explicit parent contract or authenticated parent data used by the operation.
        provenance
            Structured identities of authenticated inputs, implementation, and software
            versions.

        Returns
        -------
        FiniteRankOracleCampaignResultDocument
            Immutable exact result document for the finite-rank sweep and special
            controls.
        """
        sweep, special = self._comparison.execute(specification, parent)
        sweep_records = tuple(cast(dict[str, JsonValue], item) for item in sweep)
        energy_errors = [
            self._real(item["energy_absolute_discrepancy"]) for item in sweep_records
        ]
        projector_errors = [
            self._real(item["projector_frobenius_defect"]) for item in sweep_records
        ]
        secular_residuals = [
            self._real(item["oracle_secular_residual"]) for item in sweep_records
        ]
        bound_state_counts = [
            cast(JsonValue, value)
            for value in sorted(
                {
                    self._integer(item["numerical_bound_state_count"])
                    for item in sweep_records
                }
            )
        ]
        payload: dict[str, JsonValue] = {
            "schema_version": 1,
            "experiment_id": specification.experiment_id,
            "evidence_status": "synthetic test data",
            "calculation_status": (
                "calculated synthetic numerical-verification result"
            ),
            "oracle_contract": {
                "finite_rank_identity": specification.rank_one.equation,
                "root_domain": specification.rank_one.root_domain,
                "root_selection": specification.rank_one.root_selection,
                "oracle_route": (
                    "direct 2 by 2 Bloch-fiber resolvent sum and scalar bisection"
                ),
                "numerical_route": (
                    "independent dense site-space assembly and Hermitian eigensolve"
                ),
                "independence_boundary": (
                    "The oracle does not diagonalize the full defect Hamiltonian; "
                    "the numerical route does not call the resolvent root resolver."
                ),
            },
            "represented_space": {
                "group_id": specification.parent.group_id,
                "hopping_range_cells": specification.parent.hopping_range,
                "supercell_momentum": specification.parent.momentum,
                "energy_unit": specification.parent.energy_unit,
                "ordering": specification.parent.ordering,
                "orbital_vector": [
                    [float(value.real), float(value.imag)]
                    for value in specification.rank_one.orbital_vector
                ],
                "defect_site": specification.rank_one.defect_site,
            },
            "rank_one_sweep": sweep,
            "special_controls": special,
            "summary": {
                "case_count": len(sweep),
                "maximum_energy_absolute_discrepancy": max(energy_errors),
                "maximum_projector_frobenius_defect": max(projector_errors),
                "maximum_oracle_secular_residual": max(secular_residuals),
                "all_attractive_bound_state_counts": bound_state_counts,
            },
            "error_accounting": {
                "oracle_root_error": "retained secular residual and final bracket",
                "numerical_spectral_error": (
                    "oracle root versus independently diagonalized defect energy"
                ),
                "state_error": (
                    "equal-rank projector defect and nondegenerate fidelity"
                ),
                "finite_size_dependence": (
                    "reported by supercell size without a continuum-limit claim"
                ),
                "model_reduction_error": "Not evaluated in this exercise.",
                "scientific_validation": "Not performed.",
                "uncertainty_quantification": "Not performed.",
            },
            "source_identities": [
                {"path": item.path, "sha256": item.sha256} for item in parent.sources
            ],
            "limitations": [
                "The parent, finite-rank defects, and all observations are synthetic.",
                (
                    "The resolvent identity verifies finite represented operators, "
                    "not a continuum impurity model."
                ),
                (
                    "The supercell sequence measures finite-size dependence but does "
                    "not establish convergence to an infinite system."
                ),
                (
                    "No silicon, dopant, DFT, material validation, transferability, "
                    "scientific validation, or UQ claim is made."
                ),
            ],
            "provenance": {
                "input_path": provenance.input_path,
                "input_sha256": provenance.input_sha256,
                "script_path": provenance.script_path,
                "script_sha256": provenance.script_sha256,
                "python_version": provenance.python_version,
                "numpy_version": provenance.numpy_version,
            },
        }
        return FiniteRankOracleCampaignResultDocument(
            (
                json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
            ).encode()
        )

    def _real(self, value: JsonValue) -> float:
        """Require one retained real value for this Workflow."""
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("retained value must be numeric")
        return float(value)

    def _integer(self, value: JsonValue) -> int:
        """Require one retained integer value for this Workflow."""
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("retained value must be an integer")
        return value
