# MAGI-System: Backend Team Standard Operating Procedures

This document governs the operations, architectural guidelines, and collaboration protocols for the **Backend Team (BE-1, BE-2, BE-3)**.

---

## 1. Team Structure & Responsibilities

The Backend Team consists of three specialized agents operating concurrently without shared process memory:

| Agent | Role | Scope of Authority | Primary Branch Pattern |
| :--- | :--- | :--- | :--- |
| **BE-1** | API Architecture & Lead | Server routing, OpenAPI/contracts, migrations, middleware | `backend/be-1/task-xxx-*` |
| **BE-2** | Services Specialist | Domain business logic, third-party APIs, background tasks | `backend/be-2/task-xxx-*` |
| **BE-3** | Database & Security Specialist | Data modeling, indexing, auth (JWT/OAuth), security, sanitization | `backend/be-3/task-xxx-*` |

---

## 2. Architectural Guidelines

Regardless of backend language or framework (Node.js/Express, Python/FastAPI, Go, etc.), the following architectural rules are mandatory:

### 2.1 Layered Architecture
Backend source code resides strictly within the backend directory (e.g. `backend/` or `server/`):
- `controllers/` or `routes/`: Transport layer handling HTTP requests, headers, and status codes. Authored by **BE-1**.
- `services/`: Pure business logic layer decoupled from transport protocols. Authored by **BE-2**.
- `models/` & `db/`: Database schemas, ORM definitions, migrations, and query interfaces. Authored by **BE-3**.
- `middleware/`: Global authentication guards, request logging, rate limiting, and error handling. Authored jointly by **BE-1** and **BE-3**.

### 2.2 Contract-First Development
1. **Schema Authority**: **BE-1** must document endpoint contracts (OpenAPI/Swagger or JSON schema in `specs/api/`) before or simultaneously with endpoint creation.
2. **Predictable Responses**: All API responses must follow standardized enveloped structures:
   ```json
   {
     "success": true,
     "data": { ... },
     "error": null,
     "meta": { "timestamp": "...", "version": "1.0.0" }
   }
   ```
   Errors must return standard HTTP status codes (`400`, `401`, `403`, `404`, `422`, `500`) with actionable error messages.

### 2.3 Database Management & Migrations
- **Zero Raw Data Manipulation**: All database schema changes must be versioned migrations (`migrations/001_initial.sql` or framework-specific migration files).
- Migrations must be reversible (both `up` and `down` scripts provided).
- **BE-3** must ensure all foreign keys, unique constraints, and search indexes are properly declared.

### 2.4 Security Mandates (OWASP Compliant)
- **Zero Unparameterized Queries**: Never concatenate user input into raw SQL strings. Use parameterized queries or ORM bindings.
- **Secrets Management**: Secrets, API keys, and database passwords must never be committed to Git. Use environment variables with template documentation in `.env.example`.
- **Authentication & RBAC**: Endpoints must validate authentication tokens and verify user permissions before executing service actions.

---

## 3. Step-by-Step Backend Workflow

### Step 1: Onboarding Verification
```bash
python3 scripts/agent_onboard.py --agent BE-1   # (or BE-2, BE-3)
```
Confirm all team guidelines and global protocols are loaded.

### Step 2: Task Claiming & Branch Creation
```bash
python3 scripts/magi.py next --agent BE-1 --claim
```
This acquires the task lock in `.magi/locks/`, sets the task to `IN_PROGRESS`, and switches to the branch: `backend/<agent>/<task-id>-<slug>`.

### Step 3: Implementation
- Adhere to the layered directory separation.
- Ensure all business methods have corresponding unit tests.
- When adding or changing endpoints, update the API schema specification.

### Step 4: Local Quality Verification
Before submitting a PR, verify:
1. All unit and integration tests pass cleanly (`pytest`, `npm test`, etc.).
2. Database migrations apply cleanly (`up`) and revert cleanly (`down`).
3. Endpoint responds with correct status codes and error payloads.
4. Linter and type checker show zero errors.

### Step 5: Pull Request Submission
Push the branch to `origin`:
```bash
git push origin backend/be-1/task-002-auth-endpoints
```
Open a PR using `.github/PULL_REQUEST_TEMPLATE.md` and link the task:
```bash
python3 scripts/magi.py submit-pr TASK-002 --agent BE-1 --pr <PR_NUMBER>
```

### Step 6: QA Review & Resolution
- Notify **QA-3** (Backend QA Specialist) for API contract and security testing.
- Address any defect reports or edge-case failures identified by QA.
- Once QA approves and merges into `main`, complete the task:
```bash
python3 scripts/magi.py complete TASK-002 --agent BE-1
```
