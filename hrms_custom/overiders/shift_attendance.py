import itertools
from datetime import datetime, timedelta

import frappe
from frappe.model.document import Document
from frappe.utils import cint, get_datetime, get_time, getdate

from erpnext.setup.doctype.employee.employee import get_holiday_list_for_employee
from erpnext.setup.doctype.holiday_list.holiday_list import is_holiday

from hrms.hr.doctype.attendance.attendance import mark_attendance
from hrms.hr.doctype.employee_checkin.employee_checkin import (
	calculate_working_hours,
	mark_attendance_and_link_log,
)
from hrms.hr.doctype.shift_assignment.shift_assignment import get_employee_shift, get_shift_details
from hrms.utils import get_date_range
from hrms.utils.holiday_list import get_holiday_dates_between

def process_auto_attendance(self):
    frappe.throw("working")
    return
    if (
        not cint(self.enable_auto_attendance)
        or not self.process_attendance_after
        or not self.last_sync_of_checkin
    ):
        return

    logs = self.get_employee_checkins()

    for key, group in itertools.groupby(logs, key=lambda x: (x["employee"], x["shift_start"])):
        single_shift_logs = list(group)
        attendance_date = single_shift_logs[0].shift_actual_start.date()
        employee = key[0]

        if not self.should_mark_attendance(employee, attendance_date):
            continue

        (
            attendance_status,
            working_hours,
            late_entry,
            early_exit,
            in_time,
            out_time,
        ) = self.get_attendance(single_shift_logs)

        mark_attendance_and_link_log(
            single_shift_logs,
            attendance_status,
            attendance_date,
            working_hours,
            late_entry,
            early_exit,
            in_time,
            out_time,
            self.name,
        )

    for employee in self.get_assigned_employees(self.process_attendance_after, True):
        self.mark_absent_for_dates_with_no_attendance(employee)