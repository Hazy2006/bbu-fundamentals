class Discipline:
    def __init__(self, discipline_id, name):
        self.discipline_id = discipline_id
        self.name = name

    def __str__(self):
        return f"{self.discipline_id} - {self.name}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, Discipline):
            return False
        return self.discipline_id == other.discipline_id
