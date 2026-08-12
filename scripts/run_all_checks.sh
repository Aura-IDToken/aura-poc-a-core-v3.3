#!/bin/bash
# MASTER CHECK SCRIPT
# Runs all mandatory execution checks
# If ANY check fails: DO NOT MERGE

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHECKS_DIR="$SCRIPT_DIR/checks"

echo "=========================================="
echo "AURA PROTOCOL - MANDATORY EXECUTION CHECKS"
echo "=========================================="
echo ""
echo "Repository: aura-poc-a-core"
echo "Specification: v3.3 (FROZEN)"
echo "Requirement: ALL checks must pass"
echo ""
echo "If any check fails: DO NOT MERGE"
echo ""

# Make check scripts executable
chmod +x "$CHECKS_DIR"/*.sh
chmod +x "$SCRIPT_DIR/check_constitutional_compliance.sh"

# Track overall status
OVERALL_STATUS=0

# Run CHECK 0 - Constitutional Compliance (New)
echo ""
echo "=========================================="
echo "CHECK 0 - Constitutional Compliance"
echo "=========================================="
if bash "$SCRIPT_DIR/check_constitutional_compliance.sh"; then
    CHECK_0_STATUS="✅ PASS"
else
    CHECK_0_STATUS="❌ FAIL"
    OVERALL_STATUS=1
fi

# Run CHECK 1 - Bit Identity
echo ""
if bash "$CHECKS_DIR/check_1_bit_identity.sh"; then
    CHECK_1_STATUS="✅ PASS"
else
    CHECK_1_STATUS="❌ FAIL"
    OVERALL_STATUS=1
fi

# Run CHECK 2 - Integer Only
echo ""
if bash "$CHECKS_DIR/check_2_integer_only.sh"; then
    CHECK_2_STATUS="✅ PASS"
else
    CHECK_2_STATUS="❌ FAIL"
    OVERALL_STATUS=1
fi

# Run CHECK 3 - Layer Separation
echo ""
if bash "$CHECKS_DIR/check_3_layer_separation.sh"; then
    CHECK_3_STATUS="✅ PASS"
else
    CHECK_3_STATUS="❌ FAIL"
    OVERALL_STATUS=1
fi

# Run CHECK 4 - Audit Path
echo ""
if bash "$CHECKS_DIR/check_4_audit_path.sh"; then
    CHECK_4_STATUS="✅ PASS"
else
    CHECK_4_STATUS="❌ FAIL"
    OVERALL_STATUS=1
fi

# Run CHECK 5 - Entropy
echo ""
if bash "$CHECKS_DIR/check_5_entropy.sh"; then
    CHECK_5_STATUS="✅ PASS"
else
    CHECK_5_STATUS="❌ FAIL"
    OVERALL_STATUS=1
fi

# Run CHECK 6 - Art.5 Runtime Proof (CR-001: DEFAULT / -O / -OO)
echo ""
echo "=========================================="
echo "CHECK 6 — Art.5 Runtime Proof (CR-001)"
echo "=========================================="
echo ""
echo "--- DEFAULT ---"
if python "$SCRIPT_DIR/art5_conformance_proof.py"; then
    CHECK_6A_STATUS="✅ PASS"
else
    CHECK_6A_STATUS="❌ FAIL"
    OVERALL_STATUS=1
fi
echo ""
echo "--- -O ---"
if python -O "$SCRIPT_DIR/art5_conformance_proof.py"; then
    CHECK_6B_STATUS="✅ PASS"
else
    CHECK_6B_STATUS="❌ FAIL"
    OVERALL_STATUS=1
fi
echo ""
echo "--- -OO ---"
if python -OO "$SCRIPT_DIR/art5_conformance_proof.py"; then
    CHECK_6C_STATUS="✅ PASS"
else
    CHECK_6C_STATUS="❌ FAIL"
    OVERALL_STATUS=1
fi

# Run CHECK 7 - CR-004 Append-Only Evidence Hardening
echo ""
echo "=========================================="
echo "CHECK 7 — CR-004 Append-Only Evidence"
echo "=========================================="
if bash "$CHECKS_DIR/check_7_db_append_only.sh"; then
    CHECK_7_STATUS="✅ PASS"
else
    CHECK_7_STATUS="❌ FAIL"
    OVERALL_STATUS=1
fi

# Run CHECK 8 - CR-003 Runtime History-Independence
echo ""
echo "=========================================="
echo "CHECK 8 — CR-003 History-Independence"
echo "=========================================="
if bash "$CHECKS_DIR/check_8_cr003_statelessness.sh"; then
    CHECK_8_STATUS="✅ PASS"
else
    CHECK_8_STATUS="❌ FAIL"
    OVERALL_STATUS=1
fi

# Run CHECK 9 - CR-003 Layer 0 Static Boundary
echo ""
echo "=========================================="
echo "CHECK 9 — CR-003 Layer 0 Boundary"
echo "=========================================="
if bash "$CHECKS_DIR/check_9_cr003_layer_boundary.sh"; then
    CHECK_9_STATUS="✅ PASS"
else
    CHECK_9_STATUS="❌ FAIL"
    OVERALL_STATUS=1
fi

# Run CHECK 10 - P0-1 Vector Dimension Validation
echo ""
echo "=========================================="
echo "CHECK 10 — P0-1 Dimension Validation"
echo "=========================================="
if bash "$CHECKS_DIR/check_10_p01_dimension_validation.sh"; then
    CHECK_10_STATUS="✅ PASS"
else
    CHECK_10_STATUS="❌ FAIL"
    OVERALL_STATUS=1
fi

# Summary
echo ""
echo "=========================================="
echo "CHECK SUMMARY"
echo "=========================================="
echo ""
echo "CHECK 0 - Constitutional Compliance: $CHECK_0_STATUS"
echo "CHECK 1 - Bit Identity:              $CHECK_1_STATUS"
echo "CHECK 2 - Integer Only:              $CHECK_2_STATUS"
echo "CHECK 3 - Layer Separation:          $CHECK_3_STATUS"
echo "CHECK 4 - Audit Path:                $CHECK_4_STATUS"
echo "CHECK 5 - Entropy:                   $CHECK_5_STATUS"
echo "CHECK 6 - Art.5 (DEFAULT):           $CHECK_6A_STATUS"
echo "CHECK 6 - Art.5 (-O):                $CHECK_6B_STATUS"
echo "CHECK 6 - Art.5 (-OO):               $CHECK_6C_STATUS"
echo "CHECK 7 - CR-004 Append-Only DB:     $CHECK_7_STATUS"
echo "CHECK 8 - CR-003 History-Indep:      $CHECK_8_STATUS"
echo "CHECK 9 - CR-003 Layer Boundary:     $CHECK_9_STATUS"
echo "CHECK 10 - P0-1 Dimension Validation: $CHECK_10_STATUS"
echo ""

if [ $OVERALL_STATUS -eq 0 ]; then
    echo "=========================================="
    echo "✅ ALL CHECKS PASSED"
    echo "=========================================="
    echo ""
    echo "Merge approved from execution check perspective."
    echo ""
    exit 0
else
    echo "=========================================="
    echo "❌ CHECKS FAILED"
    echo "=========================================="
    echo ""
    echo "DO NOT MERGE until all checks pass."
    echo ""
    echo "This is a frozen regulatory measurement instrument."
    echo "Bit-for-bit reproducibility is non-negotiable."
    echo ""
    exit 1
fi
