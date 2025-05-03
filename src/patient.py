class Patient:
    def __init__(self):
        self.email = None
        self.fname = None
        self.lname = None
        self.password = None
        self.dob = None
        self.gender = None
        self.address = None
        self.upcoming_appt = None
        self.cancelled_appt = None
    
    def __str__(self):
        return f'''
Patient Details:
                fname:      {self.fname}
                lname:      {self.lname}
                email:      {self.email}
                password:   {self.password}
                dob:        {self.dob}
                gender:     {self.gender}
                address:    {self.address}
'''
    
    # Accessors
    def get_address(self):
        return self.address

    def get_cancelled_appt(self):
        return self.cancelled_appt

    def get_dob(self):
        return self.dob

    def get_email(self):
        return self.email

    def get_fname(self):
        return self.fname

    def get_gender(self):
        return self.gender

    def get_lname(self):
        return self.lname

    def get_password(self):
        return self.password

    def get_upcoming_appt(self):
        return self.upcoming_appt

    # Mutators
    def set_address(self, new_address):
        self.address = new_address
    
    def set_cancelled_appt(self, new_cancelled_appt):
        self.cancelled_appt = new_cancelled_appt

    def set_dob(self, new_dob):
        self.dob = new_dob

    def set_email(self, new_email):
        self.email = new_email

    def set_fname(self, new_fname):
        self.fname = new_fname

    def set_gender(self, new_gender):
        self.gender = new_gender
        
    def set_lname(self, new_lname):
        self.lname = new_lname

    def set_password(self, new_password):
        self.password = new_password

    def set_upcoming_appt(self, new_upcoming_appt):
        self.upcoming_appt = new_upcoming_appt
