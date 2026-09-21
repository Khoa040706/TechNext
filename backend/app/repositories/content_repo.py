from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.models.content import Topic, Concept, Skill, SkillPrerequisite, Lesson


class ContentRepository:
    # ---------------- TOPICS ----------------
    @staticmethod
    def get_topics(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        include_archived: bool = False,
    ) -> Tuple[List[Topic], int]:
        stmt = select(Topic)
        if not include_archived:
            stmt = stmt.where(Topic.is_archived == False)
        
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = db.scalar(count_stmt) or 0

        stmt = stmt.order_by(Topic.order_index, Topic.created_at).offset(skip).limit(limit)
        topics = list(db.scalars(stmt).all())
        return topics, total

    @staticmethod
    def get_topic_by_id(db: Session, topic_id: str) -> Optional[Topic]:
        stmt = select(Topic).where(Topic.id == topic_id)
        return db.scalars(stmt).first()

    @staticmethod
    def get_topic_by_slug(db: Session, slug: str) -> Optional[Topic]:
        stmt = select(Topic).where(Topic.slug == slug)
        return db.scalars(stmt).first()

    @staticmethod
    def create_topic(db: Session, topic: Topic) -> Topic:
        db.add(topic)
        db.commit()
        db.refresh(topic)
        return topic

    @staticmethod
    def update_topic(db: Session, topic: Topic) -> Topic:
        db.commit()
        db.refresh(topic)
        return topic

    @staticmethod
    def delete_topic(db: Session, topic: Topic) -> None:
        db.delete(topic)
        db.commit()

    # ---------------- CONCEPTS ----------------
    @staticmethod
    def get_concepts_by_topic(db: Session, topic_id: str) -> List[Concept]:
        stmt = select(Concept).where(Concept.topic_id == topic_id).order_by(Concept.order_index)
        return list(db.scalars(stmt).all())

    @staticmethod
    def get_concept_by_id(db: Session, concept_id: str) -> Optional[Concept]:
        stmt = select(Concept).where(Concept.id == concept_id)
        return db.scalars(stmt).first()

    @staticmethod
    def create_concept(db: Session, concept: Concept) -> Concept:
        db.add(concept)
        db.commit()
        db.refresh(concept)
        return concept

    # ---------------- SKILLS ----------------
    @staticmethod
    def get_skills(db: Session, skip: int = 0, limit: int = 50) -> Tuple[List[Skill], int]:
        stmt = select(Skill)
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = db.scalar(count_stmt) or 0
        
        stmt = stmt.offset(skip).limit(limit)
        skills = list(db.scalars(stmt).all())
        return skills, total

    @staticmethod
    def get_skill_by_id(db: Session, skill_id: str) -> Optional[Skill]:
        stmt = select(Skill).where(Skill.id == skill_id)
        return db.scalars(stmt).first()

    @staticmethod
    def get_skill_by_slug(db: Session, slug: str) -> Optional[Skill]:
        stmt = select(Skill).where(Skill.slug == slug)
        return db.scalars(stmt).first()

    @staticmethod
    def create_skill(db: Session, skill: Skill) -> Skill:
        db.add(skill)
        db.commit()
        db.refresh(skill)
        return skill

    @staticmethod
    def update_skill(db: Session, skill: Skill) -> Skill:
        db.commit()
        db.refresh(skill)
        return skill

    @staticmethod
    def delete_skill(db: Session, skill: Skill) -> None:
        db.delete(skill)
        db.commit()

    # ---------------- PREREQUISITES ----------------
    @staticmethod
    def get_prerequisites_for_skill(db: Session, skill_id: str) -> List[Skill]:
        stmt = (
            select(Skill)
            .join(SkillPrerequisite, SkillPrerequisite.prerequisite_skill_id == Skill.id)
            .where(SkillPrerequisite.skill_id == skill_id)
        )
        return list(db.scalars(stmt).all())

    @staticmethod
    def get_all_prerequisite_edges(db: Session) -> List[Tuple[str, str]]:
        stmt = select(SkillPrerequisite.skill_id, SkillPrerequisite.prerequisite_skill_id)
        return list(db.execute(stmt).all())

    @staticmethod
    def add_prerequisite(db: Session, skill_id: str, prereq_id: str) -> SkillPrerequisite:
        prereq = SkillPrerequisite(skill_id=skill_id, prerequisite_skill_id=prereq_id)
        db.add(prereq)
        db.commit()
        return prereq

    @staticmethod
    def remove_prerequisite(db: Session, skill_id: str, prereq_id: str) -> bool:
        stmt = select(SkillPrerequisite).where(
            SkillPrerequisite.skill_id == skill_id,
            SkillPrerequisite.prerequisite_skill_id == prereq_id,
        )
        row = db.scalars(stmt).first()
        if row:
            db.delete(row)
            db.commit()
            return True
        return False

    # ---------------- LESSONS ----------------
    @staticmethod
    def get_lessons_by_topic(
        db: Session,
        topic_id: str,
        only_published: bool = True,
    ) -> List[Lesson]:
        stmt = select(Lesson).where(Lesson.topic_id == topic_id)
        if only_published:
            stmt = stmt.where(Lesson.is_published == True)
        stmt = stmt.order_by(Lesson.order_index, Lesson.created_at)
        return list(db.scalars(stmt).all())

    @staticmethod
    def get_lesson_by_id(db: Session, lesson_id: str) -> Optional[Lesson]:
        stmt = select(Lesson).where(Lesson.id == lesson_id)
        return db.scalars(stmt).first()

    @staticmethod
    def create_lesson(db: Session, lesson: Lesson) -> Lesson:
        db.add(lesson)
        db.commit()
        db.refresh(lesson)
        return lesson

    @staticmethod
    def update_lesson(db: Session, lesson: Lesson) -> Lesson:
        db.commit()
        db.refresh(lesson)
        return lesson

    @staticmethod
    def delete_lesson(db: Session, lesson: Lesson) -> None:
        db.delete(lesson)
        db.commit()
