import unittest
import sys
import os

# Domain
from src.domain.student import Student
from src.domain.discipline import Discipline
from src.domain.grade import Grade
from src.domain.validators import ValidationException, StoreException

# Repositories
from src.repository.base_repos import Repository, GradeRepository
from src.repository.text_repos import TextFileRepository, TextFileGradeRepository
from src.repository.binary_repos import BinaryFileRepository, BinaryGradeRepository

# Services
from src.services.student_service import StudentService
from src.services.discipline_service import DisciplineService
from src.services.grade_service import GradeService
# NEW IMPORT: Undo Service
from src.services.undo_redo_service import UndoRedoService


class TestEverything(unittest.TestCase):
    TXT_REPO = "test_run.txt"
    BIN_REPO = "test_run.pickle"

    def setUp(self):
        # 1. Clean up old files
        if os.path.exists(self.TXT_REPO): os.remove(self.TXT_REPO)
        if os.path.exists(self.BIN_REPO): os.remove(self.BIN_REPO)

        # 2. Setup Repositories
        self.s_repo = Repository()
        self.d_repo = Repository()
        self.g_repo = GradeRepository()

        # 3. Setup Undo Service (FIX FOR YOUR ERROR)
        self.undo_srv = UndoRedoService()

        # 4. Setup Services with Undo Service
        self.s_srv = StudentService(self.s_repo, self.g_repo, self.undo_srv)
        self.d_srv = DisciplineService(self.d_repo, self.g_repo, self.undo_srv)
        self.g_srv = GradeService(self.g_repo, self.s_repo, self.d_repo, self.undo_srv)

    def tearDown(self):
        if os.path.exists(self.TXT_REPO): os.remove(self.TXT_REPO)
        if os.path.exists(self.BIN_REPO): os.remove(self.BIN_REPO)

    # --- 1. DOMAIN TESTS ---
    def test_domain_equality_and_strings(self):
        """Hits __str__, __repr__, and __eq__ logic."""
        s = Student("1", "Alice")
        d = Discipline("10", "Math")
        g = Grade("1", "10", 10)

        self.assertTrue(len(str(s)) > 0)
        self.assertTrue(len(repr(s)) > 0)
        self.assertTrue(len(str(d)) > 0)
        self.assertTrue(len(repr(d)) > 0)
        self.assertTrue(len(str(g)) > 0)
        self.assertTrue(len(repr(g)) > 0)

        self.assertEqual(Student("1", "A"), Student("1", "A"))
        self.assertNotEqual(Student("1", "A"), Student("2", "B"))
        self.assertEqual(Discipline("1", "D"), Discipline("1", "D"))
        self.assertEqual(Grade("1", "1", 5), Grade("1", "1", 5))

    # --- 2. SERVICE LOGIC & VALIDATION ---
    def test_discipline_service_logic(self):
        """Hits remove_grades_by_name and search logic."""
        self.d_srv.add_discipline("10", "Math")
        self.d_srv.add_discipline("20", "Physics")

        self.assertEqual(len(self.d_srv.search("Math")), 1)
        self.assertEqual(len(self.d_srv.search("20")), 1)

        self.d_srv.update_discipline("10", "Advanced Math")
        self.assertEqual(self.d_repo.find_by_id("10").name, "Advanced Math")

        self.d_srv.remove_grades_by_name("Advanced Math")

        with self.assertRaises(StoreException):
            self.d_srv.remove_grades_by_name("Ghost Subject")

        with self.assertRaises(StoreException):
            self.d_srv.remove_discipline("999")

    def test_validation_and_generators(self):
        # Validation - Student
        with self.assertRaises(ValidationException): self.s_srv.add_student("", "Bad")
        with self.assertRaises(ValidationException): self.s_srv.add_student("1", "")

        # Validation - Discipline
        with self.assertRaises(ValidationException): self.d_srv.add_discipline("", "Bad")

        # Validation - Grade
        with self.assertRaises(ValidationException): self.g_srv.add_grade("99", "10", 10)

        # Generators
        self.s_srv.generate_random(1)
        self.d_srv.generate_random(1)
        self.g_srv.generate_random(1)

    # --- 3. REPOSITORY OVERRIDES ---
    def test_repo_overrides(self):
        """Hits the specialized remove methods in file repos."""

        def g_ser(g): return f"{g.student_id},{g.discipline_id},{g.grade_value}"

        def g_par(line): p = line.split(','); return Grade(p[0], p[1], int(p[2]))

        # TEXT REPO
        tr = TextFileGradeRepository(self.TXT_REPO, g_par, g_ser)
        tr.add(Grade("S1", "D1", 10))
        tr.remove_by_student("S1")  # Hit override
        self.assertEqual(len(tr), 0)

        tr.add(Grade("S2", "D1", 8))
        tr.remove_by_discipline("D1")  # Hit override
        self.assertEqual(len(tr), 0)

        # BINARY REPO
        br = BinaryGradeRepository(self.BIN_REPO)
        br.add(Grade("S1", "D1", 10))
        br.remove_by_student("S1")  # Hit override
        self.assertEqual(len(br), 0)

        br.add(Grade("S2", "D1", 8))
        br.remove_by_discipline("D1")  # Hit override
        self.assertEqual(len(br), 0)

    def test_corrupt_files(self):
        # Text
        with open(self.TXT_REPO, "w") as f: f.write("GARBAGE")
        repo = TextFileRepository(self.TXT_REPO, Student, lambda x: x, lambda x: x)
        self.assertEqual(len(repo), 0)

        # Binary
        with open(self.BIN_REPO, "wb") as f: f.write(b"GARBAGE")
        repo2 = BinaryFileRepository(self.BIN_REPO)
        self.assertEqual(len(repo2), 0)


class Tests:
    def run_all_tests(self):
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromModule(sys.modules[__name__])
        runner = unittest.TextTestRunner(verbosity=0)
        result = runner.run(suite)
        return result.wasSuccessful()