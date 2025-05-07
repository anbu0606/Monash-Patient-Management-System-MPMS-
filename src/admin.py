from user import User
class Admin(User):
    _admin_list = [] # Keeping a list allows for future increase in admin numbers despite our current scope

    def __init__(
            self,
            email = None,
            fname = None,
            lname = None,
            mobile_num = None,
            password = None
        ):
        super().__init__(email, fname, lname, password, mobile_num)
        Admin._admin_list.append(self)
    
    def __str__(self):
        return f'''
Admin Details:
                First name:     {self.fname}
                Last name:      {self.lname}
                Email:          {self.email}
                Mobile number:  {self.mobile_num}
                password:       {self.password}
'''
    
    @classmethod
    def get_admin_object(cls, admin_email):
        """
        This function searches the admin list for the admin with the email passed and returns the admin object.

        Args:
            admin_email (str):    Stores the email of the admin whose object is to be initialised.
        """
        for admin in cls._admin_list:
            if admin.email == admin_email:
                return admin
        raise ValueError(f"Admin with email {admin_email} not found in database.")

    @classmethod
    def load_admins(cls, filename="admin.txt"):
        """
        This function creates admin objects and restores their instance state using a text file storing object state.
        It then stores the admin objects in a class variable.

        Args:
            filename(str):  A string storing the name of the text file from which data will be extracted. 
        """
        with open(f"src\\{filename}", "r") as file:  
            admins_raw_data = [y.rstrip().split("\n") for y in file.read().split("|\n")] # Store each admin's raw data in a list
        for admin_raw_data in admins_raw_data:
            admin = Admin()
            for key_value in admin_raw_data:
                if ":" not in key_value:
                    continue # Malformed line, skip
                key_value = key_value.split(":")
                key = key_value[0]
                value = key_value[1]
                setattr(admin, key, value)
    
    # Accessors
    @classmethod
    def get_admin_list(cls):
        return cls._admin_list
    
    def get_email(self):
        return self.email

    def get_fname(self):
        return self.fname

    def get_lname(self):
        return self.lname

    def get_password(self):
        return self.password
    
    def get_mobile_num(self):
        return self.mobile_num


    # Mutators
    def set_email(self, new_email):
        self.email = new_email

    def set_fname(self, new_fname):
        self.fname = new_fname
        
    def set_lname(self, new_lname):
        self.lname = new_lname

    def set_password(self, new_password):
        self.password = new_password

    def set_mobile_num(self, new_mobile_num):
        self.password = new_mobile_num
