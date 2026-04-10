from src.domain.student import Student
from src.domain.discipline import Discipline
from src.domain.grade import Grade
from src.repository.text_repos import TextFileRepository, TextFileGradeRepository
from src.services.student_service import StudentService
from src.services.discipline_service import DisciplineService
from src.services.grade_service import GradeService
from src.services.undo_redo_service import UndoRedoService
from src.ui.console import ConsoleUI

# --- Serialization Helpers ---
# These convert objects to text and back
def student_to_line(s):
    return f"{s.student_id},{s.name}"

def student_from_line(line):
    parts = line.split(',')
    return Student(parts[0].strip(), parts[1].strip())

def discipline_to_line(d):
    return f"{d.discipline_id},{d.name}"

def discipline_from_line(line):
    parts = line.split(',')
    return Discipline(parts[0].strip(), parts[1].strip())

def grade_to_line(g):
    return f"{g.student_id},{g.discipline_id},{g.grade_value}"

def grade_from_line(line):
    parts = line.split(',')
    return Grade(parts[0].strip(), parts[1].strip(), float(parts[2].strip()))

if __name__ == "__main__":
    # 1. Initialize Repositories (FILE BASED)
    # This ensures data is saved to .txt files
    student_repo = TextFileRepository("students.txt", student_from_line, student_to_line)
    disc_repo = TextFileRepository("disciplines.txt", discipline_from_line, discipline_to_line)
    grade_repo = TextFileGradeRepository("grades.txt", grade_from_line, grade_to_line)

    # 2. Initialize Undo Service
    undo_srv = UndoRedoService()

    # 3. Initialize Services
    student_srv = StudentService(student_repo, grade_repo, undo_srv)
    disc_srv = DisciplineService(disc_repo, grade_repo, undo_srv)
    grade_srv = GradeService(grade_repo, student_repo, disc_repo, undo_srv)

    # 4. Start UI
    ui = ConsoleUI(student_srv, disc_srv, grade_srv, undo_srv)
    ui.run()