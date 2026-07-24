"""
Audit Trail Verification
Art. 13 Transparency: Verification of Merkle proofs and Event Trust Certificates
"""

from typing import List, Tuple
from .merkle import sha256, verify_proof as merkle_verify_proof, EventTrustCertificate


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
