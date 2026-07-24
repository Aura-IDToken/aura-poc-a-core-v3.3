#!/bin/bash
# CHECK 1 — Bit Identity
# Run tests on x86 and ARM - hashes MUST match exactly

set -e

echo "=========================================="
echo "CHECK 1 — Bit Identity"
echo "=========================================="
echo ""

# Get current platform
PLATFORM=$(uname -m)
echo "Current platform: $PLATFORM"
echo ""

# Run bitwise replay tests
echo "Running bitwise replay tests..."
python3 -m unittest core.test_bitwise_replay -v

# Check for platform-specific hash file
HASH_FILE="core/test_bitwise_replay_${PLATFORM}.hash"
if [ -f "$HASH_FILE" ]; then
    echo ""
    echo "Platform-specific hash file found: $HASH_FILE"
    cat "$HASH_FILE"
else
    echo ""
    echo "No platform-specific hash file found at $HASH_FILE"
    echo "First run on this platform - baseline will be established"
fi

echo ""
echo "✅ CHECK 1 PASSED: Bitwise replay tests completed"
echo ""
echo "IMPORTANT: To verify cross-platform bit-identity:"
echo "  1. Run this check on x86_64"
echo "  2. Run this check on ARM (aarch64)"
echo "  3. Compare the hash outputs - they MUST match exactly"
echo ""
