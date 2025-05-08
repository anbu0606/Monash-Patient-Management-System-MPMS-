from menu import Menu
from user import User
from patient import Patient
from admin import Admin
from appointment_slot import AppointmentSlot
from appointment import Appointment
from datetime import datetime, timedelta


class MPMS:
    """
    This class contains the core logic of the Monash Patient Management System. 
    """

    def __init__(self):
        """
        Initialises MPMS Class instance.
        """
        self.menu = Menu()
        self.patient_list = [] 
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
        elif user_action == "clinic_report":
            pass
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
    
    def book_appointment(self, patient):
        slots = AppointmentSlot.get_appointment_slot_list()
        available_slots = [slot for slot in slots if slot.availability]
        user_action = self.menu.show_appointment_slots_page(slots)
        if user_action == "logout":
            pass #########################################################3
        elif user_action == "back":
            pass #########################################################
        elif user_action.isdigit():
            slot_index = int(user_action) - 1
            confirmed_slot = available_slots[slot_index]
            confirmed_slot.availability = False
            confirmed_slot.status = "Booked"
            AppointmentSlot.save_appointment_slots(slots)
            booked_appointment = Appointment(
                clinic_name = confirmed_slot.clinic_name,
                gp_name = confirmed_slot.gp_name,
                date = confirmed_slot.date,
                start_time = confirmed_slot.start_time,
                duration = confirmed_slot.duration,
                clinic_suburb = confirmed_slot.clinic_suburb,
                reason_for_visit = confirmed_slot.reason_for_visit,
                availability = False,
                status = "Booked",
                email = patient.email
                )
            patient.append_upcoming_appointments(booked_appointment)
            Appointment.save_appointment(booked_appointment)
            user_action = self.menu.show_booking_success_page(booked_appointment)
            self.patient_home(patient)
        else:
            raise ValueError(f"Invalid user_action:{user_action} argument returned to book_appointment() in MPMS Class.")
    
    def upcoming_appointments(self,patient):
        upcoming_appointments = patient.get_upcoming_appointments()
        for appointment in upcoming_appointments:
            print(appointment)
            print("-"*50)
        # if not upcoming:
        #     print("OOPS! No appointment found! Error 404! ^._.^")
        # else:
        #     for i in upcoming:
        #         print(i)
        user_action = input("\n Enter the Slot Numbert of the Appointment to Cancel or type 'BACK' to return to the Home Page: ").strip().lower()
        if user_action == "BACK":
            self.patient_home(patient)
            return
        elif user_action.isdigit():
            appointment_index = int(user_action) - 1

            if 0 <= appointment_index < len(upcoming_appointments):
                appointment_to_cancel = upcoming_appointments[appointment_index]
                self.cancelling_appointment(patient, appointment_to_cancel)
        
            else:
                print("\n Invalid selection. Please try again.")
                self.upcoming_appointments(patient)

        else:
            print("\n Invalid input. Please enter a Slot number or 'Back' to return to the Home Page.")
            self.upcoming_appointments(patient)


   

    def cancelling_appointment(self, patient, appointment):
        # app_datetime_str = f"{appointment.date} {appointment.start_time}"
        if len(appointment.start_time) == 2:
            app_datetime_str = f"{appointment.date} {appointment.start_time}:00"
        else:
            app_datetime_str = f"{appointment.date} {appointment.start_time}"

        appointment_datetime = datetime.strptime(app_datetime_str, "%d-%m-%Y %H:%M")

        current_time = datetime.now()
        time_diff = appointment_datetime - current_time

        if time_diff > timedelta(hours=24):
            input1 = self.menu.show_cancellation_confirmation_page(appointment)
        else:
            input1 = self.menu.show_cancellation_confirmation_page(appointment)
        
        if input1 == "CONFIRM":
            self.complete_cancellation(patient, appointment)
        elif input1 == "BACK":
            self.upcoming_appointments(patient)
        elif input1 == "LOGOUT":
            self.logout(patient)
        else:
            print("Unrecognized option. Please try again.")
            self.cancelling_appointment(patient, appointment)    


    def complete_cancellation(self, patient, appointment):
        with open("src/booked_appointment.txt", "r") as file:
            lines = file.readlines()

        with open("src/booked_appointment.txt", "w") as file:
            for line in lines:
                if not line.startswith(f"{appointment.email}|{appointment.clinic_name}|{appointment.gp_name}|{appointment.date}|{appointment.start_time}"):
                    file.write(line)

        # print("Removed the booked app from the book_appointment.txt")

        slots = AppointmentSlot.get_appointment_slot_list()
        for slot in slots:
            if (slot.clinic_name == appointment.clinic_name and
                slot.gp_name == appointment.gp_name and
                slot.date == appointment.date and
                slot.start_time == appointment.start_time):
                slot.availability = True
                slot.status = "Available"

        AppointmentSlot.save_appointment_slots(slots)
        # print(f" Successfully updated the appointment slot status to 'Available' in 'appointment_slot.txt'")

        patient.upcoming_appointments = [
            appt for appt in patient.upcoming_appointments
            if not (appt.clinic_name == appointment.clinic_name and
                appt.gp_name == appointment.gp_name and
                appt.date == appointment.date and
                appt.start_time == appointment.start_time)
    ]
        # print("Successfully Cancelled the Appointment")
        input1 = self.menu.show_cancellation_success_page(appointment)
        if input1 == "back":
            self.patient_home(patient)
        elif input1 == "logout":
            self.logout(patient)


    def get_valid_user_details(self, user_type):
        valid_details = {}
        if user_type == "admin":
            user_list = Admin.get_admin_list()
        else:
            user_list = Patient.get_patient_list()
        for user in user_list:
            valid_details[user.email] = user.password
        return valid_details

    def load_system_state(self):
        AppointmentSlot.load_appointment_slots()
        Patient.load_patients()
        self.patient_list = Patient.get_patient_list()
        for patient in self.patient_list:
            patient.set_upcoming_apppointments(Appointment.load_book_appointment(patient.email))
        Admin.load_admins()
    
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
            pass
        elif user_action == "upcoming_appointments":
            self.upcoming_appointments(patient)
            
        else:
            raise ValueError(f"Invalid user_action:{user_action} returned to patient_home() in MPMS Class.")

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
        user_action, email = self.menu.show_login_page(mpms_obj=self)
        if user_action == "exit":
            exit(0)
        elif  user_action == "patient_home_page":
            patient = Patient.get_patient_object(email)
            self.patient_home(patient)
        elif user_action == "admin_home_page":
            self.is_user_admin = True
            admin = Admin.get_admin_object(email)
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