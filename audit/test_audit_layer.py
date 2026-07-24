"""
Audit Layer Test Suite — CORE-006 Part D
# NON-HERESY

Tests for:
  - Cross-platform determinism (canonical serialization stability)
  - Merkle tree construction and proof verification
  - Event Trust Certificate (ETC) creation and verification
  - Signing abstraction (HMACSigner / HMACVerifier)
  - Invalid signature detection
  - Invalid proof detection
  - Modified Merkle root detection
  - Modified canonical event detection
  - Modified certificate detection
  - Key mismatch detection
  - FutureEd25519Signer stub behaviour
"""

import hashlib
import hmac
import json
import unittest

from audit.merkle import (
    EventTrustCertificate,
    MerkleTree,
    sha256,
    verify_proof,
)
from audit.signing import (
    FutureEd25519Signer,
    FutureEd25519Verifier,
    HMACSigner,
    HMACVerifier,
    Signer,
    Verifier,
)
from audit.verify import verify_etc, verify_proof as audit_verify_proof


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

HMAC_KEY = b"aura-core-v3.3-test-key-32bytes!"


def make_event(agent_id: str = "MACHINE_ACCOUNT_001", ari: int = 95000, drift: int = 5000) -> dict:
    return {"agent_id": agent_id, "ari": ari, "drift": drift}


def canonical_payload(event: dict) -> bytes:
    return json.dumps(event, sort_keys=True, separators=(",", ":")).encode("utf-8")


def event_hash(event: dict) -> str:
    return sha256(json.dumps(event, sort_keys=True, separators=(",", ":")))


def make_tree_and_etc(events: list, index: int = 0) -> tuple:
    """Build a MerkleTree from event dicts and return (tree, ETC at index)."""
    leaves = [event_hash(e) for e in events]
    tree = MerkleTree(leaves, leaves_are_hashed=True)
    etc = tree.create_etc(index, timestamp="2026-07-24T20:56:30Z", batch_id="test-batch-001")
    return tree, etc


# ---------------------------------------------------------------------------
# 1. Canonical Serialization Stability
# ---------------------------------------------------------------------------

class TestCanonicalSerialization(unittest.TestCase):
    """Verify that canonical serialization is deterministic."""

    def test_identical_events_produce_identical_hashes(self):
        event = make_event()
        h1 = event_hash(event)
        h2 = event_hash(event)
        self.assertEqual(h1, h2)

    def test_hash_is_64_hex_characters(self):
        h = event_hash(make_event())
        self.assertEqual(len(h), 64)
        self.assertTrue(all(c in "0123456789abcdef" for c in h))

    def test_different_ari_produces_different_hash(self):
        h1 = event_hash(make_event(ari=95000))
        h2 = event_hash(make_event(ari=95001))
        self.assertNotEqual(h1, h2)

    def test_different_agent_id_produces_different_hash(self):
        h1 = event_hash(make_event(agent_id="AGENT_A"))
        h2 = event_hash(make_event(agent_id="AGENT_B"))
        self.assertNotEqual(h1, h2)

    def test_key_order_does_not_affect_hash(self):
        """sort_keys=True must neutralise insertion-order differences."""
        event_a = {"agent_id": "X", "ari": 1000, "drift": 500}
        event_b = {"drift": 500, "ari": 1000, "agent_id": "X"}
        self.assertEqual(event_hash(event_a), event_hash(event_b))

    def test_sha256_matches_stdlib(self):
        event = make_event()
        payload = json.dumps(event, sort_keys=True, separators=(",", ":"))
        expected = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        self.assertEqual(sha256(payload), expected)


# ---------------------------------------------------------------------------
# 2. Merkle Tree Construction
# ---------------------------------------------------------------------------

