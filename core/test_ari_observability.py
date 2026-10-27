"""
RD-006 — ARI Observability Harness (CHARACTERIZATION ONLY)
# NON-HERESY

## CURRENT BEHAVIOUR ≠ NORMATIVE REQUIREMENT

This module executes the real `core.evaluator.PoCAEvaluator` on fixed inputs and
records what it produces. It records:

    "This is what the implementation produces today."

It does NOT record:

    "This is what Aura requires."

Every observed value in this file is **IMPLEMENTATION-DERIVED / NON-NORMATIVE**.
No value here was taken from a specification, because no specification defines
ARI: the only occurrence of ARI in the specification corpus is
`glossary/GLOSSARY.md`, which defines it by reference to this implementation.
See `review/2026-08-11_ENGINEERING_BASELINE/05_CORE_REMEDIATION_READINESS.md` §7.1.

If an authorized decision (RD-1, RD-3, RD-4) later defines ARI, these tests are
expected to fail, and the constants are expected to be replaced deliberately as
part of that change — never silenced as incidental maintenance.

## Why this file exists

`scripts/generate_determinism_report.py` imports exactly three modules
(`core.offline_normalizer`, `audit.merkle`, `audit.signing`). It does not import
`core.evaluator`. Its `ari_vector_hash` vector hashes the *constitution vector*,
not an ARI. Consequently the cross-platform determinism comparison observes no
ARI arithmetic at all — recorded as CORE-P1-006.

This harness is the minimal observation point: it runs the real evaluation path
and emits a machine-readable observation record including platform identity, so
that the same record can later be compared across architectures.

## What this file does NOT do

- It does not fix CORE-P0-001 (vector-length truncation).
- It does not fix CORE-P0-002 (integer-division semantics).
- It does not fix CORE-P0/P1-003 (rounding semantics).
- It does not fix CORE-P1-004 (ARI range).
- It does not fix CORE-P1-005 (divergent engines) — it observes ONE engine,
  `core.evaluator.PoCAEvaluator`, and designates neither engine authoritative.
- It does not modify CI. Wiring this harness into the determinism pipeline is
  GB-2/GB-3 and remains blocked pending RD-6.

## Constitutional basis for adding this file

`CONSTITUTIONAL_DECREE.md` Article VII (Testing): new tests are permitted when
they enforce bit-identity and do not introduce non-deterministic behaviour.
This harness uses fixed inputs only — no clock, no RNG, no network, no I/O
dependency in the observed path.

Status: CHARACTERIZATION HARNESS (RD-006)
"""

import json
import platform
import unittest
from pathlib import Path
from unittest import mock

from core.evaluator import PoCAEvaluator

REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = REPO_ROOT / "artifacts"
OBSERVATION_ARTIFACT = ARTIFACT_DIR / "rd-006-ari-observation.json"

SCALE = PoCAEvaluator.SCALING_FACTOR  # 100000, read from the implementation

# ---------------------------------------------------------------------------
# Observation cases — fixed, synthetic, well-formed unless stated otherwise.
# ---------------------------------------------------------------------------
#
# Each case declares only its INPUT. No expected value is declared here; the
# expected values live in the IMPLEMENTATION_DERIVED table below and are
# labelled as such.

OBSERVATION_CASES = [
    {
        "id": "OBS-1",
        "description": "aligned unit vector, dim 4, valid schema",
        "constitution": [SCALE, 0, 0, 0],
        "vector": [SCALE, 0, 0, 0],
        "valid_schema": True,
        "touches_finding": None,
    },
    {
        "id": "OBS-2",
        "description": "orthogonal unit vectors, dim 4, valid schema",
        "constitution": [SCALE, 0, 0, 0],
        "vector": [0, SCALE, 0, 0],
        "valid_schema": True,
        "touches_finding": None,
    },
    {
        "id": "OBS-3",
        "description": "aligned unit vector, dim 1536 (the documented dimension)",
        "constitution": [SCALE] + [0] * 1535,
        "vector": [SCALE] + [0] * 1535,
        "valid_schema": True,
        "touches_finding": None,
    },
    {
        "id": "OBS-4",
        "description": "aligned unit vector, dim 4, INVALID schema (SI = 0)",
        "constitution": [SCALE, 0, 0, 0],
        "vector": [SCALE, 0, 0, 0],
        "valid_schema": False,
        "touches_finding": None,
    },
    {
        "id": "OBS-5",
        "description": (
            "anti-aligned, dim 4 — exercises the negative-dividend rescale. "
            "Observed value is integer-division-semantics dependent."
        ),
        "constitution": [-SCALE, 0, 0, 0],
        "vector": [1, 0, 0, 0],
        "valid_schema": True,
        "touches_finding": "CORE-P0-002",
    },
]

