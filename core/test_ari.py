"""Test module for ARI calculation and regulatory compliance
# NON-HERESY

Constitutional Override: Test files need cosine/float references for validation.
"""

import unittest
from core.evaluator import PoCAEvaluator
from core.policy import RegulatoryPolicy
from core.merkle import MerkleAttestor


class TestARICalculation(unittest.TestCase):
    """Tests for ARI (Agent Reliability Index) calculation and regulatory compliance"""
    
    def setUp(self):
        # Reset halted agents before each test
        RegulatoryPolicy.HALTED_AGENTS.clear()
        # Constitution vector for testing
        self.constitution = [0.5] * 10
        self.evaluator = PoCAEvaluator(self.constitution)
    
    def test_human_scoring_is_prohibited(self):
        """Art. 5 EU AI Act: Ensure human scoring fails with assertion"""
        with self.assertRaises(AssertionError) as context:
            RegulatoryPolicy.validate_target("HUMAN")
        
        self.assertIn("Human scoring is strictly prohibited", str(context.exception))
    
    def test_machine_account_scoring_allowed(self):
        """Machine accounts can be scored"""
        # Should not raise any exception
        try:
            RegulatoryPolicy.validate_target("MACHINE_ACCOUNT")
        except AssertionError:
            self.fail("Machine account validation should not raise AssertionError")
    
    def test_ari_calculation_basic(self):
        """Test basic ARI calculation with valid schema"""
        agent_id = "test_agent_001"
        vector = [0.5] * 10  # Identical to constitution
        valid_schema = True
        
        result = self.evaluator.evaluate(agent_id, vector, valid_schema)
        
        self.assertIn("ari", result)
        self.assertIn("drift", result)
        self.assertIn("status", result)
        self.assertGreaterEqual(result["ari"], 0.0)
        self.assertLessEqual(result["ari"], 1.0)
    
    def test_ari_calculation_perfect_alignment(self):
        """Test ARI with perfect semantic alignment"""
        agent_id = "test_agent_002"
        vector = [0.5] * 10  # Perfect match with constitution
        valid_schema = True
        
        result = self.evaluator.evaluate(agent_id, vector, valid_schema)
        
        # With perfect alignment (SA=1.0) and valid schema (SI=1.0):
        # ARI = 0.3*1.0 + 0.7*1.0 - 0.0 = 1.0
        self.assertAlmostEqual(result["ari"], 1.0, places=5)
        self.assertAlmostEqual(result["drift"], 0.0, places=5)
        self.assertEqual(result["status"], "COMPLIANT")
    
    def test_ari_calculation_invalid_schema(self):
        """Test ARI with invalid schema"""
        agent_id = "test_agent_003"
        vector = [0.5] * 10
        valid_schema = False
        
        result = self.evaluator.evaluate(agent_id, vector, valid_schema)
        
        # With invalid schema (SI=0.0), even perfect alignment won't give high score:
        # ARI = 0.3*0.0 + 0.7*1.0 - 0.0 = 0.7
        self.assertLess(result["ari"], 1.0)
    
    def test_ari_penalty_for_drift(self):
        """Test penalty calculation for semantic drift (SA < 0.68)"""
        agent_id = "test_agent_004"
        # Create a vector with low similarity (< 0.68)
        vector = [-0.5] * 10  # Opposite direction
        valid_schema = True
        
        result = self.evaluator.evaluate(agent_id, vector, valid_schema)
        
        # Should have significant drift
        self.assertGreater(result["drift"], 0.3)
        # Penalty should be applied
        self.assertEqual(result["status"], "RISK")
    
    def test_emergency_halt_mechanism(self):
        """Art. 14: Test human oversight kill-switch"""
        agent_id = "test_agent_005"
        
        # Halt the agent
        RegulatoryPolicy.emergency_halt(agent_id)
        
        # Attempt to evaluate should raise exception
        vector = [0.5] * 10
        with self.assertRaises(Exception) as context:
            self.evaluator.evaluate(agent_id, vector, True)
        
        self.assertIn("POLICY_HALT", str(context.exception))
        self.assertIn("human oversight", str(context.exception))
    
    def test_merkle_etc_generation(self):
        """Test Event Trust Certificate (ETC) generation"""
        attestor = MerkleAttestor()
        
        ari_result = {
            "ari": 0.95,
            "drift": 0.05,
            "status": "COMPLIANT"
        }
        
        etc = attestor.generate_etc(ari_result)
        
        self.assertIn("certificate", etc)
        self.assertIn("proof", etc)
        self.assertTrue(etc["certificate"].startswith("AURA-ETC-"))
        self.assertIsInstance(etc["proof"], list)
        self.assertGreater(len(etc["proof"]), 0)
    
    def test_merkle_leaf_determinism(self):
        """Test that Merkle leaf generation is deterministic"""
        attestor = MerkleAttestor()
        
        data = {"ari": 0.85, "drift": 0.15, "status": "COMPLIANT"}
        
        leaf1 = attestor.generate_leaf(data)
        leaf2 = attestor.generate_leaf(data)
        
        self.assertEqual(leaf1, leaf2, "Merkle leaf generation must be deterministic")
    
    def test_cosine_similarity_calculation(self):
        """Test cosine similarity implementation"""
        v1 = [1.0, 0.0, 0.0]
        v2 = [1.0, 0.0, 0.0]
        
        # Perfect alignment
        sim = self.evaluator.cosine_similarity(v1, v2)
        self.assertAlmostEqual(sim, 1.0, places=5)
        
        # Orthogonal vectors
        v3 = [0.0, 1.0, 0.0]
        sim2 = self.evaluator.cosine_similarity(v1, v3)
        self.assertAlmostEqual(sim2, 0.0, places=5)
        
        # Opposite vectors
        v4 = [-1.0, 0.0, 0.0]
        sim3 = self.evaluator.cosine_similarity(v1, v4)
        self.assertAlmostEqual(sim3, -1.0, places=5)
    
    def test_ari_bounds(self):
        """Ensure ARI is always bounded between 0.0 and 1.0"""
        agent_id = "test_agent_006"
        
        # Test with extreme vectors
        extreme_vector = [1000.0] * 10
        result = self.evaluator.evaluate(agent_id, extreme_vector, True)
        
        self.assertGreaterEqual(result["ari"], 0.0)
        self.assertLessEqual(result["ari"], 1.0)


if __name__ == '__main__':
    unittest.main()