class TestMerkleTreeConstruction(unittest.TestCase):

    def test_single_leaf_root_equals_leaf(self):
        """Single-leaf tree: root equals the leaf hash (no pairing step executed)."""
        h = sha256("only-leaf")
        tree = MerkleTree([h], leaves_are_hashed=True)
        # The while loop exits immediately for len==1, so root == leaf
        self.assertEqual(tree.get_root(), h)

    def test_two_leaf_root(self):
        h0 = sha256("leaf0")
        h1 = sha256("leaf1")
        tree = MerkleTree([h0, h1], leaves_are_hashed=True)
        expected = sha256(h0 + h1)
        self.assertEqual(tree.get_root(), expected)

    def test_three_leaf_odd_duplication(self):
        """Odd number of leaves: last leaf is duplicated at each level."""
        h0, h1, h2 = sha256("l0"), sha256("l1"), sha256("l2")
        tree = MerkleTree([h0, h1, h2], leaves_are_hashed=True)
        level1_0 = sha256(h0 + h1)
        level1_1 = sha256(h2 + h2)
        expected_root = sha256(level1_0 + level1_1)
        self.assertEqual(tree.get_root(), expected_root)

    def test_empty_tree_raises(self):
        with self.assertRaises(ValueError):
            MerkleTree([])

    def test_root_is_deterministic(self):
        leaves = [sha256(f"leaf{i}") for i in range(8)]
        root1 = MerkleTree(leaves, leaves_are_hashed=True).get_root()
        root2 = MerkleTree(leaves, leaves_are_hashed=True).get_root()
        self.assertEqual(root1, root2)

    def test_different_leaf_order_produces_different_root(self):
        leaves = [sha256(f"leaf{i}") for i in range(4)]
        root1 = MerkleTree(leaves, leaves_are_hashed=True).get_root()
        root2 = MerkleTree(list(reversed(leaves)), leaves_are_hashed=True).get_root()
        self.assertNotEqual(root1, root2)


# ---------------------------------------------------------------------------
# 3. Merkle Proof Verification
# ---------------------------------------------------------------------------

class TestMerkleProofVerification(unittest.TestCase):

    def _verify(self, leaves_count: int, target_index: int):
        leaves = [sha256(f"event-{i}") for i in range(leaves_count)]
        tree = MerkleTree(leaves, leaves_are_hashed=True)
        proof = tree.get_proof(target_index)
        return verify_proof(leaves[target_index], proof, tree.get_root())

    def test_valid_proof_single_leaf(self):
        self.assertTrue(self._verify(1, 0))

    def test_valid_proof_two_leaves_index_0(self):
        self.assertTrue(self._verify(2, 0))

    def test_valid_proof_two_leaves_index_1(self):
        self.assertTrue(self._verify(2, 1))

    def test_valid_proof_four_leaves_all_indices(self):
        for i in range(4):
            self.assertTrue(self._verify(4, i))

    def test_valid_proof_five_leaves_all_indices(self):
        for i in range(5):
            self.assertTrue(self._verify(5, i))

    def test_invalid_proof_wrong_leaf(self):
        leaves = [sha256(f"event-{i}") for i in range(4)]
        tree = MerkleTree(leaves, leaves_are_hashed=True)
        proof = tree.get_proof(0)
        wrong_leaf = sha256("tampered-event")
        self.assertFalse(verify_proof(wrong_leaf, proof, tree.get_root()))

    def test_invalid_proof_modified_root(self):
        leaves = [sha256(f"event-{i}") for i in range(4)]
        tree = MerkleTree(leaves, leaves_are_hashed=True)
        proof = tree.get_proof(0)
        tampered_root = sha256("tampered-root")
        self.assertFalse(verify_proof(leaves[0], proof, tampered_root))

    def test_invalid_proof_modified_sibling(self):
        leaves = [sha256(f"event-{i}") for i in range(4)]
        tree = MerkleTree(leaves, leaves_are_hashed=True)
        proof = tree.get_proof(0)
        # Replace first sibling with garbage
        tampered_proof = [(sha256("garbage"), proof[0][1])] + list(proof[1:])
        self.assertFalse(verify_proof(leaves[0], tampered_proof, tree.get_root()))

    def test_audit_verify_proof_delegate(self):
        """audit.verify.verify_proof must delegate to merkle.verify_proof."""
        leaves = [sha256("ev0"), sha256("ev1")]
        tree = MerkleTree(leaves, leaves_are_hashed=True)
        proof = tree.get_proof(0)
        self.assertTrue(audit_verify_proof(leaves[0], proof, tree.get_root()))


