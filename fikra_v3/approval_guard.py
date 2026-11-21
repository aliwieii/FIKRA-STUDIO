"""Feature F: Approval Protection — SHA-256 cryptographic locks for approved project decisions."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any


class ApprovalLockedError(PermissionError):
    """Raised when attempting to modify a locked user approval without explicit override."""


LOCKABLE_DECISIONS = ("idea", "script", "voiceover", "style", "character", "storyboard", "aspect_ratio")


def decision_digest(payload: Any) -> str:
    canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def lock_decision(state: dict[str, Any], key: str, value: Any, approved_by: str = "user") -> dict[str, Any]:
    if key not in LOCKABLE_DECISIONS:
        raise ValueError(f"Unsupported lockable decision key: {key}")
    approvals = state.setdefault("approvals", {})
    digest = decision_digest(value)
    approvals[key] = {
        "locked": True,
        "approved_by": approved_by,
        "locked_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "sha256": digest,
        "value": value,
    }
    state.setdefault("decisions", {})[key] = value
    state.setdefault("audit_log", []).append({
        "action": "LOCK_APPROVAL",
        "key": key,
        "sha256": digest,
        "timestamp_utc": approvals[key]["locked_at_utc"],
    })
    return approvals[key]


def update_decision(
    state: dict[str, Any],
    key: str,
    new_value: Any,
    override_approved: bool = False,
    override_reason: str = "",
) -> dict[str, Any]:
    approvals = state.get("approvals", {})
    existing = approvals.get(key)
    if existing and existing.get("locked"):
        new_digest = decision_digest(new_value)
        if new_digest == existing.get("sha256"):
            return state
        if not override_approved or not override_reason.strip():
            raise ApprovalLockedError(
                f"Decision '{key}' is locked (sha256={existing['sha256'][:12]}). "
                "Explicit user override (override_approved=True + override_reason) is required."
            )
        state.setdefault("audit_log", []).append({
            "action": "OVERRIDE_LOCKED_APPROVAL",
            "key": key,
            "old_sha256": existing["sha256"],
            "new_sha256": new_digest,
            "reason": override_reason.strip(),
            "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        })
        existing["sha256"] = new_digest
        existing["value"] = new_value
        existing["overridden"] = True

    state.setdefault("decisions", {})[key] = new_value
    return state


def verify_approval_integrity(state: dict[str, Any]) -> dict[str, Any]:
    tampered = []
    verified = []
    for key, lock in state.get("approvals", {}).items():
        if not lock.get("locked"):
            continue
        current_val = state.get("decisions", {}).get(key)
        if decision_digest(current_val) != lock.get("sha256"):
            tampered.append(key)
        else:
            verified.append(key)
    return {
        "valid": len(tampered) == 0,
        "verified_locks": verified,
        "tampered_locks": tampered,
    }
