"""
Consistency Calculator for Proof of Consistent Agency (PoCA)
Integrates with policy enforcement and kill-switch oversight
"""

import math
from typing import Dict, Any, List
from compliance.policy import PolicyRule, SystemHaltException, get_kill_switch


class ConsistencyCalculator:
    """
    Deterministic consistency score calculator.

    Evaluates agent actions against declared constitution
    with policy enforcement and emergency halt capability.
    """

    def __init__(self, constitution_vector: List[float], rules: List[PolicyRule]):
        self.constitution = constitution_vector
        self.rules = rules
        self._kill_switch = get_kill_switch()

    def calculate(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate consistency score for an event.

        Art. 14 Compliance: Check kill-switch before evaluation.

        Args:
            event: Event dictionary with required fields

        Returns:
            Dictionary with score and metadata, or failure reason
        """
        try:
            self._kill_switch.assert_not_halted()
        except SystemHaltException as e:
            return {
                "score": 0.0,
                "reason": f"System halted: {str(e)}",
                "status": "HALTED",
                "halted": True,
            }

        structural = self._validate_structure(event)
        if structural == 0.0:
            return self._fail("Invalid structure")

        semantic = self._semantic_alignment(event["embedding"])
        penalty = self._policy_penalty(event)

        score = (0.3 * structural) + (0.7 * semantic) - penalty
        final_score = max(0.0, min(1.0, score))

        return {
            "score": final_score,
            "structural": structural,
            "semantic": semantic,
            "penalty": penalty,
            "halted": False,
        }

    def _validate_structure(self, event: Dict[str, Any]) -> float:
        """Validate event has required structure."""
        required = ["timestamp", "embedding", "content"]
        return 1.0 if all(k in event for k in required) else 0.0

    def _semantic_alignment(self, event_vec: List[float]) -> float:
        """
        Calculate cosine similarity between event and constitution.
        Deterministic semantic alignment score.
        """
        dot = sum(a * b for a, b in zip(event_vec, self.constitution))
        norm_a = math.sqrt(sum(a * a for a in event_vec))
        norm_b = math.sqrt(sum(b * b for b in self.constitution))

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return dot / (norm_a * norm_b)

    def _policy_penalty(self, event: Dict[str, Any]) -> float:
        """
        Calculate penalty from policy violations.
        Art. 5 Compliance: Purely algorithmic evaluation.
        """
        violations = sum(1.0 for rule in self.rules if rule.is_violated(event))
        return violations * 0.1

    def _fail(self, reason: str) -> Dict[str, Any]:
        """Return failure result with reason."""
        return {
            "score": 0.0,
            "reason": reason,
            "status": "FAIL",
            "halted": False,
        }
