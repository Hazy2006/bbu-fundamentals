from abc import ABC, abstractmethod


class Repository(ABC):
    """
    Abstract class for all repositories.
    Forces us to implement add, remove, find, etc.
    """

    @abstractmethod
    def add(self, entity):
        # Adds an entity to the list
        pass

    @abstractmethod
    def remove(self, entity_id):
        # Removes entity by its ID
        pass

    @abstractmethod
    def update(self, entity):
        # Updates an existing entity
        pass

    @abstractmethod
    def find_by_id(self, entity_id):
        # Returns the entity or None
        pass

    @abstractmethod
    def get_all(self):
        # Returns a list of everything
        pass

    @abstractmethod
    def size(self):
        # Returns how many items we have
        pass