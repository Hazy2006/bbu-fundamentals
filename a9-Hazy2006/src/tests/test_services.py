"""Tests for services."""

import unittest
from src.domain.student import Student
from src.domain.discipline import Discipline
from src.domain.grade import Grade
from src.domain.exceptions import ValidationException, NotFoundException, DuplicateException
from src.repository.student_repository import StudentMemoryRepository
from src.repository.discipline_repository import DisciplineMemoryRepository
from src.repository.grade_repository import GradeMemoryRepository
from src.service.student_service import StudentService
from src.service.discipline_service import DisciplineService
from src.service.grade_service import GradeService


class TestStudentService(unittest.TestCase):
    """Tests for Student service."""

    def setUp(self):
        """Set up test fixtures."""
        self.student_repo = StudentMemoryRepository()
        self.grade_repo = GradeMemoryRepository()
        self.service = StudentService(self.student_repo, self.grade_repo)

    def test_add_student(self):
        """Test adding a student."""
        student = self.service.add_student("S001", "John Doe")
        self.assertEqual(student.student_id, "S001")
        self.assertEqual(student.name, "John Doe")
        self.assertEqual(self.student_repo.size(), 1)

    def test_add_student_strips_whitespace(self):
        """Test adding student strips whitespace."""
        student = self.service.add_student("S001", "  John Doe  ")
        self.assertEqual(student.name, "John Doe")

    def test_add_student_empty_id(self):
        """Test adding student with empty ID raises error."""
        with self.assertRaises(ValidationException):
            self.service.add_student("", "John Doe")

    def test_add_student_empty_name(self):
        """Test adding student with empty name raises error."""
        with self.assertRaises(ValidationException):
            self.service.add_student("S001", "")

    def test_remove_student(self):
        """Test removing a student."""
        self.service.add_student("S001", "John Doe")
        self.service.remove_student("S001")
        self.assertEqual(self.student_repo.size(), 0)

    def test_remove_student_cascade_delete(self):
        """Test removing student cascades to grades."""
        # Add student and grade
        self.service.add_student("S001", "John Doe")
        self.grade_repo.add(Grade("S001", "D001", 9.5))

        # Remove student
        self.service.remove_student("S001")

        # Grade should be removed
        self.assertEqual(self.grade_repo.size(), 0)

    def test_update_student(self):
        """Test updating a student."""
        self.service.add_student("S001", "John Doe")
        updated = self.service.update_student("S001", "Jane Doe")
        self.assertEqual(updated.name, "Jane Doe")

    def test_update_student_empty_name(self):
        """Test updating student with empty name raises error."""
        self.service.add_student("S001", "John Doe")
        with self.assertRaises(ValidationException):
            self.service.update_student("S001", "")

    def test_update_nonexistent_student(self):
        """Test updating nonexistent student raises error."""
        with self.assertRaises(ValidationException):
            self.service.update_student("S999", "John Doe")

    def test_find_student(self):
        """Test finding a student."""
        self.service.add_student("S001", "John Doe")
        student = self.service.find_student("S001")
        self.assertIsNotNone(student)
        self.assertEqual(student.name, "John Doe")

    def test_find_nonexistent_student(self):
        """Test finding nonexistent student returns None."""
        student = self.service.find_student("S999")
        self.assertIsNone(student)

    def test_get_all_students(self):
        """Test getting all students."""
        self.service.add_student("S001", "John Doe")
        self.service.add_student("S002", "Jane Doe")
        students = self.service.get_all_students()
        self.assertEqual(len(students), 2)

    def test_search_students_by_id(self):
        """Test searching students by ID."""
        self.service.add_student("S001", "John Doe")
        self.service.add_student("S002", "Jane Doe")
        results = self.service.search_students("001")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].student_id, "S001")

    def test_search_students_by_name(self):
        """Test searching students by name."""
        self.service.add_student("S001", "John Doe")
        self.service.add_student("S002", "Jane Doe")
        results = self.service.search_students("john")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "John Doe")

    def test_search_students_case_insensitive(self):
        """Test searching students is case insensitive."""
        self.service.add_student("S001", "John Doe")
        results = self.service.search_students("JOHN")
        self.assertEqual(len(results), 1)

    def test_search_students_partial_match(self):
        """Test searching students with partial match."""
        self.service.add_student("S001", "John Doe")
        self.service.add_student("S002", "Jane Doe")
        results = self.service.search_students("doe")
        self.assertEqual(len(results), 2)


