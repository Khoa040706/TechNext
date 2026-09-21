# BE-07 – Database & Migration Plan

## Platform
- [ ] Supabase PostgreSQL connection
- [ ] SQLAlchemy 2.x configured
- [ ] Alembic configured

## Identity schema
- [ ] Supabase `auth.users` treated as provider-managed
- [ ] profiles table references auth user id
- [ ] students table references profile
- [ ] Không có password hash table trong app schema

## Schema
- [ ] profiles
- [ ] students
- [ ] topics
- [ ] concepts
- [ ] skills
- [ ] skill_prerequisites
- [ ] lessons
- [ ] quizzes
- [ ] questions
- [ ] quiz_attempts
- [ ] question_results
- [ ] coding_exercises
- [ ] test_cases
- [ ] submissions
- [ ] test_results
- [ ] execution_source/trust_level fields
- [ ] learning_resources
- [ ] resource_skill_map
- [ ] skill_mastery
- [ ] learning_paths
- [ ] recommendations
- [ ] predictions
- [ ] explanations

## Constraints
- [ ] FK
- [ ] unique rules
- [ ] cascade rules reviewed
- [ ] soft-delete/archive policy
- [ ] timestamp policy

## Indexes
- [ ] student + time
- [ ] student + skill
- [ ] student + exercise
- [ ] recommendation query path
- [ ] prediction query path

## Migration checklist
- [ ] migration reversible where practical
- [ ] seed/dev data separated
- [ ] no destructive migration without backup plan
- [ ] migration tested on clean DB
- [ ] migration tested on existing DB snapshot
