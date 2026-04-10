"""Additional tests to improve coverage."""

import unittest
import tempfile
import os
from src.domain.student import Student
from src.domain.discipline import Discipline
from src.domain.grade import Grade
from src.repository.text_repository import TextFileRepository
from src.repository.binary_repository import BinaryFileRepository
from src.repository.student_repository import StudentMemoryRepository
from src.repository.discipline_repository import DisciplineMemoryRepository
from src.service.student_service import StudentService
from src.service.discipline_service import DisciplineService
from src.service.grade_service import GradeService


class TestTextRepositoryCoverage(unittest.TestCase):
    """Additional tests for text repository coverage."""

    def test_invalid_line_handling(self):
        """Test that invalid lines in text file are skipped."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        temp_file.write("S001;John Doe\n")
        temp_file.write("invalid line without semicolon\n")
        temp_file.write("S002;Jane Doe\n")
        temp_file.close()

        try:
            repo = TextFileRepository(
                temp_file.name,
                lambda s: s.student_id,
                lambda s: f"{s.student_id};{s.name}",
                lambda line: Student(*line.split(';', 1))
            )
            # Should load 2 valid students and skip invalid line
            self.assertEqual(repo.size(), 2)
        finally:
            os.unlink(temp_file.name)

    def test_empty_file_handling(self):
        """Test handling of file with empty lines."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        temp_file.write("S001;John Doe\n")
        temp_file.write("\n")
        temp_file.write("  \n")
        temp_file.write("S002;Jane Doe\n")
        temp_file.close()

        try:
            repo = TextFileRepository(
                temp_file.name,
                lambda s: s.student_id,
                lambda s: f"{s.student_id};{s.name}",
                lambda line: Student(*line.split(';', 1))
            )
            self.assertEqual(repo.size(), 2)
        finally:
            os.unlink(temp_file.name)


class TestBinaryRepositoryCoverage(unittest.TestCase):
    """Additional tests for binary repository coverage."""

    def test_corrupted_file_handling(self):
        """Test handling of corrupted binary file."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.bin')
        temp_file.write("corrupted data")
        temp_file.close()

        try:
            # Should handle corrupted file gracefully
            repo = BinaryFileRepository(temp_file.name, lambda s: s.student_id)
            self.assertEqual(repo.size(), 0)
        finally:
            os.unlink(temp_file.name)


class TestServiceCoverage(unittest.TestCase):
    """Additional tests for service coverage."""

    def test_discipline_find(self):
        """Test finding a discipline."""
        from src.repository.grade_repository import GradeMemoryRepository
        discipline_repo = DisciplineMemoryRepository()
        grade_repo = GradeMemoryRepository()
        service = DisciplineService(discipline_repo, grade_repo)

        service.add_discipline("D001", "Mathematics")
        found = service.find_discipline("D001")
        self.assertIsNotNone(found)

        not_found = service.find_discipline("D999")
        self.assertIsNone(not_found)

    def test_discipline_get_all(self):
        """Test getting all disciplines."""
        from src.repository.grade_repository import GradeMemoryRepository
        discipline_repo = DisciplineMemoryRepository()
        grade_repo = GradeMemoryRepository()
        service = DisciplineService(discipline_repo, grade_repo)

        service.add_discipline("D001", "Mathematics")
        service.add_discipline("D002", "Physics")
        all_discs = service.get_all_disciplines()
        self.assertEqual(len(all_discs), 2)

    def test_grade_remove_not_found(self):
        """Test removing nonexistent grade."""
        from src.repository.grade_repository import GradeMemoryRepository
        student_repo = StudentMemoryRepository()
        discipline_repo = DisciplineMemoryRepository()
        grade_repo = GradeMemoryRepository()
        service = GradeService(grade_repo, student_repo, discipline_repo)

        from src.domain.exceptions import NotFoundException
        with self.assertRaises(NotFoundException):
            service.remove_grade("S001", "D001")


class TestEntityEquality(unittest.TestCase):
    """Test entity equality edge cases."""

    def test_student_not_equal_to_other_type(self):
        """Test student not equal to other types."""
        student = Student("S001", "John")
        self.assertNotEqual(student, "S001")
        self.assertNotEqual(student, None)

    def test_discipline_not_equal_to_other_type(self):
        """Test discipline not equal to other types."""
        discipline = Discipline("D001", "Math")
        self.assertNotEqual(discipline, "D001")
        self.assertNotEqual(discipline, None)

    def test_grade_not_equal_to_other_type(self):
        """Test grade not equal to other types."""
        grade = Grade("S001", "D001", 9.5)
        self.assertNotEqual(grade, ("S001", "D001"))
        self.assertNotEqual(grade, None)


if __name__ == '__main__':
    unittest.main()
