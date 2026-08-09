"""Test module for ARI calculation and regulatory compliance
# NON-HERESY

Constitutional Override: Test files need cosine/float references for validation.
"""

import unittest
import math
from core.evaluator import PoCAEvaluator
from compliance.policy import RegulatoryPolicy
from compliance.evaluator_wrapper import evaluate_with_policy
from core.merkle import MerkleAttestor


def normalize_to_int32(vector, scaling_factor=100000):
    """
    Helper function to normalize a float vector to int32 fixed-point.
    Only used in tests (NON-HERESY override allows float here).
    """
    # Normalize to unit length
    magnitude = math.sqrt(sum(x * x for x in vector))
    if magnitude == 0:
        return [0] * len(vector)
    normalized = [x / magnitude for x in vector]
    # Scale to int32
    int_vector = [round(x * scaling_factor) for x in normalized]
    return int_vector


class TestLayerSeparation(unittest.TestCase):
    """Regression tests for Constitutional Layer Separation (Art. I §6).

    Layer 0 (core/) MEASURES only.
    Layer 2 (compliance/) decides.
    core/evaluator.py MUST NOT return compliance status fields.
    """

    # Prohibited dict keys — both the exact casing from the violation description
    # and lowercase variants to cover all case conventions.
    PROHIBITED_KEYS = {
        "status", "COMPLIANT", "compliant",
        "RISK", "risk",
        "ALLOW", "allow",
        "DENY", "deny",
        "PASS", "pass",
        "FAIL", "fail",
    }

    def setUp(self):
        RegulatoryPolicy.HALTED_AGENTS.clear()
        float_const = [0.5] * 10
        constitution = normalize_to_int32(float_const)
        self.evaluator = PoCAEvaluator(constitution)

    def _evaluate(self, alignment="high"):
        float_vec = [0.5] * 10 if alignment == "high" else [-0.5] * 10
        vector = normalize_to_int32(float_vec)
        return self.evaluator.evaluate("test_layer_sep", vector, True)

    def test_evaluate_returns_only_measurement_keys(self):
        """Layer 0 must return only raw measurements: ari and drift (int, non-negative)."""
        result = self._evaluate("high")
        self.assertSetEqual(set(result.keys()), {"ari", "drift"},
                            "core/evaluator.py must return ONLY 'ari' and 'drift'")
        self.assertIsInstance(result["ari"], int)
        self.assertIsInstance(result["drift"], int)
        self.assertGreaterEqual(result["ari"], 0)
        self.assertGreaterEqual(result["drift"], 0)

    def test_evaluate_contains_no_prohibited_keys(self):
        """Layer 0 must never return compliance status strings."""
        for alignment in ("high", "low"):
            result = self._evaluate(alignment)
            overlap = set(result.keys()) & self.PROHIBITED_KEYS
            self.assertSetEqual(overlap, set(),
                                f"Prohibited keys found in evaluator output: {overlap}")

    def test_evaluate_values_are_integers(self):
        """All measurement values returned by Layer 0 must be integers (fixed-point)."""
        result = self._evaluate("high")
        for key, value in result.items():
            self.assertIsInstance(value, int,
                                  f"Layer 0 measurement '{key}' must be int, got {type(value)}")


