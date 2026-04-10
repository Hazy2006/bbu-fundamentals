class Grade:
    def __init__(self, student_id, discipline_id, grade_value):
        self.student_id = student_id
        self.discipline_id = discipline_id
        self.grade_value = grade_value

    def __str__(self):
        return f"Student: {self.student_id} | Disc: {self.discipline_id} | Grade: {self.grade_value}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        # Simplified equality check
        return (isinstance(other, Grade) and
                self.student_id == other.student_id and
                self.discipline_id == other.discipline_id and
                self.grade_value == other.grade_value)
