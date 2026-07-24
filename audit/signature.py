"""
Deterministic cryptographic signing helpers for audit certificates.
"""

import hmac
import hashlib


SIGNATURE_ALGORITHM = "HMAC-SHA256"


def sign_canonical_hash(canonical_hash: str, signing_key: str) -> str:
    return hmac.new(
        signing_key.encode("utf-8"),
        canonical_hash.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def verify_canonical_hash_signature(canonical_hash: str, signature: str, verification_key: str) -> bool:
    expected = sign_canonical_hash(canonical_hash, verification_key)
    return hmac.compare_digest(expected, signature)

