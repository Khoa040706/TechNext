from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.content import Topic, Skill, Lesson
from app.models.assessment import CodingExercise, Quiz
from app.models.mastery import SkillMastery, LearningPath
from app.repositories.mastery_repo import MasteryRepository
from app.repositories.content_repo import ContentRepository
from app.services.mastery_service import MasteryService, MASTERY_LOGIC_VERSION
from app.core.logging import logger

PREREQUISITE_MASTERY_THRESHOLD = 0.60


class AdaptiveService:
    @staticmethod
    def adjust_difficulty(mastery_score: float) -> str:
        """Quy tắc điều chỉnh độ khó:
        - mastery < 0.4 => easy (ôn tập / nền tảng)
        - 0.4 <= mastery < 0.7 => medium (rèn luyện)
        - mastery >= 0.7 => hard (thử thách nâng cao)"""
        if mastery_score < 0.4:
            return "easy"
        elif mastery_score < 0.7:
            return "medium"
        return "hard"

    @staticmethod
    def check_prerequisites(
        db: Session, student_id: str, skill: Skill
    ) -> Tuple[bool, Optional[Skill], float]:
        """Kiểm tra điều kiện tiên quyết của một skill.
        Trả về (is_satisfied, blocking_skill, blocking_skill_mastery)."""
        if not skill.prerequisites:
            return True, None, 1.0

        for prereq in skill.prerequisites:
            mastery = MasteryRepository.get_skill_mastery(db, student_id, prereq.id)
            score = mastery.mastery_score if mastery else 0.0
            if score < PREREQUISITE_MASTERY_THRESHOLD:
                return False, prereq, score

        return True, None, 1.0

    @staticmethod
    def generate_or_update_learning_path(
        db: Session, student_id: str, target_skill_id: Optional[str] = None
    ) -> LearningPath:
        """Sinh hoặc cập nhật lộ trình học thích ứng cho sinh viên."""
        # 1. Lấy toàn bộ mastery hiện tại của sinh viên
        masteries = MasteryRepository.get_student_masteries(db, student_id)
        mastery_map = {m.skill_id: m.mastery_score for m in masteries}
        total_evidences = sum(m.evidence_count for m in masteries)

        # 2. Lấy danh sách skills trong hệ thống
        all_skills, _ = ContentRepository.get_skills(db, skip=0, limit=100)

        target_skill: Optional[Skill] = None
        recommended_difficulty: str = "easy"
        reason_for_change: str = ""
        items_data: List[Dict[str, Any]] = []

        # TRƯỜNG HỢP A: Có yêu cầu cụ thể target_skill_id
        if target_skill_id:
            specified_skill = ContentRepository.get_skill_by_id(db, target_skill_id)
            if specified_skill:
                is_prereq_ok, blocking_skill, blocking_score = AdaptiveService.check_prerequisites(
                    db, student_id, specified_skill
                )
                if not is_prereq_ok and blocking_skill:
                    target_skill = blocking_skill
                    recommended_difficulty = AdaptiveService.adjust_difficulty(blocking_score)
                    reason_for_change = (
                        f"Kỹ năng mục tiêu '{specified_skill.name}' yêu cầu hoàn thành kiến thức tiên quyết "
                        f"'{blocking_skill.name}' (ngưỡng tối thiểu {PREREQUISITE_MASTERY_THRESHOLD:.2f}, "
                        f"hiện tại: {blocking_score:.2f}). Lộ trình đã điều hướng bạn hoàn thành kỹ năng tiên quyết này trước."
                    )
                else:
                    target_skill = specified_skill
                    curr_score = mastery_map.get(specified_skill.id, 0.0)
                    recommended_difficulty = AdaptiveService.adjust_difficulty(curr_score)
                    reason_for_change = (
                        f"Lộ trình học tập cho kỹ năng '{specified_skill.name}' "
                        f"với độ khó {recommended_difficulty.upper()} phù hợp năng lực hiện tại."
                    )

        # TRƯỜNG HỢP B: Kỹ năng yếu cần củng cố (Reinforcement)
        elif any((m.mastery_score < 0.4 and m.evidence_count > 0) for m in masteries):
            weak_masteries = [m for m in masteries if m.mastery_score < 0.4 and m.evidence_count > 0]
            weak_masteries.sort(key=lambda m: m.mastery_score)
            weak_mastery = weak_masteries[0]
            target_skill = weak_mastery.skill
            recommended_difficulty = "easy"
            reason_for_change = (
                f"Kỹ năng '{target_skill.name if target_skill else 'hiện tại'}' đang ở mức cần củng cố "
                f"(Mastery: {weak_mastery.mastery_score:.2f} < 0.40). Lộ trình ưu tiên bài học ôn tập "
                f"và bài tập mức độ Dễ để lấy lại nền tảng vững chắc."
            )

        # TRƯỜNG HỢP C: Cold Start (Học viên mới chưa có bất kỳ evidence nào)
        elif total_evidences == 0 or not all_skills:
            if all_skills:
                target_skill = all_skills[0]
            recommended_difficulty = "easy"
            reason_for_change = (
                "Chào mừng bạn đến với NextTech! Lộ trình khởi đầu với các bài học "
                "và bài tập nền tảng mức độ Dễ."
            )

        # TRƯỜNG HỢP D: Tự động đề xuất kỹ năng tiếp theo kèm Prerequisite Check
        else:
            candidate_skill: Optional[Skill] = None
            for s in all_skills:
                score = mastery_map.get(s.id, 0.0)
                if score < 0.70:
                    candidate_skill = s
                    break

            if not candidate_skill and all_skills:
                candidate_skill = all_skills[-1]

            if candidate_skill:
                is_prereq_ok, blocking_skill, blocking_score = AdaptiveService.check_prerequisites(
                    db, student_id, candidate_skill
                )
                if not is_prereq_ok and blocking_skill:
                    target_skill = blocking_skill
                    recommended_difficulty = AdaptiveService.adjust_difficulty(blocking_score)
                    reason_for_change = (
                        f"Kỹ năng tiếp theo '{candidate_skill.name}' yêu cầu hoàn thành kiến thức tiên quyết "
                        f"'{blocking_skill.name}' (ngưỡng tối thiểu {PREREQUISITE_MASTERY_THRESHOLD:.2f}, "
                        f"hiện tại: {blocking_score:.2f}). Lộ trình đã điều hướng bạn hoàn thành kỹ năng tiên quyết này trước."
                    )
                else:
                    target_skill = candidate_skill
                    curr_score = mastery_map.get(candidate_skill.id, 0.0)
                    recommended_difficulty = AdaptiveService.adjust_difficulty(curr_score)
                    reason_for_change = (
                        f"Bạn đã hoàn thành tốt các yêu cầu tiên quyết. Lộ trình mở khóa kỹ năng "
                        f"'{candidate_skill.name}' với độ khó {recommended_difficulty.upper()} phù hợp năng lực hiện tại."
                    )

        # 3. Thu thập các items học tập tương ứng cho target_skill
        if target_skill:
            # Bài học liên quan
            stmt_lesson = select(Lesson).where(
                (Lesson.topic_id == target_skill.topic_id) & (Lesson.is_published == True)
            ).limit(1)
            lesson = db.scalars(stmt_lesson).first()
            if lesson:
                items_data.append({
                    "item_type": "lesson",
                    "item_id": lesson.id,
                    "title": f"Lý thuyết: {lesson.title}",
                    "difficulty": "easy",
                    "order_index": 1,
                    "reason": "Ôn tập hoặc nắm vững lý thuyết cốt lõi",
                })

            # Bài tập coding liên quan
            stmt_exercise = select(CodingExercise).where(
                (CodingExercise.skill_id == target_skill.id) & (CodingExercise.is_published == True)
            ).order_by(CodingExercise.order_index).limit(1)
            exercise = db.scalars(stmt_exercise).first()
            if exercise:
                items_data.append({
                    "item_type": "coding_exercise",
                    "item_id": exercise.id,
                    "title": f"Thực hành: {exercise.title}",
                    "difficulty": recommended_difficulty,
                    "order_index": 2,
                    "reason": f"Thực hành kỹ năng {target_skill.name} ở cấp độ {recommended_difficulty.upper()}",
                })

            # Quiz liên quan
            stmt_quiz = select(Quiz).where(
                (Quiz.topic_id == target_skill.topic_id) & (Quiz.is_published == True)
            ).order_by(Quiz.order_index).limit(1)
            quiz = db.scalars(stmt_quiz).first()
            if quiz:
                items_data.append({
                    "item_type": "quiz",
                    "item_id": quiz.id,
                    "title": f"Trắc nghiệm: {quiz.title}",
                    "difficulty": recommended_difficulty,
                    "order_index": 3,
                    "reason": "Kiểm tra nhanh mức độ hiểu khái niệm",
                })

        # Tạo và lưu trữ lộ trình mới
        learning_path = MasteryRepository.create_learning_path(
            db,
            student_id=student_id,
            target_skill_id=target_skill.id if target_skill else None,
            recommended_difficulty=recommended_difficulty,
            reason_for_change=reason_for_change,
            items_data=items_data,
            version=MASTERY_LOGIC_VERSION,
        )

        logger.info(
            f"Cập nhật Learning Path cho student='{student_id}': target_skill='{target_skill.name if target_skill else None}', "
            f"diff='{recommended_difficulty}', items={len(items_data)}"
        )
        return learning_path

    @staticmethod
    def get_or_create_active_path(
        db: Session, student_id: str, target_skill_id: Optional[str] = None
    ) -> LearningPath:
        path = MasteryRepository.get_active_learning_path(db, student_id)
        if not path or (target_skill_id and path.target_skill_id != target_skill_id):
            path = AdaptiveService.generate_or_update_learning_path(
                db, student_id=student_id, target_skill_id=target_skill_id
            )
        return path
