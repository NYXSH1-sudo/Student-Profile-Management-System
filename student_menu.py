from file_handler import save_all
from auth import change_password


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


#  VIEW

def view_profile(student):
    student.display_info()
    _pause()


def view_grades(student):
    _divider(f"GRADES  —  {student.full_name}")
    student.display_grades()
    _pause()


def view_eca(student):
    _divider(f"ECA  —  {student.full_name}")
    student.display_eca()
    _pause()


def view_full(student):
    _divider(f"FULL PROFILE  —  {student.full_name}")
    student.display_full_profile()
    _pause()


#  UPDATE PERSONAL INFO

def update_profile(student, users, students_map, passwords):
    _divider("UPDATE PROFILE")
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
    print("  [+] Profile updated.")
    _pause()


#  MAIN STUDENT MENU

def student_menu(student, users, students_map, passwords):
    while True:
        _divider(f"STUDENT PORTAL  —  {student.full_name}")
        print("  [1] View My Full Profile")
        print("  [2] View My Grades")
        print("  [3] View My ECA Activities")
        print("  [4] Update Personal Information")
        print("  [5] Change Password")
        print("  [0] Logout")
        print("=" * 45)

        choice = _input("Select option: ")

        if choice == "1":
            view_full(student)
        elif choice == "2":
            view_grades(student)
        elif choice == "3":
            view_eca(student)
        elif choice == "4":
            update_profile(student, users, students_map, passwords)
        elif choice == "5":
            changed = change_password(student.username, passwords, old_password=True)
            if changed:
                save_all(users, students_map, passwords)
            _pause()
        elif choice == "0":
            print(f"\n  Goodbye, {student.full_name}!")
            break
        else:
            print("  [!] Invalid option.")