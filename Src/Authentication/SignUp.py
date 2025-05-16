import json
import uuid
import re
import getpass

class SignUp_Management:
    def __init__(self):
        self.EmployeeData = []

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
        try:
            with open(path, "r") as file:
                self.EmployeeData = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.EmployeeData = []

        # Name Validation Loop
        while True:
            name = input("Enter your name: ").strip()
            if not name:
                print("❌ Name cannot be empty. Please try again.")
                continue
            if not name.replace(" ", "").isalpha():
                print("❌ Name must contain only alphabets and spaces.")
                continue
            break

        # Email Validation Loop
        while True:
            email = input("Enter your email: ").strip()
            if not self.is_valid_email(email):
                print("❌ Invalid email format. Please try again.")
                continue
            if self.is_duplicate_email(email):
                print("❌ This email is already registered. Try a different one.")
                continue
            break

        # Password Validation Loop
        while True:
            password = getpass.getpass("Enter your password: ").strip()
            if not self.is_valid_password(password):
                print("❌ Password must be at least 6 characters long, contain at least one digit and one special character.")
                continue
            confirm_password = getpass.getpass("Confirm your password: ").strip()
            if password != confirm_password:
                print("❌ Passwords do not match. Please try again.")
                continue
            break

        employee_id = str(uuid.uuid4())[:6]

        employee = {
            "id": employee_id,
            "Username": name,
            "Email": email,
            "Password": password  
        }

        self.EmployeeData.append(employee)

        with open(path, "w") as file:
            json.dump(self.EmployeeData, file, indent=4)

        print("✅ Employee signed up successfully with ID:", employee_id)

        try:
            from Src.Authentication.Manage import Manage
            manage = Manage()
            manage.management()
        except ModuleNotFoundError:
            print("⚠️ 'Manage' module not found. Skipping post-signup management.")
