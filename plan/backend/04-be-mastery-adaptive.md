# BE-04 – Mastery & Adaptive Learning Service

## Mastery
- [ ] Define evidence types
- [ ] Define weights
- [ ] Calculate mastery
- [ ] Store confidence/evidence count
- [ ] Recompute when new evidence arrives
- [ ] Version mastery logic

## Adaptive Path
- [ ] Check prerequisite
- [ ] Select reinforcement
- [ ] Select next topic
- [ ] Adjust difficulty
- [ ] Persist path
- [ ] Persist reason for change

## API
- [ ] GET /mastery
- [ ] GET /learning-path
- [ ] Internal update hooks

## Tests
- [ ] Mastery increases after success
- [ ] Mastery decreases/adjusts after repeated failure
- [ ] Prerequisite block
- [ ] Difficulty up/down rule
- [ ] Empty evidence
