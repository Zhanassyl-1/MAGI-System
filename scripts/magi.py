#!/usr/bin/env python3
"""
MAGI-System Task Manager CLI
Autonomous coordination tool for 9-agent software engineering team.
Maintains single-source-of-truth in Git without shared daemon process.
"""

import argparse
import datetime
import glob
import json
import os
import re
import subprocess
import sys
from typing import Dict, List, Optional, Any

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TASKS_DIR = os.path.join(REPO_ROOT, ".magi", "tasks")
LOCKS_DIR = os.path.join(REPO_ROOT, ".magi", "locks")
LOGS_DIR = os.path.join(REPO_ROOT, ".magi", "logs")
TASKS_MD = os.path.join(REPO_ROOT, "TASKS.md")
PROGRESS_LOG = os.path.join(LOGS_DIR, "progress.log")

TEAM_MAP = {
    "fe-1": "frontend",
    "fe-2": "frontend",
    "fe-3": "frontend",
    "be-1": "backend",
    "be-2": "backend",
    "be-3": "backend",
    "qa-1": "qa",
    "qa-2": "qa",
    "qa-3": "qa",
    "pm": "management",
}

PRIORITY_WEIGHT = {
    "CRITICAL": 4,
    "HIGH": 3,
    "MEDIUM": 2,
    "LOW": 1,
}


def get_agent_team(agent_id: str) -> Optional[str]:
    return TEAM_MAP.get(agent_id.lower())


def load_all_tasks() -> Dict[str, Dict[str, Any]]:
    tasks = {}
    if not os.path.exists(TASKS_DIR):
        return tasks
    for path in glob.glob(os.path.join(TASKS_DIR, "TASK-*.json")):
        if os.path.basename(path) == "template.json":
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                tasks[data["id"]] = data
        except Exception as e:
            print(f"[WARN] Error reading {path}: {e}", file=sys.stderr)
    return tasks


