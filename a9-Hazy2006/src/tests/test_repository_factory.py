"""Tests for repository factory."""

import unittest
import tempfile
import os
from src.repository.repository_factory import load_settings, create_repositories
from src.repository.student_repository import (
    StudentMemoryRepository, StudentTextRepository, StudentBinaryRepository
)
from src.repository.discipline_repository import (
    DisciplineMemoryRepository, DisciplineTextRepository, DisciplineBinaryRepository
)
from src.repository.grade_repository import (
    GradeMemoryRepository, GradeTextRepository, GradeBinaryRepository
)


class TestRepositoryFactory(unittest.TestCase):
    """Tests for repository factory."""

    def test_load_settings_default(self):
        """Test loading settings with missing file defaults to memory."""
        # Temporarily move settings file if it exists
        settings_exists = os.path.exists('settings.properties')
        if settings_exists:
            os.rename('settings.properties', 'settings.properties.bak')

        try:
            settings = load_settings()
            self.assertEqual(settings.get('repository'), 'memory')
        finally:
            if settings_exists:
                os.rename('settings.properties.bak', 'settings.properties')

    def test_load_settings_from_file(self):
        """Test loading settings from file."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.properties')
        temp_file.write('repository=text\n')
        temp_file.close()

        # Temporarily use temp file
        settings_exists = os.path.exists('settings.properties')
        if settings_exists:
            os.rename('settings.properties', 'settings.properties.bak')
        os.rename(temp_file.name, 'settings.properties')

        try:
            settings = load_settings()
            self.assertEqual(settings.get('repository'), 'text')
        finally:
            os.rename('settings.properties', temp_file.name)
            if settings_exists:
                os.rename('settings.properties.bak', 'settings.properties')
            os.unlink(temp_file.name)

    def test_create_memory_repositories(self):
        """Test creating memory repositories."""
        # Temporarily set to memory
        settings_exists = os.path.exists('settings.properties')
        if settings_exists:
            os.rename('settings.properties', 'settings.properties.bak')

        with open('settings.properties', 'w') as f:
            f.write('repository=memory\n')

        try:
            student_repo, discipline_repo, grade_repo = create_repositories()
            self.assertIsInstance(student_repo, StudentMemoryRepository)
            self.assertIsInstance(discipline_repo, DisciplineMemoryRepository)
            self.assertIsInstance(grade_repo, GradeMemoryRepository)
        finally:
            os.unlink('settings.properties')
            if settings_exists:
                os.rename('settings.properties.bak', 'settings.properties')

    def test_create_text_repositories(self):
        """Test creating text repositories."""
        settings_exists = os.path.exists('settings.properties')
        if settings_exists:
            os.rename('settings.properties', 'settings.properties.bak')

        with open('settings.properties', 'w') as f:
            f.write('repository=text\n')

        try:
            student_repo, discipline_repo, grade_repo = create_repositories()
            self.assertIsInstance(student_repo, StudentTextRepository)
            self.assertIsInstance(discipline_repo, DisciplineTextRepository)
            self.assertIsInstance(grade_repo, GradeTextRepository)

            # Clean up created files
            for filename in ['students.txt', 'disciplines.txt', 'grades.txt']:
                if os.path.exists(filename):
                    os.unlink(filename)
        finally:
            os.unlink('settings.properties')
            if settings_exists:
                os.rename('settings.properties.bak', 'settings.properties')

    def test_create_binary_repositories(self):
        """Test creating binary repositories."""
        settings_exists = os.path.exists('settings.properties')
        if settings_exists:
            os.rename('settings.properties', 'settings.properties.bak')

        with open('settings.properties', 'w') as f:
            f.write('repository=binary\n')

        try:
            student_repo, discipline_repo, grade_repo = create_repositories()
            self.assertIsInstance(student_repo, StudentBinaryRepository)
            self.assertIsInstance(discipline_repo, DisciplineBinaryRepository)
            self.assertIsInstance(grade_repo, GradeBinaryRepository)

            # Clean up created files
            for filename in ['students.bin', 'disciplines.bin', 'grades.bin']:
                if os.path.exists(filename):
                    os.unlink(filename)
        finally:
            os.unlink('settings.properties')
            if settings_exists:
                os.rename('settings.properties.bak', 'settings.properties')


if __name__ == '__main__':
    unittest.main()
