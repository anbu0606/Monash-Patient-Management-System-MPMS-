class Appointment:
    def __init__(self, clinic_name, gp_name, date, start_time, duration, clinic_suburb, reason_for_visit, status="Booked", availability=False):
        self.clinic_name = clinic_name
        self.gp_name = gp_name
        self.date = date
        self.start_time = start_time
        self.duration = duration
        self.clinic_suburb = clinic_suburb
        self.reason_for_visit = reason_for_visit
        self.status = status
        self.availability = availability

        
    
    def __str__(self):
        return f"""{{
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
        return f"{self.clinic_name}|{self.gp_name}|{self.date}|{self.start_time}|{self.duration}|{self.clinic_suburb}|{self.reason_for_visit}|{self.status}"



    
    @staticmethod
    def save_appointment(appointment):
        with open(f"src/booked_appointment.txt", "a") as f:
            f.write(appointment.to_file_string() + "\n")