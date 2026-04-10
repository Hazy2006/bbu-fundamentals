"""Student entity."""


class Student:
    """Represents a student in the register."""

    def __init__(self, student_id, name):
        """
        Initialize a Student.

        Args:
            student_id: Unique identifier for the student
            name: Name of the student
        """
        self._student_id = student_id
        self._name = name

    @property
    def student_id(self):
        """Get student ID."""
        return self._student_id

    @property
    def name(self):
        """Get student name."""
        return self._name

    @name.setter
    def name(self, value):
        """Set student name."""
        self._name = value

    def __eq__(self, other):
        """Check equality based on student_id."""
        if not isinstance(other, Student):
            return False
        return self._student_id == other._student_id

    def __hash__(self):
        """Hash based on student_id."""
        return hash(self._student_id)

    def __str__(self):
        """String representation."""
        return f"Student(ID={self._student_id}, Name={self._name})"

    def __repr__(self):
        """Developer-friendly representation."""
        return f"Student({self._student_id!r}, {self._name!r})"
