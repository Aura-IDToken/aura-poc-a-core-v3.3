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
