"""
Event Trust Certificate model with canonical payload hashing and signature.
"""

from dataclasses import dataclass
import hashlib
import json
from typing import List, Tuple, Dict, Any

from .signature import (
    SIGNATURE_ALGORITHM,
    sign_canonical_hash,
    verify_canonical_hash_signature,
)


@dataclass(frozen=True)
class AuraEventTrustCertificate:
    event_id: str
    ari: int
    drift: int
    canonical_hash: str
    merkle_root: str
    merkle_proof: List[Tuple[str, str]]
    engine_version: str
    policy_version: str
    timestamp: str
    signature: str = ""
    signature_algorithm: str = SIGNATURE_ALGORITHM

    def payload_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "ari": self.ari,
            "drift": self.drift,
            "canonical_hash": self.canonical_hash,
            "merkle_root": self.merkle_root,
            "merkle_proof": [
                {"sibling": sibling, "direction": direction}
                for sibling, direction in self.merkle_proof
            ],
            "engine_version": self.engine_version,
            "policy_version": self.policy_version,
            "timestamp": self.timestamp,
        }

    def to_dict(self) -> Dict[str, Any]:
        payload = self.payload_dict()
        payload["signature_algorithm"] = self.signature_algorithm
        payload["signature"] = self.signature
        return payload

    def canonical_payload_json(self) -> str:
        return json.dumps(
            self.payload_dict(),
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )

    def canonical_payload_hash(self) -> str:
        return hashlib.sha256(self.canonical_payload_json().encode("utf-8")).hexdigest()

    def signed(self, signing_key: str) -> "AuraEventTrustCertificate":
        return AuraEventTrustCertificate(
            event_id=self.event_id,
            ari=self.ari,
            drift=self.drift,
            canonical_hash=self.canonical_hash,
            merkle_root=self.merkle_root,
            merkle_proof=self.merkle_proof,
            engine_version=self.engine_version,
            policy_version=self.policy_version,
            timestamp=self.timestamp,
            signature=sign_canonical_hash(self.canonical_payload_hash(), signing_key),
            signature_algorithm=self.signature_algorithm,
        )

    def verify_signature(self, verification_key: str) -> bool:
        if not self.signature:
            return False
        return verify_canonical_hash_signature(
            self.canonical_payload_hash(),
            self.signature,
            verification_key,
        )

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "AuraEventTrustCertificate":
        proof = [
            (item["sibling"], item["direction"])
            for item in payload["merkle_proof"]
        ]
        return cls(
            event_id=payload["event_id"],
            ari=int(payload["ari"]),
            drift=int(payload["drift"]),
            canonical_hash=payload["canonical_hash"],
            merkle_root=payload["merkle_root"],
            merkle_proof=proof,
            engine_version=payload["engine_version"],
            policy_version=payload["policy_version"],
            timestamp=payload["timestamp"],
            signature=payload.get("signature", ""),
            signature_algorithm=payload.get("signature_algorithm", SIGNATURE_ALGORITHM),
        )
