from datetime import datetime
from appointment_slot import AppointmentSlot

class Appointment:
    def __init__(
            self,
            email = None,
            slot = AppointmentSlot(),
            status = "Booked"
        ):   
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
    
    def get_email(self):
        return self.email
    
    def get_slot(self):
        return self.slot
    
    def get_status(self):
        return self.status

    def to_file_string(self):
        return f"{self.email}|{self.slot.get_clinic_name()}|{self.slot.get_gp_name()}|{self.slot.get_date()}|{self.slot.get_start_time}|{self.slot.get_duration}|{self.slot.get_clinic_suburb}|{self.slot.get_reason_for_visit}|{self.status}"

    