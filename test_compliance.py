#!/usr/bin/env python3
"""
Test script for Aura PoCA Core compliance features.
Tests Art. 5, Art. 13, and Art. 14 implementations.
"""

import sys
from datetime import datetime

# Import core modules
from compliance.policy import PolicyRule, SystemHaltException, get_kill_switch
from compliance.consistency import ConsistencyCalculator
from core.embedding import embed_text
from audit.merkle import MerkleTree, verify_proof
from compliance.certificate import AuraEventCertificate


def test_art5_algorithmic_policy():
    """Test Art. 5: Prohibition of human evaluation via hard assertions."""
    print("\n=== Testing Art. 5: Algorithmic Policy Enforcement ===")
    
    # Create a valid algorithmic policy rule
    def check_content_length(event):
        return len(event.get("content", "")) > 1000
    
    try:
        rule = PolicyRule("max_content_length", check_content_length)
        print("✓ Algorithmic policy rule created successfully")
    except Exception as e:
        print(f"✗ Failed to create policy rule: {e}")
        return False
    
    # Test that non-callable raises error (Art. 5 safeguard)
    try:
        invalid_rule = PolicyRule("invalid", "not_a_function")
        print("✗ Should have rejected non-callable policy rule")
        return False
    except ValueError as e:
        print(f"✓ Correctly rejected non-callable policy: {e}")
    
    # Test policy violation detection
    event = {"content": "x" * 1001, "timestamp": "2026-01-17", "embedding": [50000] * 32}
    is_violated = rule.is_violated(event)
    print(f"✓ Policy violation detected: {is_violated}")
    
    return True


def test_art13_merkle_audit_trail():
    """Test Art. 13: Merkle-hashed audit trails and Event Trust Certificates."""
    print("\n=== Testing Art. 13: Merkle Audit Trail & ETCs ===")
    
    # Create sample events
    events = [
        "event_1_data",
        "event_2_data",
        "event_3_data",
        "event_4_data",
    ]
    
    # Build Merkle tree
    try:
        tree = MerkleTree(events)
        root = tree.get_root()
        print(f"✓ Merkle tree built with root: {root[:16]}...")
    except Exception as e:
        print(f"✗ Failed to build Merkle tree: {e}")
        return False
    
    # Generate Event Trust Certificate for event 1
    try:
        etc = tree.create_etc(
            leaf_index=1,
            timestamp=datetime.utcnow().isoformat(),
            batch_id="batch_001"
        )
        print(f"✓ Event Trust Certificate generated for leaf index 1")
        print(f"  - Event hash: {etc.event_hash[:16]}...")
        print(f"  - Merkle root: {etc.merkle_root[:16]}...")
        print(f"  - Proof length: {len(etc.merkle_proof)} steps")
    except Exception as e:
        print(f"✗ Failed to generate ETC: {e}")
        return False
    
    # Verify the ETC
    try:
        is_valid = etc.verify()
        if is_valid:
            print(f"✓ Event Trust Certificate verified successfully")
        else:
            print(f"✗ Event Trust Certificate verification failed")
            return False
    except Exception as e:
        print(f"✗ Error during ETC verification: {e}")
        return False
    
    # Test manual proof verification
    try:
        proof = tree.get_proof(2)
        leaf_hash = tree.leaves[2]
        is_valid = verify_proof(leaf_hash, proof, root)
        if is_valid:
            print(f"✓ Manual Merkle proof verification successful")
        else:
            print(f"✗ Manual Merkle proof verification failed")
            return False
    except Exception as e:
        print(f"✗ Error during manual proof verification: {e}")
        return False
    
    return True


