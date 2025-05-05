import json
import uuid  

class SignUp_Management:
    def __init__(self):
        self.EmployeeData = []

    def Signup(self, path):
        try:
            with open(path, "r") as file:
                self.EmployeeData = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.EmployeeData = []

        print("1 - Employee Sign up")
        print("2 - Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            id=uuid.uuid4()
            employee_id = str(id)[:6]

            employee = {
                "id": employee_id,
                "Username": input("Enter your name: "),
                "Email": input("Enter your email: "),
                "Password": input("Enter your password: ")
            }

            self.EmployeeData.append(employee)

            with open(path, "w") as file:
                json.dump(self.EmployeeData, file, indent=4)

            print("Employee signed up successfully with ID:", employee_id)
        elif choice == 2:
            print("Returning to menu...")
        else:
            print("Enter a valid choice!")
