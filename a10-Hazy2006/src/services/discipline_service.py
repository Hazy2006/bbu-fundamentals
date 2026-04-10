import random
from src.domain.discipline import Discipline
from src.domain.validators import ValidationException, StoreException
from src.services.undo_redo_service import FunctionCall, Operation, CascadedOperation


class DisciplineService:
    def __init__(self, disc_repo, grade_repo, undo_service=None):
        self._repo = disc_repo
        self._grade_repo = grade_repo
        self._undo_service = undo_service

    def add_discipline(self, d_id, name):
        # 1. Force ID to string and validate
        d_id = str(d_id).strip()
        if not d_id:
            raise ValidationException("Discipline ID cannot be empty.")

        # 2. Check for DUPLICATE ID
        if self._repo.find_by_id(d_id):
            raise StoreException(f"Discipline ID {d_id} already exists.")

        # 3. Validate Name
        if not name or not name.strip():
            raise ValidationException("Discipline name cannot be empty.")
        if any(char.isdigit() for char in name):
            raise ValidationException("Discipline name cannot contain digits.")

        # 4. Check for DUPLICATE NAME
        clean_name = name.strip().title()
        for d in self._repo.get_all():
            if d.name.lower() == clean_name.lower():
                raise ValidationException(f"Discipline '{clean_name}' already exists.")

        # 5. Create and Add
        disc_obj = Discipline(d_id, clean_name)
        self._repo.add(disc_obj)

        # 6. Record Undo
        if self._undo_service:
            undo_fc = FunctionCall(self._repo.remove, d_id,
                                   param_repr=f"Remove {clean_name}")
            redo_fc = FunctionCall(self._repo.add, disc_obj,
                                   param_repr=f"Add {clean_name}")
            self._undo_service.record(Operation(undo_fc, redo_fc))

    def remove_discipline(self, d_id):
        d_id = str(d_id)
        disc_entity = self._repo.find_by_id(d_id)
        if not disc_entity:
            raise StoreException("Discipline does not exist")

        # Find related grades
        all_grades = self._grade_repo.get_all()
        related_grades = [g for g in all_grades if str(g.discipline_id) == d_id]

        casc = CascadedOperation()

        # Operation 1: Grades (Undo = Restore, Redo = Remove)
        casc.add(Operation(
            FunctionCall(self._restore_grades_list, related_grades, param_repr=f"Restore {len(related_grades)} grades"),
            FunctionCall(self._remove_grades_list, related_grades, param_repr=f"Remove {len(related_grades)} grades")
        ))

        # Operation 2: Discipline (Undo = Restore, Redo = Remove)
        casc.add(Operation(
            FunctionCall(self._repo.add, disc_entity, param_repr=f"Restore {disc_entity.name}"),
            FunctionCall(self._repo.remove, d_id, param_repr=f"Remove {disc_entity.name}")
        ))

        # Execute Removal
        self._remove_grades_list(related_grades)
        self._repo.remove(d_id)

        if self._undo_service:
            self._undo_service.record(casc)

    def remove_grades_by_name(self, disc_name):
        """
        Removes all grades associated with a discipline name.
        Required by tests.
        """
        clean = disc_name.strip().lower()
        all_discs = self._repo.get_all()
        matches = [d for d in all_discs if d.name.lower() == clean]

        if not matches:
            raise StoreException(f"Discipline '{disc_name}' not found.")

        for disc in matches:
            # We treat this as a bulk removal of grades for that ID
            d_id = str(disc.discipline_id)
            all_grades = self._grade_repo.get_all()
            related = [g for g in all_grades if str(g.discipline_id) == d_id]
            self._remove_grades_list(related)

    def _restore_grades_list(self, grades):
        # Prevent duplicates when restoring grades
        all_current = self._grade_repo.get_all()
        for g in grades:
            found = False
            for existing in all_current:
                if (str(existing.student_id) == str(g.student_id) and
                        str(existing.discipline_id) == str(g.discipline_id) and
                        abs(existing.grade_value - g.grade_value) < 0.001):
                    found = True
                    break
            if not found:
                self._grade_repo.add(g)

    def _remove_grades_list(self, grades):
        # Safe helper to remove a list of grades
        repo_grades = self._grade_repo.get_all()
        for g_to_remove in grades:
            # Try to match by value if reference fails
            target = None
            for existing in repo_grades:
                if (existing.student_id == g_to_remove.student_id and
                        existing.discipline_id == g_to_remove.discipline_id and
                        existing.grade_value == g_to_remove.grade_value):
                    target = existing
                    break

            if target:
                try:
                    self._grade_repo.remove(target)
                except:
                    # Fallback for list-based repos
                    if isinstance(repo_grades, list) and target in repo_grades:
                        repo_grades.remove(target)

    def update_discipline(self, d_id, new_name):
        d_id = str(d_id)
        disc = self._repo.find_by_id(d_id)
        if not disc:
            raise StoreException("Discipline not found")

        old_name = disc.name
        new_name = new_name.strip().title()

        # Validate Unique Name
        for other in self._repo.get_all():
            if other.name.lower() == new_name.lower() and str(other.discipline_id) != d_id:
                raise ValidationException(f"Name '{new_name}' is already used.")

        disc.name = new_name
        self._repo.update(disc)

        if self._undo_service:
            undo_fc = FunctionCall(self._update_internal, d_id, old_name)
            redo_fc = FunctionCall(self._update_internal, d_id, new_name)
            self._undo_service.record(Operation(undo_fc, redo_fc))

    def _update_internal(self, d_id, name):
        d = self._repo.find_by_id(d_id)
        if d:
            d.name = name
            self._repo.update(d)

    def get_all(self):
        return sorted(self._repo.get_all(), key=lambda d: d.name)

    def search(self, query):
        query = query.lower().strip()
        all_d = self.get_all()
        return [d for d in all_d if query in d.name.lower() or query == str(d.discipline_id)]

    def generate_random(self, n=10):
        subjects = ["Math", "Physics", "Chemistry", "Biology", "History", "Geography", "CS", "Art", "Music"]
        count = 0
        attempts = 0
        while count < n and attempts < n * 5:
            attempts += 1
            new_id = str(random.randint(100, 999))
            if not self._repo.find_by_id(new_id):
                name = random.choice(subjects)
                try:
                    self.add_discipline(new_id, name)
                    count += 1
                except:
                    pass

    def get_disciplines_with_average(self):
        """
        Returns list of tuples: (Discipline Name, Average Grade)
        Sorted by average grade descending.
        Only includes disciplines with at least one grade.
        """
        grades = self._grade_repo.get_all()

        # 1. Group grades by Discipline ID
        # Map: { discipline_id: [list_of_grades] }
        disc_grades = {}
        for g in grades:
            did = str(g.discipline_id)
            disc_grades.setdefault(did, []).append(g.grade_value)

        results = []
        all_discs = self._repo.get_all()

        # 2. Calculate Averages
        for d in all_discs:
            did = str(d.discipline_id)
            if did in disc_grades:
                grades_list = disc_grades[did]
                avg = sum(grades_list) / len(grades_list)
                results.append((d.name, avg))

        # 3. Sort Descending by Average
        results.sort(key=lambda x: x[1], reverse=True)

        return results

    def students_failing_discipline(self, d_id):
        d_id = str(d_id)
        grades = self._grade_repo.get_all()
        per_student = {}
        for g in grades:
            if str(g.discipline_id) == d_id:
                per_student.setdefault(str(g.student_id), []).append(float(g.grade_value))

        failing = []
        for sid, vals in per_student.items():
            if (sum(vals) / len(vals)) < 5.0:
                failing.append((sid, sum(vals) / len(vals)))
        return failing