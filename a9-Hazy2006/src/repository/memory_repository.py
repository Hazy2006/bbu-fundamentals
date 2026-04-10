"""In-memory repository implementation."""

from src.repository.base_repository import Repository
from src.domain.exceptions import DuplicateException, NotFoundException


class InMemoryRepository(Repository):
    # stores data in a simple dictionary

    def __init__(self, id_getter):
        # id_getter is a function that tells us how to find the ID of an object
        self._data = {}
        self._id_getter = id_getter

    def add(self, entity):
        # check if it exists, then add it
        entity_id = self._id_getter(entity)
        if entity_id in self._data:
            raise DuplicateException(f"ID {entity_id} already exists")
        self._data[entity_id] = entity

    def remove(self, entity_id):
        # remove by ID if found
        if entity_id not in self._data:
            raise NotFoundException(f"ID {entity_id} not found")
        del self._data[entity_id]

    def update(self, entity):
        # replace the existing entity
        entity_id = self._id_getter(entity)
        if entity_id not in self._data:
            raise NotFoundException(f"ID {entity_id} not found")
        self._data[entity_id] = entity

    def find_by_id(self, entity_id):
        return self._data.get(entity_id)

    def get_all(self):
        return list(self._data.values())

    def size(self):
        return len(self._data)