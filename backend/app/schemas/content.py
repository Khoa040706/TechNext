from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


# ---------------- TOPIC SCHEMAS ----------------
class TopicBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=150)
    slug: str = Field(..., min_length=2, max_length=150, pattern=r"^[a-z0-9-]+$")
    description: Optional[str] = None
    order_index: int = Field(default=0, ge=0)


class TopicCreate(TopicBase):
    pass


class TopicUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=2, max_length=150)
    description: Optional[str] = None
    order_index: Optional[int] = Field(default=None, ge=0)
    is_archived: Optional[bool] = None


class TopicRead(TopicBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    is_archived: bool
    created_at: datetime
    updated_at: datetime


# ---------------- CONCEPT SCHEMAS ----------------
class ConceptBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=150)
    description: Optional[str] = None
    order_index: int = Field(default=0, ge=0)


class ConceptCreate(ConceptBase):
    topic_id: str


class ConceptUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=2, max_length=150)
    description: Optional[str] = None
    order_index: Optional[int] = Field(default=None, ge=0)


class ConceptRead(ConceptBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    topic_id: str
    created_at: datetime


# ---------------- SKILL SCHEMAS ----------------
class SkillBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    slug: str = Field(..., min_length=2, max_length=150, pattern=r"^[a-z0-9_-]+$")
    description: Optional[str] = None
    difficulty: str = Field(default="easy", pattern=r"^(easy|medium|hard)$")


class SkillCreate(SkillBase):
    concept_id: Optional[str] = None
    topic_id: Optional[str] = None


class SkillUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=150)
    description: Optional[str] = None
    difficulty: Optional[str] = Field(default=None, pattern=r"^(easy|medium|hard)$")


class PrerequisiteItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    slug: Optional[str] = None
    difficulty: str


class SkillRead(SkillBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    concept_id: Optional[str] = None
    topic_id: Optional[str] = None
    created_at: datetime
    prerequisites: List[PrerequisiteItem] = Field(default_factory=list)


class SkillPrerequisiteAdd(BaseModel):
    prerequisite_skill_id: str = Field(..., description="ID của kỹ năng làm điều kiện tiên quyết")


# ---------------- LESSON SCHEMAS ----------------
class LessonBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=150)
    slug: str = Field(..., min_length=2, max_length=150, pattern=r"^[a-z0-9_-]+$")
    content_markdown: str = Field(..., min_length=5)
    order_index: int = Field(default=0, ge=0)
    is_published: bool = Field(default=False)


class LessonCreate(LessonBase):
    topic_id: str


class LessonUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=2, max_length=150)
    slug: Optional[str] = Field(default=None, min_length=2, max_length=150, pattern=r"^[a-z0-9_-]+$")
    content_markdown: Optional[str] = Field(default=None, min_length=5)
    order_index: Optional[int] = Field(default=None, ge=0)
    is_published: Optional[bool] = None


class LessonRead(LessonBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    topic_id: str
    created_at: datetime
    updated_at: datetime


# Detail topic response including its concepts and lessons
class TopicDetailRead(TopicRead):
    concepts: List[ConceptRead] = Field(default_factory=list)
    lessons: List[LessonRead] = Field(default_factory=list)
