from menu import Menu
from validator import Validator
from patient import Patient

class MPMS:
    """
    This class contains the core logic of the Monash Patient Management System. 
    """

    # Class variable to store valid patient details.
    _valid_patient_details = {
        "patient1@student.monash.edu":"Monash1234!",
        "patient2@student.monash.edu":"Monash1234!"
    }

    # Class variable to store valid admin details.
    _valid_admin_details = {
        "admin@monash.edu":"Admin1234!"
    }

    def __init__(self):
        """
        Initialises MPMS Class instance.
        """
        self.menu = Menu()
        self.patient_list = [] 
        self.is_user_admin = False
        # Other Attributes
    
    def admin_home(self, admin):
        """
        This function contains the logic for the Admin Home Page to display UI, take input and route user.
        
        Args:
            admin (Admin):  Stores the admin object.
        """
        self.menu.show_admin_home_page() ################## INCOMPLETE
    
    def get_patient_object(self, patient_email):
        """
        This function creates a patient object and restores its instance state using a text file storing object state.

        Args:
            patient_email (str):    Stores the email of the patient whose object is to be initialised.
        """
        patient = Patient() # Create default patient object
        # Read appropriate patient file and load object state.
        with open(f"src\{patient_email[:8]}.txt", "r") as file:  
            lines = file.readlines()
        for line in lines:
            line = line.rstrip().split(":")
            method_name = line[0] # Get attribute name
            value = line[1] # Get attribute value
            setattr(patient, method_name, value) # Set values for the respective attributes.
        return patient
    
    def patient_home(self, patient):
        """
        This function contains the logic for the Patient Home Page to display UI, take input and route user.
        """
        is_valid_input = False # Flag variable to enable loop logic
        attempt = 0 # Variable to store the number of input attempts by user
        # Loop logic for taking user input.
        while(not is_valid_input):
            self.menu.show_patient_home_page(attempt)
            user_input = input("Your Input: ").strip()
            if Validator.is_input_logout(user_input):
                attempt = -2 # Standard attempt value for Logout
                break
            elif user_input == "1":
                # Profile Page Logic
                self.user_profile_page(patient)
            elif user_input == "2":
                # Book Appointment Logic
                pass
            elif user_input == "3":
                # Upcoming Appointment Logic
                pass
            elif user_input == "4":
                # Previous Appointment Logic
                pass
            else:
                attempt += 1
        # If  loop breaks, it is always a logout case but we check for attempt value anyway to enable future expansion of user actions.
        if attempt == -2:
            self.is_user_admin = False # Reset value in case Admin logs out.
            self.user_login() # Go to login page function to emulate logging out.

    def start_app(self):
        """
        Starts the MPMS Application.
        """
        self.user_login()  # Calls user login functionality.
    
    def user_login(self):
        """
        This function contains the logic for MPMS Login Page to display UI, take input and route user for the  
        """
        is_login_valid = False
        attempt = 0
        while (not is_login_valid):
            self.menu.show_login_page(attempt)
            email = input("Please enter email address: ").strip()
            if Validator.is_input_exit(email):
                attempt = -1 # Standard attempt value for Back/Exit
                break
            password = input("Please enter password: ").strip()
            if Validator.is_input_exit(password):
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
    
    def user_profile_page(self, user):
        is_input_valid = False
        attempt = 0
        while(not is_input_valid):
            self.menu.show_profile_page(user, self.is_user_admin)
            user_input = input("Your Input: ").strip()
            if Validator.is_input_back(user_input):
                attempt = -1
                break
        if attempt == -1:
            if self.is_user_admin:
                self.admin_home(user)
            else:
                self.patient_home(user)

if __name__ == "__main__":
    mpms = MPMS()
    mpms.start_app()