"""
Audit trail verification helpers.
"""

from typing import List, Tuple, Dict, Any, Union

from .canonical import CanonicalEvent
from .certificate import AuraEventTrustCertificate
from .merkle import (
    sha256,
    verify_proof as merkle_verify_proof,
    EventTrustCertificate,
)


def verify_proof(leaf: str, proof: List[Tuple[str, str]], root: str) -> bool:
    """
    Verify a Merkle proof for backward compatibility.

    Args:
        leaf: Leaf hash to verify
        proof: List of (sibling_hash, direction) tuples
        root: Expected Merkle root

    Returns:
        True if proof is valid, False otherwise
    """
    return merkle_verify_proof(leaf, proof, root)


def verify_etc(etc: EventTrustCertificate) -> bool:
    """
    Verify an Event Trust Certificate.

    Args:
        etc: EventTrustCertificate to verify

    Returns:
        True if ETC is valid, False otherwise
    """
    return etc.verify()


def verify_event_trust_certificate(
    event: Union[CanonicalEvent, Dict[str, Any]],
    certificate: Union[AuraEventTrustCertificate, Dict[str, Any]],
    verification_key: str,
) -> bool:
    """
    Verify full chain: canonical event hash, Merkle proof/root, and certificate signature.
    """
    canonical_event = event if isinstance(event, CanonicalEvent) else CanonicalEvent.from_dict(event)
    event_hash = canonical_event.canonical_hash()

    cert = (
        certificate
        if isinstance(certificate, AuraEventTrustCertificate)
        else AuraEventTrustCertificate.from_dict(certificate)
    )

    if event_hash != cert.canonical_hash:
        return False

    if not merkle_verify_proof(cert.canonical_hash, cert.merkle_proof, cert.merkle_root):
        return False

    return cert.verify_signature(verification_key)
