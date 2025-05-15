import json
import uuid
import re
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

        name = input("Enter your name: ").strip()

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
            password = input("Enter your password: ").strip()
            if not self.is_valid_password(password):
                print("❌ Password must be at least 6 characters long, contain at least one digit and one special character.")
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
        from Src.Authentication.Manage import Manage
        manage = Manage()
        manage.management()


if __name__ == "__main__":
    manager = SignUp_Management()
    manager.Signup("employees.json")
