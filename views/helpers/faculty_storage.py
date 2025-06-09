import os

FACULTY_FILE = os.path.join(os.path.dirname(__file__), "selected_faculty.txt")

def save_selected_faculty(faculty_name: str):
    with open(FACULTY_FILE, "w") as f:
        f.write(faculty_name)

def load_selected_faculty():
    if not os.path.exists(FACULTY_FILE):
        return None
    with open(FACULTY_FILE, "r") as f:
        return f.read().strip()
