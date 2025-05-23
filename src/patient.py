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
            address = None
        ):
        super().__init__(email, fname, lname, password, mobile_num)
        self.dob = dob
        self.gender = gender
        self.address = address
    
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

    def get_email(self):
        return self.email