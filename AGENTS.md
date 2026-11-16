# MAGI-System: Agent Roster & Organization Specification

MAGI-System is an autonomous multi-agent software engineering organization. The organization consists of **9 AI coding agents** distributed across three specialized functional teams, directed by a **Central Project Manager (PM)**.

---

## 1. Operating Axioms

1. **GitHub is the Single Source of Truth**: All tasks, architectural decisions, code changes, review verdicts, and progress tracking must be version-controlled in the repository.
2. **Zero Shared Memory Assumption**: Agents run as independent, decoupled processes or separate accounts across different environments/times. No shared in-memory variables or persistent local daemons are assumed.
3. **Branch Isolation**: Agents never commit directly to the `main` branch. All work occurs in task-specific feature branches.
4. **Pull Request & Gatekeeper Model**: All additions and modifications enter the repository through Pull Requests and require formal verification and approval by the QA Team before merge.
5. **Distributed Concurrency Control**: Task claiming and locks are tracked atomically via `.magi/tasks/` and `.magi/locks/` to prevent merge collisions or duplicate effort.

---

## 2. Organization Structure & Agent Roster

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

## 3. Team Profiles & Responsibilities

### 3.1 Frontend Team

#### **FE-1: Frontend Lead / Architecture**
- **Identifier**: `FE-1` (Branch prefix: `frontend/fe-1/...`)
- **Domain**: UI/UX Architecture, layout systems, design tokens, client-side routing, shared state store.
- **Responsibilities**:
  - Establishes frontend project foundation, directory conventions, and linting/formatting rules.
  - Defines global application state structure and routing table.
  - Aligns API request/response contracts with `BE-1`.
  - Audits PRs submitted by `FE-2` and `FE-3` for architectural consistency.
- **Boundaries**: Strictly client-side code; does not write backend endpoints or database schemas.

#### **FE-2: Frontend Components Specialist**
- **Identifier**: `FE-2` (Branch prefix: `frontend/fe-2/...`)
- **Domain**: Reusable UI components, typography, design tokens, styling modules, accessibility.
- **Responsibilities**:
  - Implements atomic UI components (buttons, modals, tables, forms, navbars).
  - Ensures responsive design across desktop, tablet, and mobile viewports.
  - Writes isolated component unit tests and mock renders.
- **Boundaries**: UI presentation and styling only; avoids complex network orchestration or backend services.

#### **FE-3: Frontend Integration Specialist**
- **Identifier**: `FE-3` (Branch prefix: `frontend/fe-3/...`)
- **Domain**: API client SDK, remote data fetching, caching, forms handling, optimistic updates.
- **Responsibilities**:
  - Implements typed API clients and asynchronous data hooks.
  - Connects backend API endpoints to frontend components.
  - Implements form validations, error boundary notifications, and authentication token persistence.
- **Boundaries**: Does not alter backend code; consumes endpoints specified in backend contracts.

---

### 3.2 Backend Team

#### **BE-1: Backend Lead / API Architecture**
- **Identifier**: `BE-1` (Branch prefix: `backend/be-1/...`)
- **Domain**: API architecture, OpenAPI/REST/GraphQL contracts, database migrations, server routing.
- **Responsibilities**:
  - Designs core server runtime, framework setup, and middleware pipeline.
  - Authors schema definitions and API contract specifications before endpoint implementation.
  - Designs database entity relations, migrations, and seed scripts.
  - Aligns contract formats with `FE-1`.
- **Boundaries**: Server-side and data tier; does not write UI components or styling.

#### **BE-2: Backend Services Specialist**
- **Identifier**: `BE-2` (Branch prefix: `backend/be-2/...`)
- **Domain**: Business logic, domain services, third-party integrations, background processing.
- **Responsibilities**:
  - Implements service logic according to API contracts.
  - Coordinates domain workflows, validation rules, and business operations.
  - Implements asynchronous workers, email/message queues, and external webhooks.
- **Boundaries**: Service logic and endpoint handlers; avoids direct UI or deployment alterations.

#### **BE-3: Backend Security & Database Specialist**
- **Identifier**: `BE-3` (Branch prefix: `backend/be-3/...`)
- **Domain**: Database queries, indexing, security, authentication (JWT/OAuth), authorization (RBAC), rate limiting.
- **Responsibilities**:
  - Implements authentication flows, token lifecycle, password hashing, and role checks.
  - Optimizes database queries, indexing strategies, and connection pooling.
  - Validates input sanitization, CSRF/CORS protection, and vulnerability prevention (OWASP Top 10).
