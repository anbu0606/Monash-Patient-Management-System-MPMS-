from datetime import datetime
class Validator:
    def __init__(self):
        pass

    @staticmethod
    def is_input_back(user_input):
        if user_input == "BACK":
            return True
        return False
    
    @staticmethod
    def is_input_continue(user_input):
        if user_input == "CONTINUE":
            return True
        return False
    
    @staticmethod
    def is_input_exit(user_input):
        if user_input == "EXIT":
            return True
        return False
    
    @staticmethod
    def is_input_export(user_input):
        if user_input == "EXPORT":
            return True
        return False
    
    @staticmethod
    def is_input_logout(user_input):
        if user_input == "LOGOUT":
            return True
        return False
    
    @staticmethod
    def is_input_filter(user_input):
        if user_input == "FILTER":
            return True
        return False

    @staticmethod
    def is_valid_admin_login(valid_admin_details, input_email, input_password):
        if input_email in valid_admin_details:
            if input_password == valid_admin_details[input_email]:
                return True
        return False

    @staticmethod
    def is_valid_date_format(date_str):
        try:
            datetime.strptime(date_str, "%d-%m-%Y")
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_patient_login(valid_patient_details, input_email, input_password):
        if input_email in valid_patient_details:
            if input_password == valid_patient_details[input_email]:
                return True
        return False