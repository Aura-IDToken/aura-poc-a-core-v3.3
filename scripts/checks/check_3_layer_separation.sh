#!/bin/bash
# CHECK 3 — Layer Separation
# core/ must not: return booleans of compliance, enforce thresholds, contain business logic
# CORE-005: Now also checks for forbidden Layer 0 → Layer 2 imports

set -e

echo "=========================================="
echo "CHECK 3 — Layer Separation"
echo "=========================================="
echo ""

# Search for violations (excluding test files)
echo "Checking for policy violations in core/ (excluding tests)..."
echo ""

VIOLATIONS=""

# Check 1: Status returns (COMPLIANT, RISK, etc.)
echo "1. Checking for compliance status returns..."
STATUS_VIOLATIONS=$(grep -r "\"COMPLIANT\"\|\"RISK\"\|\"status\".*:" core/*.py --exclude="test_*.py" 2>/dev/null || true)
if [ -n "$STATUS_VIOLATIONS" ]; then
    VIOLATIONS="${VIOLATIONS}Status/compliance returns found:\n${STATUS_VIOLATIONS}\n\n"
fi

# Check 2: Threshold enforcement
echo "2. Checking for threshold enforcement..."
THRESHOLD_VIOLATIONS=$(grep -r "THRESHOLD.*=" core/*.py --exclude="test_*.py" --exclude="offline_normalizer.py" 2>/dev/null || true)
if [ -n "$THRESHOLD_VIOLATIONS" ]; then
    VIOLATIONS="${VIOLATIONS}Threshold definitions found:\n${THRESHOLD_VIOLATIONS}\n\n"
fi

# Check 3: Business logic keywords
echo "3. Checking for business logic keywords..."
BUSINESS_VIOLATIONS=$(grep -r "if.*>.*THRESHOLD\|if.*<.*THRESHOLD" core/*.py --exclude="test_*.py" --exclude="offline_normalizer.py" 2>/dev/null || true)
if [ -n "$BUSINESS_VIOLATIONS" ]; then
    VIOLATIONS="${VIOLATIONS}Threshold enforcement logic found:\n${BUSINESS_VIOLATIONS}\n\n"
fi

# Check 4: CORE-005 - Forbidden imports from compliance/ or audit/
echo "4. Checking for Layer 0 → Layer 2 import violations (CORE-005)..."
# Exclude deprecated wrappers: policy.py, consistency.py (intentionally retained for v3.3 compatibility)
IMPORT_VIOLATIONS=$(grep -r "^from compliance\|^import compliance\|^from audit\|^import audit" core/*.py --exclude="test_*.py" --exclude="policy.py" --exclude="consistency.py" 2>/dev/null || true)
if [ -n "$IMPORT_VIOLATIONS" ]; then
    VIOLATIONS="${VIOLATIONS}Forbidden Layer 0 → Layer 2 imports found:\n${IMPORT_VIOLATIONS}\n\n"
fi

if [ -n "$VIOLATIONS" ]; then
    echo "❌ CHECK 3 FAILED: Layer separation violated"
    echo ""
    echo -e "$VIOLATIONS"
    echo "LAYER SEPARATION VIOLATION:"
    echo "  - Layer 0 (core/) MEASURES only"
    echo "  - Layer 2 decides (thresholds, allow/deny)"
    echo "  - Do NOT add policy to core/"
    echo "  - Do NOT import from compliance/ or audit/ in core/"
    echo ""
    echo "FIX:"
    echo "  - Remove status fields (COMPLIANT, RISK)"
    echo "  - Remove threshold enforcement"
    echo "  - Remove imports from compliance/ or audit/ in core/"
    echo "  - Move policy logic to compliance/ or audit/ layer"
    echo "  - core/ should return RAW METRICS only (ARI score, drift value)"
    echo ""
    exit 1
fi

echo "✅ CHECK 3 PASSED: Layer separation maintained"
echo ""
