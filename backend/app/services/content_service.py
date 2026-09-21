from typing import List, Dict, Set
from collections import defaultdict
from sqlalchemy.orm import Session

from app.models.content import Topic, Concept, Skill, Lesson
from app.repositories.content_repo import ContentRepository
from app.core.errors import NotFoundError, ValidationError


class ContentService:
    @staticmethod
    def create_topic(db: Session, title: str, slug: str, description: str = None, order_index: int = 0) -> Topic:
        existing = ContentRepository.get_topic_by_slug(db, slug)
        if existing:
            raise ValidationError(f"Chủ đề với slug '{slug}' đã tồn tại", details={"field": "slug"})

        topic = Topic(title=title, slug=slug, description=description, order_index=order_index)
        return ContentRepository.create_topic(db, topic)

    @staticmethod
    def create_skill(
        db: Session,
        name: str,
        slug: str,
        description: str = None,
        difficulty: str = "easy",
        concept_id: str = None,
        topic_id: str = None,
    ) -> Skill:
        existing = ContentRepository.get_skill_by_slug(db, slug)
        if existing:
            raise ValidationError(f"Kỹ năng với slug '{slug}' đã tồn tại", details={"field": "slug"})

        if concept_id and not ContentRepository.get_concept_by_id(db, concept_id):
            raise NotFoundError(f"Không tìm thấy Concept id '{concept_id}'", details={"field": "concept_id"})

        if topic_id and not ContentRepository.get_topic_by_id(db, topic_id):
            raise NotFoundError(f"Không tìm thấy Topic id '{topic_id}'", details={"field": "topic_id"})

        skill = Skill(
            name=name,
            slug=slug,
            description=description,
            difficulty=difficulty,
            concept_id=concept_id,
            topic_id=topic_id,
        )
        return ContentRepository.create_skill(db, skill)

    @staticmethod
    def add_skill_prerequisite(db: Session, skill_id: str, prereq_id: str):
        """
        Thêm kỹ năng tiên quyết với thuật toán ngăn chặn chu trình (Cycle Prevention).
        Quy tắc:
        1. skill_id không được trùng prereq_id.
        2. Nếu từ prereq_id đã có đường đi tới skill_id trong đồ thị phụ thuộc,
           việc thêm skill_id -> prereq_id sẽ tạo thành chu trình (Cycle).
        """
        if skill_id == prereq_id:
            raise ValidationError(
                "Một kỹ năng không thể tự làm điều kiện tiên quyết cho chính nó",
                details={"skill_id": skill_id, "prerequisite_skill_id": prereq_id},
            )

        skill = ContentRepository.get_skill_by_id(db, skill_id)
        if not skill:
            raise NotFoundError(f"Không tìm thấy kỹ năng '{skill_id}'")

        prereq_skill = ContentRepository.get_skill_by_id(db, prereq_id)
        if not prereq_skill:
            raise NotFoundError(f"Không tìm thấy kỹ năng tiên quyết '{prereq_id}'")

        # Lấy toàn bộ các cạnh phụ thuộc hiện tại để dựng đồ thị
        # Edge (A, B) có nghĩa là A yêu cầu B
        edges = ContentRepository.get_all_prerequisite_edges(db)
        graph: Dict[str, Set[str]] = defaultdict(set)
        for s_id, p_id in edges:
            graph[s_id].add(p_id)

        # Kiểm tra xem từ prereq_id có đường đi đến skill_id không (DFS)
        visited = set()
        def has_path(start: str, target: str) -> bool:
            if start == target:
                return True
            visited.add(start)
            for neighbor in graph[start]:
                if neighbor not in visited:
                    if has_path(neighbor, target):
                        return True
            return False

        if has_path(prereq_id, skill_id):
            raise ValidationError(
                f"Phát hiện chu trình phụ thuộc: Kỹ năng '{prereq_skill.name}' đã trực tiếp hoặc gián tiếp phụ thuộc vào '{skill.name}'",
                code="PREREQUISITE_CYCLE_DETECTED",
                details={"skill_id": skill_id, "prerequisite_skill_id": prereq_id},
            )

        # Thêm cạnh nếu chưa có
        if prereq_id in graph[skill_id]:
            return skill  # Đã tồn tại, idempotent

        ContentRepository.add_prerequisite(db, skill_id, prereq_id)
        return ContentRepository.get_skill_by_id(db, skill_id)

    @staticmethod
    def get_lesson(db: Session, lesson_id: str, user_role: str = "student") -> Lesson:
        lesson = ContentRepository.get_lesson_by_id(db, lesson_id)
        if not lesson:
            raise NotFoundError(f"Không tìm thấy bài học '{lesson_id}'")

        # Access rules: Students cannot view unpublished draft lessons
        if user_role == "student" and not lesson.is_published:
            raise NotFoundError("Bài học này chưa được xuất bản hoặc không khả dụng")

        return lesson
