from src.repository.memory_repository import InMemoryRepository
from src.repository.text_repository import TextFileRepository
from src.repository.binary_repository import BinaryFileRepository
from src.domain.student import Student


class StudentMemoryRepository(InMemoryRepository):
    # In-memory storage for students
    def __init__(self):
        super().__init__(lambda s: s.student_id)


class StudentTextRepository(TextFileRepository):
    def __init__(self, filename):
        # We define simple helper functions instead of complex lambdas
        def student_to_line(s):
            return f"{s.student_id};{s.name}"

        def line_to_student(line):
            parts = line.split(';')
            # clean up the data
            student_id = parts[0].strip()
            name = parts[1].strip()
            return Student(student_id, name)

        super().__init__(
            filename,
            lambda s: s.student_id,
            student_to_line,
            line_to_student
        )


class StudentBinaryRepository(BinaryFileRepository):
    def __init__(self, filename):
        super().__init__(filename, lambda s: s.student_id)