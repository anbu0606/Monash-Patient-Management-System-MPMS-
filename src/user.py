class User:
    """
    User class to represent a user in the system.
    Attributes:
        email (str): The email of the user.
        fname (str): The first name of the user.
        lname (str): The last name of the user.
        password (str): The password for the user's account.
        mobile_num (str): The mobile number of the user.
    """
    def __init__(
            self,
            email = None,
            fname = None,
            lname = None,
            password = None,
            mobile_num = None
    ):
        self.email = email
        self.fname = fname
        self.lname = lname
        self.password = password
        self.mobile_num = mobile_num
    
    def __str__(self):
        """
        Returns a string representation of the user details.
        """
        return f'''
    User Details:
                First name:     {self.fname}
                Last  name:     {self.lname}
                Email:          {self.email}
                Password:       {self.password}
                Mobile number:  {self.mobile_num}
'''
    # Accessors
    def get_email(self):
        """
        Returns the email of the user.
        """
        return self.email
    
    def get_fname(self):
        """
        Returns the first name of the user.
        """
        return self.fname
    
    def get_lname(self):
        """
        Returns the last name of the user.
        """
        return self.lname
    
    def get_password(self):
        """
        Returns the password of the user.
        """
        return self.password
    
    def get_mobile_num(self):
        """
        Returns the mobile number of the user.
        """
        return self.mobile_num