import random
from src.domain.grade import Grade
from src.domain.validators import ValidationException


class GradeService:
    def __init__(self, grade_repo, student_repo, disc_repo, undo_service):
        self._repo = grade_repo
        self._s_repo = student_repo
        self._d_repo = disc_repo
        self._undo_service = undo_service

    def add_grade(self, s_id, d_id, value):
        s_id, d_id = str(s_id).strip(), str(d_id).strip()

        # 1. Validation
        if not self._find_any_type(self._s_repo, s_id):
            raise ValidationException(f"Student {s_id} not found.")
        if not self._find_any_type(self._d_repo, d_id):
            raise ValidationException(f"Discipline {d_id} not found.")

        try:
            val = float(value)
        except:
            raise ValidationException("Grade must be a number.")
        if not (1 <= val <= 10):
            raise ValidationException("Grade must be between 1 and 10.")

        # 2. Check Duplicates (To prevent logic errors)
        if self._is_duplicate(s_id, d_id, val):
            return

        # 3. Create & Add
        g = Grade(s_id, d_id, val)
        self._repo.add(g)

    def remove_grade(self, s_id, d_id):
        """
        Removes grades for a student at a specific discipline.
        """
        s_id, d_id = str(s_id).strip(), str(d_id).strip()
        all_grades = self._repo.get_all()
        to_remove = [g for g in all_grades if str(g.student_id) == s_id and str(g.discipline_id) == d_id]

        if not to_remove:
            raise ValidationException("No grades found to remove.")

        for g in to_remove:
            self._repo.remove(g)

    def force_generate_grades_for_all(self):
        # Used for Option 12
        students = self._s_repo.get_all()
        discs = self._d_repo.get_all()
        if not students or not discs: return 0

        count = 0

        for s in students:
            for _ in range(3):
                d = random.choice(discs)
                val = round(random.uniform(4.00, 10.00), 2)
                s_id, d_id = str(s.student_id), str(d.discipline_id)

                if self._is_duplicate(s_id, d_id, val): continue

                g = Grade(s_id, d_id, val)
                self._repo.add(g)
                count += 1

        return count

    # --- Helpers ---
    def _is_duplicate(self, s_id, d_id, val):
        for existing in self._repo.get_all():
            if (str(existing.student_id) == s_id and
                    str(existing.discipline_id) == d_id and
                    abs(existing.grade_value - val) < 0.001):
                return True
        return False

    def _find_any_type(self, repo, entity_id):
        res = repo.find_by_id(str(entity_id))
        if res: return res
        try:
            return repo.find_by_id(int(entity_id))
        except:
            return None

    def _remove_grade_by_val(self, sid, did, val):
        target = next((g for g in self._repo.get_all() if
                       str(g.student_id) == str(sid) and
                       str(g.discipline_id) == str(did) and
                       abs(g.grade_value - val) < 0.001), None)
        if target:
            try:
                self._repo.remove(target)
            except:
                pass

    def get_all(self):
        # Filter orphans
        raw = self._repo.get_all()
        return [g for g in raw if
                self._find_any_type(self._s_repo, g.student_id) and self._find_any_type(self._d_repo, g.discipline_id)]

    def get_top_students(self):
        grades = self.get_all()
        if not grades: return []
        s_map = {}
        for g in grades: s_map.setdefault(str(g.student_id), []).append(g.grade_value)
        results = []
        for sid, vals in s_map.items():
            avg = sum(vals) / len(vals)
            s_obj = self._find_any_type(self._s_repo, sid)
            name = s_obj.name if s_obj else "Unknown"
            results.append((avg, sid, name))
        results.sort(key=lambda x: x[0], reverse=True)
        return results[:8]  # simplified top 8

    def generate_random(self, n=20):
        # Startup generator
        students = self._s_repo.get_all()
        discs = self._d_repo.get_all()
        if not students or not discs: return
        for _ in range(n):
            s = random.choice(students)
            d = random.choice(discs)
            val = round(random.uniform(4.00, 10.00), 2)
            try:
                self.add_grade(s.student_id, d.discipline_id, val)
            except:
                pass

