class Clinic:
    def __init__(self, clinic_name=None, suburb=None, available_services=None, operating_hours=None):
        self.available_services = available_services if available_services is not None else []
        self.clinic_name = clinic_name
        self.operating_hours = operating_hours
        self.suburb = suburb


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