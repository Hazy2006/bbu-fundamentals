class Expense:
    def __init__(self, day, amount, expense_type):
        self.day = day
        self.amount = amount
        self.expense_type = expense_type

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, value):
        # ensure integer and in range
        try:
            value = int(value)
        except (TypeError, ValueError):
            raise ValueError("Day must be an integer between 1 and 30.")
        if not (1 <= value <= 30):
            raise ValueError("Day must be between 1 and 30.")
        self._day = value

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        # ensure integer and positive
        try:
            value = int(value)
        except (TypeError, ValueError):
            raise ValueError("Amount must be a positive integer.")
        if value <= 0:
            raise ValueError("Amount must be a positive integer.")
        self._amount = value

    @property
    def expense_type(self):
        return self._expense_type

    @expense_type.setter
    def expense_type(self, value):
        if not isinstance(value, str):
            raise ValueError("Type must be a string.")
        value = value.strip()
        if not value:
            raise ValueError("Type must be a non-empty string.")
        self._expense_type = value

    def __str__(self):
        return f"Day: {self.day:<3} | Amount: {self.amount:<5} | Type: {self.expense_type}"

    def __eq__(self, other):
        """Helper for testing equality."""
        if not isinstance(other, Expense):
            return False
        return (self.day == other.day and
                self.amount == other.amount and
                self.expense_type == other.expense_type)


    def to_line(self):
        """Converts expense to a CSV string."""
        # escape commas in type if needed (simple approach)
        typ = self.expense_type.replace('\n', ' ').replace('\r', ' ')
        return f"{self.day},{self.amount},{typ}"

    @staticmethod
    def from_line(line):
        """Creates expense from a CSV string. Raises ValueError on malformed lines."""
        if not isinstance(line, str):
            raise ValueError("Line must be a string.")
        parts = [p.strip() for p in line.strip().split(',')]
        if len(parts) < 3:
            raise ValueError(f"Malformed line for Expense: {line!r}")
        # allow extra commas in type by joining remaining parts
        try:
            day = int(parts[0])
            amount = int(parts[1])
            typ = ",".join(parts[2:]).strip()
            return Expense(day, amount, typ)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid values in line: {line!r}") from e


    def to_dict(self):
        """Converts expense to a dictionary."""
        return {"day": self.day, "amount": self.amount, "type": self.expense_type}

    @staticmethod
    def from_dict(data):
        """Creates expense from a dictionary. Raises ValueError on malformed input."""
        if not isinstance(data, dict):
            raise ValueError("Expected a dict to create Expense.")

        try:
            day = data.get("day") if "day" in data else data.get("Day")
            amount = data.get("amount") if "amount" in data else data.get("Amount")
            typ = data.get("type") if "type" in data else data.get("Type", "")
            return Expense(day, amount, typ)
        except (TypeError, ValueError) as e:
            raise ValueError("Invalid dict for Expense.") from e
