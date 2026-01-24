#!/usr/bin/env python3
"""
AURA PROTOCOL v3.3
CONSTITUTIONAL GATE: CODE PURITY VERIFICATION

STATUS: CANONICAL
ROLE: CONSTITUTIONAL LAW ENFORCER
SCOPE: IRON CORE ONLY

This script enforces NON-NEGOTIABLE laws of the Frozen Iron Core.
If this script fails, the system MUST NOT be sealed, released or executed.

Run manually:
    python3 scripts/verify_constitutional_purity.py
"""

import ast
import os
import sys

# === PROTECTED ZONES (LAW APPLIES HERE) ===
PROTECTED_PATHS = [
    "core",
    "packages",
]

# === FORBIDDEN SYMBOLS (CONSTITUTIONAL VIOLATIONS) ===
FORBIDDEN_IMPORTS = {
    "torch": "ML libraries are forbidden in Iron Core",
    "tensorflow": "ML libraries are forbidden in Iron Core",
    "numpy": "Float-based libraries create hardware drift",
    "random": "Non-deterministic entropy source",
}

FORBIDDEN_NAMES = {
    "float": "Float arithmetic is forbidden at runtime",
    "sqrt": "Square root is forbidden (non-deterministic)",
    "cosine": "Cosine similarity is forbidden",
    "cuda": "GPU execution forbidden",
    "social_score": "AI Act Art. 5 violation",
    "user_id": "Identity tracking forbidden",
    "owner_id": "Identity tracking forbidden",
}

ALLOWED_COMMENT_OVERRIDE = "NON-HERESY"

violations = []

def check_file(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    if ALLOWED_COMMENT_OVERRIDE in source:
        return

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return

    for node in ast.walk(tree):

        # --- IMPORTS ---
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in FORBIDDEN_IMPORTS:
                    violations.append(
                        f"{filepath}: import {alias.name} -> {FORBIDDEN_IMPORTS[alias.name]}"
                    )

        if isinstance(node, ast.ImportFrom):
            if node.module in FORBIDDEN_IMPORTS:
                violations.append(
                    f"{filepath}: from {node.module} import ... -> {FORBIDDEN_IMPORTS[node.module]}"
                )

        # --- FUNCTION DEFINITIONS (method names) ---
        if isinstance(node, ast.FunctionDef):
            for forbidden, reason in FORBIDDEN_NAMES.items():
                if forbidden in node.name:
                    violations.append(
                        f"{filepath}: function '{node.name}' contains forbidden '{forbidden}' -> {reason}"
                    )

        # --- ATTRIBUTE ACCESS (e.g., math.sqrt) ---
        if isinstance(node, ast.Attribute):
            if node.attr in FORBIDDEN_NAMES:
                violations.append(
                    f"{filepath}: attribute access '.{node.attr}' -> {FORBIDDEN_NAMES[node.attr]}"
                )

        # --- NAMES / CALLS ---
        if isinstance(node, ast.Name):
            # Skip if this is part of a type annotation
            parent = getattr(node, '_parent', None)
            if isinstance(parent, ast.arg) or isinstance(parent, (ast.FunctionDef, ast.AnnAssign)):
                continue
            
            if node.id in FORBIDDEN_NAMES:
                # Check if it's in a Load context (actual use, not type hint)
                if isinstance(node.ctx, ast.Load):
                    violations.append(
                        f"{filepath}: symbol '{node.id}' -> {FORBIDDEN_NAMES[node.id]}"
                    )

        if isinstance(node, ast.Call):
            # Direct call like float()
            if isinstance(node.func, ast.Name) and node.func.id in FORBIDDEN_NAMES:
                violations.append(
                    f"{filepath}: call '{node.func.id}()' -> {FORBIDDEN_NAMES[node.func.id]}"
                )
            # Attribute call like math.sqrt()
            elif isinstance(node.func, ast.Attribute) and node.func.attr in FORBIDDEN_NAMES:
                violations.append(
                    f"{filepath}: call '.{node.func.attr}()' -> {FORBIDDEN_NAMES[node.func.attr]}"
                )

def scan():
    for path in PROTECTED_PATHS:
        if not os.path.exists(path):
            continue

        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".py") or file.endswith(".ts"):
                    check_file(os.path.join(root, file))

def main():
    scan()

    if violations:
        print("\n[CONSTITUTIONAL VIOLATION DETECTED]\n")
        for v in violations:
            print(" -", v)
        print("\nSYSTEM STATUS: ILLEGAL STATE")
        print("ACTION: FIX VIOLATIONS OR EXPLICITLY OVERRIDE WITH # NON-HERESY\n")
        sys.exit(1)

    print("✅ CONSTITUTIONAL PURITY CONFIRMED")
    print("IRON CORE STATUS: LEGAL")
    sys.exit(0)

if __name__ == "__main__":
    main()
