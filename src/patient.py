from user import User
class Patient(User):
    _patient_list = []
    
    def __init__(
            self,
            email = None,
            fname = None,
            lname = None,
            password = None,
            mobile_num = None,
            dob = None,
            gender = None,
            address = None,
            upcoming_appointments = None,
            previous_appointments = None
        ):
        super().__init__(email, fname, lname, password, mobile_num)
        self.dob = dob
        self.gender = gender
        self.address = address
        self.upcoming_appointments = upcoming_appointments
        self.previous_appointments = previous_appointments
        Patient._patient_list.append(self)
    
    def __str__(self):
        return f'''
Patient Details:
                First name:     {self.fname}
                Last  name:     {self.lname}
                Email:          {self.email}
                Password:       {self.password}
                Mobile number:  {self.mobile_num}
                DOB:            {self.dob}
                Gender:         {self.gender}
                Address:        {self.address}
'''
    
    def append_upcoming_appointments(self, appointment_obj):
        self.upcoming_appointments.append(appointment_obj)


    @classmethod
    def get_patient_object(cls, patient_email):
        """
        This function searches the patient list for the patient with the email passed and returns the patient object.

        Args:
            patient_email (str):    Stores the email of the patient whose object is to be initialised.
        """
        for patient in cls._patient_list:
            if patient.email == patient_email:
                return patient
        raise ValueError(f"Patient with email {patient_email} not found in database.")
    
    @classmethod
    def load_patients(cls, filename="patient.txt"):
        """
        This function creates patient objects and restores their instance state using a text file storing object state.
        It then stores the patient objects in a class variable.

        Args:
            filename(str):  A string storing the name of the text file from which data will be extracted. 
        """
        patients_list = []
        with open(f"src\\{filename}", "r") as file:  
            patients_raw_data = [y.rstrip().split("\n") for y in file.read().split("|\n")] # Store each patient's raw data in a list
        for patient_raw_data in patients_raw_data:
            patient = Patient()
            for key_value in patient_raw_data:
                if ":" not in key_value:
                    continue # Malformed line, skip
                key_value = key_value.split(":")
                key = key_value[0]
                value = key_value[1]
                if value == "[]":
                    value = []
                setattr(patient, key, value)
            patients_list.append(patient)
        return patients_list

    # Accessors
    @classmethod
    def get_patient_list(cls):
        return cls._patient_list
    
    # def get_address(self):
    #     return self.address

    def get_upcoming_appointments(self):
        return self.upcoming_appointments

    def get_previous_apppointments(self):
        return self.previous_appointments

    # def get_dob(self):
    #     return self.dob

    def get_email(self):
        return self.email

    # def get_fname(self):
    #     return self.fname

    # def get_gender(self):
    #     return self.gender

    # def get_lname(self):
    #     return self.lname

    # def get_password(self):
    #     return self.password
    
    # def get_mobile_num(self):
    #     return self.mobile_num

    # def get_upcoming_appt(self):
    #     return self.upcoming_appt

    # # Mutators
    # def set_address(self, new_address):
    #     self.address = new_address
    
    # def set_cancelled_appt(self, new_cancelled_appt):
    #     self.cancelled_appt = new_cancelled_appt

    # def set_dob(self, new_dob):
    #     self.dob = new_dob

    # def set_email(self, new_email):
    #     self.email = new_email

    # def set_fname(self, new_fname):
    #     self.fname = new_fname

    # def set_gender(self, new_gender):
    #     self.gender = new_gender
        
    # def set_lname(self, new_lname):
    #     self.lname = new_lname

    # def set_password(self, new_password):
    #     self.password = new_password

    # def set_mobile_num(self, new_mobile_num):
    #     self.password = new_mobile_num

    def set_upcoming_apppointments(self, new_upcoming_appt):
        self.upcoming_appointments = new_upcoming_appt

    def set_previous_apppointments(self, new_previous_appt):
        self.previous_appointments = new_previous_appt