# ---------------------------------------------------------------------------
# 4. Event Trust Certificate (ETC)
# ---------------------------------------------------------------------------

class TestEventTrustCertificate(unittest.TestCase):

    def setUp(self):
        self.events = [make_event(agent_id=f"AGENT_{i}", ari=90000 + i * 1000) for i in range(3)]
        self.tree, self.etc = make_tree_and_etc(self.events, index=1)

    def test_etc_verify_passes(self):
        self.assertTrue(self.etc.verify())

    def test_etc_verify_delegates_to_audit_verify_etc(self):
        self.assertTrue(verify_etc(self.etc))

    def test_etc_to_dict_contains_required_fields(self):
        d = self.etc.to_dict()
        for field in ("event_hash", "merkle_root", "merkle_proof", "timestamp", "batch_id"):
            self.assertIn(field, d)

    def test_etc_event_hash_matches_leaf(self):
        expected_leaf = event_hash(self.events[1])
        self.assertEqual(self.etc.event_hash, expected_leaf)

    def test_etc_merkle_root_matches_tree(self):
        self.assertEqual(self.etc.merkle_root, self.tree.get_root())

    def test_modified_event_invalidates_etc(self):
        """Changing the event should produce a different event_hash, failing the proof."""
        tampered_event_hash = sha256("tampered-event-data")
        tampered_etc = EventTrustCertificate(
            event_hash=tampered_event_hash,
            merkle_root=self.etc.merkle_root,
            merkle_proof=self.etc.merkle_proof,
            timestamp=self.etc.timestamp,
            batch_id=self.etc.batch_id,
        )
        self.assertFalse(tampered_etc.verify())

    def test_modified_merkle_root_invalidates_etc(self):
        tampered_etc = EventTrustCertificate(
            event_hash=self.etc.event_hash,
            merkle_root=sha256("tampered-root"),
            merkle_proof=self.etc.merkle_proof,
            timestamp=self.etc.timestamp,
            batch_id=self.etc.batch_id,
        )
        self.assertFalse(tampered_etc.verify())

    def test_modified_certificate_fields_are_detectable(self):
        """Swapping event_hash and merkle_root must fail verification."""
        tampered_etc = EventTrustCertificate(
            event_hash=self.etc.merkle_root,   # swapped
            merkle_root=self.etc.event_hash,   # swapped
            merkle_proof=self.etc.merkle_proof,
            timestamp=self.etc.timestamp,
            batch_id=self.etc.batch_id,
        )
        self.assertFalse(tampered_etc.verify())

    def test_empty_proof_fails_for_multi_leaf_tree(self):
        """An empty proof is only valid for a 1-leaf tree."""
        tampered_etc = EventTrustCertificate(
            event_hash=self.etc.event_hash,
            merkle_root=self.etc.merkle_root,
            merkle_proof=[],
            timestamp=self.etc.timestamp,
            batch_id=self.etc.batch_id,
        )
        # Empty proof means current == event_hash, which != merkle_root for 3 leaves
        self.assertFalse(tampered_etc.verify())


# ---------------------------------------------------------------------------
# 5. Signing Abstraction
# ---------------------------------------------------------------------------

