import json
import subprocess
import time
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
COMPOSE_FILE = REPO_ROOT / "docker-compose.yml"
ARTIFACT_DIR = REPO_ROOT / "artifacts"
RESULTS_FILE = ARTIFACT_DIR / "db-append-only-results.json"
PROJECT_NAME = "aura_cr004_append_only"


class TestAuditEventsAppendOnlyIntegration(unittest.TestCase):
    operations = []

    @classmethod
    def setUpClass(cls):
        cls.operations = []
        ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
        cls._compose("down", "-v", "--remove-orphans", check=False)
        cls._compose("up", "-d")
        cls._wait_for_postgres()

    @classmethod
    def tearDownClass(cls):
        cls._write_results()
        cls._compose("down", "-v", "--remove-orphans", check=False)

    @classmethod
    def _write_results(cls):
        RESULTS_FILE.write_text(json.dumps({"operations": cls.operations}, indent=2), encoding="utf-8")

    @staticmethod
    def _sql_literal(value):
        return str(value).replace("'", "''")

    @classmethod
    def _run(cls, command, *, name, check=True):
        completed = subprocess.run(
            command,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        cls.operations.append(
            {
                "name": name,
                "command": command,
                "returncode": completed.returncode,
                "stdout": completed.stdout.strip(),
                "stderr": completed.stderr.strip(),
            }
        )
        if check and completed.returncode != 0:
            raise AssertionError(
                f"{name} failed with exit code {completed.returncode}\n"
                f"STDOUT:\n{completed.stdout}\nSTDERR:\n{completed.stderr}"
            )
        return completed

    @classmethod
    def _compose(cls, *args, check=True):
        return cls._run(
            [
                "docker",
                "compose",
                "-p",
                PROJECT_NAME,
                "-f",
                str(COMPOSE_FILE),
                *args,
            ],
            name=f"docker compose {' '.join(args)}",
            check=check,
        )

    @classmethod
    def _psql(cls, sql, *, name, check=True):
        return cls._run(
            [
                "docker",
                "compose",
                "-p",
                PROJECT_NAME,
                "-f",
                str(COMPOSE_FILE),
                "exec",
                "-T",
                "postgres",
                "psql",
                "-U",
                "aura",
                "-d",
                "aura_core",
                "-X",
                "-v",
                "ON_ERROR_STOP=1",
                "-P",
                "pager=off",
                "-A",
                "-F",
                "|",
                "-t",
                "-c",
                sql,
            ],
            name=name,
            check=check,
        )

    @classmethod
    def _wait_for_postgres(cls):
        for _ in range(60):
            ready = cls._compose(
                "exec",
                "-T",
                "postgres",
                "pg_isready",
                "-U",
                "aura",
                "-d",
                "aura_core",
                check=False,
            )
            if ready.returncode == 0:
                return
            time.sleep(2)
        raise AssertionError("PostgreSQL did not become ready in time")

    @staticmethod
    def _insert_sql(*, agent_id, event_hash, merkle_root, raw_ari, poca_score):
        certificate = json.dumps(
            {
                "RAW_ARI": raw_ari,
                "certificate_id": f"CERT-{event_hash[:8]}",
                "merkle_root": merkle_root,
            },
            separators=(",", ":"),
        )
        raw_event = json.dumps(
            {
                "agent_id": agent_id,
                "measurement": "append_only_evidence",
                "raw_ari": raw_ari,
            },
            separators=(",", ":"),
        )
        return (
            "INSERT INTO audit_events "
            "(agent_id, event_hash, merkle_root, poca_score, drift, status, raw_event, certificate) "
            "VALUES ("
            f"'{TestAuditEventsAppendOnlyIntegration._sql_literal(agent_id)}', "
            f"'{TestAuditEventsAppendOnlyIntegration._sql_literal(event_hash)}', "
            f"'{TestAuditEventsAppendOnlyIntegration._sql_literal(merkle_root)}', "
            f"{poca_score}, 0.32, "
            f"'COMPLIANT', "
            f"'{TestAuditEventsAppendOnlyIntegration._sql_literal(raw_event)}'::jsonb, "
            f"'{TestAuditEventsAppendOnlyIntegration._sql_literal(certificate)}'::jsonb"
            ") "
            "RETURNING id, event_hash, poca_score::text, certificate->>'RAW_ARI';"
        )

    def test_append_only_enforcement(self):
        identity_columns = self._psql(
            (
                "SELECT COALESCE("
                "string_agg(table_name || '.' || column_name, ',' ORDER BY table_name, column_name),"
                "''"
                ") "
                "FROM information_schema.columns "
                "WHERE table_schema = 'public' "
                "AND column_name IN ('owner_id', 'user_id', 'wallet_id', 'human_id', 'person_id');"
            ),
            name="identity-column-scan",
        )
        self.assertEqual(identity_columns.stdout.strip(), "")

        insert_result = self._psql(
            self._insert_sql(
                agent_id="MACHINE_ACCOUNT_APPEND_ONLY_001",
                event_hash="a" * 64,
                merkle_root="b" * 64,
                raw_ari=68000,
                poca_score="0.68",
            ),
            name="insert-valid-audit-event",
        )
        self.assertIn("|0.68|68000", insert_result.stdout.strip())

        stored_values = self._psql(
            (
                "SELECT poca_score::text, "
                "jsonb_typeof(certificate->'RAW_ARI'), "
                "certificate->>'RAW_ARI', "
                "pg_typeof(poca_score)::text "
                "FROM audit_events "
                "WHERE event_hash = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa';"
            ),
            name="select-stored-audit-event",
        )
        self.assertEqual(stored_values.stdout.strip(), "0.68|number|68000|numeric")

        invalid_fractional_raw_ari = self._psql(
            self._insert_sql(
                agent_id="MACHINE_ACCOUNT_APPEND_ONLY_002",
                event_hash="c" * 64,
                merkle_root="d" * 64,
                raw_ari=68000.5,
                poca_score="0.68",
            ),
            name="insert-invalid-fractional-raw-ari",
            check=False,
        )
        self.assertNotEqual(invalid_fractional_raw_ari.returncode, 0)
        self.assertIn("audit_events_certificate_raw_ari_integer_chk", invalid_fractional_raw_ari.stderr)

        invalid_derived_score = self._psql(
            self._insert_sql(
                agent_id="MACHINE_ACCOUNT_APPEND_ONLY_003",
                event_hash="e" * 64,
                merkle_root="f" * 64,
                raw_ari=68000,
                poca_score="0.67",
            ),
            name="insert-invalid-derived-poca-score",
            check=False,
        )
        self.assertNotEqual(invalid_derived_score.returncode, 0)
        self.assertIn("audit_events_poca_score_matches_raw_ari_chk", invalid_derived_score.stderr)

        update_result = self._psql(
            (
                "UPDATE audit_events "
                "SET status = 'DRIFT' "
                "WHERE event_hash = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa';"
            ),
            name="update-rejected",
            check=False,
        )
        self.assertNotEqual(update_result.returncode, 0)
        self.assertIn("append-only", update_result.stderr)

        delete_result = self._psql(
            (
                "DELETE FROM audit_events "
                "WHERE event_hash = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa';"
            ),
            name="delete-rejected",
            check=False,
        )
        self.assertNotEqual(delete_result.returncode, 0)
        self.assertIn("append-only", delete_result.stderr)

        transaction_result = self._psql(
            (
                "BEGIN; "
                "INSERT INTO audit_events "
                "(agent_id, event_hash, merkle_root, poca_score, drift, status, raw_event, certificate) "
                "VALUES ("
                "'MACHINE_ACCOUNT_APPEND_ONLY_004', "
                "'1111111111111111111111111111111111111111111111111111111111111111', "
                "'2222222222222222222222222222222222222222222222222222222222222222', "
                "0.95, 0.05, 'COMPLIANT', "
                "'{\"agent_id\":\"MACHINE_ACCOUNT_APPEND_ONLY_004\",\"measurement\":\"txn_integrity\",\"raw_ari\":95000}'::jsonb, "
                "'{\"RAW_ARI\":95000,\"certificate_id\":\"CERT-11111111\",\"merkle_root\":\"2222222222222222222222222222222222222222222222222222222222222222\"}'::jsonb"
                "); "
                "DELETE FROM audit_events "
                "WHERE event_hash = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'; "
                "COMMIT;"
            ),
            name="transaction-delete-rejected",
            check=False,
        )
        self.assertNotEqual(transaction_result.returncode, 0)
        self.assertIn("append-only", transaction_result.stderr)

        integrity_result = self._psql(
            (
                "SELECT "
                "(SELECT COUNT(*) FROM audit_events)::text, "
                "EXISTS("
                "SELECT 1 FROM audit_events "
                "WHERE event_hash = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'"
                ")::text, "
                "EXISTS("
                "SELECT 1 FROM audit_events "
                "WHERE event_hash = '1111111111111111111111111111111111111111111111111111111111111111'"
                ")::text;"
            ),
            name="post-transaction-integrity-check",
        )
        self.assertEqual(integrity_result.stdout.strip(), "1|true|false")


if __name__ == "__main__":
    unittest.main(verbosity=2)
