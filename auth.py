from file_handler import get_user_by_username


MAX_ATTEMPTS = 3


def login(users, passwords):
    print("\n" + "=" * 45)
    print("       STUDENT PROFILE MANAGEMENT SYSTEM")
    print("=" * 45)
    print("            Please Log In")
    print("=" * 45)

    attempts = 0
    while attempts < MAX_ATTEMPTS:
        if attempts > 0:
            print(f"\n  Attempts remaining: {MAX_ATTEMPTS - attempts}")

        username = input("\n  Username: ").strip()
        if not username:
            print("  [!] Username cannot be empty.")
            attempts += 1
            continue

        password = input("  Password: ").strip()

        if username not in passwords:
            print("  [!] Invalid username or password. Please try again.")
            attempts += 1
            continue

        if passwords[username] != password:
            print("  [!] Invalid username or password. Please try again.")
            attempts += 1
            continue

        user = get_user_by_username(users, username)
        if user is None:
            print("  [!] Account data error. Contact admin.")
            return None

        print(f"\n  Login successful! Welcome, {user.full_name}.")
        return user

    print("\n  [!] Too many failed attempts. Exiting.")
    return None


def change_password(username, passwords, old_password=None):
    if old_password is not None:
        current = input("  Current password: ").strip()
        if passwords.get(username) != current:
            print("  [!] Current password incorrect.")
            return False

    new_pwd = input("  New password: ").strip()
    confirm = input("  Confirm new password: ").strip()

    if not new_pwd:
        print("  [!] Password cannot be empty.")
        return False
    if new_pwd != confirm:
        print("  [!] Passwords do not match.")
        return False

    passwords[username] = new_pwd
    print("  [+] Password changed successfully.")
    return True