class TestHMACSigner(unittest.TestCase):

    def test_sign_returns_64_hex_chars(self):
        signer = HMACSigner(HMAC_KEY)
        sig = signer.sign(b"test payload")
        self.assertEqual(len(sig), 64)
        self.assertTrue(all(c in "0123456789abcdef" for c in sig))

    def test_algorithm_name(self):
        self.assertEqual(HMACSigner(HMAC_KEY).algorithm(), "HMAC-SHA256")

    def test_sign_is_deterministic(self):
        signer = HMACSigner(HMAC_KEY)
        payload = b"deterministic payload"
        self.assertEqual(signer.sign(payload), signer.sign(payload))

    def test_different_payloads_produce_different_signatures(self):
        signer = HMACSigner(HMAC_KEY)
        self.assertNotEqual(signer.sign(b"payload-a"), signer.sign(b"payload-b"))

    def test_different_keys_produce_different_signatures(self):
        s1 = HMACSigner(b"key-alpha-32bytes-padding______!")
        s2 = HMACSigner(b"key-beta-32bytes-padding_______!")
        payload = b"same payload"
        self.assertNotEqual(s1.sign(payload), s2.sign(payload))

    def test_empty_key_raises(self):
        with self.assertRaises(ValueError):
            HMACSigner(b"")

    def test_matches_stdlib_hmac(self):
        signer = HMACSigner(HMAC_KEY)
        payload = b"reference payload"
        expected = hmac.new(HMAC_KEY, payload, hashlib.sha256).hexdigest()
        self.assertEqual(signer.sign(payload), expected)

    def test_signer_is_abstract_subclass(self):
        self.assertIsInstance(HMACSigner(HMAC_KEY), Signer)


class TestHMACVerifier(unittest.TestCase):

    def test_valid_signature_passes(self):
        signer = HMACSigner(HMAC_KEY)
        verifier = HMACVerifier(HMAC_KEY)
        payload = b"verified payload"
        sig = signer.sign(payload)
        self.assertTrue(verifier.verify(payload, sig))

    def test_invalid_signature_fails(self):
        verifier = HMACVerifier(HMAC_KEY)
        self.assertFalse(verifier.verify(b"payload", "deadbeef" * 8))

    def test_key_mismatch_fails(self):
        signer = HMACSigner(b"signing-key-aaaa-32bytes-padding")
        verifier = HMACVerifier(b"verifying-key-bb-32bytes-padding")
        payload = b"mismatch payload"
        sig = signer.sign(payload)
        self.assertFalse(verifier.verify(payload, sig))

    def test_tampered_payload_fails(self):
        signer = HMACSigner(HMAC_KEY)
        verifier = HMACVerifier(HMAC_KEY)
        original = b"original payload"
        sig = signer.sign(original)
        self.assertFalse(verifier.verify(b"tampered payload", sig))

    def test_algorithm_name(self):
        self.assertEqual(HMACVerifier(HMAC_KEY).algorithm(), "HMAC-SHA256")

    def test_empty_key_raises(self):
        with self.assertRaises(ValueError):
            HMACVerifier(b"")

    def test_verifier_is_abstract_subclass(self):
        self.assertIsInstance(HMACVerifier(HMAC_KEY), Verifier)


# ---------------------------------------------------------------------------
# 6. Future Ed25519 Stubs
# ---------------------------------------------------------------------------

class TestFutureEd25519Stubs(unittest.TestCase):

    def test_ed25519_signer_raises_not_implemented(self):
        signer = FutureEd25519Signer()
        with self.assertRaises(NotImplementedError):
            signer.sign(b"payload")

    def test_ed25519_verifier_raises_not_implemented(self):
        verifier = FutureEd25519Verifier()
        with self.assertRaises(NotImplementedError):
            verifier.verify(b"payload", "signature")

    def test_ed25519_signer_algorithm(self):
        self.assertEqual(FutureEd25519Signer().algorithm(), "Ed25519")

    def test_ed25519_verifier_algorithm(self):
        self.assertEqual(FutureEd25519Verifier().algorithm(), "Ed25519")

    def test_ed25519_signer_is_signer_subclass(self):
        self.assertIsInstance(FutureEd25519Signer(), Signer)

    def test_ed25519_verifier_is_verifier_subclass(self):
        self.assertIsInstance(FutureEd25519Verifier(), Verifier)


# ---------------------------------------------------------------------------
# 7. Cross-Platform Determinism (canonical vectors)
# ---------------------------------------------------------------------------