# ---------------------------------------------------------------------------
# IMPLEMENTATION-DERIVED / NON-NORMATIVE
# ---------------------------------------------------------------------------
#
# These values were obtained by executing the current implementation. They are
# recorded so that any change in behaviour becomes visible. They are NOT a
# specification, NOT approved, and NOT a statement that the values are correct.
#
# OBS-5 in particular is known to differ under truncating integer division
# (Rust / C / JS would yield ari=30000, drift=100000). Neither value is
# designated correct here; see CORE-P0-002.

IMPLEMENTATION_DERIVED_NON_NORMATIVE = {
    "OBS-1": {"ari": 100000, "drift": 0},
    "OBS-2": {"ari": 30000, "drift": 100000},
    "OBS-3": {"ari": 100000, "drift": 0},
    "OBS-4": {"ari": 70000, "drift": 0},
    "OBS-5": {"ari": 29999, "drift": 100001},
}


def _runtime_identity():
    """Platform / runtime identity, for cross-architecture comparison.

    Deterministic within a run and free of clocks and randomness.
    """
    return {
        "system": platform.system(),
        "machine": platform.machine(),
        "architecture": platform.architecture()[0],
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
    }


def _observe(case):
    """Execute the REAL evaluator for one case and return an observation record."""
    evaluator = PoCAEvaluator(case["constitution"])
    record = {
        "case_id": case["id"],
        "description": case["description"],
        "evaluator": "core.evaluator.PoCAEvaluator",
        "evaluator_module": PoCAEvaluator.__module__,
        "input": {
            "constitution_dim": len(case["constitution"]),
            "vector_dim": len(case["vector"]),
            "constitution_head": case["constitution"][:4],
            "vector_head": case["vector"][:4],
            "valid_schema": case["valid_schema"],
            "scaling_factor": SCALE,
        },
        "touches_finding": case["touches_finding"],
    }
    try:
        result = evaluator.evaluate(
            agent_id="RD-006-OBSERVATION",
            vector=case["vector"],
            valid_schema=case["valid_schema"],
        )
        record["execution"] = "SUCCESS"
        record["observed"] = {"ari": result["ari"], "drift": result["drift"]}
        record["error"] = None
    except Exception as exc:  # noqa: BLE001 — observation harness records any failure
        record["execution"] = "FAILURE"
        record["observed"] = None
        record["error"] = f"{type(exc).__name__}: {exc}"
    return record


def build_observation_report():
    """Build the full observation report for all cases."""
    return {
        "schema_version": "1.0",
        "report": "RD-006 ARI observation",
        "status": "CHARACTERIZATION — IMPLEMENTATION-DERIVED / NON-NORMATIVE",
        "normative_effect": "NONE",
        "note": (
            "Observed ARI values are implementation evidence and do not "
            "constitute a normative definition of ARI."
        ),
        "runtime": _runtime_identity(),
        "observations": [_observe(c) for c in OBSERVATION_CASES],
    }


