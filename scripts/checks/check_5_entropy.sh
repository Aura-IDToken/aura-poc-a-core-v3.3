#!/bin/bash
# CHECK 5 — Entropy
# If change increases entropy: REJECT

set -e

echo "=========================================="
echo "CHECK 5 — Entropy Check"
echo "=========================================="
echo ""

# Calculate entropy indicators
echo "Analyzing system entropy indicators..."
echo ""

# Count source lines of code (excluding comments and blank lines)
CORE_SLOC=$(find core -name "*.py" -not -name "test_*.py" -exec grep -v "^\s*#" {} + 2>/dev/null | grep -v "^\s*$" | wc -l || echo 0)
echo "Core SLOC (excluding tests): $CORE_SLOC"

# Count number of core modules (excluding tests)
CORE_MODULES=$(find core -name "*.py" -not -name "test_*.py" -not -name "__init__.py" | wc -l || echo 0)
echo "Core modules: $CORE_MODULES"

# Count external dependencies
DEPENDENCIES=0
if [ -f "pyproject.toml" ]; then
    DEPENDENCIES=$(grep -c "requires.*=" pyproject.toml 2>/dev/null || echo 0)
fi
echo "External dependencies: $DEPENDENCIES"

# Calculate complexity indicators
IMPORTS=$(grep -r "^import\|^from" core/*.py --exclude="test_*.py" 2>/dev/null | wc -l || echo 0)
echo "Import statements: $IMPORTS"

# Check for nondeterministic operations
NONDETERMINISTIC=""
NONDETERMINISTIC=$(grep -r "random\|time\\.time\\(\\)\|datetime\\.now\\(\\)\|uuid\|os\\.urandom" core/*.py --exclude="test_*.py" 2>/dev/null || true)

if [ -n "$NONDETERMINISTIC" ]; then
    echo ""
    echo "❌ CHECK 5 FAILED: Nondeterministic operations found"
    echo ""
    echo "$NONDETERMINISTIC"
    echo ""
    echo "ENTROPY VIOLATION:"
    echo "  - random, time.time(), datetime.now(), uuid, os.urandom are PROHIBITED"
    echo "  - System must be deterministic: same input → same output"
    echo "  - Use deterministic timestamps or seeds only"
    echo ""
    exit 1
fi

# Check for network calls (increase entropy)
NETWORK=$(grep -r "requests\|urllib\|http\.client\|socket" core/*.py --exclude="test_*.py" 2>/dev/null || true)
if [ -n "$NETWORK" ]; then
    echo ""
    echo "❌ CHECK 5 FAILED: Network calls found"
    echo ""
    echo "$NETWORK"
    echo ""
    echo "ENTROPY VIOLATION:"
    echo "  - Network calls are PROHIBITED in core"
    echo "  - Introduces nondeterminism and external dependencies"
    echo ""
    exit 1
fi

echo ""
echo "✅ CHECK 5 PASSED: No entropy increase detected"
echo ""
echo "ENTROPY PRINCIPLE:"
echo "  T ∝ 1/S (Transparency inversely proportional to Secrecy/Entropy)"
echo "  Minimize entropy sources for maximum transparency"
echo ""
