#!/usr/bin/env python3
"""
CR-003 — Layer 0 Statelessness / History Independence
CLASS B: Structural / Static Boundary Evidence

AST-based check proving that Layer 0 source files (core/*.py, excluding
test_*.py and offline_normalizer.py which is an offline preprocessing tool)
do NOT import or directly access:

  - PostgreSQL / database drivers     (psycopg2, psycopg, asyncpg, sqlalchemy,
                                        pg8000, aiopg, databases)
  - Audit persistence modules         (audit)
  - Compliance / policy modules       (compliance)
  - Network clients                   (requests, aiohttp, httpx, urllib3,
                                        socket, http.client)
  - Persistence / repository modules  (persistence, repository, repositories)
  - Historical aggregation services   (history, aggregation)

This check is narrowly scoped to the existing Layer 0/core boundary.
It supports CLAIM A ("core/evaluator.py has no database import") and
complements the runtime test which supports CLAIM B (history independence).
"""

import ast
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = REPO_ROOT / "artifacts"
BOUNDARY_ARTIFACT = ARTIFACT_DIR / "cr-003-layer-boundary.json"

# ---------------------------------------------------------------------------
# Forbidden top-level module names for Layer 0
# ---------------------------------------------------------------------------
FORBIDDEN_TOP_MODULES = frozenset(
    [
        # Database drivers
        "psycopg2",
        "psycopg",
        "asyncpg",
        "sqlalchemy",
        "pg8000",
        "aiopg",
        "databases",
        "tortoise",
        "peewee",
        "dataset",
        # Audit persistence
        "audit",
        # Compliance / policy
        "compliance",
        # Network clients
        "requests",
        "aiohttp",
        "httpx",
        "urllib3",
        "socket",
        # Persistence / repository abstractions
        "persistence",
        "repository",
        "repositories",
        # History / aggregation
        "history",
        "aggregation",
    ]
)

# ---------------------------------------------------------------------------
# Files in core/ that are excluded from this check
# ---------------------------------------------------------------------------
EXCLUDED_FILENAMES = frozenset(
    [
        "offline_normalizer.py",  # offline preprocessing tool; float + math permitted
        # Deprecated v3.3 backward-compatibility wrappers.
        # CHECK 3 (check_3_layer_separation.sh) also excludes these files.
        # They are intentionally retained for v3.3 compatibility and will be
        # removed in v4.0.  See docs/GAP-001.md CORE-005 / KL-001.
        "policy.py",
        "consistency.py",
    ]
)


def _get_commit_sha() -> str:
    import subprocess

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


def _extract_imports(tree: ast.AST) -> list[dict]:
    """Return all import statements as dicts with line, kind, modules."""
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(
                    {
                        "line": node.lineno,
                        "kind": "import",
                        "module": alias.name,
                        "top": alias.name.split(".")[0],
                    }
                )
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            imports.append(
                {
                    "line": node.lineno,
                    "kind": "from",
                    "module": module,
                    "top": module.split(".")[0] if module else "",
                }
            )
    return imports


def check_file(path: Path) -> list[dict]:
    """
    Parse a single Python file and return any forbidden import violations.
    """
    source = path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        return [{"file": str(path.relative_to(REPO_ROOT)), "error": str(exc)}]

    violations = []
    for imp in _extract_imports(tree):
        top = imp["top"]
        if top in FORBIDDEN_TOP_MODULES:
            violations.append(
                {
                    "file": str(path.relative_to(REPO_ROOT)),
                    "line": imp["line"],
                    "kind": imp["kind"],
                    "module": imp["module"],
                    "forbidden_top": top,
                }
            )
    return violations


def main() -> int:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    core_dir = REPO_ROOT / "core"
    if not core_dir.is_dir():
        print(f"❌ core/ directory not found at {core_dir}", file=sys.stderr)
        sys.exit(1)

    # Collect files: core/*.py, skip test_*.py and excluded files
    target_files: list[Path] = sorted(
        p
        for p in core_dir.glob("*.py")
        if not p.name.startswith("test_") and p.name not in EXCLUDED_FILENAMES
    )

    print("=" * 60)
    print("CR-003 — Layer 0 Static Boundary Check (AST)")
    print("=" * 60)
    print()
    print(f"Inspecting {len(target_files)} Layer 0 source file(s):")
    for f in target_files:
        print(f"  {f.relative_to(REPO_ROOT)}")
    print()

    all_violations: list[dict] = []
    file_results: list[dict] = []

    for path in target_files:
        violations = check_file(path)
        rel = str(path.relative_to(REPO_ROOT))
        file_results.append(
            {
                "file": rel,
                "violations": violations,
                "clean": len(violations) == 0,
            }
        )
        if violations:
            all_violations.extend(violations)
            print(f"❌ {rel}: {len(violations)} violation(s)")
            for v in violations:
                print(f"     line {v.get('line')}: {v.get('kind')} {v.get('module')!r} "
                      f"(forbidden: {v.get('forbidden_top')!r})")
        else:
            print(f"✅ {rel}: clean")

    print()
    overall_pass = len(all_violations) == 0
    result = {
        "test_name": "CR-003-layer-boundary",
        "commit_sha": _get_commit_sha(),
        "scope": "core/*.py (excluding test_*.py, offline_normalizer.py)",
        "forbidden_modules": sorted(FORBIDDEN_TOP_MODULES),
        "files_checked": [fr["file"] for fr in file_results],
        "file_results": file_results,
        "total_violations": len(all_violations),
        "violations": all_violations,
        "overall": "PASS" if overall_pass else "FAIL",
    }

    BOUNDARY_ARTIFACT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Artifact written: {BOUNDARY_ARTIFACT.relative_to(REPO_ROOT)}")
    print()

    if overall_pass:
        print("✅ CR-003 LAYER BOUNDARY CHECK PASSED")
        print("   Layer 0 (core/) contains no forbidden imports.")
        print("   CLAIM A: confirmed by static AST analysis.")
        return 0
    else:
        print("❌ CR-003 LAYER BOUNDARY CHECK FAILED")
        print(f"   {len(all_violations)} forbidden import(s) found in Layer 0.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
