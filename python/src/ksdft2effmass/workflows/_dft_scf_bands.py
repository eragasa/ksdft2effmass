"""Effect-free CPN replay for one logical DFT SCF-to-bands workflow.

This private vertical slice admits already-existing calculator results and
replays only their logical dependency through the generic colored-Petri-net
kernel.  It performs no executable invocation, authorization, persistence,
retry, parsing, convergence decision, or scientific acceptance.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from ksdft2effmass.petrinet.colored import (
    ColoredPetriNetArcDefinition,
    ColoredPetriNetArcIdentity,
    ColoredPetriNetBinding,
    ColoredPetriNetBindingAssignment,
    ColoredPetriNetBindingSelector,
    ColoredPetriNetBindingVariableIdentity,
    ColoredPetriNetColorDefinition,
    ColoredPetriNetColorIdentity,
    ColoredPetriNetDefinition,
    ColoredPetriNetDefinitionIdentity,
    ColoredPetriNetFiringInput,
    ColoredPetriNetFiringOutcomeKind,
    ColoredPetriNetFiringResult,
    ColoredPetriNetGuardExpression,
    ColoredPetriNetGuardOperator,
    ColoredPetriNetInputInscription,
    ColoredPetriNetInputMode,
    ColoredPetriNetMarking,
    ColoredPetriNetMarkingIdentity,
    ColoredPetriNetOutputInscription,
    ColoredPetriNetPlaceDefinition,
    ColoredPetriNetPlaceIdentity,
    ColoredPetriNetPlaceMarking,
    ColoredPetriNetSelectionOutcomeKind,
    ColoredPetriNetToken,
    ColoredPetriNetTokenIdentity,
    ColoredPetriNetTokenPattern,
    ColoredPetriNetTokenTemplate,
    ColoredPetriNetTransitionDefinition,
    ColoredPetriNetTransitionEnabler,
    ColoredPetriNetTransitionFirer,
    ColoredPetriNetTransitionIdentity,
    ColoredPetriNetValue,
    ColoredPetriNetValueExpression,
    ColoredPetriNetValueExpressionKind,
    ColoredPetriNetValueKind,
)

from .model import ResultObjectIdentity


def _require_string(value: object, name: str) -> None:
    """Require one nonempty exact string."""
    if type(value) is not str:
        raise TypeError(f"{name} must be a string")
    if not value:
        raise ValueError(f"{name} must not be empty")


@dataclass(frozen=True, slots=True)
class DftScfBandsCpnReplayInput:
    """Workflow-level identity facts supplied for pure logical replay.

    Calculator-specific adapters retain the concrete input and output objects.
    This Workflow-owned value carries only the exact correlations needed by the
    logical CPN and therefore introduces no Workflow-to-calculator dependency.
    """

    scf_input_identity: str
    bands_input_identity: str
    scf_output_identity: ResultObjectIdentity
    scf_output_input_identity: str
    scf_native_state_identity: str
    bands_input_scf_output_identity: ResultObjectIdentity
    bands_input_native_state_identity: str
    bands_output_identity: ResultObjectIdentity
    bands_output_input_identity: str
    scf_process_observation_identity: str
    bands_process_observation_identity: str

    def __post_init__(self) -> None:
        """Validate exact nominal and lexical correlation fields."""
        for name in (
            "scf_input_identity",
            "bands_input_identity",
            "scf_output_input_identity",
            "scf_native_state_identity",
            "bands_input_native_state_identity",
            "bands_output_input_identity",
            "scf_process_observation_identity",
            "bands_process_observation_identity",
        ):
            _require_string(getattr(self, name), name)
        for name in (
            "scf_output_identity",
            "bands_input_scf_output_identity",
            "bands_output_identity",
        ):
            if type(getattr(self, name)) is not ResultObjectIdentity:
                raise TypeError(f"{name} must be ResultObjectIdentity")


class DftScfBandsCpnReplayOutcome(StrEnum):
    """Closed logical replay outcome."""

    CONFIRMED = "confirmed"
    REJECTED = "rejected"


class DftScfBandsCpnReplayIssueCode(StrEnum):
    """Closed reasons why supplied values cannot produce a confirmed replay."""

    SCF_INPUT_RESULT_MISMATCH = "scf_input_result_mismatch"
    BANDS_INPUT_RESULT_MISMATCH = "bands_input_result_mismatch"
    CONTINUATION_RESULT_MISMATCH = "continuation_result_mismatch"
    CONTINUATION_STATE_MISMATCH = "continuation_state_mismatch"
    CPN_SELECTION_MISMATCH = "cpn_selection_mismatch"
    CPN_FIRING_FAILURE = "cpn_firing_failure"


@dataclass(frozen=True, slots=True)
class DftScfBandsCpnReplayIssue:
    """One structured replay rejection reason."""

    code: DftScfBandsCpnReplayIssueCode
    diagnostic: str

    def __post_init__(self) -> None:
        """Validate exact issue state."""
        if not isinstance(self.code, DftScfBandsCpnReplayIssueCode):
            raise TypeError("code must be DftScfBandsCpnReplayIssueCode")
        if type(self.diagnostic) is not str:
            raise TypeError("diagnostic must be a string")
        if not self.diagnostic:
            raise ValueError("diagnostic must not be empty")


@dataclass(frozen=True, slots=True)
class DftScfBandsCpnReplayResult:
    """Pure CPN replay result for supplied logical SCF and bands results."""

    outcome: DftScfBandsCpnReplayOutcome
    replay_input: DftScfBandsCpnReplayInput
    definition: ColoredPetriNetDefinition
    initial_marking: ColoredPetriNetMarking
    firing_results: tuple[ColoredPetriNetFiringResult, ...]
    final_marking: ColoredPetriNetMarking | None
    issues: tuple[DftScfBandsCpnReplayIssue, ...]

    def __post_init__(self) -> None:
        """Enforce the exact confirmed or rejected result variant."""
        if not isinstance(self.outcome, DftScfBandsCpnReplayOutcome):
            raise TypeError("outcome must be DftScfBandsCpnReplayOutcome")
        if type(self.replay_input) is not DftScfBandsCpnReplayInput:
            raise TypeError("replay_input must be DftScfBandsCpnReplayInput")
        if type(self.definition) is not ColoredPetriNetDefinition:
            raise TypeError("definition must be ColoredPetriNetDefinition")
        if type(self.initial_marking) is not ColoredPetriNetMarking:
            raise TypeError("initial_marking must be ColoredPetriNetMarking")
        if type(self.firing_results) is not tuple or any(
            type(item) is not ColoredPetriNetFiringResult
            for item in self.firing_results
        ):
            raise TypeError(
                "firing_results must be a tuple of ColoredPetriNetFiringResult"
            )
        if self.final_marking is not None and (
            type(self.final_marking) is not ColoredPetriNetMarking
        ):
            raise TypeError("final_marking must be ColoredPetriNetMarking or None")
        if type(self.issues) is not tuple or any(
            type(item) is not DftScfBandsCpnReplayIssue for item in self.issues
        ):
            raise TypeError("issues must be a tuple of DftScfBandsCpnReplayIssue")
        confirmed = (
            self.outcome is DftScfBandsCpnReplayOutcome.CONFIRMED
            and len(self.firing_results) == 2
            and self.final_marking is not None
            and not self.issues
        )
        rejected = (
            self.outcome is DftScfBandsCpnReplayOutcome.REJECTED
            and self.final_marking is None
            and bool(self.issues)
        )
        if not (confirmed or rejected):
            raise ValueError("replay fields do not match the outcome")


class DftScfBandsCpnReplayer:
    """ActionObject replaying supplied SCF and bands results through a pure CPN."""

    def execute(
        self, replay_input: DftScfBandsCpnReplayInput
    ) -> DftScfBandsCpnReplayResult:
        """Validate correlations and fire the logical SCF then bands transitions."""
        if type(replay_input) is not DftScfBandsCpnReplayInput:
            raise TypeError("replay_input must be DftScfBandsCpnReplayInput")
        definition = self._definition()
        initial = self._initial_marking(definition, replay_input)
        issues = self._correlation_issues(replay_input)
        if issues:
            return DftScfBandsCpnReplayResult(
                DftScfBandsCpnReplayOutcome.REJECTED,
                replay_input,
                definition,
                initial,
                (),
                None,
                issues,
            )

        scf_firing, issue = self._fire(
            definition,
            initial,
            ColoredPetriNetTransitionIdentity("dft.scf"),
            ColoredPetriNetBindingVariableIdentity("scf_output"),
            replay_input.scf_output_identity.value,
        )
        if issue is not None:
            return DftScfBandsCpnReplayResult(
                DftScfBandsCpnReplayOutcome.REJECTED,
                replay_input,
                definition,
                initial,
                (),
                None,
                (issue,),
            )
        assert scf_firing is not None
        assert scf_firing.successor_marking is not None

        bands_firing, issue = self._fire(
            definition,
            scf_firing.successor_marking,
            ColoredPetriNetTransitionIdentity("dft.fixed-density-bands"),
            ColoredPetriNetBindingVariableIdentity("bands_output"),
            replay_input.bands_output_identity.value,
        )
        if issue is not None:
            return DftScfBandsCpnReplayResult(
                DftScfBandsCpnReplayOutcome.REJECTED,
                replay_input,
                definition,
                initial,
                (scf_firing,),
                None,
                (issue,),
            )
        assert bands_firing is not None
        assert bands_firing.successor_marking is not None
        return DftScfBandsCpnReplayResult(
            DftScfBandsCpnReplayOutcome.CONFIRMED,
            replay_input,
            definition,
            initial,
            (scf_firing, bands_firing),
            bands_firing.successor_marking,
            (),
        )

    @staticmethod
    def _correlation_issues(
        replay_input: DftScfBandsCpnReplayInput,
    ) -> tuple[DftScfBandsCpnReplayIssue, ...]:
        """Return fail-closed cross-object correlation findings."""
        issues: list[DftScfBandsCpnReplayIssue] = []
        if replay_input.scf_output_input_identity != replay_input.scf_input_identity:
            issues.append(
                DftScfBandsCpnReplayIssue(
                    DftScfBandsCpnReplayIssueCode.SCF_INPUT_RESULT_MISMATCH,
                    "SCF result does not identify the supplied SCF input",
                )
            )
        if (
            replay_input.bands_output_input_identity
            != replay_input.bands_input_identity
        ):
            issues.append(
                DftScfBandsCpnReplayIssue(
                    DftScfBandsCpnReplayIssueCode.BANDS_INPUT_RESULT_MISMATCH,
                    "bands result does not identify the supplied bands input",
                )
            )
        if (
            replay_input.bands_input_scf_output_identity
            != replay_input.scf_output_identity
        ):
            issues.append(
                DftScfBandsCpnReplayIssue(
                    DftScfBandsCpnReplayIssueCode.CONTINUATION_RESULT_MISMATCH,
                    "bands input does not reference the supplied SCF result",
                )
            )
        if (
            replay_input.bands_input_native_state_identity
            != replay_input.scf_native_state_identity
        ):
            issues.append(
                DftScfBandsCpnReplayIssue(
                    DftScfBandsCpnReplayIssueCode.CONTINUATION_STATE_MISMATCH,
                    "bands input does not reference the SCF native state",
                )
            )
        return tuple(issues)

    @staticmethod
    def _fire(
        definition: ColoredPetriNetDefinition,
        marking: ColoredPetriNetMarking,
        expected_transition: ColoredPetriNetTransitionIdentity,
        output_variable: ColoredPetriNetBindingVariableIdentity,
        output_identity: str,
    ) -> tuple[
        ColoredPetriNetFiringResult | None,
        DftScfBandsCpnReplayIssue | None,
    ]:
        """Select and purely fire one expected logical transition."""
        enablement = ColoredPetriNetTransitionEnabler().execute(definition, marking)
        selection = ColoredPetriNetBindingSelector().execute(definition, enablement)
        if (
            selection.outcome is not ColoredPetriNetSelectionOutcomeKind.SELECTED
            or selection.selected_binding is None
            or selection.selected_binding.transition_identity != expected_transition
        ):
            return None, DftScfBandsCpnReplayIssue(
                DftScfBandsCpnReplayIssueCode.CPN_SELECTION_MISMATCH,
                f"CPN did not select expected transition {expected_transition.value}",
            )
        external = ColoredPetriNetBinding(
            expected_transition,
            (
                ColoredPetriNetBindingAssignment(
                    output_variable,
                    ColoredPetriNetValue(
                        ColoredPetriNetValueKind.STRING, output_identity
                    ),
                ),
            ),
        )
        firing = ColoredPetriNetTransitionFirer().execute(
            ColoredPetriNetFiringInput(
                definition,
                expected_transition,
                marking,
                enablement,
                selection,
                selection.selected_binding,
                None,
                external,
            )
        )
        if firing.outcome is not ColoredPetriNetFiringOutcomeKind.SUCCESS:
            assert firing.failure is not None
            return None, DftScfBandsCpnReplayIssue(
                DftScfBandsCpnReplayIssueCode.CPN_FIRING_FAILURE,
                f"{firing.failure.code.value}: {firing.failure.diagnostic}",
            )
        return firing, None

    @staticmethod
    def _definition() -> ColoredPetriNetDefinition:
        """Build the private two-transition dependency definition."""
        color = ColoredPetriNetColorDefinition(
            ColoredPetriNetColorIdentity("workflow-result-identity"),
            (ColoredPetriNetValueKind.STRING,),
        )
        place_scf_input = ColoredPetriNetPlaceDefinition(
            ColoredPetriNetPlaceIdentity("scf.prepared"), (color.identity,)
        )
        place_bands_input = ColoredPetriNetPlaceDefinition(
            ColoredPetriNetPlaceIdentity("bands.prepared"), (color.identity,)
        )
        place_scf_output = ColoredPetriNetPlaceDefinition(
            ColoredPetriNetPlaceIdentity("scf.completed"), (color.identity,)
        )
        place_bands_output = ColoredPetriNetPlaceDefinition(
            ColoredPetriNetPlaceIdentity("bands.completed"), (color.identity,)
        )
        scf_input = ColoredPetriNetBindingVariableIdentity("scf_input")
        bands_input = ColoredPetriNetBindingVariableIdentity("bands_input")
        scf_output = ColoredPetriNetBindingVariableIdentity("scf_output")
        bands_output = ColoredPetriNetBindingVariableIdentity("bands_output")
        always = ColoredPetriNetGuardExpression(ColoredPetriNetGuardOperator.TRUE)
        scf_transition = ColoredPetriNetTransitionDefinition(
            ColoredPetriNetTransitionIdentity("dft.scf"),
            (scf_input,),
            (scf_output,),
            always,
        )
        bands_transition = ColoredPetriNetTransitionDefinition(
            ColoredPetriNetTransitionIdentity("dft.fixed-density-bands"),
            (scf_output, bands_input),
            (bands_output,),
            always,
        )

        def input_arc(
            identity: str,
            place: ColoredPetriNetPlaceDefinition,
            transition: ColoredPetriNetTransitionDefinition,
            variable: ColoredPetriNetBindingVariableIdentity,
            mode: ColoredPetriNetInputMode,
        ) -> ColoredPetriNetArcDefinition:
            return ColoredPetriNetArcDefinition(
                ColoredPetriNetArcIdentity(identity),
                place.identity,
                transition.identity,
                ColoredPetriNetInputInscription(
                    mode,
                    (ColoredPetriNetTokenPattern(variable, (color.identity,)),),
                ),
            )

        def output_arc(
            identity: str,
            place: ColoredPetriNetPlaceDefinition,
            transition: ColoredPetriNetTransitionDefinition,
            variable: ColoredPetriNetBindingVariableIdentity,
        ) -> ColoredPetriNetArcDefinition:
            expression = ColoredPetriNetValueExpression(
                ColoredPetriNetValueExpressionKind.VARIABLE,
                variable_identity=variable,
            )
            return ColoredPetriNetArcDefinition(
                ColoredPetriNetArcIdentity(identity),
                place.identity,
                transition.identity,
                output_inscription=ColoredPetriNetOutputInscription(
                    (
                        ColoredPetriNetTokenTemplate(
                            color.identity,
                            expression,
                            expression,
                        ),
                    )
                ),
            )

        arcs = (
            input_arc(
                "scf.input",
                place_scf_input,
                scf_transition,
                scf_input,
                ColoredPetriNetInputMode.CONSUME,
            ),
            output_arc("scf.output", place_scf_output, scf_transition, scf_output),
            input_arc(
                "bands.scf-state",
                place_scf_output,
                bands_transition,
                scf_output,
                ColoredPetriNetInputMode.READ,
            ),
            input_arc(
                "bands.input",
                place_bands_input,
                bands_transition,
                bands_input,
                ColoredPetriNetInputMode.CONSUME,
            ),
            output_arc(
                "bands.output",
                place_bands_output,
                bands_transition,
                bands_output,
            ),
        )
        return ColoredPetriNetDefinition(
            ColoredPetriNetDefinitionIdentity("dft.scf-to-fixed-density-bands.v1"),
            (color,),
            (
                place_scf_input,
                place_bands_input,
                place_scf_output,
                place_bands_output,
            ),
            (scf_transition, bands_transition),
            arcs,
            (scf_transition.identity, bands_transition.identity),
        )

    @staticmethod
    def _initial_marking(
        definition: ColoredPetriNetDefinition,
        replay_input: DftScfBandsCpnReplayInput,
    ) -> ColoredPetriNetMarking:
        """Build the exact initial marking from supplied operation inputs."""
        places = {item.identity.value: item.identity for item in definition.places}
        color = definition.colors[0].identity

        def token(value: str, identity: str) -> ColoredPetriNetToken:
            return ColoredPetriNetToken(
                color,
                ColoredPetriNetValue(ColoredPetriNetValueKind.STRING, value),
                ColoredPetriNetTokenIdentity(identity),
            )

        return ColoredPetriNetMarking(
            ColoredPetriNetMarkingIdentity("dft.scf-to-fixed-density-bands.initial"),
            definition.identity,
            (
                ColoredPetriNetPlaceMarking(
                    places["scf.prepared"],
                    (
                        token(
                            replay_input.scf_input_identity,
                            f"scf-input:{replay_input.scf_input_identity}",
                        ),
                    ),
                ),
                ColoredPetriNetPlaceMarking(
                    places["bands.prepared"],
                    (
                        token(
                            replay_input.bands_input_identity,
                            f"bands-input:{replay_input.bands_input_identity}",
                        ),
                    ),
                ),
                ColoredPetriNetPlaceMarking(places["scf.completed"], ()),
                ColoredPetriNetPlaceMarking(places["bands.completed"], ()),
            ),
        )
