# Stage Status

Update this file when a stage starts or ends. Link to immutable artifacts in this project.

| Stage | Status | Input | Artifact | Decision / blocker | Owner / next action |
|---|---|---|---|---|
| Brief, constraints and data access | pending | `RESEARCH_BRIEF.md` | | |
| Candidate story and literature | pending | | `idea2paper_runs/<run-id>/`, `literature/` | |
| Human/expert decisions (if needed) | skipped | | `decisions/` | |
| Claims and experiment plan | pending | | `CLAIMS_AND_EVIDENCE.md`, `EXPERIMENT_PLAN.md` | |
| Code/data sanity check | pending | | `experiments/` | |
| Main experiment and sensitivities | pending | | `experiments/` | |
| Result, citation and integrity audit | pending | | `paper/audits/` | |
| Manuscript, figures and compiled outputs | pending | | `paper/` | |

Allowed status values: `pending`, `running`, `blocked`, `complete`, `skipped`. A stage is complete only when its artifact exists and its material limits are recorded.

Use `skipped` only when the stage is genuinely irrelevant; record why. Do not mark a stage complete because a model produced a recommendation.
