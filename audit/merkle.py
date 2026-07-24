"""
Merkle Tree Implementation for Audit Trail
Art. 13 Transparency: Cryptographic audit trails and Event Trust Certificates (ETC)
"""

import hashlib
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass


def sha256(data: str) -> str:
    """Deterministic SHA-256 hash."""
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


@dataclass
class EventTrustCertificate:
    """
    Event Trust Certificate (ETC)
    Art. 13 Compliance: Cryptographic proof of event integrity
    
    An ETC provides:
    - Immutable event hash
    - Merkle proof for batch verification
    - Temporal ordering
    - Non-repudiation
    """
    event_hash: str
    merkle_root: str
    merkle_proof: List[Tuple[str, str]]  # List of (sibling_hash, direction)
    timestamp: str
    batch_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize ETC to dictionary."""
        return {
            "event_hash": self.event_hash,
            "merkle_root": self.merkle_root,
            "merkle_proof": [
                {"sibling": sibling, "direction": direction}
                for sibling, direction in self.merkle_proof
            ],
            "timestamp": self.timestamp,
            "batch_id": self.batch_id,
        }
    
    def verify(self) -> bool:
        """
        Verify the ETC's Merkle proof.
        Returns True if the proof is valid, False otherwise.
        """
        current = self.event_hash
        for sibling, direction in self.merkle_proof:
            if direction == "left":
                current = sha256(sibling + current)
            elif direction == "right":
                current = sha256(current + sibling)
            else:
                return False
        return current == self.merkle_root


class MerkleTree:
    """
    Deterministic Merkle Tree for audit trail integrity.
    
    Provides:
    - Cryptographic root hash
    - Individual event proofs
    - Batch verification capability
    """
    
    def __init__(self, leaves: List[str], leaves_are_hashed: bool = False):
        if not leaves:
            raise ValueError("Cannot create Merkle tree with empty leaves")
        
        if leaves_are_hashed:
            self.leaves = leaves
        else:
            self.leaves = [sha256(leaf) if isinstance(leaf, str) else leaf for leaf in leaves]
        self.tree = self._build_tree(self.leaves)
        self.root = self.tree[-1][0] if self.tree else sha256("")
    
    def _build_tree(self, leaves: List[str]) -> List[List[str]]:
        """
        Build complete Merkle tree structure.
        Returns list of levels from leaves to root.
        """
        if not leaves:
            return []
        
        tree = [leaves]
        current_level = leaves
        
        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i + 1] if i + 1 < len(current_level) else left
                parent = sha256(left + right)
                next_level.append(parent)
            tree.append(next_level)
            current_level = next_level
        
        return tree
    
    def get_root(self) -> str:
        """Get Merkle root hash."""
        return self.root
    
    def get_proof(self, leaf_index: int) -> List[Tuple[str, str]]:
        """
        Generate Merkle proof for a specific leaf.
        
        Args:
            leaf_index: Index of the leaf in the original leaves list
            
        Returns:
            List of (sibling_hash, direction) tuples for proof verification
        """
        if leaf_index < 0 or leaf_index >= len(self.leaves):
            raise IndexError(f"Leaf index {leaf_index} out of range")
        
        proof = []
        current_index = leaf_index
        
        for level in range(len(self.tree) - 1):
            current_level = self.tree[level]
            
            # Determine sibling
            if current_index % 2 == 0:
                # Current node is left child
                sibling_index = current_index + 1
                if sibling_index < len(current_level):
                    sibling = current_level[sibling_index]
                    direction = "right"
                else:
                    # No sibling (odd number of nodes), duplicate current
                    sibling = current_level[current_index]
                    direction = "right"
            else:
                # Current node is right child
                sibling_index = current_index - 1
                sibling = current_level[sibling_index]
                direction = "left"
            
            proof.append((sibling, direction))
            current_index = current_index // 2
        
        return proof
    
    def create_etc(
        self, 
        leaf_index: int, 
        timestamp: str,
        batch_id: Optional[str] = None
    ) -> EventTrustCertificate:
        """
        Create an Event Trust Certificate for a specific event.
        
        Args:
            leaf_index: Index of the event in the batch
            timestamp: ISO-8601 timestamp of event
            batch_id: Optional identifier for the event batch
            
        Returns:
            EventTrustCertificate with full Merkle proof
        """
        proof = self.get_proof(leaf_index)
        event_hash = self.leaves[leaf_index]
        
        return EventTrustCertificate(
            event_hash=event_hash,
            merkle_root=self.root,
            merkle_proof=proof,
            timestamp=timestamp,
            batch_id=batch_id,
        )


def verify_proof(leaf: str, proof: List[Tuple[str, str]], root: str) -> bool:
    """
    Verify a Merkle proof.
    
    Args:
        leaf: Leaf hash to verify
        proof: List of (sibling_hash, direction) tuples
        root: Expected Merkle root
        
    Returns:
        True if proof is valid, False otherwise
    """
    current = leaf
    for sibling, direction in proof:
        if direction == "left":
            current = sha256(sibling + current)
        elif direction == "right":
            current = sha256(current + sibling)
        else:
            return False
    return current == root
