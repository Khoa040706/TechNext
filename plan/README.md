# NextTech Plan Directory

## Structure

```text
plan/
├── 00-overview.md
├── 01-foundation.md
├── frontend/
│   ├── 01-fe-foundation.md
│   ├── 02-fe-auth-dashboard.md
│   ├── 03-fe-learning-quiz-coding.md
│   ├── 04-fe-personalization.md
│   └── 05-fe-admin.md
├── backend/
│   ├── 01-be-foundation.md
│   ├── 02-be-auth-content.md
│   ├── 03-be-quiz-coding.md
│   ├── 04-be-mastery-adaptive.md
│   ├── 05-be-recommendation.md
│   ├── 06-be-prediction-xai.md
│   └── 07-be-database.md
├── ai-data/
│   ├── 01-data-feature-pipeline.md
│   ├── 02-prediction-model.md
│   └── 03-xai.md
├── integration/
│   └── 01-integration-plan.md
├── testing/
│   ├── 00-testing-strategy.md
│   ├── 01-master-test-checklist.md
│   └── bug-report-template.md
└── release/
    └── 01-release-deployment.md
```

## Cách dùng

Agent đọc:
1. `context.md`
2. `AGENTS.md`
3. `docs/technical/tech-stack.md`
4. `plan/00-overview.md`
5. file task đúng phần mình làm
6. tài liệu chuyên môn liên quan

Không cần nhồi toàn bộ repository vào prompt nếu task hẹp.


## Tech Stack Rule

`docs/technical/tech-stack.md` là stack chính thức.

Không tạo implementation plan mới và không thay stack trong lúc làm task.
