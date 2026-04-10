"""Tests for repositories."""

import unittest
import tempfile
import os
from src.domain.student import Student
from src.domain.discipline import Discipline
from src.domain.grade import Grade
from src.domain.exceptions import DuplicateException, NotFoundException
from src.repository.student_repository import (
    StudentMemoryRepository, StudentTextRepository, StudentBinaryRepository
)
from src.repository.discipline_repository import (
    DisciplineMemoryRepository, DisciplineTextRepository, DisciplineBinaryRepository
)
from src.repository.grade_repository import (
    GradeMemoryRepository, GradeTextRepository, GradeBinaryRepository
)


class TestStudentMemoryRepository(unittest.TestCase):
    """Tests for Student in-memory repository."""

    def setUp(self):
        """Set up test fixtures."""
        self.repo = StudentMemoryRepository()

    def test_add_student(self):
        """Test adding a student."""
        student = Student("S001", "John Doe")
        self.repo.add(student)
        self.assertEqual(self.repo.size(), 1)
        self.assertEqual(self.repo.find_by_id("S001"), student)

    def test_add_duplicate_student(self):
        """Test adding duplicate student raises exception."""
        student = Student("S001", "John Doe")
        self.repo.add(student)
        with self.assertRaises(DuplicateException):
            self.repo.add(Student("S001", "Jane Doe"))

    def test_remove_student(self):
        """Test removing a student."""
        student = Student("S001", "John Doe")
        self.repo.add(student)
        self.repo.remove("S001")
        self.assertEqual(self.repo.size(), 0)
        self.assertIsNone(self.repo.find_by_id("S001"))

    def test_remove_nonexistent_student(self):
        """Test removing nonexistent student raises exception."""
        with self.assertRaises(NotFoundException):
            self.repo.remove("S999")

    def test_update_student(self):
        """Test updating a student."""
        student = Student("S001", "John Doe")
        self.repo.add(student)
        student.name = "Jane Doe"
        self.repo.update(student)
        updated = self.repo.find_by_id("S001")
        self.assertEqual(updated.name, "Jane Doe")

    def test_update_nonexistent_student(self):
        """Test updating nonexistent student raises exception."""
        student = Student("S999", "John Doe")
        with self.assertRaises(NotFoundException):
            self.repo.update(student)

    def test_get_all_students(self):
        """Test getting all students."""
        self.repo.add(Student("S001", "John Doe"))
        self.repo.add(Student("S002", "Jane Doe"))
        students = self.repo.get_all()
        self.assertEqual(len(students), 2)


class TestStudentTextRepository(unittest.TestCase):
    """Tests for Student text file repository."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        self.temp_file.close()
        self.repo = StudentTextRepository(self.temp_file.name)

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_add_and_persist(self):
        """Test adding and persisting students."""
        student = Student("S001", "John Doe")
        self.repo.add(student)

        # Create new repo instance to test persistence
        new_repo = StudentTextRepository(self.temp_file.name)
        self.assertEqual(new_repo.size(), 1)
        self.assertEqual(new_repo.find_by_id("S001").name, "John Doe")

    def test_remove_and_persist(self):
        """Test removing and persisting."""
        self.repo.add(Student("S001", "John Doe"))
        self.repo.add(Student("S002", "Jane Doe"))
        self.repo.remove("S001")

        new_repo = StudentTextRepository(self.temp_file.name)
        self.assertEqual(new_repo.size(), 1)
        self.assertIsNone(new_repo.find_by_id("S001"))


class TestStudentBinaryRepository(unittest.TestCase):
    """Tests for Student binary file repository."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_file = tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin')
        self.temp_file.close()
        self.repo = StudentBinaryRepository(self.temp_file.name)

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_add_and_persist(self):
        """Test adding and persisting students."""
        student = Student("S001", "John Doe")
        self.repo.add(student)

        new_repo = StudentBinaryRepository(self.temp_file.name)
        self.assertEqual(new_repo.size(), 1)
        self.assertEqual(new_repo.find_by_id("S001").name, "John Doe")

    def test_remove_and_persist(self):
        """Test removing and persisting."""
        self.repo.add(Student("S001", "John Doe"))
        self.repo.add(Student("S002", "Jane Doe"))
        self.repo.remove("S001")

        new_repo = StudentBinaryRepository(self.temp_file.name)
        self.assertEqual(new_repo.size(), 1)
        self.assertIsNone(new_repo.find_by_id("S001"))


class TestDisciplineRepositories(unittest.TestCase):
    """Tests for Discipline repositories."""

    def test_memory_repository(self):
        """Test discipline memory repository."""
        repo = DisciplineMemoryRepository()
        discipline = Discipline("D001", "Mathematics")
        repo.add(discipline)
        self.assertEqual(repo.size(), 1)
        self.assertEqual(repo.find_by_id("D001"), discipline)

    def test_text_repository(self):
        """Test discipline text repository."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        temp_file.close()
        try:
            repo = DisciplineTextRepository(temp_file.name)
            discipline = Discipline("D001", "Mathematics")
            repo.add(discipline)

            new_repo = DisciplineTextRepository(temp_file.name)
            self.assertEqual(new_repo.size(), 1)
            self.assertEqual(new_repo.find_by_id("D001").name, "Mathematics")
        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)

    def test_binary_repository(self):
        """Test discipline binary repository."""
        temp_file = tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin')
        temp_file.close()
        try:
            repo = DisciplineBinaryRepository(temp_file.name)
            discipline = Discipline("D001", "Mathematics")
            repo.add(discipline)

            new_repo = DisciplineBinaryRepository(temp_file.name)
            self.assertEqual(new_repo.size(), 1)
            self.assertEqual(new_repo.find_by_id("D001").name, "Mathematics")
        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)


class TestGradeRepositories(unittest.TestCase):
    """Tests for Grade repositories."""

    def test_memory_repository(self):
        """Test grade memory repository."""
        repo = GradeMemoryRepository()
        grade = Grade("S001", "D001", 9.5)
        repo.add(grade)
        self.assertEqual(repo.size(), 1)
        self.assertEqual(repo.find_by_id(("S001", "D001")), grade)

    def test_duplicate_grade(self):
        """Test adding duplicate grade."""
        repo = GradeMemoryRepository()
        repo.add(Grade("S001", "D001", 9.5))
        with self.assertRaises(DuplicateException):
            repo.add(Grade("S001", "D001", 8.0))

    def test_text_repository(self):
        """Test grade text repository."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        temp_file.close()
        try:
            repo = GradeTextRepository(temp_file.name)
            grade = Grade("S001", "D001", 9.5)
            repo.add(grade)

            new_repo = GradeTextRepository(temp_file.name)
            self.assertEqual(new_repo.size(), 1)
            found = new_repo.find_by_id(("S001", "D001"))
            self.assertEqual(found.grade_value, 9.5)  # Should be float now
        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)

    def test_binary_repository(self):
        """Test grade binary repository."""
        temp_file = tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin')
        temp_file.close()
        try:
            repo = GradeBinaryRepository(temp_file.name)
            grade = Grade("S001", "D001", 9.5)
            repo.add(grade)

            new_repo = GradeBinaryRepository(temp_file.name)
            self.assertEqual(new_repo.size(), 1)
            self.assertEqual(new_repo.find_by_id(("S001", "D001")).grade_value, 9.5)
        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)


if __name__ == '__main__':
    unittest.main()
