"""
AURA Protocol v3.3: Offline Constitution Vector Normalizer

This module implements Task #1 from the v3.3 specification:
Pre-normalize the Constitution Vector into an int32 unit vector using 10^5 scaling.

Purpose:
- Convert floating-point constitution vectors to fixed-point int32 representation
- Enable Zero-Float Policy compliance in runtime core
- Ensure deterministic, bit-identical results across platforms

Mathematical Approach:
1. Normalize input vector to unit length (L2 norm = 1.0)
2. Scale to fixed-point: v_int = round(v_float × 10^5)
3. Output as int32 array for runtime use

Compliance:
- Zero-Float Policy: All runtime operations use integer arithmetic
- Determinism: Same input → Same output (required for PoCA)
- Fixed-Point Arithmetic: 10^5 scaling factor for precision

Author: Aura Protocol Core Team
Status: v3.3 Implementation (MC-READY 2026)
"""

import math
import json
from typing import List, Union
from pathlib import Path


# Fixed-point scaling factor as per v3.3 spec
SCALING_FACTOR = 10**5  # 100,000 for custom fixed-point arithmetic

# Expected dimension for constitution vectors
CONSTITUTION_DIM = 1536


def normalize_vector(vector: List[float]) -> List[float]:
    """
    Normalize a vector to unit length (L2 norm = 1.0).
    
    This is the ONLY place where floating-point math is allowed,
    as this runs offline during pre-processing, not in runtime core.
    
    Args:
        vector: Input vector as list of floats
        
    Returns:
        Normalized unit vector (L2 norm = 1.0)
        
    Raises:
        ValueError: If input vector has zero magnitude
    """
    # Calculate L2 norm: ||v|| = sqrt(sum(v_i^2))
    magnitude = math.sqrt(sum(x * x for x in vector))
    
    if magnitude == 0.0:
        raise ValueError("Cannot normalize zero vector")
    
    # Normalize: v_normalized = v / ||v||
    normalized = [x / magnitude for x in vector]
    
    return normalized


def scale_to_fixed_point(normalized_vector: List[float]) -> List[int]:
    """
    Scale normalized float vector to fixed-point int32 representation.
    
    Uses v3.3 spec scaling: v_int = round(v_float × 10^5)
    
    Args:
        normalized_vector: Unit vector (L2 norm = 1.0) as floats
        
    Returns:
        Fixed-point int32 vector scaled by 10^5
    """
    # Scale each component: v_int = round(v_float × 10^5)
    int_vector = [round(x * SCALING_FACTOR) for x in normalized_vector]
    
    return int_vector


def verify_unit_vector(int_vector: List[int]) -> bool:
    """
    Verify that the int32 vector represents a unit vector.
    
    For a unit vector scaled by 10^5, the magnitude should be approximately 10^5.
    We check: sqrt(sum(v_i^2)) ≈ 10^5 (within tolerance)
    
    Args:
        int_vector: Fixed-point int32 vector
        
    Returns:
        True if vector is approximately unit length (within 1% tolerance)
    """
    # Calculate magnitude: ||v|| = sqrt(sum(v_i^2))
    magnitude_squared = sum(x * x for x in int_vector)
    magnitude = math.sqrt(magnitude_squared)
    
    # Expected magnitude for unit vector scaled by 10^5
    expected_magnitude = SCALING_FACTOR
    
    # Allow 1% tolerance for rounding errors
    tolerance = 0.01
    lower_bound = expected_magnitude * (1 - tolerance)
    upper_bound = expected_magnitude * (1 + tolerance)
    
    return lower_bound <= magnitude <= upper_bound