class TestDisciplineService(unittest.TestCase):
    """Tests for Discipline service."""

    def setUp(self):
        """Set up test fixtures."""
        self.discipline_repo = DisciplineMemoryRepository()
        self.grade_repo = GradeMemoryRepository()
        self.service = DisciplineService(self.discipline_repo, self.grade_repo)

    def test_add_discipline(self):
        """Test adding a discipline."""
        discipline = self.service.add_discipline("D001", "Mathematics")
        self.assertEqual(discipline.discipline_id, "D001")
        self.assertEqual(discipline.name, "Mathematics")

    def test_add_discipline_empty_id(self):
        """Test adding discipline with empty ID raises error."""
        with self.assertRaises(ValidationException):
            self.service.add_discipline("", "Mathematics")

    def test_add_discipline_empty_name(self):
        """Test adding discipline with empty name raises error."""
        with self.assertRaises(ValidationException):
            self.service.add_discipline("D001", "")

    def test_remove_discipline_cascade_delete(self):
        """Test removing discipline cascades to grades."""
        self.service.add_discipline("D001", "Mathematics")
        self.grade_repo.add(Grade("S001", "D001", 9.5))

        self.service.remove_discipline("D001")

        self.assertEqual(self.grade_repo.size(), 0)

    def test_update_discipline(self):
        """Test updating a discipline."""
        self.service.add_discipline("D001", "Mathematics")
        updated = self.service.update_discipline("D001", "Physics")
        self.assertEqual(updated.name, "Physics")

    def test_search_disciplines(self):
        """Test searching disciplines."""
        self.service.add_discipline("D001", "Mathematics")
        self.service.add_discipline("D002", "Physics")
        results = self.service.search_disciplines("math")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Mathematics")


class TestGradeService(unittest.TestCase):
    """Tests for Grade service."""

    def setUp(self):
        """Set up test fixtures."""
        self.student_repo = StudentMemoryRepository()
        self.discipline_repo = DisciplineMemoryRepository()
        self.grade_repo = GradeMemoryRepository()
        self.service = GradeService(
            self.grade_repo, self.student_repo, self.discipline_repo
        )

        # Add test data
        self.student_repo.add(Student("S001", "John Doe"))
        self.discipline_repo.add(Discipline("D001", "Mathematics"))

    def test_add_grade(self):
        """Test adding a grade."""
        grade = self.service.add_grade("S001", "D001", 9.5)
        self.assertEqual(grade.student_id, "S001")
        self.assertEqual(grade.discipline_id, "D001")
        self.assertEqual(grade.grade_value, 9.5)

    def test_add_grade_student_not_found(self):
        """Test adding grade for nonexistent student raises error."""
        with self.assertRaises(ValidationException):
            self.service.add_grade("S999", "D001", 9.5)

    def test_add_grade_discipline_not_found(self):
        """Test adding grade for nonexistent discipline raises error."""
        with self.assertRaises(ValidationException):
            self.service.add_grade("S001", "D999", 9.5)

    def test_add_grade_invalid_value(self):
        """Test adding grade with invalid value raises error."""
        with self.assertRaises(ValidationException):
            self.service.add_grade("S001", "D001", "invalid")

    def test_add_grade_out_of_range(self):
        """Test adding grade out of range raises error."""
        with self.assertRaises(ValidationException):
            self.service.add_grade("S001", "D001", 11)
        with self.assertRaises(ValidationException):
            self.service.add_grade("S001", "D001", -1)

    def test_update_grade(self):
        """Test updating a grade."""
        self.service.add_grade("S001", "D001", 9.5)
        updated = self.service.update_grade("S001", "D001", 8.0)
        self.assertEqual(updated.grade_value, 8.0)

    def test_update_nonexistent_grade(self):
        """Test updating nonexistent grade raises error."""
        with self.assertRaises(ValidationException):
            self.service.update_grade("S001", "D001", 9.5)

    def test_remove_grade(self):
        """Test removing a grade."""
        self.service.add_grade("S001", "D001", 9.5)
        self.service.remove_grade("S001", "D001")
        self.assertEqual(self.grade_repo.size(), 0)

    def test_find_grade(self):
        """Test finding a grade."""
        self.service.add_grade("S001", "D001", 9.5)
        grade = self.service.find_grade("S001", "D001")
        self.assertIsNotNone(grade)
        self.assertEqual(grade.grade_value, 9.5)

    def test_get_all_grades(self):
        """Test getting all grades."""
        self.service.add_grade("S001", "D001", 9.5)
        grades = self.service.get_all_grades()
        self.assertEqual(len(grades), 1)

    def test_get_grades_for_student(self):
        """Test getting grades for a student."""
        self.discipline_repo.add(Discipline("D002", "Physics"))
        self.service.add_grade("S001", "D001", 9.5)
        self.service.add_grade("S001", "D002", 8.0)

        grades = self.service.get_grades_for_student("S001")
        self.assertEqual(len(grades), 2)

    def test_get_grades_for_discipline(self):
        """Test getting grades for a discipline."""
        self.student_repo.add(Student("S002", "Jane Doe"))
        self.service.add_grade("S001", "D001", 9.5)
        self.service.add_grade("S002", "D001", 8.0)

        grades = self.service.get_grades_for_discipline("D001")
        self.assertEqual(len(grades), 2)


if __name__ == '__main__':
    unittest.main()