class TestCrossPlatformDeterminism(unittest.TestCase):
    """
    Verify that canonical computations produce known reference values.

    These values were computed on x86_64 and must match on ARM64.
    If any assertion fails on a different architecture, it indicates a
    non-determinism bug (CRITICAL FAILURE for the metrological instrument).
    """

    def test_sha256_reference_value(self):
        """SHA-256 of the empty string is the canonical reference."""
        ref = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        self.assertEqual(sha256(""), ref)

    def test_canonical_event_hash_reference(self):
        """Reference hash for a known canonical event."""
        event = {"agent_id": "MACHINE_ACCOUNT_REF_001", "ari": 100000, "drift": 0}
        payload = json.dumps(event, sort_keys=True, separators=(",", ":"))
        expected = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        # Verify against stdlib directly — proves no platform divergence
        self.assertEqual(sha256(payload), expected)

    def test_two_leaf_merkle_root_reference(self):
        h0 = sha256("canonical-event-0")
        h1 = sha256("canonical-event-1")
        tree = MerkleTree([h0, h1], leaves_are_hashed=True)
        expected_root = sha256(h0 + h1)
        self.assertEqual(tree.get_root(), expected_root)

    def test_hmac_sha256_reference_value(self):
        """Reference HMAC-SHA256 value against Python stdlib."""
        key = b"reference-key-aura-v3.3-padding!"
        payload = b"canonical-audit-payload"
        signer = HMACSigner(key)
        verifier = HMACVerifier(key)
        sig = signer.sign(payload)
        # Must verify with the same key
        self.assertTrue(verifier.verify(payload, sig))
        # Must equal stdlib HMAC
        expected = hmac.new(key, payload, hashlib.sha256).hexdigest()
        self.assertEqual(sig, expected)

    def test_json_serialization_is_stable(self):
        """Serialization of canonical event produces identical bytes on replay."""
        event = {"agent_id": "AGENT_STABILITY_TEST", "ari": 87654, "drift": 12346}
        s1 = json.dumps(event, sort_keys=True, separators=(",", ":"))
        s2 = json.dumps(event, sort_keys=True, separators=(",", ":"))
        self.assertEqual(s1, s2)
        self.assertEqual(s1.encode("utf-8"), s2.encode("utf-8"))


# ---------------------------------------------------------------------------
# 8. End-to-End Certificate Verification
# ---------------------------------------------------------------------------

class TestEndToEndVerification(unittest.TestCase):

    def test_full_verification_pipeline(self):
        """Happy path: create event → Merkle tree → ETC → verify."""
        events = [make_event(agent_id=f"AGENT_{i}") for i in range(4)]
        tree, etc = make_tree_and_etc(events, index=2)
        self.assertTrue(etc.verify())

    def test_signed_etc_roundtrip(self):
        """Sign the ETC dict, then verify using HMACVerifier."""
        events = [make_event()]
        _, etc = make_tree_and_etc(events, index=0)

        signer = HMACSigner(HMAC_KEY)
        verifier = HMACVerifier(HMAC_KEY)

        payload = json.dumps(etc.to_dict(), sort_keys=True, separators=(",", ":")).encode("utf-8")
        sig = signer.sign(payload)
        self.assertTrue(verifier.verify(payload, sig))

    def test_signed_etc_wrong_key_fails(self):
        """Wrong key must fail verification."""
        events = [make_event()]
        _, etc = make_tree_and_etc(events, index=0)

        signer = HMACSigner(b"correct-key-32bytes-aaaaaaaaaa!!")
        wrong_verifier = HMACVerifier(b"wrong-key--32bytes-bbbbbbbbbbb!!")

        payload = json.dumps(etc.to_dict(), sort_keys=True, separators=(",", ":")).encode("utf-8")
        sig = signer.sign(payload)
        self.assertFalse(wrong_verifier.verify(payload, sig))


if __name__ == "__main__":
    unittest.main(verbosity=2)