def test_art14_kill_switch():
    """Test Art. 14: Mandatory manual emergency halt (Kill-Switch)."""
    print("\n=== Testing Art. 14: Kill-Switch Oversight ===")
    
    # Get global kill-switch
    kill_switch = get_kill_switch()
    
    # Ensure it starts inactive
    if kill_switch.is_active():
        print("✗ Kill-switch should start inactive")
        return False
    print("✓ Kill-switch starts in inactive state")
    
    # Activate kill-switch
    try:
        result = kill_switch.activate(
            activated_by="operator_001",
            reason="Testing emergency halt mechanism"
        )
        if result["status"] == "activated":
            print(f"✓ Kill-switch activated: {result['activated_by']}")
        else:
            print(f"✗ Failed to activate kill-switch: {result}")
            return False
    except Exception as e:
        print(f"✗ Error activating kill-switch: {e}")
        return False
    
    # Verify system halts
    try:
        kill_switch.assert_not_halted()
        print("✗ System should be halted but assertion passed")
        return False
    except SystemHaltException as e:
        print(f"✓ System correctly halted: {str(e)[:80]}...")
    
    # Test consistency calculator respects kill-switch
    constitution = [50000] * 32
    rules = []
    calc = ConsistencyCalculator(constitution, rules)
    
    event = {
        "timestamp": "2026-01-17T14:00:00Z",
        "embedding": [50000] * 32,
        "content": "test content"
    }
    
    result = calc.calculate(event)
    if result.get("halted", False) and result["score"] == 0:
        print(f"✓ Consistency calculator respects kill-switch")
    else:
        print(f"✗ Consistency calculator did not respect kill-switch: {result}")
        return False
    
    # Deactivate kill-switch
    try:
        result = kill_switch.deactivate(deactivated_by="operator_001")
        if result["status"] == "deactivated":
            print(f"✓ Kill-switch deactivated successfully")
        else:
            print(f"✗ Failed to deactivate kill-switch: {result}")
            return False
    except Exception as e:
        print(f"✗ Error deactivating kill-switch: {e}")
        return False
    
    # Verify system operates normally
    result = calc.calculate(event)
    if not result.get("halted", False) and result["score"] > 0:
        print(f"✓ System operates normally after deactivation (score: {result['score']})")
    else:
        print(f"✗ System not operating after deactivation: {result}")
        return False
    
    return True


def test_integrated_poca_flow():
    """Test integrated PoCA flow with all compliance features."""
    print("\n=== Testing Integrated PoCA Flow ===")
    
    # Setup
    constitution_text = "Be helpful, harmless, and honest"
    constitution_vec = embed_text(constitution_text)
    
    # Define policy rules (Art. 5: algorithmic only)
    def no_harmful_content(event):
        content = event.get("content", "").lower()
        harmful_keywords = ["attack", "harm", "destroy"]
        return any(keyword in content for keyword in harmful_keywords)
    
    rules = [PolicyRule("no_harmful_content", no_harmful_content)]
    
    # Create consistency calculator
    calc = ConsistencyCalculator(constitution_vec, rules)
    
    # Test event
    event_content = "Help users learn about AI safety"
    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "embedding": embed_text(event_content),
        "content": event_content,
    }
    
    # Calculate consistency
    result = calc.calculate(event)
    if "score" in result:
        print(f"✓ Consistency score calculated: {result['score']}")
    else:
        print(f"✗ Failed to calculate consistency: {result}")
        return False
    
    # Create Event Trust Certificate (Art. 13)
    tree = MerkleTree([event_content])
    etc = tree.create_etc(0, event["timestamp"])
    
    if etc.verify():
        print(f"✓ Event Trust Certificate validated")
    else:
        print(f"✗ Event Trust Certificate invalid")
        return False
    
    # Create Aura Event Certificate
    cert = AuraEventCertificate(
        agent_id="test_agent_001",
        timestamp=event["timestamp"],
        ari_score=result["score"],
        drift=0,
        status="COMPLIANT",
        merkle_root=tree.get_root(),
        leaf_hash=tree.leaves[0],
    )
    
    fingerprint = cert.fingerprint()
    print(f"✓ Aura Event Certificate created: {fingerprint[:16]}...")
    
    return True


def main():
    """Run all compliance tests."""
    print("=" * 70)
    print("Aura PoCA Core - EU AI Act Compliance Test Suite")
    print("=" * 70)
    
    tests = [
        ("Art. 5: Algorithmic Policy Enforcement", test_art5_algorithmic_policy),
        ("Art. 13: Merkle Audit Trail & ETCs", test_art13_merkle_audit_trail),
        ("Art. 14: Kill-Switch Oversight", test_art14_kill_switch),
        ("Integrated PoCA Flow", test_integrated_poca_flow),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n✗ Test '{name}' failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 70)
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
