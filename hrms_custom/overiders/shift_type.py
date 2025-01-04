import frappe
from hrms.hr.doctype.employee_checkin.employee_checkin import (
	calculate_working_hours,
	mark_attendance_and_link_log,
)
from frappe.utils import cint
from datetime import datetime, timedelta

def custom_get_attendance(self, logs):
    frappe.log_error("custom_get_attendance", logs)
    """Return attendance_status, working_hours, late_entry, early_exit, in_time, out_time
    for a set of logs belonging to a single shift.
    Assumptions:
    1. These logs belongs to a single shift, single employee and it's not in a holiday date.
    2. Logs are in chronological order
    """
    late_entry = early_exit = False
    total_working_hours, in_time, out_time = calculate_working_hours(
        logs, self.determine_check_in_and_check_out, self.working_hours_calculation_based_on
    )
    if (
        cint(self.enable_late_entry_marking)
        and in_time
        and in_time > logs[0].shift_start + timedelta(minutes=cint(self.late_entry_grace_period))
    ):
        late_entry = True

    if (
        cint(self.enable_early_exit_marking)
        and out_time
        and out_time < logs[0].shift_end - timedelta(minutes=cint(self.early_exit_grace_period))
    ):
        early_exit = True 

    if (
        self.working_hours_threshold_for_absent
        and total_working_hours < self.working_hours_threshold_for_absent
    ):
        return "Absent", total_working_hours, late_entry, early_exit, in_time, out_time

    if (
        self.working_hours_threshold_for_half_day
        and total_working_hours < self.working_hours_threshold_for_half_day
    ):
        return "Half Day", total_working_hours, late_entry, early_exit, in_time, out_time

    #custom code for Attendance validation
    try:
        if logs:
            employee = logs[0].get('employee')
            query = f""" select time
                from `tabEmployee Checkin` 
                Where EXTRACT(MONTH FROM time) = EXTRACT(MONTH FROM CURRENT_DATE)
                AND EXTRACT(YEAR FROM time) = EXTRACT(YEAR FROM CURRENT_DATE)
                AND employee = '{employee}'
                GROUP BY CAST(`time` AS DATE)
                ORDER BY creation DESC
                """
            result = frappe.db.sql(query, as_dict=1)

            threshold_time = logs[0].shift_start + timedelta(minutes=cint(self.late_entry_grace_period))
            # threshold_time = datetime.strptime(str(threshold_time), '%H:%M:%S')
            
            counter = 0
            for entry in result:
                if entry['time'].time() > threshold_time.time() and entry['time'].time() <= (threshold_time + timedelta(minutes=10)).time():
                    counter += 1
                
                elif entry['time'].date() == datetime.now().date() and entry['time'].time() > (threshold_time + timedelta(minutes=10)).time():
                    return "Half Day", total_working_hours, late_entry, early_exit, in_time, out_time

            if (counter > 3):
                return "Half Day", total_working_hours, late_entry, early_exit, in_time, out_time
            else:
                late_entry = False
    except Exception as e:
        frappe.log_error("attendance validation", e)

    if early_exit:
        return "Half Day", total_working_hours, late_entry, early_exit, in_time, out_time
    #end

    return "Present", total_working_hours, late_entry, early_exit, in_time, out_time