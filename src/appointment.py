import datetime

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
            with open("src/booked_appointment.txt", "r") as f:
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
    def save_appointment(appointment):
        with open(f"src/booked_appointment.txt", "a") as f:
            f.write(appointment.to_file_string() + "\n")


    @staticmethod
    def cancel_appointment(appointment):
        try:
            current_time = datetime.datetime.now()
            appointment_datetime = datetime.datetime.strptime(f"{appointment.date} {appointment.start_time}", "%d/%m/%Y %H:%M")
            time_difference = appointment_datetime - current_time

            if time_difference.total_seconds() <= 86400:
                print("\n Cancellation is within 24 hours of the appointment. A penalty may apply.")
                confirmation = input("Do you still want to proceed with cancellation? (yes/no): ").strip().lower()
                if confirmation != "yes":
                    print("\n Cancellation aborted.")
                    return False

            # --- Step 2: Remove from booked_appointment.txt ---
            with open("src/booked_appointment.txt", "r") as file:
                lines = file.readlines()
            with open("src/booked_appointment.txt", "w") as file:
                for line in lines:
                    if not line.startswith(appointment.email) or appointment.to_file_string() not in line:
                        file.write(line)

            # --- Step 3: Update appointment_slot.txt to "Available" ---
            updated_lines = []
            with open("src/appointment_slot.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    data = line.strip().split("|")
                    if (
                        data[1] == appointment.clinic_name and
                        data[2] == appointment.gp_name and
                        data[3] == appointment.date and
                        data[4] == appointment.start_time
                    ):
                        data[-2] = "Available"  # Update status
                        data[-1] = "True"       # Update availability
                        updated_lines.append("|".join(data) + "\n")
                    else:
                        updated_lines.append(line)

            with open("src/appointment_slot.txt", "w") as file:
                file.writelines(updated_lines)

            print("\n Appointment cancelled successfully.")
            return True

        except Exception as e:
            print(f"\n An error occurred during cancellation: {e}")
            return False