class Admin:
    def __init__(self):
        self.email = None
        self.fname = None
        self.lname = None
        self.mobile_num = None
        self.password = None
        
    
    def __str__(self):
        return f'''
Patient Details:
                fname:      {self.fname}
                lname:      {self.lname}
                email:      {self.email}
                mobile_num: {self.mobile_num}
                password:   {self.password}
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
