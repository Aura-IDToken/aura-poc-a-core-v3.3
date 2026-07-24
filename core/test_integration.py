"""
Integration test to verify core components work together:
- PoCAEvaluator (core/evaluator.py)
- RegulatoryPolicy (core/policy.py)
- MerkleAttestor (core/merkle.py)

# NON-HERESY

Constitutional Override: Test files need float/sqrt references for validation.
"""

import unittest
import math
from core.evaluator import PoCAEvaluator
from core.policy import RegulatoryPolicy
from core.merkle import MerkleAttestor


def normalize_to_int32(vector, scaling_factor=100000):
    """Helper to normalize float vector to int32 (only for tests)"""
    magnitude = math.sqrt(sum(x * x for x in vector))
    if magnitude == 0:
        return [0] * len(vector)
    normalized = [x / magnitude for x in vector]
    return [round(x * scaling_factor) for x in normalized]


class TestIntegration(unittest.TestCase):
    """Integration test for AURA-IDTOKEN core components"""
    
    def setUp(self):
        RegulatoryPolicy.HALTED_AGENTS.clear()
        # Constitution as float, then normalize to int32
        float_const = [0.5, 0.3, 0.8, 0.1] * 4  # 16-dim vector
        self.constitution = normalize_to_int32(float_const)
        self.evaluator = PoCAEvaluator(self.constitution)
        self.attestor = MerkleAttestor()
    
    def test_complete_workflow(self):
        """Test complete workflow: validation -> evaluation -> ETC generation"""
        # Step 1: Validate target type (Art. 5)
        target_type = "MACHINE_ACCOUNT"
        RegulatoryPolicy.validate_target(target_type)
        
        # Step 2: Evaluate agent
        agent_id = "agent_integration_001"
        float_vec = [0.5, 0.3, 0.8, 0.1] * 4  # Similar to constitution
        vector = normalize_to_int32(float_vec)
        valid_schema = True
        
        ari_result = self.evaluator.evaluate(agent_id, vector, valid_schema)
        
        # Step 3: Generate Event Trust Certificate (ETC)
        etc = self.attestor.generate_etc(ari_result)
        
        # Verify complete flow
        self.assertIn("ari", ari_result)
        self.assertIn("certificate", etc)
        self.assertTrue(etc["certificate"].startswith("AURA-ETC-"))
        
        # Verify ARI is compliant
        self.assertEqual(ari_result["status"], "COMPLIANT")
    
    def test_workflow_with_human_rejection(self):
        """Ensure workflow fails when attempting to score humans (Art. 5)"""
        with self.assertRaises(AssertionError) as context:
            RegulatoryPolicy.validate_target("HUMAN")
        
        self.assertIn("Human scoring is strictly prohibited", str(context.exception))
    
    def test_workflow_with_emergency_halt(self):
        """Test workflow with human oversight kill-switch (Art. 14)"""
        agent_id = "agent_integration_002"
        
        # Emergency halt
        RegulatoryPolicy.emergency_halt(agent_id)
        
        # Attempt evaluation
        float_vec = [0.5] * 16
        vector = normalize_to_int32(float_vec)
        with self.assertRaises(Exception) as context:
            self.evaluator.evaluate(agent_id, vector, True)
        
        self.assertIn("POLICY_HALT", str(context.exception))


if __name__ == '__main__':
    unittest.main()