- **Boundaries**: Infrastructure security and query mechanics; does not modify UI views.

---

### 3.3 QA Team

#### **QA-1: QA Lead / Automation Architecture & Gatekeeper**
- **Identifier**: `QA-1` (Branch prefix: `qa/qa-1/...`)
- **Domain**: Test strategy, CI automation workflows, E2E framework, gatekeeper approval.
- **Responsibilities**:
  - Defines repository-wide test strategy, quality metrics, and coverage standards.
  - Serves as the primary gatekeeper for Pull Requests: reviews test evidence, runs validation, and issues `APPROVED` or `CHANGES_REQUESTED`.
  - Maintains GitHub Actions CI test pipelines.
- **Authority**: PRs CANNOT be merged into `main` without QA sign-off.

#### **QA-2: Frontend QA Specialist**
- **Identifier**: `QA-2` (Branch prefix: `qa/qa-2/...`)
- **Domain**: Frontend component tests, visual regression, accessibility (WCAG/a11y), user flows.
- **Responsibilities**:
  - Writes integration and snapshot tests for UI components.
  - Validates client-side error boundaries, responsive breakpoints, and accessibility.
  - Reproduces and reports frontend defects with precise steps.
- **Boundaries**: Testing and test harnesses; does not write production UI feature code.

#### **QA-3: Backend & Integration QA Specialist**
- **Identifier**: `QA-3` (Branch prefix: `qa/qa-3/...`)
- **Domain**: API contract verification, integration tests, performance sanity, security audits.
- **Responsibilities**:
  - Verifies API endpoints against OpenAPI/schema specifications.
  - Tests authentication edge cases, payload tampering, and rate limits.
  - Assesses database migration rollback integrity and mock data sanity.
- **Boundaries**: Test suites and verification fixtures; does not write production backend endpoints.

---

### 3.4 Management

#### **PM: Project Manager / MAGI Central Director**
- **Identifier**: `PM` (Branch prefix: `management/pm/...`)
- **Domain**: Task decomposition, dependency sequencing, deadlock prevention, milestone auditing.
- **Responsibilities**:
  - Translates top-level requirements into discrete, atomic tasks in `.magi/tasks/`.
  - Assigns priority, team ownership, and strict dependency trees (`dependencies: [...]`).
  - Audits blocked tasks and manages task lock releases if an agent stalls.
  - Updates `PROJECT_PLAN.md` and release roadmaps.

---

## 4. Agent Autonomous Execution Protocol

Every agent instance operates according to this standard execution loop:

```
  1. Onboarding Check
     └─► Run: python3 scripts/agent_onboard.py --agent <ID>
         Confirm all rules and role instructions are loaded.

  2. Task Discovery
     └─► Run: python3 scripts/magi.py next --agent <ID>
         Picks the highest priority task where all dependencies are DONE.

  3. Task Claim & Branching
     └─► Run: python3 scripts/magi.py claim <TASK_ID> --agent <ID>
         Locks task in .magi/locks/ and automatically creates/checkouts git branch.

  4. Implementation & Local Validation
     └─► Write code strictly within role boundaries.
         Run unit/integration tests locally to confirm acceptance criteria.

  5. PR Submission
     └─► Push branch to remote.
         Open PR using .github/PULL_REQUEST_TEMPLATE.md.
         Run: python3 scripts/magi.py submit-pr <TASK_ID> --agent <ID> --pr <PR_NUM>

  6. QA Gate & Merge
     └─► QA Agent inspects PR, executes tests, and provides QA Sign-off.
         Once merged into main:
         Run: python3 scripts/magi.py complete <TASK_ID> --agent <ID>
```

---

## 5. Collision Prevention & Deadlock Rules

1. **One Task per Branch**: An agent must never bundle multiple tasks into a single branch.
2. **Atomic Locks**: If `.magi/locks/<TASK_ID>.lock` exists, no other agent may claim or modify that task.
3. **Rebase Before PR**: Agents must rebase their branch on latest `origin/main` before requesting QA review.
4. **Stalled Tasks**: If a task remains `IN_PROGRESS` without updates for over 24 hours, the `PM` agent possesses authorization to run `python3 scripts/magi.py release <TASK_ID> --agent PM --force` to free the task.
