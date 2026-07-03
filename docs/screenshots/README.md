# Sample Screenshots

Placeholders for evaluators running the prototype locally. To capture real
screenshots after following the Setup Instructions in `README.md`:

1. **Copilot Console — Requirement Input**
   `docs/screenshots/01-requirement-input.png`
   The top-of-page input panel with the mandatory use case pre-filled and
   the example-preset chips ("Mandatory use case", "Brownfield", "Ambiguous").

2. **Requirement Analysis tab**
   `docs/screenshots/02-requirement-analysis.png`
   Functional/non-functional requirements, ambiguities, and assumptions
   rendered in the four-panel grid.

3. **Task Decomposition tab**
   `docs/screenshots/03-task-decomposition.png`
   Ordered task list with dependency chips and the "AI assistance" callout
   box per task.

4. **Engineering Artifacts tab**
   `docs/screenshots/04-engineering-artifacts.png`
   Folder structure, database schema, API contracts, and key files.

5. **Validation tab**
   `docs/screenshots/05-validation.png`
   Code/security/performance review findings with severity badges, missing
   edge cases, and test coverage summary.

6. **Risk Analysis tab**
   `docs/screenshots/06-risk-analysis.png`
   Risk table with category badges and mitigations.

7. **Final Summary tab**
   `docs/screenshots/07-final-summary.png`
   The four closing summary panels.

8. **Live Demo tab**
   `docs/screenshots/08-live-demo.png`
   A shortened URL in the results table, showing click count and last-click
   timestamp after clicking the generated link.

To generate these yourself: run both `npm run dev` (frontend) and
`uvicorn app.main:app --reload` (backend) per the README, open
`http://localhost:5173`, and capture each tab after clicking **Generate**
with the pre-filled mandatory requirement.
