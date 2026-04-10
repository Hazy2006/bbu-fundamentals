"""Discipline entity."""


class Discipline:
    """Represents a discipline (course/subject) in the register."""

    def __init__(self, discipline_id, name):
        """
        Initialize a Discipline.

        Args:
            discipline_id: Unique identifier for the discipline
            name: Name of the discipline
        """
        self._discipline_id = discipline_id
        self._name = name

    @property
    def discipline_id(self):
        """Get discipline ID."""
        return self._discipline_id

    @property
    def name(self):
        """Get discipline name."""
        return self._name

    @name.setter
    def name(self, value):
        """Set discipline name."""
        self._name = value

    def __eq__(self, other):
        """Check equality based on discipline_id."""
        if not isinstance(other, Discipline):
            return False
        return self._discipline_id == other._discipline_id

    def __hash__(self):
        """Hash based on discipline_id."""
        return hash(self._discipline_id)

    def __str__(self):
        """String representation."""
        return f"Discipline(ID={self._discipline_id}, Name={self._name})"

    def __repr__(self):
        """Developer-friendly representation."""
        return f"Discipline({self._discipline_id!r}, {self._name!r})"
