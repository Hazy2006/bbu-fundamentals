"""Main application entry point."""

from src.repository.repository_factory import create_repositories
from src.service.student_service import StudentService
from src.service.discipline_service import DisciplineService
from src.service.grade_service import GradeService
from src.service.data_populator import populate_data
from src.ui.console_ui import ConsoleUI


def main():
    # 1. Create repositories (loads settings automatically)
    student_repo, discipline_repo, grade_repo = create_repositories()

    # 2. Create services
    # Note: GradeService needs student and discipline repos to check if IDs exist
    student_service = StudentService(student_repo, grade_repo)
    discipline_service = DisciplineService(discipline_repo, grade_repo)

    grade_service = GradeService(student_repo, discipline_repo, grade_repo)

    # 3. Populate data if empty (only for the first run)
    if student_repo.size() == 0:
        print("Repo is empty. Generating fake data...")
        try:
            populate_data(student_service, discipline_service, grade_service, count=20)
            print("Done generating data.")
        except Exception as e:
            print(f"Warning: Could not populate data: {e}")

    # 4. Start the UI
    ui = ConsoleUI(student_service, discipline_service, grade_service)
    ui.run()


if __name__ == "__main__":
    main()