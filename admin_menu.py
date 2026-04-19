from models import Student, GradeRecord
from file_handler import (
    generate_user_id, username_exists, save_all
)
from auth import change_password


#  HELPERS

def _input(prompt):
    return input(f"  {prompt}").strip()


def _pause():
    input("\n  Press Enter to continue...")


def _divider(title=""):
    if title:
        print(f"\n{'='*45}")
        print(f"  {title}")
        print(f"{'='*45}")
    else:
        print(f"{'='*45}")


#  VIEW ALL STUDENTS

def view_all_students(students_map):
    _divider("ALL STUDENTS")
    if not students_map:
        print("  No students found.")
        _pause()
        return
    print(f"  {'ID':<8} {'Name':<25} {'Avg Grade':>10} {'Status':<15} {'ECA':>5}")
    print(f"  {'-'*65}")
    for s in students_map.values():
        print(f"  {s.user_id:<8} {s.full_name:<25} {s.average_grade():>10.1f} {s.grade_status():<15} {len(s.eca):>5}")
    _pause()


def view_student_detail(students_map):
    _divider("VIEW STUDENT DETAIL")
    uid = _input("Enter Student ID (e.g. U002): ").upper()
    if uid not in students_map:
        print("  [!] Student not found.")
        _pause()
        return
    students_map[uid].display_full_profile()
    _pause()


#  ADD USER

def add_user(users, students_map, admins_map, passwords):
    _divider("ADD NEW USER")
    role = _input("Role (student/admin): ").lower()
    if role not in ("student", "admin"):
        print("  [!] Invalid role.")
        _pause()
        return

    username = _input("Username: ")
    if not username:
        print("  [!] Username cannot be empty.")
        _pause()
        return
    if username_exists(users, username):
        print("  [!] Username already exists.")
        _pause()
        return

    first_name = _input("First name: ")
    last_name  = _input("Last name: ")
    email      = _input("Email: ")
    phone      = _input("Phone: ")
    password   = _input("Password: ")

    if not all([first_name, last_name, email, phone, password]):
        print("  [!] All fields are required.")
        _pause()
        return

    uid = generate_user_id(users)

    if role == "student":
        from models import Student
        new_user = Student(uid, username, first_name, last_name, email, phone)
        students_map[uid] = new_user
    else:
        from models import Admin as AdminClass
        new_user = AdminClass(uid, username, first_name, last_name, email, phone)
        admins_map[uid] = new_user

    users.append(new_user)
    passwords[username] = password
    save_all(users, students_map, passwords)

    print(f"\n  [+] User '{username}' added with ID {uid}.")
    _pause()


#  UPDATE USER

def update_user(users, students_map, passwords):
    _divider("UPDATE STUDENT RECORD")
    uid = _input("Enter Student ID: ").upper()
    if uid not in students_map:
        print("  [!] Student not found.")
        _pause()
        return

    student = students_map[uid]
    print(f"\n  Editing: {student.full_name} ({uid})")
    print("  Leave blank to keep current value.\n")

    fn = _input(f"First name [{student.first_name}]: ")
    ln = _input(f"Last name  [{student.last_name}]: ")
    em = _input(f"Email      [{student.email}]: ")
    ph = _input(f"Phone      [{student.phone}]: ")

    if fn: student.first_name = fn
    if ln: student.last_name  = ln
    if em: student.email      = em
    if ph: student.phone      = ph

    save_all(users, students_map, passwords)
    print("  [+] Record updated.")
    _pause()


def update_grades(users, students_map, passwords):
    _divider("UPDATE GRADES")
    uid = _input("Enter Student ID: ").upper()
    if uid not in students_map:
        print("  [!] Student not found.")
        _pause()
        return

    student = students_map[uid]
    print(f"\n  Editing grades for: {student.full_name}")
    print(f"  Subjects: {', '.join(GradeRecord.SUBJECTS)}")
    print("  Leave blank to keep current value.\n")

    for subject in GradeRecord.SUBJECTS:
        current = student.grades.get(subject, "N/A")
        val = _input(f"  {subject} [{current}]: ")
        if val:
            try:
                mark = int(val)
                if 0 <= mark <= 100:
                    student.grades[subject] = mark
                else:
                    print("    [!] Mark must be 0-100, skipped.")
            except ValueError:
                print("    [!] Invalid number, skipped.")

    save_all(users, students_map, passwords)
    print("  [+] Grades updated.")
    _pause()


