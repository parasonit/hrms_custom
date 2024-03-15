from hrms_custom.overiders.shift_type import custom_get_attendance
import frappe
from frappe import _
from datetime import datetime


def update_attendance(doc, method):
    if doc.docstatus == 1:
        query = f"""
            select name, employee, log_type, time, shift, shift_start, shift_end,
            shift_actual_start, shift_actual_end, device_id
            from `tabEmployee Checkin` 
            where name = "{doc.employee}" and time between "{doc.from_date}" and "{doc.to_date}"
        """
        checkin_logs = frappe.db.sql(query, as_dict=1)
        frappe.log_error("update_attendance", checkin_logs)
        shift_doc = frappe.get_doc("Shift Type", doc.shift_type)
        resp = custom_get_attendance(self=shift_doc, logs=checkin_logs)
        if resp:
            attendance = frappe.db.get_value('Attendance', {
                'employee': doc.employee, 
                'attendance_date': doc.from_date
            }, 'name')
            if attendance:
                frappe.db.set_value('Attendance', attendance, {
                    'status': resp[0],
                    'total_working_hours': resp[1],
                    'late_entry': resp[2],
                    'early_exit': resp[3],
                    'in_time': resp[4],
                    'out_time': resp[5]
                })
                frappe.db.commit()

def update_user_permission(doc, method):
    if frappe.db.exists("Employee", doc.name):
        leave_approver = frappe.db.get_value('Employee', doc.name, 'leave_approver')
        if leave_approver != doc.leave_approver:
            #remove old permission
            frappe.db.delete("User Permission", {
                "user": leave_approver,
                "allow": "Employee",
                "for_value": doc.name 
            })

            #insert User Permission
            insert_user_permission(doc)
    else:
        insert_user_permission(doc)

def insert_user_permission(doc):
    roles = frappe.get_roles(doc.leave_approver)
    if "HR Manager" in roles or "HR User" in roles:
        return
    else:
        doc = frappe.get_doc({
            'doctype': 'User Permission',
            "user": doc.leave_approver,
            "allow": "Employee",
            "for_value": doc.name,
            "apply_to_all_doctypes": 1
        })
        doc.insert()
        frappe.db.commit() 

def update_job_opening_date(doc, method):
    if doc.workflow_state == "Approved":
        doc.custom_open_on = frappe.utils.nowdate()

def validate_adhaar(doc, method):
    if doc.aadhar_number and not is_integer(doc.aadhar_number):
        frappe.throw(_("Aadhaar number must be integer."))
    elif doc.aadhar_number and (len(doc.aadhar_number) < 12 or len(doc.aadhar_number) > 12):
        frappe.throw(_("Aadhaar number must be 12 digits long."))

def validate_pan(doc, method):
    if doc.pan_number and (len(doc.pan_number) < 10 or len(doc.pan_number) > 10):
        frappe.throw(_("PAN number must be 10 digits long."))

def validate_uan(doc, method):
    if doc.pf_contribution != "Yes":
        return
    if doc.uan_number and (len(doc.uan_number) < 12 or len(doc.uan_number) > 12):
        frappe.throw(_("UAN number must be 12 digits long."))

def validate_pf(doc, method):
    if doc.pf_contribution != "Yes":
        return
    if doc.provident_fund_account and (len(doc.provident_fund_account) < 22 or len(doc.provident_fund_account) > 22):
        frappe.throw(_("PF number must be 22 digits long."))

def calculate_age(doc, method):
    today = datetime.today()
    dob = datetime.strptime(str(doc.date_of_birth), "%Y-%m-%d")  # Assuming DOB format is YYYY-MM-DD
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    frappe.log_error("age", age)
    doc.vay = age

# def update_kra_goal_score(doc, method):
#     if doc.workflow_state == "Saved":
#         for goal in doc.goals:
#             for self_kra in doc.custom_self_appraisal_kra:
#                 if self_kra.kra == goal.kra:
#                     self_kra.custom_self_score = self_kra.score
#                     goal.custom_self_score = self_kra.score
#                     break
        

def is_integer(adhaar):
    try:
        int(adhaar)
        return True
    except ValueError:
        return False
    
def update_reporting_manager(doc, method):
    report_manager = frappe.db.get_value('Employee', {'user_id': frappe.session.user}, ['leave_approver'])
    if report_manager and doc.workflow_state == "Draft":
        doc.custom_reporting_manager = report_manager

def update_employee(doc,method):
    employee = frappe.db.get_value('Employee', {'user_id': frappe.session.user}, ['name'])
    if employee and doc.workflow_state == "Draft":
        doc.custom_employee = employee

def validate_job_no(doc, method):
    if doc.custom_position_type == "New" and doc.custom_no_of_position < 1:
        frappe.throw(
			_("Number of positions cannot be 0. Setting it to at least 1."),
			title=_("Mandatory Field")
		)

def update_job_applicant_status(doc, method):
    job_applicant = None
    if doc.doctype == "Communication" and doc.reference_doctype == "Job Offer":
        job_applicant = frappe.db.get_value('Job Offer', doc.reference_name, 'job_applicant')
        status = "Job Ofer Sent"
    elif doc.doctype == "Job Offer" and doc.workflow_state == "Approved":
        job_applicant = doc.job_applicant
        status = "Job Offer Approved"

    if job_applicant:
        frappe.db.set_value('Job Applicant', job_applicant, 'status', status)
        frappe.db.commit()