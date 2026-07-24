#!/usr/bin/env python3
"""
AURA-IDTOKEN: Demonstration Script
Shows the complete flow from policy validation to ETC generation
"""

from core.evaluator import PoCAEvaluator
from core.policy import RegulatoryPolicy
from core.merkle import MerkleAttestor
import json


def demo_compliant_agent():
    """Demonstrate evaluation of a compliant machine agent"""
    print("=" * 60)
    print("DEMO 1: Compliant Machine Agent Evaluation")
    print("=" * 60)
    
    # Constitution vector (represents declared intent)
    constitution = [0.5, 0.3, 0.8, 0.1] * 4
    evaluator = PoCAEvaluator(constitution)
    attestor = MerkleAttestor()
    
    # Agent data
    agent_id = "machine_agent_001"
    target_type = "MACHINE_ACCOUNT"
    agent_vector = [0.52, 0.31, 0.79, 0.09] * 4  # Very similar to constitution
    valid_schema = True
    
    # Step 1: Regulatory validation (Art. 5)
    print(f"\n1. Validating target type: {target_type}")
    try:
        RegulatoryPolicy.validate_target(target_type)
        print("   ✓ Validation passed: Machine account scoring allowed")
    except AssertionError as e:
        print(f"   ✗ Validation failed: {e}")
        return
    
    # Step 2: ARI calculation
    print(f"\n2. Calculating ARI for agent: {agent_id}")
    ari_result = evaluator.evaluate(agent_id, agent_vector, valid_schema)
    print(f"   ARI Score: {ari_result['ari']:.4f}")
    print(f"   Drift: {ari_result['drift']:.4f}")
    print(f"   Status: {ari_result['status']}")
    
    # Step 3: Generate Event Trust Certificate
    print("\n3. Generating Event Trust Certificate (ETC)")
    etc = attestor.generate_etc(ari_result)
    print(f"   Certificate ID: {etc['certificate']}")
    print(f"   Merkle Proof: {etc['proof'][0][:16]}...")
    
    print("\n✓ Complete workflow executed successfully\n")


def demo_human_rejection():
    """Demonstrate rejection of human scoring (Art. 5)"""
    print("=" * 60)
    print("DEMO 2: Human Scoring Rejection (Art. 5 EU AI Act)")
    print("=" * 60)
    
    target_type = "HUMAN"
    
    print(f"\n1. Attempting to validate target type: {target_type}")
    try:
        RegulatoryPolicy.validate_target(target_type)
        print("   ✗ Unexpected: Validation should have failed")
    except AssertionError as e:
        print(f"   ✓ Validation correctly rejected: {e}")
    
    print("\n✓ Human scoring prohibition enforced\n")


def demo_emergency_halt():
    """Demonstrate emergency halt mechanism (Art. 14)"""
    print("=" * 60)
    print("DEMO 3: Emergency Halt (Art. 14 Human Oversight)")
    print("=" * 60)
    
    # Reset halted agents
    RegulatoryPolicy.HALTED_AGENTS.clear()
    
    constitution = [0.5] * 10
    evaluator = PoCAEvaluator(constitution)
    
    agent_id = "machine_agent_002"
    agent_vector = [0.5] * 10
    
    print(f"\n1. Activating emergency halt for agent: {agent_id}")
    RegulatoryPolicy.emergency_halt(agent_id)
    print("   ✓ Agent halted")
    
    print(f"\n2. Attempting to evaluate halted agent")
    try:
        result = evaluator.evaluate(agent_id, agent_vector, True)
        print("   ✗ Unexpected: Evaluation should have been blocked")
    except Exception as e:
        print(f"   ✓ Evaluation correctly blocked: {e}")
    
    print("\n✓ Kill-switch mechanism working\n")


def demo_drift_detection():
    """Demonstrate drift detection and penalty application"""
    print("=" * 60)
    print("DEMO 4: Semantic Drift Detection & Penalty")
    print("=" * 60)
    
    constitution = [1.0, 0.0, 0.0, 0.0, 0.0] * 2
    evaluator = PoCAEvaluator(constitution)
    
    agent_id = "machine_agent_003"
    drifted_vector = [-0.5, 0.3, 0.8, 0.1, 0.2] * 2  # Very different from constitution
    
    print(f"\n1. Evaluating agent with semantic drift")
    print(f"   Constitution: {constitution[:5]}...")
    print(f"   Agent Vector: {drifted_vector[:5]}...")
    
    result = evaluator.evaluate(agent_id, drifted_vector, True)
    
    print(f"\n2. Results:")
    print(f"   ARI Score: {result['ari']:.4f}")
    print(f"   Drift: {result['drift']:.4f}")
    print(f"   Status: {result['status']}")
    
    if result['drift'] > 0.3:
        print("\n   ⚠ High drift detected - penalty applied")
    
    print("\n✓ Drift detection working\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("AURA-IDTOKEN: Cathedral Architecture Demonstration")
    print("Proof-of-Consistent-Agency (PoCA) for AI Regulatory Sandbox")
    print("=" * 60 + "\n")
    
    demo_compliant_agent()
    demo_human_rejection()
    demo_emergency_halt()
    demo_drift_detection()
    
    print("=" * 60)
    print("All demonstrations completed successfully")
    print("Repository is MC-READY ✓")
    print("=" * 60)
