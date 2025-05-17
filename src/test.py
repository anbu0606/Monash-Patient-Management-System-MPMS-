from patient import Patient
from admin import Admin
from menu import Menu
from mpms import MPMS
from appointment import Appointment
from fileio import FileIO

menu = Menu()
mpms = MPMS()
menu.clear_screen()

pat_list = FileIO.load_patients(Patient)
for pat in pat_list:
    print(pat.get_email())