def normalize_constitution_vector(
    input_vector: Union[List[float], str, Path],
    output_path: Union[str, Path, None] = None,
    validate: bool = True
) -> List[int]:
    """
    Main function: Pre-normalize constitution vector to int32 fixed-point.
    
    This implements the complete offline normalization pipeline:
    1. Load or accept input vector
    2. Normalize to unit length
    3. Scale to int32 fixed-point (10^5 factor)
    4. Optionally validate unit vector property
    5. Optionally save to file
    
    Args:
        input_vector: Either a list of floats, or path to JSON file containing vector
        output_path: Optional path to save normalized int32 vector (JSON format)
        validate: Whether to verify unit vector property (default: True)
        
    Returns:
        Normalized int32 vector (1536 dimensions)
        
    Raises:
        ValueError: If input dimension is incorrect or vector is zero
        RuntimeError: If validation fails
        
    Example:
        >>> # From list
        >>> float_vec = [0.5] * 1536
        >>> int_vec = normalize_constitution_vector(float_vec)
        >>> 
        >>> # From file
        >>> int_vec = normalize_constitution_vector(
        ...     "constitution_float.json",
        ...     output_path="constitution_int32.json"
        ... )
    """
    # Load input vector
    if isinstance(input_vector, (str, Path)):
        with open(input_vector, 'r') as f:
            data = json.load(f)
            if isinstance(data, dict) and 'vector' in data:
                float_vector = data['vector']
            else:
                float_vector = data
    else:
        float_vector = input_vector
    
    # Validate dimension
    if len(float_vector) != CONSTITUTION_DIM:
        raise ValueError(
            f"Constitution vector must be {CONSTITUTION_DIM} dimensions, "
            f"got {len(float_vector)}"
        )
    
    # Step 1: Normalize to unit length
    normalized = normalize_vector(float_vector)
    
    # Step 2: Scale to fixed-point int32
    int_vector = scale_to_fixed_point(normalized)
    
    # Step 3: Validate unit vector property
    if validate:
        if not verify_unit_vector(int_vector):
            raise RuntimeError(
                "Validation failed: Normalized vector does not satisfy unit vector property. "
                "This may indicate numerical precision issues."
            )
    
    # Step 4: Save to file if requested
    if output_path is not None:
        output_data = {
            "vector": int_vector,
            "dimension": CONSTITUTION_DIM,
            "scaling_factor": SCALING_FACTOR,
            "spec_version": "v3.3",
            "description": "Pre-normalized constitution vector (int32 fixed-point)"
        }
        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=2)
    
    return int_vector


def generate_sample_constitution(
    dimension: int = CONSTITUTION_DIM,
    output_path: Union[str, Path, None] = None
) -> List[int]:
    """
    Generate a sample constitution vector for testing/demo purposes.
    
    Creates a deterministic float vector, then normalizes it to int32.
    
    Args:
        dimension: Vector dimension (default: 1536)
        output_path: Optional path to save the result
        
    Returns:
        Normalized int32 vector
    """
    # Generate deterministic sample vector
    # Use simple pattern that's easy to verify
    sample_vector = [0.5 + 0.1 * (i % 10) for i in range(dimension)]
    
    # Normalize to int32
    int_vector = normalize_constitution_vector(
        sample_vector,
        output_path=output_path,
        validate=True
    )
    
    return int_vector


# CLI interface for standalone usage
if __name__ == "__main__":
    import sys
    
    print("=" * 70)
    print("AURA Protocol v3.3: Offline Constitution Vector Normalizer")
    print("=" * 70)
    
    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python offline_normalizer.py <input.json> [output.json]")
        print("  python offline_normalizer.py --generate-sample [output.json]")
        print("\nGenerating sample constitution vector...")
        
        output_file = sys.argv[2] if len(sys.argv) > 2 else "constitution_int32.json"
        int_vec = generate_sample_constitution(output_path=output_file)
        
        print(f"\n✓ Generated sample constitution vector")
        print(f"  Dimension: {CONSTITUTION_DIM}")
        print(f"  Scaling Factor: {SCALING_FACTOR}")
        print(f"  Output: {output_file}")
        print(f"  First 5 values: {int_vec[:5]}")
        print(f"  Last 5 values: {int_vec[-5:]}")
    
    elif sys.argv[1] == "--generate-sample":
        output_file = sys.argv[2] if len(sys.argv) > 2 else "constitution_int32.json"
        int_vec = generate_sample_constitution(output_path=output_file)
        
        print(f"\n✓ Generated sample constitution vector")
        print(f"  Dimension: {CONSTITUTION_DIM}")
        print(f"  Scaling Factor: {SCALING_FACTOR}")
        print(f"  Output: {output_file}")
        print(f"  First 5 values: {int_vec[:5]}")
        print(f"  Last 5 values: {int_vec[-5:]}")
    
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        
        print(f"\nProcessing: {input_file}")
        int_vec = normalize_constitution_vector(input_file, output_path=output_file)
        
        print(f"\n✓ Constitution vector normalized successfully")
        print(f"  Dimension: {CONSTITUTION_DIM}")
        print(f"  Scaling Factor: {SCALING_FACTOR}")
        if output_file:
            print(f"  Output: {output_file}")
        print(f"  First 5 values: {int_vec[:5]}")
        print(f"  Last 5 values: {int_vec[-5:]}")
    
    print("\n" + "=" * 70)
    print("Status: READY (v3.3 compliant)")
    print("=" * 70)
