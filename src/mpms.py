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
from clinic import Clinic
from gp import Gp
import re

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
        self.clinics = []
        self.gps =[]
        self.menu = Menu()
        self.patients = []
        self.is_user_admin = False
    
    
    def admin_cancel_patient_appointment(self, admin):
        """
    This function contains the logic for the Admin Cancel Patient Appointment Page to display UI, take input and route user.
    Args:
        admin (Admin):  Stores the admin object.
    """
        print("\n--- Admin: Cancel a Patient's Appointment ---")

        # Filter booked appointments only
        booked_appointments = [appt for appt in self.appointments if appt.get_status() == "Booked"]

        if not booked_appointments:
            print("\033[91mNo booked appointments available to cancel.\033[0m")
            input("Press Enter to return to admin home.")
            return self.admin_home(admin)

        # Display booked appointments with index
        for i, appt in enumerate(booked_appointments, 1):
            print(f"\nAppointment {i}:")
            print(f"  Patient Email: {appt.get_email()}")
            print(appt)

        # Ask admin to select an appointment
        while True:
            choice = input("\nEnter the number of the appointment to cancel, or type BACK/LOGOUT: ").strip()

            if Validator.is_input_back(choice):
                return self.admin_home(admin)
            if Validator.is_input_logout(choice):
                return self.logout(admin)

            if choice.isdigit() and 1 <= int(choice) <= len(booked_appointments):
                selected_appt = booked_appointments[int(choice) - 1]
                break
            else:
                print("\033[91mInvalid selection. Please enter a valid number, BACK, or LOGOUT.\033[0m")

        # Confirm cancellation
        input1 = self.menu.show_cancellation_confirmation_page(selected_appt)
        if input1 == "BACK":
            return self.admin_home(admin)
        elif input1 != "CONFIRM":
            print("\033[91mCancellation not confirmed.\033[0m")
            return self.admin_home(admin)

        # Ask whether to make the slot available again
        availability_choice = input("Make this slot available for other patients? (yes/no): ").strip().lower()
        make_slot_available = availability_choice == "yes"

        # Set appointment status
        selected_appt.set_status("Cancelled by Clinic")

        # Remove appointment from appointments.txt
        with open("src/appointments.txt", "r") as file:
            lines = file.readlines()

        with open("src/appointments.txt", "w") as file:
            for line in lines:
                if not line.startswith(f"{selected_appt.get_email()}|{selected_appt.get_slot().get_clinic_name()}|{selected_appt.get_slot().get_gp_name()}|{selected_appt.get_slot().get_date()}|{selected_appt.get_slot().get_start_time()}"):
                    file.write(line)

        #  Only update the slots availability if admin said YES
        if make_slot_available:
            for slot in self.appointment_slots:
                if (slot.get_clinic_name() == selected_appt.get_slot().get_clinic_name() and
                    slot.get_gp_name() == selected_appt.get_slot().get_gp_name() and
                    slot.get_date() == selected_appt.get_slot().get_date() and
                    slot.get_start_time() == selected_appt.get_slot().get_start_time()):
                    slot.set_availability(True)
                    break
        else:
            # If the admin chooses not to make the slot available again, set its availability to False
            for slot in self.appointment_slots:
                if (slot.get_clinic_name() == selected_appt.get_slot().get_clinic_name() and
                    slot.get_gp_name() == selected_appt.get_slot().get_gp_name() and
                    slot.get_date() == selected_appt.get_slot().get_date() and
                    slot.get_start_time() == selected_appt.get_slot().get_start_time()):
                    slot.set_availability(False)
                    break

        # Save updated appointments and slots
        FileIO.save_appointments(self.appointments)
        FileIO.save_appointment_slots(self.appointment_slots)

        # Show success message and return to admin home
        self.menu.show_cancellation_success_page(selected_appt)
        return self.admin_home(admin)



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
            self.generate_report(admin, "gp")
        elif user_action == "reason_report":
            self.generate_report(admin, "reason")
        elif user_action == "manage_appointment_slots":
            pass
        elif user_action == "manage_clinics":
            self.manage_clinics(admin)
        elif user_action == "manage_gp":
            self.manage_gps(admin)
        elif user_action == "manage_patient_appointments":
            self.admin_cancel_patient_appointment(admin)
        else:
            raise ValueError(f"Invalid user_action:{user_action} returned to admin_home() in MPMS Class.")
    
    def book_appointment(self, patient, enable_skip = False):
        slots = self.appointment_slots
        # for i in slots:
        #     print(i)
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

            while True:
                filter_type = self.menu.show_filter_options(is_skip_enabled=enable_skip)

                if filter_type == "back":
                    return self.book_appointment(patient)
                elif filter_type == "logout":
                    return self.logout(patient)
                elif filter_type not in ["date", "gp_name", "clinic_suburb"]:
                    print("\033[91mInvalid filter option. Please try again.\033[0m")
                    continue  # Re-prompt

                value = self.menu.get_filter_value(filter_type)

                if Validator.is_input_back(value):
                    return self.book_appointment(patient)
                if Validator.is_input_logout(value):
                    return self.logout(patient)

                if filter_type == "date" and not Validator.is_valid_date_format(value):
                    print("\033[91mInvalid date format. Please use DD-MM-YYYY.\033[0m")
                    input("Press Enter to try again...")
                    continue

                filtered_slots = [slot for slot in available_slots if getattr(slot, filter_type) and getattr(slot, filter_type).lower() == value.lower()]

                if not filtered_slots:
                    print("\033[91mNo matching slots found. Press Enter to try again.\033[0m")
                    input()
                    continue  # Go back to filter option selection

                # Show results
                print("\n\033[94mFiltered Appointment Slots:\033[0m")
                for i, slot in enumerate(filtered_slots, 1):
                    print(f"\nSlot {i}:")
                    print(f"  Clinic: {slot.clinic_name}")
                    print(f"  GP: {slot.gp_name}")
                    print(f"  Date: {slot.date}")
                    print(f"  Time: {slot.start_time}")
                    print(f"  Duration: {slot.duration}")
                    print(f"  Suburb: {slot.clinic_suburb}")
                    print(f"  Reason: {slot.reason_for_visit}")
                    print("  ------------------------------------------------------------")

                # Prompt for preferred GP filter if applicable
                if filter_type in ["date", "clinic_suburb"]:
                    further_filter = input("\nWould you like to filter these results by a preferred GP? (yes/no): ").strip().lower()
                    if further_filter == "yes":
                        gp_name = input("Enter preferred GP name: ").strip()
                        filtered_slots = [slot for slot in filtered_slots if slot.gp_name and slot.gp_name.lower() == gp_name.lower()]
                        if not filtered_slots:
                            print("\033[91mNo matching GP found in these results. Press Enter to try again.\033[0m")
                            input()
                            continue  # Re-prompt from filter selection

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

        appointment.set_status("Cancelled by Patient")
        FileIO.save_appointments(self.appointments)

        FileIO.save_appointment_slots(slots)
        self.appointment_slots = slots

        self.menu.show_cancellation_success_page(appointment)
        self.patient_home(patient)

    def create_clinic(self, admin):
        user_action = self.menu.show_create_clinic_page()
        if isinstance(user_action, dict):
            new_clinic = Clinic(
                clinic_name=user_action["clinic_name"],
                suburb=user_action["suburb"],
                available_services=user_action["available_services"],
                operating_hours=user_action["operating_hours"]
            )
            self.clinics.append(new_clinic)
            FileIO.save_clinics(self.clinics)
            self.menu.show_creation_success_page(type="Clinic", instance_variable=new_clinic)
            self.manage_clinics(admin)
        elif user_action == "back":
            self.admin_home(admin)
        elif user_action == "logout":
            self.logout(admin)
        else:
            raise ValueError(f"Invalid value for user_action returned:{user_action} to create_clinic() in MPMS")
        

    def create_gp(self, admin):
        Clinic_list = [clinic.get_clinic_name() for clinic in self.clinics]  
        user_action = self.menu.show_create_gp_page(Clinic_list)
        if isinstance(user_action, dict):
            new_gp = Gp(
                gp_name=user_action["gp_name"],
                email=user_action["email"],
                assigned_clinics=user_action["assigned_clinics"],
                specialisation=user_action["specialisation"],
                availability=user_action["availability"]
            )
            self.gps.append(new_gp)
            FileIO.save_gps(self.gps)
            self.menu.show_creation_success_page(type="Gp", instance_variable=new_gp)
            self.manage_gps(admin)

        elif user_action == "back":
            self.admin_home(admin)
        elif user_action == "logout":
            self.logout(admin)
        else:
            raise ValueError(f"Invalid value for user_action returned:{user_action} to create_gp() in MPMS")








    def delete_clinic(self, admin):
        user_action = self.menu.show_delete_clinic_page(self.clinics)
        if isinstance(user_action, int): #index of clinic instance returned.
            deleted_clinic = self.clinics.pop(user_action)
            FileIO.save_clinics(self.clinics)
            self.menu.show_deletion_confirmation_page(type = "clinic", instance_variable = deleted_clinic )
            self.manage_clinics(admin)
        elif user_action == "back":
            self.manage_clinics(admin)
        elif user_action == "logout":
            self.logout(admin)
        else:
            raise ValueError(f"Invalid value for user_action:{user_action} received in delete_clinic() in MPMS")
        

    def delete_gp(self, admin):
        user_action = self.menu.show_delete_gp_page(self.gps)
        if isinstance(user_action, int): #index of gp instance returned.
            deleted_gp = self.gps.pop(user_action)
            FileIO.save_gps(self.gps)
            self.menu.show_deletion_confirmation_page(type = "gp", instance_variable = deleted_gp )
            self.manage_gps(admin)
        elif user_action == "back":
            self.manage_gps(admin)
        elif user_action == "logout":
            self.logout(admin)
        else:
            raise ValueError(f"Invalid value for user_action:{user_action} received in delete_gp() in MPMS")






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
        
        date_range_result = self.menu.get_report_date_range()
    
        # Check if the result is a string
        if isinstance(date_range_result, str):
            if date_range_result == "back":
                return self.admin_home(admin)
            elif date_range_result == "logout":
                return self.logout(admin)
            else:
                raise ValueError(f"Unexpected result from get_report_date_range: {date_range_result}")
        
        # Otherwise, it's a tuple of (start_date, end_date)
        start_date, end_date = date_range_result

        if type == "reason":
            report_data = Report.generate_appt_reason_report(self.appointments, start_date, end_date)
        elif type == "gp":
            report_data = Report.generate_gp_report(self.appointments, start_date, end_date)
        
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

    def get_non_duplicate_slots(self, associated_upcoming_slots):
        slots_raw_data = []
        non_duplicate_slots = []
        for slot in self.appointment_slots:
            slots_raw_data.append(str(slot))
        for booked_slot in associated_upcoming_slots:
            if str(booked_slot) not in slots_raw_data:
                non_duplicate_slots.append(booked_slot)
        return non_duplicate_slots

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
        for i in self.appointment_slots:
            print(i)
        self.patients = FileIO.load_patients(patient_class=Patient)
        self.appointments, associated_upcoming_slots = FileIO.load_appointments(appointment_class=Appointment, appointment_slot_class=AppointmentSlot)
        self.appointment_slots += self.get_non_duplicate_slots(associated_upcoming_slots)
        FileIO.save_appointment_slots(self.appointment_slots)
        self.admins = FileIO.load_admins(admin_class=Admin)
        self.clinics = FileIO.load_clinics(clinic_class=Clinic)
        self.gps = FileIO.load_gp(gp_class=Gp)
    
    def logout(self, user):
        if isinstance(user, Patient):
            self.user_login()
        elif isinstance(user, Admin):
            self.is_user_admin = False
            self.user_login()
        else:
            raise ValueError(f"Invalid user object argument:{user} passed to logout() in MPMS Class.")

    def manage_clinics(self,admin):
        """
        Displays all the clinics in the system.
        """
        clinics = self.clinics
        user_action = self.menu.show_clinic_management_page(clinics)
        if user_action == "logout":
            self.logout(admin)
        elif user_action == "back":
            self.admin_home(admin)
        elif user_action == "update":
            self.update_clinic(admin)
        elif user_action == "create":
            self.create_clinic(admin)
        elif user_action == "delete":
            self.delete_clinic(admin)
        else:
            raise ValueError(f"Invalid user_action received:{user_action} from show_clinic_management_page in manage_clinics() in MPMS class")
        

    def manage_gps(self,admin):
        """
        Displays all the gps in the system.
        """
        gps = self.gps
        user_action = self.menu.show_gp_management_page(gps)
        if user_action == "logout":
            self.logout(admin)
        elif user_action == "back":
            self.admin_home(admin)
        elif user_action == "update":
            self.update_gp(admin)
        elif user_action == "create":
            self.create_gp(admin)
        elif user_action == "delete":
            self.delete_gp(admin)
        else:
            raise ValueError(f"Invalid user_action received:{user_action} from show_gp_management_page in manage_gps() in MPMS class")




    
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
    
    def upcoming_appointments(self,patient):
        upcoming_appts = self.get_patient_appointments(email=patient.get_email(), type="Booked")
        
        user_action = self.menu.show_upcoming_appointments_page(upcoming_appts)
        if user_action == "logout":
            self.logout(patient)
        elif user_action == "back":
            self.patient_home(patient)
        elif user_action == "cancel":
            user_action = input("\n Enter the Slot Number of the Appointment to Cancel or type 'BACK' to return to the Home Page: ").strip()
            if user_action == "BACK":
                self.patient_home(patient)
            elif user_action.isdigit():
                appointment_index = int(user_action) - 1

                if 0 <= appointment_index < len(upcoming_appts):
                    appointment_to_cancel = upcoming_appts[appointment_index]
                    self.cancel_appointment(patient, appointment_to_cancel)
        
                else:
                    print("\033[91m!! Invalid selection. Please try again. Going back to Upcoming Appointments Page!!\033[0m")
                    input("Press Enter to continue.. ")
                    self.upcoming_appointments(patient)

            else:
                print("\033[91m!! Invalid input. Going back to Upcoming Appointments Page!!\033[0m")
                input("Press Enter to continue.. ")
                self.upcoming_appointments(patient)

    def update_clinic(self, admin):
        clinics = self.clinics
        user_action = input("\n Enter the Slot Number of the Clinic to Update or type 'BACK' to return to the Home Page: ").strip()
        if user_action == "BACK":
            self.admin_home(admin)
        elif user_action.isdigit():
            clinic_index = int(user_action) - 1
            if 0 <= clinic_index < len(clinics):
                clinic_to_update = clinics[clinic_index]
            else:
                print("\033[91m!! Invalid selection. Please try again!!\033[0m")
                input("Press Enter to continue.. ")
                self.manage_clinics(admin)
        else:
            print("\033[91m!! Invalid input. Please try again!!\033[0m")
            input("Press Enter to continue.. ")
            self.manage_clinics(admin)

        print("\n--- Update Clinic Details ---")
        print("\nLeave the field empty if you don't want to change it:")
        new_name = input(f"New Name ({clinic_to_update.get_clinic_name()}): ") or clinic_to_update.get_clinic_name()
        new_suburb = input(f"New Suburb ({clinic_to_update.get_suburb()}): ") or clinic_to_update.get_suburb()
        new_services = input(f"New Services (comma-separated) ({','.join(clinic_to_update.get_available_services())}): ")
        new_services = new_services.split(',') if new_services else clinic_to_update.get_available_services()
        new_hours = input(f"New Operating Hours ({clinic_to_update.get_operating_hours()}): ") or clinic_to_update.get_operating_hours()
        
        clinic_to_update.set_clinic_name(new_name)
        clinic_to_update.set_suburb(new_suburb)
        clinic_to_update.set_available_services(new_services)
        clinic_to_update.set_operating_hours(new_hours)

        FileIO.save_clinics(self.clinics)

        self.menu.show_update_success_page(type="clinic", instance_variable=clinic_to_update)
        self.manage_clinics(admin)


    def update_gp(self, admin):
        Clinic_list = [clinic.get_clinic_name() for clinic in self.clinics]
        gps = self.gps
        user_action = input("\n Enter the Slot Number of the GP to Update or type 'BACK' to return to the Home Page: ").strip()
        if user_action == "BACK":
            self.admin_home(admin)
        elif user_action.isdigit():
            gp_index = int(user_action) - 1
            if 0 <= gp_index < len(gps):
                gp_to_update = gps[gp_index]
            else:
                print("\033[91m!! Invalid selection. Please try again!!\033[0m")
                input("Press Enter to continue.. ")
                self.manage_gps(admin)
        else:
            print("\033[91m!! Invalid input. Please try again!!\033[0m")
            input("Press Enter to continue.. ")
            self.manage_gps(admin)

        print("\n--- Update GP Details ---")
        print("\nLeave the field empty if you don't want to change it:")
        new_name = input(f"New Name ({gp_to_update.get_gp_name()}): ") or gp_to_update.get_gp_name()
        while True:
            new_email = input(f"New Email ({gp_to_update.get_email()}): ") or gp_to_update.get_email()
            if new_email == "":
                is_input_valid = False
                continue

            if re.match(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$', new_email):
                break
            else:
                print("\033[91m!! Invalid Email id Format. Please enter a valid id. !!\033[0m") 
                
        while True:

            new_clinics = input(f"New Clinics (comma-separated) ({','.join(gp_to_update.get_assigned_clinics())}): ")
            
            if not new_clinics:
                new_clinics = gp_to_update.get_assigned_clinics()
                break
            new_clinics = [clinic.strip() for clinic in new_clinics.split(',')]

            is_valid, valid_clinics, invalid_clinics = Validator.is_valid_clinic_list(
            new_clinics, Clinic_list
        )

            if is_valid:
                new_clinics = valid_clinics
                break
            else:
                print(f"\033[91m!! These clinics are not valid: {', '.join(invalid_clinics)} !!\033[0m")
                print("Please re-enter the clinic names correctly.")

        new_specialisation = input(f"New specialisation (comma-separated) ({','.join(gp_to_update.get_specialisation())}): ")
        new_specialisation = new_specialisation.split(',') if new_specialisation else gp_to_update.get_specialisation()

        new_availability = input(f"New Operating Hours ({gp_to_update.get_availability()}): ") or gp_to_update.get_availability()
        
        gp_to_update.set_gp_name(new_name)
        gp_to_update.set_email(new_email)
        gp_to_update.set_assigned_clinics(new_clinics)
        gp_to_update.set_specialisation(new_specialisation)
        gp_to_update.set_availability(new_availability)

        FileIO.save_gps(self.gps)

        self.menu.show_update_success_page(type="gp", instance_variable=gp_to_update)
        self.manage_gps(admin)



    
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