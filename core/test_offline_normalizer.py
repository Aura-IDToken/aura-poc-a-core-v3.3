"""
Tests for offline_normalizer.py (v3.3 specification)
# NON-HERESY

Validates:
- Normalization correctness (L2 norm = 1.0)
- Fixed-point scaling (10^5 factor)
- Determinism (same input → same output)
- Unit vector property verification
- File I/O operations
- Edge cases and error handling

Constitutional Override: Test files need float/sqrt for validation purposes.
"""

import unittest
import json
import math
import tempfile
from pathlib import Path

from core.offline_normalizer import (
    normalize_vector,
    scale_to_fixed_point,
    verify_unit_vector,
    normalize_constitution_vector,
    generate_sample_constitution,
    SCALING_FACTOR,
    CONSTITUTION_DIM
)


class TestOfflineNormalizer(unittest.TestCase):
    """Test suite for offline_normalizer.py v3.3 implementation"""
    
    def test_normalize_vector_simple(self):
        """Test basic vector normalization to unit length"""
        # Simple 3D vector
        vector = [3.0, 4.0, 0.0]
        normalized = normalize_vector(vector)
        
        # Check length is 1.0
        magnitude = math.sqrt(sum(x * x for x in normalized))
        self.assertAlmostEqual(magnitude, 1.0, places=10)
        
        # Check direction is preserved (proportional to original)
        self.assertAlmostEqual(normalized[0], 0.6, places=10)  # 3/5
        self.assertAlmostEqual(normalized[1], 0.8, places=10)  # 4/5
        self.assertAlmostEqual(normalized[2], 0.0, places=10)
    
    def test_normalize_vector_already_unit(self):
        """Test normalization of already-unit vector"""
        vector = [1.0, 0.0, 0.0]
        normalized = normalize_vector(vector)
        
        magnitude = math.sqrt(sum(x * x for x in normalized))
        self.assertAlmostEqual(magnitude, 1.0, places=10)
        self.assertAlmostEqual(normalized[0], 1.0, places=10)
    
    def test_normalize_vector_zero_raises_error(self):
        """Test that zero vector raises ValueError"""
        vector = [0.0, 0.0, 0.0]
        
        with self.assertRaises(ValueError) as context:
            normalize_vector(vector)
        
        self.assertIn("zero vector", str(context.exception).lower())
    
    def test_scale_to_fixed_point_basic(self):
        """Test fixed-point scaling with 10^5 factor"""
        # Unit vector [1, 0, 0]
        normalized = [1.0, 0.0, 0.0]
        int_vector = scale_to_fixed_point(normalized)
        
        self.assertEqual(int_vector[0], 100000)  # 1.0 × 10^5
        self.assertEqual(int_vector[1], 0)
        self.assertEqual(int_vector[2], 0)
    
    def test_scale_to_fixed_point_fractional(self):
        """Test scaling with fractional values"""
        normalized = [0.6, 0.8, 0.0]
        int_vector = scale_to_fixed_point(normalized)
        
        self.assertEqual(int_vector[0], 60000)   # 0.6 × 10^5
        self.assertEqual(int_vector[1], 80000)   # 0.8 × 10^5
        self.assertEqual(int_vector[2], 0)
    
    def test_scale_to_fixed_point_negative(self):
        """Test scaling with negative values"""
        normalized = [-0.5, 0.5, 0.707107]
        int_vector = scale_to_fixed_point(normalized)
        
        self.assertEqual(int_vector[0], -50000)  # -0.5 × 10^5
        self.assertEqual(int_vector[1], 50000)   # 0.5 × 10^5
        self.assertAlmostEqual(int_vector[2], 70711, delta=1)  # Rounding
    
    def test_scale_to_fixed_point_rounding(self):
        """Test that rounding works correctly"""
        # Test rounding up
        normalized = [0.123456]
        int_vector = scale_to_fixed_point(normalized)
        self.assertEqual(int_vector[0], 12346)  # Rounds 12345.6 to 12346
        
        # Test rounding down
        normalized = [0.123454]
        int_vector = scale_to_fixed_point(normalized)
        self.assertEqual(int_vector[0], 12345)  # Rounds 12345.4 to 12345
    
    def test_verify_unit_vector_valid(self):
        """Test verification passes for valid unit vector"""
        # Create a proper unit vector in int32
        normalized = [0.6, 0.8, 0.0]
        int_vector = scale_to_fixed_point(normalized)
        
        self.assertTrue(verify_unit_vector(int_vector))
    
    def test_verify_unit_vector_invalid(self):
        """Test verification fails for non-unit vector"""
        # Not a unit vector - magnitude is too large
        int_vector = [200000, 0, 0]  # Magnitude = 2.0 × 10^5, not 10^5
        
        self.assertFalse(verify_unit_vector(int_vector))
    
    def test_verify_unit_vector_zero(self):
        """Test verification fails for zero vector"""
        int_vector = [0, 0, 0]
        
        self.assertFalse(verify_unit_vector(int_vector))
    
    def test_normalize_constitution_vector_from_list(self):
        """Test normalizing from a list of floats"""
        # Create test vector with correct dimension
        float_vector = [0.5] * CONSTITUTION_DIM
        
        int_vector = normalize_constitution_vector(float_vector)
        
        # Check output properties
        self.assertEqual(len(int_vector), CONSTITUTION_DIM)
        self.assertTrue(verify_unit_vector(int_vector))
        self.assertIsInstance(int_vector[0], int)
    
    def test_normalize_constitution_vector_wrong_dimension(self):
        """Test that wrong dimension raises ValueError"""
        float_vector = [0.5] * 100  # Wrong dimension
        
        with self.assertRaises(ValueError) as context:
            normalize_constitution_vector(float_vector)
        
        self.assertIn("1536", str(context.exception))
    
    def test_normalize_constitution_vector_determinism(self):
        """Test that same input always produces same output (determinism)"""
        float_vector = [0.5 + 0.1 * (i % 10) for i in range(CONSTITUTION_DIM)]
        
        # Run normalization multiple times
        result1 = normalize_constitution_vector(float_vector, validate=True)
        result2 = normalize_constitution_vector(float_vector, validate=True)
        result3 = normalize_constitution_vector(float_vector, validate=True)
        
        # All results must be identical
        self.assertEqual(result1, result2)
        self.assertEqual(result2, result3)
    
    def test_normalize_constitution_vector_file_io(self):
        """Test loading from file and saving to file"""
        # Create temporary files
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "input.json"
            output_path = Path(tmpdir) / "output.json"
            
            # Write input vector
            float_vector = [0.5 + 0.1 * (i % 10) for i in range(CONSTITUTION_DIM)]
            with open(input_path, 'w') as f:
                json.dump(float_vector, f)
            
            # Normalize from file to file
            int_vector = normalize_constitution_vector(
                input_path,
                output_path=output_path,
                validate=True
            )
            
            # Verify output file exists
            self.assertTrue(output_path.exists())
            
            # Load and verify output file
            with open(output_path, 'r') as f:
                output_data = json.load(f)
            
            self.assertIn('vector', output_data)
            self.assertIn('dimension', output_data)
            self.assertIn('scaling_factor', output_data)
            self.assertIn('spec_version', output_data)
            
            self.assertEqual(output_data['dimension'], CONSTITUTION_DIM)
            self.assertEqual(output_data['scaling_factor'], SCALING_FACTOR)
            self.assertEqual(output_data['spec_version'], 'v3.3')
            self.assertEqual(output_data['vector'], int_vector)
    
    def test_normalize_constitution_vector_file_io_dict_format(self):
        """Test loading from file with dict format (vector in 'vector' key)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "input_dict.json"
            
            # Write input in dict format
            float_vector = [0.5] * CONSTITUTION_DIM
            input_data = {"vector": float_vector}
            with open(input_path, 'w') as f:
                json.dump(input_data, f)
            
            # Should successfully load and normalize
            int_vector = normalize_constitution_vector(input_path, validate=True)
            
            self.assertEqual(len(int_vector), CONSTITUTION_DIM)
            self.assertTrue(verify_unit_vector(int_vector))
    
    def test_generate_sample_constitution_basic(self):
        """Test sample constitution generation"""
        int_vector = generate_sample_constitution()
        
        # Verify properties
        self.assertEqual(len(int_vector), CONSTITUTION_DIM)
        self.assertTrue(verify_unit_vector(int_vector))
        self.assertIsInstance(int_vector[0], int)
    
    def test_generate_sample_constitution_determinism(self):
        """Test that sample generation is deterministic"""
        sample1 = generate_sample_constitution()
        sample2 = generate_sample_constitution()
        
        # Should be identical
        self.assertEqual(sample1, sample2)
    
    def test_generate_sample_constitution_with_output(self):
        """Test sample generation with file output"""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "sample.json"
            
            int_vector = generate_sample_constitution(output_path=output_path)
            
            # Verify file was created
            self.assertTrue(output_path.exists())
            
            # Load and verify
            with open(output_path, 'r') as f:
                data = json.load(f)
            
            self.assertEqual(data['vector'], int_vector)
    
    def test_scaling_factor_constant(self):
        """Test that SCALING_FACTOR is 10^5 as per v3.3 spec"""
        self.assertEqual(SCALING_FACTOR, 100000)
    
    def test_constitution_dim_constant(self):
        """Test that CONSTITUTION_DIM is 1536 as per spec"""
        self.assertEqual(CONSTITUTION_DIM, 1536)
    
    def test_full_pipeline_1536_dimensions(self):
        """Test complete pipeline with full 1536 dimensions"""
        # Create a realistic vector
        float_vector = [
            0.5 + 0.001 * i + 0.1 * math.sin(i / 100.0)
            for i in range(CONSTITUTION_DIM)
        ]
        
        # Normalize
        int_vector = normalize_constitution_vector(float_vector, validate=True)
        
        # Verify all properties
        self.assertEqual(len(int_vector), CONSTITUTION_DIM)
        self.assertTrue(all(isinstance(x, int) for x in int_vector))
        self.assertTrue(verify_unit_vector(int_vector))
        
        # Check that values are within reasonable range
        # For unit vector scaled by 10^5, individual components should be < 10^5
        max_component = max(abs(x) for x in int_vector)
        self.assertLess(max_component, SCALING_FACTOR)
    
    def test_normalization_preserves_direction(self):
        """Test that normalization preserves vector direction"""
        # Create a simple pattern vector
        float_vector = [1.0 if i < CONSTITUTION_DIM // 2 else 0.5 
                       for i in range(CONSTITUTION_DIM)]
        
        int_vector = normalize_constitution_vector(float_vector)
        
        # The first half should have larger absolute values than second half
        first_half_avg = sum(abs(x) for x in int_vector[:CONSTITUTION_DIM // 2]) / (CONSTITUTION_DIM // 2)
        second_half_avg = sum(abs(x) for x in int_vector[CONSTITUTION_DIM // 2:]) / (CONSTITUTION_DIM // 2)
        
        self.assertGreater(first_half_avg, second_half_avg)
    
    def test_validation_can_be_disabled(self):
        """Test that validation can be disabled"""
        float_vector = [0.5] * CONSTITUTION_DIM
        
        # Should not raise even if we somehow get invalid result
        # (though with our implementation, result should always be valid)
        int_vector = normalize_constitution_vector(float_vector, validate=False)
        
        self.assertEqual(len(int_vector), CONSTITUTION_DIM)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions"""
    
    def test_very_small_values(self):
        """Test normalization with very small values"""
        float_vector = [1e-10] * CONSTITUTION_DIM
        
        # Should work - will normalize to unit vector
        int_vector = normalize_constitution_vector(float_vector)
        
        self.assertTrue(verify_unit_vector(int_vector))
    
    def test_very_large_values(self):
        """Test normalization with very large values"""
        float_vector = [1e10] * CONSTITUTION_DIM
        
        # Should work - normalization brings it back to unit length
        int_vector = normalize_constitution_vector(float_vector)
        
        self.assertTrue(verify_unit_vector(int_vector))
    
    def test_mixed_signs(self):
        """Test with mixed positive and negative values"""
        float_vector = [
            (-1.0 if i % 2 == 0 else 1.0) 
            for i in range(CONSTITUTION_DIM)
        ]
        
        int_vector = normalize_constitution_vector(float_vector)
        
        self.assertTrue(verify_unit_vector(int_vector))
        
        # Check that signs are preserved
        positive_count = sum(1 for x in int_vector if x > 0)
        negative_count = sum(1 for x in int_vector if x < 0)
        
        # Should be roughly equal (half positive, half negative)
        self.assertAlmostEqual(positive_count, CONSTITUTION_DIM // 2, delta=10)
        self.assertAlmostEqual(negative_count, CONSTITUTION_DIM // 2, delta=10)


if __name__ == '__main__':
    unittest.main()
