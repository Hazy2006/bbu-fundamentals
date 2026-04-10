from src.domain.validators import StoreException

class Repository:
    """
    In-Memory Repository.
    Acts as the base class for File repositories (for Student/Discipline).
    Uses dictionary storage.
    """
    def __init__(self):
        self._data = {}  # Dictionary to store items: {id: object}

    def add(self, entity):
        id_key = getattr(entity, 'student_id', None)
        if id_key is None:
            id_key = getattr(entity, 'discipline_id', None)

        if id_key is None:
            raise StoreException("Repository.add: unsupported entity type for dict repository")

        if id_key in self._data:
            raise StoreException(f"ID {id_key} already exists!")
        self._data[id_key] = entity

    def remove(self, entity_id):
        if entity_id not in self._data:
            raise StoreException("ID does not exist!")
        del self._data[entity_id]

    def update(self, entity):
        id_key = getattr(entity, 'student_id', None) or getattr(entity, 'discipline_id', None)
        if id_key not in self._data:
            raise StoreException("ID does not exist!")
        self._data[id_key] = entity

    def find_by_id(self, entity_id):
        return self._data.get(entity_id)

    def get_all(self):
        return list(self._data.values())

    def __len__(self):
        return len(self._data)


class GradeRepository(Repository):
    """
    Specialized repo for Grades since they don't have a single unique ID.
    Uses list storage.
    """
    def __init__(self):
        self._data = []

    def add(self, grade):
        self._data.append(grade)

    def remove_by_student(self, student_id):
        self._data = [g for g in self._data if g.student_id != student_id]

    def remove_by_discipline(self, discipline_id):
        self._data = [g for g in self._data if g.discipline_id != discipline_id]

    def get_all(self):
        return list(self._data)

    def __len__(self):
        return len(self._data)
