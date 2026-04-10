class UI:
    def __init__(self, service):
        self._service = service

    def print_menu(self):
        print("\n--- Expense Manager ---")
        print("1. Add Expense")
        print("2. Display Expenses")
        print("3. Filter Expenses (Keep only > value)")
        print("4. Undo")
        print("0. Exit")

    def add_ui(self):
        try:
            day = int(input("Enter day (1-30): ").strip())
            amount = int(input("Enter amount (>0): ").strip())
            exp_type = input("Enter type: ").strip()
            self._service.add_expense(day, amount, exp_type)
            print("Expense added successfully.")
        except ValueError as ve:
            print(f"Error: {ve}")

    def display_ui(self):
        expenses = self._service.get_expenses()
        if not expenses:
            print("No expenses found.")
            return
        for ex in expenses:
            print(ex)

    def filter_ui(self):
        try:
            limit = int(input("Enter value to filter by (keep items > this): ").strip())
            self._service.filter_expenses(limit)
            print("Filter applied. Expenses <= " + str(limit) + " removed.")
        except ValueError as ve:
            print(f"Error: {ve}")

    def undo_ui(self):
        try:
            self._service.undo()
            print("Last operation undone.")
        except ValueError as e:
            print(e)

    def start(self):
        while True:
            self.print_menu()
            cmd = input("Enter your option: ").strip()
            if cmd == "1":
                self.add_ui()
            elif cmd == "2":
                self.display_ui()
            elif cmd == "3":
                self.filter_ui()
            elif cmd == "4":
                self.undo_ui()
            elif cmd == "0":
                break
            else:
                print("Invalid command.")