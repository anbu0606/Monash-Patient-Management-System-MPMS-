class Clinic:
    def __init__(self, clinic_name=None, suburb=None, available_services=None, operating_hours=None):
        self.clinic_name = clinic_name
        self.suburb = suburb
        self.available_services = available_services if available_services is not None else []
        self.operating_hours = operating_hours

    #clinic obj into text for saving into the txt file
    def __str__(self):
        available_services_str = ','.join(self.available_services)
        return f"""
clinic_name:{self.clinic_name}
suburb:{self.suburb}
available_services:{available_services_str}
operating_hours:{self.operating_hours}
|"""
    
    # Getters
    def get_available_services(self):
        return self.available_services

    def get_clinic_name(self):
            return self.clinic_name

    def get_operating_hours(self):
            return self.operating_hours

    def get_suburb(self):
            return self.suburb

    # Setters
    def set_available_services(self, available_services):
            self.available_services = available_services

    def set_clinic_name(self, clinic_name):
            self.clinic_name = clinic_name

    def set_operating_hours(self, operating_hours):
            self.operating_hours = operating_hours

    def set_suburb(self, suburb):
            self.suburb = suburb

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

    