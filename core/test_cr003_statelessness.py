"""
CR-003 — Layer 0 Statelessness / History Independence
CLASS A: Runtime / Behavioral Evidence

Proves that Layer 0 measurement (PoCAEvaluator.evaluate) produces identical
output regardless of whether persisted audit history exists for the same agent.

Invariant:
    result_without_history == result_with_history

The test uses the repository's real PostgreSQL Docker environment to ensure
that merely populating the audit_events table (for the same agent_id) is
sufficient to create the populated-history condition, while the Layer 0
measurement inputs remain identical.

History records are NOT passed as explicit Layer 0 inputs; only the persisted
database state differs between the two evaluation calls.
"""

import ast
import json
import subprocess
import time
import unittest
from pathlib import Path

# ---------------------------------------------------------------------------
# Repository layout
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[1]
COMPOSE_FILE = REPO_ROOT / "docker-compose.yml"
ARTIFACT_DIR = REPO_ROOT / "artifacts"
RESULTS_FILE = ARTIFACT_DIR / "cr-003-statelessness-results.json"
LOG_FILE = ARTIFACT_DIR / "cr-003-statelessness.log"
PROJECT_NAME = "aura_cr003_statelessness"

# ---------------------------------------------------------------------------
# Fixed deterministic measurement inputs — these NEVER change between the
# two evaluation calls; only the persisted DB state differs.
# ---------------------------------------------------------------------------
TEST_AGENT_ID = "MACHINE_ACCOUNT_CR003_STATELESSNESS_001"

# Constitution vector: all components equal so norm is deterministic.
# Dimension 1536, all values = 3125 (≈ 100000/32, consistent with embed_text).
CONSTITUTION_VECTOR: list[int] = [3125] * 1536

# Agent action vector: same pattern, deterministic.
AGENT_VECTOR: list[int] = [3125] * 1536

# Schema validity flag.
VALID_SCHEMA: bool = True


def _log(msg: str) -> None:
    print(msg, flush=True)


# ---------------------------------------------------------------------------
# Helpers that mirror the CR-004 test infrastructure pattern
# ---------------------------------------------------------------------------

