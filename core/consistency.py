class ConsistencyCalculator:
    """
    Agent Reliability Index (ARI) Calculator
    
    Implements the Aura Protocol mathematical foundation:
    ARI = 0.3 * StructuralIntegrity + 0.7 * SemanticAlignment - Penalties
    
    Where:
    - StructuralIntegrity: Binary validation of event structure
    - SemanticAlignment: Dot product similarity in ℝ¹⁵³⁶ space (int32 fixed-point)
    - Penalties: Policy violation penalties
    
    SCOPE: MACHINE_ACCOUNT entities only
    PROHIBITION: Human profiling or biometric data processing (AI Act Art. 5)
    DETERMINISM: Same input → Same ARI (required for Proof of Consistent Agency)
    
    Uses fixed-point int32 arithmetic (scaling factor: 10^5 = 100,000)
    """
    
    SCALING_FACTOR = 100000  # 10^5
    
    def __init__(self, constitution_vector, rules):
        self.constitution = constitution_vector
        self.rules = rules

    def calculate(self, event):
        """
        Calculate Agent Reliability Index (ARI) for an event.
        
        Returns: ARI score as int32 (scaled by 10^5)
        """
        structural = self._validate_structure(event)
        if structural == 0:
            return self._fail("Invalid structure")

        semantic = self._semantic_alignment(event["embedding"])
        penalty = self._policy_penalty(event)

        # ARI Formula: 0.3 * StructuralIntegrity + 0.7 * SemanticAlignment - Penalties
        # All values are in fixed-point (scaled by 10^5)
        weight_structural = 30000  # 0.3 * 10^5
        weight_semantic = 70000    # 0.7 * 10^5
        
        ari = (weight_structural * structural // self.SCALING_FACTOR) + \
              (weight_semantic * semantic // self.SCALING_FACTOR) - penalty
        
        # Clamp to [0, 10^5] range
        return max(0, min(self.SCALING_FACTOR, ari))

    def _validate_structure(self, event):
        """
        Validate structural integrity of event.
        
        Returns: 10^5 (1.0 in fixed-point) if valid, 0 otherwise
        """
        required = ["timestamp", "embedding", "content"]
        return self.SCALING_FACTOR if all(k in event for k in required) else 0

    def _semantic_alignment(self, event_vec):
        """
        Calculate semantic alignment via dot product in ℝ¹⁵³⁶ space.
        
        For pre-normalized unit vectors (scaled by 10^5):
        similarity = dot(a, b) / SCALING_FACTOR
        
        Returns: Similarity score as int32 (scaled by 10^5), normalized to [0, 10^5]
        """
        # Validate dimensions
        if len(event_vec) != 1536 or len(self.constitution) != 1536:
            raise ValueError(
                f"Vector dimension mismatch: event={len(event_vec)}, "
                f"constitution={len(self.constitution)}, expected=1536"
            )
        
        # Calculate dot product (both vectors are int32, scaled by 10^5)
        # dot = sum(a * b) for unit vectors scaled by 10^5
        # Result needs to be divided by 10^5 to get back to our scale
        dot = sum(a * b for a, b in zip(event_vec, self.constitution))
        similarity = dot // self.SCALING_FACTOR
        
        # Normalize from approximately [-10^5, 10^5] to [0, 10^5]
        # For unit vectors: similarity ∈ [-10^5, 10^5]
        # Normalized: (similarity + 10^5) / 2
        normalized_similarity = (similarity + self.SCALING_FACTOR) // 2
        
        return normalized_similarity

    def _policy_penalty(self, event):
        """
        Calculate penalty from policy violations.
        
        Returns: Penalty as int32 (scaled by 10^5)
        """
        return sum(self.SCALING_FACTOR for rule in self.rules if rule.is_violated(event))

    def _fail(self, reason):
        """Return failure result with ARI = 0"""
        return {
            "ari": 0,
            "reason": reason
        }
