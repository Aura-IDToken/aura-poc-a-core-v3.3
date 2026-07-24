"""
Audit Layer Signing Abstraction
Art. 13 Transparency: Cryptographic signing of Event Trust Certificates

Provides a stable API that supports:
  - Current implementation: HMAC-SHA256 (HMACSigner / HMACVerifier)
  - Future migration path: Ed25519 asymmetric signing (stubs provided)

Layer separation note:
  This module belongs to Layer 1 (audit/).
  It must NOT be imported by Layer 0 (core/).
"""

import hmac
import hashlib
from abc import ABC, abstractmethod


class Signer(ABC):
    """
    Abstract base for Audit Layer certificate signing.

    All implementations must produce a deterministic hex-encoded
    signature string from a bytes payload.
    """

    @abstractmethod
    def sign(self, payload: bytes) -> str:
        """
        Sign a payload.

        Args:
            payload: Raw bytes to sign.

        Returns:
            Hex-encoded signature string.
        """

    @abstractmethod
    def algorithm(self) -> str:
        """Return the canonical algorithm name (e.g. 'HMAC-SHA256')."""


class Verifier(ABC):
    """
    Abstract base for Audit Layer certificate verification.

    Implementations must perform constant-time comparison where possible
    to resist timing attacks.
    """

    @abstractmethod
    def verify(self, payload: bytes, signature: str) -> bool:
        """
        Verify a signature against a payload.

        Args:
            payload:   Raw bytes that were originally signed.
            signature: Hex-encoded signature to verify.

        Returns:
            True if the signature is valid, False otherwise.
        """

    @abstractmethod
    def algorithm(self) -> str:
        """Return the canonical algorithm name (e.g. 'HMAC-SHA256')."""


class HMACSigner(Signer):
    """
    HMAC-SHA256 signer. Current production implementation.

    Uses Python's ``hmac`` module with SHA-256 as the hash function.
    The signing key must be a non-empty bytes object supplied by the
    caller (e.g. a secret loaded from a secure store).
    """

    def __init__(self, key: bytes) -> None:
        if not key:
            raise ValueError("HMAC key must not be empty")
        self._key = key

    def sign(self, payload: bytes) -> str:
        return hmac.new(self._key, payload, hashlib.sha256).hexdigest()

    def algorithm(self) -> str:
        return "HMAC-SHA256"


class HMACVerifier(Verifier):
    """
    HMAC-SHA256 verifier. Current production implementation.

    Uses ``hmac.compare_digest`` for constant-time comparison to
    prevent timing-oracle attacks.
    """

    def __init__(self, key: bytes) -> None:
        if not key:
            raise ValueError("HMAC key must not be empty")
        self._key = key

    def verify(self, payload: bytes, signature: str) -> bool:
        expected = hmac.new(self._key, payload, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)

    def algorithm(self) -> str:
        return "HMAC-SHA256"


class FutureEd25519Signer(Signer):
    """
    Placeholder for future Ed25519 asymmetric signing.

    This class satisfies the Signer interface so the Audit Layer API
    remains stable when Ed25519 is introduced.  It is intentionally
    not implemented — calling ``sign`` raises NotImplementedError.

    Migration path:
        Replace this stub with a real Ed25519 implementation using
        the ``cryptography`` package without changing any caller code.
    """

    def sign(self, payload: bytes) -> str:
        raise NotImplementedError(
            "Ed25519 signing is reserved for a future instrument version. "
            "Current Audit Layer uses HMAC-SHA256 (HMACSigner)."
        )

    def algorithm(self) -> str:
        return "Ed25519"


class FutureEd25519Verifier(Verifier):
    """
    Placeholder for future Ed25519 asymmetric verification.

    See FutureEd25519Signer for migration notes.
    """

    def verify(self, payload: bytes, signature: str) -> bool:
        raise NotImplementedError(
            "Ed25519 verification is reserved for a future instrument version. "
            "Current Audit Layer uses HMAC-SHA256 (HMACVerifier)."
        )

    def algorithm(self) -> str:
        return "Ed25519"


__all__ = [
    "Signer",
    "Verifier",
    "HMACSigner",
    "HMACVerifier",
    "FutureEd25519Signer",
    "FutureEd25519Verifier",
]
