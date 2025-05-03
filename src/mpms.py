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
    
    def get_patient_object(self, patient_email):
        patient = Patient()
        with open(f"src\{patient_email[:8]}.txt", "r") as file:
            lines = file.readlines()
        for line in lines:
            line = line.rstrip().split(":")
            method_name = line[0]
            value = line[1]
            setattr(patient, method_name, value)
        print(patient)

    def start_app(self):
        self.user_login()
    
    def user_login(self):
        is_login_valid = False
        attempt = 0
        while (not is_login_valid):
            self.menu.show_login_page(attempt)
            email = input("Please enter email address: ").strip()
            if Validator.is_input_back(email):
                attempt = -1
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
                self.menu.show_admin_home_page()
            else:
                patient = self.get_patient_object(email)
                #self.menu.show_patient_home_page()

mpms = MPMS()
mpms.start_app()