"""
Audit layer pipeline: canonical event -> hash log -> Merkle proof -> signed certificate.
"""

from dataclasses import dataclass
from typing import Dict

from .canonical import CanonicalEvent
from .event_log import AppendOnlyEventLog, EventLogEntry
from .merkle import MerkleTree
from .certificate import AuraEventTrustCertificate


@dataclass
class AuditPipelineResult:
    event: CanonicalEvent
    log_entry: EventLogEntry
    certificate: AuraEventTrustCertificate


class AuditLayerPipeline:
    def __init__(self, signing_key: str):
        self._signing_key = signing_key
        self._log = AppendOnlyEventLog()

    @property
    def event_log(self) -> AppendOnlyEventLog:
        return self._log

    def append_and_certify(self, event_payload: Dict) -> AuditPipelineResult:
        event = CanonicalEvent.from_dict(event_payload)
        event_hash = event.canonical_hash()
        log_entry = self._log.append(event_hash)

        tree = MerkleTree(list(self._log.hashes()), leaves_are_hashed=True)
        proof = tree.get_proof(log_entry.index)

        unsigned_certificate = AuraEventTrustCertificate(
            event_id=event.event_id,
            ari=event.ari,
            drift=event.drift,
            canonical_hash=event_hash,
            merkle_root=tree.get_root(),
            merkle_proof=proof,
            engine_version=event.engine_version,
            policy_version=event.policy_version,
            timestamp=event.timestamp,
        )
        certificate = unsigned_certificate.signed(self._signing_key)

        return AuditPipelineResult(
            event=event,
            log_entry=log_entry,
            certificate=certificate,
        )
