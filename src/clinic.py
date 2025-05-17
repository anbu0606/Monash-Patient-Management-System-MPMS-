class Clinic:
    clinic_list = []

    def __init__(self, clinic_name=None, suburb=None, available_services=None, operating_hours=None):
        self.clinic_name = clinic_name
        self.suburb = suburb
        self.available_services = available_services if available_services is not None else []
        self.operating_hours = operating_hours
        Clinic.clinic_list.append(self)

    #clinic obj into text for saving into the txt file

    def __str__(self):
        available_services_str = ','.join(self.available_services)
        return f"""
clinic_name:{self.clinic_name}
suburb:{self.suburb}
available_services:{available_services_str}
operating_hours:{self.operating_hours}
|"""
    
    @classmethod
    def get_clinic_list(cls):
        return cls.clinic_list
    
    @classmethod
    def load_clinics(cls, filename="clinic.txt"):
        """
        This function creates Clinic objects and restores their state from a text file.
        It then stores the objects in a class variable.
        """
        with open(f"src\\{filename}", "r") as file:
            clinics_raw_data = [y.rstrip().split("\n") for y in file.read().split("|\n")]
        for clinic_raw_data in clinics_raw_data:
            clinic = Clinic()
            for key_value in clinic_raw_data:
                if ":" not in key_value:
                    continue
                key, value = key_value.split(":", 1)
                if key == "available_services":
                    value = value.split(",")
                setattr(clinic, key, value)

    
    # @classmethod
    # def save_clinics(cls, filename="clinic.txt"):
    #     """
    #     Save all clinic objects in the text file.
    #     """
    #     with open(f"src\\{filename}", "w") as f:
    #         for clinic in cls.clinic_list:
    #             f.write(str(clinic))

    @classmethod
    def save_clinics(cls, clinics=None, filename="clinic.txt"):
        """
        Save all clinic objects in the text file.
        """
        if clinics is None:
            clinics = cls.clinic_list
    
        with open(f"src\\{filename}", "w") as f:
            for clinic in clinics:
                f.write(str(clinic))
    
    @classmethod
    def add_clinic(cls, clinic):
        """
        Adds a new clinic and saves it.
        """
        cls.clinic_list.append(clinic)
        cls.save_clinics()

    @classmethod
    def update_clinic(cls, clinic_name, updated_clinic):
        """
        Updates an existing clinic based on the name.
        """
        for idx, clinic in enumerate(cls.clinic_list):
            if clinic.clinic_name == clinic_name:
                cls.clinic_list[idx] = updated_clinic
                cls.save_clinics(cls.clinic_list)
                break
    
    @classmethod
    def delete_clinic(cls, clinic_name):
        """
        Deletes a clinic from the list and updates the storage.
        """
        cls.clinic_list = [clinic for clinic in cls.clinic_list if clinic.clinic_name != clinic_name]
        cls.save_clinics()

    