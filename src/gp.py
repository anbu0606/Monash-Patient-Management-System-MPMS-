class Gp:
    def __init__(self, gp_name=None, email=None, assigned_clinics=None, specialisation=None,availability=None):
        self.gp_name = gp_name
        self.email = email
        self.assigned_clinics = assigned_clinics if assigned_clinics is not None else []
        self.specialisation = specialisation if specialisation is not None else []
        self.availability = availability

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
    def get_gp_name(self):
        return self.gp_name

    def get_email(self):
            return self.email

    def get_assigned_clinics(self):
            return self.assigned_clinics

    def get_specialisation(self):
            return self.specialisation
    
    def get_availability(self):
            return self.availability

    # Setters
    def set_gp_name(self, gp_name):
            self.gp_name = gp_name

    def set_email(self, email):
            self.email = email

    def set_assigned_clinics(self, assigned_clinics):
            self.assigned_clinics = assigned_clinics

    def set_specialisation(self, specialisation):
            self.specialisation = specialisation

    def set_availability(self, availability):
            self.availability = availability

    # @classmethod
    # def update_clinic(cls, clinic_name, updated_clinic):
    #     """
    #     Updates an existing clinic based on the name.
    #     """
    #     for idx, clinic in enumerate(cls.clinic_list):
    #         if clinic.clinic_name == clinic_name:
    #             cls.clinic_list[idx] = updated_clinic
    #             cls.save_clinics(cls.clinic_list)
    #             break
    
    # @classmethod
    # def delete_clinic(cls, clinic_name):
    #     """
    #     Deletes a clinic from the list and updates the storage.
    #     """
    #     cls.clinic_list = [clinic for clinic in cls.clinic_list if clinic.clinic_name != clinic_name]
    #     cls.save_clinics()

    