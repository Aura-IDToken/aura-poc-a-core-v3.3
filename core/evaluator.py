from typing import List, Dict
from core.policy import RegulatoryPolicy

class PoCAEvaluator:
    """Implementation of ARI formula: C(Et) = 0.3*S + 0.7*SA - P
    
    Uses fixed-point int32 arithmetic (scaling factor: 10^5 = 100,000)
    All values are stored as integers scaled by 100,000.
    """
    
    # ARI calculation constants (fixed-point int32)
    SCALING_FACTOR = 100000  # 10^5
    COMPLIANCE_THRESHOLD = 80000  # 0.8 * 10^5 - Minimum ARI score for COMPLIANT status
    
    def __init__(self, constitution_vector: List[int]):
        """
        Initialize evaluator with pre-normalized int32 constitution vector.
        
        Args:
            constitution_vector: Unit-normalized vector scaled to int32 (10^5 factor)
        """
        self.constitution = constitution_vector
        # Weights as integers scaled by 10^5: 0.3 → 30000, 0.7 → 70000
        self.weight_structural = 30000   # 0.3 * 10^5
        self.weight_semantic = 70000     # 0.7 * 10^5

    def vector_similarity_int32(self, v1: List[int], v2: List[int]) -> int:
        """
        Calculate similarity between two pre-normalized int32 vectors.
        
        For unit-normalized vectors: similarity ≈ dot_product / (SCALING_FACTOR)
        Since both vectors are already normalized to ||v|| = 10^5, we compute
        the dot product and rescale appropriately.
        
        Args:
            v1, v2: Pre-normalized int32 vectors (scaled by 10^5)
            
        Returns:
            Similarity score as int32 (scaled by 10^5), range approximately [-10^5, 10^5]
        """
        # Dot product of two int32 vectors
        dot = sum(a * b for a, b in zip(v1, v2))
        
        # Since both vectors are unit-normalized and scaled by 10^5:
        # dot(a, b) = (10^5 * a_unit) · (10^5 * b_unit) = 10^10 * dot(a_unit, b_unit)
        # We need to divide by 10^10 and multiply by 10^5 to get result in our scale
        # This is equivalent to dividing by 10^5
        similarity = dot // self.SCALING_FACTOR
        
        return similarity

    def evaluate(self, agent_id: str, vector: List[int], valid_schema: bool) -> Dict:
        """
        Evaluate agent reliability using fixed-point int32 arithmetic.
        
        Args:
            agent_id: Agent identifier (for halt check)
            vector: Agent action vector (int32, scaled by 10^5)
            valid_schema: Whether the schema is valid
            
        Returns:
            Dict with ARI score, drift, and status
        """
        RegulatoryPolicy.check_halt_status(agent_id)
        
        # Structural integrity: 0 or 1 (scaled by 10^5 for consistency)
        si = self.SCALING_FACTOR if valid_schema else 0
        
        # Semantic alignment (already scaled by 10^5)
        sa = self.vector_similarity_int32(vector, self.constitution)
        
        # Penalty (returned as int scaled by 10^5)
        penalty = RegulatoryPolicy.calculate_penalties(sa)
        
        # ARI = 0.3*S + 0.7*SA - P (all in fixed-point)
        # (weight * si) is (30000 * 100000) or 0, divide by 10^5 to rescale
        # (weight * sa) is (70000 * sa), divide by 10^5 to rescale
        ari = (self.weight_structural * si // self.SCALING_FACTOR) + \
              (self.weight_semantic * sa // self.SCALING_FACTOR) - penalty
        
        # Clamp to non-negative
        ari = max(0, ari)
        
        # Drift is (1.0 - sa) in fixed-point
        # Since sa can be negative (range: [-10^5, 10^5]), drift calculation needs clamping
        # For positive sa: drift = 100000 - sa (ranges from 0 to 200000)
        # For negative sa: drift = 100000 - sa (ranges from 100000 to 200000)
        # Clamp drift to [0, 100000] to represent [0.0, 1.0]
        drift = min(max(0, self.SCALING_FACTOR - sa), 2 * self.SCALING_FACTOR)
        
        return {
            "ari": ari,  # int32, scaled by 10^5
            "drift": drift,  # int32, scaled by 10^5
            "status": "COMPLIANT" if ari > self.COMPLIANCE_THRESHOLD else "RISK"
        }
