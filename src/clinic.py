class Clinic:
    """
    This class contains the clinic and it's corresponding details.

    Attributes:
        clinic_name (str): Name of the clinic.
        suburb (str): The suburb where the clinic is located.
        available_services (list of str): List of services offered by the clinic.
        operating_hours (str): Operating hours of the clinic.
        
    """
    def __init__(self, clinic_name=None, suburb=None, available_services=None, operating_hours=None):
        """
        Initialises Clinic Class instance.

        Args:
            clinic_name (str): The name of the clinic.
            suburb (str): The suburb where the clinic is located.
            available_services (list of str): List of services offered by the clinic.
            operating_hours (str): Operating hours of the clinic.
        """
        self.available_services = available_services if available_services is not None else []
        self.clinic_name = clinic_name
        self.operating_hours = operating_hours
        self.suburb = suburb


    def __str__(self):
        """
        Return a string representation of the clinic objects suitable for saving to a text file.

        Returns:
            str: Formatted string of clinic objects.
        """
        available_services_str = ','.join(self.available_services)
        return f"""
clinic_name:{self.clinic_name}
suburb:{self.suburb}
available_services:{available_services_str}
operating_hours:{self.operating_hours}
|"""
    
    
    def get_available_services(self):

        """
        Get the list of available services at the clinic.

        Returns:
            list of str: The available services.
        """
        return self.available_services

    def get_clinic_name(self):
        
            """
            Get the name of the clinic.
            Returns:
                str: The clinic name.
            """
            return self.clinic_name

    def get_operating_hours(self):
            """
            Get the operating hours of the clinic.

            Returns:
                str: The operating hours.
            """
            return self.operating_hours

    def get_suburb(self):
            """
            Get the suburb of the clinic.

            Returns:
                str: The clinic suburb.
            """
            return self.suburb

    def set_available_services(self, available_services):
            """
            Set the available services for the clinic.

            Args:
                available_services (list of str): list of services.
            """
            self.available_services = available_services

    def set_clinic_name(self, clinic_name):
            """
            Set the name of the clinic.

            Args:
                clinic_name (str): The new clinic name.
            """
            self.clinic_name = clinic_name

    def set_operating_hours(self, operating_hours):
            """
            Set the operating hours for the clinic.

            Args:
                operating_hours (str): New operating hours.
            """
            self.operating_hours = operating_hours

    def set_suburb(self, suburb):
            """
            Set the suburb name for the clinic.
            Args:
                suburb (str): The new suburb.
            """
            self.suburb = suburb  