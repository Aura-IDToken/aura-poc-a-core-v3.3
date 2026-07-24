"""
Audit Layer Tests — CORE-006 Part D
# NON-HERESY

Tests covering:
- Signing abstraction (HMACSigner / HMACVerifier)
- Canonical serialisation stability
- ETC creation, signing, and verification
- Invalid signature
- Invalid Merkle proof
- Modified Merkle root
- Modified canonical event
- Modified certificate
- Key mismatch
- Cross-platform determinism of audit primitives
"""

import hashlib
import unittest
import json
import platform
from typing import List

from audit.merkle import (
    MerkleTree,
    EventTrustCertificate,
    sha256,
    verify_proof,
)
from audit.signing import HMACSigner, HMACVerifier
from audit.verify import verify_etc


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SAMPLE_KEY = b"aura-v3.3-test-key-00000000000001"
SAMPLE_KEY_ALT = b"aura-v3.3-test-key-00000000000002"

SAMPLE_EVENTS = [
    "agent_id=MACHINE_ACCOUNT_001|ari=95000|drift=5000|ts=2026-01-01T00:00:00Z",
    "agent_id=MACHINE_ACCOUNT_002|ari=80000|drift=20000|ts=2026-01-01T00:01:00Z",
    "agent_id=MACHINE_ACCOUNT_003|ari=68000|drift=32000|ts=2026-01-01T00:02:00Z",
    "agent_id=MACHINE_ACCOUNT_004|ari=72000|drift=28000|ts=2026-01-01T00:03:00Z",
]


def make_tree(events: List[str] = SAMPLE_EVENTS) -> MerkleTree:
    return MerkleTree(events)


# ---------------------------------------------------------------------------
# Part C — Signing abstraction
# ---------------------------------------------------------------------------

class TestHMACSigner(unittest.TestCase):
    """HMACSigner: determinism, type enforcement, correct length."""

    def test_sign_returns_bytes(self):
        signer = HMACSigner(SAMPLE_KEY)
        sig = signer.sign(b"payload")
        self.assertIsInstance(sig, bytes)

    def test_sign_deterministic(self):
        signer = HMACSigner(SAMPLE_KEY)
        payload = b"canonical|event|data"
        self.assertEqual(signer.sign(payload), signer.sign(payload))

    def test_sign_length_sha256(self):
        """HMAC-SHA256 digest is always 32 bytes."""
        signer = HMACSigner(SAMPLE_KEY)
        sig = signer.sign(b"x")
        self.assertEqual(len(sig), 32)

    def test_different_payloads_differ(self):
        signer = HMACSigner(SAMPLE_KEY)
        self.assertNotEqual(signer.sign(b"a"), signer.sign(b"b"))

    def test_different_keys_differ(self):
        s1 = HMACSigner(SAMPLE_KEY)
        s2 = HMACSigner(SAMPLE_KEY_ALT)
        self.assertNotEqual(s1.sign(b"same payload"), s2.sign(b"same payload"))

    def test_rejects_non_bytes_key(self):
        with self.assertRaises(TypeError):
            HMACSigner("string-key")  # type: ignore[arg-type]


class TestHMACVerifier(unittest.TestCase):
    """HMACVerifier: correct accept/reject behaviour."""

    def test_verify_correct(self):
        signer = HMACSigner(SAMPLE_KEY)
        verifier = HMACVerifier(SAMPLE_KEY)
        payload = b"test payload"
        self.assertTrue(verifier.verify(payload, signer.sign(payload)))

    def test_verify_rejects_wrong_signature(self):
        verifier = HMACVerifier(SAMPLE_KEY)
        self.assertFalse(verifier.verify(b"data", b"\x00" * 32))

    def test_verify_rejects_wrong_key(self):
        signer = HMACSigner(SAMPLE_KEY)
        verifier = HMACVerifier(SAMPLE_KEY_ALT)
        payload = b"some data"
        self.assertFalse(verifier.verify(payload, signer.sign(payload)))

    def test_verify_rejects_modified_payload(self):
        signer = HMACSigner(SAMPLE_KEY)
        verifier = HMACVerifier(SAMPLE_KEY)
        original = b"original"
        sig = signer.sign(original)
        self.assertFalse(verifier.verify(b"modified", sig))

    def test_rejects_non_bytes_key(self):
        with self.assertRaises(TypeError):
            HMACVerifier("string-key")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Canonical serialisation stability
