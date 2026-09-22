import uuid
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import Profile, Student


class UserRepository:
    @staticmethod
    def get_profile(db: Session, profile_id: str) -> Optional[Profile]:
        stmt = select(Profile).where(Profile.id == profile_id)
        return db.scalars(stmt).first()

    @staticmethod
    def get_profile_by_email(db: Session, email: str) -> Optional[Profile]:
        stmt = select(Profile).where(Profile.email == email)
        return db.scalars(stmt).first()

    @staticmethod
    def create_profile(
        db: Session,
        profile_id: str,
        email: Optional[str] = None,
        role: str = "student",
        display_name: Optional[str] = None,
    ) -> Profile:
        profile = Profile(
            id=profile_id,
            email=email,
            role=role,
            display_name=display_name or (email.split("@")[0] if email else "Người học"),
            is_active=True,
        )
        db.add(profile)
        db.flush()

        # Provision student record if role is student
        if role == "student":
            research_id = f"stu_{uuid.uuid4().hex[:10]}"
            student = Student(
                profile_id=profile.id,
                research_id=research_id,
            )
            db.add(student)
            db.flush()

        db.commit()
        db.refresh(profile)
        return profile

    @staticmethod
    def get_or_create_profile(
        db: Session,
        profile_id: str,
        email: Optional[str] = None,
        role: str = "student",
    ) -> Profile:
        profile = UserRepository.get_profile(db, profile_id)
        if not profile:
            profile = UserRepository.create_profile(
                db,
                profile_id=profile_id,
                email=email,
                role=role,
            )
        return profile

    @staticmethod
    def update_profile(
        db: Session,
        profile: Profile,
        display_name: Optional[str] = None,
    ) -> Profile:
        if display_name is not None:
            profile.display_name = display_name
        db.commit()
        db.refresh(profile)
        return profile

    @staticmethod
    def get_student_by_profile_id(db: Session, profile_id: str) -> Optional[Student]:
        stmt = select(Student).where(Student.profile_id == profile_id)
        return db.scalars(stmt).first()

    @staticmethod
    def ensure_student_for_profile(db: Session, profile_id: str) -> Student:
        student = UserRepository.get_student_by_profile_id(db, profile_id)
        if not student:
            research_id = f"stu_{uuid.uuid4().hex[:10]}"
            student = Student(
                profile_id=profile_id,
                research_id=research_id,
            )
            db.add(student)
            db.commit()
            db.refresh(student)
        return student
