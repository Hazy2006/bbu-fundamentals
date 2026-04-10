from src.repository.student_repository import (
    StudentMemoryRepository, StudentTextRepository, StudentBinaryRepository
)
from src.repository.discipline_repository import (
    DisciplineMemoryRepository, DisciplineTextRepository, DisciplineBinaryRepository
)
from src.repository.grade_repository import (
    GradeMemoryRepository, GradeTextRepository, GradeBinaryRepository
)


def load_settings():
    # Simple manual file reading that works with standard .properties format
    settings = {}
    try:
        with open('settings.properties', 'r') as f:
            for line in f:
                line = line.strip()
                # skip comments or empty lines
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    # remove quotes and whitespace
                    settings[key.strip()] = value.strip().strip('"')
    except FileNotFoundError:
        # Fallback if file is missing
        settings['repository'] = 'memory'
    return settings


def create_repositories():
    settings = load_settings()
    repo_type = settings.get('repository', 'memory')

    if repo_type == 'textfiles':
        # Get filenames from settings (defaulting to standard names if missing)
        s_file = settings.get('students', 'students.txt')
        d_file = settings.get('disciplines', 'disciplines.txt')
        g_file = settings.get('grades', 'grades.txt')

        return (
            StudentTextRepository(s_file),
            DisciplineTextRepository(d_file),
            GradeTextRepository(g_file)
        )

    elif repo_type == 'binaryfiles':
        s_file = settings.get('students', 'students.bin')
        d_file = settings.get('disciplines', 'disciplines.bin')
        g_file = settings.get('grades', 'grades.bin')

        return (
            StudentBinaryRepository(s_file),
            DisciplineBinaryRepository(d_file),
            GradeBinaryRepository(g_file)
        )

    else:
        # In-memory requires no filenames
        return (
            StudentMemoryRepository(),
            DisciplineMemoryRepository(),
            GradeMemoryRepository()
        )