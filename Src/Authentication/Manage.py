from Src.Authentication.SignIn import SignIn_Management
from Src.Authentication.SignUp import SignUp_Management

class Manage():

    def __init__(self):
        self.Staffpath=rf"F:\Restaurant_Management_System\Src\Database\Staff.json"
        self.Adminpath=rf"F:\Restaurant_Management_System\Src\Database\Admin.json"
        self.EmployeeData=[]
        

    def management(self):
        print("** Jodhpur Restaurant **")
        print("1 - Sign in")
        print("2 - Sign up")
        print("3 - Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            signin_ins = SignIn_Management()
            signin_ins.Signin(self.Adminpath,self.Staffpath)
        elif choice == 2:
            signup_ins = SignUp_Management()
            signup_ins.Signup(self.Staffpath)  
        elif choice == 3:
            exit()
        else:
            print("Enter valid choice!")
            self.management()  
