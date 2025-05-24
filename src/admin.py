from user import User
class Admin(User):
    def __init__(
            self,
            email = None,
            fname = None,
            lname = None,
            mobile_num = None,
            password = None
        ):
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
