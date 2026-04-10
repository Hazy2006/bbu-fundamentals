import unittest
import copy

from domain.entity import Expense
from repository.repo import MemoryRepository
from services.service import Service


class TestExpenseManager(unittest.TestCase):
    """
    Unit tests and specifications for non-UI functions (Domain and Service).
    """

    def setUp(self):
        """
        Setup runs before every single test method.
        It initializes a clean in-memory environment for isolation.
        """
        self.repo = MemoryRepository()
        self.service = Service(self.repo)

        # Clear the initial 10 generated items for clean testing
        self.repo.set_all([])
        self.service._undo_stack = []  # Ensure undo stack is also clean


    def test_domain_create_valid_expense(self):
        """Test successful creation of an Expense object."""
        e = Expense(day=15, amount=250, expense_type="Groceries")
        self.assertEqual(e.day, 15)
        self.assertEqual(e.amount, 250)
        self.assertEqual(e.expense_type, "Groceries")

    def test_domain_validation_day(self):
        """Test that invalid day values raise ValueError."""
        with self.assertRaises(ValueError):
            Expense(35, 100, "Food")  # Day too high
        with self.assertRaises(ValueError):
            Expense(0, 100, "Food")  # Day too low

    def test_domain_validation_amount(self):
        """Test that invalid amount values raise ValueError."""
        with self.assertRaises(ValueError):
            Expense(1, -50, "Food")  # Amount negative
        with self.assertRaises(ValueError):
            Expense(1, 0, "Food")  # Amount zero


    def test_add_expense_type_errors(self):
        """
        Test that passing incorrect data types for day or amount raises
        a TypeError because integer comparisons cannot be performed.
        """
        initial_count = len(self.service.get_expenses())

        # Test case 1: String passed for Day (should raise TypeError in Expense setter)
        with self.assertRaises(TypeError):
            self.service.add_expense(day="15", amount=50, exp_type="WrongType")

        # Test case 2: String passed for Amount (should raise TypeError in Expense setter)
        with self.assertRaises(TypeError):
            self.service.add_expense(day=15, amount="50", exp_type="WrongType")

        # Ensure no expense was actually added after the failed attempts
        self.assertEqual(len(self.service.get_expenses()), initial_count,
                         "List should remain unchanged after failed addition.")

    def test_add_expense_functionality(self):
        """
        Test adding an expense successfully increments the list count
        and verifies the added content.
        """
        initial_count = len(self.service.get_expenses())
        self.service.add_expense(day=5, amount=50, exp_type="TestAdd")

        all_items = self.service.get_expenses()
        self.assertEqual(len(all_items), initial_count + 1, "List count should increase by 1.")

        # Verify the last added item
        self.assertEqual(all_items[-1].day, 5)
        self.assertEqual(all_items[-1].amount, 50)
        self.assertEqual(all_items[-1].expense_type, "TestAdd")

    def test_undo_after_add_restores_state(self):
        """
        Test that calling undo() immediately after add_expense()
        reverts the list to its previous state.
        """
        # Step 1: Establish initial state
        self.service.add_expense(day=1, amount=10, exp_type="Before")
        initial_list_snapshot = copy.deepcopy(self.service.get_expenses())
        self.assertEqual(len(initial_list_snapshot), 1)

        # Step 2: Perform action that will be undone
        self.service.add_expense(day=2, amount=20, exp_type="ToUndo")
        self.assertEqual(len(self.service.get_expenses()), 2)

        # Step 3: Undo the last action
        self.service.undo()

        # Step 4: Verify state is restored (size and content)
        final_list = self.service.get_expenses()
        self.assertEqual(len(final_list), 1)
        self.assertEqual(final_list[0].expense_type, "Before")


    def test_filter_expenses(self):
        """Test filtering correctly removes expenses below the threshold."""
        self.service.add_expense(1, 100, "Keep_High")
        self.service.add_expense(2, 40, "Remove_Low")
        self.service.add_expense(3, 200, "Keep_VeryHigh")

        self.service.filter_expenses(min_amount=50)  # Keep only > 50

        remaining = self.service.get_expenses()
        self.assertEqual(len(remaining), 2)
        # Check that the two items remaining are the correct ones
        self.assertIn(Expense(1, 100, "Keep_High"), remaining)
        self.assertIn(Expense(3, 200, "Keep_VeryHigh"), remaining)
        self.assertNotIn(Expense(2, 40, "Remove_Low"), remaining)

    def test_undo_multiple_times(self):
        """Test sequence of three actions followed by three undos."""
        self.service.add_expense(1, 10, "A")

        # Action 1 (Add B)
        self.service.add_expense(2, 20, "B")
        self.assertEqual(len(self.service.get_expenses()), 2)

        # Action 2 (Filter)
        self.service.filter_expenses(15)  # Only 'B' remains
        self.assertEqual(len(self.service.get_expenses()), 1)

        # Undo 1: Reverts Filter -> List should be [A, B]
        self.service.undo()
        self.assertEqual(len(self.service.get_expenses()), 2)

        # Undo 2: Reverts Add B -> List should be [A]
        self.service.undo()
        self.assertEqual(len(self.service.get_expenses()), 1)
        self.assertEqual(self.service.get_expenses()[0].expense_type, "A")

        # Undo 3: Reverts Add A -> List should be []
        self.service.undo()
        self.assertEqual(len(self.service.get_expenses()), 0)

        # Test nothing left to undo
        with self.assertRaises(ValueError):
            self.service.undo()