# BE-04 – Mastery & Adaptive Learning Service

## Mastery
- [x] Define evidence types
- [x] Define weights
- [x] Calculate mastery
- [x] Store confidence/evidence count
- [x] Recompute when new evidence arrives
- [x] Version mastery logic

## Adaptive Path
- [x] Check prerequisite
- [x] Select reinforcement
- [x] Select next topic
- [x] Adjust difficulty
- [x] Persist path
- [x] Persist reason for change

## API
- [x] GET /mastery
- [x] GET /learning-path
- [x] Internal update hooks

## Tests
- [x] Mastery increases after success
- [x] Mastery decreases/adjusts after repeated failure
- [x] Prerequisite block
- [x] Difficulty up/down rule
- [x] Empty evidence
