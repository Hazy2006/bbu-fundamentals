import os
files_to_wipe = ["students.txt", "disciplines.txt", "grades.txt", "students.pickle", "disciplines.pickle", "grades.pickle"]

print("--- WIPING DATA ---")
for filename in files_to_wipe:
    if os.path.exists(filename):
        try:
            os.remove(filename)
            print(f"Deleted: {filename}")
        except Exception as e:
            print(f"Error deleting {filename}: {e}")
    else:
        print(f"Not found (Clean): {filename}")

print("\n--- DONE ---")
