from user import User
class Admin(User):
    """
    This class defines the Admin user type. It is a child class of User Class.
    """
    def __init__(
            self,
            email = None,
            fname = None,
            lname = None,
            mobile_num = None,
            password = None
        ):
        '''
        Constructor for the Admin class.

        Initializes an Admin object, which is a subclass of User.

        Args:
            email (str): The admin's email address.
            fname (str): The admin's first name.
            lname (str): The admin's last name.
            mobile_num (str): The admin's mobile number.
            password (str): The admin's account password.
        '''
        super().__init__(email, fname, lname, password, mobile_num)
        self.email = email
        self.fname = fname
        self.lname = lname
        self.password = password
        self.mobile_num = mobile_num
    def __str__(self):
        return f'''
Admin Details:
                First name:     {self.fname}
                Last name:      {self.lname}
                Email:          {self.email}
                Mobile number:  {self.mobile_num}
                password:       {self.password}
'''
    
    # Accessors
    def get_email(self):
        '''
        Returns the admin instance's email
        Returns:
            email(str): admin's email.
        '''
        return self.email

    def get_fname(self):
        '''
        Returns the admin instance's first name
        Returns:
            fname(str): admin's first name.
        '''
        return self.fname

    def get_lname(self):
        '''
        Returns the admin instance's last name
        Returns:
            lname(str): admin's last name.
        '''
        return self.lname

    def get_password(self):
        '''
        Returns the admin instance's account password
        Returns:
            password(str): admin's account password.
        '''
        return self.password
    
    def get_mobile_num(self):
        '''
        Returns the admin instance's mobile number
        Returns:
            password(str): admin's mobile number
        '''
        return self.mobile_num

    # Mutators
    def set_email(self, new_email):
        '''
        Sets the admin instance's email
        Args:
            new_email(str): new email id of admin instance
        '''
        self.email = new_email

    def set_fname(self, new_fname):
        '''
        Sets the admin instance's first name
        Args:
            new_fname(str): new first name of admin instance
        '''
        self.fname = new_fname
        
    def set_lname(self, new_lname):
        '''
        Sets the admin instance's last name
        Args:
            new_lname(str): new last name of admin instance
        '''
        self.lname = new_lname

    def set_password(self, new_password):
        '''
        Sets the admin instance's account password
        Args:
            new_password(str): new password of admin instance
        '''
        self.password = new_password

    def set_mobile_num(self, new_mobile_num):
        '''
        Sets the admin instance's mobile number
        Args:
            new_mobile_num(str): new mobile number of admin instance
        '''
        self.mobile_num = new_mobile_num