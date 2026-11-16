# MAGI-System: Frontend Team Standard Operating Procedures

This document governs the operations, architectural guidelines, and collaboration protocols for the **Frontend Team (FE-1, FE-2, FE-3)**.

---

## 1. Team Structure & Responsibilities

The Frontend Team consists of three specialized agents working concurrently without shared memory:

| Agent | Role | Scope of Authority | Primary Branch Pattern |
| :--- | :--- | :--- | :--- |
| **FE-1** | UI Architecture & Lead | Routing, state architecture, layout shell, design tokens | `frontend/fe-1/task-xxx-*` |
| **FE-2** | Component Specialist | Atomic UI components, responsive styles, accessibility | `frontend/fe-2/task-xxx-*` |
| **FE-3** | Integration Specialist | API client, remote state, forms, client validation | `frontend/fe-3/task-xxx-*` |

---

## 2. Architectural Guidelines

Regardless of the specific frontend framework chosen (React, Vue, Svelte, Next.js, or vanilla web standards), the following architectural tenets are strictly enforced:

### 2.1 Modularity & Directory Boundaries
- Frontend source code resides strictly within the designated frontend root (e.g. `frontend/` or `src/`).
- **Forbidden**: Frontend agents must never modify backend directories (`backend/`, `server/`, `api/`) or database schemas.
- Code must follow atomic design patterns:
  - `components/ui/`: Dumb, reusable presentation components (buttons, badges, inputs, dialogs) authored by **FE-2**.
  - `components/layout/`: Global layout components (navbars, sidebars, page wrappers) authored by **FE-1**.
  - `features/`: Domain-specific feature modules connecting views, authored jointly by **FE-1** and **FE-3**.
  - `services/api/`: Typed API client modules and fetch wrappers authored by **FE-3**.

### 2.2 Contract-First Integration
- **FE-3** must never invent or guess API payloads. Integration must strictly consume schemas published in backend contracts (e.g., OpenAPI specs in `specs/api/`).
- If an endpoint contract is not yet finalized or backend is under construction, **FE-3** must use typed mock fixtures matching the agreed contract specification.

### 2.3 Responsive Design & Accessibility (a11y)
- All UI layouts must support responsive viewports:
  - Mobile: 320px - 767px
  - Tablet: 768px - 1023px
  - Desktop: 1024px+
- All interactive components authored by **FE-2** must include proper semantic HTML elements, ARIA attributes (`aria-label`, `aria-expanded`), and full keyboard navigation (Tab, Enter, Escape).

---

## 3. Step-by-Step Frontend Workflow

### Step 1: Onboarding Verification
Before taking any action, run:
```bash
python3 scripts/agent_onboard.py --agent FE-1   # (or FE-2, FE-3)
```
Ensure you have reviewed `CONTRIBUTING.md`, `AGENTS.md`, `TASKS.md`, and this document.

### Step 2: Task Claiming & Branch Creation
Find the next available task prioritized for your team:
```bash
python3 scripts/magi.py next --agent FE-2 --claim
```
This automatically locks the task in `.magi/locks/`, sets the task status to `IN_PROGRESS`, and switches your working directory to the designated branch: `frontend/<agent>/<task-id>-<slug>`.

### Step 3: Implementation
- Write clean, type-safe, maintainable code.
- Keep commits small, descriptive, and formatted with Conventional Commits (e.g., `feat(ui): add responsive modal component`).
- Write unit tests for new components or utilities alongside the code.

### Step 4: Local Quality Verification
Before submitting a PR, verify:
1. Linting and formatting pass without warnings.
2. Unit tests pass cleanly.
3. Component renders correctly across target viewports.
4. No console errors or memory leaks.

### Step 5: Pull Request Submission
Push the branch to `origin`:
```bash
git push origin frontend/fe-2/task-004-modal-component
```
Open a Pull Request targeting `main` using the provided template (`.github/PULL_REQUEST_TEMPLATE.md`). Then update task tracking:
```bash
python3 scripts/magi.py submit-pr TASK-004 --agent FE-2 --pr <PR_NUMBER>
```

### Step 6: QA Review & Resolution
- Notify **QA-2** (Frontend QA Specialist) for visual, component, and accessibility testing.
- If changes are requested by QA, commit fixes to the same branch and push updates.
- Once QA marks the PR as `APPROVED` and it is merged into `main`, mark the task as complete:
```bash
python3 scripts/magi.py complete TASK-004 --agent FE-2
```
