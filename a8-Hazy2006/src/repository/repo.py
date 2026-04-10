import pickle
import os
from src.domain.entity import Expense

# Memory-only repository: keeps data in a Python list.
class MemoryRepository:
    """In-memory repository. Persists only for the life of the process."""
    def __init__(self):
        # internal storage for entities
        self._data = []

    def add(self, entity):
        # Add an entity object to the in-memory list.
        self._data.append(entity)
        self._save()

    def get_all(self):
        # Return the internal list. Callers should avoid mutating it directly.
        return self._data

    def set_all(self, new_data):
        # Replace the entire in-memory collection.
        # Expects an iterable/list of Expense objects.
        self._data = new_data
        self._save()

    def _save(self):
        pass

class TextFileRepository(MemoryRepository):
    """Text file-backed repository. Persists the list to a text file."""
    def __init__(self, file_name="expenses.txt"):
        # Initialize memory storage and keep filename for persistence.
        super().__init__()
        self._file_name = file_name
        # Load existing data from text file (if present).
        self._load()

    def _save(self):
        # Persist current in-memory list to text file
        with open(self._file_name, 'w') as f:
            for expense in self._data:
                f.write(expense.to_line() + '\n')

    def _load(self):
        # Load expenses from text file into memory.
        if not os.path.exists(self._file_name):
            # No file -> nothing to load
            return

        # Read all lines and convert them to Expense objects.
        with open(self._file_name, 'r') as f:
            lines = f.readlines()
            self._data = []
            for line in lines:
                line = line.strip()
                if line != "":
                    # Convert text line back to object using the domain parser.
                    # Expense.from_line is responsible for validating and parsing.
                    self._data.append(Expense.from_line(line))

class BinaryFileRepository(MemoryRepository):
    """Pickle-backed repository. Serializes the Python list to a binary file."""
    def __init__(self, file_name="expenses.pickle"):
        super().__init__()
        self._file_name = file_name
        # Load binary data (if exists) into memory
        self._load()

    def _save(self):
        # Write the entire list to a binary file using pickle.
        # This overwrites the file on each call.
        with open(self._file_name, 'wb') as f:
            pickle.dump(self._data, f)

    def _load(self):
        # Load data from pickle file if file exists and is non-empty.
        if os.path.exists(self._file_name) and os.path.getsize(self._file_name) > 0:
            with open(self._file_name, 'rb') as f:
                self._data = pickle.load(f)