class TestCR003Statelessness(unittest.TestCase):
    """
    Runtime history-independence test.

    Flow
    ----
    1. Start fresh PostgreSQL container.
    2. Verify no audit rows exist for TEST_AGENT_ID (empty history).
    3. Call PoCAEvaluator.evaluate(TEST_AGENT_ID, AGENT_VECTOR, VALID_SCHEMA)
       → result_A (no history condition).
    4. Insert synthetic audit_events rows for TEST_AGENT_ID (populated history).
    5. Call PoCAEvaluator.evaluate(TEST_AGENT_ID, AGENT_VECTOR, VALID_SCHEMA)
       with the EXACT SAME inputs → result_B (history present).
    6. Assert result_A == result_B.
    """

    _result: dict = {}

    @classmethod
    def setUpClass(cls) -> None:
        ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
        cls._result = {
            "test_name": "CR-003-statelessness",
            "database_mode": "docker-compose-postgresql",
            "commit_sha": cls._get_commit_sha(),
        }
        cls._compose("down", "-v", "--remove-orphans", check=False)
        cls._compose("up", "-d")
        cls._wait_for_postgres()

    @classmethod
    def tearDownClass(cls) -> None:
        cls._write_results()
        cls._compose("down", "-v", "--remove-orphans", check=False)

    # ------------------------------------------------------------------
    # Infrastructure helpers
    # ------------------------------------------------------------------

    @classmethod
    def _get_commit_sha(cls) -> str:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()
        except Exception:
            return "UNKNOWN"

    @classmethod
    def _compose(cls, *args: str, check: bool = True) -> subprocess.CompletedProcess:
        cmd = [
            "docker", "compose",
            "-p", PROJECT_NAME,
            "-f", str(COMPOSE_FILE),
            *args,
        ]
        completed = subprocess.run(
            cmd,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        _log(f"[compose] {' '.join(args)} → exit {completed.returncode}")
        if completed.stdout.strip():
            _log(completed.stdout.strip())
        if completed.stderr.strip():
            _log(completed.stderr.strip())
        if check and completed.returncode != 0:
            raise AssertionError(
                f"docker compose {' '.join(args)} failed with exit code "
                f"{completed.returncode}\n{completed.stderr}"
            )
        return completed

    @classmethod
    def _psql(cls, sql: str, *, name: str, check: bool = True) -> subprocess.CompletedProcess:
        cmd = [
            "docker", "compose",
            "-p", PROJECT_NAME,
            "-f", str(COMPOSE_FILE),
            "exec", "-T", "postgres",
            "psql", "-U", "aura", "-d", "aura_core",
            "-X", "-v", "ON_ERROR_STOP=1",
            "-P", "pager=off",
            "-A", "-F", "|", "-t",
            "-c", sql,
        ]
        completed = subprocess.run(
            cmd,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        _log(f"[psql:{name}] exit={completed.returncode} stdout={completed.stdout.strip()!r}")
        if completed.stderr.strip():
            _log(f"[psql:{name}] stderr={completed.stderr.strip()!r}")
        if check and completed.returncode != 0:
            raise AssertionError(
                f"psql {name!r} failed (exit {completed.returncode}):\n{completed.stderr}"
            )
        return completed

    @classmethod
    def _wait_for_postgres(cls) -> None:
        _log("Waiting for PostgreSQL to become ready…")
        for _ in range(60):
            ready = cls._compose(
                "exec", "-T", "postgres",
                "pg_isready", "-U", "aura", "-d", "aura_core",
                check=False,
            )
            if ready.returncode == 0:
                _log("PostgreSQL is ready.")
                return
            time.sleep(2)
        raise AssertionError("PostgreSQL did not become ready within 120 s")

    @classmethod
    def _write_results(cls) -> None:
        RESULTS_FILE.write_text(
            json.dumps(cls._result, indent=2),
            encoding="utf-8",
        )

    # ------------------------------------------------------------------
    # Layer 0 evaluation helper (no DB involvement)
    # ------------------------------------------------------------------

    @staticmethod
    def _layer0_evaluate() -> dict:
        """
        Call PoCAEvaluator.evaluate with the fixed deterministic inputs.

        Imported here (not at module level) so that the import itself is
        local and the function cannot receive any DB reference.
        """
        from core.evaluator import PoCAEvaluator  # noqa: PLC0415

        evaluator = PoCAEvaluator(constitution_vector=CONSTITUTION_VECTOR)
        return evaluator.evaluate(
            agent_id=TEST_AGENT_ID,
            vector=AGENT_VECTOR,
            valid_schema=VALID_SCHEMA,
        )

    # ------------------------------------------------------------------
    # Test
    # ------------------------------------------------------------------

    def test_history_independence(self) -> None:
        """
        EMPTY_HISTORY_RESULT must equal POPULATED_HISTORY_RESULT.

        Historical records must NOT influence Layer 0 measurement.
        """
        _log("=" * 60)
        _log("CR-003 — History Independence Test")
        _log("=" * 60)

        # ── Phase 1: Verify empty history ────────────────────────────
        _log("\n── Phase 1: Verify empty history for test agent ──")
        count_result = self._psql(
            "SELECT COUNT(*)::text FROM audit_events "
            f"WHERE agent_id = $aid${TEST_AGENT_ID}$aid$;",
            name="count-history-before",
        )
        count_before = int(count_result.stdout.strip())
        _log(f"audit_events rows for {TEST_AGENT_ID!r}: {count_before}")
        self.assertEqual(
            count_before, 0,
            "Expected zero audit_events rows before evaluation (clean baseline)"
        )

        # ── Phase 2: Evaluate with empty history ────────────────────
        _log("\n── Phase 2: Layer 0 evaluation (no history) ──")
        result_a = self._layer0_evaluate()
        _log(f"result_A = {result_a}")
        self.__class__._result["empty_history_result"] = result_a

        # ── Phase 3: Insert historical audit data ───────────────────
        _log("\n── Phase 3: Insert historical audit_events rows ──")
        for i in range(3):
            event_hash = f"cr003{i:02d}{'0' * 57}"  # 5 + 2 + 57 = 64 chars
            merkle_root = f"mr003{i:02d}{'0' * 57}"  # 5 + 2 + 57 = 64 chars
            raw_ari = 68000 + i * 1000
            poca_score_cents = (raw_ari + 500) // 1000  # deterministic rounding
            poca_score = f"0.{poca_score_cents:02d}"
            certificate = json.dumps(
                {"RAW_ARI": raw_ari, "certificate_id": f"CERT-{i}", "merkle_root": merkle_root},
                separators=(",", ":"),
            )
            raw_event = json.dumps(
                {"agent_id": TEST_AGENT_ID, "measurement": "cr003_history_fixture"},
                separators=(",", ":"),
            )
            # Use dollar-quoting to safely embed values
            sql = (
                "INSERT INTO audit_events "
                "(agent_id, event_hash, merkle_root, poca_score, drift, status, raw_event, certificate) "
                "VALUES ("
                f"$agent${TEST_AGENT_ID}$agent$, "
                f"$ev${event_hash}$ev$, "
                f"$mr${merkle_root}$mr$, "
                f"{poca_score}, 0.32, 'COMPLIANT', "
                f"$re${raw_event}$re$::jsonb, "
                f"$cert${certificate}$cert$::jsonb"
                ");"
            )
            self._psql(sql, name=f"insert-history-row-{i}")

        count_result2 = self._psql(
            "SELECT COUNT(*)::text FROM audit_events "
            f"WHERE agent_id = $aid${TEST_AGENT_ID}$aid$;",
            name="count-history-after-insert",
        )
        count_after = int(count_result2.stdout.strip())
        _log(f"audit_events rows for {TEST_AGENT_ID!r} after insert: {count_after}")
        self.assertEqual(count_after, 3, "Expected 3 historical rows to be present")

        # ── Phase 4: Evaluate with populated history ─────────────────
        _log("\n── Phase 4: Layer 0 evaluation (history populated) ──")
        result_b = self._layer0_evaluate()
        _log(f"result_B = {result_b}")
        self.__class__._result["populated_history_result"] = result_b

        # ── Phase 5: Assert equality ──────────────────────────────────
        _log("\n── Phase 5: Assert EMPTY_HISTORY_RESULT == POPULATED_HISTORY_RESULT ──")
        fields_equal = (result_a == result_b)
        self.__class__._result["equality_result"] = fields_equal

        all_fields_passed = True
        for key in result_a:
            with self.subTest(field=key):
                if result_a[key] != result_b[key]:
                    all_fields_passed = False
                self.assertEqual(
                    result_a[key],
                    result_b[key],
                    f"Layer 0 field {key!r} differs between empty and populated history: "
                    f"{result_a[key]} != {result_b[key]}\n"
                    "CR-003 VIOLATION: persisted history influenced Layer 0 measurement.",
                )

        if all_fields_passed:
            _log(f"\n✅ CR-003 PASS: result_A == result_B ({result_a})")
            _log("Persisted audit history does NOT influence Layer 0 measurement.")
            self.__class__._result["overall"] = "PASS"
        else:
            self.__class__._result["overall"] = "FAIL"


if __name__ == "__main__":
    unittest.main(verbosity=2)
