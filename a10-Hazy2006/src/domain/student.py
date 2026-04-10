# This file defines a Student class with attributes for student ID and name.
# It includes methods for string representation and equality checking of Student objects.

class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name

    def __str__(self):
        return f"ID: {self.student_id} | Name: {self.name}"

    # Equality check is useful for testing
    def __eq__(self, other):
        return isinstance(other, Student) and self.student_id == other.student_id
