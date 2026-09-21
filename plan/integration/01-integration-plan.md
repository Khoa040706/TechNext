# Integration Plan – FE + BE + AI

## INT-01 Auth
- [ ] FE login → Supabase Auth
- [ ] session/token handling
- [ ] Bearer token → FastAPI
- [ ] FastAPI JWT verification
- [ ] protected route
- [ ] logout

## INT-02 Learning
- [ ] topic list
- [ ] lesson detail
- [ ] progress update

## INT-03 Quiz
- [ ] fetch quiz
- [ ] submit quiz
- [ ] display result
- [ ] mastery update visible

## INT-04 Coding
- [ ] fetch exercise
- [ ] Monaco editor
- [ ] Pyodide worker load
- [ ] run Python client-side
- [ ] timeout terminates worker
- [ ] submit source + telemetry to FastAPI
- [ ] backend marks client execution trust level
- [ ] display test result
- [ ] attempt history

## INT-05 Personalization
- [ ] mastery API → skill UI
- [ ] learning path API → path UI
- [ ] recommendation API → cards
- [ ] prediction API → summary
- [ ] explanation API → XAI UI

## INT-06 Admin
- [ ] CRUD contracts
- [ ] validation mapping
- [ ] role error handling

## Contract checklist
- [ ] same field names
- [ ] same enum values
- [ ] nullability agreed
- [ ] date format agreed
- [ ] pagination agreed
- [ ] errors agreed

## Integration exit
- [ ] no mocked API remains in production flow
- [ ] all critical flow works end-to-end
- [ ] FE handles BE error states
