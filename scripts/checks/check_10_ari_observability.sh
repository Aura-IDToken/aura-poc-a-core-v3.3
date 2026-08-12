#!/bin/bash
# CHECK 10 — RD-006 ARI Observability (CHARACTERIZATION; NON-NORMATIVE)
#
# THIS CHECK CHARACTERIZES CURRENT IMPLEMENTATION BEHAVIOUR AND DOES NOT SELECT
# NORMATIVE SEMANTICS.
#
# Authority:  docs/ADR_006_CI_OUTSIDE_FROZEN_BOUNDARY.md, unblocked item U-1
#             ("CI-based ARI observability"), drafted in
#             review/2026-08-11_ENGINEERING_BASELINE/RD-006_ARI_OBSERVABILITY.md §7.
#
# What this check IS:
#   - the execution point that makes core/test_ari_observability.py non-inert;
#   - evidence that the real core.evaluator path ran and produced the values
#     recorded in the harness.
#
# What this check is NOT:
#   - approval of any ARI value. Per ADR-006 INV-CI-3, a passing CI run is
#     evidence, never approval. RD-1 remains unresolved; ARI has no normative
#     definition. A green CHECK 10 says only "the implementation still produces
#     what it produced before".
#
# Per ADR-006 ER-6, a failure of a pinned characterization constant MUST NOT be
# resolved by editing the constant. It is resolved by recording the authorizing
# decision, or by treating the change as a finding.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

MODULE="core.test_ari_observability"

# The harness contains 8 tests: 4 observation tests + 4 harness-integrity
# controls (ADR-006 ER-5). This is a FLOOR, not a pin: it exists to make
# zero-collection and silent subsetting fail closed. Authorized growth of the
# harness raises this number; it must never silently fall below it.
MIN_EXPECTED_TESTS=8

LOG="artifacts/rd-006-ari-observability.log"
OBSERVATION="artifacts/rd-006-ari-observation.json"

mkdir -p artifacts

# Remove any pre-existing observation record so a stale file from an earlier run
# cannot be mistaken for evidence that this run executed.
rm -f "$OBSERVATION"

echo "=========================================="
echo "CHECK 10 — RD-006 ARI Observability"
echo "=========================================="
echo ""
echo "THIS CHECK CHARACTERIZES CURRENT IMPLEMENTATION BEHAVIOUR AND DOES NOT"
echo "SELECT NORMATIVE SEMANTICS."
echo ""
echo "Status:            CHARACTERIZATION / IMPLEMENTATION-DERIVED"
echo "normative_effect:  NONE"
echo "Module:            $MODULE"
echo "Minimum tests:     $MIN_EXPECTED_TESTS"
echo ""

# ---------------------------------------------------------------------------
# Execute the harness.
#
# The module name is given EXPLICITLY rather than by discovery. A discovery-based
# invocation would silently tolerate the module disappearing or failing to
# import; naming it makes an import failure a hard error. This is the failure
# class realised at commit 110a845, where `import unittest` was deleted and
# nothing detected it because no CI step invoked the module.
# ---------------------------------------------------------------------------
set +e
python3 -m unittest "$MODULE" -v 2>&1 | tee "$LOG"
pipe_status=("${PIPESTATUS[@]}")
test_exit_code=${pipe_status[0]}
tee_exit_code=${pipe_status[1]:-0}
set -e

if [ "$test_exit_code" -ne 0 ]; then
  echo ""
  echo "❌ CHECK 10 FAILED — ARI observability harness did not pass (exit $test_exit_code)"
  echo ""
  echo "If this is an import/collection error, the harness is broken and must be"
  echo "repaired. If this is an assertion failure, the observed ARI changed:"
  echo "per ADR-006 ER-6, DO NOT edit the pinned constant. Record the authorizing"
  echo "decision, or treat the change as a finding."
  exit "$test_exit_code"
fi

if [ "$tee_exit_code" -ne 0 ]; then
  echo ""
  echo "❌ CHECK 10 FAILED — could not write evidence log $LOG"
  exit "$tee_exit_code"
fi

# ---------------------------------------------------------------------------
# GUARD 1 — non-zero collection.
#
# `python3 -m unittest <module>` exits 0 and prints "Ran 0 tests ... OK" when a
# module collects nothing. Without this guard, a harness whose test classes were
# renamed, removed or de-registered would report CI success while observing
# nothing. Verified empirically: zero-collection returns exit code 0.
# ---------------------------------------------------------------------------
RAN_LINE="$(grep -E '^Ran [0-9]+ test' "$LOG" | tail -1 || true)"

if [ -z "$RAN_LINE" ]; then
  echo ""
  echo "❌ CHECK 10 FAILED — no 'Ran N tests' line in runner output."
  echo "   Execution of $MODULE could not be established."
  exit 1
fi

RAN_COUNT="$(printf '%s' "$RAN_LINE" | sed -E 's/^Ran ([0-9]+) test.*/\1/')"

if [ "$RAN_COUNT" -lt "$MIN_EXPECTED_TESTS" ]; then
  echo ""
  echo "❌ CHECK 10 FAILED — insufficient test collection."
  echo "   Collected: $RAN_COUNT"
  echo "   Required:  >= $MIN_EXPECTED_TESTS"
  echo ""
  echo "Zero or partial collection MUST NOT be reported as success. The harness"
  echo "is inert or has been subset."
  exit 1
fi

# ---------------------------------------------------------------------------
# GUARD 2 — no skipped or expected-failure outcomes.
#
# A skipped test observes nothing. Skips must not be equivalent to execution.
# ---------------------------------------------------------------------------
if grep -qE '^(OK|FAILED).*(skipped|expected failures)=' "$LOG"; then
  echo ""
  echo "❌ CHECK 10 FAILED — harness reported skipped / expected-failure outcomes."
  echo "   $(grep -E '^(OK|FAILED)' "$LOG" | tail -1)"
  echo ""
  echo "A skipped observation is not an observation."
  exit 1
fi

# ---------------------------------------------------------------------------
# GUARD 3 — the observation record was actually emitted, and carries its own
# non-normative markers (ADR-006 ER-1 / ER-2).
# ---------------------------------------------------------------------------
if [ ! -f "$OBSERVATION" ]; then
  echo ""
  echo "❌ CHECK 10 FAILED — observation artifact was not emitted: $OBSERVATION"
  exit 1
fi

if ! grep -q '"normative_effect": "NONE"' "$OBSERVATION"; then
  echo ""
  echo "❌ CHECK 10 FAILED — observation artifact is missing its non-normative"
  echo "   marker (\"normative_effect\": \"NONE\"). ADR-006 ER-2."
  exit 1
fi

echo ""
echo "=========================================="
echo "✅ CHECK 10 PASSED — harness executed"
echo "=========================================="
echo ""
echo "Tests executed:  $RAN_COUNT (minimum $MIN_EXPECTED_TESTS)"
echo "Evidence log:    $LOG"
echo "Observation:     $OBSERVATION"
echo ""
echo "REMINDER: this records what the implementation produces TODAY."
echo "It is NOT a normative definition of ARI. RD-1 remains unresolved."
