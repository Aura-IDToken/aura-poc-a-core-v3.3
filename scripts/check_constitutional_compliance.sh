#!/bin/bash
# CONSTITUTIONAL COMPLIANCE CHECKER
# Version: 1.0
# Purpose: Validate that code changes comply with Constitutional Decree

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "═══════════════════════════════════════════════════════════"
echo "AURA PROTOCOL — CONSTITUTIONAL COMPLIANCE CHECKER v1.0"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

VIOLATIONS=0
WARNINGS=0

# Function to report violation
violation() {
    echo -e "${RED}✗ VIOLATION:${NC} $1"
    ((VIOLATIONS++))
}

# Function to report warning
warning() {
    echo -e "${YELLOW}⚠ WARNING:${NC} $1"
    ((WARNINGS++))
}

# Function to report pass
pass() {
    echo -e "${GREEN}✓ PASS:${NC} $1"
}

echo "Running Constitutional Compliance Checks..."
echo ""

# CHECK 1: No float arithmetic in runtime core
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "CHECK 1: No Float Arithmetic in Runtime Core"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd "$REPO_ROOT"

# Check for float in core/ (excluding offline_normalizer.py which is exempt)
FLOAT_VIOLATIONS=$(grep -r "float\|math\.sqrt\|math\.cos\|math\.sin" core/ \
    --include="*.py" \
    --exclude="offline_normalizer.py" \
    --exclude="test_*.py" \
    2>/dev/null || true)

if [ -n "$FLOAT_VIOLATIONS" ]; then
    violation "Float arithmetic detected in runtime core:"
    echo "$FLOAT_VIOLATIONS"
else
    pass "No float arithmetic in runtime core"
fi

echo ""

# CHECK 2: No numpy in core runtime
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "CHECK 2: No NumPy in Runtime Core"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

NUMPY_VIOLATIONS=$(grep -r "import numpy\|from numpy" core/ \
    --include="*.py" \
    --exclude="offline_normalizer.py" \
    --exclude="test_*.py" \
    2>/dev/null || true)

if [ -n "$NUMPY_VIOLATIONS" ]; then
    violation "NumPy import detected in runtime core:"
    echo "$NUMPY_VIOLATIONS"
else
    pass "No NumPy in runtime core"
fi

echo ""

# CHECK 3: No ML frameworks in core
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "CHECK 3: No ML Frameworks in Core"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

ML_VIOLATIONS=$(grep -r "import torch\|import tensorflow\|from torch\|from tensorflow\|import jax\|from jax\|import sklearn\|from sklearn" core/ \
    --include="*.py" \
    2>/dev/null || true)

if [ -n "$ML_VIOLATIONS" ]; then
    violation "ML framework detected in core:"
    echo "$ML_VIOLATIONS"
else
    pass "No ML frameworks in core"
fi

echo ""

# CHECK 4: No identity tracking
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "CHECK 4: No Identity Tracking (Art. 5 Compliance)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

IDENTITY_VIOLATIONS=$(grep -r "owner_id\|wallet_id\|user_id" core/ \
    --include="*.py" \
    --exclude="test_*.py" \
    2>/dev/null | grep -v "# " | grep -v "#.*owner_id" || true)

if [ -n "$IDENTITY_VIOLATIONS" ]; then
    violation "Identity tracking detected in core:"
    echo "$IDENTITY_VIOLATIONS"
else
    pass "No identity tracking in core"
fi

echo ""

# CHECK 5: Verify MACHINE_ACCOUNT assertions exist
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "CHECK 5: MACHINE_ACCOUNT Assertions Present"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

MACHINE_ACCOUNT_CHECKS=$(grep -r "MACHINE_ACCOUNT" core/ \
    --include="*.py" \
    2>/dev/null || true)

if [ -z "$MACHINE_ACCOUNT_CHECKS" ]; then
    warning "No MACHINE_ACCOUNT assertions found - verify Art. 5 compliance"
else
    pass "MACHINE_ACCOUNT checks present"
fi

echo ""

# CHECK 6: No GPU dependencies
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "CHECK 6: No GPU Dependencies"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

