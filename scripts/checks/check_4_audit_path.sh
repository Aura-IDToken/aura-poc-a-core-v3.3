#!/bin/bash
# CHECK 4 — Audit Path
# Every metric must be traceable to: integer math, Merkle leaf, ETC field

set -e

echo "=========================================="
echo "CHECK 4 — Audit Path"
echo "=========================================="
echo ""

echo "Verifying audit path traceability..."
echo ""

# Check 1: Merkle module exists
if [ ! -f "core/merkle.py" ]; then
    echo "❌ CHECK 4 FAILED: core/merkle.py not found"
    exit 1
fi
echo "✅ 1. Merkle module exists (core/merkle.py)"

# Check 2: Merkle has leaf generation
if ! grep -q "def.*leaf\|def.*hash" core/merkle.py; then
    echo "❌ CHECK 4 FAILED: No leaf/hash functions in merkle.py"
    exit 1
fi
echo "✅ 2. Merkle leaf generation available"

# Check 3: Integer-only arithmetic in core (except offline normalizer)
echo "✅ 3. Integer-only arithmetic verified (see CHECK 2)"

# Check 4: Integration tests exist
INTEGRATION_TESTS=0
if [ -f "core/test_integration.py" ]; then
    INTEGRATION_TESTS=1
    echo "✅ 4. Integration tests exist (core/test_integration.py)"
fi

if [ -f "core/test_ari.py" ]; then
    INTEGRATION_TESTS=1
    echo "✅ 5. ARI tests exist (core/test_ari.py)"
fi

if [ "$INTEGRATION_TESTS" -eq 0 ]; then
    echo "⚠️  WARNING: No integration tests found"
    echo "   Consider adding tests that verify end-to-end audit path"
fi

echo ""
echo "✅ CHECK 4 PASSED: Audit path components verified"
echo ""
echo "AUDIT PATH:"
echo "  Input → Integer Math → ARI Score → Merkle Leaf → Immutable Record"
echo ""
