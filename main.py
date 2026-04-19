"""
Student Management System


Default credentials:
  Admin   — username: admin,NYX      password: admin15,NYX15
  Student — username: seshank.sharma password: ram15
"""

import sys
import os

# Ensure the project directory is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from file_handler import load_all
from auth import login
from models import Admin, Student


def main():
    try:
        #Load all data
        users, students_map, admins_map, passwords = load_all()

        #Login
        user = login(users, passwords)
        if user is None:
            sys.exit(1)

        #Route to correct portal
        if isinstance(user, Admin):
            from admin_menu import admin_menu
            admin_menu(user, users, students_map, admins_map, passwords)

        elif isinstance(user, Student):
            from student_menu import student_menu
            student_menu(user, users, students_map, passwords)

        else:
            print("  [!] Unknown user role. Contact administrator.")

    except KeyboardInterrupt:
        print("\n\n  [!] Interrupted. Exiting.")
        sys.exit(0)
    except Exception as e:
        print(f"\n  [!] Unexpected error: {e}")
        raise


if __name__ == "__main__":
    main()