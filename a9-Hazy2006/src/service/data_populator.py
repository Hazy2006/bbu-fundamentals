"""Data populator using Faker."""
from faker import Faker
import random


def populate_data(student_service, discipline_service, grade_service, count=20):
    """
    Populate repositories with fake data.
    """
    fake = Faker()

    # 1. Generate Students
    student_ids = []
    print(f"Generating {count} students...")
    while len(student_ids) < count:
        # Use a string ID like '101', '102'
        s_id = str(random.randint(100, 9999))
        name = fake.name()
        try:
            student_service.add_student(s_id, name)
            student_ids.append(s_id)
        except Exception:
            # Duplicate ID, skip and try again
            pass

    # 2. Generate Disciplines
    discipline_names = [
        "Mathematics", "Computer Science", "Physics", "Chemistry", "Biology",
        "Literature", "History", "Geography", "Philosophy", "Psychology",
        "Economics", "Sociology", "Political Science", "Art", "Music",
        "Physical Education", "Foreign Languages", "Engineering", "Medicine", "Law"
    ]

    discipline_ids = []
    print(f"Generating {count} disciplines...")
    for i in range(count):
        d_id = str(random.randint(100, 9999))
        # Pick a name from the list or generate a random word if we run out
        if i < len(discipline_names):
            name = discipline_names[i]
        else:
            name = f"{fake.word().capitalize()} {i}"

        try:
            discipline_service.add_discipline(d_id, name)
            discipline_ids.append(d_id)
        except Exception:
            pass

    # 3. Generate Grades
    print("Assigning grades...")
    # Make sure we have enough data to link
    if not student_ids or not discipline_ids:
        return

    for _ in range(count * 2):  # Generate plenty of grades
        s_id = random.choice(student_ids)
        d_id = random.choice(discipline_ids)
        grade_value = round(random.uniform(1.0, 10.0), 2)
        try:
            grade_service.add_grade(s_id, d_id, grade_value)
        except Exception:
            pass