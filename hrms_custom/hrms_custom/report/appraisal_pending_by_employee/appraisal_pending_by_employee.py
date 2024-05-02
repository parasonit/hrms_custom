# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
 

def execute(filters: dict = None) -> tuple:
	filters = frappe._dict(filters or {})
	columns = get_columns()
	data = get_data(filters)

	return columns, data


def get_columns() -> list[dict]:
	return [
		{
			"fieldname": "employee",
			"fieldtype": "Link",
			"label": _("Employee"),
			"options": "Employee",
			"width": 250,
		},
		{"fieldname": "employee_name", "fieldtype": "Data", "label": _("Employee Name"), "width": 250},
		{
			"fieldname": "branch",
			"fieldtype": "Link",
			"label": _("Branch"),
			"options": "Branch",
			"width": 150,
		},
		{
			"fieldname": "designation",
			"fieldtype": "Link",
			"label": _("Designation"),
			"options": "Designation",
			"width": 200,
		},
		{
			"fieldname": "department",
			"fieldtype": "Link",
			"label": _("Department"),
			"options": "Department",
			"width": 200,
		},
	]

def get_data(filters: dict = None) -> list[dict]:
    roles = frappe.get_roles(frappe.session.user)

    query = """
        select name as employee, employee_name, branch, designation, department
        from `tabEmployee` 
        where status = "Active"
        AND custom_pms_eligibility != "Not Applicable"
    """
    
    if any(role in roles for role in ["System Manager", "HR Manager", "HR User", "HR HOD"]):
        pass
    
    elif "Leave Approver" in roles:
        logged_in_employee = frappe.db.get_value('Employee', {'user_id': frappe.session.user}, ['name'])
        query += f""" AND reports_to = "{logged_in_employee}" """
    
    if filters and filters.get("appraisal_cycle"):
        query += f""" AND employee not in (select distinct employee from `tabAppraisal` where appraisal_cycle = "{filters.get("appraisal_cycle")}" and workflow_state not in ("Draft")) """
    else:
        query += """ AND employee not in (select distinct employee from `tabAppraisal` where workflow_state not in ("Draft")) """

    data = frappe.db.sql(query, as_dict=1)
    
    return data


