#!/bin/bash
# CHECK 2 — Integer Only
# grep -R "float\|sqrt\|numpy" core/ must return NOTHING (excluding allowed files)

set -e

echo "=========================================="
echo "CHECK 2 — Integer Only"
echo "=========================================="
echo ""

echo "Scanning core/ for float/sqrt/numpy usage..."
echo "Excluding: offline_normalizer.py and test files"
echo ""

# Search for violations in core/ directory, excluding allowed files
VIOLATIONS=$(grep -r "float\|sqrt\|numpy" core/*.py --exclude="offline_normalizer.py" --exclude="test_*.py" 2>/dev/null || true)

if [ -n "$VIOLATIONS" ]; then
    echo "❌ CHECK 2 FAILED: Float/sqrt/numpy found in runtime core"
    echo ""
    echo "Violations found:"
    echo "$VIOLATIONS"
    echo ""
    echo "REGULATORY VIOLATION:"
    echo "  - Floats are PROHIBITED in runtime core (ADR-005)"
    echo "  - Only integer arithmetic allowed (Q16.16 or int32/int64)"
    echo "  - Use core/offline_normalizer.py for preprocessing"
    echo ""
    exit 1
fi

echo "✅ CHECK 2 PASSED: No float/sqrt/numpy in runtime core"
echo ""
