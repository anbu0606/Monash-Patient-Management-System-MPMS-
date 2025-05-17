class AppointmentSlot:
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
        return self.availability

    def get_clinic_name(self):
            return self.clinic_name

    def get_clinic_suburb(self):
            return self.clinic_suburb

    def get_date(self):
            return self.date

    def get_duration(self):
            return self.duration

    def get_gp_name(self):
            return self.gp_name

    def get_reason_for_visit(self):
            return self.reason_for_visit

    def get_start_time(self):
            return self.start_time
    
    # Setters
    def set_availability(self, value):
        self.availability = value