"""Custom exceptions for the Student Register application."""


class StudentRegisterException(Exception):
    """Base exception for all Student Register errors."""
    pass


class ValidationException(StudentRegisterException):
    """Exception raised when validation fails."""
    pass


class RepositoryException(StudentRegisterException):
    """Exception raised for repository operations."""
    pass


class DuplicateException(RepositoryException):
    """Exception raised when trying to add a duplicate entity."""
    pass


class NotFoundException(RepositoryException):
    """Exception raised when an entity is not found."""
    pass


class ServiceException(StudentRegisterException):
    """Exception raised for service layer operations."""
    pass
