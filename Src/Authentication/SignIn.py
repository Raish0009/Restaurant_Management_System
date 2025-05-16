import json
import getpass 
from Src.Domain.Menu.Menu import Menu

class SignIn_Management:
    def __init__(self):
        self.admin_data = []
        self.staff_data = []

    def get_credentials(self):
        while True:
            username = input("Enter your username: ").strip()
            if not username:
                print("❌ Username cannot be empty.")
                continue
            if not username.replace(" ", "").isalpha():
                print("❌ Username must contain only alphabets and spaces.")
                continue
            break

        while True:
            password = getpass.getpass("Enter your password: ").strip()
            if not password:
                print("❌ Password cannot be empty.")
                continue
            if len(password) < 6:
                print("❌ Password must be at least 6 characters long.")
                continue
            break

        return username, password

    def load_data(self, path, user_type="admin"):
        try:
            with open(path, "r") as file:
                if user_type == "admin":
                    self.admin_data = json.load(file)
                elif user_type == "staff":
                    self.staff_data = json.load(file)
        except FileNotFoundError:
            print(f"❌ Error: File not found at {path}")
        except json.JSONDecodeError:
            print("❌ Error: Failed to decode JSON file")

    def validate_login(self, username, password, user_type="admin"):
        data = self.admin_data if user_type == "admin" else self.staff_data

        for user in data:
            if user.get("Username").lower() == username.lower() and user.get("Password") == password:
                print(f"\n✅ Welcome {user_type.capitalize()} {username}!")
                MyMenu = Menu()
                if user_type == "admin":
                    MyMenu.menucard()
                elif user_type == "staff":
                    MyMenu.staff_menu()
                return

        print("❌ Invalid username or password. Please try again.")

    def Signin(self, admin_path, staff_path):
        while True:
            print("\n1 - Admin Sign in")
            print("2 - Employee Sign in")
            print("3 - Exit")

            try:
                choice = int(input("Enter your choice: "))
            except ValueError:
                print("❌ Invalid input. Please enter a number.")
                continue

            if choice == 1:
                self.load_data(admin_path, user_type="admin")
                username, password = self.get_credentials()
                self.validate_login(username, password, user_type="admin")
            elif choice == 2:
                self.load_data(staff_path, user_type="staff")
                username, password = self.get_credentials()
                self.validate_login(username, password, user_type="staff")
            elif choice == 3:
                print("👋 Exiting...")
                break
            else:
                print("❌ Enter a valid choice!")
