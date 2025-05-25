from user import User
class Patient(User):
    """
    Represents a patient in the healthcare system, inheriting from User.
    Attributes:
        email (str): The email of the patient.
        fname (str): The first name of the patient.
        lname (str): The last name of the patient.
        password (str): The password for the patient's account.
        mobile_num (str): The mobile number of the patient.
        dob (str): The date of birth of the patient
    """
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
        """
        Returns a string representation of the patient details.
        """
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
        """
        Returns the email of the patient.
        """
        return self.email