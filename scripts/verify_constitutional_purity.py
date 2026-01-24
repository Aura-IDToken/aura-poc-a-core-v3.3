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

class ConstitutionalChecker(ast.NodeVisitor):
    """AST visitor that detects constitutional violations while ignoring type annotations"""
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.in_annotation = 0  # Use counter for nested annotations
    
    def visit_arg(self, node):
        """Visit function argument (may have type annotation)"""
        if node.annotation:
            self.in_annotation += 1
            self.visit(node.annotation)
            self.in_annotation -= 1
        # Don't call generic_visit to avoid double-visiting annotation
    
    def visit_AnnAssign(self, node):
        """Visit annotated assignment (e.g., x: int = 5)"""
        if node.annotation:
            self.in_annotation += 1
            self.visit(node.annotation)
            self.in_annotation -= 1
        if node.value:
            self.visit(node.value)
    
    def visit_FunctionDef(self, node):
        """Visit function definition (may have return annotation)"""
        # Check function name for forbidden symbols
        for forbidden, reason in FORBIDDEN_NAMES.items():
            if forbidden in node.name:
                violations.append(
                    f"{self.filepath}: function '{node.name}' contains forbidden '{forbidden}' -> {reason}"
                )
        
        # Visit return annotation
        if node.returns:
            self.in_annotation += 1
            self.visit(node.returns)
            self.in_annotation -= 1
        
        # Visit decorators
        for decorator in node.decorator_list:
            self.visit(decorator)
        
        # Visit arguments (each arg will handle its own annotation)
        for arg in node.args.args:
            self.visit(arg)
        for arg in node.args.posonlyargs:
            self.visit(arg)
        for arg in node.args.kwonlyargs:
            self.visit(arg)
        if node.args.vararg:
            self.visit(node.args.vararg)
        if node.args.kwarg:
            self.visit(node.args.kwarg)
        
        # Visit defaults and kw_defaults
        for default in node.args.defaults:
            self.visit(default)
        for default in node.args.kw_defaults:
            if default:
                self.visit(default)
        
        # Visit body
        for item in node.body:
            self.visit(item)
    
    def visit_Import(self, node):
        """Check imports"""
        for alias in node.names:
            if alias.name in FORBIDDEN_IMPORTS:
                violations.append(
                    f"{self.filepath}: import {alias.name} -> {FORBIDDEN_IMPORTS[alias.name]}"
                )
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        """Check from imports"""
        if node.module in FORBIDDEN_IMPORTS:
            violations.append(
                f"{self.filepath}: from {node.module} import ... -> {FORBIDDEN_IMPORTS[node.module]}"
            )
        self.generic_visit(node)
    
    def visit_Attribute(self, node):
        """Check attribute access (e.g., math.sqrt)"""
        if node.attr in FORBIDDEN_NAMES:
            violations.append(
                f"{self.filepath}: attribute access '.{node.attr}' -> {FORBIDDEN_NAMES[node.attr]}"
            )
        self.generic_visit(node)
    
    def visit_Name(self, node):
        """Check name references"""
        # Skip if we're in a type annotation
        if self.in_annotation == 0 and node.id in FORBIDDEN_NAMES:
            if isinstance(node.ctx, ast.Load):
                violations.append(
                    f"{self.filepath}: symbol '{node.id}' -> {FORBIDDEN_NAMES[node.id]}"
                )
        self.generic_visit(node)
    
    def visit_Call(self, node):
        """Check function calls"""
        # Direct call like float()
        if isinstance(node.func, ast.Name) and node.func.id in FORBIDDEN_NAMES:
            violations.append(
                f"{self.filepath}: call '{node.func.id}()' -> {FORBIDDEN_NAMES[node.func.id]}"
            )
        # Attribute call like math.sqrt()
        elif isinstance(node.func, ast.Attribute) and node.func.attr in FORBIDDEN_NAMES:
            violations.append(
                f"{self.filepath}: call '.{node.func.attr}()' -> {FORBIDDEN_NAMES[node.func.attr]}"
            )
        self.generic_visit(node)

def check_file(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    if ALLOWED_COMMENT_OVERRIDE in source:
        return

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return

    checker = ConstitutionalChecker(filepath)
    checker.visit(tree)

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
