from patient import Patient
from admin import Admin
from menu import Menu
from mpms import MPMS
from appointment import Appointment
from appointment_slot import AppointmentSlot
from fileio import FileIO
from report import Report
from clinic import Clinic

menu = Menu()
mpms = MPMS()
menu.clear_screen()

clinics = FileIO.load_clinics(Clinic)

for clinic in clinics:
    print(str(clinic)[:-2])