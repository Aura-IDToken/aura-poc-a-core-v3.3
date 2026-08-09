"""
AG-02 — Art. 5 Runtime Conformance Proof (CR-001)

Proves that RegulatoryPolicy.validate_target() raises ValueError
(not AssertionError) for non-MACHINE_ACCOUNT targets, and accepts
MACHINE_ACCOUNT without exception.

This script is executed three times in CI:
  python    scripts/art5_conformance_proof.py   → DEFAULT
  python -O scripts/art5_conformance_proof.py   → -O
  python -OO scripts/art5_conformance_proof.py  → -OO

The ValueError-based implementation survives both -O and -OO because
Python's optimisation flags only strip 'assert' statements; an explicit
'if … raise ValueError(…)' is never affected.
"""

import sys

# Resolve project root so this script can be run from any working directory.
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from compliance.policy import RegulatoryPolicy


def _mode_label() -> str:
    if sys.flags.optimize == 0:
        return "DEFAULT"
    if sys.flags.optimize == 1:
        return "-O"
    return "-OO"


def run_proof() -> None:
    mode = _mode_label()
    failed = False

    # ── Test 1: "HUMAN" must raise ValueError ──────────────────────────────
    try:
        RegulatoryPolicy.validate_target("HUMAN")
        print(f"[FAIL] {mode} HUMAN → no exception raised (expected ValueError)")
        failed = True
    except ValueError as exc:
        expected = "Human scoring is strictly prohibited"
        if expected in str(exc):
            print(f"[PASS] {mode} HUMAN → ValueError: {exc}")
        else:
            print(f"[FAIL] {mode} HUMAN → ValueError raised but wrong message: {exc}")
            failed = True
    except AssertionError as exc:
        print(f"[FAIL] {mode} HUMAN → AssertionError (assert-based guard, not ValueError): {exc}")
        failed = True
    except Exception as exc:
        print(f"[FAIL] {mode} HUMAN → unexpected exception {type(exc).__name__}: {exc}")
        failed = True

    # ── Test 2: "MACHINE_ACCOUNT" must be accepted ─────────────────────────
    try:
        RegulatoryPolicy.validate_target("MACHINE_ACCOUNT")
        print(f"[PASS] {mode} MACHINE_ACCOUNT → accepted (no exception)")
    except Exception as exc:
        print(f"[FAIL] {mode} MACHINE_ACCOUNT → unexpected exception {type(exc).__name__}: {exc}")
        failed = True

    # ── Summary ────────────────────────────────────────────────────────────
    if failed:
        print(f"[RESULT] {mode} → FAIL")
        sys.exit(1)
    else:
        print(f"[RESULT] {mode} → PASS")


if __name__ == "__main__":
    run_proof()
