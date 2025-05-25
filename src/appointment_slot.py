class AppointmentSlot:
    """
    This class holds all the details of an Appointment Slot available in MPMS.
    An appointment slot refers to a pre-defined entity in MPMS that can be booked when available.
    It can be associated with an Appointment or exist independently.

    An appointment slot is created by the Administrator. 
    """
    #constructor
    def __init__(
            self,
            availability=True,
            clinic_name=None,
            clinic_suburb=None,
            date=None,
            duration=None,
            gp_name=None,
            reason_for_visit=None,
            start_time=None,
        ):
        '''
        Constructor for AppointmentSlot class.
        Args:
            availability(bool): A flag to store whether the Appointment Slot is available for Booking or not.
            clinic_name(str):   The name of the clinic for which the Appointment Slot was created.
            clinic_suburb(str): The name of the suburb in which the associated clinic resides.
            date(str):          The scheduled date of the Appointment Slot
            duration(str):      The total duration of the Appointment Slot in minutes.
            gp_name(str):       The name of the gp who will take up the Appointment Slot.
            reason_for_visit(str): The slot's associated reason for visit.
            start_time(str):    The scheduled start time of the Appointment Slot.   
        '''
        self.availability = availability
        self.clinic_name = clinic_name
        self.clinic_suburb = clinic_suburb
        self.date = date
        self.duration = duration
        self.gp_name = gp_name
        self.reason_for_visit = reason_for_visit
        self.start_time = start_time


    #convert an appt slot object into text format so that it can be saved into the txt file
    def __str__(self):
       return f"""
clinic_name:{self.clinic_name}
gp_name:{self.gp_name}
date:{self.date}
start_time:{self.start_time}
duration:{self.duration}
clinic_suburb:{self.clinic_suburb}
reason_for_visit:{self.reason_for_visit}
availability:{self.availability}
|"""
    
    # Getters
    def get_availability(self):
        '''
        Returns the slot instance's availability
        Returns:
            availability(bool): slot's availability.
        '''    
        return self.availability

    def get_clinic_name(self):
        '''
        Returns the slot instance's associated clinic name
        Returns:
            clinic_name(str): slot's associated clinic name.
        '''
        return self.clinic_name

    def get_clinic_suburb(self):
        '''
        Returns the slot instance's associated clinic suburb
        Returns:
            clinic_suburb(str): slot's associated clinic suburb.
        '''
        return self.clinic_suburb

    def get_date(self):
        '''
        Returns the slot instance's associated date
        Returns:
            date(str): slot's associated date.
        '''
        return self.date

    def get_duration(self):
        '''
        Returns the slot instance's associated slot duration.
        Returns:
            duration(str): slot's associated slot duration.
        '''
        return self.duration

    def get_gp_name(self):
        '''
        Returns the slot instance's associated gp name
        Returns:
            gp_name(str): slot's associated gp name.
        '''
        return self.gp_name

    def get_reason_for_visit(self):
        '''
        Returns the slot instance's associated reason for visit
        Returns:
            reason_for_visit(str): slot's associated reason for visit
        '''
        return self.reason_for_visit

    def get_start_time(self):
        '''
        Returns the slot instance's associated slot start time
        Returns:
            start_time(str): slot's associated slot start time.
        '''
        return self.start_time
    
    # Setters
    def set_availability(self, value):
        '''
        Sets the slot instance's availability
        Args:
            value(bool): new availability for slot instance.
        '''
        self.availability = value

    def set_clinic_name(self, value):
        '''
        Sets the slot instance's associated clinic name
        Args:
            value(bool): new associated clinic name for slot instance.
        '''
        self.clinic_name = value

    def set_clinic_suburb(self, value):
        '''
        Sets the slot instance's associated clinic suburb
        Args:
            value(bool): new associated clinic suburb for slot instance.
        '''
        self.clinic_suburb = value

    def set_date(self, value):
        '''
        Sets the slot instance's scheduled date.
        Args:
            value(bool): new scheduled date for slot instance.
        '''
        self.date = value

    def set_duration(self, value):
        '''
        Sets the slot instance's scheduled duration
        Args:
            value(bool): new scheduled duration for slot instance.
        '''
        self.duration = value

    def set_gp_name(self, value):
        '''
        Sets the slot instance's associated gp name
        Args:
            value(bool): new associated gp name for slot instance.
        '''
        self.gp_name = value

    def set_reason_for_visit(self, value):
        '''
        Sets the slot instance's associated reason for visit
        Args:
            value(bool): new associated reason for visit for slot instance.
        '''
        self.reason_for_visit = value

    def set_start_time(self, value):
        '''
        Sets the slot instance's scheduled start time
        Args:
            value(bool): new scheduled start time for slot instance.
        '''
        self.start_time = value