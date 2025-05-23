from datetime import datetime, timedelta
class Validator:
    def __init__(self):
        pass

    @staticmethod
    def is_booking_valid(slot):
        #print(slot)
        """
        Check if the booking slot is valid.
        :param slot: AppointmentSlot object
        :return: True if the slot is valid, False otherwise
        """
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
    def is_valid_date_format(date_str):
        """
        Check if the date string is in the format "dd-mm-yyyy".
        :param date_str: Date string to check
        :return: True if the date string is valid, False otherwise
        """
        try:
            datetime.strptime(date_str, "%d-%m-%Y")
            return True
        except ValueError:
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
        if input_email in valid_patient_details:
            if input_password == valid_patient_details[input_email]:
                return True
        return False
    
    
    @staticmethod
    def is_valid_clinic_list(assigned_clinics, available_clinics):
        """
        Check if the assigned clinics are valid by comparing them with the available clinics.
        :param assigned_clinics: List of assigned clinics
        :param available_clinics: List of available clinics
        :return: Tuple (is_valid, valid_clinics, invalid_clinics)
        """
        valid_clinics = [clinic.strip() for clinic in assigned_clinics if clinic.strip() in available_clinics]
        invalid_clinics = [clinic.strip() for clinic in assigned_clinics if clinic.strip() not in available_clinics]
        return len(invalid_clinics) == 0, valid_clinics, invalid_clinics
