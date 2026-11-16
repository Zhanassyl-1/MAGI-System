# Contributing to MAGI-System

This guide defines the mandatory engineering practices, Git conventions, and pull request procedures for all agents (and human engineers) contributing to the repository.

---

## 1. Universal Pre-Flight Protocol

Before executing any code changes or claiming work, every agent instance MUST perform the pre-flight routine:

```bash
# 1. Verify role onboarding and instruction files
python3 scripts/agent_onboard.py --agent <YOUR_AGENT_ID>

# 2. Update local tracking with remote
git checkout main
git pull origin main

# 3. Find and claim your next task
python3 scripts/magi.py next --agent <YOUR_AGENT_ID> --claim
```

---

## 2. Git Branching Standards

### 2.1 Main Branch Protection
- The `main` branch is the production release branch.
- **Direct commits or pushes to `main` are strictly prohibited.**
- Every change MUST be authored on an isolated branch and merged via Pull Request.

### 2.2 Branch Naming Pattern
All branches must adhere strictly to the pattern:
```
<team>/<agent-id>/<task-id>-<short-slug>
```

**Valid Examples:**
- `frontend/fe-1/task-003-navigation-bar`
- `frontend/fe-2/task-004-button-component`
- `backend/be-1/task-005-api-auth-routes`
- `backend/be-3/task-006-user-schema-migration`
- `qa/qa-2/task-007-button-accessibility-tests`
- `management/pm/task-008-sprint-backlog-expansion`

Branches not conforming to this structure will fail GitHub Actions PR validation.

---

## 3. Commit Message Standards (Conventional Commits)

Commit messages must be concise, descriptive, and follow the Conventional Commits specification:

```
<type>(<scope>): <short summary> (<task-id>)

[optional body explaining context or rationale]
```

### Allowed Types:
- `feat`: A new user-facing or API feature.
- `fix`: A bug fix.
- `refactor`: Code reorganization without functional changes.
- `test`: Adding or correcting tests.
- `docs`: Documentation updates.
- `chore`: Tooling, build config, dependency, or task tracking updates.

### Examples:
- `feat(ui): implement responsive navbar component (TASK-003)`
- `feat(auth): add JWT issuance and verification middleware (TASK-005)`
- `test(api): add contract validation tests for /api/login (TASK-007)`
- `fix(db): correct foreign key index in user migrations (TASK-006)`

---

## 4. Conflict Avoidance & Multi-Agent Isolation

Because 9 autonomous agents operate without shared memory:

1. **Strict Directory Isolation**:
   - Frontend developers work exclusively within frontend directories (`frontend/` or `src/client/`).
   - Backend developers work exclusively within backend directories (`backend/` or `src/server/`).
   - QA developers work in test suites (`tests/`, `e2e/`, `cypress/`, `jest/`).
   - Management edits task catalogs (`.magi/tasks/`).
2. **Distributed Task Locking**:
   - Always verify `.magi/locks/<TASK_ID>.lock` prior to modifying files.
   - The CLI `scripts/magi.py` manages locks automatically.
3. **Rebase Before PR**:
   - Always rebase your branch on the latest `origin/main` before requesting QA review:
     ```bash
     git fetch origin
     git rebase origin/main
     ```

---

## 5. Pull Request & Quality Gate Lifecycle

```
[Developer Branch]
       │
       ▼ (push & open PR)
[GitHub PR Created] ──► [CI Pipeline: Syntax, Linter & Tests]
                               │
                               ▼ (CI Passes)
                     [QA Team Review Assigned]
                               │
                ┌──────────────┴──────────────┐
                ▼                             ▼
       [Changes Requested]           [QA Approved Sign-off]
                │                             │
                ▼                             ▼
       (Developer fixes on branch)   [Squash & Merge to main]
                                              │
                                              ▼
                                     [python3 scripts/magi.py complete]
```

1. Fill out `.github/PULL_REQUEST_TEMPLATE.md` completely.
2. Ensure automated CI checks pass green.
3. Await QA review. Developers **cannot** approve their own or peer developer PRs.
4. Once merged, complete the task using `scripts/magi.py complete`.
