# MAGI-System: Quality Assurance (QA) Standard Operating Procedures

This document governs the operations, testing standards, and merge gatekeeping protocols for the **QA Team (QA-1, QA-2, QA-3)**.

---

## 1. Team Structure & Responsibilities

The QA Team acts as the repository's independent quality authority. No code enters `main` without QA validation:

| Agent | Role | Scope of Authority | Primary Branch Pattern |
| :--- | :--- | :--- | :--- |
| **QA-1** | QA Lead & Merge Gatekeeper | Test framework, CI test pipelines, PR approvals & gatekeeping | `qa/qa-1/task-xxx-*` |
| **QA-2** | Frontend QA Specialist | UI/Component tests, visual regression, a11y, browser flows | `qa/qa-2/task-xxx-*` |
| **QA-3** | Backend QA Specialist | API contracts, schema verification, security tests, migrations | `qa/qa-3/task-xxx-*` |

---

## 2. The QA Gatekeeper Mandate

### Strict Merge Policy
1. **Zero Unapproved Merges**: Direct commits to `main` are strictly blocked. Pull Requests cannot be merged without formal sign-off from a QA Agent.
2. **Developer Independence**: Frontend and Backend developers (`FE-*`, `BE-*`) are strictly prohibited from signing off on their own or peer PRs.
3. **Audit Trail**: Every approved PR must have the **QA Sign-Off section** in `.github/PULL_REQUEST_TEMPLATE.md` completed with test execution logs and an explicit `APPROVED` verdict.

---

## 3. Testing Matrix & Standards

### 3.1 Frontend Testing Standards (Owned by QA-2)
- **Component Tests**: Every reusable component authored by FE-2 must have test coverage validating rendering, property passing, and user interaction (clicks, keystrokes).
- **Responsive Viewports**: UI views must be tested across mobile (375px), tablet (768px), and desktop (1280px) breakpoints.
- **Accessibility (a11y)**: Must verify proper ARIA labels, semantic landmark elements, contrast ratios, and tab navigation order.
- **Error Boundaries**: Verify UI displays graceful fallback messages rather than crashing on network errors or malformed payloads.

### 3.2 Backend Testing Standards (Owned by QA-3)
- **API Contract Verification**: Run automated tests ensuring request schemas and response bodies conform strictly to `specs/api/` schemas.
- **Status Code Accuracy**:
  - `200/201`: Valid requests.
  - `400/422`: Invalid payloads (ensure clear validation messages).
  - `401/403`: Unauthorized or forbidden attempts.
  - `404`: Non-existent resources.
- **Security & Negative Testing**: Attempt SQL injection strings, oversized payloads, malformed JSON, and missing authorization tokens to ensure the server rejects them securely.
- **Database Migrations**: Verify migration scripts apply cleanly (`up`) and rollback cleanly (`down`) without leaving corrupted tables.

### 3.3 End-to-End & Integration Testing (Owned by QA-1)
- Automated cross-tier user journeys testing full flows from frontend interface through backend services to database persistence.
- CI pipeline health: Ensure all GitHub Actions test workflows execute reliably on every PR.

---

## 4. Step-by-Step QA PR Review Protocol

When a developer submits a PR, it enters the `UNDER_QA` status:

### Step 1: Detect Active Review Queue
```bash
python3 scripts/magi.py list --status UNDER_QA
```

### Step 2: Checkout and Inspect Branch
```bash
git fetch origin
git checkout <branch-name>
git log -n 5
```

### Step 3: Execute Local Verification
1. Run linting and automated test suites:
   ```bash
   npm test || pytest
   ```
2. Inspect the acceptance criteria defined in `.magi/tasks/<TASK_ID>.json`.
3. Manually test edge cases and error scenarios.

### Step 4: Issue Review Verdict

#### If Deficiencies or Bugs Are Found:
1. File a bug report issue using `.github/ISSUE_TEMPLATE/bug_report.md`.
2. Update the PR with `CHANGES_REQUESTED`, providing clear, reproducible steps and error output.
3. The assigned developer remains on the branch to remediate the defect.

#### If All Acceptance Criteria & Tests Pass:
1. Complete the **QA Team Sign-Off** section in the PR:
   ```markdown
   ### QA Team Sign-Off (MANDATORY BEFORE MERGE)
   - [x] **QA Reviewer Assigned**: QA-1 (or QA-2, QA-3)
   - [x] **Test Coverage Verified**: 100% of acceptance criteria tested.
   - [x] **Requirements & Edge Cases Audited**: All boundary conditions verified.
   - [x] **Regression Risk Evaluated**: Zero regression detected.
   - [x] **VERDICT**: `APPROVED`
   ```
2. Label PR as `qa-approved`.
3. Perform the GitHub merge into `main` (Squash & Merge recommended).
4. Run task completion command:
   ```bash
   python3 scripts/magi.py complete <TASK_ID> --agent QA-1
   ```
5. Delete the merged feature branch.
