from src.repository.base_repos import Repository, GradeRepository


class TextFileRepository(Repository):
    def __init__(self, file_path, entity_from_line, entity_to_line):
        super().__init__()
        self._file_path = file_path
        self._entity_from_line = entity_from_line
        self._entity_to_line = entity_to_line
        self._load_from_file()

    def _load_from_file(self):
        try:
            with open(self._file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if len(line) > 0:
                        entity = self._entity_from_line(line)
                        super().add(entity)
        except FileNotFoundError:
            pass  # File doesn't exist yet, that's fine

    def _save_to_file(self):
        with open(self._file_path, 'w') as f:
            # FIX: Use get_all() instead of _objects to be safe
            for entity in self.get_all():
                line = self._entity_to_line(entity)
                f.write(line + '\n')

    def add(self, entity):
        super().add(entity)
        self._save_to_file()

    def remove(self, entity_id):
        obj = super().remove(entity_id)
        self._save_to_file()
        return obj

    def update(self, entity):
        super().update(entity)
        self._save_to_file()


class TextFileGradeRepository(GradeRepository):
    def __init__(self, file_path, entity_from_line, entity_to_line):
        super().__init__()
        self._file_path = file_path
        self._entity_from_line = entity_from_line
        self._entity_to_line = entity_to_line
        self._load_from_file()

    def _load_from_file(self):
        try:
            with open(self._file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if len(line) > 0:
                        entity = self._entity_from_line(line)
                        super().add(entity)
        except FileNotFoundError:
            pass

    def _save_to_file(self):
        with open(self._file_path, 'w') as f:
            # FIX: Use get_all() instead of _objects or _grades
            for entity in self.get_all():
                line = self._entity_to_line(entity)
                f.write(line + '\n')

    def add(self, entity):
        super().add(entity)
        self._save_to_file()

    def remove(self, entity):
        super().remove(entity)
        self._save_to_file()

    def remove_by_discipline(self, d_id):
        # Check if base repo supports this, otherwise we rely on get_all loop in service
        if hasattr(super(), 'remove_by_discipline'):
            super().remove_by_discipline(d_id)
            self._save_to_file()