class AppointmentSlot:
    _appointment_slot_list = []

    #constructor
    def __init__(
            self,
            clinic_name = None,
            gp_name = None,
            date = None,
            start_time = None,
            duration = None, 
            clinic_suburb = None,
            reason_for_visit = None,
            availability = True,
            ):
        self.clinic_name = clinic_name
        self.gp_name = gp_name
        self.date = date
        self.start_time = start_time
        self.duration = duration
        self.clinic_suburb = clinic_suburb
        self.reason_for_visit = reason_for_visit
        self.availability = availability
        AppointmentSlot._appointment_slot_list.append(self)

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

    @classmethod
    def get_appointment_slot_list(cls):
        return cls._appointment_slot_list

    @classmethod
    def load_appointment_slots(cls, filename="appointment_slot.txt"):
        """
        This function creates AppointmentSlot objects and restores their instance state using a text file storing object state.
        It then stores the objects in a class variable.

        Args:
            filename(str):  A string storing the name of the text file from which data will be extracted. 
        """
        with open(f"src\\{filename}", "r") as file:  
            appt_slots_raw_data = [y.rstrip().split("\n") for y in file.read().split("|\n")] # Store each appt_slot's raw data in a list
        for appt_slot_raw_data in appt_slots_raw_data:
            appt_slot = AppointmentSlot()
            for key_value in appt_slot_raw_data:
                if ":" not in key_value:
                    continue # Malformed line, skip
                key_value = key_value.split(":")
                key = key_value[0]
                value = key_value[1]
                if value in ["True", "False"]:
                    if value == "True":
                        value = True
                    else:
                        value = False
                setattr(appt_slot, key, value)

    #After the admin makes any changes or adds in extra slots, 
    #call this to make sure that it is saved into the txt file
    @classmethod
    def save_appointment_slots(cls, slots, filename="appointment_slot.txt"):
        # Save all slots, each enclosed in curly braces
        with open(f"src\\{filename}", "w") as f:
            for slot in slots:
                f.write(str(slot))