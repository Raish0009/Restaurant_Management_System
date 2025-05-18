import json
import uuid
import re
import getpass
from datetime import datetime

class SignUp_Management:
    def __init__(self):
        self.EmployeeData = []
        self.Logpath = rf"F:\Restaurant_Management_System\Src\Logs\SystemLog.txt"

    def write_log(self, message):
        try:
            with open(self.Logpath, "a") as log_file:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_file.write(f"[{timestamp}] {message}\n")
        except Exception as e:
            print(f"❌ Failed to write log: {e}")

    def is_valid_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email)

    def is_duplicate_email(self, email):
        for emp in self.EmployeeData:
            if emp['Email'].lower() == email.lower():
                return True
        return False

    def is_valid_password(self, password):
        if len(password) < 6:
            return False
        if not re.search(r'\d', password):
            return False
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False
        return True

    def Signup(self, path):
        # Load existing employee data
        try:
            with open(path, "r") as file:
                self.EmployeeData = json.load(file)
        except FileNotFoundError:
            self.EmployeeData = []
        except json.JSONDecodeError as jde:
            self.EmployeeData = []
            self.write_log(f"JSONDecodeError loading data: {jde}")
        except Exception as e:
            self.EmployeeData = []
            self.write_log(f"Exception loading data: {e}")

        # Name input loop
        while True:
            try:
                name = input("Enter your name: ").strip()
                if not name:
                    print("❌ Name cannot be empty.")
                    continue
                if not name.replace(" ", "").isalpha():
                    print("❌ Name must contain only alphabets and spaces.")
                    continue
                break
            except Exception as e:
                self.write_log(f"Exception during name input: {e}")
                print("❌ Error reading name. Please try again.")

        # Email input loop
        while True:
            try:
                email = input("Enter your email: ").strip()
                if not self.is_valid_email(email):
                    print("❌ Invalid email format.")
                    continue
                if self.is_duplicate_email(email):
                    print("❌ Email already registered.")
                    continue
                break
            except Exception as e:
                self.write_log(f"Exception during email input: {e}")
                print("❌ Error reading email. Please try again.")

        # Password input loop
        while True:
            try:
                password = getpass.getpass("Enter your password: ").strip()
                if not self.is_valid_password(password):
                    print("❌ Password must be 6+ chars, include a digit & special char.")
                    continue
                confirm_password = getpass.getpass("Confirm your password: ").strip()
                if password != confirm_password:
                    print("❌ Passwords do not match.")
                    continue
                break
            except Exception as e:
                self.write_log(f"Exception during password input: {e}")
                print("❌ Error reading password. Please try again.")

        # Create employee record
        employee_id = str(uuid.uuid4())[:6]
        employee = {
            "id": employee_id,
            "Username": name,
            "Email": email,
            "Password": password
        }
        self.EmployeeData.append(employee)

        # Save data back to file
        try:
            with open(path, "w") as file:
                json.dump(self.EmployeeData, file, indent=4)
            print(f"✅ Signed up successfully! Your ID is: {employee_id}")
            self.write_log(f"New signup: ID={employee_id}, Email={email}")
        except Exception as e:
            self.write_log(f"Exception writing signup data: {e}")
            print("❌ Failed to save data. Please try again.")

        # Post-signup management call (optional)
        try:
            from Src.Authentication.Manage import Manage
            manage = Manage()
            manage.management()
        except ModuleNotFoundError:
            print("⚠️ 'Manage' module not found. Skipping post-signup step.")
        except Exception as e:
            self.write_log(f"Exception calling Manage.management: {e}")
            print("⚠️ Error after signup. Please restart.")

