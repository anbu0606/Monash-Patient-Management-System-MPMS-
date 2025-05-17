class FileIO:

    def __init__(self):
        pass

    @staticmethod
    def load_admins(admin_class, filename="admin.txt"):
        """
        This function creates admin objects and restores their instance state using a text file storing object state.
        It then stores the admin objects in a class variable.

        Args:
            filename(str):  A string storing the name of the text file from which data will be extracted. 
        """
        admins = []
        with open(f"src\\{filename}", "r") as file:  
            admins_raw_data = [y.rstrip().split("\n") for y in file.read().split("|\n")] # Store each admin's raw data in a list
        for admin_raw_data in admins_raw_data:
            admin = admin_class()
            for key_value in admin_raw_data:
                if ":" not in key_value:
                    continue # Malformed line, skip
                key_value = key_value.split(":")
                key = key_value[0]
                value = key_value[1]
                setattr(admin, key, value)
            admins.append(admin)
        return admins

    @staticmethod
    def load_appointment_slots(appointment_slot_class, filename="appointment_slot.txt"):
        """
        This function creates AppointmentSlot objects and restores their instance state using a text file storing object state.
        It then stores the objects in a class variable.

        Args:
            filename(str):  A string storing the name of the text file from which data will be extracted. 
        """
        appointment_slots = []
        with open(f"src\\{filename}", "r") as file:  
            appt_slots_raw_data = [y.rstrip().split("\n") for y in file.read().split("|\n")] # Store each appt_slot's raw data in a list
        for appt_slot_raw_data in appt_slots_raw_data:
            appt_slot = appointment_slot_class()
            for key_value in appt_slot_raw_data:
                if ":" not in key_value:
                    continue # Malformed line, skip
                key, value = key_value.split(":", 1)
                if value in ["True", "False"]:
                    if value == "True":
                        value = True
                    else:
                        value = False
                setattr(appt_slot, key, value)
            appointment_slots.append(appt_slot)
        return appointment_slots
    
    @staticmethod
    def load_appointments(appointment_class, appointment_slot_class):
        appointments= []
        try:
            with open("src/appointments.txt", "r") as f:
                for line in f:
                    fields = line.strip().split("|")
                    if fields[0] != "":
                        slot_obj = appointment_slot_class(
                            clinic_name=fields[1],
                            gp_name=fields[2],
                            date=fields[3],
                            start_time=fields[4],
                            duration=fields[5],
                            clinic_suburb=fields[6],
                            reason_for_visit=fields[7],
                            availability=False
                        )
                        appointments.append(appointment_class(
                            email=fields[0],
                            slot=slot_obj,
                            status=fields[8]
                        ))
        except FileNotFoundError:
            pass
        return appointments

    @staticmethod
    def load_patients(patient_class, filename="patient.txt"):
        """
        This function creates patient objects and restores their instance state using a text file storing object state.
        It then stores the patient objects in a class variable.

        Args:
            filename(str):  A string storing the name of the text file from which data will be extracted.

        Returns:
            patients_list(List<Patient>): List of patient instances
        """
        patients_list = []
        with open(f"src\\{filename}", "r") as file:  
            patients_raw_data = [y.rstrip().split("\n") for y in file.read().split("|\n")] # Store each patient's raw data in a list
        for patient_raw_data in patients_raw_data:
            patient = patient_class()
            for key_value in patient_raw_data:
                if ":" not in key_value:
                    continue # Malformed line, skip
                key_value = key_value.split(":")
                key = key_value[0]
                value = key_value[1]
                if value == "[]":
                    value = []
                setattr(patient, key, value)
            patients_list.append(patient)
        return patients_list
    
    @staticmethod
    def save_appointment(appointment):
        with open(f"src/appointments.txt", "a") as f:
            f.write(appointment.to_file_string() + "\n")
    
    @staticmethod
    def save_appointments(appointments):
        with open(f"src/appointments.txt", "w") as f:
            for appointment in appointments:
                f.write(appointment.to_file_string() + "\n")
    
    #After the admin makes any changes or adds in extra slots, 
    #call this to make sure that it is saved into the txt file
    @staticmethod
    def save_appointment_slots(slots, filename="appointment_slot.txt"):
        # Save all slots, each enclosed in curly braces
        with open(f"src\\{filename}", "w") as f:
            for slot in slots:
                f.write(str(slot))