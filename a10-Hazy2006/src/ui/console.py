from src.domain.validators import StoreException, ValidationException

class ConsoleUI:
    def __init__(self, student_srv, disc_srv, grade_srv, undo_srv):
        self.s_srv = student_srv
        self.d_srv = disc_srv
        self.g_srv = grade_srv
        self.undo_srv = undo_srv

    def run(self):
        # --- AUTO GENERATE IF EMPTY ---
        try:
            if len(self.s_srv.get_all()) == 0:
                self.s_srv.generate_random(10)
                self.d_srv.generate_random(10)
                self.g_srv.generate_random(30)
                # Only clear history on STARTUP generation
                if self.undo_srv: self.undo_srv.restart()
        except:
            pass

        while True:
            self.print_menu()
            cmd = input(">>> ").strip()
            try:
                if cmd == '0': break
                elif cmd == '1': self._handle_students()
                elif cmd == '2': self._handle_discs()
                elif cmd == '3': self._handle_grade()
                elif cmd == '4': self._list_all()
                elif cmd == '5': self._search()
                elif cmd == '6': self._handle_show_all()
                elif cmd == '7': self._failing_report()
                elif cmd == '8': self._top_students()
                elif cmd == '9': self._best_disciplines()
                elif cmd == '10':
                    if self.undo_srv:
                        msg = self.undo_srv.undo()
                        print(msg)
                    else: print("Service Unavailable.")
                elif cmd == '11':
                    if self.undo_srv:
                        msg = self.undo_srv.redo()
                        print(msg)
                    else: print("Service Unavailable.")
                elif cmd == '12':
                    self._force_grade_all()
                else: print("Invalid command.")
            except Exception as e:
                print(f"Error: {e}")

    def print_menu(self):
        print("\n=== ACADEMIC MENU ===")
        print("1. Manage Students")
        print("2. Manage Disciplines")
        print("3. Grade Student")
        print("4. List All")
        print("5. Search")
        print("6. Show Full Report")
        print("7. Failing Students")
        print("8. Top Students")
        print("9. Best Disciplines")
        print("10. Undo")
        print("11. Redo")
        print("12. FORCE GENERATE GRADES (Fix Empty Report)")
        print("0. Exit")

    def _handle_students(self):
        opt = input("Add (A) / Remove (R): ").upper()
        if opt == 'A':
            self.s_srv.add_student(input("ID: "), input("Name: "))
            print("Student added.")
        elif opt == 'R':
            val = input("Enter ID or Exact Name: ").strip()
            if not val: return
            try:
                self.s_srv.remove_student(val)
                print(f"Student ID {val} removed.")
                return
            except StoreException: pass

            matches = [s for s in self.s_srv.search(val) if s.name.lower() == val.lower()]
            if not matches: print("No student found.")
            elif len(matches) == 1:
                self.s_srv.remove_student(matches[0].student_id)
                print(f"Removed {matches[0].name}.")
            else:
                print(f"Found {len(matches)} named '{val}'. Use ID to remove:")
                for s in matches: print(f"- {s.name} (ID: {s.student_id})")

    def _handle_discs(self):
        opt = input("Add (A) / Remove (R): ").upper()
        if opt == 'A':
            self.d_srv.add_discipline(input("ID: "), input("Name: "))
            print("Added.")
        elif opt == 'R':
            val = input("ID: ")
            self.d_srv.remove_discipline(val)
            print("Removed.")

    def _handle_grade(self):
        self.g_srv.add_grade(input("Student ID: "), input("Disc ID: "), input("Value: "))
        print("Graded.")

    def _list_all(self):
        print("--- Students ---")
        for s in self.s_srv.get_all(): print(f"{s.student_id}: {s.name}")
        print("--- Disciplines ---")
        for d in self.d_srv.get_all(): print(f"{d.discipline_id}: {d.name}")

    def _search(self):
        q = input("Search Query: ")
        print("Results:")
        for s in self.s_srv.search(q): print(f"Student: {s}")
        for d in self.d_srv.search(q): print(f"Disc: {d}")

    def _handle_show_all(self):
        grades = self.g_srv.get_all()
        data = {}
        for g in grades:
            data.setdefault(str(g.student_id), {}).setdefault(str(g.discipline_id), []).append(g.grade_value)
        students = self.s_srv.get_all()
        discs = {str(d.discipline_id): d.name for d in self.d_srv.get_all()}
        print("\n--- FULL ACADEMIC REPORT ---")
        for s in students:
            sid = str(s.student_id)
            print(f"• {s.name} (ID: {sid})")
            if sid not in data:
                print("    - No grades recorded")
            else:
                for did, vals in data[sid].items():
                    dname = discs.get(did, "Unknown Subject")
                    g_str = ", ".join(str(v) for v in vals)
                    print(f"    - {dname:<15} : {g_str}")
            print("")

    def _failing_report(self):
        grades = self.g_srv.get_all()
        data = {}
        for g in grades:
            data.setdefault(str(g.student_id), {}).setdefault(str(g.discipline_id), []).append(g.grade_value)
        print("\n{:<20} | {:<20} | {:<10}".format("Student", "Subject", "Average"))
        print("-" * 55)
        found = False
        students = {str(s.student_id): s.name for s in self.s_srv.get_all()}
        discs = {str(d.discipline_id): d.name for d in self.d_srv.get_all()}
        for sid, d_map in data.items():
            for did, vals in d_map.items():
                avg = sum(vals) / len(vals)
                if avg < 5.0:
                    sname = students.get(sid, "Unknown")
                    dname = discs.get(did, "Unknown")
                    print("{:<20} | {:<20} | {:.2f}".format(sname, dname, avg))
                    found = True
        if not found: print("No failing students.")

    def _top_students(self):
        top = self.g_srv.get_top_students()
        if not top: print("No data available."); return
        print("\n{:<5} | {:<20} | {:<10}".format("Rank", "Name", "Average"))
        print("-" * 40)
        rank = 0; prev = -1
        for avg, sid, name in top:
            if avg != prev: rank += 1; prev = avg
            print("{:<5} | {:<20} | {:.2f}".format(rank, name, avg))

    def _best_disciplines(self):
        report = self.d_srv.get_disciplines_with_average()
        if not report: print("No grades recorded for any discipline."); return
        print("\n{:<25} | {:<10}".format("Discipline", "Average"))
        print("-" * 40)
        for name, avg in report: print("{:<25} | {:.2f}".format(name, avg))

    def _force_grade_all(self):
        print("Generating grades for all students...")
        # Now calls the Service to handle batch creation and batch undo
        count = self.g_srv.force_generate_grades_for_all()
        print(f"Success! Generated {count} new grades.")