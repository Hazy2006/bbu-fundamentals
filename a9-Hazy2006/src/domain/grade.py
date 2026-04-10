"""Grade entity."""


class Grade:
    """Represents a grade for a student in a discipline."""

    def __init__(self, student_id, discipline_id, grade_value):
        """
        Initialize a Grade.

        Args:
            student_id: ID of the student
            discipline_id: ID of the discipline
            grade_value: Grade value (numeric)
        """
        self._student_id = student_id
        self._discipline_id = discipline_id
        self._grade_value = grade_value

    @property
    def student_id(self):
        """Get student ID."""
        return self._student_id

    @property
    def discipline_id(self):
        """Get discipline ID."""
        return self._discipline_id

    @property
    def grade_value(self):
        """Get grade value."""
        return self._grade_value

    @grade_value.setter
    def grade_value(self, value):
        """Set grade value."""
        self._grade_value = value

    def __eq__(self, other):
        """Check equality based on student_id and discipline_id."""
        if not isinstance(other, Grade):
            return False
        return (self._student_id == other._student_id and
                self._discipline_id == other._discipline_id)

    def __hash__(self):
        """Hash based on student_id and discipline_id."""
        return hash((self._student_id, self._discipline_id))

    def __str__(self):
        """String representation."""
        return f"Grade(Student={self._student_id}, Discipline={self._discipline_id}, Value={self._grade_value})"

    def __repr__(self):
        """Developer-friendly representation."""
        return f"Grade({self._student_id!r}, {self._discipline_id!r}, {self._grade_value!r})"