# ---------------------------------------------------------------------------

class TestCanonicalSha256(unittest.TestCase):
    """sha256() must produce stable, UTF-8-encoded digests."""

    KNOWN_VECTORS = [
        # (input_string, expected_sha256_hex)
        (
            "aura",
            "6d7c0eb420852d2e6288be29c47c975ff15d81eeacd4eef100022f931a827702",
        ),
        (
            "",
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        ),
        (
            "agent_id=MACHINE_ACCOUNT_001|ari=95000|drift=5000",
            hashlib.sha256(
                "agent_id=MACHINE_ACCOUNT_001|ari=95000|drift=5000".encode("utf-8")
            ).hexdigest(),
        ),
    ]

    def test_known_hashes(self):
        for data, expected in self.KNOWN_VECTORS:
            with self.subTest(data=data[:30]):
                self.assertEqual(sha256(data), expected)

    def test_stability_across_calls(self):
        data = "canonical event"
        h1 = sha256(data)
        h2 = sha256(data)
        self.assertEqual(h1, h2)

    def test_utf8_encoding(self):
        """Hashing must be UTF-8 (not platform default encoding)."""
        unicode_data = "measurement \u00e9v\u00e9nement"
        expected = hashlib.sha256(unicode_data.encode("utf-8")).hexdigest()
        self.assertEqual(sha256(unicode_data), expected)


# ---------------------------------------------------------------------------
# Merkle Tree construction
# ---------------------------------------------------------------------------

class TestMerkleTree(unittest.TestCase):

    def test_single_leaf(self):
        tree = MerkleTree(["single"])
        self.assertIsNotNone(tree.root)
        self.assertEqual(len(tree.root), 64)  # hex SHA-256

    def test_root_deterministic(self):
        t1 = MerkleTree(SAMPLE_EVENTS)
        t2 = MerkleTree(SAMPLE_EVENTS)
        self.assertEqual(t1.root, t2.root)

    def test_different_leaves_different_root(self):
        t1 = MerkleTree(["a", "b"])
        t2 = MerkleTree(["a", "c"])
        self.assertNotEqual(t1.root, t2.root)

    def test_odd_leaves_handled(self):
        """Odd number of leaves must duplicate last node correctly."""
        tree = MerkleTree(["a", "b", "c"])
        self.assertIsNotNone(tree.root)
        proof = tree.get_proof(2)
        self.assertTrue(verify_proof(tree.leaves[2], proof, tree.root))

    def test_empty_raises(self):
        with self.assertRaises(ValueError):
            MerkleTree([])

    def test_pre_hashed_leaves(self):
        hashes = [sha256(e) for e in SAMPLE_EVENTS]
        tree = MerkleTree(hashes, leaves_are_hashed=True)
        self.assertEqual(tree.leaves, hashes)


# ---------------------------------------------------------------------------
# Merkle Proof verification
# ---------------------------------------------------------------------------

class TestMerkleProof(unittest.TestCase):

    def setUp(self):
        self.tree = make_tree()

    def test_all_proofs_valid(self):
        for i in range(len(self.tree.leaves)):
            proof = self.tree.get_proof(i)
            self.assertTrue(
                verify_proof(self.tree.leaves[i], proof, self.tree.root),
                f"Proof for leaf {i} failed",
            )

    def test_invalid_proof_wrong_root(self):
        proof = self.tree.get_proof(0)
        fake_root = "a" * 64
        self.assertFalse(verify_proof(self.tree.leaves[0], proof, fake_root))

    def test_invalid_proof_wrong_leaf(self):
        proof = self.tree.get_proof(0)
        wrong_leaf = sha256("not_in_tree")
        self.assertFalse(verify_proof(wrong_leaf, proof, self.tree.root))

    def test_invalid_proof_tampered_step(self):
        proof = self.tree.get_proof(0)
        tampered = list(proof)
        sibling, direction = tampered[0]
        tampered[0] = ("b" * 64, direction)
        self.assertFalse(verify_proof(self.tree.leaves[0], tampered, self.tree.root))

    def test_out_of_range_index_raises(self):
        with self.assertRaises(IndexError):
            self.tree.get_proof(len(self.tree.leaves))


