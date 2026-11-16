# MAGI-System: Project Manager (PM) Operating Guide & Workflow

This document governs the central coordination, task decomposition, dependency management, and release auditing workflows for the **Project Manager (PM)**.

---

## 1. Role & Authority

The **Project Manager (PM)** is the central coordinator of MAGI-System:
- **Authority**: High-level task creation, priority assignment, dependency graph enforcement, and lock resolution.
- **Single Source of Truth**: The PM maintains the backlog and active roadmap strictly through GitHub issues, `.magi/tasks/`, `TASKS.md`, and `PROJECT_PLAN.md`.
- **Decoupled Architecture**: The PM operates as an independent agent process without requiring direct shared memory with developer agents.

---

## 2. Core PM Workflows

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. INTAKE & DECOMPOSITION                                                   │
│    Decompose requirements into atomic, single-responsibility tasks.         │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. DEPENDENCY SEQUENCING                                                    │
│    Assign strict dependency trees (e.g. BE Models ──► Endpoints ──► FE Client)│
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 3. TASK PUBLISHING & BOARD SYNC                                             │
│    Generate .magi/tasks/TASK-XXX.json and run sync-board.                   │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 4. AUDIT & BOTTLENECK RESOLUTION                                            │
│    Audit active locks, detect stalled agents, resolve blocked dependencies. │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 5. MILESTONE ADVANCEMENT                                                    │
│    Verify Phase Definition of Done and update PROJECT_PLAN.md.              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Task Decomposition Methodology

When new project requirements are provided:
1. **Granularity**: A task should represent 1-3 hours of coding effort for an AI agent, modifying no more than 3-8 related files.
2. **Acceptance Criteria**: Each task MUST have 3-5 unambiguous, testable acceptance criteria.
3. **Team Separation**: Tasks must be assigned strictly to a single team (`frontend`, `backend`, `qa`, or `management`). Never create a single task that requires editing both frontend and backend code.

### Standard Dependency Chain:
```
[BE: Data Models (BE-3)]
         │
         ▼
[BE: API Endpoints (BE-1)] ──► [QA: API Contract Test (QA-3)]
         │
         ▼
[FE: API Client / Integration (FE-3)] ◄── [FE: UI Components (FE-2)]
         │
         ▼
[FE: Complete View (FE-1)] ──► [QA: UI E2E Flow (QA-2)]
```

---

## 4. Task Creation Protocol

To create a new task:
1. Copy `.magi/tasks/template.json` to `.magi/tasks/TASK-<NUM>-<slug>.json`.
2. Fill out all required fields adhering to `.magi/schemas/task.schema.json`:
   ```json
   {
     "id": "TASK-005",
     "title": "Implement User Authentication REST Endpoints",
     "team": "backend",
     "assigned_agent": null,
     "status": "TODO",
     "priority": "HIGH",
     "dependencies": ["TASK-002"],
     "description": "Create /api/auth/register and /api/auth/login endpoints with JWT issuance.",
     "acceptance_criteria": [
       "POST /api/auth/register validates email format and password strength",
       "POST /api/auth/login returns valid JWT and user profile",
       "Invalid credentials return HTTP 401 with structured error payload",
       "Passes unit and integration tests"
     ],
     "branch": null,
     "pr_number": null,
     "created_at": "2026-11-16T22:00:00Z",
     "updated_at": "2026-11-16T22:00:00Z",
     "completed_at": null
   }
   ```
3. Synchronize `TASKS.md`:
   ```bash
   python3 scripts/magi.py sync-board
   ```

---

## 5. Concurrency Auditing & Deadlock Resolution

Because agents operate across independent processes without shared memory:

### 5.1 Stalled Task Detection
Run periodic audits:
```bash
python3 scripts/magi.py status
```
Inspect `.magi/locks/`:
- If an agent claimed a task but pushed no commits or PR within the expected timeframe, the PM investigates.
- To release a stale lock held by another agent:
  ```bash
  python3 scripts/magi.py release TASK-005 --agent PM --force --reason "Agent timeout / stalled process"
  ```
- The task reverts to `TODO`, allowing another agent on the team to pick it up via `python3 scripts/magi.py next`.

### 5.2 Circular Dependency Prevention
- The PM must ensure task dependency graphs are Directed Acyclic Graphs (DAGs).
- A task can never depend on a task that depends on it directly or indirectly.

---

## 6. Milestone & Phase Sign-Off

At the completion of each lifecycle phase (Phases 0 through 5):
1. The PM verifies that 100% of tasks in that phase have reached `status: "DONE"`.
2. Confirms that all PRs are merged into `main` and all CI workflows are green.
3. Updates the milestone checklists in `PROJECT_PLAN.md`.
4. Appends a milestone summary entry into `.magi/logs/progress.log`.
