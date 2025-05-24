import sys #imports module that can perform system functions
import subprocess #imports module that can run commands on local system
from validator import Validator
import re
from datetime import datetime, timedelta

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
    

    def clear_screen(self):
        """
        This function clears the terminal screen.
        """
        #Checks for host machine's OS and runs appropriate clear screen command.
        if sys.platform == 'win32':
            subprocess.run('cls', shell=True)
        else:
            subprocess.run('clear', shell=True)
    
    def display_instances(self, instances, instance_type, pagination=None):
        '''
        This function displays all types of instances with indexing.
        Args:
            instances(list); List of all instances
            instance_type(str): String value that identifies the type of instance.
        '''
        if instance_type == "gp":
            for i, gp in enumerate(instances, start=1):
                if not pagination:
                    actual_index = i
                else:
                    actual_index = pagination['showing_from'] - 1 + i
                print(f"--- GP {actual_index} ---")
                print(f"gp_name:        {gp.get_gp_name()}")
                print(f"email:             {gp.get_email()}")
                print(f"assigned_clinics: {', '.join(gp.get_assigned_clinics())}")
                print(f"specialisation: {', '.join(gp.get_specialisation())}")
                print(f"availability:    {gp.get_availability()}")
                print("-" * 50 + "\n")
        elif instance_type == "appt":
            for i, appt in enumerate(instances, start=1):
                if not pagination:
                    actual_index = i
                else:
                    actual_index = pagination['showing_from'] - 1 + i
                print(f"Appointment {actual_index}:")
                print(f"  GP: {appt.slot.gp_name}")
                print(f"  Date: {appt.slot.date}")
                print(f"  Time: {appt.slot.start_time}")
                print(f"  Suburb: {appt.slot.clinic_suburb}")
                print("-" * 50)
        elif instance_type == "slot":
            for i, slot in enumerate(instances, start=1):
                if not pagination:
                    actual_index = i
                else:
                    actual_index = pagination['showing_from'] - 1 + i
                print(f"Slot {actual_index}:")
                print(f"  Clinic: {slot.get_clinic_name()}")
                print(f"  GP: {slot.get_gp_name()}")
                print(f"  Date: {slot.get_date()}")
                print(f"  Time: {slot.get_start_time()}")
                print(f"  Duration: {slot.get_duration()}")
                print(f"  Suburb: {slot.get_clinic_suburb()}")
                print(f"  Reason: {slot.get_reason_for_visit()}")
                print("-" * 50)
        elif instance_type == "clinic":
            for i, clinic in enumerate(instances, start=1):
                if not pagination:
                    actual_index = i
                else:
                    actual_index = pagination['showing_from'] - 1 + i
                print(f"--- Clinic {i} ---")
                print(f"clinic_name:        {clinic.get_clinic_name()}")
                print(f"Suburb:             {clinic.get_suburb()}")
                print(f"available_services: {', '.join(clinic.get_available_services())}")
                print(f"Operating Hours:    {clinic.get_operating_hours()}")
                print("-" * 50 + "\n")


    def get_filter_value(self, filter_type):
        """
        Prompts the user for a filter value based on the filter type.
        Args:
            filter_type (str): The type of filter to apply (date, gp_name, clinic_suburb).
        Returns:
            str: The filter value entered by the user.
        """
        prompts = {
            "date": "Enter the date (DD-MM-YYYY): ",
            "gp_name": "Enter the GP name (e.g., Dr. Emily Red): ",
            "clinic_suburb": "Enter the clinic suburb (e.g., Clayton): "
        }
        return input(prompts[filter_type]).strip()
    
    def get_valid_input(self, prompt, validator_func):
        '''
        Helper function for input loop for wrong inputs while allowing the user to go Back or Logout.
        '''
        while True:
            value = input(prompt).strip()
            if Validator.is_input_back(value):
                return "back"
            if Validator.is_input_logout(value):
                return "logout"
            if validator_func(value):
                return value
            print("\033[91m!! Input validation failed. Please try again !!\033[0m")
    
    def show_admin_home_page(self, attempt_number):
        """
        Displays the Admin home page on the terminal
        Args:
            attempt_number (int): Represents the number of times the user has failed to input valid details.
        
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
        self.show_prompt(type = "logout")
        print('''
1. View Profile
2. GP Report Generation
3. Appointment Reason Report Generation
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
            return "reason_report"
        elif user_input == "4":
            return "manage_clinics"
        elif user_input == "5":
            return "manage_gp"
        elif user_input == "6":
            return "manage_appointment_slots"
        elif user_input == "7":
            return "manage_patient_appointments"
        else:
            return self.show_admin_home_page(attempt_number+1)
    
    def show_appointment_slot_management_page(self, slots, attempt_number=0):
        '''
        Displays the appointment slots management page where the Admin can perform CRUD for AppointmentSlots.

        Args:
            slots(list): List of appointment slots.
            attempt_number(int): Represents the number of times the user has failed to input valid details.
        '''
        self.clear_screen()
        print(self.banner)
        print("""
                                                                    APPOINTMENT SLOT MANAGEMENT PAGE
""")
        if len(slots) == 0:
            print("\nYou have no slots to display.\n")
        else:
            print("\n--- List of All Appointment Slots ---")
            print("-" * 50)
            self.display_instances(slots, instance_type="slot")
        self.show_prompt(type = "logout")
        self.show_prompt(type = "back")
        self.show_prompt(type = "update")
        self.show_prompt(type = "create")
        self.show_prompt(type = "delete")
        if attempt_number > 0:
            self.show_error_message("standard")
        elif attempt_number == -1:
            print("\033[90m!!You have no appointment slots to update/delete!!\033[0m")
        user_input = input("Your Input: ").strip()
        if Validator.is_input_logout(user_input):
            return "logout"
        elif Validator.is_input_back(user_input):
            return "back"
        elif user_input == "UPDATE":
            if slots:
                return "update"
            else:
                # No gps to update
                attempt_number = -1
                return self.show_appointment_slot_management_page(slots, attempt_number)
        elif user_input == "CREATE":
            return "create"
        elif user_input == "DELETE":
            return "delete"
        else:
            return self.show_appointment_slot_management_page(slots, attempt_number=1)

    def show_appointment_slot_update_menu(self, slot_to_update, attempt_number=0):
        self.clear_screen()
        print(self.banner)
        print("""
                                                                    APPOINTMENT SLOT UPDATE PAGE
