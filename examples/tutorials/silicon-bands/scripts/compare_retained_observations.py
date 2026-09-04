"""Replay and compare the maintained paired silicon tutorial observations.

This deterministic example reads only compact committed observations.  It does
not read native external run state, invoke QE or ABINIT, authorize execution, or
claim numerical comparison, verification, validation, or acceptance.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ksdft2effmass.analysis._band_comparison import (
    BandComparisonSpecification,
    BandStructureComparator,
)
from ksdft2effmass.calculators._dft import (
    AbinitFixedDensityBandsInput,
    AbinitFixedDensityBandsOutput,
    AbinitScfInput,
    AbinitScfOutput,
    CalculatorArtifactIdentity,
    ProcessObservationIdentity,
    QuantumEspressoFixedDensityBandsInput,
    QuantumEspressoFixedDensityBandsOutput,
    QuantumEspressoScfInput,
    QuantumEspressoScfOutput,
    SimulationInputIdentity,
)
from ksdft2effmass.periodic._bands import (
    BandEnergyUnit,
    BandStructureObservation,
    BandStructureObservationIdentity,
    DftBackend,
)
from ksdft2effmass.workflows import ResultObjectIdentity
from ksdft2effmass.workflows._dft_scf_bands import (
    DftScfBandsCpnReplayer,
    DftScfBandsCpnReplayInput,
)

_REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
_QE_OBSERVATION = _REPOSITORY_ROOT / (
    "examples/tutorials/silicon-bands/qe/expected/qe75-calculated-observation.json"
)
_ABINIT_OBSERVATION = _REPOSITORY_ROOT / (
    "examples/tutorials/silicon-bands/abinit/expected/"
    "abinit1083-calculated-observation.json"
)


@dataclass(frozen=True, slots=True)
class RetainedSiliconTutorialValues:
    """Typed replay inputs and normalized observations derived from two documents."""

    qe_replay_input: DftScfBandsCpnReplayInput
    abinit_replay_input: DftScfBandsCpnReplayInput
    qe_observation: BandStructureObservation
    abinit_observation: BandStructureObservation


class RetainedSiliconTutorialObservationAdapter:
    """Adapt the two exact maintained observation shapes to the private slice."""

    def execute(
        self,
        qe_document: dict[str, Any],
        abinit_document: dict[str, Any],
    ) -> RetainedSiliconTutorialValues:
        """Return typed calculator and normalized values without external effects."""
        qe_id = self._string(qe_document, "observation_id")
        abinit_id = self._string(abinit_document, "observation_id")
        qe_pseudo = self._nested_string(qe_document, "pseudopotential", "sha256")
        abinit_pseudo = self._nested_string(
            abinit_document, "pseudopotential", "sha256"
        )

        qe_scf_input = QuantumEspressoScfInput(
            SimulationInputIdentity(f"{qe_id}:input:scf"),
            CalculatorArtifactIdentity(
                "sha256:"
                + self._nested_string(qe_document, "inputs", "si.scf.in", "sha256")
            ),
            (CalculatorArtifactIdentity(f"sha256:{qe_pseudo}"),),
        )
        qe_scf_result_identity = ResultObjectIdentity(f"{qe_id}:result:scf")
        qe_state = CalculatorArtifactIdentity(
            "sha256:"
            + self._native_output_sha256(qe_document, "scf_density_continuation")
        )
        qe_scf_output = QuantumEspressoScfOutput(
            qe_scf_result_identity,
            qe_scf_input.identity,
            ProcessObservationIdentity(f"{qe_id}:process:scf"),
            qe_state,
        )
        qe_bands_input = QuantumEspressoFixedDensityBandsInput(
            SimulationInputIdentity(f"{qe_id}:input:fixed-density-bands"),
            CalculatorArtifactIdentity(
                "sha256:"
                + self._nested_string(qe_document, "inputs", "si.band.in", "sha256")
            ),
            qe_scf_input.pseudopotential_identities,
            qe_scf_output.identity,
            qe_state,
        )
        qe_bands_output = QuantumEspressoFixedDensityBandsOutput(
            ResultObjectIdentity(f"{qe_id}:result:fixed-density-bands"),
            qe_bands_input.identity,
            ProcessObservationIdentity(f"{qe_id}:process:bands"),
            CalculatorArtifactIdentity(
                f"retained-spectrum:{qe_id}:"
                + self._nested_string(
                    qe_document, "bands", "external_run_spectrum_record"
                )
            ),
        )

        abinit_native_input = CalculatorArtifactIdentity(
            "sha256:" + self._nested_string(abinit_document, "input", "sha256")
        )
        abinit_pseudopotentials = (
            CalculatorArtifactIdentity(f"sha256:{abinit_pseudo}"),
        )
        abinit_scf_input = AbinitScfInput(
            SimulationInputIdentity(f"{abinit_id}:input:dataset-1-scf"),
            abinit_native_input,
            abinit_pseudopotentials,
        )
        abinit_scf_result_identity = ResultObjectIdentity(
            f"{abinit_id}:result:dataset-1-scf"
        )
        abinit_state = CalculatorArtifactIdentity(
            "sha256:"
            + self._native_output_sha256(abinit_document, "scf_density_continuation")
        )
        abinit_process = ProcessObservationIdentity(f"{abinit_id}:process:abinit")
        abinit_scf_output = AbinitScfOutput(
            abinit_scf_result_identity,
            abinit_scf_input.identity,
            abinit_process,
            abinit_state,
        )
        abinit_bands_input = AbinitFixedDensityBandsInput(
            SimulationInputIdentity(f"{abinit_id}:input:dataset-2-bands"),
            abinit_native_input,
            abinit_pseudopotentials,
            abinit_scf_output.identity,
            abinit_state,
        )
        abinit_bands_output = AbinitFixedDensityBandsOutput(
            ResultObjectIdentity(f"{abinit_id}:result:dataset-2-bands"),
            abinit_bands_input.identity,
            abinit_process,
            CalculatorArtifactIdentity(
                f"retained-spectrum:{abinit_id}:"
                + self._nested_string(
                    abinit_document,
                    "bands_dataset",
                    "external_run_spectrum_record",
                )
            ),
        )

        return RetainedSiliconTutorialValues(
            DftScfBandsCpnReplayInput(
                qe_scf_input.identity.value,
                qe_bands_input.identity.value,
                qe_scf_output.identity,
                qe_scf_output.input_identity.value,
                qe_scf_output.native_state_identity.value,
                qe_bands_input.scf_output_identity,
                qe_bands_input.native_state_identity.value,
                qe_bands_output.identity,
                qe_bands_output.input_identity.value,
                qe_scf_output.process_observation_identity.value,
                qe_bands_output.process_observation_identity.value,
            ),
            DftScfBandsCpnReplayInput(
                abinit_scf_input.identity.value,
                abinit_bands_input.identity.value,
                abinit_scf_output.identity,
                abinit_scf_output.input_identity.value,
                abinit_scf_output.native_state_identity.value,
                abinit_bands_input.scf_output_identity,
                abinit_bands_input.native_state_identity.value,
                abinit_bands_output.identity,
                abinit_bands_output.input_identity.value,
                abinit_scf_output.process_observation_identity.value,
                abinit_bands_output.process_observation_identity.value,
            ),
            self._qe_band_observation(qe_document, qe_bands_output, qe_pseudo),
            self._abinit_band_observation(
                abinit_document, abinit_bands_output, abinit_pseudo
            ),
        )

    def _qe_band_observation(
        self,
        document: dict[str, Any],
        output: QuantumEspressoFixedDensityBandsOutput,
        pseudopotential_sha256: str,
    ) -> BandStructureObservation:
        """Normalize the committed QE structural band summary."""
        observation_id = self._string(document, "observation_id")
        return BandStructureObservation(
            BandStructureObservationIdentity(f"{observation_id}:normalized-bands"),
            output.identity.value,
            DftBackend.QUANTUM_ESPRESSO,
            "diamond-silicon.two-atom",
            True,
            tuple(self._nested_string(document, "path", "topology").split("-")),
            self._nested_integer(document, "bands", "k_point_count"),
            self._nested_integer(document, "bands", "band_count"),
            self._nested_string(document, "bands", "k_point_coordinate_convention"),
            None,
            self._nested_float(document, "settings_summary", "lattice_parameter_bohr"),
            self._nested_float(document, "settings_summary", "wavefunction_cutoff_ry")
            / 2.0,
            pseudopotential_sha256,
            None,
            BandEnergyUnit(self._nested_string(document, "bands", "eigenvalue_unit")),
            self._nested_string(document, "bands", "eigenvalue_reference"),
            None,
            output.native_band_result_identity.value,
            None,
        )

    def _abinit_band_observation(
        self,
        document: dict[str, Any],
        output: AbinitFixedDensityBandsOutput,
        pseudopotential_sha256: str,
    ) -> BandStructureObservation:
        """Normalize the committed ABINIT structural band summary."""
        observation_id = self._string(document, "observation_id")
        return BandStructureObservation(
            BandStructureObservationIdentity(f"{observation_id}:normalized-bands"),
            output.identity.value,
            DftBackend.ABINIT,
            "diamond-silicon.two-atom",
            True,
            tuple(self._nested_string(document, "path", "topology").split("-")),
            self._nested_integer(document, "bands_dataset", "k_point_count"),
            self._nested_integer(document, "bands_dataset", "band_count"),
            self._nested_string(
                document, "bands_dataset", "k_point_coordinate_convention"
            ),
            None,
            self._nested_float(document, "settings_summary", "lattice_parameter_bohr"),
            self._nested_float(
                document, "settings_summary", "wavefunction_cutoff_hartree"
            ),
            pseudopotential_sha256,
            None,
            BandEnergyUnit(
                self._nested_string(document, "bands_dataset", "eigenvalue_unit")
            ),
            self._nested_string(document, "bands_dataset", "eigenvalue_reference"),
            None,
            output.native_band_result_identity.value,
            None,
        )

    @staticmethod
    def _string(document: dict[str, Any], key: str) -> str:
        """Return one required string field from a maintained document."""
        value = document[key]
        if type(value) is not str or not value:
            raise ValueError(f"{key} must be a nonempty string")
        return value

    @classmethod
    def _nested_string(cls, document: dict[str, Any], *keys: str) -> str:
        """Return one required nested string field."""
        value: Any = document
        for key in keys:
            if type(value) is not dict:
                raise ValueError(f"{'.'.join(keys)} has a non-object parent")
            value = value[key]
        if type(value) is not str or not value:
            raise ValueError(f"{'.'.join(keys)} must be a nonempty string")
        return value

    @classmethod
    def _nested_integer(cls, document: dict[str, Any], *keys: str) -> int:
        """Return one required nested exact integer field."""
        value: Any = document
        for key in keys:
            if type(value) is not dict:
                raise ValueError(f"{'.'.join(keys)} has a non-object parent")
            value = value[key]
        if type(value) is not int:
            raise ValueError(f"{'.'.join(keys)} must be an integer")
        return value

    @classmethod
    def _nested_float(cls, document: dict[str, Any], *keys: str) -> float:
        """Return one required nested JSON number as a float."""
        value: Any = document
        for key in keys:
            if type(value) is not dict:
                raise ValueError(f"{'.'.join(keys)} has a non-object parent")
            value = value[key]
        if type(value) not in (int, float):
            raise ValueError(f"{'.'.join(keys)} must be a number")
        return float(value)

    @staticmethod
    def _native_output_sha256(document: dict[str, Any], role: str) -> str:
        """Return the digest of one exact native-output role."""
        outputs = document["external_native_outputs"]
        if type(outputs) is not list:
            raise ValueError("external_native_outputs must be an array")
        matches = [
            item for item in outputs if type(item) is dict and item.get("role") == role
        ]
        if len(matches) != 1:
            raise ValueError(f"expected exactly one native output with role {role}")
        digest = matches[0].get("sha256")
        if type(digest) is not str or not digest:
            raise ValueError(f"native output {role} must have a SHA-256 digest")
        return digest


class RetainedSiliconTutorialReportSerializer:
    """Serialize the bounded example report to deterministic JSON text."""

    def execute(self, values: RetainedSiliconTutorialValues) -> str:
        """Replay both backends, reject unsupported comparison, and serialize."""
        if type(values) is not RetainedSiliconTutorialValues:
            raise TypeError("values must be RetainedSiliconTutorialValues")
        replayer = DftScfBandsCpnReplayer()
        qe_replay = replayer.execute(values.qe_replay_input)
        abinit_replay = replayer.execute(values.abinit_replay_input)
        comparison = BandStructureComparator().execute(
            values.qe_observation,
            values.abinit_observation,
            BandComparisonSpecification(
                "diamond-silicon.two-atom",
                ("L", "Gamma", "X", "Gamma"),
                8,
                BandEnergyUnit.HARTREE,
                "paired-silicon.common-comparison-grid.v1",
                "paired-silicon.pseudopotential-alignment.v1",
                "paired-silicon.energy-alignment.v1",
                0.0,
                0.0,
                0.0,
            ),
        )
        qe_processes = values.qe_replay_input
        abinit_processes = values.abinit_replay_input
        payload = {
            "schema_version": 1,
            "status": "internal_architecture_probe",
            "claim_boundary": (
                "Effect-free CPN replay and fail-closed software comparison only; "
                "no execution, numerical comparison, verification, validation, or "
                "acceptance."
            ),
            "replay": {
                "quantum_espresso": {
                    "outcome": qe_replay.outcome.value,
                    "transition_order": [
                        item.firing_input.transition_identity.value
                        for item in qe_replay.firing_results
                    ],
                    "logical_stages_share_process_observation": (
                        qe_processes.scf_process_observation_identity
                        == qe_processes.bands_process_observation_identity
                    ),
                },
                "abinit": {
                    "outcome": abinit_replay.outcome.value,
                    "transition_order": [
                        item.firing_input.transition_identity.value
                        for item in abinit_replay.firing_results
                    ],
                    "logical_stages_share_process_observation": (
                        abinit_processes.scf_process_observation_identity
                        == abinit_processes.bands_process_observation_identity
                    ),
                },
            },
            "comparison": {
                "outcome": comparison.outcome.value,
                "workflow_structure_compatible": (
                    comparison.workflow_structure_compatible
                ),
                "issue_codes": [item.code.value for item in comparison.issues],
                "maximum_absolute_difference_hartree": (
                    comparison.maximum_absolute_difference_hartree
                ),
            },
        }
        return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def main() -> None:
    """Read maintained observations and print the deterministic probe report."""
    qe_document = json.loads(_QE_OBSERVATION.read_text(encoding="utf-8"))
    abinit_document = json.loads(_ABINIT_OBSERVATION.read_text(encoding="utf-8"))
    values = RetainedSiliconTutorialObservationAdapter().execute(
        qe_document, abinit_document
    )
    print(RetainedSiliconTutorialReportSerializer().execute(values), end="")


if __name__ == "__main__":
    main()
