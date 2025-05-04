class AppointmentSlot:
    #constructor
    def __init__(self, clinic_name, gp_name, date, start_time, duration, clinic_suburb, reason_for_visit, availability=True, status="Available"):
        self.clinic_name = clinic_name
        self.gp_name = gp_name
        self.date = date
        self.start_time = start_time
        self.duration = duration
        self.clinic_suburb = clinic_suburb
        self.reason_for_visit = reason_for_visit
        self.availability = availability
        self.status = status

    #convert an appt slot object into text format so that it can be saved into the txt file
    def __str__(self):
       return f"""{{
            clinic_name:{self.clinic_name}
            gp_name:{self.gp_name}
            date:{self.date}
            start_time:{self.start_time}
            duration:{self.duration}
            clinic_suburb:{self.clinic_suburb}
            reason_for_visit:{self.reason_for_visit}
            availability:{self.availability}
            status:{self.status}
        }}
        """

    #This method is for deserialisation, which means that we can turn saved data into a 
    #real object
    @classmethod
    # def from_string(cls, slot_text):
    #     attributes = {}
    #     lines = slot_text.strip().splitlines()

    #     for line in lines:
    #         # Skip curly bracket lines in the txt file
    #         if line in ("{", "}"):  
    #             continue
    #         key, value = line.split(":", 1)
    #         attributes[key.strip()] = value.strip()
    def from_string(cls, slot_text):
        attributes = {}
        lines = slot_text.strip().splitlines()

        for line in lines:
            line = line.strip()
            if not line or line.startswith("{") or line.startswith("}"):
                continue
            if ":" not in line:
                continue  # Malformed line, skip
            key, value = line.split(":", 1)
            attributes[key.strip()] = value.strip()
        return cls(
            clinic_name=attributes["clinic_name"],
            gp_name=attributes["gp_name"],
            date=attributes["date"],
            start_time=attributes["start_time"],
            duration=attributes["duration"],
            clinic_suburb=attributes["clinic_suburb"],
            reason_for_visit=attributes["reason_for_visit"],
            availability=attributes["availability"] == "True",
            status=attributes["status"]
        )


# Every time we start out program, we need to be able to read all the data
# for each slot in the txt file
def load_appointment_slots(filename="appointment_slot.txt"):
    # Reads the entire file
    with open(f"src\\{filename}", "r") as f:
        content = f.read()

    # Split the file contents into blocks using the closing curly brace "}" as a marker
    blocks = content.split("}")

    #Include the closing brace and only include blocks that start with "{"
    slot_blocks = [block + "}" for block in blocks if "{" in block]
    
    # This converts each block from the txt file
    # into an Appointment slot object using from_string, 
    # so that we can use it in future
    return [AppointmentSlot.from_string(block) for block in slot_blocks]
    

#After the admin makes any changes or adds in extra slots, 
#call this to make sure that it is saved into the txt file
def save_appointment_slots(slots, filename="appointment_slot.txt"):
    # Save all slots, each enclosed in curly braces
    with open(f"src\\{filename}", "w") as f:
        for slot in slots:
            f.write(str(slot))