def save_task(task_data: Dict[str, Any]) -> str:
    task_id = task_data["id"]
    slug = re.sub(r"[^a-zA-Z0-9_-]", "-", task_data["title"].lower())[:40].strip("-")
    filename = f"{task_id}-{slug}.json"
    
    # Check if file with this ID already exists under another slug
    existing_files = glob.glob(os.path.join(TASKS_DIR, f"{task_id}*.json"))
    if existing_files:
        filepath = existing_files[0]
    else:
        filepath = os.path.join(TASKS_DIR, filename)
        
    task_data["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(task_data, f, indent=2)
    return filepath


def get_lock_file(task_id: str) -> str:
    return os.path.join(LOCKS_DIR, f"{task_id}.lock")


def is_task_locked(task_id: str) -> Optional[Dict[str, Any]]:
    lock_file = get_lock_file(task_id)
    if os.path.exists(lock_file):
        try:
            with open(lock_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"locked": True, "agent": "unknown"}
    return None


def acquire_lock(task_id: str, agent_id: str) -> bool:
    lock_file = get_lock_file(task_id)
    existing_lock = is_task_locked(task_id)
    if existing_lock:
        if existing_lock.get("agent", "").lower() == agent_id.lower():
            return True  # Already held by this agent
        return False
        
    os.makedirs(LOCKS_DIR, exist_ok=True)
    lock_data = {
        "task_id": task_id,
        "agent": agent_id.upper(),
        "claimed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "pid": os.getpid(),
    }
    with open(lock_file, "w", encoding="utf-8") as f:
        json.dump(lock_data, f, indent=2)
    return True


def release_lock(task_id: str, agent_id: str, force: bool = False) -> bool:
    lock_file = get_lock_file(task_id)
    if not os.path.exists(lock_file):
        return True
    existing_lock = is_task_locked(task_id)
    if existing_lock and not force:
        if existing_lock.get("agent", "").lower() != agent_id.lower() and agent_id.lower() != "pm":
            print(f"[ERROR] Lock is held by {existing_lock.get('agent')}, cannot be released by {agent_id}.", file=sys.stderr)
            return False
    try:
        os.remove(lock_file)
        return True
    except OSError as e:
        print(f"[ERROR] Failed to remove lock file: {e}", file=sys.stderr)
        return False


def dependencies_satisfied(task: Dict[str, Any], all_tasks: Dict[str, Any]) -> bool:
    deps = task.get("dependencies", [])
    for dep_id in deps:
        if dep_id not in all_tasks or all_tasks[dep_id].get("status") != "DONE":
            return False
    return True


def run_git_command(args: List[str]) -> subprocess.CompletedProcess:
    return subprocess.run(["git"] + args, cwd=REPO_ROOT, text=True, capture_output=True)


def create_and_checkout_branch(branch_name: str) -> bool:
    res = run_git_command(["checkout", "-b", branch_name])
    if res.returncode != 0:
        # Maybe branch already exists
        res2 = run_git_command(["checkout", branch_name])
        return res2.returncode == 0
    return True


def sync_tasks_md():
    tasks = load_all_tasks()
    sorted_tasks = sorted(tasks.values(), key=lambda t: t.get("id", ""))
    
    table_lines = [
        "| Task ID | Title | Team | Assigned | Status | Priority | Dependencies | Branch |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
    ]
    
    for t in sorted_tasks:
        tid = t.get("id", "")
        title = t.get("title", "")
        team = t.get("team", "")
        assigned = t.get("assigned_agent") or "-"
        status = t.get("status", "TODO")
        priority = t.get("priority", "MEDIUM")
        deps = ", ".join(t.get("dependencies", [])) or "None"
        branch = t.get("branch") or "-"
        table_lines.append(f"| `{tid}` | {title} | `{team}` | `{assigned}` | **{status}** | `{priority}` | {deps} | `{branch}` |")

    tasks_table_str = "\n".join(table_lines)
    
    content = f"""# Master Task Board (TASKS.md)

This file is automatically synchronized with granular task definitions in `.magi/tasks/`.
GitHub repository is the single source of truth. All agents must use `scripts/magi.py` to claim, transition, and update task states.

## Active Task Matrix

{tasks_table_str}

## Task Status Workflow

```
[ BACKLOG ]
     │
     ▼
  [ TODO ] ──(Dependencies Met)──► [ CLAIMED ]
                                        │
                                        ▼
                                 [ IN_PROGRESS ] (Agent working on branch)
                                        │
                                        ▼
                                  [ PR_OPEN ]
                                        │
                                        ▼
                                  [ UNDER_QA ]  ◄── QA Agent Review & Tests
                                    │        │
                     (Changes Req'd)│        │(QA Approved)
                                    ▼        ▼
                             [ IN_PROGRESS ][ APPROVED ]
                                                 │
                                                 ▼
                                              [ DONE ] (Merged to main)
```

## Concurrency and Distributed Locking
- Each claimed task locks `.magi/locks/<TASK_ID>.lock`.
- No agent may claim a task already locked or in progress by another agent.
- Independent agents operating across separate processes/machines coordinate exclusively through git-committed states.
"""
    with open(TASKS_MD, "w", encoding="utf-8") as f:
        f.write(content)


def log_progress(event_type: str, task_id: str, agent_id: str, message: str):
    os.makedirs(LOGS_DIR, exist_ok=True)
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    log_entry = f"[{timestamp}] [{event_type}] [Agent: {agent_id}] [Task: {task_id}] {message}\n"
    with open(PROGRESS_LOG, "a", encoding="utf-8") as f:
        f.write(log_entry)


# CLI Subcommand Handlers

def cmd_list(args):
    tasks = load_all_tasks()
    filtered = []
    for t in tasks.values():
        if args.team and t.get("team") != args.team.lower():
            continue
        if args.status and t.get("status") != args.status.upper():
            continue
        filtered.append(t)
        
    filtered.sort(key=lambda t: t.get("id"))
    print(f"\n{'ID':<10} {'TEAM':<12} {'ASSIGNED':<10} {'STATUS':<14} {'PRIORITY':<10} {'TITLE'}")
    print("-" * 80)
    for t in filtered:
        print(f"{t['id']:<10} {t.get('team', ''):<12} {str(t.get('assigned_agent') or '-'):<10} {t.get('status', ''):<14} {t.get('priority', ''):<10} {t.get('title', '')}")
    print(f"\nTotal tasks: {len(filtered)}\n")


def cmd_next(args):
    agent_id = args.agent.upper()
    team = get_agent_team(agent_id)
    if not team:
        print(f"[ERROR] Unknown agent ID: {agent_id}. Valid IDs: {list(TEAM_MAP.keys())}", file=sys.stderr)
        sys.exit(1)
        
    tasks = load_all_tasks()
    
    # Check if agent already has an active task
    active = [t for t in tasks.values() if t.get("assigned_agent") == agent_id and t.get("status") in ["CLAIMED", "IN_PROGRESS", "PR_OPEN", "UNDER_QA"]]
    if active:
        print(f"[INFO] Agent {agent_id} already has active task(s):")
        for t in active:
            print(f"  -> {t['id']}: {t['title']} ({t['status']})")
        if not args.force:
            print("To claim another task concurrently, use --force or complete active work.")
            return

    # Filter tasks for this team with status TODO & dependencies satisfied
    available = []
    for t in tasks.values():
        if t.get("status") != "TODO":
            continue
        if team != "management" and t.get("team") != team:
            continue
        if is_task_locked(t["id"]):
            continue
        if dependencies_satisfied(t, tasks):
            available.append(t)
            
    if not available:
        print(f"[INFO] No eligible tasks ready for pickup by team '{team}'.")
        return
        
    # Sort by priority then ID
    available.sort(key=lambda t: (-PRIORITY_WEIGHT.get(t.get("priority", "MEDIUM"), 1), t["id"]))
    best_task = available[0]
    
    print(f"\n[NEXT TASK RECOMMENDATION]")
    print(f"  Task ID:     {best_task['id']}")
    print(f"  Title:       {best_task['title']}")
    print(f"  Team:        {best_task['team']}")
    print(f"  Priority:    {best_task['priority']}")
    print(f"  Description: {best_task['description']}")
    print(f"  Acceptance Criteria:")
    for c in best_task.get("acceptance_criteria", []):
        print(f"    - {c}")
    print()

    if args.claim:
        claim_task(best_task["id"], agent_id, create_branch=not args.no_branch)


def claim_task(task_id: str, agent_id: str, create_branch: bool = True):
    tasks = load_all_tasks()
    if task_id not in tasks:
        print(f"[ERROR] Task {task_id} does not exist.", file=sys.stderr)
        sys.exit(1)
        
    task = tasks[task_id]
    team = get_agent_team(agent_id)
    if team != "management" and task.get("team") != team:
        print(f"[ERROR] Agent {agent_id} ({team}) cannot claim task for team {task.get('team')}.", file=sys.stderr)
        sys.exit(1)
        
    if not dependencies_satisfied(task, tasks):
        print(f"[ERROR] Dependencies not satisfied for {task_id}. Required: {task.get('dependencies')}", file=sys.stderr)
        sys.exit(1)
        
    if not acquire_lock(task_id, agent_id):
        lock_info = is_task_locked(task_id)
        print(f"[ERROR] Cannot claim {task_id}: locked by {lock_info.get('agent')}", file=sys.stderr)
        sys.exit(1)
        
    slug = re.sub(r"[^a-zA-Z0-9_-]", "-", task["title"].lower())[:30].strip("-")
    branch_name = f"{task['team']}/{agent_id.lower()}/{task_id.lower()}-{slug}"
    
    task["assigned_agent"] = agent_id.upper()
    task["status"] = "IN_PROGRESS"
    task["branch"] = branch_name
    
    save_task(task)
    sync_tasks_md()
    log_progress("CLAIM", task_id, agent_id, f"Claimed task and created branch {branch_name}")
    
    print(f"[SUCCESS] Claimed {task_id} for agent {agent_id}.")
    
    if create_branch:
        print(f"[GIT] Creating/switching to branch: {branch_name}")
        create_and_checkout_branch(branch_name)
        print(f"[GIT] Active branch is now {branch_name}")


def cmd_claim(args):
    claim_task(args.task_id.upper(), args.agent.upper(), create_branch=not args.no_branch)


def cmd_release(args):
    task_id = args.task_id.upper()
    agent_id = args.agent.upper()
    tasks = load_all_tasks()
    if task_id not in tasks:
        print(f"[ERROR] Task {task_id} not found.", file=sys.stderr)
        sys.exit(1)
        
    task = tasks[task_id]
    if not release_lock(task_id, agent_id, force=args.force):
        sys.exit(1)
        
    task["assigned_agent"] = None
    task["status"] = "TODO"
    save_task(task)
    sync_tasks_md()
    log_progress("RELEASE", task_id, agent_id, f"Released task back to TODO. Reason: {args.reason or 'None'}")
    print(f"[SUCCESS] Task {task_id} released and reset to TODO.")


def cmd_submit_pr(args):
    task_id = args.task_id.upper()
    agent_id = args.agent.upper()
    tasks = load_all_tasks()
    if task_id not in tasks:
        print(f"[ERROR] Task {task_id} not found.", file=sys.stderr)
        sys.exit(1)
        
    task = tasks[task_id]
    task["status"] = "UNDER_QA"
    task["pr_number"] = args.pr
    save_task(task)
    sync_tasks_md()
    log_progress("PR_SUBMIT", task_id, agent_id, f"Submitted PR #{args.pr} for QA review.")
    print(f"[SUCCESS] Task {task_id} status updated to UNDER_QA (PR #{args.pr}).")


def cmd_complete(args):
    task_id = args.task_id.upper()
    agent_id = args.agent.upper()
    tasks = load_all_tasks()
    if task_id not in tasks:
        print(f"[ERROR] Task {task_id} not found.", file=sys.stderr)
        sys.exit(1)
        
    task = tasks[task_id]
    task["status"] = "DONE"
    task["completed_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    release_lock(task_id, agent_id, force=True)
    save_task(task)
    sync_tasks_md()
    log_progress("COMPLETE", task_id, agent_id, f"Task marked DONE and lock released.")
    print(f"[SUCCESS] Task {task_id} completed successfully.")


def cmd_sync(args):
    sync_tasks_md()
    print("[SUCCESS] TASKS.md synchronized with .magi/tasks/ definitions.")


def cmd_status(args):
    tasks = load_all_tasks()
    counts = {}
    for t in tasks.values():
        st = t.get("status", "UNKNOWN")
        counts[st] = counts.get(st, 0) + 1
        
    print("\n=== MAGI-System Overview ===")
    print(f"Total Tasks: {len(tasks)}")
    for status, count in sorted(counts.items()):
        print(f"  {status:<15}: {count}")
        
    locks = glob.glob(os.path.join(LOCKS_DIR, "*.lock"))
    print(f"\nActive Locks: {len(locks)}")
    for lock in locks:
        try:
            with open(lock, "r") as f:
                d = json.load(f)
                print(f"  Lock {os.path.basename(lock)}: Held by {d.get('agent')} since {d.get('claimed_at')}")
        except Exception:
            pass
    print()


def main():
    parser = argparse.ArgumentParser(description="MAGI-System Autonomous Task Manager CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # list
    p_list = subparsers.add_parser("list", help="List tasks")
    p_list.add_argument("--team", choices=["frontend", "backend", "qa", "management"], help="Filter by team")
    p_list.add_argument("--status", help="Filter by status (TODO, IN_PROGRESS, DONE, etc.)")
    p_list.set_defaults(func=cmd_list)
    
    # next
    p_next = subparsers.add_parser("next", help="Find next eligible task for agent")
    p_next.add_argument("--agent", required=True, help="Agent ID (e.g. FE-1, BE-2, QA-3)")
    p_next.add_argument("--claim", action="store_true", help="Automatically claim the task")
    p_next.add_argument("--no-branch", action="store_true", help="Do not switch git branch automatically")
    p_next.add_argument("--force", action="store_true", help="Ignore active task checks")
    p_next.set_defaults(func=cmd_next)
    
    # claim
    p_claim = subparsers.add_parser("claim", help="Claim a specific task")
    p_claim.add_argument("task_id", help="Task ID (e.g. TASK-001)")
    p_claim.add_argument("--agent", required=True, help="Agent ID")
    p_claim.add_argument("--no-branch", action="store_true", help="Do not create/switch branch")
    p_claim.set_defaults(func=cmd_claim)
    
    # release
    p_release = subparsers.add_parser("release", help="Release a claimed task")
    p_release.add_argument("task_id", help="Task ID")
    p_release.add_argument("--agent", required=True, help="Agent ID")
    p_release.add_argument("--reason", help="Reason for releasing task")
    p_release.add_argument("--force", action="store_true", help="Force release another agent's lock (PM only)")
    p_release.set_defaults(func=cmd_release)
    
    # submit-pr
    p_submit = subparsers.add_parser("submit-pr", help="Update task after opening PR")
    p_submit.add_argument("task_id", help="Task ID")
    p_submit.add_argument("--agent", required=True, help="Agent ID")
    p_submit.add_argument("--pr", type=int, required=True, help="Pull Request number")
    p_submit.set_defaults(func=cmd_submit_pr)
    
    # complete
    p_complete = subparsers.add_parser("complete", help="Mark task as DONE after PR merge")
    p_complete.add_argument("task_id", help="Task ID")
    p_complete.add_argument("--agent", required=True, help="Agent ID")
    p_complete.set_defaults(func=cmd_complete)
    
    # sync-board
    p_sync = subparsers.add_parser("sync-board", help="Synchronize TASKS.md with .magi/tasks/")
    p_sync.set_defaults(func=cmd_sync)
    
    # status
    p_status = subparsers.add_parser("status", help="Show system status and locks")
    p_status.set_defaults(func=cmd_status)
    
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
