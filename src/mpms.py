from menu import Menu
from validator import Validator
from patient import Patient

class MPMS:
    _valid_patient_details = {
        "patient1@student.monash.edu":"Monash1234!",
        "patient2@student.monash.edu":"Monash1234!"
    }
    _valid_admin_details = {
        "admin@monash.edu":"Admin1234!"
    }

    def __init__(self):
        self.menu = Menu()
        self.patient_list = []
        self.is_user_admin = False
        # Other Attributes
    
    def admin_home(self, admin):
        self.menu.show_admin_home_page()
    
    def get_patient_object(self, patient_email):
        patient = Patient()
        with open(f"src\{patient_email[:8]}.txt", "r") as file:
            lines = file.readlines()
        for line in lines:
            line = line.rstrip().split(":")
            method_name = line[0]
            value = line[1]
            setattr(patient, method_name, value)
        return patient
    
    def patient_home(self, patient):
        is_valid_input = False
        attempt = 0
        while(not is_valid_input):
            self.menu.show_patient_home_page(attempt)
            user_input = input("Your Input: ").strip()
            if Validator.is_input_logout(user_input):
                attempt = -2 # Standard attempt value for Logout
                break
            elif user_input == "1":
                self.menu.show_profile_page(patient, self.is_user_admin)
            elif user_input == "2":
                pass
            elif user_input == "3":
                pass
            elif user_input == "4":
                pass
            else:
                attempt += 1
        # If  loop breaks, it is always a logout case but we check for attempt value anyway to enable future expansion of user actions.
        if attempt == -2:
            self.is_user_admin = False # Reset value in case Admin logs out.
            self.user_login() # Go to login page function to emulate logging out.

    def start_app(self):
        self.user_login()
    
    def user_login(self):
        is_login_valid = False
        attempt = 0
        while (not is_login_valid):
            self.menu.show_login_page(attempt)
            email = input("Please enter email address: ").strip()
            if Validator.is_input_back(email):
                attempt = -1 # Standard attempt value for Back
                break
            password = input("Please enter password: ").strip()
            if Validator.is_input_back(password):
                attempt = -1
                break
            is_login_valid = Validator.is_valid_patient_login(MPMS._valid_patient_details, email, password)
            if is_login_valid:
                break
            else:
                is_login_valid = Validator.is_valid_admin_login(MPMS._valid_admin_details, email, password)
                if is_login_valid:
                    self.is_user_admin = True
                    break
                attempt += 1
        if attempt == -1:
            self.menu.clear_screen()
            print("Exiting...")
        else:
            if self.is_user_admin:
                admin = None
                # admin = Admin(
                #     email = "admin@monash.edu",
                #     fname = "Alexa",
                #     lname = "Monash",
                #     mobile_num = "+61 428654982",
                #     password = "Admin1234!"
                #     )
                self.admin_home(admin)
            else:
                patient = self.get_patient_object(email)
                self.patient_home(patient)


if __name__ == "__main__":
    mpms = MPMS()
    mpms.start_app()