class ARIObservabilityTest(unittest.TestCase):
    """Executes the real ARI path and records what it produces."""

    @classmethod
    def setUpClass(cls):
        cls.report = build_observation_report()
        ARTIFACT_DIR.mkdir(exist_ok=True)
        OBSERVATION_ARTIFACT.write_text(
            json.dumps(cls.report, indent=2, sort_keys=True), encoding="utf-8"
        )
        print("\n" + "=" * 70)
        print("RD-006 — ARI OBSERVATION RECORD")
        print("CHARACTERIZATION ONLY — IMPLEMENTATION-DERIVED / NON-NORMATIVE")
        print("=" * 70)
        print(json.dumps(cls.report, indent=2, sort_keys=True))
        print("=" * 70)
        print(f"artifact: {OBSERVATION_ARTIFACT}")
        print("=" * 70 + "\n")

    def test_all_cases_executed(self):
        """Every observation case reached the evaluator and produced a result."""
        for obs in self.report["observations"]:
            with self.subTest(case=obs["case_id"]):
                self.assertEqual(
                    obs["execution"],
                    "SUCCESS",
                    f"{obs['case_id']} did not execute: {obs['error']}",
                )
                self.assertIsNotNone(obs["observed"])

    def test_runtime_identity_is_recorded(self):
        """The record carries platform identity for cross-architecture comparison."""
        runtime = self.report["runtime"]
        for key in (
            "system",
            "machine",
            "architecture",
            "python_version",
            "python_implementation",
        ):
            self.assertIn(key, runtime)
            self.assertTrue(runtime[key], f"{key} must not be empty")

    def test_observed_values_match_implementation_derived_record(self):
        """
        IMPLEMENTATION-DERIVED / NON-NORMATIVE.

        Pins what the implementation produces today. A failure here means the
        evaluation path changed. That is the signal this harness exists to give;
        it is NOT evidence that the previous or new value is correct.
        """
        for obs in self.report["observations"]:
            expected = IMPLEMENTATION_DERIVED_NON_NORMATIVE[obs["case_id"]]
            with self.subTest(case=obs["case_id"]):
                self.assertEqual(
                    obs["observed"],
                    expected,
                    f"{obs['case_id']}: observed ARI changed. "
                    "IMPLEMENTATION-DERIVED value, not a normative requirement. "
                    "If intentional, record the authorizing decision.",
                )

    def test_report_declares_non_normative_status(self):
        """The emitted artifact must carry its own non-normative disclaimer."""
        self.assertEqual(self.report["normative_effect"], "NONE")
        self.assertIn("implementation evidence", self.report["note"])
        self.assertIn("IMPLEMENTATION-DERIVED", self.report["status"])


class HarnessIntegrityControlTest(unittest.TestCase):
    """
    CONTROL CASES.

    These prove the harness genuinely executes `core.evaluator` rather than
    reading, replaying, or hard-coding a result. Without them, the observations
    above would prove nothing.
    """

    def test_control_observation_tracks_evaluator_internals(self):
        """
        CONTROL: patching the evaluator's similarity function changes the
        observed ARI.

        If the harness were hard-coding or replaying a stored value, the
        observed output would be unaffected by this patch.
        """
        baseline = _observe(OBSERVATION_CASES[0])
        self.assertEqual(baseline["observed"]["ari"], 100000)

        with mock.patch.object(
            PoCAEvaluator, "vector_similarity_int32", return_value=0
        ):
            patched = _observe(OBSERVATION_CASES[0])

        self.assertEqual(
            patched["observed"]["ari"],
            30000,
            "CONTROL FAILED: observed ARI did not follow the evaluator's "
            "internals, so the harness is not executing the real path.",
        )
        self.assertNotEqual(
            baseline["observed"]["ari"],
            patched["observed"]["ari"],
            "CONTROL FAILED: the harness produced an identical value while the "
            "evaluator behaved differently.",
        )

        # And it recovers once the patch is lifted.
        restored = _observe(OBSERVATION_CASES[0])
        self.assertEqual(restored["observed"]["ari"], baseline["observed"]["ari"])

    def test_control_distinct_inputs_produce_distinct_observations(self):
        """
        CONTROL: the harness is input-sensitive, not a constant emitter.
        """
        aligned = _observe(OBSERVATION_CASES[0])
        orthogonal = _observe(OBSERVATION_CASES[1])
        self.assertNotEqual(
            aligned["observed"],
            orthogonal["observed"],
            "CONTROL FAILED: different inputs produced identical observations.",
        )

    def test_control_evaluator_failure_is_recorded_not_swallowed(self):
        """
        CONTROL: when the evaluator raises, the harness records FAILURE rather
        than silently reporting a value.
        """
        with mock.patch.object(
            PoCAEvaluator,
            "vector_similarity_int32",
            side_effect=RuntimeError("injected"),
        ):
            failed = _observe(OBSERVATION_CASES[0])

        self.assertEqual(failed["execution"], "FAILURE")
        self.assertIsNone(failed["observed"])
        self.assertIn("injected", failed["error"])

    def test_control_evaluator_is_the_real_module(self):
        """
        CONTROL: the observed evaluator is the production module, not a stub.
        """
        self.assertEqual(PoCAEvaluator.__module__, "core.evaluator")
        source_file = Path(PoCAEvaluator.__init__.__code__.co_filename).resolve()
        self.assertEqual(source_file, (REPO_ROOT / "core" / "evaluator.py").resolve())


if __name__ == "__main__":
    unittest.main(verbosity=2)
