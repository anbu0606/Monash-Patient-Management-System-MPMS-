from datetime import datetime

class Report:
    """
    A class to generate reports based on appointment data.
    This class provides methods to generate reports summarizing appointment reasons
    and the number of patients handled by each GP.
    """
    def __init__(self):
        pass 
    
    @staticmethod
    def generate_appt_reason_report(appointments, start_date=None, end_date=None):
        """
        Generates a report summarizing the number and percentage of appointments by reason.

        Args:
            appointments (list): A list of Appointment objects, each with a linked AppointmentSlot.
            start_date (str): Start date in "dd-mm-yyyy" format to filter the appointments. Defaults to None.
            end_date (str): End date in "dd-mm-yyyy" format to filter the appointments. Defaults to None.
        """
        
        # Filter appointments by date range if specified
        filtered_appts = appointments
        if start_date and end_date:
            start = datetime.strptime(start_date, "%d-%m-%Y")
            end = datetime.strptime(end_date, "%d-%m-%Y")
            
            filtered_appts = []
            for appointment in appointments:
                appt_date = datetime.strptime(appointment.get_slot().get_date(), "%d-%m-%Y")
                if start <= appt_date <= end:
                    filtered_appts.append(appointment)

        #Create dict to store appointment reason statistics
        appt_reason_statistics = {}
        for appointment in filtered_appts:
            reason = appointment.get_slot().get_reason_for_visit()
            if reason in appt_reason_statistics.keys():
                appt_reason_statistics[reason] = appt_reason_statistics[reason] + 1
            else:
                appt_reason_statistics[reason] = 1
        
        # Generate text report
        date_range_text = ""
        if start_date and end_date:
            date_range_text = f"Period: {start_date} to {end_date}"
        else:
            date_range_text = "Period: All Time"
            
        #Report formatting
        report_txt_data = []
        report_csv_data = [r"Appointment Reason,Number of Appointments,% of Total No of Appointments"+"\n"]
        for reason, number_of_appts in appt_reason_statistics.items():
            percentage_of_appts = number_of_appts/len(appointments) * 100

            reason_cell = reason.center(28)
            number_cell = str(number_of_appts).center(24)
            percent_cell = (str(round(percentage_of_appts,2)) + "%").center(32)
            report_txt_data.append(f"|{reason_cell}|{number_cell}|{percent_cell}|")

            report_csv_data.append(f"{reason},{number_of_appts},{percentage_of_appts}\n")

        report_txt_data = "\n".join(report_txt_data)
        total_appts = sum(number_of_appts for number_of_appts in appt_reason_statistics.values())
        txt_report = f"""
                           Automatically Generated Report
----------------------------------------------------------------------------------------

                 >> Report on Appointment Distribution by Reason <<
                                {date_range_text}
                    
                            Total Appointments: {total_appts}

|     Appointment Reason     | Number of Appointments |  % of Total No of Appointments |
----------------------------------------------------------------------------------------
{report_txt_data}

"""     
        return [txt_report, report_csv_data]
    

    @staticmethod
    def generate_gp_report(appointments, start_date=None, end_date=None):
        """
        Generates a report detailing how many patients each GP handled and the reasons for visits.

        Args:
            appointments (list): A list of Appointment objects, each with a linked AppointmentSlot.
            start_date (str): Start date in "dd-mm-yyyy" format to filter the appointments. Defaults to None.
            end_date (str): End date in "dd-mm-yyyy" format to filter the appointments. Defaults to None.

        """
        # Filter appointments by date range if specified
        filtered_appointments = appointments
        if start_date and end_date:
            start = datetime.strptime(start_date, "%d-%m-%Y")
            end = datetime.strptime(end_date, "%d-%m-%Y")
            
            filtered_appointments = []
            for appointment in appointments:
                appt_date = datetime.strptime(appointment.get_slot().get_date(), "%d-%m-%Y")
                if start <= appt_date <= end:
                    filtered_appointments.append(appointment)
        
        # Create dict to store GP statistics
        gp_statistics = {}
        
        # Process appointments
        for appointment in filtered_appointments:
            gp_name = appointment.get_slot().get_gp_name()
            clinic_suburb = appointment.get_slot().get_clinic_suburb()
            reason = appointment.get_slot().get_reason_for_visit()
            
            # Create a unique key for each GP+clinic combination
            key = f"{gp_name}|{clinic_suburb}"
            
            if key not in gp_statistics:
                gp_statistics[key] = {
                    "gp_name": gp_name,
                    "clinic_suburb": clinic_suburb,
                    "total_patients": 0,
                    "reasons": {}
                }
            
            gp_statistics[key]["total_patients"] += 1
            # Count the reasons for visits
            # If the reason already exists, increment its count, otherwise initialize it
            if reason in gp_statistics[key]["reasons"]:
                gp_statistics[key]["reasons"][reason] += 1
            else:
                gp_statistics[key]["reasons"][reason] = 1
        
        # Generate text report
        date_range_text = f"Period: {start_date} to {end_date}"
        
        report_txt_data = []
        report_csv_data = ["GP Name,Clinic Suburb,Total Patients,Appointment Reasons\n"]
        
        for key, data in gp_statistics.items():
            # Format reasons as a comma-separated list with counts
            reasons_list = []
            for reason, count in data["reasons"].items():
                reasons_list.append(f"{reason} ({count})")
            reasons_str = ", ".join(reasons_list)
            
            # Text report formatting
            gp_cell = data["gp_name"].center(20)
            suburb_cell = data["clinic_suburb"].center(20)
            patients_cell = str(data["total_patients"]).center(25)
            
            report_txt_data.append(f"| {gp_cell} | {suburb_cell} | {patients_cell} | {reasons_str} ")
            
            # CSV report data
            report_csv_data.append(f"{data['gp_name']},{data['clinic_suburb']},{data['total_patients']},\"{reasons_str}\"\n")
        
        report_txt_data = "\n".join(report_txt_data)
        total_appointments = sum(data["total_patients"] for data in gp_statistics.values())
        
        txt_report = f"""
                                                    Automatically Generated Report
---------------------------------------------------------------------------------------------------------------------------------------------------

                                         >> Report on Number of Patients Handled by Each GP <<
                                                            {date_range_text}
                
                                                        Total Appointments: {total_appointments}

---------------------------------------------------------------------------------------------------------------------------------------------------
|     GP Name          |  Clinic Suburb       |  Total no of Patients     |  Reason For Visit                 
---------------------------------------------------------------------------------------------------------------------------------------------------
{report_txt_data}

    """
        
        return [txt_report, report_csv_data]