class TestARICalculation(unittest.TestCase):
    """Tests for ARI (Agent Reliability Index) calculation and regulatory compliance"""
    
    def setUp(self):
        # Reset halted agents before each test
        RegulatoryPolicy.HALTED_AGENTS.clear()
        # Constitution vector for testing - properly normalized to int32
        float_const = [0.5] * 10
        self.constitution = normalize_to_int32(float_const)
        self.evaluator = PoCAEvaluator(self.constitution)
    
    def test_human_scoring_is_prohibited(self):
        """Art. 5 EU AI Act: Ensure human scoring fails with explicit fail-closed exception"""
        with self.assertRaises(ValueError) as context:
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
        float_vec = [0.5] * 10
        vector = normalize_to_int32(float_vec)  # Properly normalized
        valid_schema = True
        
        result = self.evaluator.evaluate(agent_id, vector, valid_schema)
        
        self.assertIn("ari", result)
        self.assertIn("drift", result)
        # ARI is now int32 scaled by 10^5, so range is [0, 100000]
        self.assertGreaterEqual(result["ari"], 0)
        self.assertLessEqual(result["ari"], PoCAEvaluator.SCALING_FACTOR)
    
    def test_ari_calculation_perfect_alignment(self):
        """Test ARI with perfect semantic alignment"""
        agent_id = "test_agent_002"
        float_vec = [0.5] * 10  # Same as constitution before normalization
        vector = normalize_to_int32(float_vec)
        valid_schema = True
        
        result = self.evaluator.evaluate(agent_id, vector, valid_schema)
        
        # With perfect alignment and valid schema, ARI should be close to 100000
        self.assertGreater(result["ari"], 95000)  # Should be close to 100000
        self.assertLess(result["drift"], 5000)  # Drift should be close to 0
    
    def test_ari_calculation_invalid_schema(self):
        """Test ARI with invalid schema"""
        agent_id = "test_agent_003"
        float_vec = [0.5] * 10
        vector = normalize_to_int32(float_vec)
        valid_schema = False
        
        result = self.evaluator.evaluate(agent_id, vector, valid_schema)
        
        # With invalid schema (SI=0), RAW_ARI = 0.7*SA (no penalty at Layer 0)
        # Should be less than 100000
        self.assertLess(result["ari"], PoCAEvaluator.SCALING_FACTOR)
    
    def test_ari_penalty_for_drift(self):
        """Test penalty calculation for semantic drift (SA < 0.68)"""
        agent_id = "test_agent_004"
        # Create a vector with low similarity - opposite direction
        float_vec = [-0.5] * 10
        vector = normalize_to_int32(float_vec)
        valid_schema = True
        
        # Use orchestrator to include penalty calculation (Layer 2)
        result = evaluate_with_policy(self.evaluator, agent_id, vector, valid_schema)
        
        # Should have significant drift
        self.assertGreater(result["drift"], 30000)
        # Penalty should be applied (low ARI due to drift)
        self.assertLessEqual(result["ari"], 50000)
    
    def test_emergency_halt_mechanism(self):
        """Art. 14: Test human oversight kill-switch"""
        agent_id = "test_agent_005"
        
        # Halt the agent
        RegulatoryPolicy.emergency_halt(agent_id)
        
        # Attempt to evaluate should raise exception (using orchestrator)
        float_vec = [0.5] * 10
        vector = normalize_to_int32(float_vec)
        with self.assertRaises(Exception) as context:
            evaluate_with_policy(self.evaluator, agent_id, vector, True)
        
        self.assertIn("POLICY_HALT", str(context.exception))
        self.assertIn("human oversight", str(context.exception))
    
    def test_merkle_etc_generation(self):
        """Test Event Trust Certificate (ETC) generation"""
        attestor = MerkleAttestor()
        
        ari_result = {
            "ari": 95000,  # 0.95 in int32 (scaled by 10^5)
            "drift": 5000,  # 0.05 in int32
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
        
        data = {"ari": 85000, "drift": 15000, "status": "COMPLIANT"}  # int32 values
        
        leaf1 = attestor.generate_leaf(data)
        leaf2 = attestor.generate_leaf(data)
        
        self.assertEqual(leaf1, leaf2, "Merkle leaf generation must be deterministic")
    
    def test_cosine_similarity_calculation(self):
        """Test vector similarity implementation with int32 fixed-point"""
        # Convert float vectors to int32 (scaled by 10^5)
        v1 = [100000, 0, 0]  # Unit vector [1.0, 0.0, 0.0] in int32
        v2 = [100000, 0, 0]  # Same vector
        
        # Perfect alignment
        sim = self.evaluator.vector_similarity_int32(v1, v2)
        # For unit vectors: dot(v1, v2) / 10^5 should be approximately 10^5
        self.assertGreater(sim, 90000)  # Close to 100000 (1.0 in fixed-point)
        
        # Orthogonal vectors
        v3 = [0, 100000, 0]  # Unit vector [0.0, 1.0, 0.0] in int32
        sim2 = self.evaluator.vector_similarity_int32(v1, v3)
        # Dot product of orthogonal vectors should be 0
        self.assertAlmostEqual(sim2, 0, delta=1000)  # Close to 0
        
        # Opposite vectors
        v4 = [-100000, 0, 0]  # Unit vector [-1.0, 0.0, 0.0] in int32
        sim3 = self.evaluator.vector_similarity_int32(v1, v4)
        # Dot product of opposite vectors should be -100000
        self.assertLess(sim3, -90000)  # Close to -100000 (-1.0 in fixed-point)
    
    def test_ari_bounds(self):
        """Ensure ARI is always bounded between 0 and 100000 (0.0 and 1.0 in fixed-point)"""
        agent_id = "test_agent_006"
        
        # Test with extreme vectors - normalize them first
        float_vec = [1000.0] * 10
        extreme_vector = normalize_to_int32(float_vec)
        result = self.evaluator.evaluate(agent_id, extreme_vector, True)
        
        self.assertGreaterEqual(result["ari"], 0)
        self.assertLessEqual(result["ari"], PoCAEvaluator.SCALING_FACTOR)


if __name__ == '__main__':
    unittest.main()
