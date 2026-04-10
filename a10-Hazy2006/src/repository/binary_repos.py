import pickle
import os
from src.repository.base_repos import Repository, GradeRepository

class BinaryFileRepository(Repository):
    def __init__(self, file_path):
        super().__init__()
        self._file_path = file_path
        self._load_file()

    def _load_file(self):
        if not os.path.exists(self._file_path) or os.path.getsize(self._file_path) == 0:
            return
        with open(self._file_path, 'rb') as f:
            try:
                self._data = pickle.load(f)
                # Ensure it loaded a dictionary, otherwise reset
                if not isinstance(self._data, dict):
                    self._data = {}
            except Exception:
                self._data = {}

    def _save_file(self):
        with open(self._file_path, 'wb') as f:
            pickle.dump(self._data, f)

    def add(self, entity):
        super().add(entity)
        self._save_file()

    def remove(self, entity_id):
        super().remove(entity_id)
        self._save_file()

    def update(self, entity):
        super().update(entity)
        self._save_file()


class BinaryGradeRepository(GradeRepository):
    def __init__(self, file_path):
        super().__init__()
        self._file_path = file_path
        self._load_file()

    def _load_file(self):
        if not os.path.exists(self._file_path) or os.path.getsize(self._file_path) == 0:
            return
        with open(self._file_path, 'rb') as f:
            try:
                data = pickle.load(f)
                # Ensure it loaded a list, otherwise reset
                self._data = data if isinstance(data, list) else []
            except Exception:
                self._data = []

    def _save_file(self):
        with open(self._file_path, 'wb') as f:
            pickle.dump(self._data, f)

    def add(self, grade):
        super().add(grade)
        self._save_file()

    def remove_by_student(self, student_id):
        super().remove_by_student(student_id)
        self._save_file()

    def remove_by_discipline(self, discipline_id):
        super().remove_by_discipline(discipline_id)
        self._save_file()