""")

        print("\n--- Slot To Update ---")
        print("-" * 50)
        print(str(slot_to_update)[:-2])
        print("\n--- Update Appointment Slot Details ---")
        print("\nLeave the field empty if you don't want to change it.")
        if attempt_number > 0:
            self.show_error_message("standard")
        new_availability = input(f"New Availability (True/False only): ") or slot_to_update.get_availability()
        if new_availability not in ["True", "False"]:
            self.show_appointment_slot_update_menu(slot_to_update, attempt_number+1)
        new_clinic_name = input(f"New Clinic Name (Minimum of 3 characters) ") or slot_to_update.get_clinic_name()
        if len(new_clinic_name) < 3:
            self.show_appointment_slot_update_menu(slot_to_update, attempt_number+1)
        new_clinic_suburb = input(f"New Clinic Suburb (Minimum of 3 characters): ") or slot_to_update.get_clinic_suburb()
        if len(new_clinic_suburb) < 3:
            self.show_appointment_slot_update_menu(slot_to_update, attempt_number+1)
        new_date = input(f"New Date (dd-mm-yyyy format only. Cannot enter date from past): ") or slot_to_update.get_date()
        if not Validator.is_valid_date_format(new_date, allow_past=False):
            self.show_appointment_slot_update_menu(slot_to_update, attempt_number+1)
        new_duration = input(f"New Duration (Valid duration values: 15, 20, 45, 60): ") or slot_to_update.get_duration()
        if not Validator.is_valid_duration(new_duration):
            self.show_appointment_slot_update_menu(slot_to_update, attempt_number+1)
        new_gp_name = input(f"New GP Name (Enter 'Dr.' as prefix. Name cannot be empty): ") or slot_to_update.get_gp_name()
        if not Validator.is_valid_gp_name(new_gp_name):
            self.show_appointment_slot_update_menu(slot_to_update, attempt_number+1)
        new_reason_for_visit = input(f"New Reason for Visit (valid options: 'General Consultation','Vaccination','Specialist Referral'): ") or slot_to_update.get_reason_for_visit()
        if new_reason_for_visit not in ['General Consultation','Vaccination','Specialist Referral']:
            self.show_appointment_slot_update_menu(slot_to_update, attempt_number+1)
        new_start_time = input(f"New Start Time (24hh:mm format only): ") or slot_to_update.get_start_time()
        if not Validator.is_valid_time_format(new_start_time):
            self.show_appointment_slot_update_menu(slot_to_update, attempt_number+1)
        updated_details = {
            "availability": new_availability,
            "clinic_name": new_clinic_name,
            "clinic_suburb": new_clinic_suburb,
            "date": new_date,
            "duration": new_duration,
            "gp_name": new_gp_name,
            "reason_for_visit": new_reason_for_visit,
            "start_time": new_start_time,
        }
        return updated_details

    def show_appointment_slot_update_page(self, slots, attempt_number=0):
        self.clear_screen()
        print(self.banner)
        print("""
                                                                    APPOINTMENT SLOT UPDATE PAGE
""")
        print("\n--- List of All Appointment Slots ---")
        print("-" * 50)
        self.display_instances(slots, instance_type="slot")
        print("\nEnter the Slot Number to Update or type 'BACK' to return to the Home Page")
        if attempt_number > 0:
            self.show_error_message("standard")
        self.show_prompt(type = "logout")
        self.show_prompt(type = "back")
        user_input = input("Your Input: ").strip()
        if Validator.is_input_logout(user_input):
            return "logout"
        elif Validator.is_input_back(user_input):
            return "back"
        elif user_input.isdigit() and (int(user_input)-1 in range(len(slots))): #Check if input is a digit and within range of options displayed.
            return user_input
        else:
            return self.show_appointment_slot_update_page(slots, attempt_number=attempt_number+1)
        
    def show_appointment_slots_page(self, slots, attempt_number=0, is_skip_enabled = False):
        """
        Displays the appointment slots page with available slots for booking.
        Args:
            slots(list): List of available appointment slots.
            attempt_number(int): Represents the number of times the user has failed to input valid details.
            is_skip_enabled(bool): Flag to enable or disable the skip option.
        """
        self.clear_screen()
        print(self.banner)
        available_slots = [slot for slot in slots if slot.get_availability()]
        print("""
                                                                    APPOINTMENT BOOKING PAGE
