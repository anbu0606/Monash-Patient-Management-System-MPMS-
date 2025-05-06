from patient import Patient
from admin import Admin
from menu import Menu
from mpms import MPMS

menu = Menu()
mpms = MPMS()
menu.clear_screen()

Patient.load_patients()
patient_email = "patient1@student.monash.edu"
patient = Patient.get_patient_object(patient_email)
print(patient)

Admin.load_admins()
admin_email = "admin@monash.edu"
admin = Admin.get_admin_object(admin_email)
print(admin)

print(isinstance(admin, Admin))

pd = mpms.get_valid_user_details("patient")
print(pd)

ad = mpms.get_valid_user_details("admin")
print(ad)