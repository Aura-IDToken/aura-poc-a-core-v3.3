"""
Layer 2 Orchestrator: Policy + Measurement Integration

This module provides the orchestration layer that combines:
- Layer 0 (core/): Pure measurement (ARI calculation)
- Layer 2 (compliance/): Policy enforcement (halt checks, penalties)

Architectural Purpose:
- Layer 0 performs deterministic calculation only
- Layer 2 handles policy decisions and orchestrates the flow
- This separation enforces the constitutional layer boundaries

Usage:
    from compliance.evaluator_wrapper import evaluate_with_policy
    from core.evaluator import PoCAEvaluator
    
    evaluator = PoCAEvaluator(constitution_vector)
    result = evaluate_with_policy(evaluator, agent_id, vector, valid_schema)

See: docs/architecture.md, docs/GAP-001.md CORE-005
"""

from typing import List, Dict
from core.evaluator import PoCAEvaluator
from compliance.policy import RegulatoryPolicy


def evaluate_with_policy(
    evaluator: PoCAEvaluator,
    agent_id: str,
    vector: List[int],
    valid_schema: bool
) -> Dict:
    """
    Layer 2 Orchestrator: Combines policy enforcement with measurement.
    
    This function represents the correct architectural pattern:
    1. Layer 2 performs policy checks (halt status)
    2. Layer 2 calculates policy-based penalties
    3. Layer 0 performs pure measurement (RAW_ARI = 0.3*SI + 0.7*SA)
    4. Layer 2 applies penalty: adjusted_ARI = max(0, RAW_ARI - P)
    5. Layer 2 returns the combined result
    
    Args:
        evaluator: PoCAEvaluator instance (Layer 0 measurement engine)
        agent_id: Agent identifier for halt check
        vector: Agent action vector (int32, scaled by 10^5)
        valid_schema: Whether the schema is valid
        
    Returns:
        Dict with ARI score and drift (same format as evaluator.evaluate())
        
    Raises:
        Exception: If agent is halted (Art. 14 emergency halt)
    """
    # Step 1: Policy enforcement - Check halt status (Art. 14)
    RegulatoryPolicy.check_halt_status(agent_id)
    
    # Step 2: Calculate semantic alignment for penalty determination
    # Note: This is a Layer 2 decision based on Layer 0 computation
    sa = evaluator.vector_similarity_int32(vector, evaluator.constitution)
    
    # Step 3: Policy decision - Calculate penalty based on drift threshold
    penalty = RegulatoryPolicy.calculate_penalties(sa)
    
    # Step 4: Layer 0 measurement - Pure RAW_ARI calculation (no penalty)
    result = evaluator.evaluate(agent_id, vector, valid_schema)
    
    # Step 5: Layer 2 policy decision - Apply penalty to RAW_ARI
    adjusted_ari = max(0, result["ari"] - penalty)
    
    return {
        "ari": adjusted_ari,  # int32, scaled by 10^5 — after Layer 2 penalty
        "drift": result["drift"],  # int32, scaled by 10^5
    }


# Alias for backward compatibility with existing code patterns
def evaluate_agent_with_policy(
    evaluator: PoCAEvaluator,
    agent_id: str,
    vector: List[int],
    valid_schema: bool
) -> Dict:
    """
    Alias for evaluate_with_policy for backward compatibility.
    
    DEPRECATED: Use evaluate_with_policy instead.
    This alias will be removed in v4.0.
    """
    return evaluate_with_policy(evaluator, agent_id, vector, valid_schema)


__all__ = [
    "evaluate_with_policy",
    "evaluate_agent_with_policy",
]
