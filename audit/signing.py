"""
Audit Signing Abstraction
Art. 13 Transparency: Signing abstraction for Event Trust Certificates

Current implementation: HMAC-SHA256 via HMACSigner / HMACVerifier.

Architecture:
    The abstraction is designed to allow future migration to asymmetric
    signing (e.g., Ed25519) without changing the Audit Layer API.
    Only the concrete Signer/Verifier implementation changes; all callers
    use the abstract interface.

Layer: 1 (audit/)
"""

import hashlib
import hmac
from abc import ABC, abstractmethod


def _require_bytes_key(key: object) -> bytes:
    """Validate that *key* is bytes-like and return it as ``bytes``."""
    if not isinstance(key, (bytes, bytearray)):
        raise TypeError("key must be bytes")
    return bytes(key)


class Signer(ABC):
    """Abstract signing interface.

    Implementations must produce a deterministic byte signature
    for a given payload.  The same key and payload must always
    produce the same signature (required by BIT-IDENTITY law).
    """

    @abstractmethod
    def sign(self, payload: bytes) -> bytes:
        """Return the signature for *payload*.

        Args:
            payload: Canonical byte representation of the item to sign.

        Returns:
            Signature bytes.  Length and encoding depend on the
            concrete implementation.
        """


class Verifier(ABC):
    """Abstract verification interface.

    Implementations must verify a signature produced by the
    corresponding Signer.
    """

    @abstractmethod
    def verify(self, payload: bytes, signature: bytes) -> bool:
        """Return True iff *signature* is valid for *payload*.

        Args:
            payload:   The original byte representation that was signed.
            signature: The signature bytes to verify.

        Returns:
            True if the signature is valid, False otherwise.
        """


class HMACSigner(Signer):
    """HMAC-SHA256 signer.

    Current implementation for the Aura Protocol v3.3 Iron Core.
    Uses ``hmac.new(key, payload, sha256).digest()`` to produce a
    32-byte deterministic MAC.

    This implementation satisfies:
    - BIT-IDENTITY: same key + payload → identical bytes on all platforms
    - Zero-Float: pure integer / byte-level computation
    - Art. 13: deterministic, publicly verifiable algorithm
    """

    def __init__(self, key: bytes) -> None:
        """
        Args:
            key: Secret key bytes.  Must be kept confidential.
                 A future Ed25519 migration will replace this with
                 a private key object.
        """
        self._key = _require_bytes_key(key)

    def sign(self, payload: bytes) -> bytes:
        """Return HMAC-SHA256(key, payload)."""
        return hmac.new(self._key, payload, hashlib.sha256).digest()


class HMACVerifier(Verifier):
    """HMAC-SHA256 verifier.

    Uses ``hmac.compare_digest`` to prevent timing-oracle attacks.
    """

    def __init__(self, key: bytes) -> None:
        """
        Args:
            key: Secret key bytes — must match the key used by HMACSigner.
        """
        self._key = _require_bytes_key(key)

    def verify(self, payload: bytes, signature: bytes) -> bool:
        """Return True iff HMAC-SHA256(key, payload) == signature."""
        expected = hmac.new(self._key, payload, hashlib.sha256).digest()
        return hmac.compare_digest(expected, signature)


__all__ = [
    "Signer",
    "Verifier",
    "HMACSigner",
    "HMACVerifier",
]
