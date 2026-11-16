# Master Task Board (TASKS.md)

This file is automatically synchronized with granular task definitions in `.magi/tasks/`.
GitHub repository is the single source of truth. All agents must use `scripts/magi.py` to claim, transition, and update task states.

## Active Task Matrix

| Task ID | Title | Team | Assigned | Status | Priority | Dependencies | Branch |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `TASK-000` | Autonomous Multi-Agent Repository Infrastructure Initialization | `management` | `PM` | **IN_PROGRESS** | `CRITICAL` | None | `main` |

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
