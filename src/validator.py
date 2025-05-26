from datetime import datetime, timedelta
import re
class Validator:
    def __init__(self):
        pass

    @staticmethod
    def is_booking_valid(slot):
        """
        Check if the booking slot is valid.
        :param slot: AppointmentSlot object
        :return: True if the slot is valid, False otherwise
        """
        # Check if the slot is available and if the time is at least 2 hours in the future
        try:
            slot_time = datetime.strptime(f"{slot.get_date()} {slot.get_start_time()}", "%d-%m-%Y %H:%M")
            return slot.get_availability() and slot_time > datetime.now() + timedelta(hours=2)
        except ValueError as e:
            print(f"[DEBUG] Invalid slot: {slot.get_date()} {slot.get_start_time()} - {e}")
            return False

   
    @staticmethod
    def is_input_back(user_input):
        """
        Check if the user input is "BACK".
        :param user_input: Input string from the user
        :return: True if the input is "BACK", False otherwise
        """
        if user_input == "BACK":
            return True
        return False
    
    @staticmethod
    def is_input_continue(user_input):
        """
        Check if the user input is "CONTINUE".
        :param user_input: Input string from the user
        :return: True if the input is "CONTINUE", False otherwise
        """
        if user_input == "CONTINUE":
            return True
        return False
    
    @staticmethod
    def is_input_exit(user_input):
        """
        Check if the user input is "EXIT".
        :param user_input: Input string from the user
        :return: True if the input is "EXIT", False otherwise
        """
        if user_input == "EXIT":
            return True
        return False
    
    @staticmethod
    def is_input_export(user_input):
        """
        Check if the user input is "EXPORT".
        :param user_input: Input string from the user
        :return: True if the input is "EXPORT", False otherwise
        """
        if user_input == "EXPORT":
            return True
        return False
    
    @staticmethod
    def is_input_logout(user_input):
        """
        Check if the user input is "LOGOUT".
        :param user_input: Input string from the user
        :return: True if the input is "LOGOUT", False otherwise
        """
        if user_input == "LOGOUT":
            return True
        return False
    
    @staticmethod
    def is_input_filter(user_input):
        """
        Check if the user input is "FILTER".
        :param user_input: Input string from the user
        :return: True if the input is "FILTER", False otherwise
        """
        if user_input == "FILTER":
            return True
        return False

   
    @staticmethod
    def is_valid_admin_login(valid_admin_details, input_email, input_password):
        """
        Check if the admin login credentials are valid.
        :param valid_admin_details: Dictionary of valid admin details with email as key and password as value
        :param input_email: Input email from the user
        :param input_password: Input password from the user
        :return: True if the credentials are valid, False otherwise
        """
        if input_email in valid_admin_details:
            if input_password == valid_admin_details[input_email]:
                return True
        return False

    @staticmethod
    def is_valid_availability_gp(availability_str):
        """
        Validates GP availability contains valid days of the week.
        
        Args:
            availability_str (str): Availability string to validate
            
        Returns:
            bool: True if valid format, False otherwise
        """
        if not availability_str or availability_str.strip() == "":
            print("\033[91m!! Availability cannot be empty !!\033[0m")
            return False
        
        availability = availability_str.strip()
        
        # Valid day abbreviations and full names
        valid_days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun',
                    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        # Check if it contains at least one valid day
        has_valid_day = any(day in availability for day in valid_days)
        if not has_valid_day:
            print("\033[91m!! Availability must include valid days (Mon, Tue, Wed, Thu, Fri, Sat, Sun) !!\033[0m")
            return False
        
        # Check minimum length (at least 3 characters for shortest day "Mon")
        if len(availability) < 3:
            print("\033[91m!! Availability too short. Please include day(s) of the week !!\033[0m")
            return False
        
        return True
    
    @staticmethod
    def is_valid_clinic_list(assigned_clinics, available_clinics):
        """
        Check if the assigned clinics are valid by comparing them with the available clinics.
        :param assigned_clinics: List of assigned clinics
        :param available_clinics: List of available clinics
        :return: Tuple (is_valid, valid_clinics, invalid_clinics)
        """
        # Check if the assigned clinics are in the list of available clinics
        valid_clinics = [clinic.strip() for clinic in assigned_clinics if clinic.strip() in available_clinics]
        invalid_clinics = [clinic.strip() for clinic in assigned_clinics if clinic.strip() not in available_clinics]
        return len(invalid_clinics) == 0, valid_clinics, invalid_clinics
    

    @staticmethod
    def is_valid_date_format(date_str, allow_past = True):
        """
        Check if the date string is in the format "dd-mm-yyyy".
        :param date_str: Date string to check
        :param allow_past: Boolean flag value that decides if past date is valid or not
        :return: True if the date string is valid, False otherwise
        """
        # Check if the date string is in the format "dd-mm-yyyy" and if it is a valid date.
        try:
            datetime.strptime(date_str, "%d-%m-%Y")
            if allow_past == False and datetime.strptime(date_str, "%d-%m-%Y") < datetime.now():
                return False
            return True
        except ValueError:
            return False
        

    @staticmethod
    def is_valid_duration(duration):
        '''
        Check if the duration is an allowed value
        Args:
            duration(str): duration value.
        '''
        # Check if the duration is one of the allowed values
        if duration in ["15", "25", "45", "60"]:
            return True
        return False
    
    @staticmethod
    def is_valid_email(email, email_list = None):
        '''
        Check if the email entered is valid or not, and not already existing.
        Args:
            email(str)
            email_list(list)
        '''
        if email_list != None:
            if re.match(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$', email) is not None and email not in email_list:
                return True
        else:
            if re.match(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$', email) is not None:
                return True
        return False
    
    @staticmethod
    def is_valid_gp_name(name, gp_list = None):
        '''
        Check if the entered name has "Dr." as a prefix or not and if there is a name after the title.
        Args:
            name(str): name of gp
        '''
        if gp_list is None:
        # Check if the name starts with "Dr." and has more than 3 characters (to ensure there's a name after the title)
            if name[:3] == "Dr." and len(name) > 3:
                return True
        elif gp_list is not None:
            if name[:3] == "Dr." and len(name) > 3 and name not in gp_list:
                return True
        return False
    

    @staticmethod
    def is_valid_operating_hours_clinic(hours_str):
        """
        Validation for operating hours format.

        Args:
            hours_str (str): Operating hours string to validate
            
        Returns:
            bool: True if valid format, False otherwise
        """
        if not hours_str or hours_str.strip() == "":
            print("\033[91m!! Operating hours cannot be empty !!\033[0m")
            return False
        
        hours = hours_str.strip()
        
        # Pattern for time format: HH:MM - HH:MM
        time_pattern = r'\d{1,2}:\d{2}\s*-\s*\d{1,2}:\d{2}'
        
        if re.search(time_pattern, hours):
            return True
        else:
            print("\033[91m!! Invalid format. Use: '00:00 - 24:00' format !!\033[0m")
            return False


    @staticmethod
    def is_valid_patient_login(valid_patient_details, input_email, input_password):
        """
        Check if the patient login credentials are valid.
        :param valid_patient_details: Dictionary of valid patient details with email as key and password as value
        :param input_email: Input email from the user
        :param input_password: Input password from the user
        :return: True if the credentials are valid, False otherwise
        """
        # Check if the input email exists in the valid patient details
        # and if the input password matches the stored password for that email.
        if input_email in valid_patient_details:
            if input_password == valid_patient_details[input_email]:
                return True
        return False
        
    @staticmethod
    def is_valid_services(services_input):
        """
        Validates the services input string with flexible service names.
        
        Args:
            services_input (str): Comma-separated services string
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not services_input or services_input.strip() == "":
            return False
        
        # Split by comma and check each service
        services = [service.strip() for service in services_input.split(',')]
        
        # Check if we have at least one non-empty service
        valid_services = [service for service in services if service and len(service) >= 3]
        
        if len(valid_services) == 0:
            print("\033[91m!! Please provide at least one service with minimum 3 characters !!\033[0m")
            return False
        
        # Check for reasonable service name length
        for service in valid_services:
            if len(service) > 50:
                print(f"\033[91m!! Service name too long: '{service}' (max 50 characters) !!\033[0m")
                return False
        
        return True
    
    
    @staticmethod
    def is_valid_time_format(time_string):
        '''
        Check if the time_string is the acceptable 24hrs time format.
        Args:
            time_string(str): time value
        '''
        try:
            datetime.strptime(time_string, "%H:%M")
            return True
        except:
            return False
