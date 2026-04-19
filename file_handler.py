import os
from models import User, Student, Admin, GradeRecord, ECARecord

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

USERS_FILE     = os.path.join(DATA_DIR, "users.txt")
PASSWORDS_FILE = os.path.join(DATA_DIR, "passwords.txt")
GRADES_FILE    = os.path.join(DATA_DIR, "grades.txt")
ECA_FILE       = os.path.join(DATA_DIR, "eca.txt")


def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


#LOAD

def load_passwords():
    """Return {username: password} dict."""
    passwords = {}
    try:
        with open(PASSWORDS_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line and "," in line:
                    uname, pwd = line.split(",", 1)
                    passwords[uname.strip()] = pwd.strip()
    except FileNotFoundError:
        pass
    return passwords


def load_users():
    """Return (users_list, students_map {uid: Student}, admins_map {uid: Admin})."""
    users = []
    students = {}
    admins = {}
    try:
        with open(USERS_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                user = User.from_file_string(line)
                if user:
                    users.append(user)
                    if isinstance(user, Student):
                        students[user.user_id] = user
                    elif isinstance(user, Admin):
                        admins[user.user_id] = user
    except FileNotFoundError:
        pass
    return users, students, admins


def load_grades(students_map):
    """Populate grades into student objects."""
    try:
        with open(GRADES_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    GradeRecord.from_file_string(line, students_map)
    except FileNotFoundError:
        pass


def load_eca(students_map):
    """Populate ECA lists into student objects."""
    try:
        with open(ECA_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    ECARecord.from_file_string(line, students_map)
    except FileNotFoundError:
        pass


def load_all():
    """Load everything and return (users, students_map, admins_map, passwords)."""
    _ensure_data_dir()
    users, students, admins = load_users()
    load_grades(students)
    load_eca(students)
    passwords = load_passwords()
    return users, students, admins, passwords


#SAVE

def save_users(users):
    _ensure_data_dir()
    with open(USERS_FILE, "w") as f:
        for user in users:
            f.write(user.to_file_string() + "\n")


def save_passwords(passwords):
    _ensure_data_dir()
    with open(PASSWORDS_FILE, "w") as f:
        for uname, pwd in passwords.items():
            f.write(f"{uname},{pwd}\n")


def save_grades(students_map):
    _ensure_data_dir()
    with open(GRADES_FILE, "w") as f:
        for student in students_map.values():
            if student.grades:
                f.write(GradeRecord.to_file_string(student) + "\n")


def save_eca(students_map):
    _ensure_data_dir()
    with open(ECA_FILE, "w") as f:
        for student in students_map.values():
            if student.eca:
                f.write(ECARecord.to_file_string(student) + "\n")


def save_all(users, students_map, passwords):
    save_users(users)
    save_passwords(passwords)
    save_grades(students_map)
    save_eca(students_map)


# HELPERS

def generate_user_id(users):
    """Generate next sequential user ID like U007."""
    ids = []
    for u in users:
        try:
            ids.append(int(u.user_id[1:]))
        except (ValueError, IndexError):
            pass
    next_num = max(ids, default=0) + 1
    return f"U{next_num:03d}"


def get_user_by_username(users, username):
    for u in users:
        if u.username == username:
            return u
    return None


def username_exists(users, username):
    return any(u.username == username for u in users)