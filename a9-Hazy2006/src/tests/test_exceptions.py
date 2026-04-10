"""Tests for exceptions."""

import unittest
from src.domain.exceptions import (
    StudentRegisterException, ValidationException, RepositoryException,
    DuplicateException, NotFoundException, ServiceException
)


class TestExceptions(unittest.TestCase):
    """Tests for custom exceptions."""

    def test_student_register_exception(self):
        """Test base exception."""
        exc = StudentRegisterException("Test error")
        self.assertIsInstance(exc, Exception)
        self.assertEqual(str(exc), "Test error")

    def test_validation_exception(self):
        """Test validation exception."""
        exc = ValidationException("Validation error")
        self.assertIsInstance(exc, StudentRegisterException)
        self.assertEqual(str(exc), "Validation error")

    def test_repository_exception(self):
        """Test repository exception."""
        exc = RepositoryException("Repository error")
        self.assertIsInstance(exc, StudentRegisterException)
        self.assertEqual(str(exc), "Repository error")

    def test_duplicate_exception(self):
        """Test duplicate exception."""
        exc = DuplicateException("Duplicate error")
        self.assertIsInstance(exc, RepositoryException)
        self.assertEqual(str(exc), "Duplicate error")

    def test_not_found_exception(self):
        """Test not found exception."""
        exc = NotFoundException("Not found error")
        self.assertIsInstance(exc, RepositoryException)
        self.assertEqual(str(exc), "Not found error")

    def test_service_exception(self):
        """Test service exception."""
        exc = ServiceException("Service error")
        self.assertIsInstance(exc, StudentRegisterException)
        self.assertEqual(str(exc), "Service error")


if __name__ == '__main__':
    unittest.main()
