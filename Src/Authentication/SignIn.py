import json
import getpass
from datetime import datetime
from Src.Domain.Menu.Menu import Menu

class SignIn_Management:
    def __init__(self):
        self.admin_data = []
        self.staff_data = []
        self.Logpath = rf"F:\Restaurant_Management_System\Src\Logs\SystemLog.txt"  

    def write_log(self, message):
        with open(self.Logpath, "a") as log_file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"[{timestamp}] {message}\n")

    def get_credentials(self):
        try:
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
        except Exception as e:
            self.write_log(f"Exception in get_credentials: {e}")
            print("❌ An error occurred while getting credentials.")

    def load_data(self, path, user_type="admin"):
        try:
            with open(path, "r") as file:
                if user_type == "admin":
                    self.admin_data = json.load(file)
                elif user_type == "staff":
                    self.staff_data = json.load(file)
        except FileNotFoundError:
            print(f"❌ Error: File not found at {path}")
            self.write_log(f"FileNotFoundError: {path} not found during {user_type} data load")
        except json.JSONDecodeError:
            print("❌ Error: Failed to decode JSON file")
            self.write_log(f"JSONDecodeError: Failed to decode {user_type} data from {path}")
        except Exception as e:
            print("❌ Unexpected error while loading data.")
            self.write_log(f"Exception in load_data ({user_type}): {e}")

    def validate_login(self, username, password, user_type="admin"):
        try:
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
            self.write_log(f"Failed login attempt for {user_type}: {username}")
        except Exception as e:
            print("❌ Error during login validation.")
            self.write_log(f"Exception in validate_login ({user_type}): {e}")

    def Signin(self, admin_path, staff_path):
        while True:
            print("\n1 - Admin Sign in")
            print("2 - Employee Sign in")
            print("3 - Exit")

            try:
                choice = int(input("Enter your choice: "))
            except ValueError as ve:
                print("❌ Invalid input. Please enter a number.")
                self.write_log(f"ValueError in Signin menu: {ve}")
                continue
            except Exception as e:
                print("❌ Unexpected error in menu.")
                self.write_log(f"Exception in Signin menu input: {e}")
                continue

            if choice == 1:
                self.load_data(admin_path, user_type="admin")
                creds = self.get_credentials()
                if creds:
                    username, password = creds
                    self.validate_login(username, password, user_type="admin")
            elif choice == 2:
                self.load_data(staff_path, user_type="staff")
                creds = self.get_credentials()
                if creds:
                    username, password = creds
                    self.validate_login(username, password, user_type="staff")
            elif choice == 3:
                print("👋 Exiting...")
                break
            else:
                print("❌ Enter a valid choice!")
