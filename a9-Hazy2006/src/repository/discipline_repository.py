from src.repository.memory_repository import InMemoryRepository
from src.repository.text_repository import TextFileRepository
from src.repository.binary_repository import BinaryFileRepository
from src.domain.discipline import Discipline


class DisciplineMemoryRepository(InMemoryRepository):
    def __init__(self):
        super().__init__(lambda d: d.discipline_id)


class DisciplineTextRepository(TextFileRepository):
    def __init__(self, filename):
        def discipline_to_line(d):
            return f"{d.discipline_id};{d.name}"

        def line_to_discipline(line):
            parts = line.split(';')
            d_id = parts[0].strip()
            name = parts[1].strip()
            return Discipline(d_id, name)

        super().__init__(
            filename,
            lambda d: d.discipline_id,
            discipline_to_line,
            line_to_discipline
        )


class DisciplineBinaryRepository(BinaryFileRepository):
    def __init__(self, filename):
        super().__init__(filename, lambda d: d.discipline_id)