from user import User
class Patient(User):
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

    # Accessors
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