""")
        print("Available Appointment Slots:\n")
        self.display_instances(slots, instance_type="slot")
        if is_skip_enabled:
            return "filter"
        print("Enter the slot number to book the appointment.")
        if attempt_number > 0:
            self.show_error_message("standard")
        self.show_prompt(type = "logout")
        self.show_prompt(type = "back")
        self.show_prompt(type = "filter")
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
            return self.show_appointment_slots_page(slots, attempt_number=attempt_number+1)
    
    def show_booking_success_page(self, appointment):
        """
        Displays the booking success page with the appointment details.
        Args:
            appointment (object): The appointment object that was booked.
        """
        self.clear_screen()
        print(self.banner)
        print("\033[92m Your Appointment has been successfully booked! \033[0m")
        print(appointment)
        user_input = input("Press Enter to continue.. ")
        return user_input

    def show_cancellation_confirmation_page(self, appointment):
        """
        Displays the cancellation confirmation page with the appointment details.
        Args:
            appointment (object): The appointment object that was cancelled.
        """
        print("\033[91m You are about to cancel the following appointment:\033[0m")
        print(appointment)
        print("\nAre you sure you want to cancel this appointment? (CONFIRM/BACK/LOGOUT)")
        while True:
            user_input = input("Enter your choice: ").strip()
            if user_input in ["CONFIRM", "BACK","LOGOUT"]:
                return user_input
            else:
                print("\033[91m Invalid input. Please enter 'CONFIRM' or 'BACK' or 'LOGOUT'.\033[0m")

    def show_cancellation_success_page(self, appointment):
        """
        Displays the cancellation success page with the appointment details.
        Args:
            appointment (object): The appointment object that was cancelled.
        """
        print("\033[92m The appointment has been successfully cancelled! \033[0m")
        print(appointment)
        # input("\nPress Enter to continue...")
        user_input = input("Press Enter to continue.. ")
        return None

    def show_clinic_management_page(self, clinics, attempt_number = 0):
        """
        Displays the clinic management page with a list of clinics and options to create, update, or delete clinics.
        Args:
            clinics (list): List of clinic objects.
            attempt_number (int): Represents the number of times the user has failed to input valid details.
        """
        self.clear_screen()
        print(self.banner)
        print("""
                                                                            CLINIC DETAILS
        """)
        if len(clinics) == 0:
            print("\nYou have no clinic details to display.\n")
        else:
            print("\n--- List of All Clinics ---")
            print("------------------------------")
            for idx, clinic in enumerate(clinics, start=1):
                print(f"--- Clinic {idx} ---")
                print(f"clinic_name:        {clinic.get_clinic_name()}")
                print(f"Suburb:             {clinic.get_suburb()}")
                print(f"available_services: {', '.join(clinic.get_available_services())}")
                print(f"Operating Hours:    {clinic.get_operating_hours()}")
                print("-" * 50 + "\n")
        self.show_prompt(type = "logout")
        self.show_prompt(type = "back")
        self.show_prompt(type = "update")
        self.show_prompt(type = "create")
        self.show_prompt(type = "delete")
        if attempt_number > 0:
            self.show_error_message("standard")
        elif attempt_number == -1:
            print("\033[90m!!You have no clinics to update/delete!!\033[0m")
        user_input = input("Your Input: ").strip()
        if Validator.is_input_logout(user_input):
            return "logout"
        elif Validator.is_input_back(user_input):
            return "back"
        elif user_input == "UPDATE":
            if clinics:
                return "update"
            else:
                # No clinics to update
                attempt_number = -1
                return self.show_clinic_management_page(clinics, attempt_number)
        elif user_input == "CREATE":
            return "create"
        elif user_input == "DELETE":
            return "delete"
        else:
            return self.show_clinic_management_page(clinics, attempt_number=1)
        

    def show_create_appointment_slot_page(self, attempt_number = 0, user_input = None):
        """
        Displays the appointment slot creation page with sample slot details and prompts for user input.

        Args:
            attempt_number(int): Represents the number of times the user has failed to input valid details.
            user_input(str): A variable to pass the default user_input value.
        """
        self.clear_screen()
        print(self.banner)
        print(f"""
                                                                    APPOINTMENT SLOT CREATIION PAGE
clinic_name:        Mulgrave Clinic
gp_name:            Dr. Man
date:               17-07-2025
start_time:         23:34
duration:           15
clinic_suburb:      Mulgrave
reason_for_visit:   Specialist Referral
availability:       True
        """)
        print('Please enter \033[96m"CONTINUE"\033[0m to start creating OR \033[34m"BACK"\033[0m or \033[33m"LOGOUT"\033[0m to leave.')
        if attempt_number == 1:
            self.show_error_message("standard")
        if user_input is None:
            user_input = input("Your Input: ").strip()
        if Validator.is_input_back(user_input):
            return "back"
        elif Validator.is_input_logout(user_input):
            return "logout"
        elif Validator.is_input_continue(user_input):
            new_clinic_name = self.get_valid_input("New Clinic Name (Minimum of 3 characters): ", lambda x: len(x) > 3)
            if new_clinic_name in ["back", "logout"]:
                return new_clinic_name

            new_clinic_suburb = self.get_valid_input("New Clinic Suburb (Minimum of 3 characters): ", lambda x: len(x) > 3)
            if new_clinic_suburb in ["back", "logout"]:
                return new_clinic_suburb

            new_date = self.get_valid_input("New Date (dd-mm-yyyy format only. Cannot enter date from past): ",
                                            lambda x: Validator.is_valid_date_format(x, allow_past=False))
            if new_date in ["back", "logout"]:
                return new_date

            new_duration = self.get_valid_input("New Duration (Valid: 15, 20, 45, 60): ", Validator.is_valid_duration)
            if new_duration in ["back", "logout"]:
                return new_duration

            new_gp_name = self.get_valid_input("New GP Name (Enter 'Dr.' as prefix. Name cannot be empty): ",
                                            Validator.is_valid_gp_name)
            if new_gp_name in ["back", "logout"]:
                return new_gp_name

            new_reason_for_visit = self.get_valid_input(
                "New Reason for Visit (General Consultation, Vaccination, Specialist Referral): ",
                lambda x: x in ['General Consultation', 'Vaccination', 'Specialist Referral']
            )
            if new_reason_for_visit in ["back", "logout"]:
                return new_reason_for_visit

            new_start_time = self.get_valid_input("New Start Time (24hh:mm format only): ", Validator.is_valid_time_format)
            if new_start_time in ["back", "logout"]:
                return new_start_time

            new_availability = self.get_valid_input("New Availability (True/False only): ",
                                                    lambda x: x in ["True", "False"])
            if new_availability in ["back", "logout"]:
                return new_availability

            return {
                "availability": new_availability,
                "clinic_name": new_clinic_name,
                "clinic_suburb": new_clinic_suburb,
                "date": new_date,
                "duration": new_duration,
                "gp_name": new_gp_name,
                "reason_for_visit": new_reason_for_visit,
                "start_time": new_start_time,
            }
        else:
            return self.show_create_appointment_slot_page(attempt_number=1)
    
    
    def show_create_clinic_page(self, attempt_number = 0):
        """
        Displays the clinic creation page with sample clinic details and prompts for user input.
        
        Args:
            attempt_number(int): Represents the number of times the user has failed to input valid details.
        """
        self.clear_screen()
        print(self.banner)
        print(f"""
                                                                    CLINIC CREATIION PAGE
