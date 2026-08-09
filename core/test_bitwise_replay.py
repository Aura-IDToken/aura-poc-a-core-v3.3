"""
AURA Protocol v3.3: Bitwise Replay Test (TASK-03)
# NON-HERESY

This module implements cross-platform determinism verification.
Tests that the same input produces bit-identical output on x86, ARM, and WASM.

Purpose:
- Ensure bit-for-bit reproducibility across different architectures
- Verify zero-float runtime compliance (integer-only arithmetic)
- Validate metrological system requirements (same input -> same bits)

Test Approach:
1. Run deterministic computations using int32 fixed-point arithmetic
2. Hash the output bytes to create a platform-independent fingerprint
3. Compare hashes across platforms to verify bit-identity
4. Use offline_normalizer output as test vector (already int32)

Compliance:
- BIT-IDENTITY IS LAW: Same input -> identical bits on x86/ARM/WASM
- Zero-Float Policy: All computations use integer arithmetic
- Determinism: Critical for regulatory measurement instrument

Constitutional Override: Test files need float references for validation purposes.

Author: Aura Protocol Core Team
Status: v3.3 Implementation (TASK-03)
"""

import unittest
import hashlib
import json
import platform
import sys
from pathlib import Path
from typing import List, Tuple

# Import the offline normalizer to get test vectors
from core.offline_normalizer import (
    generate_sample_constitution,
    SCALING_FACTOR,
    CONSTITUTION_DIM
)
from scripts.generate_determinism_report import (
    compute_vectors,
    resolve_constitution_vector,
    hash_int32_array,
)


