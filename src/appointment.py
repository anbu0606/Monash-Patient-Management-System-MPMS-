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
    
    def to_file_string(self):
        return f"{self.email}|{self.clinic_name}|{self.gp_name}|{self.date}|{self.start_time}|{self.duration}|{self.clinic_suburb}|{self.reason_for_visit}|{self.status}"
    
    @staticmethod
    def load_book_appointment(email):
        booked_appointments= []
        try:
            with open("src/appointments.txt", "r") as f:
                for line in f:
                    fields = line.strip().split("|")
                    if fields[0] == email:
                        slot_obj = AppointmentSlot(
                            clinic_name=fields[1],
                            gp_name=fields[2],
                            date=fields[3],
                            start_time=fields[4],
                            duration=fields[5],
                            clinic_suburb=fields[6],
                            reason_for_visit=fields[7],
                            availability=False
                        )
                        booked_appointments.append(Appointment(
                            email=fields[0],
                            slot=slot_obj,
                            status=fields[8]
                        ))
        except FileNotFoundError:
            pass
        return booked_appointments

    # @staticmethod
    # def load_previous_appointments(email):
    #     """
    #     Load appointments that have already occurred or been cancelled.
        
    #     Args:
    #         email (str): The patient's email to filter appointments
            
    #     Returns:
    #         list: List of Appointment objects that are past or cancelled
    #     """
    #     previous_appointments = []
    #     try:
    #         current_date = datetime.now().strftime("%d-%m-%Y")
            
    #         with open("src/appointments.txt", "r") as f:
    #             for line in f:
    #                 fields = line.strip().split("|")
    #                 if fields[0] == email:
    #                     # Check if appointment has status "Attended" or "Cancelled"
    #                     # or if the appointment date has passed
    #                     status = fields[8]
    #                     date = fields[3]
                        
    #                     # Convert date strings to datetime objects for comparison
    #                     appointment_date = datetime.strptime(date, "%d-%m-%Y")
    #                     current_datetime = datetime.now()
                        
    #                     is_past_date = appointment_date.date() < current_datetime.date()
    #                     is_completed_status = status in ["Attended", "Cancelled by Clinic", "Cancelled by Patient"]
                        
    #                     if is_past_date or is_completed_status:
    #                         previous_appointments.append(Appointment(
    #                             email=fields[0],
    #                             clinic_name=fields[1],
    #                             gp_name=fields[2],
    #                             date=fields[3],
    #                             start_time=fields[4],
    #                             duration=fields[5],
    #                             clinic_suburb=fields[6],
    #                             reason_for_visit=fields[7],
    #                             status=fields[8]
    #                         ))
    #     except FileNotFoundError:
    #         pass
    #     return previous_appointments
    
    # @staticmethod
    # def load_upcoming_appointments(email):
    #     """
    #     Load appointments that are scheduled for the future with status "Booked".
        
    #     Args:
    #         email (str): The patient's email to filter appointments
            
    #     Returns:
    #         list: List of Appointment objects that are upcoming
    #     """
    #     upcoming_appointments = []
    #     try:
    #         with open("src/appointments.txt", "r") as f:
    #             for line in f:
    #                 fields = line.strip().split("|")
    #                 if fields[0] == email:
    #                     # Check if appointment has status "Booked"
    #                     # and if the appointment date is in the future
    #                     status = fields[8]
    #                     date = fields[3]
                        
    #                     # Convert date strings to datetime objects for comparison
    #                     appointment_date = datetime.strptime(date, "%d-%m-%Y")
    #                     current_datetime = datetime.now()
                        
    #                     is_future_date = appointment_date.date() >= current_datetime.date()
    #                     is_booked_status = status == "Booked"
                        
    #                     if is_future_date and is_booked_status:
    #                         upcoming_appointments.append(Appointment(
    #                             email=fields[0],
    #                             clinic_name=fields[1],
    #                             gp_name=fields[2],
    #                             date=fields[3],
    #                             start_time=fields[4],
    #                             duration=fields[5],
    #                             clinic_suburb=fields[6],
    #                             reason_for_visit=fields[7],
    #                             status=fields[8]
    #                         ))
    #     except FileNotFoundError:
    #         pass
    #     return upcoming_appointments

    @staticmethod
    def save_appointment(appointment):
        with open(f"src/appointments.txt", "a") as f:
            f.write(appointment.to_file_string() + "\n")

    