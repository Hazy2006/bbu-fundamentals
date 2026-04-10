from src.domain.grade import Grade
from src.domain.exceptions import ValidationException, NotFoundException


class GradeService:
    def __init__(self, student_repo, discipline_repo, grade_repo):
        self._student_repo = student_repo
        self._discipline_repo = discipline_repo
        self._grade_repo = grade_repo

    def add_grade(self, student_id, discipline_id, grade_value):
        # 1. Validate inputs
        if not self._student_repo.find_by_id(student_id):
            raise ValidationException(f"Student ID {student_id} does not exist")

        if not self._discipline_repo.find_by_id(discipline_id):
            raise ValidationException(f"Discipline ID {discipline_id} does not exist")

        try:
            val = float(grade_value)
            if val < 1 or val > 10:
                raise ValidationException("Grade must be between 1 and 10")
        except ValueError:
            raise ValidationException("Grade must be a number")

        # 2. Create Grade
        # NOTE: To allow multiple grades, we need a unique way to store them.
        # If your Grade entity doesn't have an ID, we might need to rely on the Repo
        # to handle it, OR we make the Grade object hashable.
        # For this assignment, assuming Grade(student_id, discipline_id, value):
        grade = Grade(student_id, discipline_id, val)

        # 3. Save
        self._grade_repo.add(grade)
        return grade

    def get_grades_for_student(self, student_id):
        # Helper to see all grades for one student
        return [g for g in self._grade_repo.get_all() if g.student_id == student_id]

    def get_all_grades(self):
        return self._grade_repo.get_all()