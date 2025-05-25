from appointment_slot import AppointmentSlot

class Appointment:
    def __init__(
            self,
            email = None,
            slot = AppointmentSlot(),
            status = "Booked"
        ):
        '''
        Constructor for the Appointment class.

        Initializes an Appointment object that links a specific appointment slot.

        Args:
            email (str): The email address of the patient booking the appointment.
            slot (AppointmentSlot): An instance of AppointmentSlot representing the booked slot.
            status (str): The status of the appointment ("Booked", "Cancelled by Patient", "Cancelled by Clinic" or "Attended"). Default is "Booked".
        ''' 
        self.email = email 
        self.slot = slot
        self.status = status
    
    def __str__(self):
        return f"""
Appointment Details:
    Clinic:     {self.slot.clinic_name}
    GP:         {self.slot.gp_name}
    Date:       {self.slot.date}
    Time:       {self.slot.start_time}
    Duration:   {self.slot.duration} minutes
    Suburb:     {self.slot.clinic_suburb}
    Reason:     {self.slot.reason_for_visit}
    Status:     {self.status}
{"-" * 50}
"""

    # Getters
    def get_email(self):
        '''
        Returns the email address associated with the appointment.

        Returns:
            email (str): The patient's email address.
        '''
        return self.email
    
    def get_slot(self):
        '''
        Returns the AppointmentSlot object associated with the appointment.

        Returns:
            slot (AppointmentSlot): The slot information for the appointment.
        '''
        return self.slot
    
    def get_status(self):
        '''
        Returns the current status of the appointment.

        Returns:
            status (str): The status of the appointment (e.g., "Booked", "Cancelled").
        '''
        return self.status
    
    # Setters
    def set_status(self, new_status):
        '''
        Sets the appointment instance's status
        Args:
            new_status(bool): new status for appointment instance.
        '''
        self.status = new_status

    def to_file_string(self):
        '''
        Returns a String value that is in the required format for storing the Appointment's details in the text database.
        Returns:
            (str): Formatted String.
        '''
        return f"{self.email}|{self.slot.get_clinic_name()}|{self.slot.get_gp_name()}|{self.slot.get_date()}|{self.slot.get_start_time()}|{self.slot.get_duration()}|{self.slot.get_clinic_suburb()}|{self.slot.get_reason_for_visit()}|{self.status}"
