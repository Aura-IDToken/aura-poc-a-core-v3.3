"""
Consistency Calculator for Proof of Consistent Agency (PoCA)
Integrates with policy enforcement and kill-switch oversight
"""

from typing import Dict, Any, List
from compliance.policy import PolicyRule, SystemHaltException, get_kill_switch


class ConsistencyCalculator:
    """
    Deterministic consistency score calculator.

    Evaluates agent actions against declared constitution
    with policy enforcement and emergency halt capability.
    """

    SCALING_FACTOR = 100000
    STRUCTURAL_WEIGHT = 30000
    SEMANTIC_WEIGHT = 70000
    VIOLATION_PENALTY = 10000

    def __init__(self, constitution_vector: List[int], rules: List[PolicyRule]):
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
                "score": 0,
                "reason": f"System halted: {str(e)}",
                "status": "HALTED",
                "halted": True,
            }

        structural = self._validate_structure(event)
        if structural == 0:
            return self._fail("Invalid structure")

        semantic = self._semantic_alignment(event["embedding"])
        penalty = self._policy_penalty(event)

        score = (
            self.STRUCTURAL_WEIGHT * structural // self.SCALING_FACTOR
            + self.SEMANTIC_WEIGHT * semantic // self.SCALING_FACTOR
            - penalty
        )
        final_score = max(0, min(self.SCALING_FACTOR, score))

        return {
            "score": final_score,
            "structural": structural,
            "semantic": semantic,
            "penalty": penalty,
            "halted": False,
        }

    def _validate_structure(self, event: Dict[str, Any]) -> int:
        """Validate event has required structure."""
        required = ["timestamp", "embedding", "content"]
        return self.SCALING_FACTOR if all(k in event for k in required) else 0

    def _semantic_alignment(self, event_vec: List[int]) -> int:
        """
        Calculate fixed-point similarity between pre-normalized event and constitution vectors.
        """
        if not event_vec or not self.constitution:
            return 0

        if all(value == 0 for value in event_vec) or all(value == 0 for value in self.constitution):
            return 0

        if any(abs(value) > self.SCALING_FACTOR for value in event_vec):
            raise ValueError("Event vector must be normalized to the fixed-point scaling factor.")

        if any(abs(value) > self.SCALING_FACTOR for value in self.constitution):
            raise ValueError("Constitution vector must be normalized to the fixed-point scaling factor.")

        dot = sum(a * b for a, b in zip(event_vec, self.constitution))
        return dot // self.SCALING_FACTOR

    def _policy_penalty(self, event: Dict[str, Any]) -> int:
        """
        Calculate penalty from policy violations.
        Art. 5 Compliance: Purely algorithmic evaluation.
        """
        violations = sum(1 for rule in self.rules if rule.is_violated(event))
        return violations * self.VIOLATION_PENALTY

    def _fail(self, reason: str) -> Dict[str, Any]:
        """Return failure result with reason."""
        return {
            "score": 0,
            "reason": reason,
            "status": "FAIL",
            "halted": False,
        }
