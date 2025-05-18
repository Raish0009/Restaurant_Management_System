from datetime import datetime
from Src.Authentication.SignIn import SignIn_Management
from Src.Authentication.SignUp import SignUp_Management

class Manage:

    def __init__(self):
        self.Staffpath = rf"F:\Restaurant_Management_System\Src\Database\Staff.json"
        self.Adminpath = rf"F:\Restaurant_Management_System\Src\Database\Admin.json"
        self.Logpath = rf"F:\Restaurant_Management_System\Src\Logs\SystemLog.txt"
        self.EmployeeData = []

    def write_log(self, message):
        with open(self.Logpath, "a") as log_file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"[{timestamp}] {message}\n")

    def management(self):
        try:
            print("** Jodhpur Restaurant **")
            print("1 - Sign in")
            print("2 - Sign up")
            print("3 - Exit")

            choice = int(input("Enter your choice: "))

            if choice == 1:
                signin_ins = SignIn_Management()
                signin_ins.Signin(self.Adminpath, self.Staffpath)
            elif choice == 2:
                signup_ins = SignUp_Management()
                signup_ins.Signup(self.Staffpath)
            elif choice == 3:
                print("Exiting program...")
                exit()
            else:
                print("Enter valid choice!")
                self.management()

        except ValueError as ve:
            self.write_log(f"ValueError: Invalid input! Expected a number. Details: {ve}")
            print("Please enter a valid number.")
            self.management()
        except Exception as e:
            self.write_log(f"Exception: Unexpected error occurred. Details: {e}")
            print("An unexpected error occurred. Please try again.")
            self.management()
