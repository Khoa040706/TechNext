import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import String, Text, Integer, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class SkillMastery(Base):
    __tablename__ = "skill_mastery"
    __table_args__ = (
        UniqueConstraint("student_id", "skill_id", name="uq_student_skill_mastery"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id: Mapped[str] = mapped_column(String(36), ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id: Mapped[str] = mapped_column(String(36), ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)
    mastery_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False) # 0.0 - 1.0
    confidence: Mapped[float] = mapped_column(Float, default=0.0, nullable=False) # 0.0 - 1.0
    evidence_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    version: Mapped[str] = mapped_column(String(30), default="v1.0-rule-baseline", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    student = relationship("Student")
    skill = relationship("Skill")


class LearningPath(Base):
    __tablename__ = "learning_paths"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id: Mapped[str] = mapped_column(String(36), ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(20), default="active", index=True) # active, superseded, completed
    target_skill_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("skills.id", ondelete="SET NULL"), nullable=True, index=True)
    recommended_difficulty: Mapped[str] = mapped_column(String(20), default="easy", nullable=False) # easy, medium, hard
    reason_for_change: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    version: Mapped[str] = mapped_column(String(30), default="v1.0-rule-baseline", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    student = relationship("Student")
    target_skill = relationship("Skill")
    items: Mapped[List["LearningPathItem"]] = relationship(
        "LearningPathItem",
        back_populates="path",
        cascade="all, delete-orphan",
        order_by="LearningPathItem.order_index",
    )


class LearningPathItem(Base):
    __tablename__ = "learning_path_items"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    path_id: Mapped[str] = mapped_column(String(36), ForeignKey("learning_paths.id", ondelete="CASCADE"), nullable=False, index=True)
    item_type: Mapped[str] = mapped_column(String(30), nullable=False) # lesson, coding_exercise, quiz, reinforcement
    item_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    difficulty: Mapped[str] = mapped_column(String(20), default="easy") # easy, medium, hard
    status: Mapped[str] = mapped_column(String(20), default="pending") # pending, in_progress, completed
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    path: Mapped["LearningPath"] = relationship("LearningPath", back_populates="items")
