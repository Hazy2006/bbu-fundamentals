"""Tests for domain entities."""

import unittest
from src.domain.student import Student
from src.domain.discipline import Discipline
from src.domain.grade import Grade


class TestStudent(unittest.TestCase):
    """Tests for Student entity."""

    def test_create_student(self):
        """Test student creation."""
        student = Student("S001", "John Doe")
        self.assertEqual(student.student_id, "S001")
        self.assertEqual(student.name, "John Doe")

    def test_student_name_setter(self):
        """Test student name setter."""
        student = Student("S001", "John Doe")
        student.name = "Jane Doe"
        self.assertEqual(student.name, "Jane Doe")

    def test_student_equality(self):
        """Test student equality based on ID."""
        student1 = Student("S001", "John Doe")
        student2 = Student("S001", "Jane Doe")
        student3 = Student("S002", "John Doe")
        self.assertEqual(student1, student2)
        self.assertNotEqual(student1, student3)

    def test_student_hash(self):
        """Test student hash."""
        student1 = Student("S001", "John Doe")
        student2 = Student("S001", "Jane Doe")
        self.assertEqual(hash(student1), hash(student2))

    def test_student_str(self):
        """Test student string representation."""
        student = Student("S001", "John Doe")
        self.assertIn("S001", str(student))
        self.assertIn("John Doe", str(student))

    def test_student_repr(self):
        """Test student repr."""
        student = Student("S001", "John Doe")
        self.assertIn("S001", repr(student))
        self.assertIn("John Doe", repr(student))


class TestDiscipline(unittest.TestCase):
    """Tests for Discipline entity."""

    def test_create_discipline(self):
        """Test discipline creation."""
        discipline = Discipline("D001", "Mathematics")
        self.assertEqual(discipline.discipline_id, "D001")
        self.assertEqual(discipline.name, "Mathematics")

    def test_discipline_name_setter(self):
        """Test discipline name setter."""
        discipline = Discipline("D001", "Mathematics")
        discipline.name = "Physics"
        self.assertEqual(discipline.name, "Physics")

    def test_discipline_equality(self):
        """Test discipline equality based on ID."""
        disc1 = Discipline("D001", "Mathematics")
        disc2 = Discipline("D001", "Physics")
        disc3 = Discipline("D002", "Mathematics")
        self.assertEqual(disc1, disc2)
        self.assertNotEqual(disc1, disc3)

    def test_discipline_hash(self):
        """Test discipline hash."""
        disc1 = Discipline("D001", "Mathematics")
        disc2 = Discipline("D001", "Physics")
        self.assertEqual(hash(disc1), hash(disc2))

    def test_discipline_str(self):
        """Test discipline string representation."""
        discipline = Discipline("D001", "Mathematics")
        self.assertIn("D001", str(discipline))
        self.assertIn("Mathematics", str(discipline))

    def test_discipline_repr(self):
        """Test discipline repr."""
        discipline = Discipline("D001", "Mathematics")
        self.assertIn("D001", repr(discipline))
        self.assertIn("Mathematics", repr(discipline))


class TestGrade(unittest.TestCase):
    """Tests for Grade entity."""

    def test_create_grade(self):
        """Test grade creation."""
        grade = Grade("S001", "D001", 9.5)
        self.assertEqual(grade.student_id, "S001")
        self.assertEqual(grade.discipline_id, "D001")
        self.assertEqual(grade.grade_value, 9.5)

    def test_grade_value_setter(self):
        """Test grade value setter."""
        grade = Grade("S001", "D001", 9.5)
        grade.grade_value = 8.0
        self.assertEqual(grade.grade_value, 8.0)

    def test_grade_equality(self):
        """Test grade equality based on student and discipline IDs."""
        grade1 = Grade("S001", "D001", 9.5)
        grade2 = Grade("S001", "D001", 8.0)
        grade3 = Grade("S001", "D002", 9.5)
        self.assertEqual(grade1, grade2)
        self.assertNotEqual(grade1, grade3)

    def test_grade_hash(self):
        """Test grade hash."""
        grade1 = Grade("S001", "D001", 9.5)
        grade2 = Grade("S001", "D001", 8.0)
        self.assertEqual(hash(grade1), hash(grade2))

    def test_grade_str(self):
        """Test grade string representation."""
        grade = Grade("S001", "D001", 9.5)
        self.assertIn("S001", str(grade))
        self.assertIn("D001", str(grade))
        self.assertIn("9.5", str(grade))

    def test_grade_repr(self):
        """Test grade repr."""
        grade = Grade("S001", "D001", 9.5)
        self.assertIn("S001", repr(grade))
        self.assertIn("D001", repr(grade))
        self.assertIn("9.5", repr(grade))


if __name__ == '__main__':
    unittest.main()
