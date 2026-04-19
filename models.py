class User:

    def __init__(self, user_id, username, first_name, last_name, email, phone, role):
        self.user_id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.role = role

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def display_info(self):
        print(f"\n{'='*45}")
        print(f"  USER PROFILE")
        print(f"{'='*45}")
        print(f"  ID       : {self.user_id}")
        print(f"  Username : {self.username}")
        print(f"  Name     : {self.full_name}")
        print(f"  Email    : {self.email}")
        print(f"  Phone    : {self.phone}")
        print(f"  Role     : {self.role.capitalize()}")
        print(f"{'='*45}")

    def to_file_string(self):
        return f"{self.user_id},{self.username},{self.first_name},{self.last_name},{self.email},{self.phone},{self.role}"

    @staticmethod
    def from_file_string(line):
        parts = line.strip().split(",")
        if len(parts) != 7:
            return None
        uid, uname, fname, lname, email, phone, role = parts
        if role == "admin":
            return Admin(uid, uname, fname, lname, email, phone)
        else:
            return Student(uid, uname, fname, lname, email, phone)


class Student(User):
    """Student user with grades and ECA data."""

    def __init__(self, user_id, username, first_name, last_name, email, phone):
        super().__init__(user_id, username, first_name, last_name, email, phone, "student")
        self.grades = {}   # {subject: mark}
        self.eca = []      # list of activity names

    def average_grade(self):
        if not self.grades:
            return 0.0
        return sum(self.grades.values()) / len(self.grades)

    def grade_status(self):
        avg = self.average_grade()
        if avg >= 80:
            return "Distinction"
        elif avg >= 60:
            return "Pass"
        else:
            return "At Risk"

    def display_grades(self):
        if not self.grades:
            print("  No grade records found.")
            return
        print(f"\n  {'Subject':<20} {'Marks':>6}  {'Grade':>10}")
        print(f"  {'-'*40}")
        for subject, mark in self.grades.items():
            grade = self._letter_grade(mark)
            print(f"  {subject:<20} {mark:>6}  {grade:>10}")
        print(f"  {'-'*40}")
        print(f"  {'Average':<20} {self.average_grade():>6.1f}  {self.grade_status():>10}")

    def _letter_grade(self, mark):
        if mark >= 90:
            return "A+"
        elif mark >= 80:
            return "A"
        elif mark >= 70:
            return "B+"
        elif mark >= 60:
            return "B"
        elif mark >= 50:
            return "C"
        else:
            return "F"

    def display_eca(self):
        if not self.eca:
            print("  No ECA records found.")
        else:
            print(f"  Activities ({len(self.eca)}): " + ", ".join(self.eca))

    def display_full_profile(self):
        self.display_info()
        print("\n  GRADES:")
        self.display_grades()
        print("\n  EXTRACURRICULAR ACTIVITIES:")
        self.display_eca()


class Admin(User):
    """Admin user with management privileges."""

    def __init__(self, user_id, username, first_name, last_name, email, phone):
        super().__init__(user_id, username, first_name, last_name, email, phone, "admin")

    def display_info(self):
        super().display_info()
        print("  [Administrator Account — Full Access]")
        print(f"{'='*45}")


class GradeRecord:
    """Encapsulates a student's grade data for file I/O."""

    SUBJECTS = ["FODS", "IT", "FOM", "AEEC"]

    @staticmethod
    def to_file_string(student):
        parts = [student.user_id]
        for subject, mark in student.grades.items():
            parts += [subject, str(mark)]
        return ",".join(parts)

    @staticmethod
    def from_file_string(line, students_map):
        parts = line.strip().split(",")
        if len(parts) < 3:
            return
        uid = parts[0]
        if uid not in students_map:
            return
        student = students_map[uid]
        i = 1
        while i + 1 < len(parts):
            subject = parts[i]
            try:
                mark = int(parts[i + 1])
                student.grades[subject] = mark
            except ValueError:
                pass
            i += 2


class ECARecord:
    """Encapsulates a student's ECA data for file I/O."""

    @staticmethod
    def to_file_string(student):
        return student.user_id + "," + ",".join(student.eca)

    @staticmethod
    def from_file_string(line, students_map):
        parts = line.strip().split(",")
        if len(parts) < 2:
            return
        uid = parts[0]
        if uid not in students_map:
            return
        students_map[uid].eca = [a.strip() for a in parts[1:] if a.strip()]