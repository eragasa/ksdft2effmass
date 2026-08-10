"""Independent evidence ownership and class/profile relation rules."""

from __future__ import annotations


def validate_owner_profile(
    mode: object, subject: object, evidence_profile: object
) -> tuple[str, str] | None:
    """Reject private class ownership and malformed explicit profile identity."""
    if mode == "class_owned" and isinstance(subject, str) and subject.startswith("_"):
        return (
            "TE.PRIVATE_CLASS_OWNER",
            "class_owned is limited to one public class as the sole system under test",
        )
    if evidence_profile is not None and evidence_profile not in {
        "routine",
        "claim_bearing",
    }:
        return ("TE.EVIDENCE_PROFILE", "evidence_profile is invalid")
    return None
