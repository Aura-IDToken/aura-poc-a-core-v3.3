"""
Canonical event record and deterministic hashing utilities.
"""

from dataclasses import dataclass
import hashlib
import json
from typing import Dict, Any


CANONICAL_EVENT_FIELDS = (
    "event_id",
    "timestamp",
    "agent_id",
    "ari",
    "drift",
    "schema_valid",
    "engine_version",
    "policy_version",
)


@dataclass(frozen=True)
class CanonicalEvent:
    event_id: str
    timestamp: str
    agent_id: str
    ari: int
    drift: int
    schema_valid: bool
    engine_version: str
    policy_version: str

    def to_ordered_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp,
            "agent_id": self.agent_id,
            "ari": self.ari,
            "drift": self.drift,
            "schema_valid": self.schema_valid,
            "engine_version": self.engine_version,
            "policy_version": self.policy_version,
        }

    def to_canonical_json(self) -> str:
        return json.dumps(
            self.to_ordered_dict(),
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=False,
        )

    def to_canonical_bytes(self) -> bytes:
        return self.to_canonical_json().encode("utf-8")

    def canonical_hash(self) -> str:
        return hashlib.sha256(self.to_canonical_bytes()).hexdigest()

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "CanonicalEvent":
        missing = [field for field in CANONICAL_EVENT_FIELDS if field not in payload]
        if missing:
            raise ValueError(f"Missing canonical event fields: {', '.join(missing)}")

        return cls(
            event_id=str(payload["event_id"]),
            timestamp=str(payload["timestamp"]),
            agent_id=str(payload["agent_id"]),
            ari=int(payload["ari"]),
            drift=int(payload["drift"]),
            schema_valid=bool(payload["schema_valid"]),
            engine_version=str(payload["engine_version"]),
            policy_version=str(payload["policy_version"]),
        )

