# Console UI for Student Register

from src.domain.exceptions import (
    ValidationException, DuplicateException, NotFoundException
)


class ConsoleUI:

    def __init__(self, student_service, discipline_service, grade_service):
        # init: stash the services
        self._student_service = student_service
        self._discipline_service = discipline_service
        self._grade_service = grade_service

    def run(self):
        # main loop: keep asking the user until they pick exit
        while True:
            self._print_main_menu()
            choice = input("Enter choice: ").strip()

            if choice == '1':
                self._student_menu()
            elif choice == '2':
                self._discipline_menu()
            elif choice == '3':
                self._grade_menu()
            elif choice == '0':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def _print_main_menu(self):
        # main menu: student/discipline/grade/exit
        print("\n" + "=" * 50)
        print("STUDENT REGISTER - MAIN MENU")
        print("=" * 50)
        print("1. Student Management")
        print("2. Discipline Management")
        print("3. Grade Management")
        print("0. Exit")
        print("=" * 50)

    def _student_menu(self):
        # student menu: add/remove/update/list/search/view
        while True:
            print("\n" + "-" * 50)
            print("STUDENT MANAGEMENT")
            print("-" * 50)
            print("1. Add Student")
            print("2. Remove Student")
            print("3. Update Student")
            print("4. List All Students")
            print("5. Search Students")
            print("6. View Student Details")
            print("0. Back to Main Menu")
            print("-" * 50)

            choice = input("Enter choice: ").strip()

            if choice == '1':
                self._add_student()
            elif choice == '2':
                self._remove_student()
            elif choice == '3':
                self._update_student()
            elif choice == '4':
                self._list_students()
            elif choice == '5':
                self._search_students()
            elif choice == '6':
                self._view_student_details()
            elif choice == '0':
                break
            else:
                print("Invalid choice. Please try again.")

    def _discipline_menu(self):
        # discipline menu: add/remove/update/list/search
        while True:
            print("\n" + "-" * 50)
            print("DISCIPLINE MANAGEMENT")
            print("-" * 50)
            print("1. Add Discipline")
            print("2. Remove Discipline")
            print("3. Update Discipline")
            print("4. List All Disciplines")
            print("5. Search Disciplines")
            print("0. Back to Main Menu")
            print("-" * 50)

            choice = input("Enter choice: ").strip()

            if choice == '1':
                self._add_discipline()
            elif choice == '2':
                self._remove_discipline()
            elif choice == '3':
                self._update_discipline()
            elif choice == '4':
                self._list_disciplines()
            elif choice == '5':
                self._search_disciplines()
            elif choice == '0':
                break
            else:
                print("Invalid choice. Please try again.")

    def _grade_menu(self):
        # grade menu: add/update/remove/list/view-by-student/view-by-discipline
        while True:
            print("\n" + "-" * 50)
            print("GRADE MANAGEMENT")
            print("-" * 50)
            print("1. Add Grade")
            print("2. Update Grade")
            print("3. Remove Grade")
            print("4. List All Grades")
            print("5. View Grades for Student")
            print("6. View Grades for Discipline")
            print("0. Back to Main Menu")
            print("-" * 50)

            choice = input("Enter choice: ").strip()

            if choice == '1':
                self._add_grade()
            elif choice == '2':
                self._update_grade()
            elif choice == '3':
                self._remove_grade()
            elif choice == '4':
                self._list_grades()
            elif choice == '5':
                self._view_student_grades()
            elif choice == '6':
                self._view_discipline_grades()
            elif choice == '0':
                break
            else:
                print("Invalid choice. Please try again.")

    # Student operations
    def _add_student(self):
        # add student: ask id and name, call service
        try:
            student_id = input("Enter student ID: ").strip()
            name = input("Enter student name: ").strip()
            student = self._student_service.add_student(student_id, name)
            print(f"Student added successfully: {student}")
        except (ValidationException, DuplicateException) as e:
            print(f"Error: {e}")

    def _remove_student(self):
        # remove student by id
        try:
            student_id = input("Enter student ID: ").strip()
            self._student_service.remove_student(student_id)
            print(f"Student {student_id} and associated grades removed successfully")
        except NotFoundException as e:
            print(f"Error: {e}")

    def _update_student(self):
        # update student name by id
        try:
            student_id = input("Enter student ID: ").strip()
            name = input("Enter new name: ").strip()
            student = self._student_service.update_student(student_id, name)
            print(f"Student updated successfully: {student}")
        except (ValidationException, NotFoundException) as e:
            print(f"Error: {e}")

    def _list_students(self):
        # list all students, sorted by id
        students = self._student_service.get_all_students()
        if not students:
            print("No students found.")
        else:
            print(f"\nTotal students: {len(students)}")
            for student in sorted(students, key=lambda s: s.student_id):
                print(f"  {student}")

    def _search_students(self):
        # search students by id or name
        search_term = input("Enter search term (ID or name): ").strip()
        students = self._student_service.search_students(search_term)
        if not students:
            print("No students found.")
        else:
            print(f"\nFound {len(students)} student(s):")
            for student in sorted(students, key=lambda s: s.student_id):
                print(f"  {student}")

    def _view_student_details(self):
        # show a student's details and their grades
        try:
            student_id = input("Enter student ID: ").strip()
            student = self._student_service.find_student(student_id)
            if not student:
                print(f"Student with ID {student_id} not found.")
                return

            print(f"\n{student}")
            grades = self._grade_service.get_grades_for_student(student_id)
            if grades:
                print("Grades:")
                for grade in grades:
                    discipline = self._discipline_service.find_discipline(grade.discipline_id)
                    disc_name = discipline.name if discipline else "Unknown"
                    print(f"  {grade.discipline_id} - {disc_name}: {grade.grade_value}")
            else:
                print("No grades recorded.")
        except Exception as e:
            print(f"Error: {e}")

    # Discipline operations
    def _add_discipline(self):
        # add discipline: ask id and name
        try:
            discipline_id = input("Enter discipline ID: ").strip()
            name = input("Enter discipline name: ").strip()
            discipline = self._discipline_service.add_discipline(discipline_id, name)
            print(f"Discipline added successfully: {discipline}")
        except (ValidationException, DuplicateException) as e:
            print(f"Error: {e}")

    def _remove_discipline(self):
        # remove discipline by id
        try:
            discipline_id = input("Enter discipline ID: ").strip()
            self._discipline_service.remove_discipline(discipline_id)
            print(f"Discipline {discipline_id} and associated grades removed successfully")
        except NotFoundException as e:
            print(f"Error: {e}")

    def _update_discipline(self):
        # update discipline name by id
        try:
            discipline_id = input("Enter discipline ID: ").strip()
            name = input("Enter new name: ").strip()
            discipline = self._discipline_service.update_discipline(discipline_id, name)
            print(f"Discipline updated successfully: {discipline}")
        except (ValidationException, NotFoundException) as e:
            print(f"Error: {e}")

    def _list_disciplines(self):
        # list all disciplines
        disciplines = self._discipline_service.get_all_disciplines()
        if not disciplines:
            print("No disciplines found.")
        else:
            print(f"\nTotal disciplines: {len(disciplines)}")
            for discipline in sorted(disciplines, key=lambda d: d.discipline_id):
                print(f"  {discipline}")

    def _search_disciplines(self):
        # search disciplines by id or name
        search_term = input("Enter search term (ID or name): ").strip()
        disciplines = self._discipline_service.search_disciplines(search_term)
        if not disciplines:
            print("No disciplines found.")
        else:
            print(f"\nFound {len(disciplines)} discipline(s):")
            for discipline in sorted(disciplines, key=lambda d: d.discipline_id):
                print(f"  {discipline}")

    # Grade operations
    def _add_grade(self):
        # add grade: ask student id, discipline id, and grade value
        try:
            student_id = input("Enter student ID: ").strip()
            discipline_id = input("Enter discipline ID: ").strip()
            grade_value = input("Enter grade value (0-10): ").strip()
            grade = self._grade_service.add_grade(student_id, discipline_id, grade_value)
            print(f"Grade added successfully: {grade}")
        except (ValidationException, DuplicateException) as e:
            print(f"Error: {e}")

    def _update_grade(self):
        # update grade value for a student+discipline
        try:
            student_id = input("Enter student ID: ").strip()
            discipline_id = input("Enter discipline ID: ").strip()
            grade_value = input("Enter new grade value (0-10): ").strip()
            grade = self._grade_service.update_grade(student_id, discipline_id, grade_value)
            print(f"Grade updated successfully: {grade}")
        except (ValidationException, NotFoundException) as e:
            print(f"Error: {e}")

    def _remove_grade(self):
        # remove a specific grade
        try:
            student_id = input("Enter student ID: ").strip()
            discipline_id = input("Enter discipline ID: ").strip()
            self._grade_service.remove_grade(student_id, discipline_id)
            print(f"Grade removed successfully")
        except NotFoundException as e:
            print(f"Error: {e}")

    def _list_grades(self):
        # list all grades in a nice table-ish form
        grades = self._grade_service.get_all_grades()
        if not grades:
            print("No grades found.")
        else:
            print(f"\nTotal grades: {len(grades)}\n")

            # 1. Print the Header with fixed widths
            # <35 means "align left, reserve 35 spaces"
            print(f"{'Student':<35} | {'Discipline':<25} | {'Grade':<5}")
            print("-" * 75)  # A separator line

            # 2. Print the Rows
            for grade in grades:
                student = self._student_service.find_student(grade.student_id)
                discipline = self._discipline_service.find_discipline(grade.discipline_id)

                student_name = student.name if student else "Unknown"
                disc_name = discipline.name if discipline else "Unknown"

                # Create the strings first so we can format them into columns
                student_str = f"{grade.student_id} ({student_name})"
                disc_str = f"{grade.discipline_id} ({disc_name})"

                # Print the row aligning with the header
                # :>5.2f means "align right, 5 spaces total, 2 decimal places"
                print(f"{student_str:<35} | {disc_str:<25} | {grade.grade_value:>5.2f}")

    def _view_student_grades(self):
        # view grades for one student
        student_id = input("Enter student ID: ").strip()
        student = self._student_service.find_student(student_id)
        if not student:
            print(f"Student with ID {student_id} not found.")
            return

        grades = self._grade_service.get_grades_for_student(student_id)
        if not grades:
            print(f"No grades found for student {student_id}.")
        else:
            print(f"\nGrades for {student.name} ({student_id}):")
            for grade in grades:
                discipline = self._discipline_service.find_discipline(grade.discipline_id)
                disc_name = discipline.name if discipline else "Unknown"
                print(f"  {grade.discipline_id} - {disc_name}: {grade.grade_value}")

    def _view_discipline_grades(self):
        # view grades for one discipline
        discipline_id = input("Enter discipline ID: ").strip()
        discipline = self._discipline_service.find_discipline(discipline_id)
        if not discipline:
            print(f"Discipline with ID {discipline_id} not found.")
            return

        grades = self._grade_service.get_grades_for_discipline(discipline_id)
        if not grades:
            print(f"No grades found for discipline {discipline_id}.")
        else:
            print(f"\nGrades for {discipline.name} ({discipline_id}):")
            for grade in grades:
                student = self._student_service.find_student(grade.student_id)
                student_name = student.name if student else "Unknown"
                print(f"  {grade.student_id} - {student_name}: {grade.grade_value}")
