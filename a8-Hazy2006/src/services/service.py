import copy
from src.domain.entity import Expense


class Service:
    def __init__(self, repository):
        self._repo = repository
        self._undo_stack = []  # Stack of repository snapshots for undo functionality
        # Generate 10 default expenses only if repository is empty (avoids duplicates on restart)
        if len(self._repo.get_all()) == 0:
            self._generate_defaults()
    def _generate_defaults(self):
        defaults = [
            (1, 100, "Food"), (2, 50, "Transport"), (5, 200, "Clothes"),
            (10, 15, "Coffee"), (12, 500, "Rent"), (15, 30, "Internet"),
            (20, 100, "Food"), (21, 60, "Gas"), (25, 300, "Insurance"),
            (30, 45, "Gift")
        ]
        for day, amount, exp_type in defaults:
            self._repo.add(Expense(day, amount, exp_type))

    def add_expense(self, day, amount, exp_type):
        """Saves the expense list state before adding a new expense."""
        self._save_state()
        new_expense = Expense(day, amount, exp_type)
        self._repo.add(new_expense)


    def get_expenses(self):
        """Returns current list of all expenses (read-only view)."""
        return self._repo.get_all()

    def filter_expenses(self, min_amount):
        """
        Creates undo snapshot before filtering.
        """
        self._save_state()
        current_list = self._repo.get_all()
        filtered_list = [ex for ex in current_list if ex.amount > min_amount]
        self._repo.set_all(filtered_list)  # Replaces ALL data!

    def undo(self):
        """Restores repository to previous state. Raises ValueError if no history."""
        if not self._undo_stack:
            raise ValueError("Nothing to undo!")
        previous_state = self._undo_stack.pop()
        self._repo.set_all(previous_state)

    def _save_state(self):
        """
        Creates DEEP COPY of current repository state and pushes to undo stack.
        Ensures future mutations don't corrupt undo history.
        """
        self._undo_stack.append(copy.deepcopy(self._repo.get_all()))
