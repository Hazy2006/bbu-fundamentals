import os
import pickle
from src.repository.base_repository import Repository
from src.domain.exceptions import DuplicateException, NotFoundException


class BinaryFileRepository(Repository):
    def __init__(self, filename):
        self._filename = filename
        self._data = {}
        self._load()

    def _load(self):
        # try to load data from the binary file
        if os.path.exists(self._filename):
            try:
                with open(self._filename, 'rb') as f:
                    self._data = pickle.load(f)
            except Exception:
                # if file is empty or corrupted, start empty
                self._data = {}
        else:
            self._data = {}

    def _save(self):
        # save the dictionary to the file
        with open(self._filename, 'wb') as f:
            pickle.dump(self._data, f)

    def add(self, entity):
        # we assume entity has an 'id' property or we handle it in the service
        # Note: Your previous code used 'id_getter'.
        # Simpler way for students: checking the specific attribute based on entity type,
        # or just passing the ID in.

        # Let's keep it generic using the ID from the entity if possible.
        # BUT, standard student way is usually checking instance types.
        # To match your structure, let's trust the entity has a unique ID property.

        entity_id = self._get_id(entity)
        if entity_id in self._data:
            raise DuplicateException(f"ID {entity_id} already exists")

        self._data[entity_id] = entity
        self._save()

    def remove(self, entity_id):
        if entity_id not in self._data:
            raise NotFoundException(f"ID {entity_id} not found")

        del self._data[entity_id]
        self._save()

    def update(self, entity):
        entity_id = self._get_id(entity)
        if entity_id not in self._data:
            raise NotFoundException(f"ID {entity_id} not found")

        self._data[entity_id] = entity
        self._save()

    def find_by_id(self, entity_id):
        return self._data.get(entity_id)

    def get_all(self):
        return list(self._data.values())

    def size(self):
        return len(self._data)

    def _get_id(self, entity):
        # Helper to get ID depending on what object it is
        # This is the "Student" way to avoid passing 'id_getter' functions around
        if hasattr(entity, 'student_id'):
            return entity.student_id
        elif hasattr(entity, 'discipline_id'):
            return entity.discipline_id
        elif hasattr(entity, 'assignment_id'):
            return entity.assignment_id
        # fallback
        return getattr(entity, 'id', None)