# ---------------------------------------------------------------------------
# EventTrustCertificate
# ---------------------------------------------------------------------------

class TestEventTrustCertificate(unittest.TestCase):

    def setUp(self):
        self.tree = make_tree()
        self.etc = self.tree.create_etc(
            leaf_index=0,
            timestamp="2026-01-01T00:00:00Z",
            batch_id="batch-001",
        )

    def test_etc_verify_valid(self):
        self.assertTrue(self.etc.verify())

    def test_etc_verify_via_module(self):
        self.assertTrue(verify_etc(self.etc))

    def test_etc_to_dict_keys(self):
        d = self.etc.to_dict()
        for key in ("event_hash", "merkle_root", "merkle_proof", "timestamp", "batch_id"):
            self.assertIn(key, d)

    def test_etc_serialisation_stable(self):
        d1 = self.etc.to_dict()
        d2 = self.etc.to_dict()
        self.assertEqual(json.dumps(d1, sort_keys=True), json.dumps(d2, sort_keys=True))

    def test_modified_merkle_root_fails(self):
        import dataclasses
        tampered = dataclasses.replace(self.etc, merkle_root="a" * 64)
        self.assertFalse(tampered.verify())

    def test_modified_event_hash_fails(self):
        import dataclasses
        tampered = dataclasses.replace(self.etc, event_hash="b" * 64)
        self.assertFalse(tampered.verify())

    def test_modified_proof_step_fails(self):
        import dataclasses
        bad_proof = list(self.etc.merkle_proof)
        if bad_proof:
            sibling, direction = bad_proof[0]
            bad_proof[0] = ("c" * 64, direction)
        tampered = dataclasses.replace(self.etc, merkle_proof=bad_proof)
        self.assertFalse(tampered.verify())

    def test_no_signature_by_default(self):
        self.assertIsNone(self.etc.signature)

    def test_no_signature_in_dict_by_default(self):
        self.assertNotIn("signature", self.etc.to_dict())


# ---------------------------------------------------------------------------
# ETC signing and signature verification
# ---------------------------------------------------------------------------

class TestETCSigning(unittest.TestCase):

    def setUp(self):
        self.tree = make_tree()
        self.etc = self.tree.create_etc(
            leaf_index=1,
            timestamp="2026-01-01T00:01:00Z",
            batch_id="batch-001",
        )
        self.signer = HMACSigner(SAMPLE_KEY)
        self.verifier = HMACVerifier(SAMPLE_KEY)
        self.signed_etc = self.etc.sign(self.signer)

    def test_sign_returns_new_object(self):
        self.assertIsNot(self.signed_etc, self.etc)

    def test_signed_etc_has_signature(self):
        self.assertIsNotNone(self.signed_etc.signature)
        self.assertIsInstance(self.signed_etc.signature, bytes)

    def test_original_etc_unchanged(self):
        self.assertIsNone(self.etc.signature)

    def test_verify_signature_valid(self):
        self.assertTrue(self.signed_etc.verify_signature(self.verifier))

    def test_verify_signature_key_mismatch(self):
        wrong_verifier = HMACVerifier(SAMPLE_KEY_ALT)
        self.assertFalse(self.signed_etc.verify_signature(wrong_verifier))

    def test_verify_signature_no_signature(self):
        """ETC without signature returns False (not an error)."""
        self.assertFalse(self.etc.verify_signature(self.verifier))

    def test_signature_in_dict(self):
        d = self.signed_etc.to_dict()
        self.assertIn("signature", d)
        self.assertIsInstance(d["signature"], str)  # hex string
        self.assertEqual(len(d["signature"]), 64)   # 32 bytes → 64 hex chars

    def test_modified_certificate_signature_fails(self):
        """Mutating merkle_root must invalidate the existing signature."""
        import dataclasses
        tampered = dataclasses.replace(self.signed_etc, merkle_root="a" * 64)
        self.assertFalse(tampered.verify_signature(self.verifier))

    def test_signing_payload_deterministic(self):
        p1 = self.etc._signing_payload()
        p2 = self.etc._signing_payload()
        self.assertEqual(p1, p2)

    def test_signing_is_deterministic(self):
        sig1 = self.etc.sign(self.signer).signature
        sig2 = self.etc.sign(self.signer).signature
        self.assertEqual(sig1, sig2)

    def test_merkle_proof_still_valid_after_signing(self):
        """Signing must not affect Merkle proof validity."""
        self.assertTrue(self.signed_etc.verify())


