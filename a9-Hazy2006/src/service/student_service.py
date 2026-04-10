from src.domain.student import Student
from src.domain.exceptions import ValidationException, ServiceException


class StudentService:
    def __init__(self, student_repo, grade_repo):
        # we need the grade repo here to handle cascade deletes
        self._student_repo = student_repo
        self._grade_repo = grade_repo

    def add_student(self, student_id, name):
        # validate input before creating object
        if not student_id or not str(student_id).strip():
            raise ValidationException("Student ID cannot be empty")
        if not name or not name.strip():
            raise ValidationException("Student name cannot be empty")

        student = Student(student_id, name.strip())
        self._student_repo.add(student)
        return student

    def remove_student(self, student_id):
        # careful: when deleting a student, we must delete their grades first
        grades_to_remove = []
        for grade in self._grade_repo.get_all():
            if grade.student_id == student_id:
                grades_to_remove.append((grade.student_id, grade.discipline_id))

        # delete the found grades
        for grade_id in grades_to_remove:
            self._grade_repo.remove(grade_id)

        # finally remove the student
        self._student_repo.remove(student_id)

    def update_student(self, student_id, name):
        if not name or not name.strip():
            raise ValidationException("Student name cannot be empty")

        student = self._student_repo.find_by_id(student_id)
        if not student:
            raise ValidationException(f"ID {student_id} not found")

        student.name = name.strip()
        self._student_repo.update(student)
        return student

    def find_student(self, student_id):
        return self._student_repo.find_by_id(student_id)

    def get_all_students(self):
        return self._student_repo.get_all()

    def search_students(self, search_term):
        # simple partial search by ID or Name
        search_term = search_term.lower().strip()
        results = []

        for student in self._student_repo.get_all():
            if (search_term in str(student.student_id).lower() or
                    search_term in student.name.lower()):
                results.append(student)

        return results