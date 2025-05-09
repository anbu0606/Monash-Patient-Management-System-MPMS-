import sys #imports module that can perform system functions
import subprocess #imports module that can run commands on local system
from validator import Validator

class Menu:
    """
    Menu class handles the display of user interface for the MPMS Application.

    Instance Variables:
        banner (str):   The raw string of the ASCII Art for displaying as banner on all screens of MPMS
    """

    def __init__(self):
        """
        Initialises a Menu instance with the banner.
        """
        # Banner created using https://patorjk.com/software/taag/
        self.banner = r'''
=====================================================================================================================================================================
 __  __                       _     _____      _   _            _   __  __                                                   _    _____           _                 
|  \/  |                     | |   |  __ \    | | (_)          | | |  \/  |                                                 | |  / ____|         | |                
| \  / | ___  _ __   __ _ ___| |__ | |__) |_ _| |_ _  ___ _ __ | |_| \  / | __ _ _ __   __ _  __ _  ___ _ __ ___   ___ _ __ | |_| (___  _   _ ___| |_ ___ _ __ ___  
| |\/| |/ _ \| '_ \ / _` / __| '_ \|  ___/ _` | __| |/ _ \ '_ \| __| |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '_ ` _ \ / _ \ '_ \| __|\___ \| | | / __| __/ _ \ '_ ` _ \ 
| |  | | (_) | | | | (_| \__ \ | | | |  | (_| | |_| |  __/ | | | |_| |  | | (_| | | | | (_| | (_| |  __/ | | | | |  __/ | | | |_ ____) | |_| \__ \ ||  __/ | | | | |
|_|  |_|\___/|_| |_|\__,_|___/_| |_|_|   \__,_|\__|_|\___|_| |_|\__|_|  |_|\__,_|_| |_|\__,_|\__, |\___|_| |_| |_|\___|_| |_|\__|_____/ \__, |___/\__\___|_| |_| |_|
                                                                                              __/ |                                      __/ |                      
                                                                                             |___/                                      |___/                       
====================================================================================================================================================================='''

    def show_appointment_slots_page(self, slots, attempt_number=0):
        self.clear_screen()
        print(self.banner)
        available_slots = [slot for slot in slots if slot.availability]
        print("""
                                                                                APPOINTMENT BOOKING PAGE
""")
        print("Available Appointment Slots:\n")
        for i, slot in enumerate(available_slots, start=1):
            print(f"Slot {i}:")
            print(f"  Clinic: {slot.clinic_name}")
            print(f"  GP: {slot.gp_name}")
            print(f"  Date: {slot.date}")
            print(f"  Time: {slot.start_time}")
            print(f"  Duration: {slot.duration}")
            print(f"  Suburb: {slot.clinic_suburb}")
            print(f"  Reason: {slot.reason_for_visit}")
            # print(f"  Status: {slot.status}")
            print("-" * 50)
        print("Enter the slot number to book the appointment.")
        if attempt_number > 0:
            self.show_error_message("standard")
        self.show_logout_prompt()
        self.show_back_prompt()
        self.show_filter_prompt()
        user_input = input("Your Input: ").strip()
        if Validator.is_input_logout(user_input):
            return "logout"
        elif Validator.is_input_back(user_input):
            return "back"
        elif Validator.is_input_filter(user_input):
            return "filter"
        elif user_input.isdigit() and (int(user_input)-1 in range(len(available_slots))): #Check if input is a digit and within range of options displayed.
            return user_input
        else:
            return self.show_appointment_slots_page(slots, attempt_number+1)
    
    def show_booking_success_page(self, appointment):
        self.clear_screen()
        print(self.banner)
        print("\033[92m Your Appointment has been successfully booked! \033[0m")
        print(f"""
Appointment Details:
    Clinic:     {appointment.clinic_name}
    GP:         {appointment.gp_name}
    Date:       {appointment.date}
    Time:       {appointment.start_time}
    Duration:   {appointment.duration}
    Suburb:     {appointment.clinic_suburb}
    Reason:     {appointment.reason_for_visit}
    Status:     {appointment.status}

Press Enter to go to home page.
""")
        user_input = input("Press Enter to continue.. ")
        return user_input

    def clear_screen(self):
        """
        This function clears the terminal screen.
        """
        #Checks for host machine's OS and runs appropriate clear screen command.
        if sys.platform == 'win32':
            subprocess.run('cls', shell=True)
        else:
            subprocess.run('clear', shell=True)
    
    def show_admin_home_page(self, attempt_number):
        """
        Displays the Admin home page on the terminal
        """
        self.clear_screen()
        print(self.banner)
        print('''
                                                                     ADMIN HOME PAGE
                                                       Hi, Admin! What would you like to do today?
            ''')
        # Display error message is not first attempt
        if attempt_number > 0:
            self.show_error_message("standard")
        self.show_logout_prompt()
        print('''
1. View Profile
2. GP Report Generation
3. Clinic Report Generation
4. Manage Clinic
5. Manage GP
6. Manage Appointment Slots
7. Manage Patient Appointments

Please enter the Option Number or LOGOUT
            ''')
        user_input = input("Your Input: ").strip()
        if  Validator.is_input_logout(user_input):
            return "logout"
        elif user_input ==  "1":
            return "profile_page"
        elif user_input == "2":
            return "gp_report"
        elif user_input == "3":
            return "clinic_report"
        elif user_input == "4":
            return "manage_clinic"
        elif user_input == "5":
            return "manage_gp"
        elif user_input == "6":
            return "manage_appointment_slots"
        elif user_input == "7":
            return "manage_patient_appointments"
        else:
            return self.show_admin_home_page(attempt_number+1)
    
    def show_back_prompt(self):
        """
        Displays the standard prompt to inform the user that they can enter "BACK" as input on this screen.
        """
        print('''Enter \033[34m"BACK"\033[0m to go back to previous page\n''')

    def show_error_message(self, type):
        """
        This function displays an error message based on the type provided.

        Args:
            type (str): Type of error to be displayed.
        """
        if type == "login":
            print("\033[91m!! Invalid credentials. Please try again !!\033[0m")
        elif type == "standard":
            print("\033[91m!! Invalid input. Please try again !!\033[0m")

    def show_login_page(self, mpms_obj, attempt_number = 0):
        """
        Displays the Login Page and an Error message based on user attempt number.

        Args:
            attempt_number (int): Represents the number of times the user has failed to input valid details.
        """
        self.clear_screen()
        print(self.banner)
        print('''
                                                                     LOGIN PAGE
                                                       Please Enter Your Credentials To Login
            ''')
        # Display error message if not first attempt
        if attempt_number > 0:
            self.show_error_message("login")
        print('''Enter \033[34m"EXIT"\033[0m to go back to previous page\n''')
        email = input("Please enter email address: ").strip()
        if Validator.is_input_exit(email):
            self.clear_screen()
            print("Exiting...")
            return "exit", email
        password = input("Please enter password: ").strip()
        if Validator.is_input_exit(password):
            self.clear_screen()
            print("Exiting...")
            return "exit", email
        is_login_valid = Validator.is_valid_patient_login(mpms_obj.get_valid_user_details("patient"), email, password)
        if is_login_valid:
            return "patient_home_page",email
        else:
            is_login_valid = Validator.is_valid_admin_login(mpms_obj.get_valid_user_details("admin"), email, password)
            if is_login_valid:
                return "admin_home_page",email
            else: # Invalid details
                return self.show_login_page(mpms_obj, attempt_number+1)
    
    def show_logout_prompt(self):
        """
        Displays the standard prompt to inform the user that they can enter "LOGOUT" as input on this screen.
        """
        print('''Enter \033[34m"LOGOUT"\033[0m to go back to Login Page\n''')

    def show_filter_prompt(self):
        """
        Displays the standard prompt to inform the user that they can enter "FILTER" as input on this screen.
        """
        print('''Enter \033[34m"FILTER"\033[0m to go back to filter appointment slots\n''')

    def show_cancel_prompt(self):
        """
        Displays the standard prompt to inform the user that they can enter "cancel" as input on this screen.
        """
        print('''Enter \033[34m"CANCEL"\033[0m to cancel the Appointment\n''')

    def show_patient_home_page(self, attempt_number=0):
        """
        Displays the  patient home page with user action menu.

        Args:
            attempt_number (int): Represents the number of times the user has failed to input valid details.
        """
        self.clear_screen()
        print(self.banner)
        print('''
                                                                     PATIENT HOME PAGE
                                                           Hi! What would you like to do today?
            ''')
        # Display error message if not first attempt
        if attempt_number > 0:
            self.show_error_message("standard")
        self.show_logout_prompt()
        print('''
1. My Profile
2. Book an Appointment
3. View Upcoming Appointments
4. Previous Appointments

Please enter the Option Number or LOGOUT
            ''')
        user_input = input("Your Input: ").strip()
        if  Validator.is_input_logout(user_input):
            return "logout"
        elif user_input ==  "1":
            return "profile_page"
        elif user_input == "2":
            return "book_appointment"
        elif user_input == "3":
            return "upcoming_appointments"
        elif user_input == "4":
            return "previous_appointments"
        else:
            return self.show_patient_home_page(attempt_number+1)
    
    def show_previous_appointments_page(self, appointments):
        """
        Displays the previous appointments page with a list of past appointments.
        
        Args:
            appointments (list): List of past Appointment objects
        """
        self.clear_screen()
        print(self.banner)
        print("""
                                                                                PREVIOUS APPOINTMENTS
        """)
        
        if not appointments:
            print("\nYou have no previous appointments to display.\n")
        else:
            print("\nYour Previous Appointments:\n")
            for i, appt in enumerate(appointments, start=1):
                print(f"Appointment {i}:")
                print(f"  Clinic: {appt.clinic_name}")
                print(f"  GP: {appt.gp_name}")
                print(f"  Date: {appt.date}")
                print(f"  Time: {appt.start_time}")
                print(f"  Duration: {appt.duration} minutes")
                print(f"  Suburb: {appt.clinic_suburb}")
                print(f"  Reason: {appt.reason_for_visit}")
                print(f"  Status: {appt.status}")
                print("-" * 50)
        
        
        self.show_logout_prompt()
        self.show_back_prompt()
        user_input = input("Your Input: ").strip()
        if Validator.is_input_logout(user_input):
            return "logout"
        elif Validator.is_input_back(user_input):
            print("trying to go back")
            return "back"
        

    def show_profile_page(self, attempt_number, user_obj, is_user_admin):
        """
        Displays the user profile page with user details.

        Args:
            attempt_number (int):       Represents the number of times the user has failed to input valid details.
            user_obj (Admin/Patient):   User object that is user to extract user details    
            is_user_admin (bool):       A flag to represent the user's system role.
        """
        if is_user_admin:
            user_role = "ADMIN"
        else:
            user_role = "PATIENT"
        self.clear_screen()
        print(self.banner)
        print(f'''
                                                                     {user_role} PROFILE PAGE
{user_obj}
            ''')
        # Display error message is not first attempt
        if attempt_number > 0:
            self.show_error_message("standard")
        self.show_logout_prompt()
        self.show_back_prompt()
        user_input = input("Your Input: ").strip()
        if Validator.is_input_logout(user_input):
            return "logout"
        elif Validator.is_input_back(user_input):
            print("trying to go back")
            return "back"
        else:
            return self.show_profile_page(attempt_number+1, user_obj, is_user_admin)
        

    
    def show_upcoming_appointments_page(self, appointments):
        """
        Displays the upcoming appointments page with a list of upcoming appointments.
        
        Args:
            appointments (list): List of past Appointment objects
        """
        self.clear_screen()
        print(self.banner)
        print("""
                                                                                UPCOMING APPOINTMENTS
        """)
        
        if not appointments:
            print("\nYou have no upcoming appointments to display.\n")
        else:
            print("\nYour Upcoming Appointments:\n")
            for i, appt in enumerate(appointments, start=1):
                print(f"Appointment {i}:")
                print(f"  Clinic: {appt.clinic_name}")
                print(f"  GP: {appt.gp_name}")
                print(f"  Date: {appt.date}")
                print(f"  Time: {appt.start_time}")
                print(f"  Duration: {appt.duration} minutes")
                print(f"  Suburb: {appt.clinic_suburb}")
                print(f"  Reason: {appt.reason_for_visit}")
                print(f"  Status: {appt.status}")
                print("-" * 50)
        
        self.show_logout_prompt()
        self.show_back_prompt()
        self.show_cancel_prompt()
        user_input = input("Your Input: ").strip()
        if Validator.is_input_logout(user_input):
            return "logout"
        elif Validator.is_input_back(user_input):
            print("trying to go back")
            return "back"
        elif user_input == "cancel":
            return user_input
    def show_cancellation_confirmation_page(self, appointment):

        print("\033[91m You are about to cancel the following appointment:\033[0m")
        print(appointment)
        print("\nAre you sure you want to cancel this appointment? (CONFIRM/BACK)")
        while True:
            user_input = input("Enter your choice: ").strip()
            if user_input in ["CONFIRM", "BACK"]:
                return user_input
            else:
                print("\033[91m Invalid input. Please enter 'CONFIRM' or 'BACK'.\033[0m")

    def show_cancellation_success_page(self, appointment):

        print("\033[92m The appointment has been successfully cancelled! \033[0m")
        print(appointment)
        # input("\nPress Enter to continue...")
        user_input = input("Press Enter to continue.. ")
        return user_input

    # def show_cancellation_failure_page(self):

    #     print("\nUnable to cancel the appointment. Please try again.")
    #     input("\nPress Enter to continue...")


     # implementation of filter
    def show_filter_options(self):
        #self.clear_screen()
       # print(self.banner)
        print("""
FILTER APPOINTMENT SLOTS

    You can filter by:
    1. Date
    2. GP Name
    3. Clinic Suburb

    Enter the option number or BACK/LOGOUT to return.
        """)
        return input("Your Input: ").strip()

    def get_filter_value(self, filter_type):
        prompts = {
            "date": "Enter the date (DD-MM-YYYY): ",
            "gp": "Enter the GP name (e.g., Dr. Smith): ",
            "suburb": "Enter the clinic suburb (e.g., Clayton): "
        }
        return input(prompts[filter_type]).strip()
