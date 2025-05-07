from patient import Patient
from admin import Admin
from menu import Menu
from mpms import MPMS
from appointment import Appointment

menu = Menu()
mpms = MPMS()
menu.clear_screen()

Patient.load_patients()
patients = Patient.get_patient_list()
patient = patients[0]
temp = Appointment.load_book_appointment(patient.email)
print(temp)
patient.set_upcoming_apppointments(temp)
print(patients[0])

# Admin.load_admins()
# admin_email = "admin@monash.edu"
# admin = Admin.get_admin_object(admin_email)
# print(admin)

# print(isinstance(admin, Admin))

# pd = mpms.get_valid_user_details("patient")
# print(pd)

# ad = mpms.get_valid_user_details("admin")
# print(ad)