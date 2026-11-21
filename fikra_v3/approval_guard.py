"""Feature F: Approval Protection — SHA-256 cryptographic locks for approved project decisions."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any


class ApprovalLockedError(PermissionError):
    """Raised when attempting to modify or re-lock a locked user approval without explicit override."""


LOCKABLE_DECISIONS = ("idea", "script", "voiceover", "style", "character", "storyboard", "aspect_ratio")


def decision_digest(payload: Any) -> str:
    canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def lock_decision(
    state: dict[str, Any],
    key: str,
    value: Any,
    approved_by: str = "user",
    override_approved: bool = False,
    override_reason: str = "",
) -> dict[str, Any]:
    if key not in LOCKABLE_DECISIONS:
        raise ValueError(f"Unsupported lockable decision key: {key}")
    approvals = state.setdefault("approvals", {})
    existing = approvals.get(key)
    digest = decision_digest(value)

    if existing and existing.get("locked"):
        if existing.get("sha256") == digest:
            return existing
        if not override_approved or not override_reason.strip():
            raise ApprovalLockedError(
                f"Decision '{key}' is already locked (sha256={existing['sha256'][:12]}). "
                "Cannot overwrite via lock_decision() without override_approved=True and non-empty override_reason."
            )
        state.setdefault("audit_log", []).append({
            "action": "OVERRIDE_LOCKED_APPROVAL",
            "key": key,
            "approved_by": approved_by,
            "old_sha256": existing["sha256"],
            "new_sha256": digest,
            "old_value": existing.get("value"),
            "new_value": value,
            "reason": override_reason.strip(),
            "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        })

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    approvals[key] = {
        "locked": True,
        "approved_by": approved_by,
        "locked_at_utc": now,
        "sha256": digest,
        "value": value,
        "overridden": bool(existing and existing.get("locked")),
    }
    state.setdefault("decisions", {})[key] = value
    state.setdefault("audit_log", []).append({
        "action": "LOCK_APPROVAL",
        "key": key,
        "approved_by": approved_by,
        "sha256": digest,
        "timestamp_utc": now,
    })
    return approvals[key]


def update_decision(
    state: dict[str, Any],
    key: str,
    new_value: Any,
    override_approved: bool = False,
    override_reason: str = "",
    approved_by: str = "user",
) -> dict[str, Any]:
    approvals = state.get("approvals", {})
    existing = approvals.get(key)
    if existing and existing.get("locked"):
        lock_decision(
            state,
            key,
            new_value,
            approved_by=approved_by,
            override_approved=override_approved,
            override_reason=override_reason,
        )
        return state
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
