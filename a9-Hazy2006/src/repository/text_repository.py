"""Text file repository implementation."""

import os
from src.repository.base_repository import Repository
from src.domain.exceptions import DuplicateException, NotFoundException


class TextFileRepository(Repository):
    # handles saving and loading from a .txt file

    def __init__(self, filename, id_getter, entity_to_string, string_to_entity):
        # we need functions to convert objects to strings and back
        self._filename = filename
        self._id_getter = id_getter
        self._entity_to_string = entity_to_string
        self._string_to_entity = string_to_entity
        self._load()

    def _load(self):
        # read from file when we start
        self._data = {}
        if os.path.exists(self._filename):
            with open(self._filename, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            # convert line back to object
                            entity = self._string_to_entity(line)
                            entity_id = self._id_getter(entity)
                            self._data[entity_id] = entity
                        except Exception:
                            # ignore bad lines
                            pass

    def _save(self):
        # write everything to file
        with open(self._filename, 'w', encoding='utf-8') as f:
            for entity in self._data.values():
                f.write(self._entity_to_string(entity) + '\n')

    def add(self, entity):
        # add to memory then save to file
        entity_id = self._id_getter(entity)
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
        entity_id = self._id_getter(entity)
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