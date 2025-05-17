from menu import Menu
from user import User
from patient import Patient
from admin import Admin
from appointment_slot import AppointmentSlot
from appointment import Appointment
from datetime import datetime, timedelta
from validator import Validator
from fileio import FileIO
from report import Report


class MPMS:
    """
    This class contains the core logic of the Monash Patient Management System. 
    """

    def __init__(self):
        """
        Initialises MPMS Class instance.
        """
        self.admins = []
        self.appointment_slots = []
        self.appointments = []
        self.menu = Menu()
        self.patients = []
        self.is_user_admin = False
        # Other Attributes
    
    def admin_home(self, admin):
        """
        This function contains the logic for the Admin Home Page to display UI, take input and route user.
        
        Args:
            admin (Admin):  Stores the admin object.
        """
        user_action = self.menu.show_admin_home_page(attempt_number=0)
        if user_action == "logout":
            self.logout(admin)
        elif user_action == "profile_page":
            self.user_profile_page(admin)
        elif user_action == "gp_report":
            pass
        elif user_action == "reason_report":
            self.generate_report(admin, "reason")
        elif user_action == "manage_appointment_slots":
            pass
        elif user_action == "manage_clinic":
            pass
        elif user_action == "manage_gp":
            pass
        elif user_action == "manage_patient_appointments":
            pass
        else:
            raise ValueError(f"Invalid user_action:{user_action} returned to admin_home() in MPMS Class.")
    
    def book_appointment(self, patient, enable_skip = False):
        slots = self.appointment_slots
        for i in slots:
            print(i)
        # Filter out slots that are not available or are less than 2 hours away.
        # The program checks the time difference once again in line 110, just after the user selects a slot
        # to see if it is < 2 hours away.
        def is_booking_valid(slot):
            print(slot)
            try:
                slot_time = datetime.strptime(f"{slot.get_date()} {slot.get_start_time()}", "%d-%m-%Y %H:%M")
                return slot.get_availability() and slot_time > datetime.now() + timedelta(hours=2)
            except ValueError as e:
                print(f"[DEBUG] Invalid slot: {slot.get_date()} {slot.get_start_time()} - {e}")
                return False
        # Displays the available slots to the user
        available_slots = [slot for slot in slots if is_booking_valid(slot)]
       
       #If there are no available slots, inform the user and return to the patient home page
        user_action = self.menu.show_appointment_slots_page(available_slots, is_skip_enabled=enable_skip)
        if not available_slots:
            print("\n\033[91mNo appointment slots are currently available (must be at least 2 hours ahead).\033[0m")
            input("Press Enter to return to the patient home page.")
            return self.patient_home(patient)

        if user_action == "logout":
            self.logout(patient)
        elif user_action == "back":
            self.patient_home(patient)
        elif user_action == "filter":

            filter_type = self.menu.show_filter_options(is_skip_enabled = enable_skip)
            if filter_type == "back":
                return self.book_appointment(patient)
            elif filter_type == "logout":
                return self.logout(patient)
            elif filter_type == "error":
                return self.book_appointment(patient, enable_skip = True)
            else:
                value = self.menu.get_filter_value(filter_type)
                if Validator.is_input_back(value): return self.book_appointment(patient)
                if Validator.is_input_logout(value): return self.logout(patient)
                filtered_slots = [slot for slot in available_slots if getattr(slot, filter_type) and getattr(slot, filter_type).lower() == value.lower()]

            if not filtered_slots:
                print("\033[91mNo matching slots found. Press Enter to try again. \033[0m")
                input()
                return self.book_appointment(patient)

            return self._finalise_appointment(filtered_slots, patient)

        elif user_action.isdigit():
            # Check if the user has selected a valid slot
            slot_index = int(user_action) - 1
            if slot_index < 0 or slot_index >= len(available_slots):
                print("\n\033[91mInvalid selection. Please try again.\033[0m")
                return self.book_appointment(patient)

            selected_slot = available_slots[slot_index]

            # Check once again if the selected slot is still valid, if not then it will redirec the user to the home page
            appt_slot_time = datetime.strptime(f"{selected_slot.date} {selected_slot.start_time}", "%d-%m-%Y %H:%M")

            if appt_slot_time < datetime.now() + timedelta(hours=2):
                print("\n\033[91mYou cannot proceed with this booking because the appointment time is now less than two hours away.\033[0m")
                input("Press Enter to return to the patient home page.")
                return self.patient_home(patient)
            
            #If eeverything is valid, then proceed to finalise the appointment
            return self._finalise_appointment(available_slots, patient, slot_index)

        else:
            raise ValueError(f"Invalid user_action:{user_action} argument returned to book_appointment() in MPMS Class.")


    def _finalise_appointment(self, slots, patient, slot_index=None):
        if slot_index is None:
            user_action = self.menu.show_appointment_slots_page(slots)
            if user_action == "logout":
                return self.logout(patient)
            elif user_action == "back":
                return self.book_appointment(patient)
            elif not user_action.isdigit():
                return self.book_appointment(patient)
            slot_index = int(user_action) - 1

        confirmed_slot = slots[slot_index]
        confirmed_slot.set_availability(False)
        FileIO.save_appointment_slots(self.appointment_slots)

        booked_appointment = Appointment(
            slot=confirmed_slot,
            status="Booked",
            email=patient.get_email()
        )
        self.appointments.append(booked_appointment)
        FileIO.save_appointment(booked_appointment)
        self.menu.show_booking_success_page(booked_appointment)
        self.patient_home(patient)
    
    def check_appointment_booking_validity(self, appointment):
        """
        Check if the user is booking the appointment within 2 hours of the appointment time.
        """
        app_datetime_str = f"{appointment.date} {appointment.start_time}"
        appointment_datetime = datetime.strptime(app_datetime_str, "%d-%m-%Y %H:%M")
        current_time = datetime.now()
        time_diff = appointment_datetime - current_time

        if time_diff < timedelta(hours=2):
            print("\033[91m You cannot book an appointment within 2 hours of the appointment time. \033[0m")
            return False
        return True
     
    def upcoming_appointments(self,patient):
        upcoming_appts = self.get_patient_appointments(email=patient.get_email(), type="Booked")
        
        user_action = self.menu.show_upcoming_appointments_page(upcoming_appts)
        if user_action == "logout":
            self.logout(patient)
        elif user_action == "back":
            self.patient_home(patient)
        elif user_action == "cancel":
            user_action = input("\n Enter the Slot Number of the Appointment to Cancel or type 'BACK' to return to the Home Page: ").strip().lower()
            if user_action == "BACK":
                self.patient_home(patient)
                return
            elif user_action.isdigit():
                appointment_index = int(user_action) - 1

                if 0 <= appointment_index < len(upcoming_appts):
                    appointment_to_cancel = upcoming_appts[appointment_index]
                    self.cancel_appointment(patient, appointment_to_cancel)
        
                else:
                    print("\033[91m!! Invalid selection. Please try again !!\033[0m")
                    self.upcoming_appointments(patient)

            else:
                print("\033[91m!! Invalid input. Please enter a Slot number or 'Back' to return to the Home Page !!\033[0m")
                self.upcoming_appointments(patient)


    def cancel_appointment(self, patient, appointment):
        # app_datetime_str = f"{appointment.date} {appointment.start_time}"
        appt_slot_details = appointment.get_slot() #Get slot instance as all details are stored there
        if len(appt_slot_details.get_start_time()) == 2:
            app_datetime_str = f"{appt_slot_details.get_date()} {appt_slot_details.get_start_time()}:00"
        else:
            app_datetime_str = f"{appt_slot_details.get_date()} {appt_slot_details.get_start_time()}"

        appointment_datetime = datetime.strptime(app_datetime_str, "%d-%m-%Y %H:%M")

        current_time = datetime.now()
        time_diff = appointment_datetime - current_time

        # if time_diff > timedelta(hours=24):
        #     input1 = self.menu.show_cancellation_confirmation_page(appointment)
        # else:
        #     input1 = self.menu.show_cancellation_confirmation_page(appointment)

        if time_diff < timedelta(hours=24):
            print("\033[91m This cancellation is within 24 hours of the appointment time. \033[0m")
            print("\033[91m A cancellation fee will be applied if you wish to proceed. \033[0m")
            
        input1 = self.menu.show_cancellation_confirmation_page(appointment)
        if input1 == "CONFIRM":
            self.complete_cancellation(patient, appointment)
        elif input1 == "BACK":
            self.upcoming_appointments(patient)
        elif input1 == "LOGOUT":
            self.logout(patient)
        else:
            print("\033[91m Unrecognized option. Please try again.\033[0m")
            self.cancel_appointment(patient, appointment)    

    # Remove the booked appoointment from appointments.txt
    def complete_cancellation(self, patient, appointment):
        with open("src/appointments.txt", "r") as file:
            lines = file.readlines()

        with open("src/appointments.txt", "w") as file:
            for line in lines:
                if not line.startswith(f"{appointment.get_email()}|{appointment.get_slot().get_clinic_name()}|{appointment.get_slot().get_gp_name()}|{appointment.get_slot().get_date()}|{appointment.get_slot().get_start_time()}"):
                    file.write(line)

        slots = self.appointment_slots
        for slot in slots:
            if (
                slot.get_clinic_name() == appointment.get_slot().get_clinic_name() and
                slot.get_gp_name() == appointment.get_slot().get_gp_name() and
                slot.get_date() == appointment.get_slot().get_date() and
                slot.get_start_time() == appointment.get_slot().get_start_time()
                ):
                slot.set_availability(True)
                slot.set_status("Available")

        appointment.set_status("Cancelled by Patient")
        FileIO.save_appointments(self.appointments)

        FileIO.save_appointment_slots(slots)
        self.appointment_slots = slots

        self.menu.show_cancellation_success_page(appointment)
        self.patient_home(patient)

    def export_report(self, admin, report_data, type):
        user_action = self.menu.show_report_export_page(report_data[0])
        if user_action == "back":
            self.generate_report(admin, type)
        elif user_action == "logout":
            self.is_user_admin = False # Set to False as admin is logging out
            self.user_login()
        elif user_action == "txt":
            FileIO.export_report(format=".txt", report_data=report_data[0])
            self.menu.show_export_success_page(report_data[0])
            self.generate_report(admin, type)
        elif user_action == "csv":
            FileIO.export_report(format=".csv", report_data=report_data[1])
            self.menu.show_export_success_page(report_data[1])
            self.generate_report(admin, type)
        else:
            raise ValueError(f"Invalid value returned from show_report_export_page: {user_action} to export_report() in MPMS")
    
    def generate_report(self, admin, type):
        if type == "reason":
            report_data = Report.generate_appt_reason_report(self.appointments)
        elif type == "TDB":
            pass
        user_action = self.menu.show_view_report_page(report_data[0])
        if user_action == "back":
            self.admin_home(admin)
        elif user_action == "logout":
            self.is_user_admin = False # Set to False as admin is logging out
            self.user_login()
        elif user_action == "export":
            self.export_report(admin, report_data, type)
        else:
            raise ValueError(f"Invalid user_action:{user_action} returned to user_profile_page() in MPMS Class.")

    def get_patient_appointments(self, email, type):
        '''
        Returns a list of appointments that are associated with the given user email.
        The returned list depends on the type requested.

        Args:
            email (str): email of the user whose appointments are to be returned
            type (str):  type of appointments that are to be returned
                        Values: "Booked", "Previous", "All"

        Returns:
            list<Appointment>: A list of appointment instances of given type associated to given email
        '''
        booked_appointments = []
        previous_appointments = []
        for appointment in self.appointments:
            if email == appointment.get_email():
                if appointment.get_status() == "Booked":
                    booked_appointments.append(appointment)
                else:
                    previous_appointments.append(appointment)
        if type == "Booked":
            return booked_appointments
        elif type == "Previous":
            return previous_appointments
        else:
            return booked_appointments + previous_appointments
    
    def get_user_object(self, email, user_type):
        if user_type == "patient":
            user_list = self.patients
        elif user_type == "admin":
            for admin in self.admins:
                user_list = self.admins
        else:
            raise ValueError(f"Invalid user_type:{user_type} passed to get_user_object() in MPMS Class.")
        for user in user_list:
            if user.get_email() == email:
                return user

    def get_valid_user_details(self, user_type):
        valid_details = {}
        if user_type == "admin":
            user_list = self.admins
        else:
            user_list = self.patients
        for user in user_list:
            valid_details[user.get_email()] = user.get_password()
        return valid_details

    def load_system_state(self):
        self.appointment_slots = FileIO.load_appointment_slots(appointment_slot_class=AppointmentSlot)
        self.patients = FileIO.load_patients(patient_class=Patient)
        self.appointments = FileIO.load_appointments(appointment_class=Appointment, appointment_slot_class=AppointmentSlot)
        self.admins = FileIO.load_admins(admin_class=Admin)
    
    def logout(self, user):
        if isinstance(user, Patient):
            self.user_login()
        elif isinstance(user, Admin):
            self.is_user_admin = False
            self.user_login()
        else:
            raise ValueError(f"Invalid user object argument:{user} passed to logout() in MPMS Class.")
    
    def patient_home(self, patient):
        """
        This function contains the logic for the Patient Home Page to display UI, take input and route user.

        Args:
            patient (Patient):  The object of current user of the system.
        """
        user_action = self.menu.show_patient_home_page(attempt_number=0)
        if user_action == "logout":
            self.logout(patient)
        elif user_action == "profile_page":
            self.user_profile_page(patient)
        elif user_action == "book_appointment":
            self.book_appointment(patient)
        elif user_action == "previous_appointments":
            self.previous_appointments(patient)
        elif user_action == "upcoming_appointments":
            self.upcoming_appointments(patient)
            
        else:
            raise ValueError(f"Invalid user_action:{user_action} returned to patient_home() in MPMS Class.")

    def previous_appointments(self, patient):
        """
        Display a list of the patient's previous appointments.
        
        Args:
            patient (Patient): The patient object
        """
        previous_appts = self.get_patient_appointments(email=patient.get_email(), type="Previous")
        user_action = self.menu.show_previous_appointments_page(previous_appts)
        
        if user_action == "logout":
            self.logout(patient)
        elif user_action == "back":
            self.patient_home(patient)
        
        #self.patient_home(patient)

    def set_is_user_admin(self, value):
        self.is_user_admin = value

    def start_app(self):
        """
        Starts the MPMS Application.
        """
        self.load_system_state()
        self.user_login()  # Calls user login functionality.
    
    def user_login(self):
        """
        This function contains the logic for MPMS Login Page to display UI, take input and route user for the  
        """
        patient_details = self.get_valid_user_details(user_type="patient")
        admin_details = self.get_valid_user_details(user_type="admin")
        
        user_action, email = self.menu.show_login_page(valid_patient_details=patient_details, valid_admin_details=admin_details)
        if user_action == "exit":
            exit(0)
        elif  user_action == "patient_home_page":
            patient = self.get_user_object(user_type="patient", email=email)
            self.patient_home(patient)
        elif user_action == "admin_home_page":
            self.is_user_admin = True
            admin = self.get_user_object(user_type="admin", email=email)
            self.admin_home(admin)
        else:
            raise ValueError(f"Invalid user_action:{user_action} returned to user_login() in MPMS Class.")

    def user_profile_page(self, user):
        user_action = self.menu.show_profile_page(user_obj=user, attempt_number=0, is_user_admin=self.is_user_admin)
        if user_action == "back":
            if isinstance(user, Admin):
                self.admin_home(user)
            else:
                self.patient_home(user)
        elif user_action == "logout":
            self.is_user_admin = False # Set to False irrespective of user class for safety.
            self.user_login()
        else:
            raise ValueError(f"Invalid user_action:{user_action} returned to user_profile_page() in MPMS Class.")

if __name__ == "__main__":
    mpms = MPMS()
    mpms.start_app()