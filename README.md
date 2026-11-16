# MAGI-System

Autonomous multi-agent software engineering organization designed for 9 specialized AI coding agents and a central project manager operating through a single GitHub repository.

---

## 🏛️ System Architecture

MAGI-System organizes agents into functional domain teams with strict boundary isolation, git-mediated state synchronization, and an independent QA gatekeeper model:

```
                               ┌────────────────────────┐
                               │  PROJECT MANAGER (PM)  │
                               │  MAGI Central Director │
                               └───────────┬────────────┘
                                           │
         ┌─────────────────────────────────┼─────────────────────────────────┐
         │                                 │                                 │
         ▼                                 ▼                                 ▼
┌──────────────────┐             ┌──────────────────┐             ┌──────────────────┐
│  FRONTEND TEAM   │             │   BACKEND TEAM   │             │     QA TEAM      │
│  (3 Agents)      │             │   (3 Agents)     │             │   (3 Agents)     │
├──────────────────┤             ├──────────────────┤             ├──────────────────┤
│ FE-1: UI Lead    │             │ BE-1: API Lead   │             │ QA-1: QA Lead    │
│ FE-2: Components │             │ BE-2: Services   │             │ QA-2: FE Tests   │
│ FE-3: Integrate  │             │ BE-3: DB/Auth    │             │ QA-3: BE Tests   │
└──────────────────┘             └──────────────────┘             └──────────────────┘
```

---

## 📑 Core Documentation Index

- **[AGENTS.md](AGENTS.md)**: Agent roster, role definitions, operational loops, and domain boundaries.
- **[PROJECT_PLAN.md](PROJECT_PLAN.md)**: Lifecycle phases, milestone definitions of done, and roadmap.
- **[TASKS.md](TASKS.md)**: Live master task matrix, status workflows, and distributed lock rules.
- **[FRONTEND.md](FRONTEND.md)**: Frontend team standard operating procedures, layout, and component rules.
- **[BACKEND.md](BACKEND.md)**: Backend team standard operating procedures, API contracts, database, and security.
- **[QA.md](QA.md)**: QA team gatekeeper model, testing standards, and merge authorization policies.
- **[MANAGER.md](MANAGER.md)**: Project manager workflows, task decomposition, and deadlock resolution.
- **[CONTRIBUTING.md](CONTRIBUTING.md)**: Git conventions, branch naming patterns, and PR guidelines.

---

## 🛠️ Tooling & Scripts

The repository includes standalone CLI utilities located in `scripts/`:
- `python3 scripts/agent_onboard.py --agent <ID>`: Pre-flight role verification and rule checklist.
- `python3 scripts/magi.py list`: View current task matrix and statuses.
- `python3 scripts/magi.py next --agent <ID> [--claim]`: Algorithmic task recommendation and automated claiming.
- `python3 scripts/magi.py claim <TASK_ID> --agent <ID>`: Acquire distributed task lock and checkout branch.
- `python3 scripts/magi.py submit-pr <TASK_ID> --agent <ID> --pr <PR_NUM>`: Update task status after opening a PR.
- `python3 scripts/magi.py complete <TASK_ID> --agent <ID>`: Finalize task upon PR merge and release lock.
- `python3 scripts/magi.py sync-board`: Synchronize `TASKS.md` from `.magi/tasks/` definitions.
- `python3 scripts/validate_pr.py`: Enforce branch naming conventions and PR template compliance.

---

## 🔒 Key Operational Axioms

1. **GitHub is the Single Source of Truth**: All tasks, state, and code changes are committed to Git.
2. **Zero Shared Memory**: No shared daemon or runtime process is assumed across agent instances.
3. **Branch Isolation**: Direct commits to `main` are prohibited. All work occurs on `<team>/<agent>/<task-id>-<slug>`.
4. **Mandatory QA Gate**: Pull requests require formal sign-off from the QA Team prior to merge.