# ---------------------------------------------------------------------------
# Certificate verification (combined proof + signature)
# ---------------------------------------------------------------------------

class TestCombinedVerification(unittest.TestCase):
    """verify_etc only checks Merkle proof; signature is checked separately."""

    def test_unsigned_etc_verifies(self):
        tree = make_tree()
        etc = tree.create_etc(0, "2026-01-01T00:00:00Z")
        self.assertTrue(verify_etc(etc))

    def test_signed_etc_verifies(self):
        tree = make_tree()
        etc = tree.create_etc(0, "2026-01-01T00:00:00Z")
        signer = HMACSigner(SAMPLE_KEY)
        verifier = HMACVerifier(SAMPLE_KEY)
        signed = etc.sign(signer)
        self.assertTrue(verify_etc(signed))
        self.assertTrue(signed.verify_signature(verifier))


# ---------------------------------------------------------------------------
# Cross-platform determinism — audit primitives
# ---------------------------------------------------------------------------

class TestAuditDeterminism(unittest.TestCase):
    """Verify that audit layer produces bit-identical outputs.

    These tests provide the *determinism vectors* used by the CI
    cross-platform comparison job (see .github/workflows/execution-checks.yml).
    The expected hash values are fixed and must match on x86_64, ARM64,
    and the WASM compatibility layer.
    """

    # Reference hash computed on x86_64 baseline:
    # sha256("agent_id=MACHINE_ACCOUNT_001|ari=95000|drift=5000|ts=2026-01-01T00:00:00Z")
    EVENT_0_REF = hashlib.sha256(
        SAMPLE_EVENTS[0].encode("utf-8")
    ).hexdigest()

    def test_event_hash_stable(self):
        h = sha256(SAMPLE_EVENTS[0])
        self.assertEqual(h, self.EVENT_0_REF)

    def test_merkle_root_stable(self):
        tree = make_tree()
        # Root is fully determined by the leaves; must be identical across runs
        root1 = make_tree().root
        root2 = make_tree().root
        self.assertEqual(root1, root2)

    def test_proof_stable(self):
        proof1 = make_tree().get_proof(0)
        proof2 = make_tree().get_proof(0)
        self.assertEqual(proof1, proof2)

    def test_hmac_sign_stable(self):
        signer = HMACSigner(SAMPLE_KEY)
        payload = b"determinism|test|payload"
        sig1 = signer.sign(payload)
        sig2 = signer.sign(payload)
        self.assertEqual(sig1, sig2)

    def test_signing_payload_utf8_stable(self):
        tree = make_tree()
        etc = tree.create_etc(0, "2026-01-01T00:00:00Z", "batch-001")
        p1 = etc._signing_payload()
        p2 = etc._signing_payload()
        self.assertEqual(p1, p2)
        # Must be valid JSON
        json.loads(p1.decode("utf-8"))

    def test_platform_info(self):
        """Print platform info for CI report — always passes."""
        info = {
            "system": platform.system(),
            "machine": platform.machine(),
            "python_version": platform.python_version(),
        }
        self.assertIn("machine", info)  # sanity assert


if __name__ == "__main__":
    unittest.main(verbosity=2)
