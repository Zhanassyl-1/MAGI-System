#!/usr/bin/env python3
"""
MAGI-System PR Validation Script
Checks branch naming conventions, task associations, and PR requirements.
Can be executed locally or inside GitHub Actions CI.
"""

import argparse
import os
import re
import subprocess
import sys

BRANCH_PATTERN = re.compile(r"^(frontend|backend|qa|management)/(fe-[1-3]|be-[1-3]|qa-[1-3]|pm)/task-[0-9]{3,}-[\w-]+$")


def run_git(args):
    return subprocess.run(["git"] + args, capture_output=True, text=True)


def check_branch_name(branch_name: str) -> bool:
    if branch_name in ["main", "master"]:
        print(f"[FAIL] Direct operations on '{branch_name}' are forbidden.", file=sys.stderr)
        return False
    if not BRANCH_PATTERN.match(branch_name.lower()):
        print(
            f"[FAIL] Branch '{branch_name}' does not match required convention:\n"
            f"       <team>/<agent-id>/<task-id>-<slug>\n"
            f"       Example: frontend/fe-2/task-004-button-component",
            file=sys.stderr
        )
        return False
    print(f"[PASS] Branch name '{branch_name}' complies with MAGI standard.")
    return True


def check_pr_body(pr_body: str) -> bool:
    required_sections = [
        "### Task ID",
        "### Agent ID",
        "### Team",
        "### Summary of Changes",
        "### Verification Checklist"
    ]
    missing = [sec for sec in required_sections if sec not in pr_body]
    if missing:
        print(f"[FAIL] PR description missing mandatory sections: {missing}", file=sys.stderr)
        return False
    print("[PASS] PR description contains all mandatory sections.")
    return True


def main():
    parser = argparse.ArgumentParser(description="MAGI PR Compliance Checker")
    parser.add_argument("--branch", help="Branch name to validate (defaults to current git branch)")
    parser.add_argument("--pr-body-file", help="Path to file containing PR description body")
    args = parser.parse_args()
    
    success = True
    
    branch = args.branch
    if not branch:
        res = run_git(["rev-parse", "--abbrev-ref", "HEAD"])
        if res.returncode == 0:
            branch = res.stdout.strip()
            
    if branch:
        if not check_branch_name(branch):
            success = False
            
    if args.pr_body_file:
        if os.path.exists(args.pr_body_file):
            with open(args.pr_body_file, "r", encoding="utf-8") as f:
                body = f.read()
            if not check_pr_body(body):
                success = False
        else:
            print(f"[WARN] PR body file '{args.pr_body_file}' not found.")
            
    if not success:
        sys.exit(1)
        
    print("[PASS] All PR validation checks passed successfully.")


if __name__ == "__main__":
    main()
