from datetime import datetime

class Appointment:
    def __init__(
            self,
            clinic_name = None,
            gp_name = None,
            date = None,
            start_time = None,
            duration = None,
            clinic_suburb = None,
            reason_for_visit = None,
            status = "Booked",
            availability = False,
            email = None
        ):
        self.clinic_name = clinic_name
        self.gp_name = gp_name
        self.date = date
        self.start_time = start_time
        self.duration = duration
        self.clinic_suburb = clinic_suburb
        self.reason_for_visit = reason_for_visit
        self.status = status
        self.availability = availability   
        self.email = email     
    
    def __str__(self):
        return f"""{{
        email:{self.email}
        clinic_name:{self.clinic_name}
        gp_name:{self.gp_name}
        date:{self.date}
        start_time:{self.start_time}
        duration:{self.duration}
        clinic_suburb:{self.clinic_suburb}
        reason_for_visit:{self.reason_for_visit}
        status:{self.status}
    }}"""
    
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
                        booked_appointments.append(Appointment(
                            email=fields[0],
                            clinic_name=fields[1],
                            gp_name=fields[2],
                            date=fields[3],
                            start_time=fields[4],
                            duration=fields[5],
                            clinic_suburb=fields[6],
                            reason_for_visit=fields[7],
                            status=fields[8]
                        ))
        except FileNotFoundError:
            pass
        return booked_appointments

    @staticmethod
    def load_previous_appointments(email):
        """
        Load appointments that have already occurred or been cancelled.
        
        Args:
            email (str): The patient's email to filter appointments
            
        Returns:
            list: List of Appointment objects that are past or cancelled
        """
        previous_appointments = []
        try:
            current_date = datetime.now().strftime("%d-%m-%Y")
            
            with open("src/appointments.txt", "r") as f:
                for line in f:
                    fields = line.strip().split("|")
                    if fields[0] == email:
                        # Check if appointment has status "Attended" or "Cancelled"
                        # or if the appointment date has passed
                        status = fields[8]
                        date = fields[3]
                        
                        # Convert date strings to datetime objects for comparison
                        appointment_date = datetime.strptime(date, "%d-%m-%Y")
                        current_datetime = datetime.now()
                        
                        is_past_date = appointment_date.date() < current_datetime.date()
                        is_completed_status = status in ["Attended", "Cancelled by Clinic", "Cancelled by Patient"]
                        
                        if is_past_date or is_completed_status:
                            previous_appointments.append(Appointment(
                                email=fields[0],
                                clinic_name=fields[1],
                                gp_name=fields[2],
                                date=fields[3],
                                start_time=fields[4],
                                duration=fields[5],
                                clinic_suburb=fields[6],
                                reason_for_visit=fields[7],
                                status=fields[8]
                            ))
        except FileNotFoundError:
            pass
        return previous_appointments
    
    @staticmethod
    def load_upcoming_appointments(email):
        """
        Load appointments that are scheduled for the future with status "Booked".
        
        Args:
            email (str): The patient's email to filter appointments
            
        Returns:
            list: List of Appointment objects that are upcoming
        """
        upcoming_appointments = []
        try:
            with open("src/appointments.txt", "r") as f:
                for line in f:
                    fields = line.strip().split("|")
                    if fields[0] == email:
                        # Check if appointment has status "Booked"
                        # and if the appointment date is in the future
                        status = fields[8]
                        date = fields[3]
                        
                        # Convert date strings to datetime objects for comparison
                        appointment_date = datetime.strptime(date, "%d-%m-%Y")
                        current_datetime = datetime.now()
                        
                        is_future_date = appointment_date.date() >= current_datetime.date()
                        is_booked_status = status == "Booked"
                        
                        if is_future_date and is_booked_status:
                            upcoming_appointments.append(Appointment(
                                email=fields[0],
                                clinic_name=fields[1],
                                gp_name=fields[2],
                                date=fields[3],
                                start_time=fields[4],
                                duration=fields[5],
                                clinic_suburb=fields[6],
                                reason_for_visit=fields[7],
                                status=fields[8]
                            ))
        except FileNotFoundError:
            pass
        return upcoming_appointments

    @staticmethod
    def save_appointment(appointment):
        with open(f"src/appointments.txt", "a") as f:
            f.write(appointment.to_file_string() + "\n")

    