def update_eca(users, students_map, passwords):
    _divider("UPDATE ECA")
    uid = _input("Enter Student ID: ").upper()
    if uid not in students_map:
        print("  [!] Student not found.")
        _pause()
        return

    student = students_map[uid]
    print(f"\n  Current ECA for {student.full_name}: {', '.join(student.eca) or 'None'}")
    print("  Enter activities as comma-separated list (replaces existing):")
    raw = _input("  Activities: ")

    if raw:
        student.eca = [a.strip() for a in raw.split(",") if a.strip()]
        save_all(users, students_map, passwords)
        print("  [+] ECA updated.")
    else:
        print("  [!] No changes made.")
    _pause()


#  DELETE USER

def delete_user(users, students_map, admins_map, passwords):
    _divider("DELETE STUDENT")
    uid = _input("Enter Student ID to delete: ").upper()
    if uid not in students_map:
        print("  [!] Student not found.")
        _pause()
        return

    student = students_map[uid]
    confirm = _input(f"  Delete '{student.full_name}' ({uid})? (yes/no): ").lower()
    if confirm != "yes":
        print("  Cancelled.")
        _pause()
        return

    username = student.username
    users.remove(student)
    del students_map[uid]
    if username in passwords:
        del passwords[username]

    save_all(users, students_map, passwords)
    print(f"  [+] Student {uid} deleted.")
    _pause()


#  INSIGHTS

def generate_insights(students_map):
    _divider("INSIGHTS & ANALYTICS")
    if not students_map:
        print("  No student data available.")
        _pause()
        return

    # Average per subject
    subject_totals = {}
    subject_counts = {}
    for s in students_map.values():
        for subj, mark in s.grades.items():
            subject_totals[subj] = subject_totals.get(subj, 0) + mark
            subject_counts[subj] = subject_counts.get(subj, 0) + 1

    print("\n  AVERAGE GRADES BY SUBJECT")
    print(f"  {'-'*35}")
    for subj in sorted(subject_totals):
        avg = subject_totals[subj] / subject_counts[subj]
        bar = "█" * int(avg / 5)
        print(f"  {subj:<15} {avg:>6.1f}  {bar}")

    # Top students
    print("\n\n  TOP 3 STUDENTS BY AVERAGE")
    print(f"  {'-'*35}")
    ranked = sorted(students_map.values(), key=lambda s: s.average_grade(), reverse=True)
    for i, s in enumerate(ranked[:3], 1):
        print(f"  {i}. {s.full_name:<22} {s.average_grade():.1f} ({s.grade_status()})")

    # Most active ECA
    print("\n\n  MOST ACTIVE ECA STUDENTS")
    print(f"  {'-'*35}")
    by_eca = sorted(students_map.values(), key=lambda s: len(s.eca), reverse=True)
    for s in by_eca[:3]:
        print(f"  {s.full_name:<22} {len(s.eca)} activit{'y' if len(s.eca)==1 else 'ies'}")

    # At-risk students
    at_risk = [s for s in students_map.values() if s.average_grade() < 60]
    print("\n\n  AT-RISK STUDENTS (avg < 60)")
    print(f"  {'-'*35}")
    if at_risk:
        for s in at_risk:
            print(f"  ⚠  {s.full_name:<22} avg: {s.average_grade():.1f}")
    else:
        print("  All students are performing above threshold.")

    _pause()


#  MAIN ADMIN MENU

def admin_menu(admin_user, users, students_map, admins_map, passwords):
    while True:
        _divider(f"ADMIN PANEL  —  {admin_user.full_name}")
        print("  [1] View All Students")
        print("  [2] View Student Detail")
        print("  [3] Add New User")
        print("  [4] Update Student Info")
        print("  [5] Update Student Grades")
        print("  [6] Update Student ECA")
        print("  [7] Delete Student")
        print("  [8] Generate Insights")
        print("  [9] Analytics Dashboard (Graphs)")
        print("  [0] Logout")
        print("=" * 45)

        choice = _input("Select option: ")

        if choice == "1":
            view_all_students(students_map)
        elif choice == "2":
            view_student_detail(students_map)
        elif choice == "3":
            add_user(users, students_map, admins_map, passwords)
        elif choice == "4":
            update_user(users, students_map, passwords)
        elif choice == "5":
            update_grades(users, students_map, passwords)
        elif choice == "6":
            update_eca(users, students_map, passwords)
        elif choice == "7":
            delete_user(users, students_map, admins_map, passwords)
        elif choice == "8":
            generate_insights(students_map)
        elif choice == "9":
            try:
                from analytics import analytics_dashboard
                analytics_dashboard(students_map)
            except ImportError:
                print("  [!] matplotlib/pandas not installed. Run: pip install matplotlib pandas")
                _pause()
        elif choice == "0":
            print(f"\n  Goodbye, {admin_user.full_name}!")
            break
        else:
            print("  [!] Invalid option.")