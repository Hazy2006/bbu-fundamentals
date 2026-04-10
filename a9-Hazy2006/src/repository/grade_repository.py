from src.repository.memory_repository import InMemoryRepository
from src.repository.text_repository import TextFileRepository
from src.repository.binary_repository import BinaryFileRepository
from src.domain.grade import Grade


class GradeMemoryRepository(InMemoryRepository):
    def __init__(self):
        # Grade ID is a tuple of (student_id, discipline_id)
        super().__init__(lambda g: (g.student_id, g.discipline_id))


class GradeTextRepository(TextFileRepository):
    def __init__(self, filename):
        def grade_to_line(g):
            return f"{g.student_id};{g.discipline_id};{g.grade_value}"

        def line_to_grade(line):
            parts = line.split(';')
            s_id = parts[0].strip()
            d_id = parts[1].strip()
            val = float(parts[2].strip())
            return Grade(s_id, d_id, val)

        super().__init__(
            filename,
            lambda g: (g.student_id, g.discipline_id),
            grade_to_line,
            line_to_grade
        )


class GradeBinaryRepository(BinaryFileRepository):
    def __init__(self, filename):
        super().__init__(filename, lambda g: (g.student_id, g.discipline_id))