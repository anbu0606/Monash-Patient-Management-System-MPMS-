class User:
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
        return f'''
    User Details:
                First name:     {self.fname}
                Last  name:     {self.lname}
                Email:          {self.email}
                Password:       {self.password}
                Mobile number:  {self.mobile_num}
'''
    
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