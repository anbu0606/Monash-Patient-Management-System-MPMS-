from menu import Menu
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
    
    
    def admin_cancel_patient_appointment(self, admin, page=1, page_size=5):
        """
    This function contains the logic for the Admin Cancel Patient Appointment. 
    It displays appointments booked by pateints and allows the admin to cancel a patient's appointment.
    It then provides the option to make the slot available again for other patients or not.
    Args:
        admin (Admin):  Stores the admin object.
        page (int): Current page number for pagination.
        page_size (int): Number of appointments to display per page.
    
    """
        self.menu.clear_screen()
        print(self.menu.banner)
        print("""
                                                        ADMIN: CANCEL PATIENT APPOINTMENT
        """)
        
        #print("\n--- Admin: Cancel a Patient's Appointment ---")

        # Filter booked appointments only
        booked_appointments = [appt for appt in self.appointments if appt.get_status() == "Booked"]
        
        # If no booked appointments, inform the admin
        if not booked_appointments:
            print("\033[91mNo booked appointments available to cancel.\033[0m")
            self.menu.show_prompt(type="logout")
            self.menu.show_prompt(type="back")
            
            user_input = input("Your Input: ").strip()
            if Validator.is_input_logout(user_input):
                return self.logout(admin)
            elif Validator.is_input_back(user_input):
                return self.admin_home(admin)
            else:
                return self.admin_cancel_patient_appointment(admin, page, page_size)

        print("\n--- List of Booked Patient Appointments ---")
        print("-" * 60)

        # Paginate and display appointments
        pagination = self.menu.paginate_items(booked_appointments, page_size, page)
        current_appointments = pagination["items"]

        # Display pagination information
        print(f"Showing {pagination['showing_from']}-{pagination['showing_to']} of {pagination['total_items']} appointments (Page {pagination['current_page']} of {pagination['total_pages']})\n")


        # Display booked appointments with index
        for i, appt in enumerate(current_appointments, 1):
            actual_index = pagination['showing_from'] - 1 + i
            print(f"\nAppointment {actual_index}:")
            print(f"  Patient Email: {appt.get_email()}")
            print(f"  GP: {appt.get_slot().get_gp_name()}")
            print(f"  Date: {appt.get_slot().get_date()}")
            print(f"  Time: {appt.get_slot().get_start_time()}")
            print(f"  Duration: {appt.get_slot().get_duration()} minutes")
            print(f"  Clinic: {appt.get_slot().get_clinic_name()}")
            print(f"  Suburb: {appt.get_slot().get_clinic_suburb()}")
            print(f"  Reason: {appt.get_slot().get_reason_for_visit()}")
            print("-" * 60)

        # Show pagination navigation options
        if pagination["total_pages"] > 1:
            print("\nNavigation options:")
            if pagination["has_prev"]:
                print("P - Previous page")
            if pagination["has_next"]:
                print("N - Next page")

        # Ask admin to select an appointment
        print("\nEnter the number of the appointment to cancel")
        self.menu.show_prompt(type="logout")
        self.menu.show_prompt(type="back")
    
        user_input = input("Your Input: ").strip()
        if Validator.is_input_back(user_input):
            return self.admin_home(admin)
        elif Validator.is_input_logout(user_input):
            return self.logout(admin)
        elif user_input == "P" and pagination["has_prev"]:
            return self.admin_cancel_patient_appointment(admin, page-1, page_size)
        elif user_input == "N" and pagination["has_next"]:
            return self.admin_cancel_patient_appointment(admin, page+1, page_size)

        # Handle appointment selection
        if not user_input.isdigit():
            print("\033[91mInvalid input. Please enter a valid appointment number, P, N, BACK, or LOGOUT.\033[0m")
            input("Press Enter to continue...")
            return self.admin_cancel_patient_appointment(admin, page, page_size)
        
        appointment_number = int(user_input)
        if appointment_number < 1 or appointment_number > len(booked_appointments):
            print("\033[91mInvalid selection. Please enter a valid appointment number.\033[0m")
            input("Press Enter to continue...")
            return self.admin_cancel_patient_appointment(admin, page, page_size)

        # Get the selected appointment
        selected_appt = booked_appointments[appointment_number - 1] 

        # Confirm cancellation
        confirmation_result = self.menu.show_cancellation_confirmation_page(selected_appt).strip().upper()

        if confirmation_result == "BACK":
            return self.admin_cancel_patient_appointment(admin, page, page_size)
        elif confirmation_result == "LOGOUT":
            return self.logout(admin)
        elif confirmation_result != "CONFIRM":
            print("\033[91mInvalid input. Please enter 'CONFIRM', 'BACK', or 'LOGOUT'.\033[0m")
            input("Press Enter to continue...")
            return self.admin_cancel_patient_appointment(admin, page, page_size)

        # Ask whether to make the slot available to other patients again
        while True:
            availability_choice = input("Make this slot available for other patients? (yes/no/BACK/LOGOUT): ").strip().lower()
            
            if availability_choice == "logout":
                return self.logout(admin)
            elif availability_choice == "back":
                return self.admin_cancel_patient_appointment(admin, page, page_size)
            elif availability_choice == "yes":
                make_slot_available = True
                break
            elif availability_choice == "no":
                make_slot_available = False
                break
            else:
                print("\033[91mInvalid input. Please enter 'yes', 'no', 'BACK', or 'LOGOUT'.\033[0m")


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
        # Displays the admin home page with all the options
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
            self.manage_appointment_slots(admin)
        elif user_action == "manage_clinics":
            self.manage_clinics(admin)
        elif user_action == "manage_gp":
            self.manage_gps(admin)
        elif user_action == "manage_patient_appointments":
            self.admin_cancel_patient_appointment(admin)
        else:
            raise ValueError(f"Invalid user_action:{user_action} returned to admin_home() in MPMS Class.")
    
    def book_appointment(self, patient, enable_skip = False):
        """
        This function contains the logic for the Book Appointment feature.
        It enables the user to filter the appointment slots based on date, GP name, and suburb.
        If the patient chooses to filter by date or GP name, they can also choose to book using their preferred GP.
        Args:
            patient (Patient):  The object of current user of the system.
            enable_skip (bool):  If True, allows the user to skip the filter step.
        """
        slots = self.appointment_slots        
        # Displays the available slots to the user
        available_slots = [slot for slot in slots if Validator.is_booking_valid(slot)]
       
       #If there are no available slots, inform the user and return to the patient home page
        if not available_slots:
            print("\n\033[91mNo appointment slots are currently available (must be at least 2 hours ahead).\033[0m")
            while True:
                user_input = input("Type 'LOGOUT' to return to Login Page or 'BACK' to return to the Home Page: ").strip().upper()
                if user_input == "LOGOUT":
                    return self.logout(patient)
                elif user_input == "BACK":
                    return self.patient_home(patient)
                else:
                    print("\033[91mInvalid input. Please type 'LOGOUT' or 'BACK'.\033[0m")

        # Display the available slots to the user
        user_action = self.menu.show_appointment_slots_page(available_slots, is_skip_enabled=enable_skip)

        if user_action == "logout":
            self.logout(patient)
        elif user_action == "back":
            self.patient_home(patient)
        elif user_action == "filter": #If the user wants to filter the slots they can filter by date, GP name or suburb

            while True:
                filter_type = self.menu.show_filter_options(is_skip_enabled=enable_skip)

                if filter_type == "back":
                    return self.book_appointment(patient)
                elif filter_type == "logout":
                    return self.logout(patient)
                elif filter_type not in ["date", "gp_name", "clinic_suburb"]:
                    print("\033[91mInvalid filter option. Please try again.\033[0m")
                    continue  # Re-prompt

                # Get the filter value from the user
                value = self.menu.get_filter_value(filter_type)

                if Validator.is_input_back(value):
                    return self.book_appointment(patient)
                if Validator.is_input_logout(value):
                    return self.logout(patient)
                
                #if they are filtering by date then check if the date is in the correct format
                if filter_type == "date" and not Validator.is_valid_date_format(value):
                    print("\033[91mInvalid date format. Please use DD-MM-YYYY.\033[0m")
                    input("Press Enter to try again...")
                    continue

                # Filter the available slots based on the selected filter type and value
                filtered_slots = [slot for slot in available_slots if getattr(slot, filter_type) and getattr(slot, filter_type).lower() == value.lower()]
                
                # If no slots match the filter, inform the user and re-prompt
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
                return self.finalise_appointment(filtered_slots, patient) #otherwise return the filtered slots to finalise the appointment

        elif user_action.isdigit():
            # Check if the user has selected a valid slot
            slot_index = int(user_action) - 1
            selected_slot = available_slots[slot_index]

            # Check once again if the selected slot is still valid, if not then it will redirec the user to the home page
            appt_slot_time = datetime.strptime(f"{selected_slot.date} {selected_slot.start_time}", "%d-%m-%Y %H:%M")

            if appt_slot_time < datetime.now() + timedelta(hours=2):
                print("\n\033[91mYou cannot proceed with this booking because the appointment time is now less than two hours away.\033[0m")
                input("Press Enter to continue.. ")
                return self.book_appointment(patient)
            
            #If eeverything is valid, then proceed to finalise the appointment
            return self.finalise_appointment(available_slots, patient, slot_index)

        else:
            raise ValueError(f"Invalid user_action:{user_action} argument returned to book_appointment() in MPMS Class.")


    def cancel_appointment(self, patient, appointment):
        """
        
        Handles the cancellation process for a given appointment by a patient.

        Args:
            patient (Patient): The patient object requesting the cancellation.
            appointment (Appointment): The appointment object to be cancelled.

        """
        # app_datetime_str = f"{appointment.date} {appointment.start_time}"
        appt_slot_details = appointment.get_slot() #Get slot instance as all details are stored there
        if len(appt_slot_details.get_start_time()) == 2:
            app_datetime_str = f"{appt_slot_details.get_date()} {appt_slot_details.get_start_time()}:00"
        else:
            app_datetime_str = f"{appt_slot_details.get_date()} {appt_slot_details.get_start_time()}"

        appointment_datetime = datetime.strptime(app_datetime_str, "%d-%m-%Y %H:%M")

        current_time = datetime.now()
        time_diff = appointment_datetime - current_time

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
        Args:
            appointment (Appointment):  The appointment object to check.
        Returns:
            bool:  True if the booking is valid, False otherwise.
        """
        # Joins the date and start time of the appointment to create a datetime string
        app_datetime_str = f"{appointment.date} {appointment.start_time}"
        #Parse the datetime string to a datetime object
        appointment_datetime = datetime.strptime(app_datetime_str, "%d-%m-%Y %H:%M")
        current_time = datetime.now()
        # Calculate the time difference between the appointment time and the current time
        time_diff = appointment_datetime - current_time

        if time_diff < timedelta(hours=2):
            print("\033[91m You cannot book an appointment within 2 hours of the appointment time. \033[0m")
            return False
        return True
     
    # Remove the booked appoointment from appointments.txt
    def complete_cancellation(self, patient, appointment):
        """
        Finalizes the cancellation of a patient's appointment.

        Args:
            patient (Patient): The patient who is cancelling the appointment.
            appointment (Appointment): The appointment to be cancelled.

        """
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

    def create_appointment_slot(self, admin):
        """
            Allows an admin user to create a new appointment slot.

            Args:
                admin (Admin): The admin user performing the operation.        

        """
        user_action = self.menu.show_create_appointment_slot_page()
        if isinstance(user_action, dict):
            new_slot_details = user_action
            new_slot = AppointmentSlot()
            for attr, value in new_slot_details.items():
                setattr(new_slot, attr, value)
            self.appointment_slots.append(new_slot)
            FileIO.save_appointment_slots(self.appointment_slots)
            self.menu.show_creation_success_page(type="Slot", instance_variable=new_slot)
            self.manage_appointment_slots(admin)
        elif user_action == "back":
            self.admin_home(admin)
        elif user_action == "logout":
            self.logout(admin)
        else:
            raise ValueError(f"Invalid value for user_action returned:{user_action} to create_appointment_slot() in MPMS")

    def create_clinic(self, admin):
        """
            Allows an admin user to create a new clinic.

            Args:
                admin (Admin): The admin user performing the operation.        

        """
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
            return self.create_clinic(admin)
        

    def create_gp(self, admin):
        """
            Allows an admin user to create a new GP.

            Args:
                admin (Admin): The admin user performing the operation.        

        """
        clinic_list = [clinic.get_clinic_name() for clinic in self.clinics]
        gp_list = [gp.get_gp_name() for gp in self.gps]
        gp_email_list = [gp.get_email() for gp in self.gps]
        user_action = self.menu.show_create_gp_page(clinic_list, gp_list, gp_email_list)
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
            return self.create_gp(admin)

    
    def delete_appointment_slot(self, admin):
        """
            Allows an admin user to delete an existing appointment slot.

            Args:
                admin (Admin): The admin user performing the operation.        

        """
        slots = self.get_slots_for_management()
        user_action = self.menu.show_delete_appointment_slot_page(slots)
        if isinstance(user_action, AppointmentSlot): #Appointment Slot instance returned.
            deleted_slot = user_action
            self.appointment_slots.remove(deleted_slot)
            FileIO.save_appointment_slots(self.appointment_slots)
            self.menu.show_deletion_confirmation_page(type = "slot", instance_variable = deleted_slot )
            self.manage_appointment_slots(admin)
        elif user_action == "back":
            self.manage_appointment_slots(admin)
        elif user_action == "logout":
            self.logout(admin)
        else:
            raise ValueError(f"Invalid value for user_action:{user_action} received in delete_appointment_slot() in MPMS")

    
    def delete_clinic(self, admin):
        """
            Allows an admin user to delete an existing clinic.

            Args:
                admin (Admin): The admin user performing the operation.        

        """
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
            return self.delete_clinic(admin)
        

    def delete_gp(self, admin):
        """
            Allows an admin user to delete an existing GP.

            Args:
                admin (Admin): The admin user performing the operation.        

        """
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
            return self.delete_gp(admin)

    def export_report(self, admin, report_data, type):
        """
        Handles exporting of a generated report in TXT or CSV format based on admin input.

        Args:
            admin (Admin): The admin user performing the export.
            report_data (list): A list containing the versions of the report
            type (str): A string indicating the type of report being exported

        """
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
        
    def finalise_appointment(self, slots, patient, slot_index=None):
        """
        This function finalises the appointment booking process.
        It sets the selected slot as unavailable and creates a new appointment object.
        Args:
            slots (list<AppointmentSlot>):  List of available appointment slots.
            patient (Patient):  The object of current user of the system.
            slot_index (int):  Index of the selected appointment slot.
        """
        #If no specified slot index, then show the appointment slots page to the user
        if slot_index is None:
            user_action = self.menu.show_appointment_slots_page(slots) #show available slots to the user
            if user_action == "logout":
                return self.logout(patient)
            elif user_action == "back":
                return self.book_appointment(patient)
            elif not user_action.isdigit():
                return self.book_appointment(patient)
            slot_index = int(user_action) - 1 #convert the user input to an integer
        #retrieve the selected slot and mark it as unavailable
        confirmed_slot = slots[slot_index]
        confirmed_slot.set_availability(False)
        # Save the updated appointment slots to the file
        FileIO.save_appointment_slots(self.appointment_slots)
        # Create a new appointment object
        booked_appointment = Appointment(
            slot=confirmed_slot,
            status="Booked",
            email=patient.get_email()
        )
        #Add the booked appointment to the list of appointments and save it
        self.appointments.append(booked_appointment)
        FileIO.save_appointment(booked_appointment)
        #Show the confirmation page to the user
        self.menu.show_booking_success_page(booked_appointment)
        self.patient_home(patient)
    
    def generate_report(self, admin, type):
        """
        Generates a report based on the selected type ('reason' or 'gp') and a specified date range.

        Args:
            admin (Admin): The admin user requesting the report.
            type (str): The type of report to generate.
        """
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
        """
        Identifies appointment slots from the user's upcoming appointments that are not
        present in the system's master list of appointment slots.

        Args:
            associated_upcoming_slots (list): A list of AppointmentSlot objects associated with a patient.

        """
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
    
    def get_slots_for_management(self):
        '''
        A function to get all available slots and all unavailable slots that are not associated with an appointment
        and are not from the past.

        Returns:
            slots(list): List of all slots that the admin can manage.
        ''' 
        available_slots = [slot for slot in self.appointment_slots if slot.get_availability()] # Get all available slots
        unavailable_slots = [slot for slot in self.appointment_slots if not slot.get_availability()] # Get all unavailable slots

        # Filter unavailable slots to only contain valid slots -- slots that are not associated with an appointment or from the past.
        for appointment in self.appointments:
            occupied_slot = appointment.get_slot() # Get slot associated with Appointment
            for slot in unavailable_slots:
                if str(slot) == str(occupied_slot):
                    unavailable_slots.remove(slot) # Remove is match.
                if datetime.strptime(slot.get_date() + slot.get_start_time(), "%d-%m-%Y%H:%M") < datetime.now() and slot in unavailable_slots:
                    unavailable_slots.remove(slot) # Remove if appointment from past.
        return available_slots + unavailable_slots
    
    def get_user_object(self, email, user_type):
        """
        Retrieves a user object (Patient or Admin) based on the provided email and user type.

        Args:
            email (str): The email address of the user to retrieve.
            user_type (str): The type of user to search for ("patient" or "admin").
        """
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
        """
        Returns a dictionary of valid login credentials (email and password) for all users
        of the specified type.

        Args:
            user_type (str): The type of user ("patient" or "admin").
        """
        valid_details = {}
        if user_type == "admin":
            user_list = self.admins
        else:
            user_list = self.patients
        for user in user_list:
            valid_details[user.get_email()] = user.get_password()
        return valid_details

    def load_system_state(self):
        """
            Loads the current system state from the persistent storage.
        """
        self.appointment_slots = FileIO.load_appointment_slots(appointment_slot_class=AppointmentSlot)
        self.patients = FileIO.load_patients(patient_class=Patient)
        self.appointments, associated_upcoming_slots = FileIO.load_appointments(appointment_class=Appointment, appointment_slot_class=AppointmentSlot)
        self.appointment_slots += self.get_non_duplicate_slots(associated_upcoming_slots)
        FileIO.save_appointment_slots(self.appointment_slots)
        self.admins = FileIO.load_admins(admin_class=Admin)
        self.clinics = FileIO.load_clinics(clinic_class=Clinic)
        self.gps = FileIO.load_gp(gp_class=Gp)
    
    def logout(self, user):
        """
        Logs out the current user and returns to the login page.

    Args:
        user (object): The user object to log out. Must be an instance of Patient or Admin.

        """
        if isinstance(user, Patient):
            self.user_login()
        elif isinstance(user, Admin):
            self.is_user_admin = False
            self.user_login()
        else:
            raise ValueError(f"Invalid user object argument:{user} passed to logout() in MPMS Class.")

    def manage_appointment_slots(self, admin):
        '''
        Handles the Manage Appointment Slots function for Admins.
        Args:
            admin(Admin): Admin instance variable
        '''
        slots = self.get_slots_for_management()
        user_action = self.menu.show_appointment_slot_management_page(slots)
        if user_action == "logout":
            self.logout(admin)
        elif user_action == "back":
            self.admin_home(admin)
        elif user_action == "update":
            self.update_appointment_slot(admin)
        elif user_action == "create":
            self.create_appointment_slot(admin)
        elif user_action == "delete":
            self.delete_appointment_slot(admin)
        else:
            raise ValueError(f"Invalid user_action received:{user_action} from show_clinic_management_page in manage_clinics() in MPMS class")

    def manage_clinics(self,admin):
        """
        Displays all the clinics in the system.
        
        Args:
            admin(Admin): Admin instance variable

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

        Args:
            admin(Admin): Admin instance variable

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
        elif user_action == "slots":
            self.view_gp_slots(admin)
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
        
        

    def set_is_user_admin(self, value):
        """
        Sets the user role flag to indicate whether the current user is an admin.

    Args:
        value (bool): True if the user is an admin, False otherwise.

        """
        self.is_user_admin = value

    def start_app(self):
        """
        Starts the MPMS Application.
        """
        self.load_system_state()
        self.user_login()  # Calls user login functionality.
    
    def upcoming_appointments(self,patient):
        """
        Display the patient's upcoming booked appointments and handle user actions 
        related to viewing, cancelling, or navigating from the upcoming appointments page.

        Args:
            patient (Patient): The patient object whose upcoming appointments are to be displayed.

        """
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

    def update_appointment_slot(self, admin):
        '''
        Handles the updating of Appointment Slots as a function for admins.
        Args:
            admin(Admin): Admin instance variable
        '''
        slots = self.get_slots_for_management()
        user_action = self.menu.show_appointment_slot_update_page(slots)
        if user_action == "back":
            self.manage_appointment_slots(admin)
        elif user_action == "logout":
            self.logout(admin)
        elif user_action.isdigit():
            slot_index = int(user_action) - 1
            slot_to_update = slots[slot_index]
            updated_slot_details = self.menu.show_appointment_slot_update_menu(slot_to_update, attempt_number=0)
            for attr, value in updated_slot_details.items():
                setattr(slot_to_update, attr, value)
            FileIO.save_appointment_slots(self.appointment_slots)
            self.menu.show_update_success_page(type="slot", instance_variable=slot_to_update)
            self.manage_appointment_slots(admin)
        else:
            raise ValueError(f"Invalid useraction:{user_action} returned to update_appointment_slot() in MPMS.")

    def update_clinic(self, admin):
        """
        Allows an admin user to update the details of a selected clinic.

        Args:
            admin (Admin): The admin user performing the update.

        """
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
        """
        Allows an admin user to update the details of a selected GP.

        Args:
            admin (Admin): The admin user performing the update.
        """
        Clinic_list = [clinic.get_clinic_name() for clinic in self.clinics]
        gp_list = [gp.get_gp_name() for gp in self.gps]
        gp_email_list = [gp.get_email() for gp in self.gps]
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
        while True:
            new_name = input(f"New Name ({gp_to_update.get_gp_name()}): ") or gp_to_update.get_gp_name()
            if new_name == "" or not Validator.is_valid_gp_name(new_name, gp_list.remove(gp_to_update.get_gp_name())):
                is_input_valid = False
                print("\033[91m!! Invalid Name. Please enter new name. !!\033[0m")
                continue

            if Validator.is_valid_gp_name(new_name, gp_list):
                break
            else:
                print("\033[91m!! Invalid Name. Please enter new name. !!\033[0m") 
        while True:
            new_email = input(f"New Email ({gp_to_update.get_email()}): ") or gp_to_update.get_email()
            if new_email == "" or not Validator.is_valid_email(new_email, gp_email_list.remove(gp_to_update.get_email())):
                is_input_valid = False
                print("\033[91m!! Invalid Email id Format. Please enter a valid id. !!\033[0m") 
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
        """

        Display the profile page for the given user and handle navigation actions.

        Args:
            user (Admin or Patient): The user object whose profile is being displayed.

        """
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
    
    def view_gp_slots(self, admin,enable_skip = False):
        '''
        Functionality for user to select a GP and view the appointment associated with them.
        Args:
            admin(Admin): The admin instance.
        '''
        gps = self.gps
        user_action = input("\n Enter the Slot Number of the GP to list of all the appointment slots or type 'BACK' to return to the Home Page: ").strip()
        if user_action == "BACK":
            self.admin_home(admin)
        elif user_action.isdigit():
            gp_index = int(user_action) - 1
            if 0 <= gp_index < len(gps):
                selected_gp = gps[gp_index]
            else:
                print("\033[91m!! Invalid selection. Please try again!!\033[0m")
                input("Press Enter to continue.. ")
                self.manage_gps(admin)
        else:
            print("\033[91m!! Invalid input. Please try again!!\033[0m")
            input("Press Enter to continue.. ")
            self.manage_gps(admin)

        gp_slots = []
        for slot in self.get_slots_for_management():
            if slot.get_gp_name().strip().lower() == selected_gp.get_gp_name().strip().lower():
                gp_slots.append(slot)
        user_action = self.menu.show_gp_appointment_slots(gp_slots, selected_gp.get_gp_name())
        if user_action == "back":
            self.manage_gps(admin)
        elif user_action == "logout":
            self.logout(admin)
        elif user_action == "filter":

            while True:
                filter_type = self.menu.show_clinic_filter_option(is_skip_enabled=enable_skip)

                if filter_type == "back":
                    return self.view_gp_slots(admin)
                elif filter_type == "logout":
                    return self.logout(admin)
                elif filter_type not in ["clinic_suburb"]:
                    print("\033[91mInvalid filter option. Please try again.\033[0m")
                    continue  # Re-prompt

                # Get the filter value from the user
                value = self.menu.get_filter_value(filter_type)

                if Validator.is_input_back(value):
                    return self.view_gp_slots(admin)
                if Validator.is_input_logout(value):
                    return self.logout(admin)
                

                # Filter the available slots based on the selected filter type and value
                filtered_slots = [slot for slot in gp_slots if getattr(slot, filter_type) and getattr(slot, filter_type).lower() == value.lower()]
                
                # If no slots match the filter, inform the user and re-prompt
                if not filtered_slots:
                    print("\033[91mNo matching slots found. Press Enter to try again.\033[0m")
                    input()
                    continue  # Go back to filter option selection
                user_action = self.menu.show_gp_appointment_slots(filtered_slots, selected_gp.get_gp_name())
                
        else:
            raise ValueError(f"Invalid value for user_action:{user_action} received in delete_gp() in MPMS")


if __name__ == "__main__":
    mpms = MPMS()
    mpms.start_app()