from hrms_custom.overiders.shift_type import custom_get_attendance
import frappe
from frappe import _
from datetime import datetime
from frappe.model.naming import make_autoname
from frappe.model.mapper import get_mapped_doc
from frappe.utils import get_url_to_form
from frappe.utils.nestedset import get_descendants_of
import json

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
        if checkin_logs:
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
    if "HR Manager" in roles or "HR User" in roles or "HR HOD" in roles:
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
    doc.vay = age


def calculate_age_daily():
    frappe.log_error("Age Scheduler Working")
    employees = frappe.db.get_list('Employee',
        filters={
            'status': 'Active'
        },
        fields=['name', 'date_of_birth']
    )
    if len(employees) > 20:
        frappe.enqueue(update_age, employees=employees, queue="long")
    
def update_age(employees):
    for emp in employees:
        today = datetime.today()
        dob = datetime.strptime(str(emp.get('date_of_birth')), "%Y-%m-%d")  # Assuming DOB format is YYYY-MM-DD
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        frappe.db.set_value('Employee', emp.get('name'), 'vay', age)
        frappe.db.commit()

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
    if not report_manager:
        frappe.throw(
			_("Reporting Manager is Missing. Contact to your HR Admin"),
			title=_("Mandatory Field")
		)
    if report_manager and doc.workflow_state == "Draft":
        doc.custom_reporting_manager = report_manager

def update_employee(doc,method):
    employee = frappe.db.get_value('Employee', {'user_id': frappe.session.user}, ['name'])
    if not employee:
        frappe.throw(
			_("Logged In Employee is Missing. Contact to your HR Admin"),
			title=_("Mandatory Field")
		)
    if employee and not doc.custom_employee and doc.workflow_state == "Draft":
        doc.custom_employee = employee

def validate_job_no(doc, method):
    if doc.custom_position_type == "New" and doc.custom_no_of_position < 1:
        frappe.throw(
			_("Number of positions cannot be 0. Setting it to at least 1."),
			title=_("Mandatory Field")
		)

def update_job_applicant_status(doc, method):
    job_applicant = None
    if method == "on_trash":
        job_applicant = doc.job_applicant
        status = "Open"
    elif method == "validate":
        if doc.doctype == "Communication" and doc.reference_doctype == "Job Offer":
            job_applicant = frappe.db.get_value('Job Offer', doc.reference_name, 'job_applicant')
            status = "Job Offer Sent"
        elif doc.doctype == "Job Offer" and doc.workflow_state == "Approved":
            job_applicant = doc.job_applicant
            status = "Job Offer Approved"

    if job_applicant:
        frappe.db.set_value('Job Applicant', job_applicant, 'status', status)
        frappe.db.commit()

def update_appraisal_name(doc, method):
    name = doc.employee + "-APR-" + doc.appraisal_cycle + "-"
    doc.name = make_autoname(name + ".####")

def calculate_weightage(doc, method):
    total_weightage = 0
    for kra in doc.goals:
        total_weightage += kra.per_weightage
    
    doc.custom_total_weightage = total_weightage

def map_employee(doc, method):
    employee = frappe.db.get_value('Employee', {'company_email': doc.email}, ['name'])
    if employee:
        frappe.db.set_value('Employee', employee, 'user_id', doc.email)
        frappe.db.commit()

        #update euser permissions for employee
        employee_user_permission(doc, employee)

        #update user permissions for company
        company_user_permission(doc)
        
        doc.role_profile_name = "Employee"
        doc.save()


def employee_user_permission(doc, employee):
    user_perm = frappe.new_doc("User Permission")
    user_perm.user = doc.email
    user_perm.allow = "Employee"
    user_perm.for_value = employee
    user_perm.apply_to_all_doctypes = 1
    user_perm.insert(ignore_permissions=True)
    frappe.db.commit()

def company_user_permission(doc):
    user_perm = frappe.new_doc("User Permission")
    user_perm.user = doc.email
    user_perm.allow = "Company"
    user_perm.for_value = "Parason Machinery India Pvt Ltd"
    user_perm.apply_to_all_doctypes = 1
    user_perm.insert(ignore_permissions=True)
    frappe.db.commit()


@frappe.whitelist()
def make_job_opening(source_name, designation, target_doc=None):
    # Check if job opening already exists
    job_opening_exists = frappe.db.exists('Job Opening', {'job_title': designation})

    if job_opening_exists:
        return {'message': f'Job opening already exists: <a href="{get_url_to_form("Job Opening", job_opening_exists)}">{job_opening_exists}</a>'}
    else:
        # Set missing values for job opening document
        def set_missing_values(source, target):
            target.job_title = source.designation
            target.status = "Open"
            target.currency = frappe.db.get_value("Company", source.company, "default_currency")
            target.lower_range = source.expected_compensation
            target.description = source.description
        
        # Create job opening document
        doc = get_mapped_doc(
            "Job Requisition",
            source_name,
            {
                "Job Requisition": {
                    "doctype": "Job Opening",
                },
                "field_map": {
                    "designation": "designation",
                    "name": "job_requisition",
                    "department": "department",
                    "no_of_positions": "vacancies",
                },
            },
            target_doc,
            set_missing_values,
        )
        try:
            # Save and commit the document
            doc.insert()
            doc.save()
            frappe.db.commit()
            return {'message': f'Job opening created: <a href="{get_url_to_form("Job Opening", doc.name)}">{doc.name}</a>'}
        except Exception as e:
            return {'message': f'Error creating job opening: {str(e)}'}



@frappe.whitelist()
def get_total_cost(designation, company, department=None):
    company_set = get_descendants_of("Company", company) + [company]

    sql_query = """
        SELECT SUM(ctc)
        FROM `tabEmployee`
        WHERE designation = %s AND status = 'Active' AND company IN %s
    """
    
    if department:
        sql_query += " AND department = %s"
        filters = (designation, tuple(company_set), department)
    else:
        filters = (designation, tuple(company_set))

    total_cost = frappe.db.sql(sql_query, filters)[0][0] or 0

    return total_cost



@frappe.whitelist()
def render_appointment_template( appt_template,doc):
	doc = json.loads(doc) if isinstance(doc, str) else doc
	template = frappe.get_doc("Appointment Letter Template",appt_template)
	return frappe.render_template(template.custom_template_format, doc) if template.custom_template_format else ""


def update_holiday_list_for_employees(doc,method):
    old_doc = doc.get_doc_before_save()
    if doc.holiday_list != old_doc.holiday_list:
        employees = frappe.db.get_list('Employee',
                                       filters={'default_shift': doc.name},
                                       fields=['name']
                                       )
        for employee in employees:
            frappe.db.set_value('Employee', employee.name, 'holiday_list', doc.holiday_list)
      
def update_job_opening_status(doc, method):
    query = """
        SELECT jo.name AS job_opening, COUNT(ja.name) AS total_accepted_applicants
        FROM `tabJob Opening` jo
        LEFT JOIN `tabJob Applicant` ja ON jo.name = ja.job_title
        WHERE ja.status = 'Accepted'
        AND ja.name IN (
            SELECT te.job_applicant
            FROM `tabEmployee` te
        )
        GROUP BY jo.name;
    """

    data = frappe.db.sql(query, as_dict=1)
    for jo in data:
        if jo.get('job_opening'):
            total_vacancies = frappe.db.get_value("Job Opening", jo.get('job_opening'), "vacancies")
            if total_vacancies == jo.get('total_accepted_applicants'):
                frappe.db.set_value('Job Opening', jo.get('job_opening'), 'status', 'Closed')
                frappe.db.commit()