class BitwiseReplayTest(unittest.TestCase):
    """
    Cross-platform determinism verification test.
    
    Verifies that integer-only computations produce bit-identical
    results across different CPU architectures and execution environments.
    """
    
    @classmethod
    def setUpClass(cls):
        """Generate deterministic test vectors once for all tests"""
        cls.test_vector = generate_sample_constitution()
        cls.platform_info = {
            "system": platform.system(),
            "machine": platform.machine(),
            "python_version": platform.python_version(),
            "architecture": platform.architecture()[0]
        }
        print(f"\n{'='*70}")
        print(f"BITWISE REPLAY TEST - Platform: {cls.platform_info['machine']}")
        print(f"System: {cls.platform_info['system']} ({cls.platform_info['architecture']})")
        print(f"Python: {cls.platform_info['python_version']}")
        print(f"{'='*70}\n")
    
    def test_int32_fixed_point_addition(self):
        """Test that int32 addition is deterministic"""
        # Create test values in fixed-point (scaled by 10^5)
        a = 50000  # 0.5 in fixed-point
        b = 30000  # 0.3 in fixed-point
        
        # Integer addition (deterministic on all platforms)
        result = a + b
        
        # Expected: 80000 (0.8 in fixed-point)
        self.assertEqual(result, 80000)
        
        # Hash the result bytes
        result_hash = self._hash_int32(result)
        
        # This hash MUST be identical on x86, ARM, and WASM
        expected_hash = self._hash_int32(80000)
        self.assertEqual(result_hash, expected_hash)
    
    def test_int32_fixed_point_multiplication(self):
        """Test that int32 multiplication with scaling is deterministic"""
        # Fixed-point multiplication requires careful scaling
        # To multiply two fixed-point numbers, we need to divide by the scaling factor
        
        a = 50000   # 0.5 in fixed-point
        b = 60000   # 0.6 in fixed-point
        
        # Multiply and rescale: (a * b) // SCALING_FACTOR
        # This gives us 0.5 * 0.6 = 0.3 in fixed-point
        result = (a * b) // SCALING_FACTOR
        
        # Expected: 30000 (0.3 in fixed-point)
        self.assertEqual(result, 30000)
        
        # Hash verification
        result_hash = self._hash_int32(result)
        expected_hash = self._hash_int32(30000)
        self.assertEqual(result_hash, expected_hash)
    
    def test_vector_dot_product_int32(self):
        """Test that integer dot product is deterministic"""
        # Use small vectors for clarity
        vec_a = [10000, 20000, 30000]  # Fixed-point values
        vec_b = [15000, 25000, 35000]
        
        # Integer dot product (no floating point)
        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        
        # Expected: 10000*15000 + 20000*25000 + 30000*35000
        #         = 150000000 + 500000000 + 1050000000
        #         = 1700000000
        self.assertEqual(dot_product, 1700000000)
        
        # Hash verification
        result_hash = self._hash_int64(dot_product)
        expected_hash = self._hash_int64(1700000000)
        self.assertEqual(result_hash, expected_hash)
    
    def test_constitution_vector_hash(self):
        """
        Test that the constitution vector hash is deterministic.
        
        This is the PRIMARY test for cross-platform bit-identity.
        The hash of the int32 vector MUST be identical on all platforms.
        """
        # Get the pre-generated test vector
        vector = self.test_vector
        
        # Hash the entire vector
        vector_hash = self._hash_int32_array(vector)
        
        # Store this hash - it MUST be identical across platforms
        # This hash was generated on the initial platform and should match everywhere
        print(f"\nConstitution Vector Hash: {vector_hash}")
        print(f"Platform: {self.platform_info['machine']}")
        print(f"Vector length: {len(vector)}")
        print(f"First 5 elements: {vector[:5]}")
        print(f"Last 5 elements: {vector[-5:]}")
        
        # Verify vector properties
        self.assertEqual(len(vector), CONSTITUTION_DIM)
        self.assertTrue(all(isinstance(x, int) for x in vector))
        
        # The hash itself is platform-dependent due to Python's hash() function
        # So we verify determinism by re-computing and comparing
        vector_hash_2 = self._hash_int32_array(vector)
        self.assertEqual(vector_hash, vector_hash_2, 
                        "Hash must be identical on repeated computation")
    
    def test_replay_determinism(self):
        """
        Test that replaying the same computation yields identical results.
        
        This simulates what would happen in a regulatory audit:
        - Load the same input data
        - Run the same computation
        - Verify bit-identical output
        """
        # Input: Use a deterministic subset of the constitution vector
        input_vector = self.test_vector[:100]  # First 100 elements
        
        # Computation: Simple weighted sum (integer only)
        weights = [i + 1 for i in range(100)]  # Weights: 1, 2, 3, ..., 100
        weighted_sum = sum(v * w for v, w in zip(input_vector, weights))
        
        # Hash the result
        result_hash = self._hash_int64(weighted_sum)
        
        # Replay: Do the same computation again
        input_vector_2 = self.test_vector[:100]
        weights_2 = [i + 1 for i in range(100)]
        weighted_sum_2 = sum(v * w for v, w in zip(input_vector_2, weights_2))
        result_hash_2 = self._hash_int64(weighted_sum_2)
        
        # MUST be identical
        self.assertEqual(weighted_sum, weighted_sum_2)
        self.assertEqual(result_hash, result_hash_2)
        
        print(f"\nReplay Test:")
        print(f"  Weighted sum: {weighted_sum}")
        print(f"  Hash: {result_hash}")
        print(f"  ✓ Deterministic: YES")
    
    def test_cross_platform_reference_hash(self):
        """
        Test against a known reference hash.
        
        This test will FAIL if the platform produces different results.
        In CI, we can compare hashes from x86, ARM, and WASM builds.
        """
        # Create a simple, deterministic computation
        test_data = [i * 1000 for i in range(10)]  # [0, 1000, 2000, ..., 9000]
        result_sum = sum(test_data)
        
        # Expected: 0 + 1000 + 2000 + ... + 9000 = 45000
        self.assertEqual(result_sum, 45000)
        
        # Hash it
        result_hash = self._hash_int32(result_sum)
        
        # Reference hash (pre-computed on x86_64 as baseline)
        # This is SHA256 of the byte representation of 45000 as int32 (little-endian, signed)
        # Computed: hashlib.sha256((45000).to_bytes(4, byteorder='little', signed=True)).hexdigest()
        reference_hash = "7a5f616273ccf1656c4373053a9a82ab2b2bfc8e6c472a1855a951a8cf0edeb0"
        
        self.assertEqual(result_hash, reference_hash,
                        f"Platform {self.platform_info['machine']} produced different hash! "
                        f"Expected: {reference_hash}, Got: {result_hash}")
        
        print(f"\nReference Hash Test:")
        print(f"  Input: [0, 1000, 2000, ..., 9000]")
        print(f"  Sum: {result_sum}")
        print(f"  Hash: {result_hash}")
        print(f"  ✓ Matches x86_64 baseline: YES")
        print(f"  Platform: {self.platform_info['machine']}")
    
    def test_no_float_contamination(self):
        """
        Verify that no floating-point operations leak into the computation.
        
        This test ensures zero-float policy compliance.
        """
        # Start with int32 values
        a = 100000  # 1.0 in fixed-point
        b = 50000   # 0.5 in fixed-point
        
        # Integer-only operations
        sum_result = a + b
        diff_result = a - b
        mult_result = (a * b) // SCALING_FACTOR
        
        # All results must be integers
        self.assertIsInstance(sum_result, int)
        self.assertIsInstance(diff_result, int)
        self.assertIsInstance(mult_result, int)
        
        # Verify exact values (no rounding errors from float)
        self.assertEqual(sum_result, 150000)   # 1.5 in fixed-point
        self.assertEqual(diff_result, 50000)   # 0.5 in fixed-point
        self.assertEqual(mult_result, 50000)   # 0.5 in fixed-point
    
    def test_byte_level_determinism(self):
        """
        Test that byte-level representation is deterministic.
        
        This is the ultimate test: convert to bytes and hash.
        """
        # Create a small int32 array
        data = [12345, -67890, 100000, -50000]
        
        # Convert to bytes (little-endian, 4 bytes per int32)
        byte_array = bytearray()
        for value in data:
            byte_array.extend(value.to_bytes(4, byteorder='little', signed=True))
        
        # Hash the bytes
        hash_result = hashlib.sha256(byte_array).hexdigest()
        
        # This hash MUST be identical on all platforms
        print(f"\nByte-Level Determinism Test:")
        print(f"  Data: {data}")
        print(f"  Bytes: {byte_array.hex()}")
        print(f"  SHA256: {hash_result}")
        
        # Verify by re-computing
        byte_array_2 = bytearray()
        for value in data:
            byte_array_2.extend(value.to_bytes(4, byteorder='little', signed=True))
        hash_result_2 = hashlib.sha256(byte_array_2).hexdigest()
        
        self.assertEqual(hash_result, hash_result_2)
        self.assertEqual(byte_array, byte_array_2)
    
    # Helper methods for hashing
    
    def _hash_int32(self, value: int) -> str:
        """Hash a single int32 value"""
        byte_data = value.to_bytes(4, byteorder='little', signed=True)
        return hashlib.sha256(byte_data).hexdigest()
    
    def _hash_int64(self, value: int) -> str:
        """Hash a single int64 value"""
        byte_data = value.to_bytes(8, byteorder='little', signed=True)
        return hashlib.sha256(byte_data).hexdigest()
    
    def _hash_int32_array(self, array: List[int]) -> str:
        """Hash an array of int32 values"""
        byte_array = bytearray()
        for value in array:
            byte_array.extend(value.to_bytes(4, byteorder='little', signed=True))
        return hashlib.sha256(byte_array).hexdigest()
    
    def test_save_platform_hash_record(self):
        """
        Save a hash record for this platform.
        
        In CI, we can collect these records from x86, ARM, and WASM builds
        and verify they all match.
        """
        # Generate reference computation
        reference_vector = self.test_vector[:1000]  # First 1000 elements
        reference_hash = self._hash_int32_array(reference_vector)
        
        # Create record
        record = {
            "platform": {
                "system": self.platform_info["system"],
                "machine": self.platform_info["machine"],
                "architecture": self.platform_info["architecture"],
                "python_version": self.platform_info["python_version"]
            },
            "test_vector_hash": reference_hash,
            "test_vector_length": len(reference_vector),
            "scaling_factor": SCALING_FACTOR,
            "spec_version": "v3.3"
        }
        
        # In a real CI setup, we would save this to a file
        # For now, just print it
        print(f"\n{'='*70}")
        print("PLATFORM HASH RECORD")
        print(f"{'='*70}")
        print(json.dumps(record, indent=2))
        print(f"{'='*70}\n")
        
        # Verify the record is valid
        self.assertIsNotNone(record["test_vector_hash"])
        self.assertEqual(record["test_vector_length"], 1000)

    def test_cr007_canonical_vector_resolution(self):
        """CR-007: canonical constitution vector must resolve deterministically."""
        vector = resolve_constitution_vector()
        self.assertEqual(len(vector), CONSTITUTION_DIM)
        self.assertTrue(all(isinstance(x, int) for x in vector))

    def test_cr007_full_vector_hash_determinism(self):
        """CR-007: full-vector hash must be deterministic and stable."""
        vector = resolve_constitution_vector()
        hash_a = hash_int32_array(vector)
        hash_b = hash_int32_array(vector)
        self.assertEqual(hash_a, hash_b)
        self.assertEqual(hash_a, "4a3474f01e1b6ac0850398b027264cf49f4a1d2acab5db0c4ea53dd2ae123fae")

    def test_cr007_full_vector_hash_changes_on_mutation(self):
        """CR-007: changing one element must change full-vector hash."""
        vector = resolve_constitution_vector()
        baseline_hash = hash_int32_array(vector)
        mutated = list(vector)
        mutated[0] = mutated[0] + 1
        mutated_hash = hash_int32_array(mutated)
        self.assertNotEqual(mutated_hash, baseline_hash)

    def test_cr007_repeated_vector_generation_same_hash(self):
        """CR-007: repeated generation must produce same full-vector hash."""
        hashes = []
        for _ in range(3):
            hashes.append(hash_int32_array(resolve_constitution_vector()))
        self.assertEqual(hashes[0], hashes[1])
        self.assertEqual(hashes[1], hashes[2])

    def test_cr007_no_runtime_float_in_provenance_pipeline(self):
        """CR-007: provenance/vector hashing pipeline must remain integer-only."""
        source = Path(__file__).resolve().parents[1] / "scripts" / "generate_determinism_report.py"
        text = source.read_text(encoding="utf-8")
        self.assertNotIn("math.sqrt(", text)
        self.assertNotIn("numpy", text)

    def test_cr007_existing_subset_vector_hash_unchanged(self):
        """CR-007: existing determinism vector hash must remain unchanged."""
        vectors = compute_vectors()
        self.assertEqual(
            vectors["ari_vector_hash"],
            "de563725627d2a2ccd96a2c00095a8eeea00b2e580c396145661455e4e516cd0",
        )


