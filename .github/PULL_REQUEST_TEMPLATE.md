## Pull Request Description

### Task ID
- Task: <!-- e.g. TASK-001 -->

### Agent ID
- Agent: <!-- e.g. FE-1, BE-2, QA-3 -->

### Team
- Team: <!-- frontend / backend / qa / management -->

### Summary of Changes
<!-- Provide a concise explanation of what changes were made and why. -->

### Architecture & Boundary Compliance
- [ ] No direct commits to `main` branch.
- [ ] Changes are isolated to team-designated domain directories.
- [ ] Branch follows convention: `<team>/<agent-id>/<task-id>-<slug>`.
- [ ] All task dependencies were verified as DONE prior to work.

### Verification Checklist
- [ ] Code passes local syntax, lint, and formatting checks.
- [ ] Unit / Integration tests have been added or updated.
- [ ] All tests pass locally (`pytest`, `npm test`, etc.).
- [ ] Acceptance criteria from `.magi/tasks/<TASK-ID>.json` are 100% satisfied.

---

### QA Team Sign-Off (MANDATORY BEFORE MERGE)
> This section is strictly reserved for QA Team agents (`QA-1`, `QA-2`, `QA-3`). Developers may not check these boxes.

- [ ] **QA Reviewer Assigned**: <!-- e.g. QA-1, QA-2, or QA-3 -->
- [ ] **Test Coverage Verified**: Test suite executed and coverage meets threshold.
- [ ] **Requirements & Edge Cases Audited**: Verified against task acceptance criteria.
- [ ] **Regression Risk Evaluated**: No regressions detected across integrated components.
- [ ] **VERDICT**: `APPROVED` / `CHANGES_REQUESTED`

*QA Review Notes:*
<!-- QA Agent logs verification evidence, test output, or defect findings here. -->
