from src.domain.discipline import Discipline
from src.domain.exceptions import ValidationException


class DisciplineService:
    def __init__(self, discipline_repo, grade_repo):
        self._discipline_repo = discipline_repo
        self._grade_repo = grade_repo

    def add_discipline(self, discipline_id, name):
        if not discipline_id or not str(discipline_id).strip():
            raise ValidationException("Discipline ID cannot be empty")
        if not name or not name.strip():
            raise ValidationException("Discipline name cannot be empty")

        discipline = Discipline(discipline_id, name.strip())
        self._discipline_repo.add(discipline)
        return discipline

    def remove_discipline(self, discipline_id):
        # cascade delete: remove grades for this discipline
        grades_to_remove = []
        for grade in self._grade_repo.get_all():
            if grade.discipline_id == discipline_id:
                grades_to_remove.append((grade.student_id, grade.discipline_id))

        for grade_id in grades_to_remove:
            self._grade_repo.remove(grade_id)

        self._discipline_repo.remove(discipline_id)

    def update_discipline(self, discipline_id, name):
        if not name or not name.strip():
            raise ValidationException("Discipline name cannot be empty")

        discipline = self._discipline_repo.find_by_id(discipline_id)
        if not discipline:
            raise ValidationException(f"ID {discipline_id} not found")

        discipline.name = name.strip()
        self._discipline_repo.update(discipline)
        return discipline

    def find_discipline(self, discipline_id):
        return self._discipline_repo.find_by_id(discipline_id)

    def get_all_disciplines(self):
        return self._discipline_repo.get_all()

    def search_disciplines(self, search_term):
        search_term = search_term.lower().strip()
        results = []

        for discipline in self._discipline_repo.get_all():
            if (search_term in str(discipline.discipline_id).lower() or
                    search_term in discipline.name.lower()):
                results.append(discipline)

        return results