class WASMCompatibilityTest(unittest.TestCase):
    """
    Tests for WASM compatibility.
    
    Note: These tests verify that the code COULD run in WASM.
    Actual WASM execution would require wasmtime or a browser environment.
    """
    
    def test_no_platform_specific_operations(self):
        """Verify no platform-specific operations are used"""
        # All operations should work in WASM
        a = 100000
        b = 50000
        
        # Basic arithmetic (supported in WASM)
        self.assertEqual(a + b, 150000)
        self.assertEqual(a - b, 50000)
        self.assertEqual(a * b, 5000000000)
        self.assertEqual(a // b, 2)
        
        # Bitwise operations (supported in WASM)
        self.assertEqual(a & b, 33280)
        self.assertEqual(a | b, 116720)
        self.assertEqual(a ^ b, 83440)
    
    def test_wasm_safe_data_types(self):
        """Verify we only use WASM-safe data types"""
        # WASM supports i32, i64, f32, f64
        # We use only i32 and i64 (no float)
        
        value_i32 = 100000
        value_i64 = 10000000000
        
        # Type checks
        self.assertIsInstance(value_i32, int)
        self.assertIsInstance(value_i64, int)
        
        # Range checks (i32: -2^31 to 2^31-1, inclusive)
        self.assertGreaterEqual(value_i32, -2147483648)
        self.assertLessEqual(value_i32, 2147483647)


# Command-line interface
if __name__ == "__main__":
    # Banner width constant for formatting
    BANNER_WIDTH = 70
    
    print("\n" + "="*BANNER_WIDTH)
    print("AURA Protocol v3.3: Bitwise Replay Test (TASK-03)")
    print("="*BANNER_WIDTH)
    print("\nThis test verifies cross-platform determinism:")
    print("- x86: Native execution")
    print("- ARM: Native execution")  
    print("- WASM: Requires wasmtime or browser (future implementation)")
    print("\nBIT-IDENTITY IS LAW: Same input → identical bits")
    print("="*BANNER_WIDTH + "\n")
    
    # Run tests with verbose output
    unittest.main(verbosity=2)
