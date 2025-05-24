class Gp:
    def __init__(self, gp_name=None, email=None, assigned_clinics=None, specialisation=None,availability=None):
        self.assigned_clinics = assigned_clinics if assigned_clinics is not None else []
        self.availability = availability
        self.email = email
        self.gp_name = gp_name
        self.specialisation = specialisation if specialisation is not None else []

    #gp obj into text for saving into the txt file
    def __str__(self):
        assigned_clinics_str = ','.join(self.assigned_clinics)
        specialisation_str = ','.join(self.specialisation)
        return f"""
gp_name:{self.gp_name}
email:{self.email}
assigned_clinics:{assigned_clinics_str}
specialisation:{specialisation_str}
availability:{self.availability}
|"""
    
    # Getters
    def get_availability(self):
            return self.availability
    
    def get_assigned_clinics(self):
            return self.assigned_clinics
    
    def get_email(self):
            return self.email

    def get_gp_name(self):
        return self.gp_name

    def get_specialisation(self):
            return self.specialisation

    # Setters
    def set_assigned_clinics(self, assigned_clinics):
            self.assigned_clinics = assigned_clinics

    def set_availability(self, availability):
            self.availability = availability

    def set_email(self, email):
            self.email = email

    def set_gp_name(self, gp_name):
            self.gp_name = gp_name

    def set_specialisation(self, specialisation):
            self.specialisation = specialisation