GPU_VIOLATIONS=$(grep -r "cuda\|CUDA\|\.to\(.*device.*\)\|\.gpu\(\)" core/ \
    --include="*.py" \
    2>/dev/null || true)

if [ -n "$GPU_VIOLATIONS" ]; then
    violation "GPU dependencies detected in core:"
    echo "$GPU_VIOLATIONS"
else
    pass "No GPU dependencies in core"
fi

echo ""

# CHECK 7: Verify constitutional constants
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "CHECK 7: Constitutional Constants Verification"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check for Sentinel constant (0.68)
SENTINEL_CHECK=$(grep -r "0\.68\|SENTINEL.*0\.68" core/ \
    --include="*.py" \
    2>/dev/null || true)

if [ -n "$SENTINEL_CHECK" ]; then
    pass "Sentinel constant (0.68) found"
else
    warning "Sentinel constant (0.68) not found - verify if needed"
fi

# Check for scaling factor (100000 or 100_000)
SCALING_CHECK=$(grep -r "100000\|100_000" core/ \
    --include="*.py" \
    2>/dev/null || true)

if [ -n "$SCALING_CHECK" ]; then
    pass "Scaling factor (100,000) found"
else
    warning "Scaling factor (100,000) not found - verify if needed"
fi

echo ""

# CHECK 8: No network calls in core
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "CHECK 8: No Network Calls in Core"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

NETWORK_VIOLATIONS=$(grep -r "requests\.\|urllib\.\|http\.\|socket\." core/ \
    --include="*.py" \
    --exclude="test_*.py" \
    2>/dev/null | grep -v "# " || true)

if [ -n "$NETWORK_VIOLATIONS" ]; then
    violation "Network calls detected in core:"
    echo "$NETWORK_VIOLATIONS"
else
    pass "No network calls in core"
fi

echo ""

# CHECK 9: Layer separation - no thresholds in core
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "CHECK 9: Layer Separation - No Thresholds in Core"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# This is a heuristic check - look for common threshold patterns
THRESHOLD_VIOLATIONS=$(grep -r "if.*>.*threshold\|if.*<.*threshold\|THRESHOLD\s*=" core/ \
    --include="*.py" \
    --exclude="test_*.py" \
    --exclude="policy.py" \
    2>/dev/null | grep -v "# " || true)

if [ -n "$THRESHOLD_VIOLATIONS" ]; then
    warning "Potential threshold logic in core (verify Layer 0/2 separation):"
    echo "$THRESHOLD_VIOLATIONS"
else
    pass "No obvious threshold logic in core"
fi

echo ""

# CHECK 10: Verify Constitutional Decree exists
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "CHECK 10: Constitutional Decree Document Present"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f "$REPO_ROOT/CONSTITUTIONAL_DECREE.md" ]; then
    pass "CONSTITUTIONAL_DECREE.md present"
else
    violation "CONSTITUTIONAL_DECREE.md missing"
fi

echo ""

# SUMMARY
echo "═══════════════════════════════════════════════════════════"
echo "COMPLIANCE SUMMARY"
echo "═══════════════════════════════════════════════════════════"
echo ""

if [ $VIOLATIONS -eq 0 ]; then
    echo -e "${GREEN}✓ CONSTITUTIONALLY COMPLIANT${NC}"
    echo ""
    echo "No constitutional violations detected."
    
    if [ $WARNINGS -gt 0 ]; then
        echo ""
        echo -e "${YELLOW}$WARNINGS warning(s) detected - review recommended.${NC}"
    fi
    
    echo ""
    echo "This change may proceed to the next validation stage."
    exit 0
else
    echo -e "${RED}✗ CONSTITUTIONAL VIOLATIONS DETECTED${NC}"
    echo ""
    echo -e "${RED}$VIOLATIONS violation(s) found.${NC}"
    
    if [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}$WARNINGS warning(s) also detected.${NC}"
    fi
    
    echo ""
    echo "REGULATORY_HALT"
    echo ""
    echo "This change violates the Constitutional Decree."
    echo "Please review /CONSTITUTIONAL_DECREE.md and fix violations."
    echo ""
    echo "DO NOT MERGE until all violations are resolved."
    exit 1
fi
