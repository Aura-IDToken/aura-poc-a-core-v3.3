import random
import unittest

from audit.canonical import CanonicalEvent
from audit.pipeline import AuditLayerPipeline
from audit.verify import verify_event_trust_certificate
from audit.merkle import verify_proof


class TestAuditLayer(unittest.TestCase):
    def setUp(self):
        self.key = "audit-test-key"
        self.pipeline = AuditLayerPipeline(signing_key=self.key)

    def _event_payload(self, event_id: str, ari: int = 84562, drift: int = 312):
        return {
            "event_id": event_id,
            "timestamp": "2026-07-24T20:00:00Z",
            "agent_id": "machine-agent-1",
            "ari": ari,
            "drift": drift,
            "schema_valid": True,
            "engine_version": "3.3",
            "policy_version": "4.0",
        }

    def test_identical_event_same_hash(self):
        event = CanonicalEvent.from_dict(self._event_payload("evt-1"))
        hash_1 = event.canonical_hash()
        hash_2 = CanonicalEvent.from_dict(self._event_payload("evt-1")).canonical_hash()
        self.assertEqual(hash_1, hash_2)

    def test_single_bit_change_changes_hash(self):
        hash_1 = CanonicalEvent.from_dict(self._event_payload("evt-1")).canonical_hash()
        changed = self._event_payload("evt-1")
        changed["agent_id"] = "machine-agent-2"
        hash_2 = CanonicalEvent.from_dict(changed).canonical_hash()
        self.assertNotEqual(hash_1, hash_2)

    def test_valid_merkle_path_passes(self):
        for index in range(4):
            self.pipeline.append_and_certify(self._event_payload(f"evt-{index}"))

        result = self.pipeline.append_and_certify(self._event_payload("evt-4"))
        cert = result.certificate
        self.assertTrue(verify_proof(cert.canonical_hash, cert.merkle_proof, cert.merkle_root))

    def test_append_only_log_order(self):
        first = self.pipeline.append_and_certify(self._event_payload("evt-1"))
        second = self.pipeline.append_and_certify(self._event_payload("evt-2"))
        hashes = self.pipeline.event_log.hashes()
        self.assertEqual(len(hashes), 2)
        self.assertEqual(hashes[0], first.event.canonical_hash())
        self.assertEqual(hashes[1], second.event.canonical_hash())

    def test_corrupted_merkle_path_fails(self):
        result = self.pipeline.append_and_certify(self._event_payload("evt-1"))
        cert = result.certificate
        bad_proof = list(cert.merkle_proof)
        bad_proof[0] = ("0" * 64, bad_proof[0][1])
        self.assertFalse(verify_proof(cert.canonical_hash, bad_proof, cert.merkle_root))

    def test_modified_certificate_fails(self):
        result = self.pipeline.append_and_certify(self._event_payload("evt-1"))
        cert_payload = result.certificate.to_dict()
        cert_payload["ari"] = cert_payload["ari"] + 1
        self.assertFalse(verify_event_trust_certificate(result.event.to_ordered_dict(), cert_payload, self.key))

    def test_modified_signature_fails(self):
        result = self.pipeline.append_and_certify(self._event_payload("evt-1"))
        cert_payload = result.certificate.to_dict()
        cert_payload["signature"] = "f" * 64
        self.assertFalse(verify_event_trust_certificate(result.event.to_ordered_dict(), cert_payload, self.key))

    def test_modified_root_fails(self):
        result = self.pipeline.append_and_certify(self._event_payload("evt-1"))
        cert_payload = result.certificate.to_dict()
        cert_payload["merkle_root"] = "a" * 64
        self.assertFalse(verify_event_trust_certificate(result.event.to_ordered_dict(), cert_payload, self.key))

    def test_thousand_event_proofs_verify(self):
        rng = random.Random(1337)
        records = []

        for index in range(1000):
            payload = self._event_payload(
                event_id=f"evt-{index}",
                ari=rng.randint(0, 100000),
                drift=rng.randint(0, 100000),
            )
            payload["timestamp"] = f"2026-07-24T20:{index // 60:02d}:{index % 60:02d}Z"
            records.append(self.pipeline.append_and_certify(payload))

        self.assertEqual(len(self.pipeline.event_log), 1000)
        for record in records:
            self.assertTrue(
                verify_event_trust_certificate(
                    record.event.to_ordered_dict(),
                    record.certificate,
                    self.key,
                )
            )


if __name__ == "__main__":
    unittest.main()
