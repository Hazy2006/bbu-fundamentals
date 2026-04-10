import random
from src.domain.validators import ValidationException, StoreException
from src.domain.student import Student
from src.services.undo_redo_service import FunctionCall, Operation, CascadedOperation


class StudentService:
    def __init__(self, student_repository, grade_repository, undo_service):
        self.__repo = student_repository
        self.__grade_repo = grade_repository
        self.__undo_service = undo_service

    def add_student(self, student_id, name):
        student_id = str(student_id).strip()
        name = name.strip()

        if not student_id:
            raise ValidationException("ID cannot be empty.")
        if not name or len(name) < 2:
            raise ValidationException("Name must be at least 2 characters.")
        if self.__repo.find_by_id(student_id):
            raise StoreException(f"ID {student_id} is already taken.")

        # Check for Duplicate Name
        for s in self.__repo.get_all():
            if s.name.lower() == name.lower():
                raise ValidationException(f"Student '{name}' already exists.")

        new_student = Student(student_id, name)
        self.__repo.add(new_student)

        if self.__undo_service:
            undo = FunctionCall(self.__repo.remove, student_id, param_repr=f"Remove {name}")
            redo = FunctionCall(self.__repo.add, new_student, param_repr=f"Add {name}")
            self.__undo_service.record(Operation(undo, redo))

    def remove_student(self, student_id):
        # 1. Find Student (Use __repo, not _repo)
        student_id = str(student_id)
        student = self.__repo.find_by_id(student_id)
        if not student:
            raise StoreException("Student not found.")

        # 2. Find Grades (Cascade)
        all_grades = self.__grade_repo.get_all()
        related_grades = [g for g in all_grades if str(g.student_id) == student_id]

        # 3. Prepare Cascade
        casc = CascadedOperation()

        # Op 1: Grades (Undo=Restore, Redo=Remove)
        casc.add(Operation(
            FunctionCall(self._restore_grades, related_grades, param_repr=f"Restore {len(related_grades)} grades"),
            FunctionCall(self._remove_grades_list, related_grades, param_repr=f"Remove {len(related_grades)} grades")
        ))

        # Op 2: Student (Undo=Restore, Redo=Remove)
        casc.add(Operation(
            FunctionCall(self.__repo.add, student, param_repr=f"Restore {student.name}"),
            FunctionCall(self.__repo.remove, student_id, param_repr=f"Remove {student.name}")
        ))

        # 4. Execute Removal
        self._remove_grades_list(related_grades)
        self.__repo.remove(student_id)

        # 5. Record
        if self.__undo_service:
            self.__undo_service.record(casc)

        return student

    def update_student(self, sid, new_name):
        s = self.__repo.find_by_id(str(sid))
        if not s: raise StoreException("Student not found.")

        old_name = s.name
        s.name = new_name
        self.__repo.update(s)

        if self.__undo_service:
            undo = FunctionCall(self._update_internal, sid, old_name)
            redo = FunctionCall(self._update_internal, sid, new_name)
            self.__undo_service.record(Operation(undo, redo))

    def _update_internal(self, sid, name):
        s = self.__repo.find_by_id(sid)
        if s:
            s.name = name
            self.__repo.update(s)

    def _restore_grades(self, grades):
        # Prevent duplicates when restoring grades
        all_current = self.__grade_repo.get_all()
        for g in grades:
            found = False
            for existing in all_current:
                if (str(existing.student_id) == str(g.student_id) and
                        str(existing.discipline_id) == str(g.discipline_id) and
                        abs(existing.grade_value - g.grade_value) < 0.001):
                    found = True
                    break
            if not found:
                self.__grade_repo.add(g)

    def _remove_grades_list(self, grades):
        # Safely remove a list of grades
        repo_grades = self.__grade_repo.get_all()
        for g in grades:
            # Find the exact object in the repo
            target = next((x for x in repo_grades if
                           str(x.student_id) == str(g.student_id) and
                           str(x.discipline_id) == str(g.discipline_id) and
                           x.grade_value == g.grade_value), None)
            if target:
                try:
                    self.__grade_repo.remove(target)
                except:
                    # Fallback if repo behaves like a list
                    if isinstance(repo_grades, list): repo_grades.remove(target)

    def get_all(self):
        return self.__repo.get_all()

    def search(self, text):
        text = text.lower().strip()
        return [s for s in self.__repo.get_all() if text in s.name.lower() or text == str(s.student_id)]

    def generate_random(self, n=10):
        names = ["Alice", "Bob", "Charlie", "Diana", "Evan", "Frank", "Grace", "Heidi", "Ivan", "Judy"]
        surnames = ["Smith", "Doe", "Brown", "Wilson", "Taylor", "Miller", "Davis"]
        count = 0
        attempts = 0
        while count < n and attempts < n * 5:
            attempts += 1
            rnd_id = str(random.randint(100, 9999))
            rnd_name = random.choice(names) + " " + random.choice(surnames)
            try:
                self.add_student(rnd_id, rnd_name)
                count += 1
            except:
                pass