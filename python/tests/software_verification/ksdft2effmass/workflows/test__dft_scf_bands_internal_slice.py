r"""Software verification of private DFT SCF-to-bands CPN replay contract.

Evidence profile: routine

Bounded artifact scope: private DFT SCF-to-bands CPN replay contract.

Facet and represented meaning

Effect-free replay of already-adapted SCF and fixed-density-bands result
correlations through the generic CPN kernel.

Intrinsic and cross-object scope

Exact result/input and native-continuation identities are the oracle. Distinct or
shared process identities remain reported facts and do not alter topology.

VVUQ and scientific exclusions

These tests invoke no scientific executable and establish no numerical
verification, scientific validation, convergence, equivalence, or acceptance.
"""

from dataclasses import replace

import pytest

from ksdft2effmass.workflows import ResultObjectIdentity
from ksdft2effmass.workflows._dft_scf_bands import (
    DftScfBandsCpnReplayer,
    DftScfBandsCpnReplayInput,
    DftScfBandsCpnReplayIssueCode,
    DftScfBandsCpnReplayOutcome,
)

pytestmark = pytest.mark.software_verification


def make_replay_input(
    prefix: str,
    scf_process: str,
    bands_process: str,
) -> DftScfBandsCpnReplayInput:
    """Evidence ID: Owns no identifier; supports SV-DFT-SCF-BANDS-CPN-001
    through SV-DFT-SCF-BANDS-CPN-003.

    Requirement: Test setup supplies one exact internally correlated identity set.

    Method: Construct immutable replay input from explicit lexical identities.

    Oracle: The supplied prefix and process identities define the exact setup.

    Acceptance: The returned value preserves the requested correlations exactly.

    Interpretation: Failure identifies test-setup construction drift.

    Limitations: The helper owns no independent replay or scientific claim.
    """
    scf_input = f"{prefix}:scf-input"
    bands_input = f"{prefix}:bands-input"
    scf_output = ResultObjectIdentity(f"{prefix}:scf-output")
    return DftScfBandsCpnReplayInput(
        scf_input,
        bands_input,
        scf_output,
        scf_input,
        f"{prefix}:native-density",
        scf_output,
        f"{prefix}:native-density",
        ResultObjectIdentity(f"{prefix}:bands-output"),
        bands_input,
        scf_process,
        bands_process,
    )


def test_artifact__cpn_replay__fires_scf_then_fixed_density_bands() -> None:
    """Evidence ID: SV-DFT-SCF-BANDS-CPN-001

    Requirement: Pure replay fires SCF before fixed-density bands and represents
    both supplied results only after consuming their prepared-input tokens.

    Method: Replay one correlated identity set and inspect transitions and places.

    Oracle: The accepted logical topology has exactly SCF then bands transitions.

    Acceptance: Both prepared places are empty and both completed places contain
    one token after the exact transition order fires.

    Interpretation: Failure identifies CPN topology, selection, or firing drift.

    Limitations: The test performs no effect or calculator execution.
    """
    result = DftScfBandsCpnReplayer().execute(
        make_replay_input("qe", "qe-scf-process", "qe-bands-process")
    )

    assert result.outcome is DftScfBandsCpnReplayOutcome.CONFIRMED
    assert [
        firing.firing_input.transition_identity.value
        for firing in result.firing_results
    ] == ["dft.scf", "dft.fixed-density-bands"]
    assert result.final_marking is not None
    places = {
        place.place_identity.value: place.tokens
        for place in result.final_marking.places
    }
    assert places["scf.prepared"] == ()
    assert places["bands.prepared"] == ()
    assert len(places["scf.completed"]) == 1
    assert len(places["bands.completed"]) == 1


def test_artifact__cpn_replay__does_not_equate_process_and_logical_stage() -> None:
    """Evidence ID: SV-DFT-SCF-BANDS-CPN-002

    Requirement: Process-observation identity does not define logical CPN stage
    identity or alter the SCF-to-bands dependency.

    Method: Replay distinct-process and shared-process correlation sets.

    Oracle: Process identities are retained inputs rather than transition identities.

    Acceptance: Both process arrangements produce confirmed replay without findings.

    Interpretation: Failure would couple logical stages incorrectly to processes.

    Limitations: Supplied identities are synthetic software-test values.
    """
    qe = make_replay_input("qe", "qe-scf-process", "qe-bands-process")
    abinit = make_replay_input("abinit", "abinit-process", "abinit-process")

    assert qe.scf_process_observation_identity != qe.bands_process_observation_identity
    assert (
        abinit.scf_process_observation_identity
        == abinit.bands_process_observation_identity
    )
    assert DftScfBandsCpnReplayer().execute(qe).issues == ()
    assert DftScfBandsCpnReplayer().execute(abinit).issues == ()


def test_artifact__cpn_replay__rejects_mismatched_continuation_state() -> None:
    """Evidence ID: SV-DFT-SCF-BANDS-CPN-003

    Requirement: Bands replay requires the exact native state produced by the
    supplied logical SCF result.

    Method: Replace only the bands-side native-state identity before replay.

    Oracle: Exact identity equality is required at the continuation boundary.

    Acceptance: Replay returns only the continuation-state issue and no final marking.

    Interpretation: Failure identifies fail-closed continuation-correlation drift.

    Limitations: This checks identity correlation, not native-state contents.
    """
    replay_input = replace(
        make_replay_input("qe", "qe-scf-process", "qe-bands-process"),
        bands_input_native_state_identity="different-density",
    )

    result = DftScfBandsCpnReplayer().execute(replay_input)

    assert result.outcome is DftScfBandsCpnReplayOutcome.REJECTED
    assert result.final_marking is None
    assert tuple(item.code for item in result.issues) == (
        DftScfBandsCpnReplayIssueCode.CONTINUATION_STATE_MISMATCH,
    )
