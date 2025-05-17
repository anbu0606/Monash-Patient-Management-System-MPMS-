class Report:
    def __init__(self):
        pass 
    
    @staticmethod
    def generate_appt_reason_report(appointments):
        appt_reason_statistics = {}
        for appointment in appointments:
            reason = appointment.get_slot().get_reason_for_visit()
            if reason in appt_reason_statistics.keys():
                appt_reason_statistics[reason] = appt_reason_statistics[reason] + 1
            else:
                appt_reason_statistics[reason] = 1
        
        report_txt_data = []
        report_csv_data = [r"Appointment Reason,Number of Appointments,% of Total No of Appointments"+"\n"]
        for reason, number_of_appts in appt_reason_statistics.items():
            percentage_of_appts = number_of_appts/len(appointments) * 100

            reason_cell = reason.center(28)
            number_cell = str(number_of_appts).center(24)
            percent_cell = (str(percentage_of_appts) + "%").center(32)
            report_txt_data.append(f"|{reason_cell}|{number_cell}|{percent_cell}|")

            report_csv_data.append(f"{reason},{number_of_appts},{percentage_of_appts}\n")

        report_txt_data = "\n".join(report_txt_data)
        txt_report = f"""
                           Automatically Generated Report
----------------------------------------------------------------------------------------

                 >> Report on Appointment Distribution by Reason <<

|     Appointment Reason     | Number of Appointments |  % of Total No of Appointments |
----------------------------------------------------------------------------------------
{report_txt_data}

"""     
        return [txt_report, report_csv_data]