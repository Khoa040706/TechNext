# Release & Deployment Plan

## Pre-release
- [ ] All Critical closed
- [ ] All High closed
- [ ] Automated tests pass
- [ ] E2E critical flow pass
- [ ] Migration tested
- [ ] Environment variables documented
- [ ] Secrets configured
- [ ] Build succeeds
- [ ] No dev/mock endpoint enabled

## Backend – Render
- [ ] Python 3.12 runtime/config
- [ ] DB migration
- [ ] FastAPI deploy
- [ ] Health check
- [ ] Log check
- [ ] model.joblib/model artifact loads
- [ ] model/feature version verified

## Frontend – Vercel
- [ ] `npm` production build
- [ ] API base URL
- [ ] Supabase public config
- [ ] Auth callback/config
- [ ] Pyodide version/source pinned
- [ ] Pyodide worker smoke test
- [ ] Static asset check
- [ ] Logo/favicon

## AI – loaded in FastAPI
- [ ] Model artifact deployed with backend
- [ ] Model version verified
- [ ] Feature version verified
- [ ] Fallback behavior verified
- [ ] No separate AI service required V1

## Smoke test
- [ ] Login
- [ ] Dashboard
- [ ] Quiz
- [ ] Coding submission
- [ ] Recommendation
- [ ] Prediction
- [ ] Admin login

## Rollback
- [ ] Previous app version known
- [ ] DB rollback/forward-fix plan
- [ ] Previous model artifact available


## Supabase
- [ ] Database connection
- [ ] Auth configured
- [ ] Storage policy nếu dùng
- [ ] Service role secret only on backend
