from patient import Patient
from admin import Admin
from menu import Menu
from mpms import MPMS
from appointment import Appointment
from appointment_slot import AppointmentSlot
from fileio import FileIO
from report import Report

menu = Menu()
mpms = MPMS()
menu.clear_screen()

appointments = FileIO.load_appointments(Appointment, AppointmentSlot)

report_data = Report.generate_appt_reason_report(appointments)
Report.export_report(".txt", report_data[0])
Report.export_report(".csv", report_data[1])