Sample Clinic Details:
clinic_name:        Mulgrave Clinic
suburb:             Mulgrave
available_services: General Consultation,Specialist Referral
operating_hours:    Tue-Fri 8AM-10PM
              
Please enter \033[96m"CONTINUE"\033[0m to start creating OR \033[34m"BACK"\033[0m or \033[33m"LOGOUT"\033[0m to leave.
        """)
        if attempt_number > 0:
            self.show_error_message("standard")
        user_input = input("Your Input: ").strip()
        if Validator.is_input_back(user_input):
            return "back"
        elif Validator.is_input_logout(user_input):
            return "logout"
        elif Validator.is_input_continue(user_input):
            is_input_valid = True
            while True:
                if not is_input_valid:
                    print("\033[91m!! Input cannot be Blank !!\033[0m")
                new_name = input(f"New Name (Mulgrave Clinic): ").strip()
                if new_name == "":
                    is_input_valid = False
                    continue
                new_suburb = input(f"New Suburb (Mulgrave): ").strip()
                if new_suburb == "":
                    is_input_valid = False
                    continue
                new_services = input(f"New Services (comma-separated) (General Consultation,Specialist Referral): ").strip()
                if new_services == "":
                    is_input_valid = False
                    continue
                new_services = new_services.split(',')
                new_hours = input(f"New Operating Hours (Tue-Fri 8AM-10PM): ").strip()
                if new_hours == "":
                    is_input_valid = False
                    continue
                break
        else:
            return self.show_create_clinic_page(attempt_number+1)
        new_clinic_details = {}
        new_clinic_details["clinic_name"] = new_name
        new_clinic_details["suburb"] = new_suburb
        new_clinic_details["available_services"] = new_services
        new_clinic_details["operating_hours"] = new_hours
        return new_clinic_details
    

    def show_create_gp_page(self,clinic_list, attempt_number = 0):
        """
        Displays the GP creation page with sample GP details and prompts for user input.
        Args:
            clinic_list (list): List of available clinics.
            attempt_number (int): Represents the number of times the user has failed to input valid details.
        """
        self.clear_screen()
        print(self.banner)
        print(f"""
                                                                    GP CREATIION PAGE
Sample GP Details:
gp_name: Dr.David
email: anbuchandran06@gmail.com
assigned_clinics: kerala hospital,melb hospital,syd hospital
specialisation: Vaccinations
availability: Mon-Fri 6AM-7AM
              
              
Please enter \033[96m"CONTINUE"\033[0m to start creating OR \033[34m"BACK"\033[0m or \033[33m"LOGOUT"\033[0m to leave.
        """)


        print("Available Clinics: ", clinic_list)

        if attempt_number > 0:
            self.show_error_message("standard")
        user_input = input("Your Input: ").strip()
        if Validator.is_input_back(user_input):
            return "back"
        elif Validator.is_input_logout(user_input):
            return "logout"
        elif Validator.is_input_continue(user_input):
            is_input_valid = True
            while True:
                if not is_input_valid:
                    print("\033[91m!! Input cannot be Blank !!\033[0m")
                new_name = input(f"New GP Name (Dr.David): ").strip()
                if new_name == "":
                    is_input_valid = False
                    continue

                while True:

                    new_email = input(f"New email-id (david1@monash.gp.in): ").strip()
                    if new_email == "":
                        is_input_valid = False
                        continue

                    if re.match(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$', new_email):
                        break
                    else:
                        print("\033[91m!! Invalid Email id Format. Please enter a valid id. !!\033[0m") 
                        continue

                new_assigned_clinics = input(f"New Clinics (comma-separated) (Clayton Hospital,Glen Waverley Hospital): ").strip()
                if new_assigned_clinics == "":
                    is_input_valid = False
                    continue
                new_assigned_clinics = [clinic.strip() for clinic in new_assigned_clinics.split(',')]

                is_valid, valid_clinics, invalid_clinics = Validator.is_valid_clinic_list(
                    new_assigned_clinics, clinic_list
                )

                if not is_valid:
                    print(f"\033[91m!! These clinics are not valid: {', '.join(invalid_clinics)} !!\033[0m")
                    continue
                    
            
                new_specialisation = input(f"New specialisation (comma-separated) (Vaccinations,General Consultation): ").strip()
                if new_specialisation == "":
                    is_input_valid = False
                    continue
                new_specialisation = new_specialisation.split(',')
                new_availability = input(f"New availability of the GP (Tue-Fri 8AM-10PM): ").strip()
                if new_availability == "":
                    is_input_valid = False
                    continue
                break
        else:
            return self.show_create_gp_page(attempt_number+1)

        new_gp_details = {}
        new_gp_details["gp_name"] = new_name
        new_gp_details["email"] = new_email
        new_gp_details["assigned_clinics"] = valid_clinics
        new_gp_details["specialisation"] = new_specialisation
        new_gp_details["availability"] = new_availability
        return new_gp_details

    def show_creation_success_page(self, type, instance_variable):
        """
        Displays the creation success page with the details of the created instance.
        Args:
            type (str): The type of instance created (Clinic or GP).
            instance_variable (object): The instance object that was created.
        """
        self.clear_screen()
        print(self.banner)
        print(f"""
                                                                    {type.upper()} CREATIION SUCCESSFULL
"\n\033[92m The {type} has been created successfully!\033[0m
{str(instance_variable)[:-2]}
        """)
        input("Please Enter to continue.. ")
        return None
    

    def show_delete_appointment_slot_page(self, slots, attempt_number=0):
        """
        Displays the Appointment Slot deletion page with a list of slots and prompts for user input to delete a slot.
        Args:
            slots(list): List of AppointmentSlot instances.
            attempt_number(int): Represents the number of times the user has failed to input valid details.
        """
        self.clear_screen()
        print(self.banner)
        print(f"""
                                                                            APPOINTMENT SLOT DELETTION PAGE
        """)
        if len(slots) == 0:
            print("\nYou have no slots to display.\n")
        else:
            print("\n--- List of All Appointment Slots ---")
            print("-" * 50)
            for i, slot in enumerate(slots, start=1):
                print(f"Slot {i}:")
                print(f"  Clinic: {slot.get_clinic_name()}")
                print(f"  GP: {slot.get_gp_name()}")
                print(f"  Date: {slot.get_date()}")
                print(f"  Time: {slot.get_start_time()}")
                print(f"  Duration: {slot.get_duration()}")
                print(f"  Suburb: {slot.get_clinic_suburb()}")
                print(f"  Reason: {slot.get_reason_for_visit()}")
                print("-" * 50)
        print("Please enter the number to choose the Appointment Slot for deletion.")
        self.show_prompt(type = "logout")
        self.show_prompt(type = "back")
        if attempt_number > 0:
            self.show_error_message("standard")
        elif attempt_number == -1:
            print("\033[90m!!You have no slots to delete!!\033[0m")
        user_input = input("Your Input: ").strip()
        if Validator.is_input_logout(user_input):
            return "logout"
        elif Validator.is_input_back(user_input):
            return "back"
        elif user_input.isdigit():
            if slots:
                slot_index = int(user_input) - 1
                if 0 <= slot_index < len(slots):
                    user_input = input("Are You Sure? This Action Is Permanent (yes/no):  ")
                    if user_input == "yes":
                        slot = slots[slot_index]
                        return slot
                    elif user_input == "no":
                        print("\033[91m!!Deletion of Appointment Slot Aborted!!\033[0m")
                        input("Press Enter to continue.. ")
                        return self.show_delete_appointment_slot_page(slots)
                    else:
                        print("\033[91m!! Invalid input. Appointment Slot Deletion Aborted!!\033[0m")
                        input("Press Enter to continue.. ")
                        return self.show_delete_appointment_slot_page(slots)
                else:
                    print("\033[91m!! Invalid selection. Please try again!!\033[0m")
                    input("Press Enter to continue.. ")
                    return self.show_delete_appointment_slot_page(slots)
            else:
                # No Appointment Slots to delete
                attempt_number = -1
                return self.show_appointment_slot_management_page(slots, attempt_number)
        else:
            return self.show_delete_appointment_slot_page(slots, attempt_number=1)
    

    def show_delete_clinic_page(self, clinics, attempt_number=0):
        """
        Displays the clinic deletion page with a list of clinics and prompts for user input to delete a clinic.
        Args:
            clinics(list): List of clinic objects.
            attempt_number(int): Represents the number of times the user has failed to input valid details.
        """
        self.clear_screen()
        print(self.banner)
        print(f"""
                                                                            CLINIC DELETTION PAGE
        """)
        if len(clinics) == 0:
            print("\nYou have no clinic details to display.\n")
        else:
            print("\n--- List of All Clinics ---")
            print("------------------------------")
            for idx, clinic in enumerate(clinics, start=1):
                print(f"--- Clinic {idx} ---")
                print(f"clinic_name:        {clinic.get_clinic_name()}")
                print(f"Suburb:             {clinic.get_suburb()}")
                print(f"available_services: {', '.join(clinic.get_available_services())}")
                print(f"Operating Hours:    {clinic.get_operating_hours()}")
                print("-" * 50 + "\n")
        print("Please enter the number to choose the clinic for deletion.")
        self.show_prompt(type = "logout")
        self.show_prompt(type = "back")
        if attempt_number > 0:
            self.show_error_message("standard")
        elif attempt_number == -1:
            print("\033[90m!!You have no clinics to delete!!\033[0m")
        user_input = input("Your Input: ").strip()
        if Validator.is_input_logout(user_input):
            return "logout"
        elif Validator.is_input_back(user_input):
            return "back"
        elif user_input.isdigit():
            if clinics:
                clinic_index = int(user_input) - 1
                if 0 <= clinic_index < len(clinics):
                    user_input = input("Are You Sure? This Action Is Permanent (yes/no):  ")
                    if user_input == "yes":
                        return clinic_index
                    elif user_input == "no":
                        print("\033[91m!!Deletion of Clinic Aborted!!\033[0m")
                        input("Press Enter to continue.. ")
                        return self.show_delete_clinic_page(clinics)
                    else:
                        print("\033[91m!! Invalid input. Clinic Deletion Aborted!!\033[0m")
                        input("Press Enter to continue.. ")
                        return self.show_delete_clinic_page(clinics)
                else:
                    print("\033[91m!! Invalid selection. Please try again!!\033[0m")
                    input("Press Enter to continue.. ")
                    return self.show_delete_clinic_page(clinics)
            else:
                # No clinics to update
                attempt_number = -1
                return self.show_clinic_management_page(clinics, attempt_number)
        else:
            return self.show_clinic_management_page(clinics, attempt_number=1)
        

    def show_delete_gp_page(self, gps, attempt_number=0):
        """
        Displays the GP deletion page with a list of GPs and prompts for user input to delete a GP.
        Args:
            gps (list): List of GP objects.
            attempt_number (int): Represents the number of times the user has failed to input valid details.
        """
        self.clear_screen()
        print(self.banner)
        print(f"""
                                                                            GP DELETTION PAGE
        """)
        if len(gps) == 0:
            print("\nYou have no GP details to display.\n")
        else:
            print("\n--- List of All GPs ---")
            print("------------------------------")
            for idx, gp in enumerate(gps, start=1):
                print(f"--- GP {idx} ---")
                print(f"gp_name:        {gp.get_gp_name()}")
                print(f"email:             {gp.get_email()}")
                print(f"assigned_clinics: {', '.join(gp.get_assigned_clinics())}")
                print(f"specialisation: {', '.join(gp.get_specialisation())}")
                print(f"availability:    {gp.get_availability()}")
                print("-" * 50 + "\n")
        print("Please enter the number to choose the gp for deletion.")
        self.show_prompt(type = "logout")
        self.show_prompt(type = "back")
        if attempt_number > 0:
            self.show_error_message("standard")
        elif attempt_number == -1:
            print("\033[90m!!You have no GPs to delete!!\033[0m")
        user_input = input("Your Input: ").strip()
        if Validator.is_input_logout(user_input):
            return "logout"
        elif Validator.is_input_back(user_input):
            return "back"
        elif user_input.isdigit():
            if gps:
                gp_index = int(user_input) - 1
                if 0 <= gp_index < len(gps):
                    user_input = input("Are You Sure? This Action Is Permanent (yes/no):  ")
                    if user_input == "yes":
                        return gp_index
                    elif user_input == "no":
                        print("\033[91m!!Deletion of GP Aborted!!\033[0m")
                        input("Press Enter to continue.. ")
                        return self.show_delete_gp_page(gps)
                    else:
                        print("\033[91m!! Invalid input. GP Deletion Aborted!!\033[0m")
                        input("Press Enter to continue.. ")
                        return self.show_delete_gp_page(gps)
                else:
                    print("\033[91m!! Invalid selection. Please try again!!\033[0m")
                    input("Press Enter to continue.. ")
                    return self.show_delete_gp_page(gps)
            else:
                # No gps to update
                attempt_number = -1
                return self.show_gp_management_page(gps, attempt_number)
        else:
            return self.show_gp_management_page(gps, attempt_number=1)

    
    def show_deletion_confirmation_page(self, type, instance_variable):
        '''
        Args:
            type(str): Can be either "Clinic" or "Gp"
        '''
        self.clear_screen()
        print(self.banner)
        print(f"""
                                                                    {type.upper()} DELETION SUCCESSFULL
"\n\033[92m The {type} has been deleted successfully!\033[0m
{str(instance_variable)[:-2]}
        """)
        input("Please Enter to continue.. ")
        return None
        
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

    def show_export_success_page(self, report_data):
        """
        Displays the export success page with the report data.
        Args:
            report_data (str): The report data that was exported.
        """
        self.clear_screen()
        print(self.banner)
        print("\n\033[92m The report has been successfully exported! \033[0m")
        print(report_data)
        # input("\nPress Enter to continue...")
        user_input = input("Press Enter to go to Report Generation Page.. ")
        return None

    def show_filter_options(self, is_skip_enabled = False):
        """
        Displays the filter options for appointment slots.
        Args:
            is_skip_enabled (bool): Flag to enable or disable the skip option.
        """
        print("""
FILTER APPOINTMENT SLOTS

    You can filter by:
    1. Date
    2. GP Name
    3. Clinic Suburb

    Enter the option number or \033[34m"BACK"\033[0m/\033[33m"LOGOUT"\033[0m to return.
        """)
        if is_skip_enabled:
            self.show_error_message("standard")
        user_input = input("Your Input: ").strip()
        if Validator.is_input_back(user_input):
            return "back"
        elif Validator.is_input_logout(user_input):
            return "logout"
        elif user_input == "1":
            return "date"
        elif user_input == "2":
            return "gp_name"
        elif user_input == "3":
            return "clinic_suburb"
        else:
            return "error"
    

    def show_gp_appointment_slots(self, slots, gp_name, attempt_number = 0):
        '''
        Shows a specific GP's Appointment slots

        Args:
            slots(list): List of AppointmentSlot instances that are associated with the GP
            attempt_number(int): Represents the number of times the user has failed to input valid details.
        '''
        self.clear_screen()
        print(self.banner)
        print("""
                                                                    GP's APPOINTMENT SLOTS PAGE
""")
        print(f"Available Appointment Slots for {gp_name}\n")
        self.display_instances(slots, instance_type="slot")
        if attempt_number > 0:
            self.show_error_message("standard")
        self.show_prompt(type = "logout")
        self.show_prompt(type = "back")
        print('''Enter \033[96m"FILTER"\033[0m to filter appointment slots by Clinic Suburb\n''')
        user_input = input("Your Input: ").strip()
        if Validator.is_input_logout(user_input):
            return "logout"
        elif Validator.is_input_back(user_input):
            return "back"
        elif Validator.is_input_filter(user_input):
            return "filter"
        else:
            return self.show_appointment_slots_page(slots, attempt_number=attempt_number+1)
        

    def show_gp_management_page(self, gps, attempt_number = 0):
        """
        Displays the GP management page with a list of GPs and options to create, update, or delete GPs.
        
        Args:
            gps(list): List of GP objects.
            attempt_number(int): Represents the number of times the user has failed to input valid details.
        """
        self.clear_screen()
        print(self.banner)
        print("""
                                                                            GP DETAILS
        """)
        if len(gps) == 0:
            print("\nYou have no gp details to display.\n")
        else:
            print("\n--- List of All GPs ---")
            print("------------------------------")
            for idx, gp in enumerate(gps, start=1):
                print(f"--- GP {idx} ---")
                print(f"gp_name:        {gp.get_gp_name()}")
                print(f"email:             {gp.get_email()}")
                print(f"assigned_clinics: {', '.join(gp.get_assigned_clinics())}")
                print(f"specialisation: {', '.join(gp.get_specialisation())}")
                print(f"availability:    {gp.get_availability()}")
                print("-" * 50 + "\n")
        self.show_prompt(type = "logout")
        self.show_prompt(type = "back")
        self.show_prompt(type = "update")
        self.show_prompt(type = "create")
        self.show_prompt(type = "delete")
        print('''Enter \033[96m"SLOTS"\033[0m to view GP's appointment slots\n''')
        if attempt_number > 0:
            self.show_error_message("standard")
        elif attempt_number == -1:
            print("\033[90m!!You have no gps to update/delete!!\033[0m")
        user_input = input("Your Input: ").strip()
        if Validator.is_input_logout(user_input):
            return "logout"
        elif Validator.is_input_back(user_input):
            return "back"
        elif user_input == "UPDATE" or user_input == "SLOTS":
            if gps and user_input == "UPDATE":
                return "update"
            elif gps and user_input == "SLOTS":
                return "slots"
            else:
                # No gps to update
                attempt_number = -1
                return self.show_gp_management_page(gps, attempt_number)
        elif user_input == "CREATE":
            return "create"
        elif user_input == "DELETE":
            return "delete"
        else:
            return self.show_gp_management_page(gps, attempt_number=1)


    def show_login_page(self, valid_patient_details, valid_admin_details, attempt_number = 0):
        """
        Displays the Login Page and an Error message based on user attempt number.

        Args:
            valid_patient_details(dict): 
            valid_admin_details(dict):
            attempt_number(int): Represents the number of times the user has failed to input valid details.
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
        is_login_valid = Validator.is_valid_patient_login(valid_patient_details, email, password)
        if is_login_valid:
            return "patient_home_page",email
        else:
            is_login_valid = Validator.is_valid_admin_login(valid_admin_details, email, password)
            if is_login_valid:
                return "admin_home_page",email
            else: # Invalid details
                return self.show_login_page(valid_patient_details, valid_admin_details, attempt_number+1)

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
        self.show_prompt(type = "logout")
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
    
    def show_previous_appointments_page(self, appointments, attempt_number = 0):
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
                print(f"  Clinic: {appt.get_slot().get_clinic_name()}")
                print(f"  GP: {appt.get_slot().get_gp_name()}")
                print(f"  Date: {appt.get_slot().get_date()}")
                print(f"  Time: {appt.get_slot().get_start_time()}")
                print(f"  Duration: {appt.get_slot().get_duration()} minutes")
                print(f"  Suburb: {appt.get_slot().get_clinic_suburb()}")
                print(f"  Reason: {appt.get_slot().get_reason_for_visit()}")
                print(f"  Status: {appt.get_status()}")
                print("-" * 50)
        if attempt_number > 0:
            self.show_error_message("standard")
        self.show_prompt(type = "logout")
        self.show_prompt(type = "back")
        user_input = input("Your Input: ").strip()
        if Validator.is_input_logout(user_input):
            return "logout"
        elif Validator.is_input_back(user_input):
            return "back"
        else:
            return self.show_previous_appointments_page(appointments, attempt_number+1)

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
        self.show_prompt(type = "logout")
        self.show_prompt(type = "back")
        user_input = input("Your Input: ").strip()
        if Validator.is_input_logout(user_input):
            return "logout"
        elif Validator.is_input_back(user_input):
            print("trying to go back")
            return "back"
        else:
            return self.show_profile_page(attempt_number+1, user_obj, is_user_admin)

    def show_prompt(self, type):
        """
        Displays the standard prompt to inform the user that they can/cannot enter a certain Prompt as input on this screen.
        Args:
            type (str): The type of prompt to display.
        """
        if type == "back" : print('''Enter \033[34m"BACK"\033[0m to go back to previous page\n''')
        elif type == "logout" : print('''Enter \033[33m"LOGOUT"\033[0m to go back to Login Page\n''')
        elif type == "filter" : print('''Enter \033[96m"FILTER"\033[0m to filter appointment slots\n''')
        elif type == "cancel" : print('''Enter \033[96m"CANCEL"\033[0m to cancel the Appointment\n''')
        elif type == "update" : print('''Enter \033[96m"UPDATE"\033[0m to update the details\n''')
        elif type == "create" : print('''Enter \033[96m"CREATE"\033[0m to create a new entry\n''')
        elif type == "delete" : print('''Enter \033[90m"DELETE"\033[0m to delete an entry\n''')
    
    def get_report_date_range(self, attempt_number = 0):
        """
        Displays the report date range selection page and returns the selected date range.
        Args:
            attempt_number (int): Represents the number of times the user has failed to input valid details.
        """
        self.clear_screen()
        print(self.banner)
        print("""
                                                        SELECT REPORT DATE RANGE
        """)
        print("""
        1. Daily (Today)
        2. Weekly (Last 7 days)
        3. Monthly (Last 30 days)
        4. Custom range
        5. All time
        """)
        
        today = datetime.now()
        if attempt_number > 0:
            self.show_error_message("standard")
        self.show_prompt(type = "logout")
        self.show_prompt(type = "back")
        user_input = input("Your Input: ").strip()
        if Validator.is_input_logout(user_input):
            return "logout"
        elif Validator.is_input_back(user_input):
            return "back"
        elif user_input == "1":
            # Daily - just today
            start_date = today.strftime("%d-%m-%Y")
            end_date = start_date
            return start_date, end_date
        elif user_input == "2":
            # Weekly - last 7 days
            start_date = (today - timedelta(days=6)).strftime("%d-%m-%Y")
            end_date = today.strftime("%d-%m-%Y")
            return start_date, end_date
        elif user_input == "3":
            # Monthly - last 30 days
            start_date = (today - timedelta(days=29)).strftime("%d-%m-%Y")
            end_date = today.strftime("%d-%m-%Y")
            return start_date, end_date
        elif user_input == "4":
            # Custom range
            print("\nEnter date in DD-MM-YYYY format")
            while True:
                start_date = input("Start date: ").strip()
                if Validator.is_valid_date_format(start_date):
                    break
                print("\033[91mInvalid date format. Please use DD-MM-YYYY.\033[0m")
            
            while True:
                end_date = input("End date: ").strip()
                if Validator.is_valid_date_format(end_date):
                    break
                print("\033[91mInvalid date format. Please use DD-MM-YYYY.\033[0m")
            
            return start_date, end_date
        elif user_input == "5":
            # All time
            return None, None
        else:
            return self.get_report_date_range(attempt_number = 1)


    def paginate_items(self, items, page_size=10, current_page=1):
        """
        Paginate a list of items.
        Args:
            items (list): List of items to paginate.
            page_size (int): Number of items per page.
            current_page (int): Current page number.
        Returns:
            dict: A dictionary containing paginated items and pagination information.
        """
    
        total_items = len(items)
        total_pages = max(1, (total_items + page_size - 1) // page_size)  # Ceiling division
        
        # Ensure current_page is within valid range
        current_page = max(1, min(current_page, total_pages))
        
        # Calculate start and end indices
        start_index = (current_page - 1) * page_size
        end_index = min(start_index + page_size, total_items)
        
        # Get items for the current page
        current_items = items[start_index:end_index]
        
        return {
            "items": current_items,
            "total_pages": total_pages,
            "current_page": current_page,
            "has_next": current_page < total_pages,
            "has_prev": current_page > 1,
            "total_items": total_items,
            "showing_from": start_index + 1 if total_items > 0 else 0,
            "showing_to": end_index
        }


    def show_report_export_page(self, report_data, attempt_number = 0):
        """
        Displays the report export page with options to export the report in different formats.
        Args:
            report_data (str): The report data to be exported.
            attempt_number (int): Represents the number of times the user has failed to input valid details.
        """
        self.clear_screen()
        print(self.banner)
        print(f'''
                                                                     EXPORT REPORT PAGE

Your generated report:
{report_data}

--------------------------------
Please Choose the Export Format
1. Export as Text File \033[96m(.txt)\033[0m
2. Export as Comma Seperated Values File \033[96m(.csv)\033[0m

''')

        if attempt_number > 0:
            self.show_error_message("standard")
        print("Enter the Option Number to export in desired format\n")
        self.show_prompt(type = "logout")
        self.show_prompt(type = "back")
        user_input = input("Your Input: ").strip()
        if Validator.is_input_logout(user_input):
            return "logout"
        elif Validator.is_input_back(user_input):
            return "back"
        elif user_input == "1":
            return "txt"
        elif user_input == "2":
            return "csv"
        else:
            return self.show_report_export_page(report_data, attempt_number+1)
        

    def show_update_success_page(self, type , instance_variable):
        """
        Displays the update success page with the details of the updated instance.
        Args:
            type (str): The type of instance updated (Clinic, GP or Slot).
            instance_variable (object): The instance object that was updated.
        """
        self.clear_screen()
        print(self.banner)
        if type == "clinic":
            print(f"\n\033[92mClinic updated successfully.\033[0m\n")
        elif type == "gp":
            print(f"\n\033[92mGP updated successfully.\033[0m\n")
        elif type == "slot":
            print(f"\n\033[92mAppointment Slot updated successfully.\033[0m\n")
        print(str(instance_variable)[:-2]) # [:-2] to perform some formatting of the output
        input("\nPress  Enter to continue.. ")      
        return None
        
    def show_upcoming_appointments_page(self, appointments,page=1, page_size=10, attempt_number = 0):
        """
        Displays the upcoming appointments page with a list of upcoming appointments.
        
        Args:
            appointments (list): List of past Appointment objects
            page (int): The current page number for pagination.
            page_size (int): The number of items to display per page.
            attempt_number (int): Represents the number of times the user has failed to input valid details.
        """
        self.clear_screen()
        print(self.banner)
        print("""
                                                                            UPCOMING APPOINTMENTS
        """)

        # Paginate the appointments
        pagination = self.paginate_items(appointments, page_size, page)
        current_appointments = pagination["items"]
    
        # Display pagination information
        print(f"\nShowing {pagination['showing_from']}-{pagination['showing_to']} of {pagination['total_items']} appointments (Page {pagination['current_page']} of {pagination['total_pages']})\n")

        if not appointments:
            print("\n\033[92mYou have no upcoming appointments to display.\033[0m\n")
        else:
            print("\nYour Upcoming Appointments:\n")
            for i, appt in enumerate(current_appointments, start=1):
                actual_index = pagination['showing_from'] - 1 + i
                print(f"Appointment {actual_index}:")
                print(f"  GP: {appt.slot.gp_name}")
                print(f"  Date: {appt.slot.date}")
                print(f"  Time: {appt.slot.start_time}")
                print(f"  Suburb: {appt.slot.clinic_suburb}")
                print("-" * 50)
        
        # Show pagination navigation options
        print("\nNavigation options:")
        if pagination["has_prev"]:
            print("P - Previous page")
        if pagination["has_next"]:
            print("N - Next page")

        print("Enter appointment number to see full details\n")
        self.show_prompt(type = "logout")
        self.show_prompt(type = "back")
        self.show_prompt(type = "cancel")
        if attempt_number > 0:
            self.show_error_message("standard")
        elif attempt_number == -1:
            print("\033[90m!!You have no appointments to cancel!!\033[0m")
        
        user_input = input("Your Input: ").strip()
        
        if Validator.is_input_logout(user_input):
            return "logout"
        elif Validator.is_input_back(user_input):
            print("trying to go back")
            return "back"
        elif user_input.lower() == "p" and pagination["has_prev"]:
            return self.show_upcoming_appointments_page(appointments, page-1, page_size)
        elif user_input.lower() == "n" and pagination["has_next"]:
            return self.show_upcoming_appointments_page(appointments, page+1, page_size)
        elif user_input == "CANCEL":
            if appointments:
                return "cancel"
            else:
                return self.show_upcoming_appointments_page(appointments, page, page_size, -1)
        elif user_input.isdigit():
            appointment_num = int(user_input) - 1
            selected_appointment = appointment_num
            if selected_appointment is not None and 0 <= selected_appointment < len(appointments):
                self.clear_screen()
                print(self.banner)
                print("""
                                                                            APPOINTMENT DETAILS
                """)
                appt = appointments[selected_appointment]
                print(f"\nAppointment {selected_appointment + 1} Details:")
                print(appt)
                input("Press Enter to return to appointment list.. ")
                return self.show_upcoming_appointments_page(appointments,page, page_size, attempt_number=0)
            else:
                return self.show_upcoming_appointments_page(appointments, page, page_size, attempt_number=1)
        else:
            return self.show_upcoming_appointments_page(appointments, page, page_size, attempt_number=1)
    
    def show_view_report_page(self, report_data, attempt_number = 0):
        """
        Displays the view report page with the generated report data.
        Args:
            report_data (str): The generated report data to be displayed.
            attempt_number (int): Represents the number of times the user has failed to input valid details.
        """
        self.clear_screen()
        print(self.banner)
        print(f'''
                                                                     VIEW REPORT PAGE''')
        print(report_data)

        if attempt_number > 0:
            self.show_error_message("standard")
        self.show_prompt(type = "logout")
        self.show_prompt(type = "back")
        print('''Enter \033[96m"EXPORT"\033[0m to export the generated report\n''')
        user_input = input("Your Input: ").strip()
        if Validator.is_input_logout(user_input):
            return "logout"
        elif Validator.is_input_back(user_input):
            return "back"
        elif Validator.is_input_export(user_input):
            return "export"
        else:
            return self.show_view_report_page(report_data, attempt_number+1)
  