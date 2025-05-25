class FileIO:
    """
    This class used for handling file input/output operations related to the whole MPMS system.
    
    This class includes static methods to load and save different entities like
    clinics, GPs, patients, appointments, and appointment slots. It also used for exporting reports in different formats.
    """
    
    def __init__(self):
        pass
    
    @staticmethod
    def export_report(format, report_data):
        """
        This function exports the report data to a file in the specified format.
        Args:
            format(str): The format in which the report data should be exported.
            report_data(str): The report data to be exported.
        Raises:
            ValueError: If an unsupported format is passed in the function.
        """
        if format == ".txt":
            with open("appoint_reason_report.txt", "w") as file:
                file.write(report_data)
        elif format == ".csv":
            with open("appoint_reason_report.csv", "w") as file:
                file.writelines(report_data)
        else:
            raise ValueError(f"Invalid export format:{format} was passed to export_report() in report.py")
    
    @staticmethod
    def load_admins(admin_class, filename="admin.txt"):
        """
        This function creates admin objects and restores their instance state using a text file storing object state.
        It then stores the admin objects in a class variable.

        Args:
            admin_class(type): The Admin class to instantiate.
            filename(str):  A string storing the name of the text file from which data will be extracted.

        Returns:
            list: A list of Admin objects. 
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
            appointment_slot_class (type): The AppointmentSlot class to instantiate.
            filename(str):  A string storing the name of the text file from which data will be extracted.

        Returns:
            list: A list of AppointmentSlot objects. 
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
            if appt_slot.get_clinic_name() == None:
                del appt_slot
            else:
                appointment_slots.append(appt_slot)
        return appointment_slots
    
    @staticmethod
    def load_appointments(appointment_class, appointment_slot_class):
        """
        This function creates Appointment objects and restores their instance state using a text file storing object state.
        It then stores the appointment objects in a class variable.
        Args:
            appointment_class (type): The Appointment class to instantiate.
            appointment_slot_class (type): The AppointmentSlot class to instantiate slot info.
        
        Returns:
            tuple: A list of Appointment objects and a list of booked slot objects.
        """
        appointments= []
        associated_upcoming_slots = []
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
                        if fields[8] == "Booked":
                            associated_upcoming_slots.append(slot_obj)
        except FileNotFoundError:
            pass
        return appointments, associated_upcoming_slots

    @staticmethod
    def load_clinics(clinic_class, filename="clinic.txt"):
        """
        This function creates Clinic objects and restores their state from a text file.
        It then stores the objects in a class variable.

        Args:
            clinic_class (type): The Clinic class to instantiate.
            filename (str): The name of the clinic data file.

        Returns:
            list: A list of Clinic objects.
        """
        clinic_list = []
        with open(f"src\\{filename}", "r") as file:
            clinics_raw_data = [y.rstrip().split("\n") for y in file.read().split("|\n")]
        for clinic_raw_data in clinics_raw_data:
            clinic = clinic_class()
            for key_value in clinic_raw_data:
                if ":" not in key_value:
                    continue
                key, value = key_value.split(":", 1)
                if key == "available_services":
                    value = value.split(",")
                setattr(clinic, key, value)
            clinic_list.append(clinic)
        return clinic_list
    
    @staticmethod
    def load_gp(gp_class, filename="gp.txt"):
        """
        This function creates gp objects and restores their state from a text file.
        It then stores the objects in a class variable.

        Args:
            gp_class(type): The GP class to instantiate.
            filename(str): The name of the GP data file.

        Returns:
            list: A list of GP objects.
        """
        gp_list = []
        with open(f"src\\{filename}", "r") as file:
            gps_raw_data = [y.rstrip().split("\n") for y in file.read().split("|\n")]
        for gp_raw_data in gps_raw_data:
            gp = gp_class()
            for key_value in gp_raw_data:
                if ":" not in key_value:
                    continue
                key, value = key_value.split(":", 1)
                if key == "assigned_clinics":
                    value = value.split(",")
                elif key == "specialisation":
                    value = value.split(",")
            
                setattr(gp, key, value)
            gp_list.append(gp)
        return gp_list

    @staticmethod
    def load_patients(patient_class, filename="patient.txt"):
        """
        This function creates patient objects and restores their instance state using a text file storing object state.
        It then stores the patient objects in a class variable.

        Args:
            patient_class (type): The Patient class to instantiate.
            filename(str):  A string storing the name of the text file from which data will be extracted.

        Returns:
            list: A list of Patient objects.
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
        """
        Save a single appointment object to the appointments.txt file.
        Args:
            appointment (Appointment): The appointment object to save.
        """
        with open(f"src/appointments.txt", "a") as f:
            f.write(appointment.to_file_string() + "\n")
    
    @staticmethod
    def save_appointments(appointments):
        """
        Save a list of appointment objects to the appointments.txt file.
        Args:
            appointments (list): A list of appointment objects to save.
        """
        with open(f"src/appointments.txt", "w") as f:
            for appointment in appointments:
                f.write(appointment.to_file_string() + "\n")
    
    #After the admin makes any changes or adds in extra slots, 
    #call this to make sure that it is saved into the txt file
    @staticmethod
    def save_appointment_slots(slots, filename="appointment_slot.txt"):
        """
        Save all appointment slots in the text file.
        Args:
            slots (list): A list of appointment slot objects to save.
            filename (str): The name of the file to save the appointment slots to.
        """
        # Save all slots, each enclosed in curly braces
        with open(f"src\\{filename}", "w") as f:
            for slot in slots:
                f.write(str(slot))

    @staticmethod
    def save_clinics(clinics=[], filename="clinic.txt"):
        """
        Save all clinic objects in the text file.
        Args:
            clinics (list): A list of clinic objects to save.
            filename (str): The name of the file to save the clinics to.
        """   
        with open(f"src\\{filename}", "w") as f:
            for clinic in clinics:
                f.write(str(clinic))

    @staticmethod
    def save_gps(gps=[], filename="gp.txt"):
        """
        Save all gp objects in the text file.
        Args:
            gps (list): A list of gp objects to save.
            filename (str): The name of the file to save the gps to.
        """  
        with open(f"src\\{filename}", "w") as f:
            for gp in gps:
                f.write(str(gp))